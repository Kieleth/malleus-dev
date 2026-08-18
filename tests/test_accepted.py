"""Accepted graph binding, atomic materialization, and bitemporal replay gates."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from malleus.accepted import (
    AcceptedGraphError,
    AcceptedGraphProjector,
    AcceptedGraphView,
    acceptance_result_head,
    accepted_application_record,
    candidate_artifact_digest,
    candidate_artifact_fields,
    candidate_manifest,
    candidate_manifest_hash,
    graph_base_artifact_digest,
    graph_base_metadata,
    temporal_write,
)
from malleus.assent import EventType, ProtocolError, ProtocolLedger, make_record
from malleus.control import (
    epistemic_policy_digest,
    evaluate_epistemic_policy,
    monitor_specification_digest,
)
from malleus.kg import KnowledgeGraph
from malleus.ledger import canonical_json, event_hash, record_hash
from malleus.logic import LogicCheckResult, logic_contract_digest
from malleus.ontology import OntologyRegistry
from malleus.staging import ProposedOperation, stage_subgraph
from malleus.valid_time import ValidTime


ASSENT_SCHEMA = Path(__file__).parent.parent / "ontology" / "assent.yaml"
OPAQUE_SNAPSHOT = "sha256:" + "1" * 64
ARTIFACT_BODY = "sha256:" + "2" * 64
VALID_0 = "2026-01-01T00:00:00+00:00"
VALID_1 = "2026-02-01T00:00:00+00:00"
VALID_2 = "2026-03-01T00:00:00+00:00"
EXACT_0 = ValidTime.exact(VALID_0)
EXACT_1 = ValidTime.exact(VALID_1)
EXACT_2 = ValidTime.exact(VALID_2)


def at(minute: int) -> str:
    return f"2026-08-12T08:{minute:02d}:00Z"


@pytest.fixture
def registry(tmp_path):
    domain = tmp_path / "accepted_test.yaml"
    domain.write_text(
        """id: https://malleus.dev/schema/accepted-test
name: accepted_test
version: 0.1.0
imports:
  - assent
classes:
  TestNode:
    is_a: Entity
  TestFlaggedNode:
    is_a: Entity
    slots:
      - is_event
  TestEvent:
    is_a: Event
  TestSignal:
    is_a: Signal
  TestLink:
    is_a: Relation
    slot_usage:
      relation_type:
        equals_string: TEST_LINK
      source_id:
        range: TestNode
      target_id:
        range: TestNode
slots:
  is_event:
    range: boolean
""",
        encoding="utf-8",
    )
    return OntologyRegistry(domain, import_map={"assent": ASSENT_SCHEMA})


@pytest.fixture
def ledger(tmp_path, registry):
    return ProtocolLedger(
        tmp_path / "accepted.jsonl",
        registry,
        accepted_graph_base=KnowledgeGraph(registry),
    )


def anchor(ledger: ProtocolLedger) -> None:
    ledger.append_event(
        event_id="event:anchor",
        event_type=EventType.EXTERNAL_SNAPSHOT_ANCHORED,
        transaction_time=at(0),
        actor_id="actor:system",
        payload={
            "snapshot_id": "snapshot:research",
            "snapshot_hash": OPAQUE_SNAPSHOT,
            "source": "external research ledger",
            "record_count": 10,
            "opaque": True,
        },
    )


def append_artifact(
    ledger: ProtocolLedger,
    record_type: str,
    artifact_id: str,
    kind: str,
    minute: int,
    *,
    artifact_hash: str,
    source_record_ids=(),
    **fields,
) -> dict:
    event_id = f"event:{artifact_id}"
    record = make_record(
        record_type,
        event_id=event_id,
        generated_at=at(minute),
        actor_id="actor:system",
        role="registrar",
        source_record_ids=source_record_ids,
        id=artifact_id,
        artifact_kind=kind,
        artifact_version="1",
        artifact_hash=artifact_hash,
        **fields,
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ARTIFACT_RECORDED,
        transaction_time=at(minute),
        actor_id="actor:system",
        payload={"artifact_type": record_type, "artifact": record},
    )
    return record


def register_graph_base(
    ledger: ProtocolLedger,
    minute: int = 1,
    *,
    intervals=(),
) -> dict:
    base = ledger._accepted_graph_base
    metadata = graph_base_metadata(base, list(intervals))
    artifact_id = "artifact:graph-base"
    fields = {
        "graph_schema_version": "2",
        "graph_ontology_hash": "sha256:" + base.registry.content_hash(),
        "base_state_digest": base.state_digest(),
        "base_record_metadata": metadata,
        "base_record_count": len(intervals),
    }
    return append_artifact(
        ledger,
        "GraphBaseArtifact",
        artifact_id,
        "GRAPH_BASE",
        minute,
        artifact_hash=graph_base_artifact_digest(
            artifact_id=artifact_id,
            artifact_version="1",
            graph_ontology_hash=fields["graph_ontology_hash"],
            base_state_digest=fields["base_state_digest"],
            base_record_metadata=metadata,
        ),
        **fields,
    )


def add_logic_artifacts(ledger: ProtocolLedger, rules: dict, minute: int = 3) -> dict[str, dict]:
    """Register the pinned logic contract and the LOGICAL monitor that reads it."""
    ontology_hash = "sha256:" + ledger.registry.content_hash()
    contract_id = "artifact:logic-contract"
    contract_fields = {
        "logic_contract_schema_version": "1",
        "ontology_hash": ontology_hash,
        "fact_contract_version": "2",
        "ruleset_id": rules["id"],
        "ruleset_version": "1",
        "ruleset_record_hash": rules["content_hash"],
        "ruleset_artifact_hash": rules["artifact_hash"],
        "rule_ids": ["RULE_ONE"],
        "timeout_seconds": 5,
    }
    contract = append_artifact(
        ledger,
        "LogicContractArtifact",
        contract_id,
        "LOGIC_CONTRACT",
        minute,
        artifact_hash=logic_contract_digest(
            schema_version="1",
            contract_id=contract_id,
            contract_version="1",
            ontology_hash=ontology_hash,
            fact_contract_version="2",
            ruleset_id=rules["id"],
            ruleset_version="1",
            rule_ids=["RULE_ONE"],
            timeout_seconds=5,
            ruleset_hash=rules["artifact_hash"],
        ),
        source_record_ids=[rules["id"]],
        **contract_fields,
    )
    monitor_id = "artifact:logic-monitor"
    monitor_fields = {
        "monitor_schema_version": "1",
        "assessment_kind": "LOGICAL",
        "monitor_implementation_hash": "sha256:" + "4" * 64,
        "input_artifact_ids": [contract["id"]],
        "input_artifact_record_hashes": [contract["content_hash"]],
    }
    monitor = append_artifact(
        ledger,
        "MonitorSpecificationArtifact",
        monitor_id,
        "MONITOR_SPECIFICATION",
        minute,
        artifact_hash=monitor_specification_digest(
            schema_version="1",
            monitor_id=monitor_id,
            monitor_version="1",
            assessment_kind="LOGICAL",
            implementation_hash=monitor_fields["monitor_implementation_hash"],
            input_artifact_ids=monitor_fields["input_artifact_ids"],
            input_artifact_record_hashes=monitor_fields["input_artifact_record_hashes"],
        ),
        source_record_ids=[contract["id"]],
        **monitor_fields,
    )
    return {"logic_contract": contract, "logic_monitor": monitor}


def setup_policy(
    ledger: ProtocolLedger,
    *,
    violation_verdict="REJECT",
    include_logic: bool = False,
) -> dict[str, dict]:
    rules = append_artifact(
        ledger,
        "ProtocolArtifact",
        "artifact:rules",
        "RULE_SET",
        2,
        artifact_hash=ARTIFACT_BODY,
    )
    monitor_id = "artifact:type-monitor"
    monitor_fields = {
        "monitor_schema_version": "1",
        "assessment_kind": "TYPE",
        "monitor_implementation_hash": "sha256:" + "3" * 64,
        "input_artifact_ids": [],
        "input_artifact_record_hashes": [],
    }
    monitor = append_artifact(
        ledger,
        "MonitorSpecificationArtifact",
        monitor_id,
        "MONITOR_SPECIFICATION",
        3,
        artifact_hash=monitor_specification_digest(
            schema_version="1",
            monitor_id=monitor_id,
            monitor_version="1",
            assessment_kind="TYPE",
            implementation_hash=monitor_fields["monitor_implementation_hash"],
            input_artifact_ids=[],
            input_artifact_record_hashes=[],
        ),
        **monitor_fields,
    )
    extra = add_logic_artifacts(ledger, rules) if include_logic else {}
    ordered = sorted(
        [monitor, *([extra["logic_monitor"]] if include_logic else [])],
        key=lambda item: item["id"],
    )
    required_ids = [item["id"] for item in ordered]
    required_hashes = [item["content_hash"] for item in ordered]
    policy_id = "artifact:policy"
    policy_fields = {
        "policy_schema_version": "1",
        "ruleset_id": rules["id"],
        "ruleset_record_hash": rules["content_hash"],
        "ruleset_artifact_hash": rules["artifact_hash"],
        "required_monitor_ids": required_ids,
        "required_monitor_record_hashes": required_hashes,
        "violation_verdicts": [violation_verdict] * len(ordered),
        "unknown_verdicts": ["DEFER"] * len(ordered),
        "control_precedence": ["REJECT", "CONTEST", "DEFER"],
    }
    policy = append_artifact(
        ledger,
        "EpistemicPolicyArtifact",
        policy_id,
        "EPISTEMIC_POLICY",
        4,
        artifact_hash=epistemic_policy_digest(
            schema_version="1",
            policy_id=policy_id,
            policy_version="1",
            ruleset_id=rules["id"],
            ruleset_record_hash=rules["content_hash"],
            ruleset_artifact_hash=rules["artifact_hash"],
            required_monitor_ids=required_ids,
            required_monitor_record_hashes=required_hashes,
            violation_verdicts=policy_fields["violation_verdicts"],
            unknown_verdicts=policy_fields["unknown_verdicts"],
            control_precedence=["REJECT", "CONTEST", "DEFER"],
        ),
        source_record_ids=[rules["id"], *required_ids],
        **policy_fields,
    )
    return {"rules": rules, "monitor": monitor, "policy": policy, **extra}


def register_candidate(
    ledger: ProtocolLedger,
    graph_base: dict,
    writes,
    *,
    suffix: str,
    minute: int,
    mutate=None,
    recompute_artifact_hash: bool = False,
) -> dict:
    projection = ledger.replay()
    artifact_id = f"artifact:candidate:{suffix}"
    fields, _ = candidate_artifact_fields(
        projection.accepted_graph,
        writes,
        graph_base_id=graph_base["id"],
        graph_base_hash=graph_base["content_hash"],
        base_acceptance_head=projection.acceptance_head,
        base_materialization_head=projection.materialization_head,
    )
    artifact_hash = candidate_artifact_digest(
        artifact_id=artifact_id,
        artifact_version="1",
        **fields,
    )
    if mutate is not None:
        mutate(fields)
    if recompute_artifact_hash:
        artifact_hash = candidate_artifact_digest(
            artifact_id=artifact_id,
            artifact_version="1",
            **fields,
        )
    return append_artifact(
        ledger,
        "CandidateSubgraphArtifact",
        artifact_id,
        "CANDIDATE_SUBGRAPH",
        minute,
        artifact_hash=artifact_hash,
        source_record_ids=[graph_base["id"]],
        **fields,
    )


def propose(
    ledger: ProtocolLedger,
    artifacts: dict[str, dict],
    candidate: dict,
    *,
    suffix: str,
    minute: int,
    mutate=None,
) -> dict:
    event_id = f"event:proposal:{suffix}"
    claim = make_record(
        "ClaimVersion",
        event_id=event_id,
        generated_at=at(minute),
        actor_id="actor:proposer",
        role="proposer",
        id=f"claim:{suffix}",
        claim_key=f"claim-key:{suffix}",
        revision=1,
        revises_claim_version_id=None,
        statement=f"Candidate {suffix} is proposed.",
        domain_valid_from=EXACT_0.as_dict(),
        domain_valid_to=None,
        dependency_ids=[],
    )
    proposal = make_record(
        "ProposedSubgraph",
        event_id=event_id,
        generated_at=at(minute),
        actor_id="actor:proposer",
        role="proposer",
        source_record_ids=[artifacts["policy"]["id"], candidate["id"]],
        id=f"proposal:{suffix}",
        proposal_key=f"proposal-key:{suffix}",
        revision=1,
        revises_proposal_id=None,
        base_acceptance_head=ledger.replay().acceptance_head,
        epistemic_policy_id=artifacts["policy"]["id"],
        epistemic_policy_hash=artifacts["policy"]["content_hash"],
        member_content_hashes=[claim["content_hash"]],
        claim_version_ids=[claim["id"]],
        evidence_ids=[],
        evidence_assertion_ids=[],
        action_proposal_ids=[],
        candidate_artifact_id=candidate["id"],
        candidate_artifact_hash=candidate["content_hash"],
        candidate_digest=candidate["candidate_digest"],
    )
    if mutate is not None:
        mutate(proposal)
        proposal["content_hash"] = record_hash("ProposedSubgraph", proposal)
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.PROPOSAL_RECORDED,
        transaction_time=at(minute),
        actor_id="actor:proposer",
        payload={
            "proposal": proposal,
            "members": [{"record_type": "ClaimVersion", "record": claim}],
        },
    )
    return proposal


def assess(
    ledger: ProtocolLedger,
    artifacts: dict[str, dict],
    proposal: dict,
    *,
    suffix: str,
    minute: int,
    outcome: str = "SATISFIED",
) -> dict:
    event_id = f"event:assessment:{suffix}"
    monitor = artifacts["monitor"]
    record = make_record(
        "TypeAssessment",
        event_id=event_id,
        generated_at=at(minute),
        actor_id="actor:monitor",
        role="type-monitor",
        source_record_ids=[proposal["id"], monitor["id"]],
        id=f"assessment:{suffix}",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        assessment_kind="TYPE",
        assessment_outcome=outcome,
        monitor_id=monitor["id"],
        monitor_version="1",
        monitor_hash=monitor["content_hash"],
        monitor_failure_id=None,
        input_record_ids=[proposal["id"]],
        reason_codes=["TYPE_RESULT"],
        rationale="The typed candidate completed validation.",
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=at(minute),
        actor_id="actor:monitor",
        payload={"assessment_type": "TypeAssessment", "assessment": record},
    )
    return record


def record_logic_check(
    ledger: ProtocolLedger,
    artifacts: dict[str, dict],
    proposal: dict,
    candidate: dict,
    *,
    suffix: str,
    minute: int,
    translated_record_ids: tuple[str, ...] = ("node:one",),
) -> dict:
    """Record one LogicCheckRecord bound to the supplied candidate's digests."""
    event_id = f"event:logic-check:{suffix}"
    timestamp = at(minute)
    result = LogicCheckResult(
        candidate_digest=candidate["candidate_digest"],
        base_state_digest=candidate["base_state_digest"],
        candidate_state_digest=candidate["candidate_state_digest"],
        context_state_digests=(),
        ontology_hash=candidate["graph_ontology_hash"],
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
        translated_record_ids=translated_record_ids,
        checked_rule_ids=("RULE_ONE",),
        violations=(),
    )
    check, witnesses = result.to_protocol_records(
        check_id=f"logic-check:{suffix}",
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
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.LOGIC_CHECK_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"check": check, "witnesses": list(witnesses)},
    )
    return check


def record_logical_assessment(
    ledger: ProtocolLedger,
    artifacts: dict[str, dict],
    proposal: dict,
    check: dict,
    *,
    suffix: str,
    minute: int,
) -> dict:
    event_id = f"event:logical-assessment:{suffix}"
    timestamp = at(minute)
    assessment = make_record(
        "LogicalAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role="logic-monitor",
        source_record_ids=sorted({
            proposal["id"],
            artifacts["logic_monitor"]["id"],
            check["id"],
            artifacts["logic_contract"]["id"],
            artifacts["rules"]["id"],
        }),
        id=f"assessment:logical:{suffix}",
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
        rationale="The pinned logic check completed against this candidate.",
        checked_rule_ids=check["checked_rule_ids"],
        violated_rule_ids=check["violated_rule_ids"],
        logic_check_record_ids=[check["id"]],
        logic_contract_id=artifacts["logic_contract"]["id"],
        logic_contract_record_hash=artifacts["logic_contract"]["content_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_hash=artifacts["rules"]["content_hash"],
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:monitor",
        payload={"assessment_type": "LogicalAssessment", "assessment": assessment},
    )
    return assessment


def transition(event_id, timestamp, proposal_id, decision_id, target, sequence):
    return make_record(
        "TransitionRecord",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:reviewer",
        role="state-controller",
        source_record_ids=[decision_id],
        id=f"transition:{proposal_id}",
        transition_subject_id=proposal_id,
        from_state="PROPOSED",
        to_state=target,
        triggering_record_id=decision_id,
        ledger_event_id=event_id,
        sequence=sequence,
        transition_time=timestamp,
    )


def decide(
    ledger: ProtocolLedger,
    artifacts: dict[str, dict],
    proposal: dict,
    candidate: dict,
    assessment: dict,
    *,
    suffix: str,
    minute: int,
    include_application: bool = True,
    application_id: str | None = None,
    extra_assessments: list[dict] | None = None,
    mutate_decision=None,
    mutate_application=None,
) -> dict:
    event_id = f"event:decision:{suffix}"
    timestamp = at(minute)
    assessments = [assessment, *(extra_assessments or [])]
    monitors = {
        item["id"]: item
        for item in artifacts.values()
        if item.get("artifact_kind") == "MONITOR_SPECIFICATION"
    }
    evaluation = evaluate_epistemic_policy(
        artifacts["policy"],
        monitors,
        assessments,
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
    )
    application_id = (
        application_id or f"application:{suffix}"
        if include_application
        else None
    )
    decision = make_record(
        "EpistemicDecision",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:reviewer",
        role="epistemic-controller",
        source_record_ids=sorted({
            proposal["id"],
            artifacts["policy"]["id"],
            artifacts["rules"]["id"],
            candidate["id"],
            *(item["id"] for item in assessments),
        }),
        id=f"decision:{suffix}",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        epistemic_verdict=evaluation.verdict,
        assessment_ids=list(evaluation.assessment_ids),
        triggered_assessment_ids=list(evaluation.triggered_assessment_ids),
        policy_evaluation_hash=evaluation.evaluation_hash,
        evidence_assertion_ids=[],
        request_ids=[],
        claim_revision_ids=[],
        policy_id=artifacts["policy"]["id"],
        policy_hash=artifacts["policy"]["content_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_hash=artifacts["rules"]["content_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The policy selected the recorded verdict.",
        candidate_artifact_id=candidate["id"],
        candidate_artifact_hash=candidate["content_hash"],
        candidate_digest=candidate["candidate_digest"],
        accepted_application_id=application_id,
    )
    if mutate_decision is not None:
        mutate_decision(decision)
        decision["content_hash"] = record_hash("EpistemicDecision", decision)
    projection = ledger.replay()
    result_head = acceptance_result_head(
        previous_acceptance_head=projection.acceptance_head,
        proposal_content_hash=proposal["content_hash"],
        decision_content_hash=decision["content_hash"],
        revision_content_hashes=[],
    )
    application = None
    if include_application:
        application = accepted_application_record(
            application_id=application_id,
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:reviewer",
            role="graph-materializer",
            proposal=proposal,
            decision=decision,
            candidate=candidate,
            previous_acceptance_head=projection.acceptance_head,
            result_acceptance_head=result_head,
            previous_materialization_head=projection.materialization_head,
        )
        if mutate_application is not None:
            mutate_application(application)
            application["content_hash"] = record_hash(
                "AcceptedGraphApplication",
                application,
            )
    target = {
        "ACCEPT": "ACCEPTED",
        "REJECT": "REJECTED",
        "DEFER": "DEFERRED",
        "CONTEST": "CONTESTED",
    }[evaluation.verdict]
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.EPISTEMIC_DECIDED,
        transaction_time=timestamp,
        actor_id="actor:reviewer",
        payload={
            "decision": decision,
            "requests": [],
            "revisions": [],
            "application": application,
            "transition": transition(
                event_id,
                timestamp,
                proposal["id"],
                decision["id"],
                target,
                projection.event_count + 1,
            ),
        },
    )
    return decision


def prepared(ledger, *, write, suffix="one", outcome="SATISFIED", include_logic=False):
    anchor(ledger)
    graph_base = register_graph_base(ledger)
    artifacts = setup_policy(ledger, include_logic=include_logic)
    candidate = register_candidate(
        ledger,
        graph_base,
        [write],
        suffix=suffix,
        minute=5,
    )
    proposal = propose(ledger, artifacts, candidate, suffix=suffix, minute=6)
    assessment = assess(
        ledger,
        artifacts,
        proposal,
        suffix=suffix,
        minute=7,
        outcome=outcome,
    )
    if include_logic:
        check = record_logic_check(
            ledger,
            artifacts,
            proposal,
            candidate,
            suffix=suffix,
            minute=7,
        )
        artifacts["logic_check"] = check
        artifacts["logical_assessment"] = record_logical_assessment(
            ledger,
            artifacts,
            proposal,
            check,
            suffix=suffix,
            minute=8,
        )
    return graph_base, artifacts, candidate, proposal, assessment


def node_write(node_id="node:one", *, valid_from=EXACT_0, valid_to=None, supersedes=None):
    return temporal_write(
        ProposedOperation.entity("TestNode", node_id, {"name": node_id}),
        valid_from=valid_from,
        valid_to=valid_to,
        supersedes_record_id=supersedes,
    )


def test_candidate_manifest_binds_order_payload_and_temporal_envelope():
    first = node_write("node:one")
    second = node_write("node:two", valid_from=EXACT_1)
    original = candidate_manifest([first, second])
    reversed_manifest = candidate_manifest([second, first])
    changed_time = candidate_manifest([first, node_write("node:two", valid_from=EXACT_2)])
    assert candidate_manifest_hash(original) != candidate_manifest_hash(reversed_manifest)
    assert candidate_manifest_hash(original) != candidate_manifest_hash(changed_time)
    with pytest.raises(AcceptedGraphError, match="precision-aware object"):
        node_write(valid_from="2026-01-01T00:00:00Z")


def test_candidate_manifest_v1_exact_time_path_is_dead():
    parsed = json.loads(candidate_manifest([node_write()]))
    parsed["schema_version"] = "1"
    with pytest.raises(AcceptedGraphError, match="unsupported candidate manifest schema '1'"):
        candidate_manifest_hash(canonical_json(parsed))


def test_graph_base_v1_exact_time_path_is_dead(registry):
    graph = KnowledgeGraph(registry)
    metadata = graph_base_metadata(graph, [])
    parsed = json.loads(metadata)
    parsed["schema_version"] = "1"
    with pytest.raises(AcceptedGraphError, match="unsupported graph base schema '1'"):
        graph_base_artifact_digest(
            artifact_id="artifact:graph-base:v1",
            artifact_version="1",
            graph_ontology_hash="sha256:" + registry.content_hash(),
            base_state_digest=graph.state_digest(),
            base_record_metadata=canonical_json(parsed),
        )


def test_candidate_artifact_recomputes_semantics_before_append(ledger):
    anchor(ledger)
    graph_base = register_graph_base(ledger)
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="candidate semantic hash mismatch"):
        register_candidate(
            ledger,
            graph_base,
            [node_write()],
            suffix="tampered",
            minute=5,
            mutate=lambda fields: fields.update(candidate_digest="sha256:" + "9" * 64),
        )
    assert ledger.path.read_bytes() == before


@pytest.mark.parametrize("tamper", ["payload", "order"])
def test_candidate_manifest_tamper_fails_after_record_hash_recomputation(ledger, tamper):
    anchor(ledger)
    graph_base = register_graph_base(ledger)

    def mutate(fields):
        manifest = json.loads(fields["candidate_manifest"])
        if tamper == "payload":
            manifest["writes"][0]["operation"]["properties"]["name"] = "tampered"
        else:
            manifest["writes"].reverse()
        fields["candidate_manifest"] = canonical_json(manifest)
        fields["candidate_manifest_hash"] = candidate_manifest_hash(
            fields["candidate_manifest"]
        )

    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="candidate candidate_digest mismatch"):
        register_candidate(
            ledger,
            graph_base,
            [node_write("node:one"), node_write("node:two")],
            suffix=f"manifest-{tamper}",
            minute=5,
            mutate=mutate,
            recompute_artifact_hash=True,
        )
    assert ledger.path.read_bytes() == before


@pytest.mark.parametrize(
    "field,message",
    [
        ("graph_ontology_hash", "ontology differs"),
        ("base_acceptance_head", "stale base_acceptance_head"),
        ("base_materialization_head", "stale base_materialization_head"),
        ("base_state_digest", "stale base_state_digest"),
        ("candidate_digest", "candidate candidate_digest mismatch"),
        ("candidate_state_digest", "candidate candidate_state_digest mismatch"),
    ],
)
def test_candidate_context_and_state_bindings_fail_independently(
    ledger,
    field,
    message,
):
    anchor(ledger)
    graph_base = register_graph_base(ledger)
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match=message):
        register_candidate(
            ledger,
            graph_base,
            [node_write()],
            suffix=field,
            minute=5,
            mutate=lambda fields: fields.update({field: "sha256:" + "9" * 64}),
            recompute_artifact_hash=True,
        )
    assert ledger.path.read_bytes() == before


@pytest.mark.parametrize(
    "mutate,message",
    [
        (
            lambda proposal, _other: proposal.pop("candidate_artifact_hash"),
            "candidate binding must be all-or-none",
        ),
        (
            lambda proposal, other: proposal.update(
                candidate_artifact_id=other["id"],
            ),
            "Artifact hash mismatch",
        ),
        (
            lambda proposal, _other: proposal.update(
                candidate_digest="sha256:" + "9" * 64,
            ),
            "candidate digest mismatch",
        ),
    ],
)
def test_proposal_candidate_binding_fails_closed(ledger, mutate, message):
    anchor(ledger)
    graph_base = register_graph_base(ledger)
    artifacts = setup_policy(ledger)
    candidate = register_candidate(
        ledger,
        graph_base,
        [node_write("node:one")],
        suffix="one",
        minute=5,
    )
    other = register_candidate(
        ledger,
        graph_base,
        [node_write("node:two")],
        suffix="two",
        minute=6,
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match=message):
        propose(
            ledger,
            artifacts,
            candidate,
            suffix="one",
            minute=7,
            mutate=lambda proposal: mutate(proposal, other),
        )
    assert ledger.path.read_bytes() == before


def test_decision_cannot_substitute_another_registered_candidate(ledger):
    graph_base, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write("node:one"),
    )
    other = register_candidate(
        ledger,
        graph_base,
        [node_write("node:two")],
        suffix="two",
        minute=8,
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="decision changes proposal candidate binding"):
        decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=9,
            include_application=False,
            mutate_decision=lambda decision: decision.update(
                candidate_artifact_id=other["id"],
                candidate_artifact_hash=other["content_hash"],
                candidate_digest=other["candidate_digest"],
            ),
        )
    assert ledger.path.read_bytes() == before


def test_candidate_bound_accept_materializes_atomically_and_defensively(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    before = ledger.replay()
    assert not before.accepted_graph.has_node("node:one")
    decide(ledger, artifacts, proposal, candidate, assessment, suffix="one", minute=8)
    projection = ledger.replay()
    assert projection.accepted_graph.has_node("node:one")
    assert projection.acceptance_head != before.acceptance_head
    assert projection.materialization_head != before.materialization_head
    assert projection.accepted_application_order == ["application:one"]
    assert projection.accepted_graph.operations == []

    view = AcceptedGraphProjector(ledger).current(valid_as_of=VALID_0)
    assert view.graph.has_node("node:one")
    mutated = view.graph
    mutated.create_entity("TestNode", "node:local", {"name": "local"})
    assert not AcceptedGraphProjector(ledger).current(valid_as_of=VALID_0).graph.has_node(
        "node:local"
    )
    assert AcceptedGraphProjector(ledger).current(valid_as_of=VALID_0).graph.operations == []


def test_accepted_projection_drops_uncommitted_base_operation_audit(tmp_path, registry):
    base = KnowledgeGraph(registry)
    base.set_turn(99)
    base.create_entity("MissingType", "node:rejected")
    assert len(base.operations) == 1
    ledger = ProtocolLedger(
        tmp_path / "audit-free.jsonl",
        registry,
        accepted_graph_base=base,
    )
    anchor(ledger)
    register_graph_base(ledger)
    projection = ledger.replay()
    assert projection.accepted_graph.node_count == 0
    assert projection.accepted_graph.operations == []
    assert projection.accepted_graph.current_turn == 0
    assert AcceptedGraphProjector(ledger).current(
        valid_as_of=VALID_0
    ).graph.current_turn == 0


def test_repeated_replay_has_no_nondeterministic_operation_timestamps(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    decide(ledger, artifacts, proposal, candidate, assessment, suffix="one", minute=8)
    first = ledger.replay().accepted_graph
    second = ledger.replay().accepted_graph
    assert first.snapshot() == second.snapshot()
    assert first.operations == second.operations == []


def test_accept_without_application_fails_without_ledger_or_graph_change(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="requires one application"):
        decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=8,
            include_application=False,
        )
    assert ledger.path.read_bytes() == before
    assert not ledger.replay().accepted_graph.has_node("node:one")


@pytest.mark.parametrize(
    "field",
    [
        "candidate_artifact_id",
        "candidate_artifact_hash",
        "candidate_digest",
        "candidate_state_digest",
        "previous_acceptance_head",
        "result_acceptance_head",
        "previous_materialization_head",
        "result_materialization_head",
    ],
)
def test_application_cannot_change_any_bound_state(ledger, field):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="accepted application binding mismatch"):
        decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=8,
            mutate_application=lambda app: app.update({field: "sha256:" + "9" * 64}),
        )
    assert ledger.path.read_bytes() == before


def test_partial_decision_candidate_binding_fails_closed(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="candidate binding must be all-or-none"):
        decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=8,
            include_application=False,
            mutate_decision=lambda decision: decision.pop("candidate_artifact_hash"),
        )
    assert ledger.path.read_bytes() == before


@pytest.mark.parametrize(
    "field",
    [
        "candidate_digest",
        "base_state_digest",
        "candidate_state_digest",
        "ontology_hash",
    ],
)
def test_candidate_bound_logic_check_rejects_different_graph_state(ledger, field):
    _, artifacts, candidate, proposal, _ = prepared(
        ledger,
        write=node_write(),
    )
    event_id = f"event:logic-mismatch:{field}"
    check = make_record(
        "LogicCheckRecord",
        event_id=event_id,
        generated_at=at(8),
        actor_id="actor:monitor",
        role="logic-monitor",
        source_record_ids=[
            proposal["id"],
            "artifact:logic-monitor",
            "artifact:logic-contract",
            artifacts["rules"]["id"],
        ],
        id=f"logic-check:{field}",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        monitor_id="artifact:logic-monitor",
        monitor_version="1",
        monitor_hash="sha256:" + "a" * 64,
        candidate_digest=candidate["candidate_digest"],
        base_state_digest=candidate["base_state_digest"],
        candidate_state_digest=candidate["candidate_state_digest"],
        context_state_digests=[],
        ontology_hash=candidate["graph_ontology_hash"],
        fact_contract_version="2",
        logic_contract_id="artifact:logic-contract",
        logic_contract_version="1",
        logic_contract_record_hash="sha256:" + "b" * 64,
        logic_contract_artifact_hash="sha256:" + "c" * 64,
        ruleset_id=artifacts["rules"]["id"],
        ruleset_version="1",
        ruleset_record_hash=artifacts["rules"]["content_hash"],
        ruleset_artifact_hash=artifacts["rules"]["artifact_hash"],
        engine_name="SWI-Prolog",
        engine_version="100002",
        timeout_seconds=5,
        facts_hash="sha256:" + "d" * 64,
        fact_count=1,
        translated_record_ids=["node:one"],
        checked_rule_ids=["RULE_ONE"],
        violated_rule_ids=[],
        violation_witness_ids=[],
        check_outcome="SATISFIED",
    )
    check[field] = "sha256:" + "9" * 64
    check["content_hash"] = record_hash("LogicCheckRecord", check)
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="logic check targets a different candidate"):
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.LOGIC_CHECK_RECORDED,
            transaction_time=at(8),
            actor_id="actor:monitor",
            payload={"check": check, "witnesses": []},
        )
    assert ledger.path.read_bytes() == before


def test_rejected_candidate_never_changes_accepted_graph(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
        outcome="VIOLATED",
    )
    decide(
        ledger,
        artifacts,
        proposal,
        candidate,
        assessment,
        suffix="one",
        minute=8,
        include_application=False,
    )
    projection = ledger.replay()
    assert not projection.accepted_graph.has_node("node:one")
    assert projection.accepted_application_order == []
    assert projection.materialization_head.startswith("sha256:")


def test_nonaccepting_decision_forbids_graph_application(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
        outcome="VIOLATED",
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="graph application is forbidden"):
        decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=8,
        )
    assert ledger.path.read_bytes() == before


def test_direct_staging_materialization_is_not_ledger_acceptance(ledger):
    _, _, _, _, _ = prepared(ledger, write=node_write())
    external = ledger.replay().accepted_graph
    stage_subgraph(external, [ProposedOperation.entity("TestNode", "node:direct")]).materialize_into(
        external
    )
    assert external.has_node("node:direct")
    assert not ledger.replay().accepted_graph.has_node("node:direct")


def test_bitemporal_supersession_and_transaction_prefix(ledger):
    graph_base, artifacts, first, proposal, assessment = prepared(
        ledger,
        write=node_write("node:old"),
        suffix="old",
    )
    decide(ledger, artifacts, proposal, first, assessment, suffix="old", minute=8)
    second = register_candidate(
        ledger,
        graph_base,
        [
            node_write(
                "node:new",
                valid_from=EXACT_1,
                supersedes="node:old",
            )
        ],
        suffix="new",
        minute=9,
    )
    second_proposal = propose(ledger, artifacts, second, suffix="new", minute=10)
    second_assessment = assess(
        ledger,
        artifacts,
        second_proposal,
        suffix="new",
        minute=11,
    )
    decide(
        ledger,
        artifacts,
        second_proposal,
        second,
        second_assessment,
        suffix="new",
        minute=12,
    )

    projector = AcceptedGraphProjector(ledger)
    before_revision = projector.as_of(
        transaction_as_of="2026-08-12T08:08:00+00:00",
        transaction_sequence=9,
        valid_as_of=VALID_2,
    )
    after_revision_old_time = projector.current(valid_as_of=VALID_0)
    after_revision_new_time = projector.current(valid_as_of=VALID_1)
    assert before_revision.graph.has_node("node:old")
    assert not before_revision.graph.has_node("node:new")
    assert after_revision_old_time.graph.has_node("node:old")
    assert not after_revision_old_time.graph.has_node("node:new")
    assert not after_revision_new_time.graph.has_node("node:old")
    assert after_revision_new_time.graph.has_node("node:new")


def test_accepted_graph_view_constructor_break_is_explicit_and_projector_binds_it(
    ledger,
):
    graph = KnowledgeGraph(ledger.registry)
    with pytest.raises(TypeError) as failure:
        AcceptedGraphView(
            graph=graph,
            protocol_head_hash="sha256:" + "1" * 64,
            event_count=1,
            acceptance_head="sha256:" + "2" * 64,
            materialization_head="sha256:" + "3" * 64,
            accepted_history_state_digest=graph.state_digest(),
            visible_graph_digest=graph.state_digest(),
            transaction_as_of=at(1),
            transaction_sequence=1,
            valid_as_of=VALID_2,
            application_ids=(),
        )
    message = str(failure.value)
    for field in (
        "valid_time_resolution_digest",
        "valid_time_state",
        "record_states",
        "indeterminate_transitions",
    ):
        assert field in message

    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    decide(
        ledger,
        artifacts,
        proposal,
        candidate,
        assessment,
        suffix="one",
        minute=8,
    )
    view = AcceptedGraphProjector(ledger).current(valid_as_of=VALID_2)
    assert view.valid_time_resolution_digest.startswith("sha256:")
    assert view.valid_time_state == "DETERMINATE"
    assert view.record_states == {"node:one": "DEFINITELY_PRESENT"}
    assert view.indeterminate_transitions == ()


@pytest.mark.parametrize(
    "boundary,before,inside,after,reason_code",
    [
        (
            ValidTime.calendar_day(
                "2026-02-01",
                timezone="America/Los_Angeles",
                indeterminacy_reason=(
                    "The invoice establishes the service day but no installation time."
                ),
            ),
            "2026-02-01T07:59:59+00:00",
            "2026-02-01T12:00:00-08:00",
            "2026-02-02T08:00:00+00:00",
            "CALENDAR_DAY_TRANSITION_WINDOW",
        ),
        (
            ValidTime.bounded_interval(
                "2026-02-01T09:00:00-08:00",
                "2026-02-01T17:00:00-08:00",
                indeterminacy_reason=(
                    "The source establishes opening and closing bounds only."
                ),
            ),
            "2026-02-01T08:59:59-08:00",
            "2026-02-01T12:00:00-08:00",
            "2026-02-01T17:00:00-08:00",
            "BOUNDED_TRANSITION_WINDOW",
        ),
    ],
)
def test_uncertain_transition_returns_prior_then_reason_then_replacement(
    ledger,
    boundary,
    before,
    inside,
    after,
    reason_code,
):
    graph_base, artifacts, first, proposal, assessment = prepared(
        ledger,
        write=node_write("node:old"),
        suffix="old",
    )
    decide(ledger, artifacts, proposal, first, assessment, suffix="old", minute=8)
    second = register_candidate(
        ledger,
        graph_base,
        [node_write("node:new", valid_from=boundary, supersedes="node:old")],
        suffix="new",
        minute=9,
    )
    second_proposal = propose(ledger, artifacts, second, suffix="new", minute=10)
    second_assessment = assess(
        ledger,
        artifacts,
        second_proposal,
        suffix="new",
        minute=11,
    )
    decide(
        ledger,
        artifacts,
        second_proposal,
        second,
        second_assessment,
        suffix="new",
        minute=12,
    )

    projector = AcceptedGraphProjector(ledger)
    prior = projector.current(valid_as_of=before)
    uncertain = projector.current(valid_as_of=inside)
    replacement = projector.current(valid_as_of=after)

    assert prior.valid_time_state == "DETERMINATE"
    assert prior.graph.has_node("node:old")
    assert not prior.graph.has_node("node:new")
    assert replacement.valid_time_state == "DETERMINATE"
    assert not replacement.graph.has_node("node:old")
    assert replacement.graph.has_node("node:new")

    assert uncertain.valid_time_state == "INDETERMINATE"
    assert uncertain.record_states == {
        "node:new": "INDETERMINATE",
        "node:old": "INDETERMINATE",
    }
    assert uncertain.definite_graph.node_count == 0
    with pytest.raises(AcceptedGraphError, match="inspect indeterminate_transitions"):
        _ = uncertain.graph
    assert len(uncertain.indeterminate_transitions) == 1
    transition = uncertain.indeterminate_transitions[0]
    assert transition.prior_record_id == "node:old"
    assert transition.replacement_record_id == "node:new"
    assert transition.reason_code == reason_code
    assert transition.reason == boundary.indeterminacy_reason
    assert transition.valid_time == boundary
    assert uncertain.valid_time_resolution_digest.startswith("sha256:")


@pytest.mark.parametrize(
    "boundary,reason_code",
    [
        (
            ValidTime.order_only(
                order_scope="service:114430",
                order_index=2,
                indeterminacy_reason=(
                    "The invoice establishes operation order but no physical time."
                ),
            ),
            "ORDER_ONLY_WITHOUT_ABSOLUTE_BOUNDARY",
        ),
        (
            ValidTime.unresolved_prior_boundary(
                indeterminacy_reason=(
                    "The removed component has no established installation boundary."
                )
            ),
            "UNRESOLVED_PRIOR_BOUNDARY",
        ),
    ],
)
def test_unbounded_indeterminacy_returns_the_extracted_reason(ledger, boundary, reason_code):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write("node:uncertain", valid_from=boundary),
    )
    decide(ledger, artifacts, proposal, candidate, assessment, suffix="one", minute=8)
    view = AcceptedGraphProjector(ledger).current(valid_as_of=VALID_2)
    assert view.valid_time_state == "INDETERMINATE"
    assert view.record_states == {"node:uncertain": "INDETERMINATE"}
    transition = view.indeterminate_transitions[0]
    assert transition.reason_code == reason_code
    assert transition.reason == boundary.indeterminacy_reason
    assert transition.earliest_possible is None
    assert transition.latest_possible is None


def test_visible_relation_requires_visible_endpoints(ledger):
    anchor(ledger)
    graph_base = register_graph_base(ledger)
    artifacts = setup_policy(ledger)
    writes = [
        node_write("node:left", valid_to=EXACT_1),
        node_write("node:right"),
        temporal_write(
            ProposedOperation.relation(
                "TestLink",
                "link:one",
                "node:left",
                "node:right",
                {"relation_type": "TEST_LINK"},
            ),
            valid_from=EXACT_0,
        ),
    ]
    candidate = register_candidate(
        ledger,
        graph_base,
        writes,
        suffix="relation",
        minute=5,
    )
    proposal = propose(ledger, artifacts, candidate, suffix="relation", minute=6)
    assessment = assess(ledger, artifacts, proposal, suffix="relation", minute=7)
    decide(
        ledger,
        artifacts,
        proposal,
        candidate,
        assessment,
        suffix="relation",
        minute=8,
    )
    with pytest.raises(AcceptedGraphError, match="structurally incomplete"):
        AcceptedGraphProjector(ledger).current(valid_as_of=VALID_1)


def test_graph_base_is_required_and_must_match_external_graph(tmp_path, registry):
    no_base = ProtocolLedger(tmp_path / "no-base.jsonl", registry)
    anchor(no_base)
    metadata = graph_base_metadata(KnowledgeGraph(registry), [])
    fields = {
        "graph_schema_version": "2",
        "graph_ontology_hash": "sha256:" + registry.content_hash(),
        "base_state_digest": KnowledgeGraph(registry).state_digest(),
        "base_record_metadata": metadata,
        "base_record_count": 0,
    }
    with pytest.raises(ProtocolError, match="externally supplied graph base"):
        append_artifact(
            no_base,
            "GraphBaseArtifact",
            "artifact:graph-base",
            "GRAPH_BASE",
            1,
            artifact_hash=graph_base_artifact_digest(
                artifact_id="artifact:graph-base",
                artifact_version="1",
                graph_ontology_hash=fields["graph_ontology_hash"],
                base_state_digest=fields["base_state_digest"],
                base_record_metadata=metadata,
            ),
            **fields,
        )


def test_graph_base_artifact_cannot_substitute_external_state(tmp_path, registry):
    base = KnowledgeGraph(registry)
    ledger = ProtocolLedger(
        tmp_path / "wrong-base.jsonl",
        registry,
        accepted_graph_base=base,
    )
    anchor(ledger)
    metadata = graph_base_metadata(base, [])
    substituted = "sha256:" + "9" * 64
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="graph base state digest mismatch"):
        append_artifact(
            ledger,
            "GraphBaseArtifact",
            "artifact:graph-base",
            "GRAPH_BASE",
            1,
            artifact_hash=graph_base_artifact_digest(
                artifact_id="artifact:graph-base",
                artifact_version="1",
                graph_ontology_hash="sha256:" + registry.content_hash(),
                base_state_digest=substituted,
                base_record_metadata=metadata,
            ),
            graph_schema_version="2",
            graph_ontology_hash="sha256:" + registry.content_hash(),
            base_state_digest=substituted,
            base_record_metadata=metadata,
            base_record_count=0,
        )
    assert ledger.path.read_bytes() == before


def test_application_identifier_cannot_be_reused(ledger):
    graph_base, artifacts, first, proposal, assessment = prepared(
        ledger,
        write=node_write("node:one"),
        suffix="one",
    )
    decide(ledger, artifacts, proposal, first, assessment, suffix="one", minute=8)
    second = register_candidate(
        ledger,
        graph_base,
        [node_write("node:two")],
        suffix="two",
        minute=9,
    )
    second_proposal = propose(ledger, artifacts, second, suffix="two", minute=10)
    second_assessment = assess(
        ledger,
        artifacts,
        second_proposal,
        suffix="two",
        minute=11,
    )
    before = ledger.path.read_bytes()
    with pytest.raises(ProtocolError, match="application was already applied"):
        decide(
            ledger,
            artifacts,
            second_proposal,
            second,
            second_assessment,
            suffix="two",
            minute=12,
            application_id="application:one",
        )
    assert ledger.path.read_bytes() == before


def test_nonempty_graph_base_requires_complete_valid_time_metadata(tmp_path, registry):
    base = KnowledgeGraph(registry)
    base.create_entity("TestNode", "node:base", {"name": "base"})
    ledger = ProtocolLedger(
        tmp_path / "base.jsonl",
        registry,
        accepted_graph_base=base,
    )
    anchor(ledger)
    with pytest.raises(AcceptedGraphError, match="exactly cover graph records"):
        graph_base_metadata(base, [])
    with pytest.raises(AcceptedGraphError, match="precision-aware object"):
        graph_base_metadata(
            base,
            [{
                "record_id": "node:base",
                "valid_from": VALID_0,
                "valid_to": None,
                "supersedes_record_id": None,
            }],
        )
    metadata = graph_base_metadata(
        base,
        [
            {
                "record_id": "node:base",
                "valid_from": EXACT_0.as_dict(),
                "valid_to": EXACT_1.as_dict(),
                "supersedes_record_id": None,
            }
        ],
    )
    fields = {
        "graph_schema_version": "2",
        "graph_ontology_hash": "sha256:" + registry.content_hash(),
        "base_state_digest": base.state_digest(),
        "base_record_metadata": metadata,
        "base_record_count": 1,
    }
    append_artifact(
        ledger,
        "GraphBaseArtifact",
        "artifact:graph-base",
        "GRAPH_BASE",
        1,
        artifact_hash=graph_base_artifact_digest(
            artifact_id="artifact:graph-base",
            artifact_version="1",
            graph_ontology_hash=fields["graph_ontology_hash"],
            base_state_digest=fields["base_state_digest"],
            base_record_metadata=metadata,
        ),
        **fields,
    )
    projector = AcceptedGraphProjector(ledger)
    assert projector.current(valid_as_of=VALID_0).graph.has_node("node:base")
    assert not projector.current(valid_as_of=VALID_1).graph.has_node("node:base")


def test_graph_base_round_trips_entity_event_and_signal(tmp_path, registry):
    base = KnowledgeGraph(registry)
    operations = [
        base.create_entity("TestNode", "node:base", {"name": "base"}),
        base.create_entity("TestNode", "node:right", {"name": "right"}),
        base.create_relation(
            "TestLink",
            "link:base",
            "node:base",
            "node:right",
            {"relation_type": "TEST_LINK"},
        ),
        base.create_event("TestEvent", "event:base", {"event_type": "TEST"}),
        base.create_signal(
        "TestSignal",
        "signal:base",
            {"bearer_id": "node:base", "signal_type": "TEST", "value": 1.0},
        ),
    ]
    assert all(operation.op_status.value == "COMMITTED" for operation in operations)
    ledger = ProtocolLedger(
        tmp_path / "typed-base.jsonl",
        registry,
        accepted_graph_base=base,
    )
    anchor(ledger)
    intervals = [
        {
            "record_id": record_id,
            "valid_from": EXACT_0.as_dict(),
            "valid_to": None,
            "supersedes_record_id": None,
        }
        for record_id in (
            "node:base",
            "node:right",
            "link:base",
            "event:base",
            "signal:base",
        )
    ]
    metadata = graph_base_metadata(base, intervals)
    fields = {
        "graph_schema_version": "2",
        "graph_ontology_hash": "sha256:" + registry.content_hash(),
        "base_state_digest": base.state_digest(),
        "base_record_metadata": metadata,
        "base_record_count": 5,
    }
    append_artifact(
        ledger,
        "GraphBaseArtifact",
        "artifact:graph-base",
        "GRAPH_BASE",
        1,
        artifact_hash=graph_base_artifact_digest(
            artifact_id="artifact:graph-base",
            artifact_version="1",
            graph_ontology_hash=fields["graph_ontology_hash"],
            base_state_digest=fields["base_state_digest"],
            base_record_metadata=metadata,
        ),
        **fields,
    )
    view = AcceptedGraphProjector(ledger).current(valid_as_of=VALID_0).graph
    assert view.state_digest() == base.state_digest()
    assert {item["kind"] for item in view.canonical_operations()} == {
        "ENTITY",
        "EVENT",
        "SIGNAL",
        "RELATION",
    }


@pytest.mark.parametrize(
    "properties",
    [
        {"is_event": False},
        {"type": "domain-value"},
    ],
)
def test_internal_graph_category_markers_are_reserved(registry, properties):
    graph = KnowledgeGraph(registry)
    operation = graph.create_entity(
        "TestFlaggedNode",
        "node:flagged",
        properties,
    )
    assert operation.op_status.value == "REJECTED"
    assert "Reserved positional properties" in operation.rejection_reason


def test_historical_projection_verifies_later_ledger_semantics(ledger):
    _, artifacts, candidate, proposal, assessment = prepared(
        ledger,
        write=node_write(),
    )
    decide(ledger, artifacts, proposal, candidate, assessment, suffix="one", minute=8)
    append_artifact(
        ledger,
        "ProtocolArtifact",
        "artifact:later",
        "RULE_SET",
        9,
        artifact_hash=ARTIFACT_BODY,
    )
    events = [json.loads(line) for line in ledger.path.read_text(encoding="utf-8").splitlines()]
    artifact = events[-1]["payload"]["artifact"]
    artifact["artifact_kind"] = "MONITOR_SPECIFICATION"
    artifact["content_hash"] = record_hash("ProtocolArtifact", artifact)
    events[-1]["event_hash"] = event_hash(events[-1])
    ledger.path.write_text(
        "\n".join(canonical_json(event) for event in events) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ProtocolError, match="requires MonitorSpecificationArtifact"):
        AcceptedGraphProjector(ledger).as_of(
            transaction_as_of="2026-08-12T08:08:00+00:00",
            transaction_sequence=9,
            valid_as_of=VALID_0,
        )


class TestLogicalAssessmentBindsTheAppliedCandidate:
    """The ACCEPT arm re-checks every LogicalAssessment against the candidate it
    materializes (second self-inquisition S2, src/malleus/assent.py:1505-1517)."""

    def test_candidate_bound_accept_carries_a_logical_assessment(self, ledger):
        _, artifacts, candidate, proposal, assessment = prepared(
            ledger,
            write=node_write(),
            include_logic=True,
        )
        logical = artifacts["logical_assessment"]
        check = artifacts["logic_check"]
        decision = decide(
            ledger,
            artifacts,
            proposal,
            candidate,
            assessment,
            suffix="one",
            minute=9,
            extra_assessments=[logical],
        )
        assert decision["epistemic_verdict"] == "ACCEPT"
        assert logical["id"] in decision["assessment_ids"]
        assert check["candidate_digest"] == candidate["candidate_digest"]
        assert check["base_state_digest"] == candidate["base_state_digest"]
        assert check["candidate_state_digest"] == candidate["candidate_state_digest"]
        assert check["ontology_hash"] == candidate["graph_ontology_hash"]
        projection = ledger.replay()
        assert projection.accepted_graph.node_count == 1
        assert len(projection.accepted_application_ids) == 1

    def test_logic_check_for_another_candidate_never_reaches_the_accept_arm(self, ledger):
        anchor(ledger)
        graph_base = register_graph_base(ledger)
        artifacts = setup_policy(ledger, include_logic=True)
        candidate = register_candidate(
            ledger,
            graph_base,
            [node_write()],
            suffix="one",
            minute=5,
        )
        other = register_candidate(
            ledger,
            graph_base,
            [node_write("node:two")],
            suffix="two",
            minute=5,
        )
        proposal = propose(ledger, artifacts, candidate, suffix="one", minute=6)
        assess(ledger, artifacts, proposal, suffix="one", minute=7)
        before = ledger.path.read_bytes()
        with pytest.raises(ProtocolError, match="logic check targets a different candidate"):
            record_logic_check(
                ledger,
                artifacts,
                proposal,
                other,
                suffix="one",
                minute=7,
                translated_record_ids=("node:two",),
            )
        assert ledger.path.read_bytes() == before


class TestGraphBaseSupersessionLineage:
    """A graph base may carry supersession lineage of its own
    (second self-inquisition S2, src/malleus/accepted.py:650-680)."""

    @staticmethod
    def _base(registry, second_type="TestNode", third=False):
        graph = KnowledgeGraph(registry)
        graph.create_entity("TestNode", "node:one")
        graph.create_entity(second_type, "node:two")
        if third:
            graph.create_entity("TestNode", "node:three")
        return graph

    @staticmethod
    def _interval(record_id, valid_from, valid_to, supersedes=None):
        return {
            "record_id": record_id,
            "valid_from": valid_from.as_dict(),
            "valid_to": valid_to.as_dict() if valid_to is not None else None,
            "supersedes_record_id": supersedes,
        }

    def test_superseded_base_record_is_closed_and_linked(self, tmp_path, registry):
        base = self._base(registry)
        ledger = ProtocolLedger(
            tmp_path / "superseded.jsonl",
            registry,
            accepted_graph_base=base,
        )
        anchor(ledger)
        register_graph_base(
            ledger,
            intervals=[
                self._interval("node:one", EXACT_0, EXACT_1),
                self._interval("node:two", EXACT_1, None, "node:one"),
            ],
        )
        metadata = ledger.replay().accepted_record_metadata
        assert metadata["node:one"]["valid_to"] == EXACT_1.as_dict()
        assert metadata["node:one"]["superseded_by"] == "node:two"
        assert metadata["node:one"]["supersedes_record_id"] is None
        assert metadata["node:two"]["supersedes_record_id"] == "node:one"
        assert metadata["node:two"]["superseded_by"] is None

    def test_supersession_lineage_drives_the_valid_time_projection(self, tmp_path, registry):
        base = self._base(registry)
        ledger = ProtocolLedger(
            tmp_path / "superseded-projection.jsonl",
            registry,
            accepted_graph_base=base,
        )
        anchor(ledger)
        register_graph_base(
            ledger,
            intervals=[
                self._interval("node:one", EXACT_0, EXACT_1),
                self._interval("node:two", EXACT_1, None, "node:one"),
            ],
        )
        projector = AcceptedGraphProjector(ledger)
        early = projector.current(valid_as_of=VALID_0).graph
        late = projector.current(valid_as_of=VALID_2).graph
        assert early.node_count == 1
        assert late.node_count == 1
        assert early.snapshot() != late.snapshot()

    @pytest.mark.parametrize(
        "case,message",
        [
            ("self", "cannot supersede itself"),
            ("unknown", "supersedes unknown record 'node:absent'"),
            ("fork", "base supersession forks record 'node:one'"),
            ("type", "supersession type differs from prior record"),
            ("gap", "must begin at the prior valid_to"),
        ],
    )
    def test_base_supersession_lineage_fails_closed(self, registry, case, message):
        graph = self._base(
            registry,
            second_type="TestFlaggedNode" if case == "type" else "TestNode",
            third=case == "fork",
        )
        if case == "self":
            intervals = [
                self._interval("node:one", EXACT_0, EXACT_1, "node:one"),
                self._interval("node:two", EXACT_1, None),
            ]
        elif case == "unknown":
            intervals = [
                self._interval("node:one", EXACT_0, EXACT_1),
                self._interval("node:two", EXACT_1, None, "node:absent"),
            ]
        elif case == "fork":
            intervals = [
                self._interval("node:one", EXACT_0, EXACT_1),
                self._interval("node:three", EXACT_1, None, "node:one"),
                self._interval("node:two", EXACT_1, None, "node:one"),
            ]
        elif case == "type":
            intervals = [
                self._interval("node:one", EXACT_0, EXACT_1),
                self._interval("node:two", EXACT_1, None, "node:one"),
            ]
        else:
            intervals = [
                self._interval("node:one", EXACT_0, EXACT_2),
                self._interval("node:two", EXACT_1, None, "node:one"),
            ]
        with pytest.raises(AcceptedGraphError, match=message):
            graph_base_metadata(graph, intervals)

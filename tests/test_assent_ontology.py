"""Ontology-level separation guarantees for the assent protocol."""

from pathlib import Path

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry


ASSENT_SCHEMA = Path(__file__).parent.parent / "ontology" / "assent.yaml"


def test_assent_ontology_loads_with_disjoint_outcome_vocabularies():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.get_enum_values("AssessmentOutcome") == {
        "SATISFIED",
        "VIOLATED",
        "UNKNOWN",
    }
    assert registry.get_enum_values("EpistemicVerdict") == {
        "ACCEPT",
        "REJECT",
        "DEFER",
        "CONTEST",
    }
    assert registry.get_enum_values("AuthorizationVerdict") == {
        "AUTHORIZE",
        "BLOCK",
        "CLARIFY",
    }
    assert registry.get_enum_values("RequestState") == {
        "OPEN",
        "FULFILLED",
        "CANCELLED",
    }
    assert registry.get_enum_values("ViolationEpistemicVerdict") == {
        "REJECT",
        "DEFER",
        "CONTEST",
    }
    assert registry.get_enum_values("UnknownEpistemicVerdict") == {
        "DEFER",
        "CONTEST",
    }


def test_records_assessments_and_failures_are_distinct_categories():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("TypeAssessment", "Assessment")
    assert registry.is_subtype_of("Assessment", "ProtocolRecord")
    assert registry.is_subtype_of("MonitorFailure", "ProtocolRecord")
    assert not registry.is_subtype_of("MonitorFailure", "Assessment")
    assert "assessment_outcome" not in registry.effective_slots("MonitorFailure")
    assert registry.is_subtype_of("UnavailableAssessment", "Assessment")


def test_stage_six_artifacts_are_concrete_protocol_types():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("MonitorSpecificationArtifact", "ProtocolArtifact")
    assert registry.is_subtype_of("EpistemicPolicyArtifact", "ProtocolArtifact")
    monitor_kind = registry.get_slot_constraint(
        "MonitorSpecificationArtifact",
        "artifact_kind",
    )
    policy_kind = registry.get_slot_constraint("EpistemicPolicyArtifact", "artifact_kind")
    assert monitor_kind.equals_string == "MONITOR_SPECIFICATION"
    assert policy_kind.equals_string == "EPISTEMIC_POLICY"


def test_source_artifact_replaces_free_form_evidence_source_version():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("SourceArtifact", "ProtocolArtifact")
    assert (
        registry.get_slot_constraint("SourceArtifact", "artifact_kind").equals_string
        == "SOURCE"
    )
    evidence = registry.effective_slots("Evidence")
    assert evidence["source_artifact_id"].required
    assert evidence["source_artifact_hash"].required
    assert "source_version_id" not in evidence


def test_dispatch_execution_and_external_outcome_are_distinct_records():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("OutcomeContractArtifact", "ProtocolArtifact")
    assert (
        registry.get_slot_constraint(
            "OutcomeContractArtifact",
            "artifact_kind",
        ).equals_string
        == "OUTCOME_CONTRACT"
    )
    for record_type in ("ActionDispatch", "ActionExecution", "OutcomeObservation"):
        assert registry.is_subtype_of(record_type, "ProtocolRecord")
    assert registry.get_enum_values("ExecutionStatus") == {
        "SUCCEEDED",
        "FAILED",
        "ABORTED",
    }
    assert registry.get_enum_values("OutcomeResult") == {
        "CONFIRMED",
        "CONTRADICTED",
        "INDETERMINATE",
    }
    observation = registry.effective_slots("OutcomeObservation")
    assert observation["observed_source_artifact_id"].required
    assert observation["observed_source_artifact_hash"].required
    assert "evidence_ids" not in observation


def test_stage_seven_c_authorization_contract_is_typed_and_action_bound():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("AuthorizationPolicyArtifact", "ProtocolArtifact")
    assert registry.is_subtype_of(
        "UnavailableAuthorityAssessment",
        "UnavailableAssessment",
    )
    policy_kind = registry.get_slot_constraint(
        "AuthorizationPolicyArtifact",
        "artifact_kind",
    )
    assert policy_kind.equals_string == "AUTHORIZATION_POLICY"
    action_slots = registry.effective_slots("ActionProposal")
    assert action_slots["authorization_policy_id"].required
    assert action_slots["authorization_policy_hash"].required
    decision_slots = registry.effective_slots("AuthorizationDecision")
    assert decision_slots["policy_evaluation_hash"].required
    assert decision_slots["triggered_assessment_ids"].multivalued


def test_stage_seven_b_graph_records_are_separate_typed_categories():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("GraphBaseArtifact", "ProtocolArtifact")
    assert registry.is_subtype_of("CandidateSubgraphArtifact", "ProtocolArtifact")
    assert registry.is_subtype_of("AcceptedGraphApplication", "ProtocolRecord")
    assert not registry.is_subtype_of("AcceptedGraphApplication", "Decision")
    assert (
        registry.get_slot_constraint("GraphBaseArtifact", "artifact_kind").equals_string
        == "GRAPH_BASE"
    )
    assert (
        registry.get_slot_constraint(
            "CandidateSubgraphArtifact",
            "artifact_kind",
        ).equals_string
        == "CANDIDATE_SUBGRAPH"
    )


def test_candidate_and_application_bindings_remain_distinct():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    proposal_slots = registry.effective_slots("ProposedSubgraph")
    decision_slots = registry.effective_slots("EpistemicDecision")
    application_slots = registry.effective_slots("AcceptedGraphApplication")
    for name in ("candidate_artifact_id", "candidate_artifact_hash", "candidate_digest"):
        assert name in proposal_slots
        assert name in decision_slots
        assert name in application_slots
    assert "accepted_application_id" in decision_slots
    assert "result_materialization_head" in application_slots


def test_unavailable_assessment_is_unknown_only():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    outcome = registry.get_slot_constraint("UnavailableAssessment", "assessment_outcome")
    assert outcome.equals_string == "UNKNOWN"


def test_epistemic_decision_records_policy_evaluation_and_triggers():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    slots = registry.effective_slots("EpistemicDecision")
    assert slots["policy_evaluation_hash"].required
    assert slots["triggered_assessment_ids"].multivalued


def test_proposal_requires_exact_epistemic_policy_binding():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    slots = registry.effective_slots("ProposedSubgraph")
    assert slots["epistemic_policy_id"].required
    assert slots["epistemic_policy_hash"].required


def test_epistemic_and_authorization_slots_use_different_enums():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    epistemic = registry.get_slot_constraint("EpistemicDecision", "epistemic_verdict")
    authorization = registry.get_slot_constraint(
        "AuthorizationDecision",
        "authorization_verdict",
    )
    assessment = registry.get_slot_constraint("Assessment", "assessment_outcome")
    assert epistemic.range == "EpistemicVerdict"
    assert authorization.range == "AuthorizationVerdict"
    assert assessment.range == "AssessmentOutcome"


def test_cross_category_outcomes_fail_closed():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    base = {
        "id": "decision:1",
        "content_hash": "sha256:" + "1" * 64,
        "generation_event_id": "event:1",
        "generated_at": "2026-08-12T08:00:00Z",
        "responsible_actor_id": "actor:1",
        "responsible_role": "reviewer",
        "source_record_ids": [],
        "base_acceptance_head": "sha256:" + "2" * 64,
        "policy_id": "policy:1",
        "policy_hash": "sha256:" + "3" * 64,
        "rationale_codes": ["TEST"],
        "rationale": "test",
        "proposal_id": "proposal:1",
        "proposal_content_hash": "sha256:" + "4" * 64,
        "assessment_ids": ["assessment:1"],
        "evidence_assertion_ids": [],
        "request_ids": [],
        "claim_revision_ids": [],
        "ruleset_id": "rules:1",
        "ruleset_hash": "sha256:" + "5" * 64,
        "epistemic_verdict": "AUTHORIZE",
    }
    errors = registry.validate_instance("EpistemicDecision", base)
    assert any("Invalid value 'AUTHORIZE'" in error for error in errors)


def test_abstract_protocol_and_action_roots_cannot_materialize():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    graph = KnowledgeGraph(registry)
    for record_type in ("ProtocolRecord", "Assessment", "Decision", "ActionProposal"):
        operation = graph.create_entity(record_type, f"record:{record_type}")
        assert operation.op_status == OpStatus.REJECTED
        assert "abstract" in operation.rejection_reason


def test_monitor_failure_reason_vocabulary_is_closed():
    """R3 S1. `arbiter_is_accountable` asks the judge to record its reason.
    The reason was recorded as an open string, so "how many deferrals came
    from a timeout" was a substring search rather than a query, one layer
    away from enums this same schema already closes properly."""
    registry = OntologyRegistry(ASSENT_SCHEMA)
    for slot, enum_name in (("failure_category", "MonitorFailureCategory"),
                            ("error_code", "MonitorErrorCode")):
        constraint = registry.get_slot_constraint("MonitorFailure", slot)
        assert constraint.range == enum_name
        assert registry.has_enum(constraint.range)
    assert registry.get_enum_values("MonitorFailureCategory") == {
        "TIMEOUT", "DEPENDENCY", "EXECUTION",
    }


def test_unavailable_assessment_reason_codes_carry_the_closed_vocabulary():
    """R4 S4. The category and code were closed at their origin and left open
    at the place the finding named: `UnavailableAssessment.reason_codes` is
    populated from `error_code`, so an arbitrary string replayed clean through
    the vocabulary that had just been closed. Narrowed at the class, because
    decisions use the shared slot for a different vocabulary."""
    registry = OntologyRegistry(ASSENT_SCHEMA)
    constraint = registry.get_slot_constraint("UnavailableAssessment", "reason_codes")
    assert constraint.range == "MonitorErrorCode"
    assert registry.get_slot_constraint("TypeAssessment", "reason_codes").range == "string"
    errors = registry.validate_instance("UnavailableAssessment", {
        "id": "assessment:1",
        "assessment_kind": "TYPE",
        "assessment_outcome": "UNKNOWN",
        "reason_codes": ["Set via AI [confidence=low]"],
    })
    assert any("Invalid value" in error for error in errors)


def test_unrecognised_failure_category_is_rejected():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    errors = registry.validate_instance("MonitorFailure", {
        "id": "failure:1",
        "monitor_id": "monitor:1",
        "monitor_version": "1",
        "monitor_hash": "sha256:" + "1" * 64,
        "proposal_id": "proposal:1",
        "proposal_content_hash": "sha256:" + "2" * 64,
        "base_acceptance_head": "sha256:" + "3" * 64,
        "failed_assessment_kind": "TYPE",
        "failure_category": "FLAKY",
        "error_code": "FAILED",
        "error_message": "monitor did not answer",
    })
    assert any("Invalid value 'FLAKY'" in error for error in errors)


def test_monitor_failure_has_no_decision_or_assessment_outcome_slot():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    slots = registry.effective_slots("MonitorFailure")
    assert "assessment_outcome" not in slots
    assert "epistemic_verdict" not in slots
    assert "authorization_verdict" not in slots


def test_requests_and_revision_are_records_not_decision_values():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("EvidenceRequest", "Request")
    assert registry.is_subtype_of("HumanReviewRequest", "Request")
    assert registry.is_subtype_of("ClaimRevision", "ProtocolRecord")
    assert "SEEK_EVIDENCE" not in registry.get_enum_values("EpistemicVerdict")
    assert "SEEK_HUMAN" not in registry.get_enum_values("EpistemicVerdict")
    assert "SUPERSEDE" not in registry.get_enum_values("EpistemicVerdict")


def test_proposal_has_no_mutable_state_or_unresolved_graph_member_ids():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    slots = registry.effective_slots("ProposedSubgraph")
    assert "state" not in slots
    assert "node_record_ids" not in slots
    assert "relation_record_ids" not in slots
    assert "base_acceptance_head" in slots


class TestResponsibleRoleIsClosed:
    """The authority model turns on role; role is a closed vocabulary
    (self-inquisition S2)."""

    def test_out_of_vocabulary_role_is_rejected(self):
        registry = OntologyRegistry(ASSENT_SCHEMA)
        error = registry.validate_enum_field(
            "EpistemicDecision", "responsible_role", "emperor"
        )
        assert error is not None and "emperor" in error
        assert registry.validate_enum_field(
            "EpistemicDecision", "responsible_role", "epistemic-controller"
        ) is None

    def test_protocol_actor_carries_the_agent_mixin(self):
        registry = OntologyRegistry(ASSENT_SCHEMA)
        assert registry.has_type("ProtocolActor")
        assert registry.has_mixin("ProtocolActor", "Agent")
        constraint = registry.get_slot_constraint("ProtocolActor", "agent_type")
        assert constraint is not None and constraint.range == "ResponsibleRole"

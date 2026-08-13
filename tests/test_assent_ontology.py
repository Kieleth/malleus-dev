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


def test_records_assessments_and_failures_are_distinct_categories():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.is_subtype_of("TypeAssessment", "Assessment")
    assert registry.is_subtype_of("Assessment", "ProtocolRecord")
    assert registry.is_subtype_of("MonitorFailure", "ProtocolRecord")
    assert not registry.is_subtype_of("MonitorFailure", "Assessment")
    assert "assessment_outcome" not in registry.effective_slots("MonitorFailure")


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

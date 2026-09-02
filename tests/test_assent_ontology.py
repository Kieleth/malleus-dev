"""Ontology-level separation guarantees for the assent protocol."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from linkml_runtime.utils.schemaview import SchemaView

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry
from malleus.valid_time import ValidTime, ValidTimeError


ASSENT_SCHEMA = Path(__file__).parent.parent / "ontology" / "assent.yaml"


def claim_version_properties(valid_time):
    return {
        "content_hash": "sha256:" + "0" * 64,
        "generation_event_id": "event:1",
        "generated_at": "2026-08-17T00:00:00+00:00",
        "responsible_actor_id": "actor:1",
        "responsible_role": "proposer",
        "source_record_ids": [],
        "claim_key": "claim:alpha",
        "revision": 1,
        "statement": "A claim with an explicit valid-time boundary.",
        "domain_valid_from": valid_time,
    }


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
    assert registry.get_enum_values("ValidTimePrecision") == {
        "EXACT_TIMESTAMP",
        "CALENDAR_DAY",
        "BOUNDED_INTERVAL",
        "ORDER_ONLY",
        "UNRESOLVED_PRIOR_BOUNDARY",
    }


def test_claim_and_revision_times_use_the_same_inlined_valid_time_object():
    registry = OntologyRegistry(ASSENT_SCHEMA)
    for record_type, field in (
        ("ClaimVersion", "domain_valid_from"),
        ("ClaimVersion", "domain_valid_to"),
        ("ClaimRevision", "replacement_valid_from"),
        ("ClaimRevision", "replaced_valid_to"),
    ):
        constraint = registry.get_slot_constraint(record_type, field)
        assert constraint.range == "ValidTime"
        assert constraint.inlined is True
    exact = {
        "valid_time_precision": "EXACT_TIMESTAMP",
        "exact_timestamp": "2026-01-27T12:00:00-08:00",
    }
    assert registry.validate_instance("ValidTime", exact) == []
    errors = registry.validate_instance(
        "ClaimVersion",
        {"domain_valid_from": exact["exact_timestamp"]},
    )
    assert any("Inlined property 'domain_valid_from' must be a mapping" in error for error in errors)


@pytest.mark.parametrize(
    "value",
    [
        {
            "valid_time_precision": "EXACT_TIMESTAMP",
            "exact_timestamp": "2026-08-17T00:00:00+00:00",
        },
        {
            "valid_time_precision": "CALENDAR_DAY",
            "calendar_date": "2026-08-17",
            "timezone": "America/Los_Angeles",
            "timezone_database_version": "2026c",
            "indeterminacy_reason": "The source establishes only a day.",
        },
        {
            "valid_time_precision": "BOUNDED_INTERVAL",
            "earliest_possible": "2026-08-17T00:00:00+00:00",
            "latest_possible": "2026-08-18T00:00:00+00:00",
            "indeterminacy_reason": "The source establishes an interval.",
        },
        {
            "valid_time_precision": "ORDER_ONLY",
            "order_scope": "claim:alpha",
            "order_index": 2,
            "indeterminacy_reason": "The source establishes only order.",
        },
        {
            "valid_time_precision": "UNRESOLVED_PRIOR_BOUNDARY",
            "indeterminacy_reason": "The prior boundary is not recoverable.",
        },
    ],
)
def test_valid_time_exactly_one_of_accepts_each_canonical_variant(value):
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.validate_instance("ValidTime", value) == []


@pytest.mark.parametrize(
    ("value", "detail"),
    [
        ({"valid_time_precision": "EXACT_TIMESTAMP"}, "exact_timestamp"),
        (
            {
                "valid_time_precision": "CALENDAR_DAY",
                "calendar_date": "2026-08-17",
                "timezone": "America/Los_Angeles",
                "timezone_database_version": "2026c",
            },
            "indeterminacy_reason",
        ),
        (
            {
                "valid_time_precision": "BOUNDED_INTERVAL",
                "earliest_possible": "2026-08-17T00:00:00+00:00",
                "indeterminacy_reason": "The upper bound is missing.",
            },
            "latest_possible",
        ),
        (
            {
                "valid_time_precision": "ORDER_ONLY",
                "order_scope": "claim:alpha",
                "indeterminacy_reason": "The index is missing.",
            },
            "order_index",
        ),
        (
            {"valid_time_precision": "UNRESOLVED_PRIOR_BOUNDARY"},
            "indeterminacy_reason",
        ),
    ],
)
def test_valid_time_exactly_one_of_rejects_incomplete_variants(value, detail):
    errors = OntologyRegistry(ASSENT_SCHEMA).validate_instance("ValidTime", value)
    assert any("matched 0" in error and detail in error for error in errors)


@pytest.mark.parametrize("forbidden", ["unexpected", None])
def test_valid_time_exact_variant_rejects_present_reason_even_when_null(forbidden):
    value = {
        "valid_time_precision": "EXACT_TIMESTAMP",
        "exact_timestamp": "2026-08-17T00:00:00+00:00",
        "indeterminacy_reason": forbidden,
    }
    errors = OntologyRegistry(ASSENT_SCHEMA).validate_instance("ValidTime", value)
    assert any("indeterminacy_reason" in error and "absent" in error for error in errors)


def test_valid_time_calendar_day_rejects_unpinned_timezone_database():
    value = {
        "valid_time_precision": "CALENDAR_DAY",
        "calendar_date": "2026-08-17",
        "timezone": "America/Los_Angeles",
        "timezone_database_version": "2025b",
        "indeterminacy_reason": "The source establishes only a day.",
    }
    errors = OntologyRegistry(ASSENT_SCHEMA).validate_instance("ValidTime", value)
    assert any("timezone_database_version" in error and "2026c" in error for error in errors)


@pytest.mark.parametrize(
    "value",
    [
        {
            "valid_time_precision": "EXACT_TIMESTAMP",
            "exact_timestamp": "2026-08-17T00:00:00",
        },
        {
            "valid_time_precision": "BOUNDED_INTERVAL",
            "earliest_possible": "2026-08-18T00:00:00+00:00",
            "latest_possible": "2026-08-17T00:00:00+00:00",
            "indeterminacy_reason": "The interval order is invalid.",
        },
    ],
)
def test_valid_time_lexical_and_temporal_semantics_remain_runtime_checked(value):
    registry = OntologyRegistry(ASSENT_SCHEMA)
    assert registry.validate_instance("ValidTime", value) == []
    with pytest.raises(ValidTimeError):
        ValidTime.from_value(value)


def test_malformed_inlined_valid_time_cannot_commit_a_claim_version():
    graph = KnowledgeGraph(OntologyRegistry(ASSENT_SCHEMA))
    operation = graph.create_entity(
        "ClaimVersion",
        "claim-version:malformed-time",
        claim_version_properties(
            {
                "valid_time_precision": "EXACT_TIMESTAMP",
            }
        ),
    )
    assert operation.op_status is OpStatus.REJECTED
    assert "exact_timestamp" in operation.rejection_reason
    assert graph.canonical_operations() == ()


def test_standalone_kg_validates_shape_not_valid_time_runtime_semantics():
    naive_time = {
        "valid_time_precision": "EXACT_TIMESTAMP",
        "exact_timestamp": "2026-08-17T00:00:00",
    }
    graph = KnowledgeGraph(OntologyRegistry(ASSENT_SCHEMA))
    operation = graph.create_entity(
        "ClaimVersion",
        "claim-version:structural-time",
        claim_version_properties(naive_time),
    )
    assert operation.op_status is OpStatus.COMMITTED
    with pytest.raises(ValidTimeError, match="timezone"):
        ValidTime.from_value(naive_time)


def test_official_linkml_loads_union_and_smoke_generates_json_schema():
    schema_view = SchemaView(str(ASSENT_SCHEMA))
    valid_time = schema_view.get_class("ValidTime")
    assert valid_time is not None
    assert len(valid_time.exactly_one_of) == 5
    assert {
        str(expression.slot_conditions["valid_time_precision"].equals_string)
        for expression in valid_time.exactly_one_of
    } == {
        "EXACT_TIMESTAMP",
        "CALENDAR_DAY",
        "BOUNDED_INTERVAL",
        "ORDER_ONLY",
        "UNRESOLVED_PRIOR_BOUNDARY",
    }
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "linkml.generators.jsonschemagen",
            str(ASSENT_SCHEMA),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    generated = json.loads(result.stdout)
    assert "ValidTime" in generated["$defs"]


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


def test_authority_grant_has_required_identity_bearing_scope_commitments():
    schema_view = SchemaView(str(ASSENT_SCHEMA))
    assert str(schema_view.schema.version) == "0.11.0"

    registry = OntologyRegistry(ASSENT_SCHEMA)
    grant = registry.effective_slots("AuthorityGrant")
    assert grant["scope_record_id"].required
    assert grant["scope_record_id"].range == "string"
    assert grant["scope_record_id"].multivalued is not True
    assert grant["may_subdelegate"].required
    assert grant["may_subdelegate"].range == "boolean"
    assert grant["may_subdelegate"].multivalued is not True

    epistemic = registry.effective_slots("EpistemicDecision")
    assert "scope_record_id" not in epistemic
    assert "may_subdelegate" not in epistemic


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
    assert registry.is_subtype_of("ReviewRequest", "ProtocolRecord")
    assert registry.is_subtype_of("ReviewReport", "ProtocolRecord")
    assert registry.is_subtype_of("ReviewFinding", "ProtocolRecord")
    assert registry.is_subtype_of("ReviewDisposition", "ProtocolRecord")
    request_slots = registry.effective_slots("ReviewRequest")
    assert "requested_by_actor_id" not in request_slots
    assert "issued_at" not in request_slots
    report_slots = registry.effective_slots("ReviewReport")
    assert "reviewer_id" not in report_slots
    assert report_slots["request_hash"].required
    disposition_slots = registry.effective_slots("ReviewDisposition")
    assert "revision" not in disposition_slots
    assert "revises_review_disposition_id" not in disposition_slots
    assert "revises_review_disposition_hash" not in disposition_slots
    assert registry.get_enum_values("ReviewDispositionValue") == {
        "ADOPT",
        "DEFER",
        "DISMISS",
        "RETURN",
        "INVALIDATE",
    }
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

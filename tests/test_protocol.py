"""Adversarial tests for assent transitions and their JSONL envelope."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from malleus.ontology import OntologyRegistry
from malleus.protocol import (
    AuthorizationState,
    EventType,
    LedgerError,
    ProposalState,
    ProtocolError,
    ProtocolLedger,
    canonical_json,
    event_hash,
    make_record,
    record_hash,
)


ASSENT_SCHEMA = Path(__file__).parent.parent / "ontology" / "assent.yaml"
T0 = "2026-08-12T08:00:00Z"
SNAPSHOT = "sha256:" + "1" * 64
ARTIFACT_BODY = "sha256:" + "2" * 64


def time_at(minute: int) -> str:
    return f"2026-08-12T08:{minute:02d}:00Z"


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
        artifact_hash=ARTIFACT_BODY,
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


def setup_artifacts(ledger: ProtocolLedger) -> dict[str, dict]:
    return {
        "monitor": add_artifact(ledger, "artifact:monitor", "MONITOR_SPECIFICATION", 1),
        "epistemic_policy": add_artifact(
            ledger,
            "artifact:epistemic-policy",
            "EPISTEMIC_POLICY",
            2,
        ),
        "rules": add_artifact(ledger, "artifact:rules", "RULE_SET", 3),
        "authorization_policy": add_artifact(
            ledger,
            "artifact:authorization-policy",
            "AUTHORIZATION_POLICY",
            4,
        ),
        "grant": add_artifact(
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
        ),
    }


def record_proposal(
    ledger: ProtocolLedger,
    *,
    include_action: bool = False,
    minute: int = 6,
    proposal_id: str = "proposal:1",
    proposal_revision: int = 1,
    revises_proposal_id: str | None = None,
    claim_id: str = "claim:1",
    action_id: str = "action:1",
    action_revision: int = 1,
    revises_action_id: str | None = None,
) -> tuple[dict, dict, dict | None]:
    projection = ledger.replay()
    event_id = f"event:{proposal_id}"
    timestamp = time_at(minute)
    claim = make_record(
        "ClaimVersion",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:proposer",
        role="proposer",
        id=claim_id,
        claim_key="claim-key",
        revision=1,
        revises_claim_version_id=None,
        statement="The declared relation is structurally valid.",
        domain_valid_from=timestamp,
        domain_valid_to=None,
        dependency_ids=[],
    )
    action = None
    members = [("ClaimVersion", claim)]
    if include_action:
        action = make_record(
            "TestActionProposal",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:proposer",
            role="proposer",
            id=action_id,
            action_type="TEST",
            action_payload_hash="sha256:" + "6" * 64,
            action_key="action-key",
            revision=action_revision,
            revises_action_proposal_id=revises_action_id,
            test_parameter="value",
        )
        members.append(("TestActionProposal", action))
    proposal = make_record(
        "ProposedSubgraph",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:proposer",
        role="proposer",
        id=proposal_id,
        proposal_key="proposal-key",
        revision=proposal_revision,
        revises_proposal_id=revises_proposal_id,
        base_acceptance_head=projection.acceptance_head,
        member_content_hashes=[record["content_hash"] for _, record in members],
        claim_version_ids=[claim["id"]],
        evidence_ids=[],
        evidence_assertion_ids=[],
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
) -> dict:
    event_id = f"event:assessment:{outcome.lower()}"
    timestamp = time_at(minute)
    assessment = make_record(
        "TypeAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:monitor",
        role="type-monitor",
        source_record_ids=[proposal["id"], monitor["id"]],
        id=f"assessment:{outcome.lower()}",
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


def record_authority_assessment(
    ledger: ProtocolLedger,
    proposal: dict,
    action: dict,
    artifacts: dict[str, dict],
    *,
    outcome: str = "SATISFIED",
    checked: list[str] | None = None,
    violated: list[str] | None = None,
) -> dict:
    event_id = "event:authority-assessment"
    timestamp = time_at(9)
    authority = make_record(
        "AuthorityAssessment",
        event_id=event_id,
        generated_at=timestamp,
        actor_id="actor:authority-monitor",
        role="authority-monitor",
        source_record_ids=[proposal["id"], action["id"], artifacts["authorization_policy"]["id"]],
        id="assessment:authority:1",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=ledger.replay().acceptance_head,
        assessment_kind="AUTHORITY",
        assessment_outcome=outcome,
        monitor_id=artifacts["monitor"]["id"],
        monitor_version="1",
        monitor_hash=artifacts["monitor"]["content_hash"],
        monitor_failure_id=None,
        input_record_ids=[proposal["id"], action["id"]],
        reason_codes=["GRANT_RESULT"],
        rationale="The versioned authority policy was evaluated.",
        action_proposal_id=action["id"],
        evaluated_actor_id="actor:executor",
        authority_policy_id=artifacts["authorization_policy"]["id"],
        authority_policy_hash=artifacts["authorization_policy"]["content_hash"],
        checked_policy_predicates=checked if checked is not None else ["actor_in_scope"],
        violated_policy_predicates=violated if violated is not None else [],
    )
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.ASSESSMENT_RECORDED,
        transaction_time=timestamp,
        actor_id="actor:authority-monitor",
        payload={"assessment_type": "AuthorityAssessment", "assessment": authority},
    )
    return authority


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


def decide_epistemically(
    ledger: ProtocolLedger,
    proposal: dict,
    assessment: dict,
    artifacts: dict[str, dict],
    *,
    verdict: str = "ACCEPT",
    minute: int = 8,
) -> dict:
    event_id = "event:epistemic:1"
    timestamp = time_at(minute)
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
        id="decision:epistemic:1",
        proposal_id=proposal["id"],
        proposal_content_hash=proposal["content_hash"],
        base_acceptance_head=proposal["base_acceptance_head"],
        epistemic_verdict=verdict,
        assessment_ids=[assessment["id"]],
        evidence_assertion_ids=[],
        request_ids=[],
        claim_revision_ids=[],
        policy_id=artifacts["epistemic_policy"]["id"],
        policy_hash=artifacts["epistemic_policy"]["content_hash"],
        ruleset_id=artifacts["rules"]["id"],
        ruleset_hash=artifacts["rules"]["content_hash"],
        rationale_codes=["POLICY_RESULT"],
        rationale="The versioned policy selected a verdict.",
    )
    target = {
        "ACCEPT": "ACCEPTED",
        "REJECT": "REJECTED",
        "DEFER": "DEFERRED",
        "CONTEST": "CONTESTED",
    }[verdict]
    sequence = ledger.replay().event_count + 1
    ledger.append_event(
        event_id=event_id,
        event_type=EventType.EPISTEMIC_DECIDED,
        transaction_time=timestamp,
        actor_id="actor:reviewer",
        payload={
            "decision": decision,
            "requests": [],
            "revisions": [],
            "transition": transition(
                event_id=event_id,
                timestamp=timestamp,
                actor_id="actor:reviewer",
                transition_id="transition:proposal:1",
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

    def test_hash_chain_and_external_anchor_checks_detect_corruption(self, ledger):
        first = anchor(ledger)
        add_artifact(ledger, "artifact:monitor", "MONITOR_SPECIFICATION", 1)
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
        add_artifact(ledger, "artifact:monitor", "MONITOR_SPECIFICATION", 1)
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
        decide_epistemically(ledger, proposal, assessment, artifacts)
        first = ledger.replay()
        second = ledger.replay()
        assert first.proposal_states[proposal["id"]] == ProposalState.ACCEPTED
        assert first.current_claim_by_key[claim["claim_key"]] == claim["id"]
        assert first.acceptance_head == second.acceptance_head
        assert "state" not in proposal

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
        artifacts = setup_artifacts(ledger)
        proposal, _, _ = record_proposal(ledger)
        assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        before = ledger.replay().acceptance_head
        decide_epistemically(ledger, proposal, assessment, artifacts, verdict=verdict)
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
        with pytest.raises(ProtocolError, match="every cited assessment SATISFIED"):
            decide_epistemically(ledger, proposal, assessment, artifacts)
        assert ledger.path.read_bytes() == before

    def test_state_outputs_cannot_be_smuggled_as_proposal_members(self, ledger):
        anchor(ledger)
        proposal = make_record(
            "ProposedSubgraph",
            event_id="event:proposal:1",
            generated_at=time_at(1),
            actor_id="actor:proposer",
            role="proposer",
            id="proposal:1",
            proposal_key="proposal-key",
            revision=1,
            revises_proposal_id=None,
            base_acceptance_head=ledger.replay().acceptance_head,
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
                transaction_time=time_at(1),
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
            domain_valid_from=timestamp,
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
        failure = make_record(
            "MonitorFailure",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            source_record_ids=[proposal["id"], artifacts["monitor"]["id"]],
            id="failure:1",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            failed_assessment_kind="TYPE",
            failure_category="TIMEOUT",
            error_code="DEADLINE",
            error_message="The monitor exceeded its deadline.",
        )
        unknown = make_record(
            "TypeAssessment",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:monitor",
            role="type-monitor",
            source_record_ids=[failure["id"]],
            id="assessment:unknown",
            proposal_id=proposal["id"],
            proposal_content_hash=proposal["content_hash"],
            base_acceptance_head=proposal["base_acceptance_head"],
            assessment_kind="TYPE",
            assessment_outcome="UNKNOWN",
            monitor_id=artifacts["monitor"]["id"],
            monitor_version="1",
            monitor_hash=artifacts["monitor"]["content_hash"],
            monitor_failure_id=failure["id"],
            input_record_ids=[proposal["id"]],
            reason_codes=["MONITOR_FAILED"],
            rationale="No assessment result was available.",
        )
        ledger.append_event(
            event_id=event_id,
            event_type=EventType.MONITOR_FAILED,
            transaction_time=timestamp,
            actor_id="actor:monitor",
            payload={
                "failure": failure,
                "assessment_type": "TypeAssessment",
                "assessment": unknown,
            },
        )
        projection = ledger.replay()
        assert failure["id"] in projection.monitor_failure_ids
        assert unknown["id"] in projection.assessment_ids
        with pytest.raises(ProtocolError, match="every cited assessment SATISFIED"):
            decide_epistemically(ledger, proposal, unknown, artifacts)

    def test_authorization_requires_action_bound_actor_and_satisfied_authority(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        proposal, claim, action = record_proposal(ledger, include_action=True)
        type_assessment = record_type_assessment(ledger, proposal, artifacts["monitor"])
        epistemic = decide_epistemically(ledger, proposal, type_assessment, artifacts)
        base = ledger.replay().acceptance_head
        authority = record_authority_assessment(ledger, proposal, action, artifacts)
        event_id = "event:authorization:1"
        timestamp = time_at(10)
        decision = make_record(
            "AuthorizationDecision",
            event_id=event_id,
            generated_at=timestamp,
            actor_id="actor:authorizer",
            role="authorizer",
            source_record_ids=[epistemic["id"], authority["id"], artifacts["grant"]["id"]],
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

    def test_action_revision_cannot_fork_from_nonlatest_revision(self, ledger):
        anchor(ledger)
        artifacts = setup_artifacts(ledger)
        first_proposal, _, first_action = record_proposal(ledger, include_action=True)
        assessment = record_type_assessment(ledger, first_proposal, artifacts["monitor"])
        decide_epistemically(ledger, first_proposal, assessment, artifacts, verdict="REJECT")
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

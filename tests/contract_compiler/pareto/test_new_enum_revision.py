"""New closed vocabularies grow a history without reinterpreting its prefix."""

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto.test_contract_revision import (
    ADD_CLASS_SOURCE,
    BASE_SOURCE,
    _admit,
    _compile,
    _compose_revision,
    _history,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
)
from tests.contract_compiler.pareto.test_ontology_gap_answer import (
    CONSUMERS,
    DECIDER,
    _proposal_bytes,
    _retain_proposal,
)


HISTORICAL_POLICIES = (
    "sha256:05b6880517ae8287333973e421248e2eb803c2f50569adcea26ca114d154ce8e",
    "sha256:e129b6e87bd06abc8d23b22bdefee2142c07574237b273a068040fc14d09db59",
)
ENUM_FRAGMENT = b"""enums:
  NewStatus:
    permissible_values:
      PENDING:
      CONTESTED:
"""
ADDITION = (
    ENUM_FRAGMENT
    + b"""slots:
  assessment_status:
    range: NewStatus
classes:
  Assessment:
    is_a: Entity
    slots: [assessment_status]
    slot_usage:
      assessment_status:
        required: true
"""
)


def _revision(history, source, policy, *, revision_id="revision:explicit-policy"):
    target = _compile(source)
    replay = history.replay()
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=replay.partial_contract.normative_profile,
    )
    return api.compile_contract_revision(
        revision_id=revision_id,
        base_ledger_head=replay.ledger_head,
        base_ledger_event_count=replay.ledger_event_count,
        base_acceptance_head=replay.acceptance_head,
        base_materialization_head=replay.materialization_head,
        base_accepted_state_digest=replay.graph.state_digest(),
        current_validated_contract_bytes=replay.contract_view.artifact_bytes,
        current_partial_contract_bytes=replay.partial_contract.canonical_bytes,
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="new closed vocabulary",
        issued_at=TRANSACTION_TIME,
        policy=policy,
        previous_migration_receipt=(
            replay.contract_revisions[-1].migration_receipt.digest
            if replay.contract_revisions
            else None
        ),
    )


def test_successor_policy_preserves_both_historical_identities():
    assert tuple(p.identity for p in api.SUPPORTED_CONTRACT_REVISION_POLICIES[:-1]) == (
        HISTORICAL_POLICIES
    )
    assert api.SUPPORTED_CONTRACT_REVISION_POLICIES[-1] is api.CONTRACT_REVISION_POLICY
    assert api.CONTRACT_REVISION_POLICY.outcome("ADD_ENUM") == "ADMIT"
    assert api.CONTRACT_REVISION_POLICY.identity not in HISTORICAL_POLICIES


def test_new_enum_declaration_and_members_have_distinct_changes(tmp_path):
    history, _, _ = _history(tmp_path)
    before = history.path.read_bytes()
    source = api.compose_linkml_addition(BASE_SOURCE, ENUM_FRAGMENT)
    revision, _, _ = _compose_revision(history, source)
    assert [(c.kind, c.value) for c in revision.changes] == [
        ("ADD_ENUM", None),
        ("ADD_ENUM_VALUE", "CONTESTED"),
        ("ADD_ENUM_VALUE", "PENDING"),
    ]
    assert len({c.subject for c in revision.changes}) == 1
    assert api.ContractRevision.from_bytes(revision.canonical_bytes) == revision
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("policy_identity", HISTORICAL_POLICIES)
def test_historical_policy_replays_but_cannot_admit_new_enum(tmp_path, policy_identity):
    history, _, _ = _history(tmp_path)
    policy = api.contract_revision_policy(policy_identity)
    old_revision = _revision(history, ADD_CLASS_SOURCE, policy)
    history.record_contract_revision(
        revision=old_revision, transaction_time=TRANSACTION_TIME, actor_id=DECIDER
    )
    prefix = history.path.read_bytes()
    assert api.KnowledgeChangeHistory.reopen(
        history.path
    ).replay().contract_revisions == (old_revision,)
    with pytest.raises(api.ContractRevisionRefusal) as caught:
        _revision(
            history,
            api.compose_linkml_addition(ADD_CLASS_SOURCE, ENUM_FRAGMENT),
            policy,
        )
    assert caught.value.change_kind == "ADD_ENUM"
    assert history.path.read_bytes() == prefix
    successor = _revision(
        history,
        api.compose_linkml_addition(ADD_CLASS_SOURCE, ENUM_FRAGMENT),
        api.CONTRACT_REVISION_POLICY,
        revision_id="revision:new-enum",
    )
    history.record_contract_revision(
        revision=successor, transaction_time=TRANSACTION_TIME, actor_id=DECIDER
    )
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.contract_revisions == (old_revision, successor)
    assert (
        successor.migration_receipt.previous_receipt
        == old_revision.migration_receipt.digest
    )
    assert history.path.read_bytes().startswith(prefix)


@pytest.mark.parametrize("accepted", [False, True])
def test_predecessor_gap_proposal_and_answer_replay_unchanged(
    tmp_path, monkeypatch, accepted
):
    from malleus._contract_pipeline import knowledge
    from tests.contract_compiler.pareto.test_ontology_gap_answer import _plan_history

    history, gap_identity, _ = _plan_history(tmp_path)
    # Reproduce the predecessor's proposal validator and acceptance policy.
    with monkeypatch.context() as previous_runtime:
        previous_runtime.setattr(
            knowledge,
            "CONTRACT_REVISION_POLICY",
            api.contract_revision_policy(HISTORICAL_POLICIES[-1]),
        )
        _retain_proposal(history, _proposal_bytes(answers=(gap_identity,)))
        if accepted:
            history.accept_ontology_revision_proposal(
                proposal_id="proposal:customer",
                deciding_actor=DECIDER,
                transaction_time=TRANSACTION_TIME,
                actor_id=DECIDER,
            )
        old = history.replay()
        prefix = history.path.read_bytes()
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.receipt == old.receipt
    assert reopened.contract_revisions == old.contract_revisions
    assert reopened.gap_answers == old.gap_answers
    assert reopened.open_gaps() == old.open_gaps()
    assert history.path.read_bytes() == prefix


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_gap_answer_adds_closed_vocabulary_preserves_records_and_reopens(
    tmp_path, consumer
):
    history, gap_identity, _ = consumer(tmp_path)
    before = history.replay()
    prefix = history.path.read_bytes()
    records = before.graph.export_records()
    proposal = _proposal_bytes(answers=(gap_identity,), addition=ADDITION.decode())
    _retain_proposal(history, proposal)
    retained = history.replay()
    assert not retained.contract_view.has_type("Assessment")
    assert retained.partial_contract.identity == before.partial_contract.identity
    assert retained.graph.export_records() == records
    assert (
        api.KnowledgeChangeHistory.reopen(history.path).replay().receipt
        == retained.receipt
    )

    revised = history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id=DECIDER,
    )
    assert revised.graph.export_records() == records
    assert revised.record_history == before.record_history
    assert revised.open_gaps() == ()
    assert {c.kind for c in revised.contract_revisions[-1].changes} == {
        "ADD_CLASS",
        "ADD_ENUM",
        "ADD_ENUM_VALUE",
        "ADD_SLOT",
    }
    assert history.path.read_bytes().startswith(prefix)

    def change(value):
        return history.compose_change_set(
            change_set_id="change:assessment",
            source_record_ids=("source-generic",),
            evidence_record_ids=("evidence-generic",),
            operations=(
                api.KnowledgeOperation(
                    ordinal=0,
                    operation_id="create:assessment",
                    operation_type="CREATE_ENTITY",
                    record_type="Assessment",
                    record_id="assessment:1",
                    properties={"assessment_status": value},
                    depends_on=(),
                ),
            ),
            valid_time=api.KnowledgeValidTime("ORDER_ONLY", "capture:assessment"),
            supersedes=(),
        )

    before_refusal = history.path.read_bytes()
    with pytest.raises(api.PopulationAdmissionRefusal):
        api.check_and_admit_change_set(
            history=history,
            change_set=change("UNDECLARED"),
            transaction_time=TRANSACTION_TIME,
            actor_id=DECIDER,
        )
    assert history.path.read_bytes() == before_refusal
    admitted = api.check_and_admit_change_set(
        history=history,
        change_set=change("CONTESTED"),
        transaction_time=TRANSACTION_TIME,
        actor_id=DECIDER,
    ).replay
    # Reopen a ledger-only copy, not the live object's in-memory state.
    copied = tmp_path / "ledger-only.jsonl"
    copied.write_bytes(history.path.read_bytes())
    reopened = api.KnowledgeChangeHistory.reopen(copied).replay()
    assert reopened.receipt == admitted.receipt
    assert reopened.contract_revisions == revised.contract_revisions
    assert reopened.gap_answers == revised.gap_answers
    assert reopened.graph.query("Assessment")[0]["assessment_status"] == "CONTESTED"
    complement = reopened.graph.export_records()
    complement["entities"] = [
        record for record in complement["entities"] if record["id"] != "assessment:1"
    ]
    assert complement == records
    for record_id, prior in before.record_history.items():
        assert reopened.record_history[record_id] == prior


def test_new_enum_revision_stale_after_an_intervening_change(tmp_path):
    history, _, _ = _history(tmp_path)
    revision, _, _ = _compose_revision(
        history, api.compose_linkml_addition(BASE_SOURCE, ADDITION)
    )
    _admit(
        history,
        change_set_id="change:intervening",
        order="1",
        operations=(
            api.KnowledgeOperation(
                ordinal=0,
                operation_id="create:right",
                operation_type="CREATE_ENTITY",
                record_type="RightObject",
                record_id="right:1",
                properties={"label": "unchanged"},
                depends_on=(),
            ),
        ),
    )
    before = history.path.read_bytes()
    with pytest.raises(api.ContractRevisionRefusal) as caught:
        history.record_contract_revision(
            revision=revision, transaction_time=TRANSACTION_TIME, actor_id=DECIDER
        )
    assert caught.value.reason is api.ContractRevisionRefusalReason.STALE_BASE
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("mutation", ["remove_value", "change_range", "narrow_slot"])
def test_new_enum_does_not_license_changing_existing_meaning(tmp_path, mutation):
    history, _, _ = _history(tmp_path)
    source = api.compose_linkml_addition(BASE_SOURCE, ADDITION)
    if mutation == "remove_value":
        source = source.replace(b"OLD:", b"REPLACEMENT:")
    elif mutation == "change_range":
        source = source.replace(b"range: Stage", b"range: NewStatus")
    else:
        source = source.replace(
            b"    range: string\n", b"    range: string\n    equals_string: fixed\n"
        )
    before = history.path.read_bytes()
    with pytest.raises(api.ContractRevisionRefusal) as caught:
        _compose_revision(history, source)
    assert caught.value.reason is api.ContractRevisionRefusalReason.NON_ADDITIVE_CHANGE
    assert history.path.read_bytes() == before

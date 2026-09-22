"""RED contract for ROADMAP F2: a declared gap is a trigger, not a note.

A producer that meets a record the ontology cannot type declares a
``TYPE_ABSENT`` or ``RELATION_ABSENT`` gap. Until this contract, nothing
consumed it. These tests bind the whole answer: a gap has an identity derived
from its own bytes, a proposal answers named gaps and is refused at retention
unless it composes additively, acceptance is the revision in one act, refusal
closes the gaps with a reason and moves no ontology, and the replay reports the
open gaps with their open proposals.

Two consumers with different shapes run the same path: a population-plan
history, whose gaps artifact Core generates from a compiled plan, and a
change-set history, whose producer composes its own operations and retains its
gaps artifact itself.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

import malleus.compiler as compiler
from malleus._contract_pipeline import gap_answer, population
from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from tests.contract_compiler.pareto.test_governed_population import (
    NEUTRAL_PROFILE_DATA,
    _gaps_bytes,
    _prepare,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchor,
    _anchored_history,
    _digest,
    _event,
)
from tests.contract_compiler.pareto.test_linkml_addition import BASE, CLASS_FRAGMENT
from tests.contract_compiler.pareto.test_ontology_source_set import (
    _sources,
    run_probe,
)
from tests.contract_compiler.pareto.test_population_plan import _plan
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
)


DECIDER = "actor:ontology-owner"
BASE_SOURCE = BASE
ADDITION = CLASS_FRAGMENT.decode("utf-8")
EXISTING_CLASS_ADDITION = """\
classes:
  RightObject:
    is_a: Entity
    slots:
      - label
"""
UNCOMPILABLE_ADDITION = """\
classes:
  CustomerObject:
    is_a: NoSuchParentClass
    slots:
      - label
"""


def _gap(
    *,
    kind: str = "TYPE_ABSENT",
    statement: str = "the contract has no customer type",
    locator: str = "row:0",
) -> dict[str, str]:
    return {
        "kind": kind,
        "locator": locator,
        "source_id": "source-generic",
        "statement": statement,
    }


def _proposal_bytes(
    *,
    answers: tuple[str, ...],
    proposal_id: str = "proposal:customer",
    revision_id: str = "revision:customer",
    addition: str = ADDITION,
    reason: str = "the source names a customer the contract cannot type",
    issued_at: str = "2026-09-21T00:00:00Z",
) -> bytes:
    """A proposal as its owner writes it: a fragment, and no compiled artifact."""

    return _canonical(
        {
            "answers_gaps": sorted(answers),
            "grammar": compiler.ONTOLOGY_REVISION_PROPOSAL_GRAMMAR,
            "issued_at": issued_at,
            "linkml_addition": addition,
            "proposal_id": proposal_id,
            "reason": reason,
            "revision_id": revision_id,
        }
    )


def _retain_source(history: KnowledgeChangeHistory) -> None:
    history.retain_ontology_source(
        root_locator="generic",
        sources=_sources(BASE_SOURCE),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )


def _retain_proposal(history: KnowledgeChangeHistory, proposal: bytes) -> None:
    history.retain_ontology_revision_proposal(
        proposal_bytes=proposal,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )


def _plan_history(tmp_path: Path, *, gap: dict[str, str] | None = None):
    """Consumer one: a population-plan history whose plan declares a gap."""

    history, _, partial, _, source, evidence = _anchored_history(
        tmp_path, contract_source=BASE_SOURCE
    )
    _retain_source(history)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [gap or _gap()]
    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)
    assert prepared.change_set is not None
    compiler.check_and_admit_change_set(
        history=history,
        change_set=prepared.change_set,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    identity = compiler.ontology_gap_identity(
        gap=plan["gaps"][0], plan_id=plan["plan_id"]
    )
    return history, identity, plan


def _change_set_history(tmp_path: Path, *, gap: dict[str, str] | None = None):
    """Consumer two: a change-set history that retains its own gaps artifact."""

    history, _, _, _, _, _ = _anchored_history(
        tmp_path, contract_source=BASE_SOURCE
    )
    _retain_source(history)
    round_id = "round:change-set:1"
    declared = {"gaps": [gap or _gap()], "plan_id": round_id}
    gaps_artifact = _canonical(declared)
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id=f"{round_id}:gaps",
            artifact_identity=_digest(gaps_artifact),
        ),
        gaps_artifact,
        "RETAINED_EVIDENCE",
        media_type="application/json",
    )
    change = history.compose_change_set(
        change_set_id="change:composed:1",
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        operations=(
            KnowledgeOperation(
                operation_id="operation:1",
                ordinal=0,
                operation_type="CREATE_ENTITY",
                record_id="left-1",
                record_type="LeftObject",
                properties={"label": "left"},
                depends_on=(),
            ),
        ),
        valid_time=KnowledgeValidTime("ORDER_ONLY", "1"),
        supersedes=(),
    )
    compiler.check_and_admit_change_set(
        history=history,
        change_set=change,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    identity = compiler.ontology_gap_identity(gap=gap or _gap(), plan_id=round_id)
    return history, identity, declared


CONSUMERS = [
    pytest.param(_plan_history, id="population-plan"),
    pytest.param(_change_set_history, id="change-set"),
]


# --- gap identity ------------------------------------------------------------


def test_gap_identity_digests_the_canonical_gap_with_its_plan_id() -> None:
    gap = _gap()

    identity = compiler.ontology_gap_identity(gap=gap, plan_id="plan:neutral:1")

    expected = _canonical({"gap": gap, "plan_id": "plan:neutral:1"})
    assert identity == "sha256:" + sha256(expected).hexdigest()
    assert (
        compiler.ontology_gap_identity(
            gap=dict(reversed(list(gap.items()))), plan_id="plan:neutral:1"
        )
        == identity
    )
    assert compiler.ontology_gap_identity(gap=gap, plan_id="plan:neutral:2") != identity


def test_the_ontology_gap_kinds_are_the_two_the_ontology_can_answer() -> None:
    assert compiler.ONTOLOGY_GAP_KINDS == ("RELATION_ABSENT", "TYPE_ABSENT")
    assert set(compiler.ONTOLOGY_GAP_KINDS) < set(compiler.POPULATION_GAP_KINDS)


def test_the_proposal_and_answer_grammars_are_versioned() -> None:
    assert (
        compiler.ONTOLOGY_REVISION_PROPOSAL_GRAMMAR
        == "malleus.ontology-revision-proposal/v1"
    )
    assert compiler.ONTOLOGY_GAP_ANSWER_GRAMMAR == "malleus.ontology-gap-answer/v1"


# --- (a) an open gap ---------------------------------------------------------


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_open_gaps_lists_a_declared_gap_with_no_proposals(tmp_path, consumer) -> None:
    history, identity, plan = consumer(tmp_path)

    open_gaps = history.replay().open_gaps()

    assert len(open_gaps) == 1
    gap = open_gaps[0]
    assert gap.identity == identity
    assert gap.kind == "TYPE_ABSENT"
    assert gap.source_id == "source-generic"
    assert gap.locator == "row:0"
    assert gap.statement == "the contract has no customer type"
    assert gap.plan_id == plan["plan_id"]
    assert gap.open_proposals == ()


def test_a_gap_of_a_non_ontology_kind_is_not_reported(tmp_path) -> None:
    history, _, _ = _plan_history(
        tmp_path,
        gap=_gap(kind="AGGREGATE_ONLY", statement="the source states only a total"),
    )

    assert history.replay().open_gaps() == ()


# --- (b) a retained proposal is open against its gap -------------------------


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_a_retained_proposal_shows_as_open_against_its_gap(tmp_path, consumer) -> None:
    history, identity, _ = consumer(tmp_path)
    proposal = _proposal_bytes(answers=(identity,))

    _retain_proposal(history, proposal)

    open_gaps = history.replay().open_gaps()
    assert len(open_gaps) == 1
    assert len(open_gaps[0].open_proposals) == 1
    assert open_gaps[0].open_proposals[0].proposal_id == "proposal:customer"
    assert open_gaps[0].open_proposals[0].identity == _digest(proposal)


# --- (c) acceptance is the revision ------------------------------------------


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_acceptance_records_the_revision_and_closes_the_gap(tmp_path, consumer) -> None:
    history, identity, _ = consumer(tmp_path)
    proposal = _proposal_bytes(answers=(identity,))
    _retain_proposal(history, proposal)
    before = history.replay()
    records_before = before.graph.export_records()
    revisions_before = len(before.contract_revisions)

    replay = history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert replay.open_gaps() == ()
    assert len(replay.contract_revisions) == revisions_before + 1
    revision = replay.contract_revisions[-1]
    assert revision.revision_id == "revision:customer"
    assert {change.kind for change in revision.changes} == {"ADD_CLASS"}
    answer = replay.gap_answers[-1]
    assert answer.disposition == "ACCEPTED"
    assert answer.answered_gaps == (identity,)
    assert answer.deciding_actor == DECIDER
    assert answer.proposal_id == "proposal:customer"
    assert answer.revision_identity == revision.identity
    # The graph replays byte-identical; only the new class became available.
    assert replay.graph.export_records() == records_before
    assert not before.contract_view.has_type("CustomerObject")
    assert replay.contract_view.has_type("CustomerObject")
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.graph.export_records() == records_before
    assert reopened.open_gaps() == ()
    assert reopened.gap_answers[-1].canonical_bytes == answer.canonical_bytes


def test_acceptance_writes_the_revision_and_the_answer_in_one_batch(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    before = len(history.path.read_text().splitlines())

    history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    ledger = [json.loads(line) for line in history.path.read_text().splitlines()]
    assert len(ledger) == before + 2
    assert [event["event_type"] for event in ledger[-2:]] == [
        "CONTRACT_REVISION_RECORDED",
        "ONTOLOGY_GAP_ANSWER_RECORDED",
    ]


# --- (d) a second acceptance refuses -----------------------------------------


def test_a_second_acceptance_of_the_same_proposal_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.accept_ontology_revision_proposal(
            proposal_id="proposal:customer",
            deciding_actor=DECIDER,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.PROPOSAL_ALREADY_DECIDED
    )
    assert history.path.read_bytes() == before


def test_accepting_an_unknown_proposal_refuses(tmp_path) -> None:
    history, _, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.accept_ontology_revision_proposal(
            proposal_id="proposal:absent",
            deciding_actor=DECIDER,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason is compiler.OntologyGapAnswerRefusalReason.UNKNOWN_PROPOSAL
    )
    assert history.path.read_bytes() == before


def test_acceptance_without_a_deciding_actor_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.accept_ontology_revision_proposal(
            proposal_id="proposal:customer",
            deciding_actor="",
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.MISSING_DECIDING_ACTOR
    )
    assert history.path.read_bytes() == before


# --- (e) refusal closes the gap ----------------------------------------------


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_refusal_closes_the_gap_with_its_reason_and_records_no_revision(
    tmp_path, consumer
) -> None:
    history, identity, _ = consumer(tmp_path)
    before = history.replay()

    replay = history.refuse_ontology_gaps(
        gap_identities=(identity,),
        reason="the customer is out of scope for this ontology",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert replay.open_gaps() == ()
    assert len(replay.contract_revisions) == len(before.contract_revisions)
    assert replay.partial_contract.identity == before.partial_contract.identity
    answer = replay.gap_answers[-1]
    assert answer.disposition == "REFUSED"
    assert answer.answered_gaps == (identity,)
    assert answer.reason == "the customer is out of scope for this ontology"
    assert answer.deciding_actor == DECIDER
    assert answer.proposal_id is None
    assert answer.revision_identity is None


def test_refusal_without_a_deciding_actor_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.refuse_ontology_gaps(
            gap_identities=(identity,),
            reason="out of scope",
            deciding_actor="",
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.MISSING_DECIDING_ACTOR
    )
    assert history.path.read_bytes() == before


def test_a_refused_gap_cannot_be_answered_again(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    history.refuse_ontology_gaps(
        gap_identities=(identity,),
        reason="out of scope",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.refuse_ontology_gaps(
            gap_identities=(identity,),
            reason="again",
            deciding_actor=DECIDER,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.GAP_ALREADY_ANSWERED
    )
    assert history.path.read_bytes() == before


def test_refusing_an_unknown_gap_identity_refuses(tmp_path) -> None:
    history, _, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        history.refuse_ontology_gaps(
            gap_identities=("sha256:" + "0" * 64,),
            reason="out of scope",
            deciding_actor=DECIDER,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert refusal.value.reason is compiler.OntologyGapAnswerRefusalReason.UNKNOWN_GAP
    assert history.path.read_bytes() == before


# --- (f) a proposal that does not compile or is not additive -----------------


def test_a_non_additive_proposal_refuses_at_retention_and_writes_nothing(
    tmp_path,
) -> None:
    history, identity, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(
            history,
            _proposal_bytes(answers=(identity,), addition=EXISTING_CLASS_ADDITION),
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.PROPOSAL_NOT_ADDITIVE
    )
    # The composition rule refused first, and it says which rule it was.
    assert "EXISTING_CLASS" in refusal.value.detail
    assert history.path.read_bytes() == before
    assert history.replay().open_gaps()[0].open_proposals == ()


def test_a_proposal_that_does_not_compile_refuses_at_retention(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(
            history,
            _proposal_bytes(answers=(identity,), addition=UNCOMPILABLE_ADDITION),
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.PROPOSAL_DOES_NOT_COMPILE
    )
    assert history.path.read_bytes() == before


def test_a_proposal_whose_fields_are_not_closed_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()
    extra = json.loads(_proposal_bytes(answers=(identity,)))
    extra["note"] = "an undeclared field"

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(history, _canonical(extra))

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL
    )
    assert history.path.read_bytes() == before


def test_a_proposal_retained_under_another_record_id_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    proposal = _proposal_bytes(answers=(identity,))
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="some-other-id",
                artifact_identity=_digest(proposal),
            ),
            proposal,
            "RETAINED_EVIDENCE",
            media_type="application/json",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL
    )
    assert history.path.read_bytes() == before


# --- (g) a proposal against a gap of a non-ontology kind ---------------------


def test_a_proposal_against_an_aggregate_only_gap_refuses(tmp_path) -> None:
    history, _, plan = _plan_history(
        tmp_path,
        gap=_gap(kind="AGGREGATE_ONLY", statement="the source states only a total"),
    )
    identity = compiler.ontology_gap_identity(
        gap=plan["gaps"][0], plan_id=plan["plan_id"]
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(history, _proposal_bytes(answers=(identity,)))

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.GAP_KIND_NOT_ONTOLOGY
    )
    assert history.path.read_bytes() == before


def test_a_proposal_naming_an_unknown_gap_identity_refuses(tmp_path) -> None:
    history, _, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(history, _proposal_bytes(answers=("sha256:" + "1" * 64,)))

    assert refusal.value.reason is compiler.OntologyGapAnswerRefusalReason.UNKNOWN_GAP
    assert history.path.read_bytes() == before


def test_a_proposal_against_an_already_answered_gap_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    history.refuse_ontology_gaps(
        gap_identities=(identity,),
        reason="out of scope",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(history, _proposal_bytes(answers=(identity,)))

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.GAP_ALREADY_ANSWERED
    )
    assert history.path.read_bytes() == before


# --- the proposal is born a fragment -----------------------------------------


def test_a_proposal_carries_the_fragment_and_no_compiled_artifact() -> None:
    proposal = json.loads(_proposal_bytes(answers=("sha256:" + "0" * 64,)))

    assert set(proposal) == {
        "answers_gaps",
        "grammar",
        "issued_at",
        "linkml_addition",
        "proposal_id",
        "reason",
        "revision_id",
    }
    assert proposal["linkml_addition"] == ADDITION


def test_a_proposal_that_supplies_its_own_target_refuses(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    supplied = json.loads(_proposal_bytes(answers=(identity,)))
    supplied["target"] = {"partial_contract": {}, "validated_contract": {}}
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(history, _canonical(supplied))

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL
    )
    assert "target" in refusal.value.detail
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_core_derives_and_retains_the_target_the_proposer_did_not_supply(
    tmp_path, consumer
) -> None:
    history, identity, _ = consumer(tmp_path)
    proposal = _proposal_bytes(answers=(identity,))
    current = history.replay().ontology_source_set()

    _retain_proposal(history, proposal)

    replay = history.replay()
    target = replay.ontology_revision_target("proposal:customer")
    assert target.proposal_identity == _digest(proposal)
    assert target.source_set_identity == current.identity
    # The composed root is in the history, and it is the base plus the fragment.
    composed = compiler.compose_linkml_addition(
        BASE_SOURCE, ADDITION.encode("utf-8")
    )
    assert _digest(composed) == target.composed_root_sha256
    assert replay.retained_bytes(
        f"ontology-source:{target.composed_root_sha256}"
    ) == composed


def test_a_proposal_against_a_history_with_no_retained_source_refuses(
    tmp_path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(
        tmp_path, contract_source=BASE_SOURCE
    )
    plan = _plan(partial.identity, source_identity=source, evidence_identity=evidence)
    plan["gaps"] = [_gap()]
    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)
    assert prepared.change_set is not None
    compiler.check_and_admit_change_set(
        history=history,
        change_set=prepared.change_set,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    identity = compiler.ontology_gap_identity(
        gap=plan["gaps"][0], plan_id=plan["plan_id"]
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as refusal:
        _retain_proposal(history, _proposal_bytes(answers=(identity,)))

    assert (
        refusal.value.reason
        is compiler.OntologySourceRefusalReason.ONTOLOGY_SOURCE_NOT_RETAINED
    )
    assert history.path.read_bytes() == before


def test_a_proposal_retained_without_a_derived_target_refuses(tmp_path) -> None:
    """The ordinary anchor door cannot slip a proposal past the derivation."""

    history, identity, _ = _plan_history(tmp_path)
    proposal = _proposal_bytes(answers=(identity,))
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="proposal:customer",
                artifact_identity=_digest(proposal),
            ),
            proposal,
            "RETAINED_EVIDENCE",
            media_type="application/json",
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.PROPOSAL_TARGET_NOT_DERIVED
    )
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_acceptance_makes_the_composed_root_the_current_source(
    tmp_path, consumer
) -> None:
    history, identity, _ = consumer(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    composed = compiler.compose_linkml_addition(
        BASE_SOURCE, ADDITION.encode("utf-8")
    )

    replay = history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    source_set = replay.ontology_source_set()
    assert source_set is not None
    assert source_set.root_sha256 == _digest(composed)
    assert source_set.validated_contract_identity == (
        replay.partial_contract.validated_fact_set_sha256
    )
    assert replay.ontology_source_bytes("generic") == composed


def test_a_second_proposal_composes_onto_the_first_acceptance(tmp_path) -> None:
    history, identity, _ = _plan_history(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    history.accept_ontology_revision_proposal(
        proposal_id="proposal:customer",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    second = _canonical(
        {
            "gaps": [_gap(statement="no type for the referral agent")],
            "plan_id": "round:second",
        }
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="round:second:gaps",
            artifact_identity=_digest(second),
        ),
        second,
        "RETAINED_EVIDENCE",
        media_type="application/json",
    )
    next_identity = compiler.ontology_gap_identity(
        gap=json.loads(second)["gaps"][0], plan_id="round:second"
    )

    _retain_proposal(
        history,
        _proposal_bytes(
            answers=(next_identity,),
            proposal_id="proposal:referral",
            revision_id="revision:referral",
            addition="classes:\n  ReferralObject:\n    is_a: Entity\n",
        ),
    )
    replay = history.accept_ontology_revision_proposal(
        proposal_id="proposal:referral",
        deciding_actor=DECIDER,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert replay.contract_view.has_type("CustomerObject")
    assert replay.contract_view.has_type("ReferralObject")
    assert len(replay.contract_revisions) == 2
    assert replay.open_gaps() == ()


def test_a_fragment_importing_a_module_the_source_set_lacks_refuses(
    tmp_path,
) -> None:
    """The composition rule allows a new import; the retained map must carry it."""

    history, identity, _ = _plan_history(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologyGapAnswerRefusal) as refusal:
        _retain_proposal(
            history,
            _proposal_bytes(
                answers=(identity,), addition="imports:\n  - not-in-the-source-set\n"
            ),
        )

    assert (
        refusal.value.reason
        is compiler.OntologyGapAnswerRefusalReason.PROPOSAL_DOES_NOT_COMPILE
    )
    assert history.path.read_bytes() == before


def test_two_proposals_composing_to_the_same_contract_both_retain(
    tmp_path,
) -> None:
    """One digest is one record, and a shared derivation is not a collision."""

    history, identity, _ = _plan_history(tmp_path)
    second = _canonical(
        {
            "gaps": [_gap(statement="the contract has no customer type either")],
            "plan_id": "round:second",
        }
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="round:second:gaps",
            artifact_identity=_digest(second),
        ),
        second,
        "RETAINED_EVIDENCE",
        media_type="application/json",
    )
    other = compiler.ontology_gap_identity(
        gap=json.loads(second)["gaps"][0], plan_id="round:second"
    )

    _retain_proposal(history, _proposal_bytes(answers=(identity,)))
    _retain_proposal(
        history,
        _proposal_bytes(
            answers=(other,),
            proposal_id="proposal:customer-again",
            revision_id="revision:customer-again",
        ),
    )

    replay = history.replay()
    first = replay.ontology_revision_target("proposal:customer")
    again = replay.ontology_revision_target("proposal:customer-again")
    assert first.composed_root_sha256 == again.composed_root_sha256
    assert first.source_set_identity == again.source_set_identity
    assert first.identity != again.identity
    assert [gap.plan_id for gap in replay.open_gaps()] == [
        "plan:neutral:1",
        "round:second",
    ]


def test_acceptance_and_replay_need_no_compiler(tmp_path) -> None:
    """The proposer needs a compiler for retention; nobody else needs one."""

    history, identity, _ = _plan_history(tmp_path)
    _retain_proposal(history, _proposal_bytes(answers=(identity,)))

    finished = run_probe(
        "from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory\n"
        f"history = KnowledgeChangeHistory.reopen({str(history.path)!r})\n"
        "replay = history.accept_ontology_revision_proposal(\n"
        "    proposal_id='proposal:customer',\n"
        f"    deciding_actor={DECIDER!r},\n"
        f"    transaction_time={TRANSACTION_TIME!r},\n"
        "    actor_id='actor:test',\n"
        ")\n"
        "assert replay.open_gaps() == ()\n"
        "assert len(replay.contract_revisions) == 1\n"
    )

    assert finished.returncode == 0, finished.stderr
    assert finished.stdout.strip() == ""


# --- determinism and closure -------------------------------------------------


def test_open_gaps_is_sorted_and_repeatable(tmp_path) -> None:
    history, _, _ = _plan_history(tmp_path)
    second = _canonical(
        {
            "gaps": [
                _gap(statement="no relation for the referral", kind="RELATION_ABSENT"),
                _gap(statement="no type for the referral agent"),
            ],
            "plan_id": "round:second",
        }
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="round:second:gaps",
            artifact_identity=_digest(second),
        ),
        second,
        "RETAINED_EVIDENCE",
        media_type="application/json",
    )

    first_read = history.replay().open_gaps()
    second_read = KnowledgeChangeHistory.reopen(history.path).replay().open_gaps()

    assert len(first_read) == 3
    assert first_read == second_read
    assert list(first_read) == sorted(
        first_read, key=lambda gap: (gap.plan_id, gap.identity)
    )


def test_the_gaps_artifact_bytes_are_unchanged_by_this_contract(tmp_path) -> None:
    """F2 reads the gaps artifact; it does not move one byte of it."""

    _, _, plan = _plan_history(tmp_path)

    assert _gaps_bytes(plan) == _canonical(
        {"gaps": plan["gaps"], "plan_id": plan["plan_id"]}
    )
    assert set(plan["gaps"][0]) == {"kind", "locator", "source_id", "statement"}
    # The plan compiled and was retained, so population accepted exactly this
    # field set. Two modules hold the literal; this holds them to one value.
    assert gap_answer.GAP_FIELDS == set(plan["gaps"][0])


def test_population_gap_kinds_are_untouched() -> None:
    assert population.POPULATION_GAP_KINDS == (
        "AGGREGATE_ONLY",
        "INTERVAL_NOT_EXPRESSIBLE",
        "MODALITY_NOT_EXPRESSIBLE",
        "RELATION_ABSENT",
        "REQUIRED_FIELD_ABSENT_IN_SOURCE",
        "TYPE_ABSENT",
    )


def test_the_contract_revision_policy_identity_is_unmoved() -> None:
    """F2 adds no change kind, so the content-addressed policy cannot move."""

    assert compiler.CONTRACT_REVISION_POLICY.change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_IMPORT",
        "ADD_SLOT",
        "REBIND_CHECK_CONTRACT",
    )

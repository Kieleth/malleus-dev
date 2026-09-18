"""One Small Shop history carries its rule layer across an additive revision.

The census under ``private/shop-progressive-01/census/revision-01`` (paper
ledger E-0458) found the dead end this module pins. A ``PolicyProgram`` whose
required check is a Prolog ``LogicContract`` binds the compiled ontology inside
the check contract's own digest. Re-pinning the same rule bytes to the revised
ontology therefore moves the check contract identity, the policy, and the
normative profile, and the revision refused. Keeping the old pin left every
later check unable to run. Both refusals are correct alone; together an adopter
with a rule layer could never grow its ontology.

A revision may now declare that re-binding. The negative controls below are the
boundary: changed rule bytes, an added check and a changed verdict still refuse.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as compiler
from malleus.kg import KnowledgeGraph
from malleus.logic import LogicContract, LogicError
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph

from tests.contract_compiler.pareto.test_public_compiler import (
    SHOP_BASE,
    SHOP_FIXTURE,
    SHOP_RUNTIME,
    TRANSACTION_TIME,
    _anchor,
    _bootstrap,
    _canonical,
    _digest,
    _event,
    _protocol_events,
)
from tests.contract_compiler.pareto.test_small_shop_contract_revision import (
    BASE_INPUT,
    REVISION_TARGET,
    _admit_ret010,
    _compile,
    _retain_source,
)


RULES = b"""\
malleus_rule('NO_EMPTY_RECORD').

% A record of any kind carries no property at all.
malleus_violation('NO_EMPTY_RECORD', 'RECORD_WITHOUT_PROPERTIES', [Record]) :-
    m_record(Record, _, _),
    \\+ m_property(Record, _, _, _).
"""
OTHER_RULES = b"""\
malleus_rule('NO_EMPTY_RECORD').

% The same rule, written over m_type instead of m_record. Different bytes.
malleus_violation('NO_EMPTY_RECORD', 'RECORD_WITHOUT_PROPERTIES', [Record]) :-
    m_record(Record, Type, _),
    m_type(Type),
    \\+ m_property(Record, _, _, _).
"""
CHECK_ID = "shop-content-rules"
POLICY_REF = "required-check-verdict"


def _ontology_hash(compiled) -> str:
    return "sha256:" + compiled.view.content_hash()


def _logic(directory: Path, ontology_hash: str, rules: bytes = RULES) -> LogicContract:
    """Write and load one pinned rule contract, the way an adopter retains it."""

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "rules.pl").write_bytes(rules)
    (directory / "logic.yaml").write_text(
        "schema_version: '1'\n"
        f"contract_id: {CHECK_ID}\n"
        "contract_version: '1'\n"
        f"ontology_hash: {ontology_hash}\n"
        "fact_contract_version: '2'\n"
        f"ruleset_id: {CHECK_ID}\n"
        "ruleset_version: '1'\n"
        "rules_file: rules.pl\n"
        "rule_ids: [NO_EMPTY_RECORD]\n"
        "timeout_seconds: 10\n",
        encoding="utf-8",
    )
    return LogicContract.load(directory / "logic.yaml")


def _descriptor(contract: LogicContract) -> dict[str, object]:
    """The exact semantic fields whose canonical digest is ``contract_hash``."""

    return {
        "schema_version": contract.schema_version,
        "contract_id": contract.contract_id,
        "contract_version": contract.contract_version,
        "ontology_hash": contract.ontology_hash,
        "fact_contract_version": contract.fact_contract_version,
        "ruleset_id": contract.ruleset_id,
        "ruleset_version": contract.ruleset_version,
        "rule_ids": sorted(contract.rule_ids),
        "timeout_seconds": contract.timeout_seconds,
        "ruleset_hash": contract.ruleset_hash,
    }


def _policy(
    checks: tuple[tuple[str, str], ...],
    *,
    outcome_verdicts: dict[str, str] | None = None,
    precedence: list[str] | None = None,
) -> compiler.PolicyProgram:
    verdicts = outcome_verdicts or {
        "SATISFIED": "ACCEPT",
        "UNKNOWN": "DEFER",
        "VIOLATED": "REJECT",
    }
    return compiler.PolicyProgram.from_bytes(
        _canonical(
            {
                "grammar": "malleus.policy-program/private-v0",
                "outcome_verdicts": verdicts,
                "policy_id": "shop-content-rule-policy",
                "precedence": precedence or ["REJECT", "DEFER", "ACCEPT"],
                "required_checks": [
                    {
                        "check_contract_id": check_id,
                        "check_contract_identity": identity,
                    }
                    for check_id, identity in checks
                ],
            }
        )
    )


def _profile(policy: compiler.PolicyProgram):
    machine = compiler.ProtocolMachineProgram.from_bytes(
        (SHOP_RUNTIME / "machine.json").read_bytes()
    )
    return compiler.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={POLICY_REF: policy},
        capability_refs=(),
    )


def _history(tmp_path: Path):
    """The Shop history up to the point the census reached: one accepted change.

    Its single required check is the pinned rule contract, exactly the shape
    the Shop's stage-B history carries.
    """

    base = _compile(SHOP_BASE.read_bytes())
    logic = _logic(tmp_path / "rules-base", _ontology_hash(base))
    policy = _policy(((CHECK_ID, logic.contract_hash),))
    partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=base.artifact.validated_fact_set_sha256,
        normative_profile=_profile(policy),
    )
    mapping = json.loads((SHOP_RUNTIME / "mapping.json").read_bytes())
    binding = compiler.KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(mapping["history_binding"])
    )
    history = compiler.KnowledgeChangeHistory(
        tmp_path / "shop-rebinding-history.jsonl",
        partial_contract=partial,
        contract_view=base.view,
        binding=binding,
    )
    supplier_source = (
        SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl"
    ).read_bytes()
    _bootstrap(compiler, history, base, partial, supplier_source)
    mapping_bytes = (SHOP_RUNTIME / "mapping.json").read_bytes()
    _retain_source(
        history,
        artifact_id="artifact:ret010-source:warehouse",
        source_id="source:ret010:warehouse",
        content=(BASE_INPUT / "sources/warehouse.jsonl").read_bytes(),
    )
    _retain_source(
        history,
        artifact_id="artifact:ret010-source:inventory",
        source_id="source:ret010:inventory",
        content=(BASE_INPUT / "sources/inventory-units.csv").read_bytes(),
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="artifact:ret010-mapping",
            artifact_identity=_digest(mapping_bytes),
        ),
        mapping_bytes,
        "RETAINED_EVIDENCE",
    )
    accepted = _admit_ret010(history, policy, mapping)
    return history, base, partial, policy, logic, accepted


def _target(tmp_path: Path, *, rules: bytes = RULES):
    """The revised ontology and the same rule bytes re-pinned to it."""

    target = _compile(REVISION_TARGET.read_bytes())
    logic = _logic(tmp_path / "rules-target", _ontology_hash(target), rules)
    return target, logic


def _revise(
    history,
    target,
    partial,
    profile,
    *,
    descriptors,
    revision_id: str = "revision:shop:rebind",
    reason: str = "add supplier-order state vocabulary and re-pin the rule layer",
):
    target_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=profile,
    )
    extra = {"check_contract_descriptors": descriptors} if descriptors else {}
    revision = history.compose_contract_revision(
        revision_id=revision_id,
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=target_partial.canonical_bytes,
        reason=reason,
        issued_at=TRANSACTION_TIME,
        **extra,
    )
    return revision, target_partial


def _admit_new_class(history, partial, policy, occurrence: str):
    """Admit one record of the added class under the current required checks."""

    before = history.replay()
    change = history.compose_change_set(
        change_set_id=f"change:rebind:{occurrence}",
        source_record_ids=("source:supplier-order-history",),
        evidence_record_ids=("artifact:ret010-mapping",),
        operations=(
            compiler.KnowledgeOperation(
                ordinal=0,
                operation_id=f"operation:rebind:{occurrence}",
                operation_type="CREATE_ENTITY",
                record_type="SupplierOrderState",
                record_id=f"supplier-order-state:B:{occurrence}",
                properties={
                    "product_code": "Y",
                    "ordered_quantity": 2,
                    "supplier_order_id": "B",
                    "source_occurrence_id": occurrence,
                },
                depends_on=(),
                source_id=None,
                target_id=None,
            ),
        ),
        valid_time=compiler.KnowledgeValidTime("INSTANT", "2026-02-02T00:00:00Z"),
        supersedes=(),
    )
    return (
        history.admit(
            change_set=change,
            machine_events=_protocol_events(
                policy, change, before.machine_state.identity, occurrence
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:public-adopter",
        ),
        change,
    )


def _candidate(graph: KnowledgeGraph, occurrence: str):
    return stage_subgraph(
        graph,
        [
            ProposedOperation(
                op_type="CREATE_ENTITY",
                record_type="SupplierOrderState",
                record_id=f"supplier-order-state:B:{occurrence}",
                properties={
                    "product_code": "Y",
                    "ordered_quantity": 2,
                    "supplier_order_id": "B",
                    "source_occurrence_id": occurrence,
                },
            )
        ],
    )


# --- today's two refusals, which stay refusals --------------------------------


def test_an_undeclared_profile_change_still_refuses_the_revision(
    tmp_path: Path,
) -> None:
    """A profile that moved for any reason the revision did not declare refuses.

    This is the guard the census hit. It passes before and after this change
    and discriminates nothing on its own; it is here so the narrowing is
    visible.
    """

    history, _, partial, _, _ = _history(tmp_path)[:5]
    target, repinned = _target(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(_policy(((CHECK_ID, repinned.contract_hash),))),
            descriptors={},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        "domain revision changes the normative protocol profile"
    )
    assert history.path.read_bytes() == before


@pytest.mark.skipif(
    shutil.which("swipl") is None, reason="SWI-Prolog executable is not available"
)
def test_the_old_pin_cannot_check_the_revised_graph_and_the_new_pin_can(
    tmp_path: Path,
) -> None:
    """The second census refusal, isolated over one staged candidate.

    Core runs no Prolog. This asserts the adopter-side fact that forced the
    capability: once the ontology moves, the contract pinned to the old one
    cannot execute at all, so no further change could ever be admitted.
    """

    history, base, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    revised_graph = KnowledgeGraph.from_records(
        target.view, history.replay().graph.export_records()
    )
    candidate = _candidate(revised_graph, "e7")
    assert candidate.valid

    with pytest.raises(LogicError) as refusal:
        PrologVerifier(logic).verify_candidate_subgraph(candidate)

    assert str(refusal.value) == (
        "Logic contract and compiled facts use different ontologies"
    )
    assert logic.ruleset_hash == repinned.ruleset_hash
    result = PrologVerifier(repinned).verify_candidate_subgraph(candidate)
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


# --- the declared re-binding --------------------------------------------------


def test_a_revision_carries_the_re_pinned_check_contract_and_later_checks_run(
    tmp_path: Path,
) -> None:
    history, base, partial, policy, logic, accepted = _history(tmp_path)
    target, repinned = _target(tmp_path)
    repinned_policy = _policy(((CHECK_ID, repinned.contract_hash),))

    revision, target_partial = _revise(
        history,
        target,
        partial,
        _profile(repinned_policy),
        descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    admitted, change = _admit_new_class(history, target_partial, repinned_policy, "e7")
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    rebinding = revision.check_rebinding
    assert rebinding is not None
    assert rebinding.from_normative_profile_identity == (
        partial.normative_profile.identity
    )
    assert rebinding.to_normative_profile_identity == (
        target_partial.normative_profile.identity
    )
    assert tuple(
        (item.check_contract_id, item.from_identity, item.to_identity)
        for item in rebinding.checks
    ) == ((CHECK_ID, logic.contract_hash, repinned.contract_hash),)
    assert rebinding.checks[0].rebound_field == "ontology_hash"
    assert rebinding.checks[0].from_check_contract == _descriptor(logic)
    assert rebinding.checks[0].to_check_contract == _descriptor(repinned)
    assert rebinding.checks[0].unchanged_fields_digest == _digest(
        _canonical(
            {
                key: value
                for key, value in _descriptor(logic).items()
                if key != "ontology_hash"
            }
        )
    )
    assert (
        "REBIND_CHECK_CONTRACT",
        CHECK_ID,
        repinned.contract_hash,
    ) in tuple((item.kind, item.subject, item.value) for item in revision.changes)
    assert {item.kind for item in revision.changes} == {
        "ADD_CLASS",
        "ADD_SLOT",
        "REBIND_CHECK_CONTRACT",
    }

    assert reopened.contract_revisions == (revision,)
    assert reopened.partial_contract.identity == target_partial.identity
    assert reopened.required_checks[POLICY_REF] == ((CHECK_ID, repinned.contract_hash),)
    assert tuple(item.contract_identity for item in reopened.change_sets) == (
        accepted.contract_identity,
        target_partial.identity,
    )
    assert accepted.contract_identity == partial.identity
    assert reopened.change_sets[-1].identity == change.identity
    assert reopened.graph.query("SupplierOrderState") == [
        {
            "id": "supplier-order-state:B:e7",
            "ordered_quantity": 2,
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "supplier_order_id": "B",
            "type": "SupplierOrderState",
        }
    ]
    assert reopened.receipt == admitted.receipt


def test_the_earlier_check_receipts_keep_the_identity_they_were_recorded_under(
    tmp_path: Path,
) -> None:
    """Archival verification does not move when the live selection does."""

    history, _, partial, policy, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    before = tuple(
        record
        for record in history.replay().machine_state.records
        if record.record_type == "CheckRecord"
    )
    assert before

    revision, target_partial = _revise(
        history,
        target,
        partial,
        _profile(_policy(((CHECK_ID, repinned.contract_hash),))),
        descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    after = tuple(
        record
        for record in reopened.machine_state.records
        if record.record_type == "CheckRecord"
    )
    assert after == before
    assert {record.fields["check_contract_identity"] for record in after} == {
        logic.contract_hash
    }
    assert {record.fields["outcome"] for record in after} == {"SATISFIED"}
    assert reopened.required_checks[POLICY_REF] == ((CHECK_ID, repinned.contract_hash),)


@pytest.mark.skipif(
    shutil.which("swipl") is None, reason="SWI-Prolog executable is not available"
)
def test_after_the_revision_the_history_names_the_contract_a_runner_must_load(
    tmp_path: Path,
) -> None:
    """The accessor an adopter runner reads instead of a fixed retained ID."""

    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    revision, _ = _revise(
        history,
        target,
        partial,
        _profile(_policy(((CHECK_ID, repinned.contract_hash),))),
        descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    selected = dict(reopened.required_checks[POLICY_REF])[CHECK_ID]
    assert selected == repinned.contract_hash
    assert selected != logic.contract_hash
    loaded = {contract.contract_hash: contract for contract in (logic, repinned)}[
        selected
    ]
    result = PrologVerifier(loaded).verify_candidate_subgraph(
        _candidate(reopened.graph, "e7")
    )
    assert result.outcome == "SATISFIED"


# --- the negative controls ----------------------------------------------------


def test_a_revision_that_changes_rule_bytes_refuses_and_writes_nothing(
    tmp_path: Path,
) -> None:
    history, _, partial, _, logic, _ = _history(tmp_path)
    target, other = _target(tmp_path, rules=OTHER_RULES)
    assert other.ruleset_hash != logic.ruleset_hash
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(_policy(((CHECK_ID, other.contract_hash),))),
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(other))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        f"check contract {CHECK_ID} changes fields beyond its ontology binding: "
        "ruleset_hash"
    )
    assert refusal.value.change_kind == "REBIND_CHECK_CONTRACT"
    assert history.path.read_bytes() == before


def test_a_revision_that_adds_a_required_check_refuses_and_writes_nothing(
    tmp_path: Path,
) -> None:
    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    added = "sha256:" + "a" * 64
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(
                _policy(
                    (
                        (CHECK_ID, repinned.contract_hash),
                        ("structural-conformance", added),
                    )
                )
            ),
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        "domain revision changes the required checks of policy "
        "shop-content-rule-policy: structural-conformance"
    )
    assert history.path.read_bytes() == before


def test_a_revision_that_changes_a_verdict_refuses_and_writes_nothing(
    tmp_path: Path,
) -> None:
    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(
                _policy(
                    ((CHECK_ID, repinned.contract_hash),),
                    outcome_verdicts={
                        "SATISFIED": "ACCEPT",
                        "UNKNOWN": "ACCEPT",
                        "VIOLATED": "REJECT",
                    },
                    precedence=["REJECT", "ACCEPT"],
                )
            ),
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        "domain revision changes the outcome verdicts of policy "
        "shop-content-rule-policy"
    )
    assert history.path.read_bytes() == before


def test_a_descriptor_that_does_not_reproduce_the_pinned_identity_refuses(
    tmp_path: Path,
) -> None:
    """The declared proof is checked, not trusted."""

    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    lying = dict(_descriptor(repinned))
    lying["timeout_seconds"] = 11
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(_policy(((CHECK_ID, repinned.contract_hash),))),
            descriptors={CHECK_ID: (_descriptor(logic), lying)},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.IDENTITY_MISMATCH
    )
    assert refusal.value.detail == (
        f"declared check contract {CHECK_ID} does not hash to the identity the "
        "target policy requires"
    )
    assert history.path.read_bytes() == before


def test_a_rebinding_to_an_ontology_other_than_the_targets_refuses(
    tmp_path: Path,
) -> None:
    """The one field that may move must move to this revision's own ontology."""

    history, base, partial, _, logic, _ = _history(tmp_path)
    target, _ = _target(tmp_path)
    elsewhere = _logic(tmp_path / "rules-elsewhere", "sha256:" + "b" * 64)
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(_policy(((CHECK_ID, elsewhere.contract_hash),))),
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(elsewhere))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        f"check contract {CHECK_ID} does not rebind ontology_hash to the target "
        "ontology"
    )
    assert history.path.read_bytes() == before


def test_a_declared_rebinding_no_policy_asks_for_refuses(tmp_path: Path) -> None:
    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            partial.normative_profile,
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        f"revision declares a re-binding of {CHECK_ID} that no policy requires"
    )
    assert history.path.read_bytes() == before


def test_a_profile_change_the_field_walk_cannot_see_still_refuses(
    tmp_path: Path,
) -> None:
    """Undoing the declared re-binding must reproduce the current profile.

    A policy names its identifier under a key of the adopter's choosing. Two
    policies can therefore carry the same identifier under different keys, so
    the field-by-field comparison sees nothing while the bytes differ. The
    closing byte comparison is what refuses it; the field walk exists to name
    what moved, not to be the authority.
    """

    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    renamed = compiler.PolicyProgram.from_bytes(
        _canonical(
            {
                "grammar": "malleus.policy-program/private-v0",
                "outcome_verdicts": {
                    "SATISFIED": "ACCEPT",
                    "UNKNOWN": "DEFER",
                    "VIOLATED": "REJECT",
                },
                "name": "shop-content-rule-policy",
                "precedence": ["REJECT", "DEFER", "ACCEPT"],
                "required_checks": [
                    {
                        "check_contract_id": CHECK_ID,
                        "check_contract_identity": repinned.contract_hash,
                    }
                ],
            }
        )
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        _revise(
            history,
            target,
            partial,
            _profile(renamed),
            descriptors={CHECK_ID: (_descriptor(logic), _descriptor(repinned))},
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT
    )
    assert refusal.value.detail == (
        "domain revision changes the normative protocol profile beyond the "
        "declared re-binding"
    )
    assert history.path.read_bytes() == before


def test_the_revision_policy_declares_the_new_change_kind() -> None:
    assert compiler.CONTRACT_REVISION_POLICY.change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_IMPORT",
        "ADD_SLOT",
        "REBIND_CHECK_CONTRACT",
    )
    assert compiler.CONTRACT_REVISION_POLICY.admitted_change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_SLOT",
        "REBIND_CHECK_CONTRACT",
    )


def test_both_revision_policies_stay_supported_so_recorded_revisions_replay(
    tmp_path: Path,
) -> None:
    """A ledger written before this change carries the superseded policy.

    Adding the change kind moves the revision policy's own digest. The policy
    a revision declares is the policy Core executes for it, so an ontology-only
    revision recorded under the superseded policy still replays.
    """

    superseded, current = compiler.SUPPORTED_CONTRACT_REVISION_POLICIES
    assert superseded.change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_IMPORT",
        "ADD_SLOT",
    )
    assert current is compiler.CONTRACT_REVISION_POLICY
    assert superseded.identity != current.identity

    history, _, partial, policy, _, _ = _history(tmp_path)
    target, _ = _target(tmp_path)
    target_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=partial.normative_profile,
    )
    revision = compiler.compile_contract_revision(
        revision_id="revision:shop:ontology-only",
        base_ledger_head=history.replay().ledger_head,
        base_ledger_event_count=history.replay().ledger_event_count,
        base_acceptance_head=history.replay().acceptance_head,
        base_materialization_head=history.replay().materialization_head,
        base_accepted_state_digest=history.replay().graph.state_digest(),
        current_validated_contract_bytes=history.replay().contract_view.artifact_bytes,
        current_partial_contract_bytes=partial.canonical_bytes,
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=target_partial.canonical_bytes,
        reason="an ontology-only revision under the superseded policy",
        issued_at=TRANSACTION_TIME,
        policy=superseded,
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:public-adopter",
    )
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    assert revision.policy_identity == superseded.identity
    assert reopened.contract_revisions == (revision,)
    assert revision.check_rebinding is None
    assert (
        reopened.required_checks[POLICY_REF]
        == partial.normative_profile.policy(POLICY_REF).required_checks
    )


def test_the_superseded_policy_cannot_carry_a_re_binding(tmp_path: Path) -> None:
    superseded, _ = compiler.SUPPORTED_CONTRACT_REVISION_POLICIES
    history, _, partial, _, logic, _ = _history(tmp_path)
    target, repinned = _target(tmp_path)
    target_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=_profile(_policy(((CHECK_ID, repinned.contract_hash),))),
    )
    replay = history.replay()
    before = history.path.read_bytes()

    with pytest.raises(compiler.ContractRevisionRefusal) as refusal:
        compiler.compile_contract_revision(
            revision_id="revision:shop:rebind-under-old-policy",
            base_ledger_head=replay.ledger_head,
            base_ledger_event_count=replay.ledger_event_count,
            base_acceptance_head=replay.acceptance_head,
            base_materialization_head=replay.materialization_head,
            base_accepted_state_digest=replay.graph.state_digest(),
            current_validated_contract_bytes=replay.contract_view.artifact_bytes,
            current_partial_contract_bytes=partial.canonical_bytes,
            target_validated_contract_bytes=target.artifact.artifact_bytes,
            target_partial_contract_bytes=target_partial.canonical_bytes,
            reason="re-pin under a policy that does not declare the kind",
            issued_at=TRANSACTION_TIME,
            check_contract_descriptors={
                CHECK_ID: (_descriptor(logic), _descriptor(repinned))
            },
            policy=superseded,
        )

    assert refusal.value.reason is (
        compiler.ContractRevisionRefusalReason.MALFORMED_REVISION
    )
    assert refusal.value.change_kind == "REBIND_CHECK_CONTRACT"
    assert history.path.read_bytes() == before

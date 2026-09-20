"""Compile, check and admit one population plan as one Core operation.

ROADMAP F1, ruled on 2026-09-19 (paper ledger E-0486, E-0488). Two shipped
consumers wrote the same sequence by hand: the Shop experiment's runner at
``private/shop-progressive-01/producer/workspace-stage-c/runner.py`` and the
document path at ``paper-v4/experiment-v4/content-rules-doc-02/admit.py``.
They differ in machine program, history profile, fact contract version and
provenance, so the operation is written against both shapes and not against
either one.

The first two tests are the measurement nobody had taken: what Core does today
when a producer admits under an installed policy without running the check.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

import malleus.compiler as compiler
from malleus.logic import LogicContract, RetainedSourceText

from tests.contract_compiler.pareto.test_check_contract_rebinding import (
    CHECK_ID,
    POLICY_REF,
    _descriptor,
    _history,
    _policy,
    _profile,
    _revise,
    _target,
)
from tests.contract_compiler.pareto.test_public_compiler import (
    SHOP_RUNTIME,
    TRANSACTION_TIME,
    _canonical,
    _digest,
    _event,
)
from tests.contract_compiler.pareto.test_small_shop_contract_revision import (
    REVISION_TARGET,
    _compile,
    _retain_source,
)


ACTOR = "actor:public-adopter"
PACKET = (
    b'{"event_id":"e1","supplier_order_id":"B","product_code":"Y","quantity":2}\n'
    b'{"event_id":"e2","supplier_order_id":"B","product_code":"Y","quantity":5}\n'
)
SOURCE_ID = "source:packet"
QUANTITY_RULES = b"""\
malleus_rule('NO_CONFLICTING_QUANTITY').

% Two current records state a different quantity for the same order and product.
malleus_violation('NO_CONFLICTING_QUANTITY', 'QUANTITY_DISAGREEMENT', [A, B]) :-
    m_property(A, 'supplier_order_id', SubjectKind, Subject),
    m_property(B, 'supplier_order_id', SubjectKind, Subject),
    A @< B,
    m_property(A, 'product_code', ProductKind, Product),
    m_property(B, 'product_code', ProductKind, Product),
    m_property(A, 'ordered_quantity', QuantityKind, QuantityA),
    m_property(B, 'ordered_quantity', QuantityKind, QuantityB),
    QuantityA \\== QuantityB.
"""
DERIVED_RULES = b"""\
malleus_rule('NUMBER_IN_CITED_TEXT').

% A quantity a record carries is not among the numbers of the sentence it cites.
malleus_violation('NUMBER_IN_CITED_TEXT', 'NUMBER_NOT_IN_SOURCE', [Record]) :-
    m_property(Record, 'ordered_quantity', _, Quantity),
    m_derivation(Record, 'properties/ordered_quantity', SourceId, Locator),
    m_source_text(SourceId, Locator, Text),
    term_to_atom(Quantity, Rendered),
    \\+ sub_string(Text, _, _, _, Rendered).
"""

swipl = pytest.mark.skipif(
    __import__("shutil").which("swipl") is None,
    reason="SWI-Prolog is required to run a pinned check contract",
)


def _logic_files(
    directory: Path,
    ontology_hash: str,
    rules: bytes,
    version: str,
    rule_id: str = "NO_CONFLICTING_QUANTITY",
):
    """One pinned rule contract written the way an adopter retains it."""

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "rules.pl").write_bytes(rules)
    (directory / "logic.yaml").write_text(
        "schema_version: '1'\n"
        f"contract_id: {CHECK_ID}\n"
        "contract_version: '1'\n"
        f"ontology_hash: {ontology_hash}\n"
        f"fact_contract_version: '{version}'\n"
        f"ruleset_id: {CHECK_ID}\n"
        "ruleset_version: '1'\n"
        "rules_file: rules.pl\n"
        f"rule_ids: [{rule_id}]\n"
        "timeout_seconds: 30\n",
        encoding="utf-8",
    )
    return LogicContract.load(directory / "logic.yaml")


def _plan(plan_id: str, records: list[dict], *, gaps: list | None = None) -> bytes:
    derivations = [
        {
            "locator": f"row:{row}:{field}",
            "path": ["properties", slot],
            "record_id": record["id"],
            "source_id": SOURCE_ID,
        }
        for record, row in zip(records, range(len(records)))
        for field, slot in (
            ("supplier_order_id", "supplier_order_id"),
            ("product_code", "product_code"),
            ("quantity", "ordered_quantity"),
            ("event_id", "source_occurrence_id"),
        )
    ]
    return _canonical(
        {
            "adapter": {"adapter_id": "test-row-mapping", "version": "0"},
            "contract_identity": None,
            "derivations": derivations,
            "evidence": [],
            "gaps": gaps or [],
            "grammar": "malleus.population-plan/private-v0",
            "history_profile": {"profile_id": None, "sha256": None},
            "plan_id": plan_id,
            "records": {"entities": records, "relations": []},
            "sources": [{"source_id": SOURCE_ID, "sha256": _digest(PACKET)}],
            "supersessions": [],
            "valid_time": {"kind": "ORDER_ONLY", "value": plan_id},
        }
    )


def _bind(plan_bytes: bytes, replay, profile) -> bytes:
    """Fill the three fields the history, not the producer, decides."""

    plan = json.loads(plan_bytes)
    plan["contract_identity"] = replay.partial_contract.identity
    plan["history_profile"] = {
        "profile_id": profile.profile_id,
        "sha256": profile.identity,
    }
    return _canonical(plan)


def _record(occurrence: str, quantity: int) -> dict:
    return {
        "id": f"supplier-order-state:B:{occurrence}",
        "properties": {
            "ordered_quantity": quantity,
            "product_code": "Y",
            "source_occurrence_id": occurrence,
            "supplier_order_id": "B",
        },
        "type": "SupplierOrderState",
    }


def _shop_shaped(tmp_path: Path, *, rules: bytes = QUANTITY_RULES, version: str = "2"):
    """A history on the revised Shop ontology with a Prolog policy installed.

    This is the Shop runner's shape: the private machine program the Shop
    selects, an adopter rule contract, and a JSONL source packet whose rows the
    plan's locators resolve against.
    """

    compiled = _compile(REVISION_TARGET.read_bytes())
    logic = _logic_files(
        tmp_path / "rules",
        "sha256:" + compiled.view.content_hash(),
        rules,
        version,
        "NUMBER_IN_CITED_TEXT" if rules is DERIVED_RULES else "NO_CONFLICTING_QUANTITY",
    )
    policy = _policy(((CHECK_ID, logic.contract_hash),))
    partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=_profile(policy),
    )
    mapping = json.loads((SHOP_RUNTIME / "mapping.json").read_bytes())
    history = compiler.KnowledgeChangeHistory(
        tmp_path / "history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=compiler.KnowledgeChangeHistoryBinding.from_bytes(
            _canonical(mapping["history_binding"])
        ),
    )
    history.append_anchors(
        anchors=(
            _artifact(
                "artifact:validated-contract",
                compiled.artifact.artifact_bytes,
                "VALIDATED_CONTRACT",
            ),
            _artifact(
                "artifact:partial-contract",
                partial.canonical_bytes,
                "PARTIAL_EFFECTIVE_CONTRACT",
            ),
            _artifact(
                "artifact:history-binding",
                history.binding.canonical_bytes,
                "KNOWLEDGE_HISTORY_BINDING",
            ),
            _artifact(
                "artifact:logic", (tmp_path / "rules/logic.yaml").read_bytes(), None
            ),
            _artifact("artifact:rules", rules, None),
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    _retain_source(
        history,
        artifact_id="artifact:packet",
        source_id=SOURCE_ID,
        content=PACKET,
    )
    return history, compiled, logic, policy


def _artifact(record_id: str, content: bytes, role: str | None):
    return compiler.KnowledgeAnchorInput(
        machine_event=_event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=_digest(content),
        ),
        retained_bytes=content,
        media_type="application/octet-stream",
        role=role or "RETAINED_EVIDENCE",
    )


def history_path(history) -> Path:
    return Path(history._ledger.path)


def _admit(history, plan_bytes, profile, **extra):
    replay = history.replay()
    return compiler.check_and_admit_population_plan(
        history=history,
        plan_bytes=_bind(plan_bytes, replay, profile),
        history_profile=profile,
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
        **extra,
    )


# --- the door: what the public admission surface does now --------------------
#
# These two were the step-1 measurement of the hole: an admission carrying no
# check record refused, and one carrying a fabricated ``SATISFIED`` was
# accepted with no engine run. Both premises are gone. The public door refuses
# a caller-written check or verdict record before any append, so the events
# those tests built can no longer be admitted at all, by anyone.


def test_the_public_door_refuses_a_caller_written_verdict_record(
    tmp_path: Path,
) -> None:
    """``CHANGE_PROPOSED`` plus a caller's verdict refuses before any append.

    Where this used to reach the machine and refuse ``MISSING_REQUIRED_CHECK``,
    the verdict record never gets that far: it is Core's to write, and the
    machine derives it from the check records, so a caller who may write it
    may still decide the outcome by choosing which checks exist.
    """

    history, _, logic, policy = _shop_shaped(tmp_path)
    before = history.replay()
    change = _change(history)
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change,
            machine_events=(
                _event(
                    "CHANGE_PROPOSED",
                    expected_machine_state_identity=before.machine_state.identity,
                    knowledge_change_set_identity=change.identity,
                    policy_id=policy.identifier,
                    policy_identity=policy.identity,
                    proposal_id="proposal:no-check",
                ),
                _event(
                    "VERDICT_RECORDED",
                    decision_id="decision:no-check",
                    proposal_id="proposal:no-check",
                ),
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR,
        )

    assert (
        refusal.value.reason
        is compiler.KnowledgeChangeRefusalReason.CALLER_SUPPLIED_CHECK_EVENT
    )
    assert "VERDICT_RECORDED" in refusal.value.detail
    assert history_path(history).read_bytes() == ledger_before


def test_a_proposal_alone_still_refuses_as_an_incomplete_admission(
    tmp_path: Path,
) -> None:
    """The door refuses check and verdict records; it does not replace ``_admit``.

    A batch carrying only ``CHANGE_PROPOSED`` passes the door, because nothing
    in it is Core's to write, and then refuses ``INCOMPLETE_ADMISSION`` as it
    always has: no terminal acceptance of the retained change set.
    """

    history, _, logic, policy = _shop_shaped(tmp_path)
    before = history.replay()
    change = _change(history)
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change,
            machine_events=(
                _event(
                    "CHANGE_PROPOSED",
                    expected_machine_state_identity=before.machine_state.identity,
                    knowledge_change_set_identity=change.identity,
                    policy_id=policy.identifier,
                    policy_identity=policy.identity,
                    proposal_id="proposal:proposal-only",
                ),
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR,
        )

    assert (
        refusal.value.reason
        is compiler.KnowledgeChangeRefusalReason.INCOMPLETE_ADMISSION
    )
    assert history_path(history).read_bytes() == ledger_before


def test_a_fabricated_check_outcome_can_no_longer_reach_the_ledger(
    tmp_path: Path,
) -> None:
    """The hole, closed. The exact events that admitted a conflict now refuse.

    Both records state a different quantity for the same order and product, so
    the installed contract's ``NO_CONFLICTING_QUANTITY`` returns VIOLATED. The
    caller's ``SATISFIED`` used to be read off the event and admitted. It is
    now refused before any append, and nothing is written.
    """

    history, _, logic, policy = _shop_shaped(tmp_path)
    before = history.replay()
    change = _change(history)
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change,
            machine_events=(
                _event(
                    "CHANGE_PROPOSED",
                    expected_machine_state_identity=before.machine_state.identity,
                    knowledge_change_set_identity=change.identity,
                    policy_id=policy.identifier,
                    policy_identity=policy.identity,
                    proposal_id="proposal:fabricated",
                ),
                _event(
                    "CHECK_RECORDED",
                    check_contract_id=CHECK_ID,
                    check_contract_identity=logic.contract_hash,
                    outcome="SATISFIED",
                    policy_identity=policy.identity,
                    proposal_id="proposal:fabricated",
                    receipt_id="receipt:fabricated",
                ),
                _event(
                    "VERDICT_RECORDED",
                    decision_id="decision:fabricated",
                    proposal_id="proposal:fabricated",
                ),
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR,
        )

    assert (
        refusal.value.reason
        is compiler.KnowledgeChangeRefusalReason.CALLER_SUPPLIED_CHECK_EVENT
    )
    assert "CHECK_RECORDED" in refusal.value.detail
    assert history_path(history).read_bytes() == ledger_before
    assert history.replay().change_sets == ()


def test_no_public_callable_accepts_a_caller_check_outcome_under_a_policy() -> None:
    """The facades expose no remaining way in that reads a caller's outcome.

    ``malleus`` and ``malleus.compiler`` are the facades; ``malleus.population``
    does not exist. Every public callable that appends a change set either
    takes no machine events at all, in which case Core writes them, or is the
    door itself, which refuses the two Core-authored types.
    """

    import malleus

    reaching: dict[str, set[str]] = {}
    for facade in (malleus, compiler):
        for name in getattr(facade, "__all__", ()):
            member = getattr(facade, name)
            if not callable(member):
                continue
            try:
                parameters = set(inspect.signature(member).parameters)
            except (TypeError, ValueError):
                continue
            if {"change_set", "plan_bytes", "preparation"} & parameters:
                reaching[name] = parameters

    assert {
        "admit_structural_change",
        "check_and_admit_change_set",
        "check_and_admit_population_plan",
    } <= set(reaching)
    for name, parameters in reaching.items():
        assert "machine_events" not in parameters, name
        assert not {
            parameter
            for parameter in parameters
            if "outcome" in parameter or "verdict" in parameter
        }, name

    door = compiler.KnowledgeChangeHistory
    public = {
        name
        for name in dir(door)
        if not name.startswith("_")
        and callable(getattr(door, name))
        and "machine_events" in getattr(
            inspect.signature(getattr(door, name)), "parameters", {}
        )
    }
    assert public == {"admit", "admit_with_anchors"}
    for name in sorted(public):
        source = inspect.getsource(getattr(door, name))
        assert "_refuse_caller_authored(self.partial_contract, machine_events)" in (
            source
        )


def _change(history):
    """One conflicting pair composed by hand, bypassing the new operation."""

    return history.compose_change_set(
        change_set_id="change:by-hand",
        source_record_ids=(SOURCE_ID,),
        evidence_record_ids=("artifact:logic",),
        operations=tuple(
            compiler.KnowledgeOperation(
                ordinal=ordinal,
                operation_id=f"operation:by-hand:{ordinal}",
                operation_type="CREATE_ENTITY",
                record_type="SupplierOrderState",
                record_id=record["id"],
                properties=record["properties"],
                depends_on=(),
                source_id=None,
                target_id=None,
            )
            for ordinal, record in enumerate((_record("e1", 2), _record("e2", 5)))
        ),
        valid_time=compiler.KnowledgeValidTime("ORDER_ONLY", "e1"),
        supersedes=(),
    )


# --- the operation: the hole closed ------------------------------------------


@swipl
def test_the_operation_refuses_the_conflict_the_fabricated_outcome_admitted(
    tmp_path: Path,
) -> None:
    """Same plan, same history: the engine's outcome decides, and nothing is written."""

    history, _, logic, _ = _shop_shaped(tmp_path)
    plan = _plan("plan:conflict", [_record("e1", 2), _record("e2", 5)])
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, plan, compiler.STATE_VERSION_PROFILE)

    error = refusal.value
    assert error.stage is compiler.PopulationAdmissionStage.CHECK
    assert error.reason == "CONTENT_RULE_VIOLATED"
    assert error.violated_rule_ids == ("NO_CONFLICTING_QUANTITY",)
    assert error.witness_record_ids == (
        "supplier-order-state:B:e1",
        "supplier-order-state:B:e2",
    )
    assert error.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before
    assert history.replay().change_sets == ()


@swipl
def test_the_operation_admits_the_plan_its_gaps_the_change_receipt_and_three_events(
    tmp_path: Path,
) -> None:
    history, _, logic, _ = _shop_shaped(tmp_path)
    plan = _plan(
        "plan:ok",
        [_record("e1", 2)],
        gaps=[
            {
                "kind": "TYPE_ABSENT",
                "locator": "row:0:supplier_order_id",
                "source_id": SOURCE_ID,
                "statement": "the packet names a customer the contract has no class for",
            }
        ],
    )
    before = history.replay()

    admitted = _admit(history, plan, compiler.STATE_VERSION_PROFILE)

    after = admitted.replay
    assert admitted.check.outcome == "SATISFIED"
    assert admitted.check_contract_identity == logic.contract_hash
    assert admitted.gap_count == 1
    assert len(after.change_sets) == 1
    retained = {member.record_id for member in after.retained_inputs}
    assert {
        "profile:state-version",
        "plan:ok",
        "plan:ok:gaps",
        f"receipt:{admitted.change_set.change_set_id}:{CHECK_ID}",
    } <= retained
    assert after.ledger_event_count == before.ledger_event_count + 8
    assert _digest(after.retained_bytes(admitted.receipt_id)) == admitted.receipt_identity


@swipl
def test_the_receipt_states_the_engine_outcome_and_the_required_check_identity(
    tmp_path: Path,
) -> None:
    """The receipt's check identity is the one ``required_checks`` names."""

    history, _, logic, _ = _shop_shaped(tmp_path)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    receipt = json.loads(admitted.replay.retained_bytes(admitted.receipt_id))
    required = dict(admitted.replay.required_checks)[POLICY_REF]
    assert receipt["check"]["outcome"] == "SATISFIED"
    assert receipt["check"]["contract_hash"] == logic.contract_hash
    assert receipt["knowledge_change_set_identity"] == admitted.change_set.identity
    assert required == ((CHECK_ID, logic.contract_hash),)


@swipl
def test_the_admitted_history_reopens_and_replays_to_the_same_state(
    tmp_path: Path,
) -> None:
    history, _, _, _ = _shop_shaped(tmp_path)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    reopened = compiler.KnowledgeChangeHistory.reopen(history_path(history)).replay()
    assert reopened.ledger_head == admitted.replay.ledger_head
    assert reopened.graph.export_records() == admitted.replay.graph.export_records()
    assert reopened.graph.export_records()["entities"][0]["id"] == (
        "supplier-order-state:B:e1"
    )


@swipl
def test_the_same_plan_on_the_same_ledger_twice_appends_identical_bytes(
    tmp_path: Path,
) -> None:
    """Determinism: two independent histories, byte-identical appended events."""

    first, _, _, _ = _shop_shaped(tmp_path / "a")
    second, _, _, _ = _shop_shaped(tmp_path / "b")
    plan = _plan("plan:ok", [_record("e1", 2)])
    opening = history_path(first).read_bytes()
    assert opening == history_path(second).read_bytes()

    _admit(first, plan, compiler.STATE_VERSION_PROFILE)
    _admit(second, plan, compiler.STATE_VERSION_PROFILE)

    appended = history_path(first).read_bytes()[len(opening) :]
    assert appended == history_path(second).read_bytes()[len(opening) :]
    assert appended


# --- compile-stage refusals write nothing ------------------------------------


@pytest.mark.parametrize(
    ("label", "reason"),
    [
        ("unknown_class", "RECORDS_NOT_REHYDRATABLE"),
        ("missing_derivation", "UNDERIVED_FIELD"),
        ("unknown_gap_kind", "UNKNOWN_GAP_KIND"),
    ],
)
def test_a_compile_stage_refusal_names_the_stage_and_writes_nothing(
    tmp_path: Path, label: str, reason: str
) -> None:
    history, _, _, _ = _shop_shaped(tmp_path)
    plan = json.loads(_plan("plan:bad", [_record("e1", 2)]))
    if label == "unknown_class":
        plan["records"]["entities"][0]["type"] = "NoSuchClass"
    elif label == "missing_derivation":
        plan["derivations"] = [
            item
            for item in plan["derivations"]
            if item["path"] != ["properties", "ordered_quantity"]
        ]
    else:
        plan["gaps"] = [
            {
                "kind": "NOT_A_GAP_KIND",
                "locator": "row:0:quantity",
                "source_id": SOURCE_ID,
                "statement": "invented",
            }
        ]
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, _canonical(plan), compiler.STATE_VERSION_PROFILE)

    assert refusal.value.stage is compiler.PopulationAdmissionStage.COMPILE
    assert refusal.value.reason == reason
    assert refusal.value.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


def test_plan_bytes_that_are_not_json_refuse_at_the_compile_stage(
    tmp_path: Path,
) -> None:
    history, _, _, _ = _shop_shaped(tmp_path)
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        compiler.check_and_admit_population_plan(
            history=history,
            plan_bytes=b"{not json",
            history_profile=compiler.STATE_VERSION_PROFILE,
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.COMPILE
    assert refusal.value.reason == "MALFORMED_PLAN"
    assert history_path(history).read_bytes() == ledger_before


# --- the check contract the history requires ---------------------------------


def test_a_required_check_the_history_does_not_retain_refuses(tmp_path: Path) -> None:
    """``CHECK_CONTRACT_NOT_RETAINED``: the policy names what nothing reproduces."""

    history, compiled, logic, _ = _shop_shaped(tmp_path)
    other = _logic_files(
        tmp_path / "unretained",
        "sha256:" + compiled.view.content_hash(),
        QUANTITY_RULES.replace(b"@<", b"@>"),
        "2",
    )
    assert other.contract_hash != logic.contract_hash
    stranded = compiler.KnowledgeChangeHistory(
        tmp_path / "stranded.jsonl",
        partial_contract=compiler.compose_partial_effective_contract(
            validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
            normative_profile=_profile(_policy(((CHECK_ID, other.contract_hash),))),
        ),
        contract_view=compiled.view,
        binding=history.binding,
    )
    stranded.append_anchors(
        anchors=(
            _artifact(
                "artifact:logic", (tmp_path / "rules/logic.yaml").read_bytes(), None
            ),
            _artifact("artifact:rules", QUANTITY_RULES, None),
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    _retain_source(
        stranded, artifact_id="artifact:packet", source_id=SOURCE_ID, content=PACKET
    )
    ledger_before = history_path(stranded).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(
            stranded,
            _plan("plan:ok", [_record("e1", 2)]),
            compiler.STATE_VERSION_PROFILE,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "CHECK_CONTRACT_NOT_RETAINED"
    assert history_path(stranded).read_bytes() == ledger_before


@swipl
def test_after_a_rebinding_the_operation_checks_the_new_contract_not_the_old(
    tmp_path: Path,
) -> None:
    """``REBIND_CHECK_CONTRACT`` moves the required identity; the operation follows."""

    history, base, partial, policy, logic, _ = _history(tmp_path)
    target, target_logic = _target(tmp_path)
    assert target_logic.contract_hash != logic.contract_hash
    revision, _ = _revise(
        history,
        target,
        partial,
        _profile(_policy(((CHECK_ID, target_logic.contract_hash),))),
        descriptors={CHECK_ID: (_descriptor(logic), _descriptor(target_logic))},
    )
    history.record_contract_revision(
        revision=revision, transaction_time=TRANSACTION_TIME, actor_id=ACTOR
    )
    history.append_anchors(
        anchors=(
            _artifact(
                "artifact:logic:target",
                (tmp_path / "rules-target/logic.yaml").read_bytes(),
                None,
            ),
            _artifact(
                "artifact:rules:target",
                (tmp_path / "rules-target/rules.pl").read_bytes(),
                None,
            ),
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    _retain_source(
        history, artifact_id="artifact:packet", source_id=SOURCE_ID, content=PACKET
    )

    admitted = _admit(
        history, _plan("plan:rebound", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    assert admitted.check_contract_identity == target_logic.contract_hash
    assert admitted.check_contract_identity != logic.contract_hash
    assert dict(admitted.replay.required_checks)[POLICY_REF] == (
        (CHECK_ID, target_logic.contract_hash),
    )


# --- the second consumer's shape: provenance the contract declares ------------


@swipl
def test_a_contract_that_declares_provenance_reads_the_plans_own_derivations(
    tmp_path: Path,
) -> None:
    """The document path's shape: a rule compares a value to its cited sentence."""

    history, _, _, _ = _shop_shaped(tmp_path, rules=DERIVED_RULES, version="3")
    plan = _plan("plan:derived", [_record("e1", 2)])
    texts = (
        RetainedSourceText(
            source_id=SOURCE_ID,
            locator="row:0:quantity",
            text="the shop ordered 2 units of Y",
        ),
    )

    admitted = _admit(
        history, plan, compiler.STATE_VERSION_PROFILE, retained_source_texts=texts
    )

    assert admitted.check.outcome == "SATISFIED"
    assert admitted.check.fact_contract_version == "3"
    assert "NUMBER_IN_CITED_TEXT" in admitted.check.checked_rule_ids


@swipl
def test_a_value_absent_from_its_cited_sentence_refuses_with_the_record_as_witness(
    tmp_path: Path,
) -> None:
    history, _, _, _ = _shop_shaped(tmp_path, rules=DERIVED_RULES, version="3")
    texts = (
        RetainedSourceText(
            source_id=SOURCE_ID,
            locator="row:0:quantity",
            text="the shop ordered some units of Y",
        ),
    )
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(
            history,
            _plan("plan:derived", [_record("e1", 2)]),
            compiler.STATE_VERSION_PROFILE,
            retained_source_texts=texts,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.violated_rule_ids == ("NUMBER_IN_CITED_TEXT",)
    assert refusal.value.witness_record_ids == ("supplier-order-state:B:e1",)
    assert history_path(history).read_bytes() == ledger_before


def test_source_text_against_a_contract_that_cannot_read_it_refuses(
    tmp_path: Path,
) -> None:
    """Fail closed: the provenance is not silently dropped at fact contract 2."""

    history, _, _, _ = _shop_shaped(tmp_path)
    texts = (
        RetainedSourceText(source_id=SOURCE_ID, locator="row:0:quantity", text="2"),
    )
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(
            history,
            _plan("plan:ok", [_record("e1", 2)]),
            compiler.STATE_VERSION_PROFILE,
            retained_source_texts=texts,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "PROVENANCE_NOT_DECLARED"
    assert history_path(history).read_bytes() == ledger_before


def test_the_staged_check_writes_thaw_the_compiled_operations_properties() -> None:
    """The defect both shipped runners carry, guarded at its one Core site.

    A compiled operation freezes list values into tuples and the ontology
    validator accepts only ``list`` for a multivalued slot, so
    ``dict(operation.properties)`` refuses every multivalued property at the
    check. Both `runner.py` and `admit.py` do exactly that. This pins the Core
    site to `_staged_properties`, the same thaw
    `test_repository_guards.py::test_staged_writes_thaw_the_frozen_change_set_properties`
    pins inside `knowledge.py`.
    """

    import ast

    source = Path(
        __import__("malleus._contract_pipeline.admission", fromlist=["x"]).__file__
    )
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    writes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "ProposedOperation"
    ]

    assert len(writes) == 1, "the staged check-write site moved"
    properties = [
        keyword.value for keyword in writes[0].keywords if keyword.arg == "properties"
    ]
    assert len(properties) == 1
    assert (
        isinstance(properties[0], ast.Call)
        and isinstance(properties[0].func, ast.Name)
        and properties[0].func.id == "_staged_properties"
    ), "staged check writes must thaw the compiled operation's properties"


def test_the_operation_is_declared_on_the_public_facade() -> None:
    assert {
        "PopulationAdmission",
        "PopulationAdmissionRefusal",
        "PopulationAdmissionStage",
        "REQUIRED_CHECK_POLICY_REFERENCE",
        "check_and_admit_population_plan",
    } <= set(compiler.__all__)

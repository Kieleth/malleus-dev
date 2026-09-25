"""Core runs every check a policy requires, through executors Core ships.

Paper ledger E-0502, decision D, step 1. A check contract names its executor
and Core executes it; an adopter supplies contracts and rules, never programs
and never outcomes. The executor kinds are closed: a retained Prolog rule
layer, or a Core builtin from the registry in ``check_contract.py``.

The measurements this module pins were taken on the operation as ROADMAP F1
shipped it: it refused ``UNEXPECTED_REQUIRED_CHECKS`` for any policy not
requiring exactly one contract, and it wrote a six-field ``CHECK_RECORDED``
whatever the selected machine declared, so ``correction/machine.json`` with its
seven-field ``CheckRecord`` refused ``MALFORMED_EVENT`` after the retention had
already been appended.
"""

from __future__ import annotations

import ast
import inspect
import json
import textwrap
from pathlib import Path

import pytest

import malleus.compiler as compiler
from malleus._contract_pipeline.check_contract import (
    CHECK_CONTRACT_GRAMMAR,
    CORE_BUILTIN_CHECKS,
    OPERATIONS_APPLY_ATOMICALLY,
    CandidateChange,
    CheckContractError,
    CheckExecutorKind,
    CheckRequest,
    parse_check_contract,
    resolve_core_builtin,
)
from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory

from tests.contract_compiler.pareto.test_atomic_population_admission import (
    ACTOR,
    PACKET,
    QUANTITY_RULES,
    SOURCE_ID,
    _admit,
    _artifact,
    _logic_files,
    _plan,
    _record,
    history_path,
    swipl,
)
from tests.contract_compiler.pareto.test_check_contract_rebinding import (
    CHECK_ID,
    POLICY_REF,
    _policy,
)
from tests.contract_compiler.pareto.test_public_compiler import (
    SHOP_RUNTIME,
    TRANSACTION_TIME,
    _canonical,
    _digest,
)
from tests.contract_compiler.pareto.test_small_shop_contract_revision import (
    REVISION_TARGET,
    _compile,
    _retain_source,
)


STRUCTURAL_CHECK_ID = "malleus.core.structural-conformance"
BUILTIN_CONTRACT = _canonical(
    {
        "check_contract_id": STRUCTURAL_CHECK_ID,
        "executor": {
            "builtin_id": OPERATIONS_APPLY_ATOMICALLY,
            "builtin_version": "1",
            "kind": "CORE_BUILTIN",
        },
        "grammar": CHECK_CONTRACT_GRAMMAR,
        "outcomes": ["SATISFIED", "VIOLATED"],
    }
)
BUILTIN_IDENTITY = _digest(BUILTIN_CONTRACT)


def _machine_bytes(*, receipt_identity: bool = False) -> bytes:
    """The Shop machine, optionally declaring the seventh ``CheckRecord`` field.

    ``correction/machine.json`` declares ``receipt_identity`` and the shipped
    structural machine does not. Both are legitimate; the operation reads the
    declaration rather than carrying one of them as a constant.
    """

    program = json.loads((SHOP_RUNTIME / "machine.json").read_bytes())
    if receipt_identity:
        schema = program["record_schemas"]["CheckRecord"]
        schema["fields"]["receipt_identity"] = "DIGEST"
        schema["input_fields"] = sorted([*schema["input_fields"], "receipt_identity"])
    return _canonical(program)


def _two_check_history(
    tmp_path: Path,
    *,
    builtin_first: bool = True,
    machine: bytes | None = None,
    builtin_only: bool = False,
    retain_check_contract: bool = True,
    check_contract_bytes: bytes | None = None,
):
    """A Shop-shaped history whose policy requires a builtin and a rule layer.

    ``builtin_only`` drops the rule layer from the policy, which is the
    cheapest real check a fixture can require: it needs no Prolog and no rule
    bytes. ``retain_check_contract`` and ``check_contract_bytes`` are for the
    two refusals a history can carry, a required contract it does not retain
    and one whose executor Core does not ship.
    """

    contract_bytes = (
        BUILTIN_CONTRACT if check_contract_bytes is None else check_contract_bytes
    )
    compiled = _compile(REVISION_TARGET.read_bytes())
    logic = _logic_files(
        tmp_path / "rules",
        "sha256:" + compiled.view.content_hash(),
        QUANTITY_RULES,
        "2",
    )
    builtin_check = (STRUCTURAL_CHECK_ID, _digest(contract_bytes))
    checks = (
        (builtin_check,)
        if builtin_only
        else (builtin_check, (CHECK_ID, logic.contract_hash))
    )
    policy = _policy(checks if builtin_first else tuple(reversed(checks)))
    profile = compiler.compose_normative_profile(
        protocol_machine_program=compiler.ProtocolMachineProgram.from_bytes(
            machine if machine is not None else _machine_bytes()
        ),
        policy_programs={POLICY_REF: policy},
        capability_refs=(),
    )
    partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=profile,
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
    anchors = [
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
        _artifact("artifact:rules", QUANTITY_RULES, None),
    ]
    if retain_check_contract:
        anchors.append(_artifact("artifact:structural-check", contract_bytes, None))
    history.append_anchors(
        anchors=tuple(anchors),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    _retain_source(
        history, artifact_id="artifact:packet", source_id=SOURCE_ID, content=PACKET
    )
    return history, compiled, logic


# --- the grammar and its closed executor set ---------------------------------


def test_the_grammar_reads_a_core_builtin_contract_from_its_exact_bytes() -> None:
    contract = parse_check_contract(BUILTIN_CONTRACT)

    assert contract.check_contract_id == STRUCTURAL_CHECK_ID
    assert contract.identity == BUILTIN_IDENTITY
    assert contract.executor_kind is CheckExecutorKind.CORE_BUILTIN
    assert contract.builtin_id == OPERATIONS_APPLY_ATOMICALLY
    assert contract.outcomes == ("SATISFIED", "VIOLATED")


def test_the_registry_refuses_an_executor_kind_outside_the_closed_set() -> None:
    """No adopter-program kind exists, and the parser will not invent one."""

    for executor in (
        {"artifact_id": "artifact:entrypoint", "sha256": "sha256:" + "0" * 64},
        {"builtin_id": OPERATIONS_APPLY_ATOMICALLY, "kind": "ADOPTER_PROGRAM"},
        {"kind": "SHACL_SHAPES", "shapes_record_id": "artifact:shapes"},
    ):
        document = _canonical(
            {
                "check_contract_id": STRUCTURAL_CHECK_ID,
                "executor": executor,
                "grammar": CHECK_CONTRACT_GRAMMAR,
                "outcomes": ["SATISFIED", "VIOLATED"],
            }
        )
        with pytest.raises(CheckContractError) as refusal:
            parse_check_contract(document)
        assert "executor kind" in str(refusal.value)


def test_the_registry_refuses_a_builtin_id_it_does_not_know() -> None:
    with pytest.raises(CheckContractError) as by_name:
        resolve_core_builtin("malleus.core.invented-check", "1")
    assert "holds no builtin check" in str(by_name.value)

    with pytest.raises(CheckContractError):
        resolve_core_builtin(OPERATIONS_APPLY_ATOMICALLY, "3")

    document = _canonical(
        {
            "check_contract_id": STRUCTURAL_CHECK_ID,
            "executor": {
                "builtin_id": "malleus.core.invented-check",
                "builtin_version": "1",
                "kind": "CORE_BUILTIN",
            },
            "grammar": CHECK_CONTRACT_GRAMMAR,
            "outcomes": ["SATISFIED"],
        }
    )
    with pytest.raises(CheckContractError):
        parse_check_contract(document)


def test_the_grammar_closes_its_outcomes() -> None:
    document = _canonical(
        {
            "check_contract_id": STRUCTURAL_CHECK_ID,
            "executor": {
                "builtin_id": OPERATIONS_APPLY_ATOMICALLY,
                "builtin_version": "1",
                "kind": "CORE_BUILTIN",
            },
            "grammar": CHECK_CONTRACT_GRAMMAR,
            "outcomes": ["SATISFIED", "PROBABLY"],
        }
    )
    with pytest.raises(CheckContractError) as refusal:
        parse_check_contract(document)
    assert "outcomes" in str(refusal.value)


def test_the_grammar_does_not_reopen_the_logic_contract_fields() -> None:
    """A rule layer is referenced by its retained records, never restated.

    ``LogicContract`` validates an exact field set. A check contract that
    carried rule bytes, an ontology hash or a rule id list would be a second
    place the same pin is written, and the two could disagree.
    """

    from malleus.logic import CONTRACT_FIELDS

    document = _canonical(
        {
            "check_contract_id": CHECK_ID,
            "executor": {
                "descriptor_record_id": "artifact:logic",
                "kind": "PROLOG_RULES",
                "rules_record_id": "artifact:rules",
            },
            "grammar": CHECK_CONTRACT_GRAMMAR,
            "outcomes": ["SATISFIED", "VIOLATED"],
        }
    )
    contract = parse_check_contract(document)

    assert contract.executor_kind is CheckExecutorKind.PROLOG_RULES
    assert contract.descriptor_record_id == "artifact:logic"
    executor_fields = {"descriptor_record_id", "kind", "rules_record_id"}
    assert executor_fields.isdisjoint(CONTRACT_FIELDS)


def test_the_candidate_change_carries_every_field_the_application_reads() -> None:
    """``_apply_change`` may not grow a read this value cannot answer.

    The builtin applies a candidate that has no ledger coordinates yet, so it
    passes ``CandidateChange`` where a composed change set would go. If the
    primitive starts reading a fourth attribute, this fails here rather than
    with an ``AttributeError`` inside a check.
    """

    source = textwrap.dedent(inspect.getsource(KnowledgeChangeHistory._apply_change))
    tree = ast.parse(source)
    read = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "change"
    }

    assert read == set(CandidateChange.__dataclass_fields__)


# --- the builtin -------------------------------------------------------------


def test_the_structural_builtin_is_the_only_one_core_ships() -> None:
    """Two versions of one builtin: 2 applies ``supersession_kind``, 1 refuses it."""

    assert set(CORE_BUILTIN_CHECKS) == {
        (OPERATIONS_APPLY_ATOMICALLY, "1"),
        (OPERATIONS_APPLY_ATOMICALLY, "2"),
    }


@swipl
def test_the_structural_builtin_digests_the_state_the_change_would_produce(
    tmp_path: Path,
) -> None:
    history, _, _ = _two_check_history(tmp_path)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    structural = next(
        check
        for check in admitted.checks
        if check.check_contract_id == STRUCTURAL_CHECK_ID
    )
    assert structural.executor_kind is CheckExecutorKind.CORE_BUILTIN
    assert structural.result["result_state_digest"] == (
        admitted.replay.graph.state_digest()
    )


@swipl
def test_the_structural_builtin_reports_violated_when_the_change_cannot_apply(
    tmp_path: Path,
) -> None:
    """A supersession of a record the history never accepted does not apply."""

    history, _, _ = _two_check_history(tmp_path)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )
    replay = admitted.replay
    operation = compiler.KnowledgeOperation(
        ordinal=0,
        operation_id="operation:unknown-supersession",
        operation_type="CREATE_ENTITY",
        record_type="SupplierOrderState",
        record_id="supplier-order-state:B:e9",
        properties={
            "ordered_quantity": 3,
            "product_code": "Y",
            "source_occurrence_id": "e9",
            "supplier_order_id": "B",
        },
        depends_on=(),
        source_id=None,
        target_id=None,
        supersedes_record_id="supplier-order-state:B:absent",
    )
    outcome = resolve_core_builtin(OPERATIONS_APPLY_ATOMICALLY, "1")(
        CheckRequest(
            replay=replay,
            candidate=CandidateChange(
                change_set_id="change:probe",
                operations=(operation,),
                valid_time=compiler.KnowledgeValidTime("ORDER_ONLY", "probe"),
            ),
            candidate_graph=replay.graph,
        )
    )

    assert outcome.outcome == "VIOLATED"
    assert "UNKNOWN_SUPERSESSION" in outcome.detail
    assert outcome.witness_record_ids == ("supplier-order-state:B:e9",)


# --- the operation runs N checks, in policy order ----------------------------


@swipl
def test_the_operation_runs_every_required_check_in_policy_order(
    tmp_path: Path,
) -> None:
    """Two required checks, both run by Core, both with their own receipt."""

    history, _, logic = _two_check_history(tmp_path)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    assert [check.check_contract_id for check in admitted.checks] == [
        STRUCTURAL_CHECK_ID,
        CHECK_ID,
    ]
    assert [check.executor_kind for check in admitted.checks] == [
        CheckExecutorKind.CORE_BUILTIN,
        CheckExecutorKind.PROLOG_RULES,
    ]
    assert all(check.outcome == "SATISFIED" for check in admitted.checks)
    retained = {member.record_id for member in admitted.replay.retained_inputs}
    assert {check.receipt_id for check in admitted.checks} <= retained
    assert len({check.record_receipt_id for check in admitted.checks}) == 2
    assert admitted.check_contract_identity == BUILTIN_IDENTITY


@swipl
def test_the_policys_own_order_decides_which_check_runs_first(
    tmp_path: Path,
) -> None:
    history, _, logic = _two_check_history(tmp_path, builtin_first=False)
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    assert [check.check_contract_id for check in admitted.checks] == [
        CHECK_ID,
        STRUCTURAL_CHECK_ID,
    ]
    assert admitted.check_contract_identity == logic.contract_hash


@swipl
def test_a_violation_of_one_of_two_checks_refuses_and_writes_nothing(
    tmp_path: Path,
) -> None:
    """The builtin is satisfied, the rule layer is not, and no byte is written."""

    history, _, _ = _two_check_history(tmp_path)
    ledger_before = history_path(history).read_bytes()
    plan = _plan("plan:conflict", [_record("e1", 2), _record("e2", 5)])

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, plan, compiler.STATE_VERSION_PROFILE)

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "CONTENT_RULE_VIOLATED"
    assert refusal.value.violated_rule_ids == ("NO_CONFLICTING_QUANTITY",)
    assert refusal.value.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


def test_a_required_check_whose_executor_core_cannot_run_refuses(
    tmp_path: Path,
) -> None:
    """A retained contract naming an unknown builtin never reaches an engine."""

    stranded = _canonical(
        {
            "check_contract_id": STRUCTURAL_CHECK_ID,
            "executor": {
                "builtin_id": "malleus.core.not-shipped",
                "builtin_version": "1",
                "kind": "CORE_BUILTIN",
            },
            "grammar": CHECK_CONTRACT_GRAMMAR,
            "outcomes": ["SATISFIED", "VIOLATED"],
        }
    )
    compiled = _compile(REVISION_TARGET.read_bytes())
    policy = _policy(((STRUCTURAL_CHECK_ID, _digest(stranded)),))
    profile = compiler.compose_normative_profile(
        protocol_machine_program=compiler.ProtocolMachineProgram.from_bytes(
            _machine_bytes()
        ),
        policy_programs={POLICY_REF: policy},
        capability_refs=(),
    )
    partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=profile,
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
            _artifact("artifact:stranded-check", stranded, None),
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    _retain_source(
        history, artifact_id="artifact:packet", source_id=SOURCE_ID, content=PACKET
    )
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(
            history,
            _plan("plan:ok", [_record("e1", 2)]),
            compiler.STATE_VERSION_PROFILE,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "UNRUNNABLE_REQUIRED_CHECK"
    assert refusal.value.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


# --- the check record carries the selected machine's declared fields ---------


@swipl
def test_the_check_record_carries_the_selected_machines_declared_fields(
    tmp_path: Path,
) -> None:
    """A seven-field ``CheckRecord`` is filled, not refused ``MALFORMED_EVENT``.

    ``correction/machine.json`` declares ``receipt_identity`` beside the six
    fields the shipped structural machine declares. The operation used to write
    six fields whatever the machine said, so that machine refused the admission
    after its retention batch was already appended.
    """

    history, _, _ = _two_check_history(
        tmp_path, machine=_machine_bytes(receipt_identity=True)
    )
    admitted = _admit(
        history, _plan("plan:ok", [_record("e1", 2)]), compiler.STATE_VERSION_PROFILE
    )

    written = [
        record
        for record in admitted.replay.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    assert len(written) == 2
    for record in written:
        assert set(record.fields) == {
            "check_contract_id",
            "check_contract_identity",
            "outcome",
            "policy_identity",
            "proposal_id",
            "receipt_id",
            "receipt_identity",
        }
    by_receipt = {record.fields["receipt_id"]: record for record in written}
    for check in admitted.checks:
        assert (
            by_receipt[check.record_receipt_id].fields["receipt_identity"]
            == check.receipt_identity
        )


def test_a_machine_field_core_cannot_state_refuses_before_the_first_append(
    tmp_path: Path,
) -> None:
    """An undeclared field is a typed refusal, never a guessed value."""

    program = json.loads((SHOP_RUNTIME / "machine.json").read_bytes())
    schema = program["record_schemas"]["CheckRecord"]
    schema["fields"]["reviewer_id"] = "STRING"
    schema["input_fields"] = sorted([*schema["input_fields"], "reviewer_id"])
    history, _, _ = _two_check_history(tmp_path, machine=_canonical(program))
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(
            history,
            _plan("plan:ok", [_record("e1", 2)]),
            compiler.STATE_VERSION_PROFILE,
        )

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "UNSUPPORTED_EVENT_FIELD"
    assert "reviewer_id" in refusal.value.detail
    assert history_path(history).read_bytes() == ledger_before


def test_the_operation_no_longer_refuses_a_policy_on_its_check_count() -> None:
    """``UNEXPECTED_REQUIRED_CHECKS`` is gone from the operation's source."""

    from malleus._contract_pipeline import admission

    assert "UNEXPECTED_REQUIRED_CHECKS" not in inspect.getsource(admission)

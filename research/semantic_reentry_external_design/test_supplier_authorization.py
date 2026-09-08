"""Actual direct-grant policy control, not execution or a synthesized action."""

from importlib import import_module
import inspect
import json
import shutil

import pytest

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import content_digest
from research.semantic_reentry_external_design import test_supplier_proposals as entry
from research.semantic_reentry_external_design.test_supplier_proposals import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_authorization"
TIME = "2026-09-08T06:00:00Z"
EXECUTOR = "actor:supplier:executor"
FUNCTIONS = (
    "prepare_supplier_authority",
    "record_supplier_authority_check",
    "decide_supplier_authorization",
)


def api():
    return import_module(MODULE)


def domain_frame(replay):
    """Snapshot public bytes and immutable history values, never pickle Core."""
    return (
        replay.partial_contract.identity,
        replay.acceptance_head,
        replay.materialization_head,
        entry.ingress.canonical(replay.graph.export_records()),
        tuple(change.canonical_bytes for change in replay.change_sets),
        tuple(sorted(replay.record_history.items())),
        tuple(revision.canonical_bytes for revision in replay.contract_revisions),
    )


def test_contract_api_has_no_required_input_defaults():
    for name in FUNCTIONS:
        function = getattr(api(), name)
        assert all(
            p.default is inspect.Parameter.empty
            for p in inspect.signature(function).parameters.values()
        )


@pytest.fixture(scope="module", name="input_prefix")
def supplier_source_prefix(tmp_path_factory, compilation, action_compilation):
    return entry.input_prefix.__wrapped__(
        tmp_path_factory, compilation, action_compilation
    )


@pytest.fixture(scope="module")
def accepted_prefix(tmp_path_factory, input_prefix):
    api()
    inputs = entry.inputs.__wrapped__(
        tmp_path_factory.mktemp("supplier-authority-entry"), input_prefix
    )
    owner = inputs[0]
    entry.api().submit_supplier_proposal(**entry.submit_arguments(inputs))
    for ordinal in range(2):
        entry.api().record_supplier_type_check(**entry.check_arguments(owner, ordinal))
    entry.api().decide_supplier_proposal(**entry.decision_arguments(owner))
    return owner.path


def grant_bytes(grantee):
    fields = {
        "grantor_actor_id": "actor:supplier:grantor",
        "grantee_actor_id": grantee,
        "permitted_action_types": ["AMEND_SUPPLIER_ORDER"],
        "scope_record_id": entry.ROLE_IDS["goal"],
        "may_subdelegate": False,
        "grant_valid_from": TIME,
        "grant_valid_to": "2026-09-08T08:00:00Z",
    }
    return entry.ingress.canonical(
        make_record(
            "AuthorityGrant",
            id="grant:supplier:direct",
            event_id="event:grant:supplier:direct",
            generated_at=TIME,
            actor_id=fields["grantor_actor_id"],
            role="registrar",
            source_record_ids=[fields["scope_record_id"]],
            artifact_kind="AUTHORITY_GRANT",
            artifact_version="research-v1",
            artifact_hash=content_digest(fields),
            **fields,
        )
    )


@pytest.fixture
def preparation(tmp_path, accepted_prefix):
    path = tmp_path / "history.jsonl"
    shutil.copyfile(accepted_prefix, path)
    owner = core.KnowledgeChangeHistory.reopen(path)
    return dict(
        history=owner,
        original_context_id=entry.CONTEXT,
        grant_bytes=grant_bytes(EXECUTOR),
        scope_association_id="source:supplier:scope-association",
        requested_interval_id="source:supplier:requested-interval",
        current_context_id="source:supplier:current-context",
        requested_interval_bytes=entry.ingress.canonical(
            {"start": TIME, "end": "2026-09-08T07:00:00Z"}
        ),
        actor_id="actor:supplier:authority-registrar",
        generated_at=TIME,
        artifact_version="research-v1",
        **entry.position(owner),
    )


def bindings(args):
    owner = args["history"]
    return dict(
        history=owner,
        original_context_id=args["original_context_id"],
        current_context_id=args["current_context_id"],
        grant_id=json.loads(args["grant_bytes"])["id"],
        scope_association_id=args["scope_association_id"],
        requested_interval_id=args["requested_interval_id"],
        executor_id=EXECUTOR,
        **entry.position(owner),
    )


def check_arguments(args, ordinal):
    owner = args["history"]
    policy = owner.replay().protocol_replay.data["records"][
        entry.initial.POLICIES["authorization"]
    ]["record"]
    return dict(
        **bindings(args),
        monitor_id=policy["required_monitor_ids"][ordinal],
        assessment_id="authority:supplier:" + str(ordinal),
        failure_id="authority-failure:supplier:" + str(ordinal),
        actor_id="actor:supplier:authority-checker",
        generated_at=TIME,
    )


def decision_arguments(args):
    return dict(
        **bindings(args),
        assessment_ids=("authority:supplier:0", "authority:supplier:1"),
        decision_id="authorization:supplier:1",
        transition_id="authorization-transition:supplier:1",
        actor_id="actor:supplier:authorizer",
        generated_at=TIME,
    )


@pytest.mark.parametrize("expected", ["AUTHORIZE", "BLOCK", "CLARIFY"])
def test_actual_supplier_permission_and_replay_preserve_domain(
    preparation,
    expected,
    monkeypatch,
    tmp_path,
):
    from research.action_history_contract_freeze.programs import check_executor

    owner = preparation["history"]
    frame = domain_frame(owner.replay())
    if expected == "BLOCK":
        preparation["grant_bytes"] = grant_bytes("actor:supplier:other-grantee")
    after = api().prepare_supplier_authority(**preparation)
    assert domain_frame(after) == frame
    for ordinal in range(2):
        with monkeypatch.context() as patch:
            if expected == "CLARIFY" and ordinal == 0:

                def unavailable(*args, **kwargs):
                    raise RuntimeError("controlled DIRECT_GRANT engine failure")

                patch.setattr(check_executor, "execute_program", unavailable)
            after = api().record_supplier_authority_check(
                **check_arguments(preparation, ordinal)
            )
        assert domain_frame(after) == frame
        record = after.protocol_replay.data["records"][
            "authority:supplier:" + str(ordinal)
        ]
        outcome = (
            "UNKNOWN"
            if expected == "CLARIFY" and ordinal == 0
            else ("VIOLATED" if expected == "BLOCK" else "SATISFIED")
        )
        assert record["record"]["assessment_outcome"] == outcome
        if outcome == "UNKNOWN":
            assert record["record_type"] == "UnavailableAuthorityAssessment"
            assert (
                after.protocol_replay.data["records"]["authority-failure:supplier:0"][
                    "record_type"
                ]
                == "MonitorFailure"
            )

    def forbidden(*args, **kwargs):
        pytest.fail("authorization or replay invoked a check producer")

    monkeypatch.setattr(check_executor.CheckExecutor, "execute", forbidden)
    after = api().decide_supplier_authorization(**decision_arguments(preparation))
    assert domain_frame(after) == frame
    records = after.protocol_replay.data["records"]
    decision = records["authorization:supplier:1"]["record"]
    assert decision["authorization_verdict"] == expected
    assert decision["authorized_actor_id"] == EXECUTOR
    assert decision["authorization_valid_from"] == (
        TIME if expected == "AUTHORIZE" else None
    )
    assert decision["authorization_valid_to"] == (
        "2026-09-08T07:00:00Z" if expected == "AUTHORIZE" else None
    )
    target = {
        "AUTHORIZE": "AUTHORIZED",
        "BLOCK": "BLOCKED",
        "CLARIFY": "CLARIFICATION_REQUIRED",
    }[expected]
    assert after.protocol_replay.data["state"]["protocol"]["authorization_states"] == [
        {"keys": [entry.ACTION], "value": target}
    ]
    assert not {"ActionDispatch", "ActionExecution", "OutcomeObservation"} & {
        r["record_type"] for r in records.values()
    }
    assert after.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    isolated = tmp_path / "reopened"
    isolated.mkdir()
    path = isolated / "history.jsonl"
    shutil.copyfile(owner.path, path)
    reopened = core.KnowledgeChangeHistory.reopen(path).replay()
    assert reopened.receipt == after.receipt
    assert domain_frame(reopened) == frame
    assert [p.name for p in isolated.iterdir()] == ["history.jsonl"]


@pytest.mark.parametrize(
    "fault", ["stale", "grant-bytes", "grant-hash", "interval", "time", "duplicate"]
)
def test_invalid_preparation_refuses_before_retention(preparation, fault):
    owner = preparation["history"]
    if fault == "stale":
        preparation["expected_count"] -= 1
    elif fault == "grant-bytes":
        preparation["grant_bytes"] = b"not JSON"
    elif fault == "grant-hash":
        grant = json.loads(preparation["grant_bytes"])
        grant["content_hash"] = content_digest("wrong")
        preparation["grant_bytes"] = entry.ingress.canonical(grant)
    elif fault == "interval":
        preparation["requested_interval_bytes"] = b"{}"
    elif fault == "time":
        preparation["generated_at"] = "2026-09-08T06:00:00"
    else:
        preparation["scope_association_id"] = preparation["current_context_id"]
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(api().SupplierAuthorityError):
        api().prepare_supplier_authority(**preparation)
    assert (owner.path.read_bytes(), owner.replay().receipt) == before


@pytest.mark.parametrize("function", FUNCTIONS)
def test_substitute_owner_refuses_without_consulting_it(preparation, function):
    args = {
        "prepare_supplier_authority": lambda: preparation,
        "record_supplier_authority_check": lambda: check_arguments(preparation, 0),
        "decide_supplier_authorization": lambda: decision_arguments(preparation),
    }[function]()

    class OtherOwner:
        def __getattr__(self, name):
            pytest.fail("substitute owner consulted: " + name)

    args["history"] = OtherOwner()
    with pytest.raises(api().SupplierAuthorityError):
        getattr(api(), function)(**args)


def test_unaccepted_proposal_cannot_prepare_authority(
    preparation, input_prefix, tmp_path
):
    pending = tmp_path / "pending"
    pending.mkdir()
    inputs = entry.inputs.__wrapped__(pending, input_prefix)
    owner = inputs[0]
    entry.api().submit_supplier_proposal(**entry.submit_arguments(inputs))
    preparation.update(history=owner, **entry.position(owner))
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(api().SupplierAuthorityError):
        api().prepare_supplier_authority(**preparation)
    assert (owner.path.read_bytes(), owner.replay().receipt) == before


def test_domain_frame_preserves_public_canonical_and_frozen_values(accepted_prefix):
    replay = core.KnowledgeChangeHistory.reopen(accepted_prefix).replay()
    frame = domain_frame(replay)
    assert type(frame[3]) is bytes
    assert len(frame[4]) == len(replay.change_sets) == 2
    assert all(type(value) is bytes for value in frame[4])
    assert frame[5] == tuple(sorted(replay.record_history.items()))
    assert all(value.__dataclass_params__.frozen for _, value in frame[5])
    assert all(type(value) is bytes for value in frame[6])
    assert frame == domain_frame(
        core.KnowledgeChangeHistory.reopen(accepted_prefix).replay()
    )


def test_protocol_snapshot_never_uses_deepcopy():
    import ast
    from pathlib import Path

    tree = ast.parse(Path(__file__).read_text())
    assert not any(
        isinstance(n, ast.alias) and n.name == "deepcopy" for n in ast.walk(tree)
    )
    assert not any(
        isinstance(n, ast.Attribute) and n.attr == "deepcopy" for n in ast.walk(tree)
    )

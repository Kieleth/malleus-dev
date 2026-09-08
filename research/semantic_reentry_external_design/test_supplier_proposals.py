"""Real supplier protocol entry from an authored action, not a fake synthesizer."""

from copy import deepcopy
from importlib import import_module
import inspect
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import content_digest, record_hash
from malleus.source import source_artifact_fields
from research.semantic_reentry_external_design import (
    test_supplier_initialization as initial,
)
from research.semantic_reentry_external_design import (
    test_supplier_initial_source as ingress,
)
from research.semantic_reentry_external_design.accepted_read_view import (
    freeze_accepted_replay,
)
from research.semantic_reentry_external_design.supplier_initialization import (
    initialize_supplier_protocol,
    _draft,
)
from research.semantic_reentry_external_design.supplier_program import (
    build_supplier_program,
)
from research.semantic_reentry_external_design.test_supplier_action_contract import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_proposals"
TIME = "2026-09-08T06:00:00Z"
ACTOR = "actor:supplier:proposer"
ROLE_IDS = {
    role: "source:supplier:" + role
    for role in ("goal", "preservation", "mapping", "pre_state_source")
}
CONTEXT = "context:supplier:authored-action"
ACTION = "action:supplier:authored-action"
PROPOSAL = "proposal:supplier:authored-action"


def api():
    return import_module(MODULE)


def test_contract_api_is_present_and_has_no_required_input_defaults():
    for name in (
        "original_supplier_context",
        "submit_supplier_proposal",
        "record_supplier_type_check",
        "decide_supplier_proposal",
    ):
        function = getattr(api(), name)
        assert all(
            p.default is inspect.Parameter.empty
            for p in inspect.signature(function).parameters.values()
        )


@pytest.fixture(scope="module")
def input_prefix(tmp_path_factory, compilation, action_compilation):
    api()  # Missing implementation refuses before history construction.
    directory = tmp_path_factory.mktemp("supplier-proposal-source")
    owner = ingress.complement_owner.__wrapped__(directory, compilation)
    values = ingress.initial_inputs.__wrapped__()
    prepared = import_module(ingress.PRODUCER).prepare_initial_supplier_change(
        **ingress.initial_arguments(owner, values)
    )
    core.admit_structural_change(
        history=owner,
        preparation=prepared,
        transaction_time=ingress.TIME,
        actor_id=ingress.ACTOR,
    )
    program = build_supplier_program(
        action_compilation.artifact.artifact_bytes,
        source_ids=initial.SOURCES,
        policy_ids=initial.POLICIES,
    )
    args = initial.arguments.__wrapped__(
        tmp_path_factory.mktemp("supplier-proposal-init"), owner.path, program
    )
    initialize_supplier_protocol(**args)
    owner = args["history"]
    replay = owner.replay()
    trace = core.trace_population_record(replay, "supplier-order-state:B:e4")
    assert len(trace.sources) == 1 and trace.sources[0].record_id == ingress.SOURCE_ID
    assert trace.sources[0].content == values["source_bytes"]
    case = json.loads((ingress.FIXTURE / "case.json").read_bytes())
    contents = {
        "goal": ingress.canonical(case["goal"]),
        "mapping": ingress.canonical(case["mapping"]),
        "preservation": ingress.canonical(case["preservation"]),
        "pre_state_source": trace.sources[0].content,
    }
    for role, content in contents.items():
        identifier = ROLE_IDS[role]
        value = make_record(
            "SourceArtifact",
            id=identifier,
            event_id="event:" + identifier,
            generated_at=TIME,
            actor_id=ACTOR,
            role="registrar",
            source_record_ids=[],
            artifact_kind="SOURCE",
            artifact_version="research-v1",
            **source_artifact_fields(
                artifact_id=identifier,
                artifact_version="research-v1",
                source_bytes=content,
                media_type="application/json",
                locator="urn:retained:" + identifier,
            ),
        )
        replay = owner.append_protocol_events(
            transaction="source",
            events=(_draft("SourceArtifact", value, content=content),),
            expected_head=replay.ledger_head,
            expected_count=replay.ledger_event_count,
        )
    return owner.path, args["initialization_id"], case


@pytest.fixture
def inputs(tmp_path, input_prefix):
    path, initialization_id, case = input_prefix
    target = tmp_path / "history.jsonl"
    shutil.copyfile(path, target)
    owner = core.KnowledgeChangeHistory.reopen(target)
    replay = owner.replay()
    view = freeze_accepted_replay(replay=replay, context=owner.composition_context())
    original_args = dict(
        view=view,
        initialization_id=initialization_id,
        source_ids=deepcopy(ROLE_IDS),
        context_id=CONTEXT,
        action_id=ACTION,
        proposal_id=PROPOSAL,
        episode_key=case["episode"]["id"],
    )
    original = api().original_supplier_context(**original_args)
    policy = replay.protocol_replay.data["records"][initial.POLICIES["authorization"]][
        "record"
    ]
    payload = {
        "logical_source_id": ingress.SOURCE_ID,
        "supplier_order_id": "B",
        "product_code": "Y",
        "expected_quantity": 1,
        "requested_quantity": 2,
        "expected_source_digest": case["source"]["sha256"],
        "new_source_occurrence_id": case["operator"]["new_source_occurrence_id"],
    }
    action = make_record(
        "SupplierOrderAmendment",
        id=ACTION,
        event_id="event:" + PROPOSAL,
        generated_at=TIME,
        actor_id=ACTOR,
        role="proposer",
        source_record_ids=[CONTEXT, policy["id"]],
        action_type="AMEND_SUPPLIER_ORDER",
        action_payload_hash=content_digest(payload),
        action_key=case["episode"]["action_key"],
        revision=1,
        authorization_policy_id=policy["id"],
        authorization_policy_hash=policy["content_hash"],
        **payload,
    )
    return owner, original_args, original, action


def position(owner):
    replay = owner.replay()
    return dict(
        expected_head=replay.ledger_head, expected_count=replay.ledger_event_count
    )


def submit_arguments(inputs):
    owner, _, original, action = inputs
    return dict(
        history=owner,
        original_context_bytes=original,
        action_bytes=ingress.canonical(action),
        proposal_key="supplier:authored-fixture:proposal",
        context_actor_id=ACTOR,
        artifact_version="research-v1",
        **position(owner),
    )


def check_arguments(owner, ordinal):
    policy = owner.replay().protocol_replay.data["records"][
        initial.POLICIES["epistemic"]
    ]["record"]
    return dict(
        history=owner,
        proposal_id=PROPOSAL,
        context_id=CONTEXT,
        monitor_id=policy["required_monitor_ids"][ordinal],
        assessment_id="assessment:supplier:" + str(ordinal),
        failure_id="failure:supplier:" + str(ordinal),
        actor_id="actor:supplier:type-checker",
        generated_at=TIME,
        **position(owner),
    )


def decision_arguments(owner):
    return dict(
        history=owner,
        proposal_id=PROPOSAL,
        context_id=CONTEXT,
        assessment_ids=("assessment:supplier:0", "assessment:supplier:1"),
        decision_id="decision:supplier:1",
        transition_id="transition:supplier:1",
        actor_id="actor:supplier:epistemic-controller",
        generated_at=TIME,
        **position(owner),
    )


def test_original_context_is_pure_canonical_and_binds_actual_sources(
    inputs, monkeypatch
):
    import builtins

    owner, args, content, action = inputs
    before = owner.path.read_bytes()
    value = json.loads(content)
    assert ingress.canonical(value) == content
    assert value["prefix"] == {
        "head": args["view"].context.base_ledger_head,
        "event_count": args["view"].context.base_ledger_event_count,
    }
    assert (
        value["domain"]["accepted_graph_digest"] == owner.replay().graph.state_digest()
    )
    assert value["action_id"] == action["id"]
    assert value["pre_state_source"]["bytes_sha256"] == action["expected_source_digest"]

    def forbidden(*a, **k):
        pytest.fail("pure context construction performed I/O")

    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", forbidden)
        patch.setattr(Path, "open", forbidden)
        assert api().original_supplier_context(**args) == content
    assert owner.path.read_bytes() == before


def test_real_supplier_proposal_checks_and_acceptance_preserve_domain(
    inputs, monkeypatch, tmp_path
):
    owner = inputs[0]
    before = owner.replay()
    after = api().submit_supplier_proposal(**submit_arguments(inputs))
    assert initial.domain(after) == initial.domain(before)
    assert after.protocol_replay.data["state"]["protocol"]["proposal_states"] == [
        {"keys": [PROPOSAL], "value": "PROPOSED"}
    ]
    for ordinal in range(2):
        after = api().record_supplier_type_check(**check_arguments(owner, ordinal))
        assert initial.domain(after) == initial.domain(before)
        assert (
            after.protocol_replay.data["records"][
                "assessment:supplier:" + str(ordinal)
            ]["record"]["assessment_outcome"]
            == "SATISFIED"
        )
    from research.action_history_contract_freeze.programs.check_executor import (
        CheckExecutor,
    )

    with monkeypatch.context() as patch:
        patch.setattr(
            CheckExecutor,
            "execute",
            lambda *a, **k: pytest.fail("decision/replay executed a producer"),
        )
        after = api().decide_supplier_proposal(**decision_arguments(owner))
        assert initial.domain(after) == initial.domain(before)
        assert after.protocol_replay.data["state"]["protocol"]["proposal_states"] == [
            {"keys": [PROPOSAL], "value": "ACCEPTED"}
        ]
        assert (
            after.protocol_replay.data["state"]["action_acceptance_head"]
            != before.protocol_replay.data["state"]["action_acceptance_head"]
        )
        assert (
            after.protocol_replay.data["records"]["decision:supplier:1"]["record"][
                "epistemic_verdict"
            ]
            == "ACCEPT"
        )
        reopened_dir = tmp_path / "reopened"
        reopened_dir.mkdir()
        copied = reopened_dir / "history.jsonl"
        shutil.copyfile(owner.path, copied)
        assert (
            core.KnowledgeChangeHistory.reopen(copied).replay().receipt == after.receipt
        )
    assert after.protocol_replay.data["state"]["protocol"]["authorization_states"] == [
        {"keys": [ACTION], "value": "PENDING"}
    ]
    assert after.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1


@pytest.mark.parametrize(
    "fault",
    [
        "stale",
        "original-head",
        "payload",
        "record",
        "source",
        "operator",
        "extra",
        "action-id",
        "policy",
        "provenance",
    ],
)
def test_bad_supplier_proposal_refuses_whole_atomic_pair(inputs, fault):
    owner = inputs[0]
    args = submit_arguments(inputs)
    if fault == "stale":
        args["expected_count"] -= 1
    elif fault in {"original-head", "source"}:
        original = json.loads(args["original_context_bytes"])
        if fault == "original-head":
            original["prefix"]["head"] = content_digest("stale")
        else:
            original["goal"]["bytes_sha256"] = content_digest("wrong")
        args["original_context_bytes"] = ingress.canonical(original)
    else:
        action = json.loads(args["action_bytes"])
        if fault == "payload":
            action["action_payload_hash"] = content_digest("wrong")
        elif fault == "record":
            action["content_hash"] = content_digest("wrong")
        elif fault == "operator":
            action["action_type"] = "UNSUPPORTED"
        elif fault == "action-id":
            action["id"] = "action:wrong-context-binding"
        elif fault == "policy":
            action["authorization_policy_hash"] = content_digest("wrong policy")
        elif fault == "provenance":
            action["source_record_ids"] = [CONTEXT]
        else:
            action["operations"] = []
        if fault != "record":
            action["content_hash"] = record_hash("SupplierOrderAmendment", action)
        args["action_bytes"] = ingress.canonical(action)
    before, receipt = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError) as caught:
        api().submit_supplier_proposal(**args)
    if fault in {"action-id", "policy", "provenance"}:
        assert (
            type(caught.value).__module__
            == "malleus._contract_pipeline.protocol_runtime"
        )
        assert type(caught.value).__name__ == "ProtocolProgramRefusal"
    else:
        assert type(caught.value) is api().SupplierProtocolError
    assert owner.path.read_bytes() == before and owner.replay().receipt == receipt


@pytest.mark.parametrize("moment", ["before-producer", "after-producer"])
def test_moving_prefix_never_rebases_a_real_check(inputs, monkeypatch, moment):
    owner = inputs[0]
    api().submit_supplier_proposal(**submit_arguments(inputs))
    args = check_arguments(owner, 0)
    producer = api().run_history_check
    intervening = []

    def advance():
        # Real evidence-only append, not a fake changed context or second writer.
        owner.append_anchors(
            anchors=(
                core.structural_evidence_anchor(
                    record_id="artifact:supplier:intervening-check-note",
                    content=ingress.canonical({"purpose": "stale-check conformance"}),
                    media_type="application/json",
                ),
            ),
            transaction_time=TIME,
            actor_id=ACTOR,
        )
        intervening.append((owner.path.read_bytes(), owner.replay().receipt))

    def moving(history, *, invocation):
        if moment == "before-producer":
            advance()
        result = producer(history, invocation=invocation)
        if moment == "after-producer":
            advance()
        return result

    monkeypatch.setattr(api(), "run_history_check", moving)
    before = owner.replay()
    with pytest.raises(ValueError) as caught:
        api().record_supplier_type_check(**args)
    if moment == "before-producer":
        assert type(caught.value) is api().SupplierProtocolError
        assert caught.value.reason == "STALE_BASE"
    else:
        assert (
            type(caught.value).__module__
            == "malleus._contract_pipeline.protocol_runtime"
        )
        assert type(caught.value).__name__ == "ProtocolProgramRefusal"
        assert caught.value.reason == "STALE_PROTOCOL_BASE"
    assert len(intervening) == 1
    after = owner.replay()
    assert (owner.path.read_bytes(), after.receipt) == intervening[0]
    assert initial.domain(after) == initial.domain(before)
    assert args["assessment_id"] not in after.protocol_replay.data["records"]
    assert args["failure_id"] not in after.protocol_replay.data["records"]


@pytest.mark.parametrize(
    "function", ["record_supplier_type_check", "decide_supplier_proposal"]
)
def test_stale_coordinator_refuses_before_any_producer(inputs, monkeypatch, function):
    owner = inputs[0]
    args = (
        check_arguments(owner, 0)
        if function == "record_supplier_type_check"
        else decision_arguments(owner)
    )
    args["expected_count"] -= 1

    def forbidden(*args, **kwargs):
        pytest.fail("stale coordinator invoked a producer or policy evaluator")

    monkeypatch.setattr(api(), "run_history_check", forbidden)
    monkeypatch.setattr(api(), "evaluate_epistemic_policy", forbidden)
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(api().SupplierProtocolError, match="STALE_BASE"):
        getattr(api(), function)(**args)
    assert (owner.path.read_bytes(), owner.replay().receipt) == before


@pytest.mark.parametrize(
    "function",
    [
        "original_supplier_context",
        "submit_supplier_proposal",
        "record_supplier_type_check",
        "decide_supplier_proposal",
    ],
)
def test_missing_required_inputs_are_typed_and_never_defaulted(function):
    with pytest.raises(api().SupplierProtocolError, match="MALFORMED_INPUT"):
        getattr(api(), function)()


@pytest.mark.parametrize("kind", ["upstream", "knowledge", "check", "local"])
def test_declared_refusal_classes_propagate_the_same_exception(kind):
    from research.action_history_contract_freeze.programs.check_executor import (
        CheckRefusal,
    )

    class UpstreamRefusal(ValueError):
        """An opaque upstream failure, not a simulated completed protocol result."""

    error = {
        "upstream": lambda: UpstreamRefusal("exact failure"),
        "knowledge": lambda: core.KnowledgeChangeRefusal(
            core.KnowledgeChangeRefusalReason.STALE_BASE, "exact failure"
        ),
        "check": lambda: CheckRefusal("exact failure"),
        "local": lambda: api().SupplierProtocolError("CONFORMANCE", "exact failure"),
    }[kind]()

    def refuse():
        raise error

    with pytest.raises(type(error)) as caught:
        api()._guarded(refuse)()
    assert caught.value is error


def test_exception_handlers_do_not_resolve_dependency_attributes_during_failure():
    import ast

    tree = ast.parse(Path(api().__file__).read_text())
    for handler in (n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)):
        assert handler.type is not None
        assert not any(isinstance(n, ast.Attribute) for n in ast.walk(handler.type))


def test_gate_and_runtime_belong_to_this_checkout():
    root = Path(__file__).resolve().parents[2]
    assert Path(core.__file__).resolve().is_relative_to(root / "src/malleus")
    assert Path(api().__file__).resolve().parent == Path(__file__).resolve().parent
    gate = json.loads(
        (Path(__file__).parent / "supplier-proposal-gate.json").read_bytes()
    )
    assert str(Path(__file__).resolve().relative_to(root)) in gate["tests"]
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert all((root / path).is_file() for path in gate["tests"])


def test_adapter_imports_no_test_fixture_or_private_core_implementation():
    import ast

    tree = ast.parse(Path(api().__file__).read_text())
    imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert not any("test_" in name or name.startswith("tests.") for name in imports)
    assert not any(name.startswith("malleus._") for name in imports)


def test_actual_checker_unavailability_records_unknown_and_defers(inputs, monkeypatch):
    from research.action_history_contract_freeze.programs import check_executor

    owner = inputs[0]
    before = owner.replay()
    api().submit_supplier_proposal(**submit_arguments(inputs))
    with monkeypatch.context() as patch:

        def unavailable(*args, **kwargs):
            raise RuntimeError("controlled producer failure")

        patch.setattr(
            check_executor,
            "execute_program",
            unavailable,
        )
        first = api().record_supplier_type_check(**check_arguments(owner, 0))
    records = first.protocol_replay.data["records"]
    assert records["failure:supplier:0"]["record_type"] == "MonitorFailure"
    assert records["assessment:supplier:0"]["record_type"] == "UnavailableAssessment"
    assert records["assessment:supplier:0"]["record"]["assessment_outcome"] == "UNKNOWN"
    api().record_supplier_type_check(**check_arguments(owner, 1))
    after = api().decide_supplier_proposal(**decision_arguments(owner))
    assert (
        after.protocol_replay.data["records"]["decision:supplier:1"]["record"][
            "epistemic_verdict"
        ]
        == "DEFER"
    )
    assert initial.domain(after) == initial.domain(before)


@pytest.mark.parametrize(
    "function",
    [
        "submit_supplier_proposal",
        "record_supplier_type_check",
        "decide_supplier_proposal",
    ],
)
def test_substitute_owner_is_never_consulted(inputs, function):
    owner = inputs[0]
    args = {
        "submit_supplier_proposal": lambda: submit_arguments(inputs),
        "record_supplier_type_check": lambda: check_arguments(owner, 0),
        "decide_supplier_proposal": lambda: decision_arguments(owner),
    }[function]()

    class OtherOwner:
        def __getattr__(self, name):
            pytest.fail("substitute owner was consulted: " + name)

    args["history"] = OtherOwner()
    with pytest.raises(api().SupplierProtocolError):
        getattr(api(), function)(**args)

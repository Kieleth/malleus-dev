"""Actual read-only capture after execution, not a receipt-to-fact shortcut."""

from importlib import import_module
import inspect
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from research.semantic_reentry_external_design import (
    test_supplier_execution as execution,
)
from research.semantic_reentry_external_design.test_supplier_proposals import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_observation"
TIME = "2026-09-08T06:30:00Z"
CONTRACT = "outcome-contract:supplier:source"
OBSERVER_SOURCE = "source:supplier:observer-implementation"
FUNCTIONS = ("register_supplier_observer", "observe_supplier_execution")


def api():
    return import_module(MODULE)


def test_observation_contract_api_has_no_required_input_defaults():
    for name in FUNCTIONS:
        assert all(
            p.default is inspect.Parameter.empty
            for p in inspect.signature(getattr(api(), name)).parameters.values()
        )
    assert type(api().IMPLEMENTATION_BYTES) is bytes


def register_arguments(owner):
    return dict(
        history=owner,
        **execution.entry.position(owner),
        implementation_source_id=OBSERVER_SOURCE,
        outcome_contract_id=CONTRACT,
        actor_id="actor:supplier:observer-registrar",
        generated_at=TIME,
        artifact_version="research-v1",
    )


def observation_arguments(owner, path):
    return dict(
        history=owner,
        **execution.entry.position(owner),
        execution_id="execution:supplier:1",
        outcome_contract_id=CONTRACT,
        observer_id="actor:supplier:observer",
        observed_source_id="source:supplier:captured:1",
        observation_id="observation:supplier:1",
        observed_at=TIME,
        source_path=path,
        logical_source_id=execution.entry.ingress.SOURCE_ID,
        artifact_version="research-v1",
    )


@pytest.fixture(scope="module")
def observed_prefixes(tmp_path_factory, compilation, action_compilation):
    api()
    prefix = execution.execution_prefix.__wrapped__(
        tmp_path_factory, compilation, action_compilation
    )
    cases = {}
    for fault in ("none", "unchanged-success", "after-write"):
        args = execution.execution_inputs.__wrapped__(
            tmp_path_factory.mktemp("supplier-observation-execution"), prefix
        )
        writer = execution.api()._write_source

        def controlled(stream, content):
            if fault != "unchanged-success":
                writer(stream, content)
            if fault == "after-write":
                raise OSError("controlled failure after write")

        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(execution.api(), "_write_source", controlled)
            execution.api().dispatch_and_execute_supplier(**args)
        owner = args["history"]
        api().register_supplier_observer(**register_arguments(owner))
        cases[fault] = owner.path, args["source_path"]
    return cases


@pytest.fixture
def observation_inputs(tmp_path, observed_prefixes):
    def copied(fault):
        ledger, source = observed_prefixes[fault]
        path, target = tmp_path / "history.jsonl", tmp_path / "supplier.jsonl"
        shutil.copyfile(ledger, path)
        shutil.copyfile(source, target)
        return core.KnowledgeChangeHistory.reopen(path), target

    return copied


@pytest.mark.parametrize(
    "fault,expected,status",
    [
        ("none", "CONFIRMED", "SUCCEEDED"),
        ("unchanged-success", "CONTRADICTED", "SUCCEEDED"),
        ("after-write", "CONFIRMED", "FAILED"),
        ("malformed", "INDETERMINATE", "SUCCEEDED"),
    ],
)
def test_actual_capture_is_separate_from_execution_and_accepted_knowledge(
    observation_inputs, tmp_path, monkeypatch, fault, expected, status
):
    owner, source = observation_inputs("none" if fault == "malformed" else fault)
    if fault == "malformed":
        source.write_bytes(b"actual malformed controlled source\n")
    actual = source.read_bytes()
    frame = execution.authority.domain_frame(owner.replay())
    args = observation_arguments(owner, source)
    after = api().observe_supplier_execution(**args)
    assert source.read_bytes() == actual
    assert execution.authority.domain_frame(after) == frame
    records = after.protocol_replay.data["records"]
    observation = records[args["observation_id"]]["record"]
    assert observation["observation_result"] == expected
    assert records[args["execution_id"]]["record"]["execution_status"] == status
    assert after.retained_bytes(args["observed_source_id"]) == actual
    assert (
        observation["observed_source_artifact_hash"]
        == records[args["observed_source_id"]]["record"]["content_hash"]
    )
    assert after.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1

    def forbidden(*args, **kwargs):
        pytest.fail("reopen or duplicate observation invoked capture")

    monkeypatch.setattr(api(), "_capture", forbidden)
    repeated = dict(
        args,
        **execution.entry.position(owner),
        observed_source_id="source:supplier:captured:retry",
        observation_id="observation:supplier:retry",
    )
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError):
        api().observe_supplier_execution(**repeated)
    assert (owner.path.read_bytes(), owner.replay().receipt) == before
    isolated = tmp_path / "jsonl-only"
    isolated.mkdir()
    path = isolated / "history.jsonl"
    shutil.copyfile(owner.path, path)
    assert core.KnowledgeChangeHistory.reopen(path).replay().receipt == after.receipt
    assert [p.name for p in isolated.iterdir()] == ["history.jsonl"]


@pytest.mark.parametrize(
    "fault",
    [
        "stale",
        "observer",
        "source",
        "time",
        "missing-source",
        "implementation",
        "relative-path",
        "symlink",
    ],
)
def test_ineligible_capture_refuses_without_retention(
    observation_inputs, monkeypatch, fault
):
    owner, source = observation_inputs("none")
    args = observation_arguments(owner, source)
    if fault == "stale":
        args["expected_count"] -= 1
    elif fault == "observer":
        args["observer_id"] = execution.authority.EXECUTOR
    elif fault == "source":
        args["logical_source_id"] = "source:other"
    elif fault == "time":
        args["observed_at"] = execution.DISPATCH_TIME
    elif fault == "implementation":
        monkeypatch.setattr(api(), "IMPLEMENTATION_IDENTITY", "sha256:" + "0" * 64)
    elif fault == "relative-path":
        args["source_path"] = Path("supplier.jsonl")
    elif fault == "symlink":
        link = source.with_name("supplier-link.jsonl")
        link.symlink_to(source)
        args["source_path"] = link
    else:
        args["source_path"] = source.with_name("absent.jsonl")

    def forbidden(*args, **kwargs):
        pytest.fail("ineligible observation invoked capture")

    monkeypatch.setattr(api(), "_capture", forbidden)
    before = owner.path.read_bytes(), source.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError):
        api().observe_supplier_execution(**args)
    assert (
        owner.path.read_bytes(),
        source.read_bytes(),
        owner.replay().receipt,
    ) == before


def test_observer_identity_is_actual_and_does_not_import_executor_or_model():
    import ast
    from hashlib import sha256

    module = api()
    assert module.IMPLEMENTATION_BYTES == Path(module.__file__).read_bytes()
    assert (
        module.IMPLEMENTATION_IDENTITY
        == "sha256:" + sha256(module.IMPLEMENTATION_BYTES).hexdigest()
    )
    for node in ast.walk(ast.parse(module.IMPLEMENTATION_BYTES)):
        if isinstance(node, ast.ImportFrom):
            assert node.module is not None
            assert not node.module.startswith(("malleus._", "tests."))
            assert not any(part.startswith("test_") for part in node.module.split("."))
            assert not any(
                name in node.module
                for name in ("supplier_components", "supplier_execution")
            )
        elif isinstance(node, ast.ExceptHandler):
            assert node.type is not None
            assert not any(isinstance(n, ast.Attribute) for n in ast.walk(node.type))


def test_capture_io_failure_retains_no_empty_source_or_observation(
    observation_inputs, monkeypatch
):
    owner, source = observation_inputs("none")
    args = observation_arguments(owner, source)
    original_open = api().os.open

    def unavailable(path, *values, **kwargs):
        if path == source:
            raise OSError("controlled source-read failure")
        return original_open(path, *values, **kwargs)

    monkeypatch.setattr(api().os, "open", unavailable)
    before = owner.path.read_bytes(), source.read_bytes(), owner.replay().receipt
    with pytest.raises(api().SupplierObservationError, match="CAPTURE_UNAVAILABLE"):
        api().observe_supplier_execution(**args)
    assert (
        owner.path.read_bytes(),
        source.read_bytes(),
        owner.replay().receipt,
    ) == before


def test_history_movement_after_capture_refuses_before_source_retention(
    observation_inputs, monkeypatch
):
    owner, source = observation_inputs("none")
    args = observation_arguments(owner, source)
    capture = api()._capture
    intervening = []

    def captured_then_moved(path):
        content = capture(path)
        owner.append_anchors(
            anchors=(
                core.structural_evidence_anchor(
                    record_id="evidence:supplier:during-capture",
                    content=b"explicit intervening evidence",
                    media_type="text/plain",
                ),
            ),
            transaction_time=TIME,
            actor_id="actor:supplier:intervening",
        )
        intervening.append(owner.path.read_bytes())
        return content

    monkeypatch.setattr(api(), "_capture", captured_then_moved)
    frame = execution.authority.domain_frame(owner.replay())
    with pytest.raises(ValueError) as caught:
        api().observe_supplier_execution(**args)
    execution.authority.assert_native_refusal(caught.value, "STALE_PROTOCOL_BASE")
    assert len(intervening) == 1 and owner.path.read_bytes() == intervening[0]
    after = owner.replay()
    assert execution.authority.domain_frame(after) == frame
    assert args["observed_source_id"] not in after.protocol_replay.data["records"]
    assert args["observation_id"] not in after.protocol_replay.data["records"]


def test_late_observation_refusal_preserves_capture_but_no_observation(
    observation_inputs, monkeypatch
):
    owner, source = observation_inputs("none")
    args = observation_arguments(owner, source)
    record = api().make_record

    def wrong_execution_hash(kind, **values):
        if kind == "OutcomeObservation":
            values["execution_hash"] = "sha256:" + "0" * 64
        return record(kind, **values)

    monkeypatch.setattr(api(), "make_record", wrong_execution_hash)
    frame = execution.authority.domain_frame(owner.replay())
    with pytest.raises(ValueError) as caught:
        api().observe_supplier_execution(**args)
    execution.authority.assert_native_refusal(caught.value, "UNAPPLIED_EXECUTION")
    after = core.KnowledgeChangeHistory.reopen(owner.path).replay()
    assert execution.authority.domain_frame(after) == frame
    assert after.retained_bytes(args["observed_source_id"]) == source.read_bytes()
    assert args["observation_id"] not in after.protocol_replay.data["records"]


@pytest.mark.parametrize("function", FUNCTIONS)
def test_missing_observer_inputs_have_no_defaults(function):
    with pytest.raises(api().SupplierObservationError, match="MALFORMED_INPUT"):
        getattr(api(), function)()


@pytest.mark.parametrize("function", FUNCTIONS)
def test_substitute_observer_owner_is_not_consulted(function):
    class Substitute:
        def __getattr__(self, name):
            pytest.fail("substitute observer owner consulted: " + name)

    args = {
        name: None for name in inspect.signature(getattr(api(), function)).parameters
    }
    args["history"] = Substitute()
    with pytest.raises(
        api().SupplierObservationError, match="actual owning Core history"
    ):
        getattr(api(), function)(**args)


def test_observation_gate_and_runtime_belong_to_this_checkout():
    import json

    root = Path(__file__).resolve().parents[2]
    assert Path(core.__file__).resolve().is_relative_to(root / "src/malleus")
    assert Path(api().__file__).resolve().parent == Path(__file__).resolve().parent
    gate = json.loads(
        (Path(__file__).parent / "supplier-observation-gate.json").read_bytes()
    )
    assert str(Path(__file__).resolve().relative_to(root)) in gate["tests"]
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert all((root / path).is_file() for path in gate["tests"])

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
    "fault", ["stale", "observer", "source", "time", "missing-source"]
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

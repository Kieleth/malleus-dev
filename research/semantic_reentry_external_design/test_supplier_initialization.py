"""Actual supplier initialization, never historical e7 or a simulated writer."""

from copy import deepcopy
from importlib import import_module
import inspect
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs.check_executor import (
    CheckExecutor,
    load_check_executor,
)
from research.semantic_reentry_external_design.test_supplier_action_contract import (
    compile_supplier_action as compile_supplier_action,
)
from research.semantic_reentry_external_design.test_supplier_program import (
    SOURCES,
    POLICIES,
)
from research.semantic_reentry_external_design.supplier_program import (
    build_supplier_program,
)
from research.semantic_reentry_external_design.test_supplier_initial_source import (
    ACTOR,
    TIME,
    canonical,
    complement_owner,
    initial_arguments,
    initial_inputs,
    PRODUCER,
)


MODULE = "research.semantic_reentry_external_design.supplier_initialization"
CONTROL = {
    "schema": "malleus.reentry.supplier.epistemic-control/research-v1",
    "violation_verdicts": ["REJECT", "REJECT"],
    "unknown_verdicts": ["DEFER", "DEFER"],
    "control_precedence": ["REJECT", "DEFER", "CONTEST"],
}


def initializer():
    return import_module(MODULE).initialize_supplier_protocol


@pytest.fixture(scope="module")
def supplier_prefix(tmp_path_factory, compilation):
    # Reuse only test setup that calls real public source/population/admission.
    owner = complement_owner.__wrapped__(
        tmp_path_factory.mktemp("supplier-init-prefix"), compilation
    )
    prepared = import_module(PRODUCER).prepare_initial_supplier_change(
        **initial_arguments(owner, initial_inputs.__wrapped__())
    )
    api.admit_structural_change(
        history=owner, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )
    return owner.path


@pytest.fixture
def arguments(tmp_path, supplier_prefix, initialization_program):
    path = tmp_path / "history.jsonl"
    shutil.copyfile(supplier_prefix, path)
    owner = api.KnowledgeChangeHistory.reopen(path)
    before = owner.replay()
    return dict(
        history=owner,
        expected_head=before.ledger_head,
        expected_count=before.ledger_event_count,
        program_bytes=initialization_program,
        program_record_id="artifact:supplier:program",
        selection_event_id="event:supplier:select",
        initialization_id="source:supplier:initialization",
        checker=load_check_executor(),
        checker_source_ids={
            "definition": "source:supplier:checks:definition",
            "implementation": "source:supplier:checks:implementation",
        },
        monitor_ids={
            "epistemic": ["monitor:supplier:type:0", "monitor:supplier:type:1"],
            "authorization": [
                "monitor:supplier:authority:0",
                "monitor:supplier:authority:1",
            ],
        },
        ruleset_id="ruleset:supplier:type",
        epistemic_control_bytes=canonical(CONTROL),
        transaction_time="2026-09-08T05:00:00Z",
        actor_id="actor:supplier:registrar",
        artifact_version="research-v1",
    )


@pytest.fixture(scope="module", name="initialization_program")
def compile_initialization_program(action_compilation):
    return build_supplier_program(
        action_compilation.artifact.artifact_bytes,
        source_ids=SOURCES,
        policy_ids=POLICIES,
    )


def domain(replay):
    return (
        replay.partial_contract.identity,
        replay.acceptance_head,
        replay.materialization_head,
        replay.graph.export_records(),
        replay.change_sets,
        replay.record_history,
        replay.contract_revisions,
    )


def test_initialize_real_supplier_prefix_preserves_domain_at_every_append(
    arguments, monkeypatch, tmp_path
):
    run = initializer()
    owner = arguments["history"]
    before = owner.replay()
    assert before.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    assert "supplier-order-state:B:e7" not in before.record_history
    append = api.KnowledgeChangeHistory.append_protocol_events
    stages = []

    def checked_append(self, **kwargs):
        after = append(self, **kwargs)
        assert domain(after) == domain(before)
        stages.append(kwargs["transaction"])
        return after

    monkeypatch.setattr(
        api.KnowledgeChangeHistory, "append_protocol_events", checked_append
    )
    monkeypatch.setattr(
        CheckExecutor,
        "execute",
        lambda *a, **k: pytest.fail("initialization ran a check"),
    )
    after = run(**arguments)
    assert type(after) is api.KnowledgeHistoryReplay
    assert len(stages) == 14 and stages[-1] == "initialize"
    assert after.ledger_event_count == before.ledger_event_count + 16
    records = after.protocol_replay.data["records"]
    assert len(records) == 14
    assert {v["record_type"] for v in records.values()} == {
        "SourceArtifact",
        "ProtocolArtifact",
        "MonitorSpecificationArtifact",
        "EpistemicPolicyArtifact",
        "AuthorizationPolicyArtifact",
    }
    for wrapped in records.values():
        value = wrapped["record"]
        assert value["content_hash"] == record_hash(wrapped["record_type"], value)
    for role, identifier in arguments["checker_source_ids"].items():
        assert after.retained_bytes(identifier) == getattr(
            arguments["checker"], role + "_bytes"
        )
    assert after.retained_bytes(arguments["ruleset_id"]) == canonical(CONTROL)
    assert after.retained_bytes(SOURCES["machine"]) == arguments["program_bytes"]
    checkpoint = json.loads(after.retained_bytes(arguments["initialization_id"]))
    assert checkpoint["prefix"]["event_count"] == after.ledger_event_count - 1
    assert checkpoint["domain"]["accepted_graph_digest"] == before.graph.state_digest()
    assert after.protocol_replay.data["state"][
        "action_acceptance_head"
    ] == content_digest(checkpoint)
    assert checkpoint["epistemic_policy"]["id"] == POLICIES["epistemic"]
    assert checkpoint["authorization_policy"]["id"] == POLICIES["authorization"]
    for role, ids in arguments["monitor_ids"].items():
        policy = records[POLICIES[role]]["record"]
        assert policy["required_monitor_ids"] == ids
        for identifier in ids:
            monitor = records[identifier]["record"]
            assert (
                monitor["monitor_implementation_hash"]
                == arguments["checker"].implementation_reference["bytes_sha256"]
            )
    reopened_dir = tmp_path / "jsonl-only"
    reopened_dir.mkdir()
    copy = reopened_dir / "history.jsonl"
    shutil.copyfile(owner.path, copy)
    assert list(reopened_dir.iterdir()) == [copy]
    old_read = Path.read_bytes

    def log_only(path):
        if path.resolve() != copy.resolve():
            pytest.fail("reopen consulted a non-ledger file: " + str(path))
        return old_read(path)

    monkeypatch.setattr(Path, "read_bytes", log_only)
    reopened = api.KnowledgeChangeHistory.reopen(copy).replay()
    assert reopened.receipt == after.receipt
    assert reopened.protocol_replay == after.protocol_replay
    assert domain(reopened) == domain(before)


@pytest.mark.parametrize(
    "fault",
    [
        "head",
        "count",
        "boolean-count",
        "program",
        "tampered-program",
        "checker",
        "missing-source",
        "unknown-source",
        "duplicate-id",
        "retained-id",
        "monitor-arity",
        "monitor-order",
        "blank-actor",
        "time",
        "version",
        "control-unknown",
        "control-missing",
        "control-outcome",
        "control-canonical",
    ],
)
def test_bad_initialization_refuses_before_any_retention(arguments, fault):
    run = initializer()
    owner = arguments["history"]
    before, original = owner.path.read_bytes(), owner.replay().receipt
    if fault == "head":
        arguments["expected_head"] = "sha256:" + "0" * 64
    elif fault in {"count", "boolean-count"}:
        arguments["expected_count"] = (
            True if fault == "boolean-count" else arguments["expected_count"] + 1
        )
    elif fault == "program":
        arguments["program_bytes"] = b"{}"
    elif fault == "tampered-program":
        program = json.loads(arguments["program_bytes"])
        del program["transactions"]["observation"]
        arguments["program_bytes"] = canonical(program)
    elif fault == "checker":
        arguments["checker"] = object()
    elif fault == "missing-source":
        del arguments["checker_source_ids"]["definition"]
    elif fault == "unknown-source":
        arguments["checker_source_ids"]["extra"] = "source:extra"
    elif fault == "duplicate-id":
        arguments["ruleset_id"] = arguments["initialization_id"]
    elif fault == "retained-id":
        arguments["ruleset_id"] = owner.replay().retained_inputs[0].record_id
    elif fault == "monitor-arity":
        arguments["monitor_ids"]["epistemic"].pop()
    elif fault == "monitor-order":
        arguments["monitor_ids"]["authorization"].reverse()
    elif fault == "blank-actor":
        arguments["actor_id"] = " "
    elif fault == "time":
        arguments["transaction_time"] = "2026-09-08T05:00:00"
    elif fault == "version":
        arguments["artifact_version"] = ""
    else:
        control = deepcopy(CONTROL)
        if fault == "control-unknown":
            control["fallback"] = "ACCEPT"
        elif fault == "control-missing":
            del control["unknown_verdicts"]
        elif fault == "control-outcome":
            control["unknown_verdicts"][0] = "ACCEPT"
        arguments["epistemic_control_bytes"] = canonical(control)
        if fault == "control-canonical":
            arguments["epistemic_control_bytes"] += b"\n"
    with pytest.raises(import_module(MODULE).SupplierInitializationError) as refused:
        run(**arguments)
    assert refused.value.reason in {
        "MALFORMED_INPUT",
        "UNSUPPORTED",
        "STALE_BASE",
        "DUPLICATE_ID",
    }
    assert owner.path.read_bytes() == before and owner.replay().receipt == original


def test_substitute_owner_is_refused_before_any_callback(arguments):
    calls = []

    class OtherOwner:
        def __getattr__(self, name):
            calls.append(name)
            pytest.fail("substitute owner was consulted")

    arguments["history"] = OtherOwner()
    with pytest.raises(import_module(MODULE).SupplierInitializationError):
        initializer()(**arguments)
    assert calls == []


def test_second_initialization_refuses_without_reselection_or_retention(arguments):
    run = initializer()
    after = run(**arguments)
    owner = arguments["history"]
    before = owner.path.read_bytes()
    arguments.update(
        expected_head=after.ledger_head, expected_count=after.ledger_event_count
    )
    with pytest.raises(import_module(MODULE).SupplierInitializationError) as refused:
        run(**arguments)
    assert refused.value.reason == "ALREADY_SELECTED"
    assert owner.path.read_bytes() == before


def test_every_initializer_input_is_explicit_and_no_test_helpers_are_imported():
    run = initializer()
    assert all(
        p.default is inspect.Parameter.empty
        for p in inspect.signature(run).parameters.values()
    )
    source = inspect.getsource(import_module(MODULE))
    assert "test_" not in source and 'content_digest("pending")' not in source


def test_initialization_gate_and_runtime_are_from_this_checkout():
    root = Path(__file__).resolve().parents[2]
    assert Path(api.__file__).resolve().is_relative_to(root / "src")
    assert (
        Path(inspect.getfile(initializer())).resolve().parent
        == Path(__file__).resolve().parent
    )
    manifest = json.loads(
        (Path(__file__).parent / "supplier-initialization-gate.json").read_bytes()
    )
    paths = manifest["tests"]
    assert paths and len(paths) == len(set(paths))
    assert all((root / path).is_file() for path in paths)

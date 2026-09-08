"""Actual capture through public population, never receipt or oracle as source."""

from importlib import import_module
import inspect
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from research.semantic_reentry_external_design import (
    test_supplier_observation as observe,
)
from research.semantic_reentry_external_design.test_supplier_proposals import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_observed_source"
TIME = "2026-09-08T06:40:00Z"
ACTOR = "actor:supplier:observed-population"
SOURCE = "source:supplier:observed-population:1"
EVIDENCE = "evidence:supplier:observation-binding:1"
REPLACEMENT = "supplier-order-state:B:reentry-amendment-1"


def api():
    return import_module(MODULE)


def test_observed_source_api_has_no_required_input_defaults():
    function = api().prepare_observed_supplier_change
    assert all(
        p.default is inspect.Parameter.empty
        for p in inspect.signature(function).parameters.values()
    )
    assert type(api().ADAPTER_IDENTITY) is str


@pytest.fixture(scope="module")
def captured_prefixes(tmp_path_factory, compilation, action_compilation):
    api()
    cases = observe.observed_prefixes.__wrapped__(
        tmp_path_factory, compilation, action_compilation
    )
    captured = {}
    for fault, (ledger, source) in cases.items():
        owner = core.KnowledgeChangeHistory.reopen(ledger)
        observe.api().observe_supplier_execution(
            **observe.observation_arguments(owner, source)
        )
        captured[fault] = ledger
    return captured


@pytest.fixture
def inputs(tmp_path, captured_prefixes):
    def copied(fault):
        path = tmp_path / "history.jsonl"
        shutil.copyfile(captured_prefixes[fault], path)
        owner = core.KnowledgeChangeHistory.reopen(path)
        case = json.loads(
            (observe.execution.entry.ingress.FIXTURE / "case.json").read_bytes()
        )
        return dict(
            history=owner,
            **observe.execution.entry.position(owner),
            original_context_id=observe.execution.entry.CONTEXT,
            observation_id="observation:supplier:1",
            outcome_contract_id=observe.CONTRACT,
            observer_implementation_identity=observe.api().IMPLEMENTATION_IDENTITY,
            operator_bytes=observe.execution.entry.ingress.canonical(case["operator"]),
            source_id=SOURCE,
            source_artifact_id="artifact:supplier:observed-population:1",
            evidence_id=EVIDENCE,
            plan_id="plan:supplier:observed-population:1",
            history_profile=core.STATE_VERSION_PROFILE,
            transaction_time=TIME,
            actor_id=ACTOR,
        )

    return copied


@pytest.mark.parametrize(
    "fault,status", [("none", "SUCCEEDED"), ("after-write", "FAILED")]
)
def test_actual_observed_bytes_only_change_knowledge_after_admission(
    inputs, fault, status, monkeypatch, tmp_path
):
    args = inputs(fault)
    owner = args["history"]
    before = owner.replay()
    frame = observe.execution.authority.domain_frame(before)
    actual = before.retained_bytes("source:supplier:captured:1")
    original_read = Path.read_bytes

    def no_oracle(path):
        assert "oracle" not in path.parts
        assert path.name not in {"supplier.jsonl", "supplier-order-history.jsonl"}
        return original_read(path)

    monkeypatch.setattr(Path, "read_bytes", no_oracle)
    prepared = api().prepare_observed_supplier_change(**args)
    assert type(prepared) is core.PopulationPreparation
    assert type(prepared.change_set) is core.KnowledgeChangeSet
    assert observe.execution.authority.domain_frame(owner.replay()) == frame
    assert prepared.change_set.sources == (
        (SOURCE, observe.execution.entry.ingress.digest(actual)),
    )
    assert (
        core.KnowledgeChangeSet.from_bytes(prepared.change_set.canonical_bytes)
        == prepared.change_set
    )
    final = core.admit_structural_change(
        history=owner, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )
    assert final.graph.query("SupplierOrderState", supplier_order_id="B") == [
        dict(
            id=REPLACEMENT,
            type="SupplierOrderState",
            supplier_order_id="B",
            product_code="Y",
            source_occurrence_id="reentry-amendment-1",
            ordered_quantity=2,
        )
    ]
    assert len(final.change_sets) == len(before.change_sets) + 1
    for family, members in before.graph.export_records().items():
        assert [
            r for r in final.graph.export_records()[family] if r["id"] != REPLACEMENT
        ] == [r for r in members if r["id"] != "supplier-order-state:B:e4"]
    for identifier, history in before.record_history.items():
        if identifier != "supplier-order-state:B:e4":
            assert final.record_history[identifier] == history
    assert (
        final.record_history["supplier-order-state:B:e4"].superseded_by == REPLACEMENT
    )
    trace = core.trace_population_record(final, REPLACEMENT)
    assert trace.sources[0].record_id == SOURCE
    assert trace.sources[0].content == actual
    binding = json.loads(
        next(e.content for e in trace.evidence if e.record_id == EVIDENCE)
    )
    assert binding["observation"]["id"] == args["observation_id"]
    assert binding["observed_source"]["id"] == "source:supplier:captured:1"
    assert binding["population_source"]["source_id"] == SOURCE
    records = final.protocol_replay.data["records"]
    assert (
        binding["observation"]["record_hash"]
        == records[args["observation_id"]]["record"]["content_hash"]
    )
    assert records["execution:supplier:1"]["record"]["execution_status"] == status
    assert final.protocol_replay == before.protocol_replay
    isolated = tmp_path / "jsonl-only"
    isolated.mkdir()
    path = isolated / "history.jsonl"
    shutil.copyfile(owner.path, path)
    reopened = core.KnowledgeChangeHistory.reopen(path).replay()
    assert reopened.receipt == final.receipt
    assert (
        core.trace_population_record(reopened, REPLACEMENT).sources[0].content == actual
    )
    assert [p.name for p in isolated.iterdir()] == ["history.jsonl"]


def test_unchanged_capture_emits_no_candidate_or_retention(inputs):
    args = inputs("unchanged-success")
    owner = args["history"]
    before = owner.path.read_bytes(), owner.replay().receipt
    assert api().prepare_observed_supplier_change(**args) is None
    assert (owner.path.read_bytes(), owner.replay().receipt) == before
    assert (
        owner.replay().graph.get_node("supplier-order-state:B:e4")["ordered_quantity"]
        == 1
    )


@pytest.mark.parametrize(
    "fault",
    ["stale", "observation", "contract", "implementation", "operator", "source-id"],
)
def test_invalid_observation_mapping_refuses_before_retention(
    inputs, monkeypatch, fault
):
    args = inputs("none")
    owner = args["history"]
    if fault == "stale":
        args["expected_count"] -= 1
    elif fault == "observation":
        args["observation_id"] = "execution:supplier:1"
    elif fault == "contract":
        args["outcome_contract_id"] = observe.OBSERVER_SOURCE
    elif fault == "implementation":
        args["observer_implementation_identity"] = "sha256:" + "0" * 64
    elif fault == "source-id":
        args["source_id"] = "source:supplier:captured:1"
    else:
        value = json.loads(args["operator_bytes"])
        value["requested_quantity"] = 3
        args["operator_bytes"] = observe.execution.entry.ingress.canonical(value)

    def forbidden(*args, **kwargs):
        pytest.fail("invalid observation mapping invoked retention")

    monkeypatch.setattr(core.KnowledgeChangeHistory, "append_anchors", forbidden)
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError):
        api().prepare_observed_supplier_change(**args)
    assert (owner.path.read_bytes(), owner.replay().receipt) == before


def test_observed_candidate_is_not_rebased_at_admission(inputs):
    args = inputs("none")
    owner = args["history"]
    prepared = api().prepare_observed_supplier_change(**args)
    owner.append_anchors(
        anchors=(
            core.structural_evidence_anchor(
                record_id="evidence:supplier:intervening",
                content=b"later evidence",
                media_type="text/plain",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    before = owner.path.read_bytes(), owner.replay().receipt
    with pytest.raises(core.KnowledgeChangeRefusal) as caught:
        core.admit_structural_change(
            history=owner, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    assert caught.value.reason is core.KnowledgeChangeRefusalReason.STALE_BASE
    assert (owner.path.read_bytes(), owner.replay().receipt) == before


def test_missing_observed_mapping_inputs_never_acquire_defaults():
    with pytest.raises(api().SupplierObservationMappingError, match="MALFORMED_INPUT"):
        api().prepare_observed_supplier_change()


def test_substitute_mapping_owner_is_not_consulted():
    class Substitute:
        def __getattr__(self, name):
            pytest.fail("substitute mapping owner consulted: " + name)

    args = {
        name: None
        for name in inspect.signature(api().prepare_observed_supplier_change).parameters
    }
    args["history"] = Substitute()
    with pytest.raises(
        api().SupplierObservationMappingError, match="owning Core history"
    ):
        api().prepare_observed_supplier_change(**args)


def test_mapping_stage_cannot_import_effectors_or_admit_a_change():
    import ast
    from hashlib import sha256
    from research.semantic_reentry_external_design import supplier_components

    module = api()
    content = Path(module.__file__).read_bytes()
    assert (
        module.ADAPTER_IDENTITY
        == "sha256:"
        + sha256(
            module.ADAPTER_ID.encode()
            + b"\0"
            + Path(supplier_components.__file__).read_bytes()
            + b"\0"
            + content
        ).hexdigest()
    )
    root = Path(__file__).resolve().parents[2]
    assert Path(core.__file__).resolve().is_relative_to(root / "src/malleus")
    assert Path(module.__file__).resolve().parent == Path(__file__).resolve().parent
    gate = json.loads(
        (Path(__file__).parent / "supplier-observed-source-gate.json").read_bytes()
    )
    assert str(Path(__file__).resolve().relative_to(root)) in gate["tests"]
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert all((root / path).is_file() for path in gate["tests"])
    for node in ast.walk(ast.parse(content)):
        if isinstance(node, ast.ImportFrom):
            assert node.module is not None
            assert not node.module.startswith(("malleus._", "tests."))
            assert not any(p.startswith("test_") for p in node.module.split("."))
            assert not any(
                p in node.module for p in ("supplier_execution", "supplier_observation")
            )
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in {
                "admit_structural_change",
                "add_node",
                "add_edge",
                "apply_change_set",
                "dispatch_and_execute_supplier",
                "observe_supplier_execution",
            }
        elif isinstance(node, ast.ExceptHandler):
            assert node.type is not None
            assert not any(isinstance(n, ast.Attribute) for n in ast.walk(node.type))

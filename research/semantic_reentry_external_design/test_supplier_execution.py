"""Actual controlled source attempts, never observation or accepted correction."""

from importlib import import_module
import inspect
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from malleus.assent import make_record
from malleus.source import source_artifact_fields
from research.semantic_reentry_external_design import (
    test_supplier_authorization as authority,
)
from research.semantic_reentry_external_design import test_supplier_proposals as entry
from research.semantic_reentry_external_design.test_supplier_proposals import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_execution"
DISPATCH_TIME = "2026-09-08T06:10:00Z"
END_TIME = "2026-09-08T06:20:00Z"
IMPLEMENTATION = "source:supplier:executor-implementation"


def api():
    return import_module(MODULE)


def test_execution_contract_api_has_no_required_input_defaults():
    function = api().dispatch_and_execute_supplier
    assert all(
        p.default is inspect.Parameter.empty
        for p in inspect.signature(function).parameters.values()
    )
    assert type(api().IMPLEMENTATION_BYTES) is bytes


@pytest.fixture(scope="module")
def execution_prefix(tmp_path_factory, compilation, action_compilation):
    module = api()
    initial = authority.supplier_source_prefix.__wrapped__(
        tmp_path_factory, compilation, action_compilation
    )
    accepted = authority.accepted_prefix.__wrapped__(tmp_path_factory, initial)
    args = authority.preparation.__wrapped__(
        tmp_path_factory.mktemp("supplier-execution-authority"), accepted
    )
    owner = args["history"]
    authority.api().prepare_supplier_authority(**args)
    for ordinal in range(2):
        authority.api().record_supplier_authority_check(
            **authority.check_arguments(args, ordinal)
        )
    assessed = owner.path.read_bytes()
    authority.api().decide_supplier_authorization(**authority.decision_arguments(args))
    content = module.IMPLEMENTATION_BYTES
    value = make_record(
        "SourceArtifact",
        id=IMPLEMENTATION,
        event_id="event:" + IMPLEMENTATION,
        generated_at=authority.TIME,
        actor_id="actor:supplier:executor-registrar",
        role="registrar",
        source_record_ids=[],
        artifact_kind="SOURCE",
        artifact_version="research-v1",
        **source_artifact_fields(
            artifact_id=IMPLEMENTATION,
            artifact_version="research-v1",
            source_bytes=content,
            media_type="text/x-python",
            locator="urn:retained:" + IMPLEMENTATION,
        ),
    )
    event = entry._draft("SourceArtifact", value, content=content)
    event["retained"]["source"]["media_type"] = value["source_media_type"]
    owner.append_protocol_events(
        transaction="source",
        events=(event,),
        **entry.position(owner),
    )
    return owner.path, assessed, args["current_context_id"]


@pytest.fixture
def execution_inputs(tmp_path, execution_prefix):
    prefix, _, current = execution_prefix
    path = tmp_path / "history.jsonl"
    shutil.copyfile(prefix, path)
    owner = core.KnowledgeChangeHistory.reopen(path)
    source = tmp_path / "supplier.jsonl"
    source.write_bytes(
        (entry.ingress.FIXTURE / "input/supplier-before.jsonl").read_bytes()
    )
    return dict(
        history=owner,
        **entry.position(owner),
        original_context_id=entry.CONTEXT,
        current_context_id=current,
        action_id=entry.ACTION,
        authorization_id="authorization:supplier:1",
        executor_implementation_id=IMPLEMENTATION,
        executor_id=authority.EXECUTOR,
        dispatcher_id="actor:supplier:dispatcher",
        dispatch_id="dispatch:supplier:1",
        execution_id="execution:supplier:1",
        dispatched_at=DISPATCH_TIME,
        execution_started_at=DISPATCH_TIME,
        execution_ended_at=END_TIME,
        source_path=source,
        logical_source_id=entry.ingress.SOURCE_ID,
    )


@pytest.mark.parametrize(
    "fault",
    ["none", "before-write", "after-write", "unchanged-success", "stale-source"],
)
def test_controlled_attempt_and_receipt_never_change_accepted_knowledge(
    execution_inputs, monkeypatch, tmp_path, fault
):
    args = execution_inputs
    owner, source = args["history"], args["source_path"]
    frame = authority.domain_frame(owner.replay())
    original_source = source.read_bytes()
    writer = api()._write_source
    attempts = []

    def controlled(stream, content):
        attempts.append(content)
        if fault == "before-write":
            raise OSError("controlled failure before write")
        if fault != "unchanged-success":
            writer(stream, content)
        if fault == "after-write":
            raise OSError("controlled failure after write")

    monkeypatch.setattr(api(), "_write_source", controlled)
    if fault == "stale-source":
        row = json.loads(original_source)
        row["quantity"] = 3
        source.write_bytes(entry.ingress.canonical(row) + b"\n")
    before_source = source.read_bytes()
    after = api().dispatch_and_execute_supplier(**args)
    assert authority.domain_frame(after) == frame
    records = after.protocol_replay.data["records"]
    execution = records[args["execution_id"]]["record"]
    status = {
        "none": "SUCCEEDED",
        "before-write": "FAILED",
        "after-write": "FAILED",
        "unchanged-success": "SUCCEEDED",
        "stale-source": "ABORTED",
    }[fault]
    assert execution["execution_status"] == status
    assert json.loads(after.retained_bytes(execution["id"]))["status"] == status
    if fault in {"none", "after-write"}:
        assert (
            source.read_bytes()
            == (entry.ingress.FIXTURE / "oracle/supplier-after.jsonl").read_bytes()
        )
    else:
        assert source.read_bytes() == before_source
    assert len(attempts) == (0 if fault == "stale-source" else 1)
    assert not any(r["record_type"] == "OutcomeObservation" for r in records.values())
    assert after.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1

    def forbidden(*args, **kwargs):
        pytest.fail("replay or repeated dispatch invoked the file attempt")

    monkeypatch.setattr(api(), "_attempt", forbidden)
    repeated = dict(args, **entry.position(owner))
    before = owner.path.read_bytes(), source.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError):
        api().dispatch_and_execute_supplier(**repeated)
    assert (
        owner.path.read_bytes(),
        source.read_bytes(),
        owner.replay().receipt,
    ) == before
    isolated = tmp_path / "reopen"
    isolated.mkdir()
    replay_path = isolated / "history.jsonl"
    shutil.copyfile(owner.path, replay_path)
    assert (
        core.KnowledgeChangeHistory.reopen(replay_path).replay().receipt
        == after.receipt
    )
    assert [p.name for p in isolated.iterdir()] == ["history.jsonl"]


@pytest.mark.parametrize(
    "fault",
    [
        "stale",
        "actor",
        "expiry",
        "implementation",
        "source-id",
        "time",
        "duplicate-id",
        "relative-path",
        "symlink",
    ],
)
def test_ineligible_dispatch_never_attempts_source(
    execution_inputs, monkeypatch, fault, tmp_path
):
    args = execution_inputs
    owner, source = args["history"], args["source_path"]
    if fault == "stale":
        args["expected_count"] -= 1
    elif fault == "actor":
        args["executor_id"] = "actor:supplier:other"
    elif fault == "expiry":
        args.update(
            dispatched_at="2026-09-08T07:00:00Z",
            execution_started_at="2026-09-08T07:00:00Z",
            execution_ended_at="2026-09-08T07:01:00Z",
        )
    elif fault == "implementation":
        args["executor_implementation_id"] = entry.ROLE_IDS["goal"]
    elif fault == "source-id":
        args["logical_source_id"] = "source:other"
    elif fault == "time":
        args["execution_ended_at"] = args["execution_started_at"]
    elif fault == "duplicate-id":
        args["execution_id"] = args["dispatch_id"]
    elif fault == "relative-path":
        args["source_path"] = Path("supplier.jsonl")
    else:
        link = tmp_path / "supplier-link.jsonl"
        link.symlink_to(source)
        args["source_path"] = link

    def forbidden(*args, **kwargs):
        pytest.fail("ineligible dispatch invoked the file attempt")

    monkeypatch.setattr(api(), "_attempt", forbidden)
    before = owner.path.read_bytes(), source.read_bytes(), owner.replay().receipt
    with pytest.raises(ValueError):
        api().dispatch_and_execute_supplier(**args)
    assert (
        owner.path.read_bytes(),
        source.read_bytes(),
        owner.replay().receipt,
    ) == before

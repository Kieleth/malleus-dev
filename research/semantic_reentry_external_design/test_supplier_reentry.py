"""Pure pinned supplier candidate, then the existing real lifecycle, never a stub."""

from importlib import import_module
import inspect
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as core
from malleus.assent import make_record
from malleus.source import source_artifact_fields
from research.semantic_reentry_external_design import test_supplier_proposals as entry
from research.semantic_reentry_external_design import (
    supplier_components,
    supplier_execution,
    supplier_observation,
    supplier_observed_source,
)
from research.semantic_reentry_external_design.accepted_read_view import (
    freeze_accepted_replay,
)
from research.semantic_reentry_external_design.test_supplier_proposals import (
    compile_supplier_action as compile_supplier_action,
)


MODULE = "research.semantic_reentry_external_design.supplier_reentry"
RULE = "source:supplier:reentry-rule"
IMPLEMENTATION = "source:supplier:reentry-implementation"
GOAL = "source:supplier:bound-goal"
MAPPER = "source:supplier:observed-mapper-implementation"
EXECUTOR = "source:supplier:executor-implementation"
OBSERVER = "outcome-contract:supplier:source"


def api():
    return import_module(MODULE)


def test_reentry_api_has_explicit_required_inputs():
    for function in (
        api().bind_supplier_reentry,
        api().SupplierReentrySynthesizer.synthesize,
        api().SupplierSourceModel.predict,
        api().SupplierActionStrategy.payload,
    ):
        assert all(
            p.default is inspect.Parameter.empty
            for p in inspect.signature(function).parameters.values()
        )
    assert type(api().IMPLEMENTATION_BYTES) is bytes


def retain_source(owner, identifier, content, dependencies):
    record = make_record(
        "SourceArtifact",
        id=identifier,
        event_id="event:" + identifier,
        generated_at=entry.TIME,
        actor_id="actor:supplier:reentry-registrar",
        role="registrar",
        source_record_ids=dependencies,
        artifact_kind="SOURCE",
        artifact_version="research-v1",
        **source_artifact_fields(
            artifact_id=identifier,
            artifact_version="research-v1",
            source_bytes=content,
            media_type="application/octet-stream",
            locator="urn:retained:" + identifier,
        ),
    )
    event = entry._draft("SourceArtifact", record, content=content)
    event["retained"]["source"]["media_type"] = record["source_media_type"]
    return owner.append_protocol_events(
        transaction="source", events=(event,), **entry.position(owner)
    )


def rule_value(initialization_id, case):
    return dict(
        schema="malleus.reentry.supplier-rule/research-v1",
        initialization_id=initialization_id,
        goal_kind="GoalPredicate",
        output_type="SupplierOrderAmendment",
        logical_source_id=entry.ingress.SOURCE_ID,
        operator=case["operator"],
        ambiguity="REFUSE_IF_NOT_UNIQUE",
        candidate_budget=1,
        dispatch_attempt_budget=1,
        automatic_retry=False,
        stopping="INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS",
        implementations={
            name: dict(
                source_id=IMPLEMENTATION,
                bytes_sha256=api().IMPLEMENTATION_IDENTITY,
                entrypoint=engine.entrypoint,
            )
            for name, engine in (
                ("synthesizer", api().SupplierReentrySynthesizer()),
                ("model", api().SupplierSourceModel()),
                ("update_strategy", api().SupplierActionStrategy()),
            )
        },
        executor=dict(
            source_id=EXECUTOR, bytes_sha256=supplier_execution.IMPLEMENTATION_IDENTITY
        ),
        observer=dict(
            outcome_contract_id=OBSERVER,
            observer_implementation_hash=supplier_observation.IMPLEMENTATION_IDENTITY,
        ),
        observed_mapper=dict(
            source_id=MAPPER,
            bytes_sha256=supplier_observed_source.ADAPTER_IDENTITY,
            adapter_id=supplier_observed_source.ADAPTER_ID,
        ),
        output=dict(
            proposer_id=entry.ACTOR,
            generated_at=entry.TIME,
            proposal_key="supplier:synthesized:proposal",
        ),
    )


@pytest.fixture(scope="module")
def reentry_prefix(tmp_path_factory, compilation, action_compilation):
    api()
    prefix, initialization_id, case = entry.input_prefix.__wrapped__(
        tmp_path_factory, compilation, action_compilation
    )
    path = tmp_path_factory.mktemp("supplier-reentry-inputs") / "history.jsonl"
    shutil.copyfile(prefix, path)
    owner = core.KnowledgeChangeHistory.reopen(path)
    retain_source(owner, IMPLEMENTATION, api().IMPLEMENTATION_BYTES, [])
    retain_source(owner, EXECUTOR, supplier_execution.IMPLEMENTATION_BYTES, [])
    mapper_bytes = (
        supplier_observed_source.ADAPTER_ID.encode()
        + b"\0"
        + Path(supplier_components.__file__).read_bytes()
        + b"\0"
        + Path(supplier_observed_source.__file__).read_bytes()
    )
    retain_source(owner, MAPPER, mapper_bytes, [])
    supplier_observation.register_supplier_observer(
        history=owner,
        **entry.position(owner),
        implementation_source_id="source:supplier:observer-implementation",
        outcome_contract_id=OBSERVER,
        actor_id="actor:supplier:observer-registrar",
        generated_at=entry.TIME,
        artifact_version="research-v1",
    )
    rule = rule_value(initialization_id, case)
    retain_source(
        owner,
        RULE,
        entry.ingress.canonical(rule),
        [IMPLEMENTATION, EXECUTOR, MAPPER, OBSERVER],
    )
    retain_source(owner, GOAL, entry.ingress.canonical(case["goal"]), [RULE])
    return path, initialization_id, case


@pytest.fixture
def reentry_inputs(tmp_path, reentry_prefix):
    path, initialization_id, case = reentry_prefix
    target = tmp_path / "history.jsonl"
    shutil.copyfile(path, target)
    owner = core.KnowledgeChangeHistory.reopen(target)
    view = freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )
    source_ids = dict(entry.ROLE_IDS, goal=GOAL)
    original = entry.api().original_supplier_context(
        view=view,
        initialization_id=initialization_id,
        source_ids=source_ids,
        context_id=entry.CONTEXT,
        action_id=entry.ACTION,
        proposal_id=entry.PROPOSAL,
        episode_key=case["episode"]["id"],
    )
    contract = api().bind_supplier_reentry(
        view=view, original_context_bytes=original, rule_source_id=RULE
    )
    return owner, view, original, contract


def synthesize(contract, view):
    return (
        api()
        .SupplierReentrySynthesizer()
        .synthesize(
            contract,
            view,
            model=api().SupplierSourceModel(),
            update_strategy=api().SupplierActionStrategy(),
        )
    )


def test_real_pinned_candidate_round_trip_and_submission(reentry_inputs):
    owner, view, original, contract = reentry_inputs
    before = owner.path.read_bytes(), owner.replay().graph.export_records()
    parsed = api().SupplierReentryContract.from_bytes(contract.canonical_bytes)
    assert parsed == contract
    result = synthesize(contract, view)
    assert result.status == "CANDIDATES" and len(result.candidates) == 1
    assert result == synthesize(contract, view)
    assert result.finding.current_quantity == 1 and result.finding.shortfall == 1
    assert (
        result.model_prediction
        == (entry.ingress.FIXTURE / "oracle/supplier-after.jsonl").read_bytes()
    )
    action = json.loads(result.candidates[0])
    assert action["expected_quantity"] == 1 and action["requested_quantity"] == 2
    assert action["new_source_occurrence_id"] == "reentry-amendment-1"
    assert (owner.path.read_bytes(), owner.replay().graph.export_records()) == before
    after = entry.api().submit_supplier_proposal(
        history=owner,
        original_context_bytes=original,
        action_bytes=result.candidates[0],
        proposal_key="supplier:synthesized:proposal",
        context_actor_id=entry.ACTOR,
        artifact_version="research-v1",
        **entry.position(owner),
    )
    assert after.protocol_replay.data["records"][entry.ACTION]["record"] == action
    assert after.graph.export_records() == before[1]


def test_pure_synthesis_has_no_io_or_owner_capability(reentry_inputs, monkeypatch):
    import builtins
    import os
    import socket
    import subprocess

    _, view, _, contract = reentry_inputs

    def forbidden(*args, **kwargs):
        pytest.fail("pure re-entry crossed an I/O boundary")

    for target, name in (
        (builtins, "open"),
        (os, "open"),
        (Path, "open"),
        (socket, "socket"),
        (subprocess, "Popen"),
    ):
        monkeypatch.setattr(target, name, forbidden)
    assert synthesize(contract, view).status == "CANDIDATES"
    for name in ("graph", "history", "path", "replay", "admit"):
        assert not hasattr(contract, name) and not hasattr(view, name)


def test_stale_contract_refuses_before_model_invocation(reentry_inputs, monkeypatch):
    owner, _, _, contract = reentry_inputs
    owner.append_anchors(
        anchors=(
            core.structural_evidence_anchor(
                record_id="evidence:supplier:after-binding",
                content=b"explicit later evidence",
                media_type="text/plain",
            ),
        ),
        transaction_time=entry.TIME,
        actor_id=entry.ACTOR,
    )
    fresh = freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )

    def forbidden(*args, **kwargs):
        pytest.fail("stale contract invoked the source model")

    monkeypatch.setattr(api().SupplierSourceModel, "predict", forbidden)
    before = owner.path.read_bytes()
    result = synthesize(contract, fresh)
    assert result.status == "REFUSED" and result.reason == "STALE_BASE"
    assert not result.candidates and owner.path.read_bytes() == before

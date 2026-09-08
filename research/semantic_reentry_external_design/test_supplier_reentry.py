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
    test_supplier_authorization as authority,
)
from research.semantic_reentry_external_design import (
    test_supplier_observation as observe,
)
from research.semantic_reentry_external_design import (
    test_supplier_observed_source as population,
)
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
        operator=json.loads(entry.ingress.canonical(case["operator"])),
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


def fresh_evaluation(owner, original):
    before = owner.path.read_bytes()
    view = freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )
    contract = api().bind_supplier_reentry(
        view=view, original_context_bytes=original, rule_source_id=RULE
    )
    result = synthesize(contract, view)
    assert owner.path.read_bytes() == before
    return result


def test_rule_variants_do_not_mutate_frozen_case():
    case = json.loads((entry.ingress.FIXTURE / "case.json").read_bytes())
    before = entry.ingress.canonical(case)
    value = rule_value("source:supplier:initialization", case)
    value["operator"]["kind"] = "DIRECT_GRAPH_WRITE"
    assert entry.ingress.canonical(case) == before


def test_model_prediction_must_meet_goal_and_frame(reentry_inputs, monkeypatch):
    owner, view, _, contract = reentry_inputs

    def wrong_prediction(self, **kwargs):
        row = json.loads(kwargs["before_bytes"])
        row["quantity"] = 3
        row["event_id"] = "reentry-amendment-1"
        return entry.ingress.canonical(row) + b"\n"

    monkeypatch.setattr(api().SupplierSourceModel, "predict", wrong_prediction)
    before = owner.path.read_bytes(), authority.domain_frame(owner.replay())
    result = synthesize(contract, view)
    assert result.status == "REFUSED" and result.reason == "UNSUPPORTED_CHANGE"
    assert not result.candidates
    assert (owner.path.read_bytes(), authority.domain_frame(owner.replay())) == before


def alternate_accepted_source(owner, case, *, quantity, supersede):
    """Explicit conformance source through real population, never an observation."""
    source_id = "source:supplier:initial-law"
    occurrence = "initial-law"
    record_id = "supplier-order-state:B:" + occurrence
    mapping = dict(
        case["mapping"],
        initial_record_id=record_id,
        supersedes_record_id=record_id,
        replacement_record_id="supplier-order-state:B:unused-law-replacement",
    )
    content = (
        entry.ingress.canonical(
            dict(
                event_id=occurrence,
                supplier_order_id="B",
                product_code="Y",
                quantity=quantity,
            )
        )
        + b"\n"
    )
    evidence = entry.ingress.canonical(
        dict(kind="CONFORMANCE_SOURCE_NOT_ACTION_OBSERVATION", mapping=mapping)
    )
    owner.append_anchors(
        anchors=(
            *core.structural_source_anchors(
                source_id=source_id,
                artifact_id="artifact:supplier:initial-law",
                content=content,
                media_type="application/x-ndjson",
            ),
            core.structural_evidence_anchor(
                record_id="evidence:supplier:initial-law",
                content=evidence,
                media_type="application/json",
            ),
        ),
        transaction_time=entry.TIME,
        actor_id=entry.ACTOR,
    )
    fragment = json.loads(
        supplier_components.map_initial_source(
            content,
            source_sha256=entry.ingress.digest(content),
            mapping=mapping,
            source_id=source_id,
        )
    )
    if supersede:
        fragment["supersessions"] = [
            dict(
                record_id=record_id,
                supersedes_record_id=case["mapping"]["initial_record_id"],
            )
        ]
    profile = core.STATE_VERSION_PROFILE
    replay = owner.replay()
    plan = dict(
        grammar="malleus.population-plan/private-v0",
        plan_id="plan:supplier:initial-law",
        contract_identity=replay.partial_contract.identity,
        history_profile=dict(profile_id=profile.profile_id, sha256=profile.identity),
        adapter=dict(adapter_id="conformance:initial-goal-law", version="research-v1"),
        evidence=[
            dict(
                evidence_id="evidence:supplier:initial-law",
                sha256=entry.ingress.digest(evidence),
            )
        ],
        gaps=[],
        **fragment,
    )
    compiled = core.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=core.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    prepared = core.prepare_population_change(
        history=owner,
        plan=plan,
        profile=json.loads(profile.canonical_bytes),
        retention_events=core.population_retention_events(
            history=owner, compilation=compiled, profile=profile
        ),
        transaction_time=entry.TIME,
        actor_id=entry.ACTOR,
    )
    core.admit_structural_change(
        history=owner,
        preparation=prepared,
        transaction_time=entry.TIME,
        actor_id=entry.ACTOR,
    )
    return source_id, content, mapping


@pytest.mark.parametrize(
    "quantity,supersede,status,reason",
    [
        (2, True, "SATISFIED", "INITIAL_SATISFIED"),
        (3, True, "REFUSED", "UNREALIZABLE"),
        (2, False, "REFUSED", "AMBIGUOUS"),
    ],
)
def test_initial_goal_and_ambiguity_use_real_accepted_source(
    reentry_inputs, reentry_prefix, monkeypatch, quantity, supersede, status, reason
):
    owner = reentry_inputs[0]
    _, initialization_id, case = reentry_prefix
    source_id, content, mapping = alternate_accepted_source(
        owner, case, quantity=quantity, supersede=supersede
    )
    rule_id, goal_id = RULE + ":initial-law", GOAL + ":initial-law"
    mapping_id, prestate_id = (
        "source:supplier:law-mapping",
        "source:supplier:law-prestate",
    )
    rule = rule_value(initialization_id, case)
    rule["logical_source_id"] = source_id
    retain_source(owner, mapping_id, entry.ingress.canonical(mapping), [])
    retain_source(owner, prestate_id, content, [])
    retain_source(
        owner,
        rule_id,
        entry.ingress.canonical(rule),
        [IMPLEMENTATION, EXECUTOR, MAPPER, OBSERVER],
    )
    retain_source(owner, goal_id, entry.ingress.canonical(case["goal"]), [rule_id])
    view = freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )
    original = entry.api().original_supplier_context(
        view=view,
        initialization_id=initialization_id,
        source_ids=dict(
            goal=goal_id,
            mapping=mapping_id,
            preservation=entry.ROLE_IDS["preservation"],
            pre_state_source=prestate_id,
        ),
        context_id=entry.CONTEXT,
        action_id=entry.ACTION,
        proposal_id=entry.PROPOSAL,
        episode_key=case["episode"]["id"],
    )
    contract = api().bind_supplier_reentry(
        view=view, original_context_bytes=original, rule_source_id=rule_id
    )

    def forbidden(*args, **kwargs):
        pytest.fail("satisfied, unsupported or ambiguous state invoked the model")

    monkeypatch.setattr(api().SupplierSourceModel, "predict", forbidden)
    before = owner.path.read_bytes(), authority.domain_frame(owner.replay())
    result = synthesize(contract, view)
    assert (result.status, result.reason) == (status, reason)
    assert not result.candidates and result.model_prediction is None
    assert (owner.path.read_bytes(), authority.domain_frame(owner.replay())) == before


@pytest.mark.parametrize("role", ["model", "update_strategy"])
def test_unselected_engine_refuses_before_invocation(reentry_inputs, role):
    owner, view, _, contract = reentry_inputs

    class Unselected:
        implementation_identity = "sha256:" + "0" * 64
        entrypoint = "unselected"

        def predict(self, **kwargs):
            pytest.fail("unselected model ran")

        def payload(self, **kwargs):
            pytest.fail("unselected strategy ran")

    engines = dict(
        model=api().SupplierSourceModel(),
        update_strategy=api().SupplierActionStrategy(),
    )
    engines[role] = Unselected()
    before = owner.path.read_bytes()
    result = api().SupplierReentrySynthesizer().synthesize(contract, view, **engines)
    assert result.status == "REFUSED" and result.reason == "UNSUPPORTED_IMPLEMENTATION"
    assert not result.candidates and owner.path.read_bytes() == before


@pytest.mark.parametrize("field", ["current", "rule", "original_context", "schema"])
def test_contract_parser_never_defaults_missing_closure(reentry_inputs, field):
    contract = reentry_inputs[3]
    value = json.loads(contract.canonical_bytes)
    del value[field]
    with pytest.raises(api().ReentryRefusal) as error:
        api().SupplierReentryContract.from_bytes(entry.ingress.canonical(value))
    assert error.value.reason == "MALFORMED_INPUT"


@pytest.mark.parametrize(
    "fault,reason",
    [
        ("operation", "UNSUPPORTED"),
        ("quantity", "UNSUPPORTED"),
        ("ambiguity", "MALFORMED_INPUT"),
        ("budget", "MALFORMED_INPUT"),
        ("boolean-budget", "UNSUPPORTED"),
        ("unknown", "MALFORMED_INPUT"),
    ],
)
def test_retained_unsupported_rule_is_not_interpreted_by_defaults(
    reentry_inputs, reentry_prefix, fault, reason
):
    owner, _, _, _ = reentry_inputs
    _, initialization_id, case = reentry_prefix
    value = rule_value(initialization_id, case)
    if fault == "operation":
        value["operator"]["kind"] = "DIRECT_GRAPH_WRITE"
    elif fault == "quantity":
        value["operator"]["requested_quantity"] = 3
    elif fault in {"ambiguity", "budget"}:
        del value["ambiguity" if fault == "ambiguity" else "candidate_budget"]
    elif fault == "boolean-budget":
        value["candidate_budget"] = True
    else:
        value["unrecognized_required_semantics"] = True
    identifier = RULE + ":invalid"
    retain_source(
        owner,
        identifier,
        entry.ingress.canonical(value),
        [IMPLEMENTATION, EXECUTOR, MAPPER, OBSERVER],
    )
    view = freeze_accepted_replay(
        replay=owner.replay(), context=owner.composition_context()
    )
    before = owner.path.read_bytes()
    with pytest.raises(api().ReentryRefusal) as error:
        api().bind_supplier_reentry(
            view=view,
            original_context_bytes=reentry_inputs[2],
            rule_source_id=identifier,
        )
    assert error.value.reason == reason
    assert owner.path.read_bytes() == before


@pytest.fixture(scope="module")
def synthesized_authorized_prefix(tmp_path_factory, reentry_prefix):
    owner, view, original, contract = reentry_inputs.__wrapped__(
        tmp_path_factory.mktemp("supplier-synthesized-lifecycle"), reentry_prefix
    )
    frame = authority.domain_frame(owner.replay())
    result = synthesize(contract, view)
    assert result.status == "CANDIDATES" and len(result.candidates) == 1
    entry.api().submit_supplier_proposal(
        history=owner,
        original_context_bytes=original,
        action_bytes=result.candidates[0],
        proposal_key="supplier:synthesized:proposal",
        context_actor_id=entry.ACTOR,
        artifact_version="research-v1",
        **entry.position(owner),
    )
    assert fresh_evaluation(owner, original).status == "PENDING"
    for ordinal in range(2):
        entry.api().record_supplier_type_check(**entry.check_arguments(owner, ordinal))
    entry.api().decide_supplier_proposal(**entry.decision_arguments(owner))
    assert fresh_evaluation(owner, original).status == "PENDING"
    # Same real direct grant semantics, with this episode's actual bound goal scope.
    from malleus.ledger import content_digest

    fields = dict(
        grantor_actor_id="actor:supplier:grantor",
        grantee_actor_id=authority.EXECUTOR,
        permitted_action_types=["AMEND_SUPPLIER_ORDER"],
        scope_record_id=GOAL,
        may_subdelegate=False,
        grant_valid_from=entry.TIME,
        grant_valid_to="2026-09-08T08:00:00Z",
    )
    grant = make_record(
        "AuthorityGrant",
        id="grant:supplier:direct",
        event_id="event:grant:supplier:direct",
        generated_at=entry.TIME,
        actor_id=fields["grantor_actor_id"],
        role="registrar",
        source_record_ids=[GOAL],
        artifact_kind="AUTHORITY_GRANT",
        artifact_version="research-v1",
        artifact_hash=content_digest(fields),
        **fields,
    )
    args = dict(
        history=owner,
        original_context_id=entry.CONTEXT,
        grant_bytes=entry.ingress.canonical(grant),
        scope_association_id="source:supplier:scope-association",
        requested_interval_id="source:supplier:requested-interval",
        current_context_id="source:supplier:current-context",
        requested_interval_bytes=entry.ingress.canonical(
            dict(start=entry.TIME, end="2026-09-08T07:00:00Z")
        ),
        actor_id="actor:supplier:authority-registrar",
        generated_at=entry.TIME,
        artifact_version="research-v1",
        **entry.position(owner),
    )
    authority.api().prepare_supplier_authority(**args)
    for ordinal in range(2):
        authority.api().record_supplier_authority_check(
            **authority.check_arguments(args, ordinal)
        )
    authority.api().decide_supplier_authorization(**authority.decision_arguments(args))
    assert authority.domain_frame(owner.replay()) == frame
    assert fresh_evaluation(owner, original).status == "PENDING"
    return owner.path, original, result.candidates[0]


@pytest.mark.parametrize("fault", ["none", "after-write", "unchanged-success"])
def test_synthesized_action_observed_kcs_and_fresh_quiescence(
    synthesized_authorized_prefix, tmp_path, monkeypatch, fault
):
    prefix, original, action_bytes = synthesized_authorized_prefix
    path = tmp_path / "history.jsonl"
    shutil.copyfile(prefix, path)
    owner = core.KnowledgeChangeHistory.reopen(path)
    before = owner.replay()
    frame = authority.domain_frame(before)
    source = tmp_path / "supplier.jsonl"
    source.write_bytes(before.retained_bytes(entry.ingress.SOURCE_ID))
    attempts = []
    actual_write = supplier_execution._write_source

    def controlled(stream, content):
        attempts.append(content)
        if fault != "unchanged-success":
            actual_write(stream, content)
        if fault == "after-write":
            raise OSError("controlled failure after actual write")

    monkeypatch.setattr(supplier_execution, "_write_source", controlled)
    supplier_execution.dispatch_and_execute_supplier(
        history=owner,
        **entry.position(owner),
        original_context_id=entry.CONTEXT,
        current_context_id="source:supplier:current-context",
        action_id=entry.ACTION,
        authorization_id="authorization:supplier:1",
        executor_implementation_id=EXECUTOR,
        executor_id=authority.EXECUTOR,
        dispatcher_id="actor:supplier:dispatcher",
        dispatch_id="dispatch:supplier:1",
        execution_id="execution:supplier:1",
        dispatched_at="2026-09-08T06:10:00Z",
        execution_started_at="2026-09-08T06:10:00Z",
        execution_ended_at="2026-09-08T06:20:00Z",
        source_path=source,
        logical_source_id=entry.ingress.SOURCE_ID,
    )
    assert len(attempts) == 1
    assert authority.domain_frame(owner.replay()) == frame
    assert fresh_evaluation(owner, original).status == "PENDING"
    supplier_observation.observe_supplier_execution(
        **observe.observation_arguments(owner, source)
    )
    captured = owner.replay()
    assert authority.domain_frame(captured) == frame
    actual = captured.retained_bytes("source:supplier:captured:1")
    assert actual == source.read_bytes()
    assert fresh_evaluation(owner, original).status != "SATISFIED"
    case = json.loads((entry.ingress.FIXTURE / "case.json").read_bytes())
    prepared = supplier_observed_source.prepare_observed_supplier_change(
        history=owner,
        **entry.position(owner),
        original_context_id=entry.CONTEXT,
        observation_id="observation:supplier:1",
        outcome_contract_id=OBSERVER,
        observer_implementation_identity=supplier_observation.IMPLEMENTATION_IDENTITY,
        operator_bytes=entry.ingress.canonical(case["operator"]),
        source_id=population.SOURCE,
        source_artifact_id="artifact:supplier:observed-population:1",
        evidence_id=population.EVIDENCE,
        plan_id="plan:supplier:observed-population:1",
        history_profile=core.STATE_VERSION_PROFILE,
        transaction_time=population.TIME,
        actor_id=population.ACTOR,
    )
    assert authority.domain_frame(owner.replay()) == frame
    if fault == "unchanged-success":
        assert prepared is None
        stopped = fresh_evaluation(owner, original)
        assert stopped.status == "REFUSED" and stopped.reason == "EPISODE_TERMINAL"
        assert not stopped.candidates
        assert authority.domain_frame(owner.replay()) == frame
        return
    assert type(prepared.change_set) is core.KnowledgeChangeSet
    assert fresh_evaluation(owner, original).status == "PENDING"
    # Even exact retained candidate bytes are not an accepted observed correction.
    retained_path = tmp_path / "retained-only.jsonl"
    shutil.copyfile(owner.path, retained_path)
    retained_owner = core.KnowledgeChangeHistory.reopen(retained_path)
    retained_owner.append_anchors(
        anchors=(
            core.structural_evidence_anchor(
                record_id="evidence:supplier:unaccepted-candidate",
                content=prepared.change_set.canonical_bytes,
                media_type="application/json",
            ),
        ),
        transaction_time=population.TIME,
        actor_id=population.ACTOR,
    )
    assert fresh_evaluation(retained_owner, original).status == "PENDING"
    with pytest.raises(core.KnowledgeChangeRefusal):
        core.admit_structural_change(
            history=retained_owner,
            preparation=prepared,
            transaction_time=population.TIME,
            actor_id=population.ACTOR,
        )
    assert authority.domain_frame(retained_owner.replay()) == frame
    # The untouched prepared prefix can admit its exact candidate. No rebasing.
    final = core.admit_structural_change(
        history=owner,
        preparation=prepared,
        transaction_time=population.TIME,
        actor_id=population.ACTOR,
    )
    assert final.graph.get_node(population.REPLACEMENT)["ordered_quantity"] == 2
    assert len(final.change_sets) == len(before.change_sets) + 1
    for family, members in before.graph.export_records().items():
        assert [
            r
            for r in final.graph.export_records()[family]
            if r["id"] != population.REPLACEMENT
        ] == [r for r in members if r["id"] != "supplier-order-state:B:e4"]
    for identifier, historical in before.record_history.items():
        if identifier != "supplier-order-state:B:e4":
            assert final.record_history[identifier] == historical
    assert (
        final.record_history["supplier-order-state:B:e4"].superseded_by
        == population.REPLACEMENT
    )
    assert (
        final.record_history[population.REPLACEMENT].supersedes_record_id
        == "supplier-order-state:B:e4"
    )
    trace = core.trace_population_record(final, population.REPLACEMENT)
    assert trace.sources[0].content == actual
    assert (
        json.loads(
            next(
                e.content for e in trace.evidence if e.record_id == population.EVIDENCE
            )
        )["observation"]["id"]
        == "observation:supplier:1"
    )
    status = "FAILED" if fault == "after-write" else "SUCCEEDED"
    assert (
        final.protocol_replay.data["records"]["execution:supplier:1"]["record"][
            "execution_status"
        ]
        == status
    )
    assert (
        entry.ingress.canonical(
            final.protocol_replay.data["records"][entry.ACTION]["record"]
        )
        == action_bytes
    )
    # Reopen with only the ledger in another directory, not the mutable source file.
    reopen_directory = tmp_path / "jsonl-only"
    reopen_directory.mkdir()
    reopened_path = reopen_directory / "history.jsonl"
    shutil.copyfile(owner.path, reopened_path)

    def forbidden(*args, **kwargs):
        pytest.fail("reopen or satisfied evaluation invoked an effect/model")

    monkeypatch.setattr(supplier_execution, "_attempt", forbidden)
    monkeypatch.setattr(api().SupplierSourceModel, "predict", forbidden)
    reopened = core.KnowledgeChangeHistory.reopen(reopened_path)
    reopened_replay = reopened.replay()
    assert reopened_replay.receipt == final.receipt
    assert authority.domain_frame(reopened_replay) == authority.domain_frame(final)
    assert reopened_replay.protocol_replay == final.protocol_replay
    assert [p.name for p in reopen_directory.iterdir()] == ["history.jsonl"]
    bytes_before = reopened_path.read_bytes(), source.read_bytes()
    stopped = fresh_evaluation(reopened, original)
    assert stopped.status == "SATISFIED" and stopped.reason == "LINKED_OBSERVED_KCS"
    assert stopped.finding.current_quantity == 2 and stopped.finding.shortfall == 0
    assert stopped.candidates == () and stopped.model_prediction is None
    assert fresh_evaluation(reopened, original) == stopped
    assert (reopened_path.read_bytes(), source.read_bytes()) == bytes_before
    assert len(attempts) == 1

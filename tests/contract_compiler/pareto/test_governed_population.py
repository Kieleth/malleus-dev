"""P2 RED contract for governed population preparation and replay."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from malleus import KnowledgeGraph
from malleus._contract_pipeline import population
from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchor,
    _anchored_history,
    _binding_payload,
    _event,
    _generic_compilation,
    _ledger_bytes,
    _protocol_events,
    _record_change,
    _admit_record_change,
)
from tests.contract_compiler.pareto.test_domain_history_profile import (
    SOURCE_ASSERTION_PROFILE_DATA,
    STATE_VERSION_PROFILE_DATA,
)
from tests.contract_compiler.pareto.test_population_plan import (
    PROFILE_BYTES,
    _plan,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
    _effective,
    _program_payload,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


PROFILE_IDENTITIES = {
    "source-assertion": "sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5",
    "state-version": "sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3",
}
NEUTRAL_PROFILE_DATA = json.loads(PROFILE_BYTES)
SHOP_FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_correction_v1"
)
SHOP_BASE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment/input/tbox/small-shop.yaml"
)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _artifact_event(record_id: str, content: bytes) -> bytes:
    return _event(
        "ARTIFACT_REGISTERED",
        artifact_id=record_id,
        artifact_identity=_digest(content),
    )


def _gaps_bytes(plan: dict[str, object]) -> bytes:
    return _canonical({"gaps": plan["gaps"], "plan_id": plan["plan_id"]})


def _retention_events(
    plan: dict[str, object],
    profile: dict[str, object],
    *,
    include_profile: bool = True,
) -> dict[str, bytes]:
    profile_id = f"profile:{profile['profile_id']}"
    plan_id = plan["plan_id"]
    assert isinstance(plan_id, str)
    events = {plan_id: _artifact_event(plan_id, _canonical(plan))}
    if include_profile:
        events[profile_id] = _artifact_event(profile_id, _canonical(profile))
    if plan["gaps"]:
        gaps_id = f"{plan_id}:gaps"
        events[gaps_id] = _artifact_event(gaps_id, _gaps_bytes(plan))
    return events


def _prepare(
    history: KnowledgeChangeHistory,
    plan: dict[str, object],
    profile: dict[str, object],
    *,
    include_profile: bool = True,
):
    return population.prepare_population_change(
        history=history,
        plan=plan,
        profile=profile,
        retention_events=_retention_events(
            plan,
            profile,
            include_profile=include_profile,
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )


def _custom_evidence_history(tmp_path: Path):
    compiled = _generic_compilation()
    machine = _program_payload()
    machine["events"]["EVIDENCE_CAPTURED"] = {
        "instructions": [
            {
                "id_field": "evidence_id",
                "opcode": "REQUIRE_GLOBAL_ID_ABSENT",
                "refusal": "GLOBAL_RECORD_ID_EXISTS",
            },
            {"opcode": "STORE_EVENT_RECORD", "record_type": "EvidenceRecord"},
        ],
        "record_type": "EvidenceRecord",
    }
    machine["record_schemas"]["EvidenceRecord"] = {
        "fields": {
            "evidence_id": "STRING",
            "evidence_identity": "DIGEST",
        },
        "id_field": "evidence_id",
        "input_fields": ["evidence_id", "evidence_identity"],
    }
    partial = _effective(
        machine,
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
    )
    binding_payload = _binding_payload()
    binding_payload["retention_events"]["EVIDENCE_CAPTURED"] = {
        "allowed_roles": ["RETAINED_EVIDENCE"],
        "identity_field": "evidence_identity",
        "record_id_field": "evidence_id",
    }
    binding = KnowledgeChangeHistoryBinding.from_bytes(_canonical(binding_payload))
    history = KnowledgeChangeHistory(
        tmp_path / "custom-evidence-history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    source_bytes = b"custom retained source\n"
    evidence_bytes = b"custom retained adapter evidence\n"
    anchors = (
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="validated-contract-artifact",
                artifact_identity=_digest(compiled.artifact.artifact_bytes),
            ),
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="contract-artifact",
                artifact_identity=_digest(partial.canonical_bytes),
            ),
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="history-binding-artifact",
                artifact_identity=_digest(binding.canonical_bytes),
            ),
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="source-artifact",
                artifact_identity=_digest(source_bytes),
            ),
            source_bytes,
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="source-artifact",
                source_id="source-generic",
                source_identity=_digest(source_bytes),
            ),
            source_bytes,
            "RETAINED_SOURCE",
        ),
        (
            _event(
                "EVIDENCE_CAPTURED",
                evidence_id="evidence-generic",
                evidence_identity=_digest(evidence_bytes),
            ),
            evidence_bytes,
            "RETAINED_EVIDENCE",
        ),
    )
    for event, content, role in anchors:
        _anchor(history, event, content, role)
    return history, compiled, partial, _digest(source_bytes), _digest(evidence_bytes)


@pytest.mark.parametrize(
    ("profile_data", "constant_name"),
    [
        (SOURCE_ASSERTION_PROFILE_DATA, "SOURCE_ASSERTION_PROFILE"),
        (STATE_VERSION_PROFILE_DATA, "STATE_VERSION_PROFILE"),
    ],
)
def test_profiles_are_canonical_immutable_and_content_addressed(
    profile_data: dict[str, object], constant_name: str
) -> None:
    compiled = population.DomainHistoryProfile.from_data(deepcopy(profile_data))
    shipped = getattr(population, constant_name)

    assert compiled == shipped
    assert compiled.canonical_bytes == _canonical(profile_data)
    assert compiled.identity == PROFILE_IDENTITIES[compiled.profile_id]
    assert set(compiled.data) == {
        "change_semantics",
        "genesis",
        "grammar",
        "grounding",
        "ontology_roles",
        "origin",
        "profile_id",
        "projection_rule_family",
        "semantic_unit",
        "time_semantics",
    }
    with pytest.raises(TypeError):
        compiled.data["grounding"]["note"] = "changed"
    with pytest.raises(AttributeError):
        compiled.identity = "sha256:" + "0" * 64


def test_profile_exposes_the_exact_value_bound_by_its_bytes() -> None:
    value = deepcopy(STATE_VERSION_PROFILE_DATA)
    value["grounding"] = {1: "integer key is canonicalized"}

    compiled = population.DomainHistoryProfile.from_data(value)

    assert compiled.canonical_bytes == _canonical(value)
    assert compiled.grounding == {"1": "integer key is canonicalized"}
    with pytest.raises(TypeError):
        compiled.grounding["1"] = "changed"


def test_profile_rebuilds_a_directly_constructed_mutable_value() -> None:
    canonical_bytes = _canonical(STATE_VERSION_PROFILE_DATA)
    mutable_data = deepcopy(STATE_VERSION_PROFILE_DATA)
    forged = population.DomainHistoryProfile(
        canonical_bytes=canonical_bytes,
        identity=_digest(canonical_bytes),
        data=mutable_data,
        profile_id="state-version",
        semantic_unit="STATE_VERSION",
        origin="EMPTY",
        genesis=mutable_data["genesis"],
        time_semantics=mutable_data["time_semantics"],
        change_semantics=mutable_data["change_semantics"],
        ontology_roles=mutable_data["ontology_roles"],
        projection_rule_family=mutable_data["projection_rule_family"],
        grounding=mutable_data["grounding"],
    )

    rebuilt = population.DomainHistoryProfile.from_data(forged)

    assert rebuilt.canonical_bytes == forged.canonical_bytes
    assert rebuilt.identity == forged.identity
    assert rebuilt is not forged
    with pytest.raises(TypeError):
        rebuilt.grounding["note"] = "changed"


@pytest.mark.parametrize("canonical_bytes", [b"not-json", b'{"grammar":'])
def test_profile_wraps_malformed_instance_bytes(
    canonical_bytes: bytes,
) -> None:
    forged = population.DomainHistoryProfile(
        canonical_bytes=canonical_bytes,
        identity=_digest(canonical_bytes),
        data=STATE_VERSION_PROFILE_DATA,
        profile_id="state-version",
        semantic_unit="STATE_VERSION",
        origin="EMPTY",
        genesis=STATE_VERSION_PROFILE_DATA["genesis"],
        time_semantics=STATE_VERSION_PROFILE_DATA["time_semantics"],
        change_semantics=STATE_VERSION_PROFILE_DATA["change_semantics"],
        ontology_roles=STATE_VERSION_PROFILE_DATA["ontology_roles"],
        projection_rule_family=STATE_VERSION_PROFILE_DATA["projection_rule_family"],
        grounding=STATE_VERSION_PROFILE_DATA["grounding"],
    )

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.DomainHistoryProfile.from_data(forged)

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE
    )


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        ("extra", "FIELDS_NOT_CLOSED"),
        ("missing", "FIELDS_NOT_CLOSED"),
        ("grammar", "UNSUPPORTED_GRAMMAR"),
        ("semantic-unit", "UNKNOWN_SEMANTIC_UNIT"),
        ("origin", "UNKNOWN_ORIGIN"),
        ("empty-grounding", "GROUNDING_REQUIRED"),
        ("nonobject-grounding", "GROUNDING_REQUIRED"),
    ],
)
def test_profile_refuses_undeclared_semantics(mutation: str, reason: str) -> None:
    value = deepcopy(STATE_VERSION_PROFILE_DATA)
    if mutation == "extra":
        value["extra"] = True
    elif mutation == "missing":
        del value["origin"]
    elif mutation == "grammar":
        value["grammar"] = "other"
    elif mutation == "semantic-unit":
        value["semantic_unit"] = "VIBE"
    elif mutation == "origin":
        value["origin"] = "SOMEWHERE"
    elif mutation == "empty-grounding":
        value["grounding"] = {}
    elif mutation == "nonobject-grounding":
        value["grounding"] = []
    else:
        raise AssertionError(mutation)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.DomainHistoryProfile.from_data(value)

    assert refusal.value.reason is getattr(
        population.PopulationPlanRefusalReason, reason
    )


def test_prepared_neutral_change_admits_reopens_and_matches_direct_graph(
    tmp_path: Path,
) -> None:
    history, compiled, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    before = history.replay()

    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    assert prepared.compilation.status is population.PopulationPlanStatus.CHANGE_SET
    assert prepared.change_set is not None
    assert prepared.change_set.sources == (("source-generic", source),)
    assert tuple(identifier for identifier, _ in prepared.change_set.evidence) == (
        "profile:state-version",
        "plan:neutral:1",
        "evidence-generic",
    )
    assert prepared.change_set.operations == prepared.compilation.operations
    assert prepared.change_set.valid_time == prepared.compilation.valid_time
    assert prepared.change_set.base_ledger_head == prepared.retention_replay.ledger_head
    assert (
        prepared.change_set.base_ledger_event_count
        == prepared.retention_replay.ledger_event_count
    )
    assert prepared.retention_replay.graph.snapshot() == before.graph.snapshot()

    admitted = history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            identifier_suffix="-population-p2",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    direct = KnowledgeGraph.from_records(compiled.view, plan["records"])

    assert admitted.graph.export_records() == direct.export_records()
    assert reopened.graph.export_records() == admitted.graph.export_records()
    assert reopened.receipt == admitted.receipt
    assert reopened.change_sets == admitted.change_sets


def test_preparation_accepts_a_shipped_profile_value(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["history_profile"]["sha256"] = population.STATE_VERSION_PROFILE.identity

    prepared = population.prepare_population_change(
        history=history,
        plan=plan,
        profile=population.STATE_VERSION_PROFILE,
        retention_events=_retention_events(plan, STATE_VERSION_PROFILE_DATA),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert prepared.profile == population.STATE_VERSION_PROFILE
    assert prepared.profile is not population.STATE_VERSION_PROFILE
    assert prepared.change_set is not None


def test_preparation_retains_profile_plan_and_gaps_in_one_ordered_batch(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "the contract has no neutral missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    before = history.replay()

    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    retained_ids = tuple(
        member.record_id for member in prepared.retention_replay.retained_inputs
    )
    assert retained_ids[-3:] == (
        "profile:state-version",
        "plan:neutral:1",
        "plan:neutral:1:gaps",
    )
    assert prepared.retention_replay.retained_bytes(
        "profile:state-version"
    ) == _canonical(NEUTRAL_PROFILE_DATA)
    assert prepared.retention_replay.retained_bytes("plan:neutral:1") == _canonical(
        plan
    )
    assert prepared.retention_replay.retained_bytes(
        "plan:neutral:1:gaps"
    ) == _gaps_bytes(plan)
    assert prepared.retention_replay.ledger_event_count == before.ledger_event_count + 3
    assert prepared.change_set is not None
    assert prepared.change_set.base_ledger_head == prepared.retention_replay.ledger_head

    ledger = [json.loads(line) for line in history.path.read_text().splitlines()]
    assert [event["payload"]["record_id"] for event in ledger[-3:]] == list(
        retained_ids[-3:]
    )


def test_custom_evidence_retention_event_prepares_admits_and_reopens(
    tmp_path: Path,
) -> None:
    history, compiled, partial, source, evidence = _custom_evidence_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    artifacts = {
        "profile:state-version": _canonical(NEUTRAL_PROFILE_DATA),
        "plan:neutral:1": _canonical(plan),
        "plan:neutral:1:gaps": _gaps_bytes(plan),
    }
    events = {
        record_id: _event(
            "EVIDENCE_CAPTURED",
            evidence_id=record_id,
            evidence_identity=_digest(content),
        )
        for record_id, content in artifacts.items()
    }

    prepared = population.prepare_population_change(
        history=history,
        plan=plan,
        profile=NEUTRAL_PROFILE_DATA,
        retention_events=events,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    assert prepared.change_set is not None
    admitted = history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            identifier_suffix="-custom-evidence-event",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    direct = KnowledgeGraph.from_records(compiled.view, plan["records"])

    assert reopened.graph.export_records() == direct.export_records()
    assert reopened.receipt == admitted.receipt
    for record_id, content in artifacts.items():
        assert reopened.retained_bytes(record_id) == content
        assert (
            reopened.machine_state.get_record("EvidenceRecord", record_id) is not None
        )


@pytest.mark.parametrize(
    ("defect", "reason"),
    [
        ("absent-source", "UNRETAINED_SOURCE"),
        ("absent-evidence", "UNRETAINED_EVIDENCE"),
        ("source-digest", "IDENTITY_MISMATCH"),
        ("evidence-digest", "IDENTITY_MISMATCH"),
        ("profile-digest", "IDENTITY_MISMATCH"),
        ("profile-id", "IDENTITY_MISMATCH"),
    ],
)
def test_reference_preflight_refuses_without_retaining_partial_artifacts(
    tmp_path: Path, defect: str, reason: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    if defect == "absent-source":
        plan["sources"][0]["source_id"] = "source:absent"
        for derivation in plan["derivations"]:
            derivation["source_id"] = "source:absent"
    elif defect == "absent-evidence":
        plan["evidence"][0]["evidence_id"] = "evidence:absent"
    elif defect == "source-digest":
        plan["sources"][0]["sha256"] = "sha256:" + "0" * 64
    elif defect == "evidence-digest":
        plan["evidence"][0]["sha256"] = "sha256:" + "0" * 64
    elif defect == "profile-digest":
        plan["history_profile"]["sha256"] = "sha256:" + "0" * 64
    elif defect == "profile-id":
        plan["history_profile"]["profile_id"] = "other-profile"
    else:
        raise AssertionError(defect)
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    assert refusal.value.reason is getattr(
        population.PopulationPlanRefusalReason, reason
    )
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.node_count == 0


def test_duplicate_plan_id_refuses_before_any_second_write(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    _prepare(history, plan, NEUTRAL_PROFILE_DATA)
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events={},
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.DUPLICATE_PLAN_ID
    )
    assert _ledger_bytes(history) == ledger_before


def test_duplicate_change_set_id_refuses_before_retaining_the_plan(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    legacy = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change:plan:neutral:1",
        record_id="left-legacy",
        label="legacy",
        order="legacy-1",
    )
    _admit_record_change(history, legacy, suffix="-legacy-change-id")
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.DUPLICATE_CHANGE_SET_ID
    )
    assert _ledger_bytes(history) == ledger_before


def test_generated_gaps_id_collision_refuses_before_any_write(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    collision_id = "plan:neutral:1:gaps"
    collision_bytes = b"existing artifact\n"
    _anchor(
        history,
        _artifact_event(collision_id, collision_bytes),
        collision_bytes,
        "RETAINED_EVIDENCE",
    )
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.DUPLICATE_ARTIFACT_ID
    )
    assert _ledger_bytes(history) == ledger_before


@pytest.mark.parametrize("mutation", ["missing", "extra"])
def test_retention_event_set_is_closed_and_refuses_before_write(
    tmp_path: Path, mutation: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    if mutation == "missing":
        del events["plan:neutral:1"]
    else:
        events["extra"] = _artifact_event("extra", b"extra\n")
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before


def test_invalid_later_retention_event_rolls_back_the_whole_anchor_batch(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    events["plan:neutral:1"] = _artifact_event(
        "plan:neutral:1", b"different plan bytes\n"
    )
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before
    retained_ids = {member.record_id for member in history.replay().retained_inputs}
    assert "profile:state-version" not in retained_ids
    assert "plan:neutral:1" not in retained_ids
    assert "plan:neutral:1:gaps" not in retained_ids


@pytest.mark.parametrize("artifact", ["profile", "plan", "gaps"])
def test_retention_event_identifier_substitution_refuses_before_any_write(
    tmp_path: Path,
    artifact: str,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    expected = {
        "profile": ("profile:state-version", _canonical(NEUTRAL_PROFILE_DATA)),
        "plan": ("plan:neutral:1", _canonical(plan)),
        "gaps": ("plan:neutral:1:gaps", _gaps_bytes(plan)),
    }
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    expected_id, content = expected[artifact]
    events[expected_id] = _artifact_event(f"misbound:{artifact}", content)
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before


@pytest.mark.parametrize("artifact", ["profile", "plan", "gaps"])
def test_source_event_cannot_retain_generated_evidence_artifact(
    tmp_path: Path,
    artifact: str,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    expected = {
        "profile": ("profile:state-version", _canonical(NEUTRAL_PROFILE_DATA)),
        "plan": ("plan:neutral:1", _canonical(plan)),
        "gaps": ("plan:neutral:1:gaps", _gaps_bytes(plan)),
    }
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    expected_id, content = expected[artifact]
    events[expected_id] = _event(
        "SOURCE_REGISTERED",
        artifact_id="validated-contract-artifact",
        source_id=expected_id,
        source_identity=_digest(content),
    )
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before


def test_no_domain_change_refuses_a_misbound_plan_event_without_writing(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["records"] = {"entities": [], "relations": []}
    plan["derivations"] = []
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "missing type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    events["plan:neutral:1"] = _artifact_event(
        "misbound:no-domain-change-plan", _canonical(plan)
    )
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before


def test_retention_event_identifier_permutation_refuses_before_any_write(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    profile_id = "profile:state-version"
    plan_id = "plan:neutral:1"
    profile_bytes = _canonical(NEUTRAL_PROFILE_DATA)
    plan_bytes = _canonical(plan)
    events = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    events[profile_id] = _artifact_event(plan_id, profile_bytes)
    events[plan_id] = _artifact_event(profile_id, plan_bytes)
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before


def test_stateful_retention_mapping_cannot_change_after_preflight(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    profile_id = "profile:state-version"
    plan_id = "plan:neutral:1"
    profile_bytes = _canonical(NEUTRAL_PROFILE_DATA)
    plan_bytes = _canonical(plan)
    valid = _retention_events(plan, NEUTRAL_PROFILE_DATA)
    substituted = {
        profile_id: _artifact_event(plan_id, profile_bytes),
        plan_id: _artifact_event(profile_id, plan_bytes),
    }

    class StatefulEvents(Mapping[str, bytes]):
        def __init__(self) -> None:
            self.reads = {key: 0 for key in valid}

        def __getitem__(self, key: str) -> bytes:
            self.reads[key] += 1
            return valid[key] if self.reads[key] == 2 else substituted[key]

        def __iter__(self) -> Iterator[str]:
            return iter(valid)

        def __len__(self) -> int:
            return len(valid)

    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.prepare_population_change(
            history=history,
            plan=plan,
            profile=NEUTRAL_PROFILE_DATA,
            retention_events=StatefulEvents(),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT
    )
    assert _ledger_bytes(history) == ledger_before
    retained_ids = {member.record_id for member in history.replay().retained_inputs}
    assert profile_id not in retained_ids
    assert plan_id not in retained_ids


def test_no_domain_change_retains_evidence_without_composing_a_change_set(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["records"] = {"entities": [], "relations": []}
    plan["derivations"] = []
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "the source statement has no contract type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]
    before = history.replay()

    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert (
        prepared.compilation.status is population.PopulationPlanStatus.NO_DOMAIN_CHANGE
    )
    assert prepared.change_set is None
    assert prepared.retention_replay.graph.snapshot() == before.graph.snapshot()
    assert prepared.retention_replay.acceptance_head == before.acceptance_head
    assert prepared.retention_replay.materialization_head == before.materialization_head
    assert prepared.retention_replay.ledger_head != before.ledger_head
    assert (
        prepared.retention_replay.machine_state.identity
        != before.machine_state.identity
    )
    assert prepared.retention_replay.change_sets == ()
    assert reopened.receipt == prepared.retention_replay.receipt
    assert {
        "evidence-generic",
        "profile:state-version",
        "plan:neutral:1",
        "plan:neutral:1:gaps",
    } <= {member.record_id for member in reopened.retained_inputs}
    assert all(
        json.loads(line)["event_type"] != "KNOWLEDGE_CHANGE_SET_RETAINED"
        for line in history.path.read_text().splitlines()
    )


def test_no_domain_change_ignores_an_unused_change_set_id_collision(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    plan_id = "plan:gaps-only:collision"
    legacy = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id=f"change:{plan_id}",
        record_id="left-existing",
        label="existing",
        order="existing-1",
    )
    _admit_record_change(history, legacy, suffix="-gaps-only-change-id")
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    plan["plan_id"] = plan_id
    plan["records"] = {"entities": [], "relations": []}
    plan["derivations"] = []
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "the source statement has no contract type",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]

    prepared = _prepare(history, plan, NEUTRAL_PROFILE_DATA)

    assert (
        prepared.compilation.status is population.PopulationPlanStatus.NO_DOMAIN_CHANGE
    )
    assert prepared.change_set is None
    retained_ids = {member.record_id for member in history.replay().retained_inputs}
    assert plan_id in retained_ids
    assert f"{plan_id}:gaps" in retained_ids


def test_reused_historical_record_refuses_before_retaining_the_next_plan(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    prepared = _prepare(history, first, NEUTRAL_PROFILE_DATA)
    assert prepared.change_set is not None
    history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            identifier_suffix="-population-first",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    repeated = deepcopy(first)
    repeated["plan_id"] = "plan:neutral:2"
    ledger_before = _ledger_bytes(history)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _prepare(
            history,
            repeated,
            NEUTRAL_PROFILE_DATA,
            include_profile=False,
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.DUPLICATE_RECORD_ID
    )
    assert _ledger_bytes(history) == ledger_before


def _shop_history(tmp_path: Path):
    correction = (SHOP_FIXTURE / "input/tbox/small-shop-correction.yaml").read_bytes()
    base = SHOP_BASE.read_bytes()
    source = (SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl").read_bytes()
    compiled = _compile_binding(
        _binding(
            {
                "small-shop-correction": correction,
                "small-shop": base,
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "small-shop-correction",
        )
    )
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    binding = KnowledgeChangeHistoryBinding.from_bytes(_canonical(_binding_payload()))
    history = KnowledgeChangeHistory(
        tmp_path / "shop-history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    anchors = (
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="validated-contract-artifact",
                artifact_identity=_digest(compiled.artifact.artifact_bytes),
            ),
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="contract-artifact",
                artifact_identity=_digest(partial.canonical_bytes),
            ),
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="history-binding-artifact",
                artifact_identity=_digest(binding.canonical_bytes),
            ),
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="source-artifact",
                artifact_identity=_digest(source),
            ),
            source,
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="source-artifact",
                source_id="source:supplier-order-history",
                source_identity=_digest(source),
            ),
            source,
            "RETAINED_SOURCE",
        ),
    )
    for event, content, role in anchors:
        _anchor(history, event, content, role)
    return history, partial, source


def _shop_plan(
    contract_identity: str,
    source_identity: str,
    *,
    occurrence: str,
    quantity: int,
    supersedes: str | None,
) -> dict[str, object]:
    record_id = f"supplier-order-state:B:{occurrence}"
    properties = {
        "ordered_quantity": quantity,
        "product_code": "Y",
        "source_occurrence_id": occurrence,
        "supplier_order_id": "B",
    }
    plan = {
        "adapter": {"adapter_id": "small-shop-row-mapping", "version": "0"},
        "contract_identity": contract_identity,
        "derivations": [
            {
                "locator": f"row:{0 if occurrence == 'e4' else 1}:{column}",
                "path": ["properties", field],
                "record_id": record_id,
                "source_id": "source:supplier-order-history",
            }
            for field, column in (
                ("supplier_order_id", "supplier_order_id"),
                ("product_code", "product_code"),
                ("ordered_quantity", "quantity"),
                ("source_occurrence_id", "event_id"),
            )
        ],
        "evidence": [],
        "gaps": [],
        "grammar": "malleus.population-plan/private-v0",
        "history_profile": {
            "profile_id": "state-version",
            "sha256": PROFILE_IDENTITIES["state-version"],
        },
        "plan_id": f"plan:shop:B:{occurrence}",
        "records": {
            "entities": [
                {
                    "id": record_id,
                    "properties": properties,
                    "type": "SupplierOrderState",
                }
            ],
            "relations": [],
        },
        "sources": [
            {
                "sha256": source_identity,
                "source_id": "source:supplier-order-history",
            }
        ],
        "supersessions": (
            []
            if supersedes is None
            else [{"record_id": record_id, "supersedes_record_id": supersedes}]
        ),
        "valid_time": {"kind": "ORDER_ONLY", "value": occurrence},
    }
    return plan


def test_small_shop_e4_e7_reopens_as_one_current_state_version(
    tmp_path: Path,
) -> None:
    history, partial, source = _shop_history(tmp_path)
    e4 = _shop_plan(
        partial.identity,
        _digest(source),
        occurrence="e4",
        quantity=1,
        supersedes=None,
    )
    prepared_e4 = _prepare(history, e4, STATE_VERSION_PROFILE_DATA)
    assert prepared_e4.change_set is not None
    history.admit(
        change_set=prepared_e4.change_set,
        machine_events=_protocol_events(
            prepared_e4.change_set,
            prepared_e4.retention_replay.machine_state.identity,
            identifier_suffix="-shop-e4",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    e4_id = "supplier-order-state:B:e4"
    e7 = _shop_plan(
        partial.identity,
        _digest(source),
        occurrence="e7",
        quantity=2,
        supersedes=e4_id,
    )
    prepared_e7 = _prepare(
        history,
        e7,
        STATE_VERSION_PROFILE_DATA,
        include_profile=False,
    )
    assert prepared_e7.change_set is not None
    admitted = history.admit(
        change_set=prepared_e7.change_set,
        machine_events=_protocol_events(
            prepared_e7.change_set,
            prepared_e7.retention_replay.machine_state.identity,
            identifier_suffix="-shop-e7",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert admitted.graph.query("SupplierOrderState", supplier_order_id="B") == [
        {
            "id": "supplier-order-state:B:e7",
            "ordered_quantity": 2,
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "supplier_order_id": "B",
            "type": "SupplierOrderState",
        }
    ]
    assert prepared_e7.change_set.supersedes == ("change:plan:shop:B:e4",)
    assert prepared_e7.change_set.operations[0].supersedes_record_id == e4_id
    assert reopened.record_history[e4_id].superseded_by == ("supplier-order-state:B:e7")
    assert reopened.record_history[e4_id].valid_to == prepared_e7.change_set.valid_time
    assert (
        sum(
            member.record_id == "profile:state-version"
            for member in reopened.retained_inputs
        )
        == 1
    )
    assert reopened.retained_bytes("plan:shop:B:e4") == _canonical(e4)
    assert reopened.retained_bytes("plan:shop:B:e7") == _canonical(e7)
    assert reopened.graph.export_records() == admitted.graph.export_records()
    assert reopened.receipt == admitted.receipt

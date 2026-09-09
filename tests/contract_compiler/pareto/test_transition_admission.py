"""Selected transition rules must gate the owning history, not its helpers."""

from base64 import b64encode
import json

import pytest

from malleus import compiler as api
from tests.contract_compiler.pareto import test_knowledge_change_history as fixtures
from tests.contract_compiler.pareto import test_public_compiler as public
from tests.contract_compiler.pareto.test_maintained_projection import (
    assert_parity,
    coordinates,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
    _effective,
    _program_payload,
)


SOURCE = b"""\
id: https://example.malleus.dev/transition-test
name: transition_test
default_range: string
prefixes:
  malleus: https://malleus.dev/schema/
  linkml: https://w3id.org/linkml/
imports: [linkml:types, malleus]
classes:
  State:
    is_a: Entity
  LeafState:
    is_a: State
  Occurrence:
    is_a: Event
"""


def profile(*, state="State", event="Occurrence"):
    data = json.loads(api.OBJECT_EVENT_PROFILE.canonical_bytes)
    data["ontology_roles"]["state"] = [state] if state else []
    data["ontology_roles"]["event"] = [event]
    return api.DomainHistoryProfile.from_data(data)


def program(history_profile, *, role="state", match="EXACT"):
    data = _program_payload()
    data["grammar"] = "malleus.protocol-machine/private-v1"
    data["admission_rules"] = {
        "history_profile_identity": history_profile.identity,
        "instructions": [
            {
                "opcode": "REQUIRE_TYPES_IN_ROLE",
                "selection": "REPLACEMENTS",
                "role": role,
                "match": match,
                "refusal": "REPLACEMENT_OUTSIDE_SELECTED_ROLE",
            }
        ],
    }
    return data


def setup_history(tmp_path, monkeypatch, *, rules=None, selected=None, source=SOURCE):
    selected = profile() if selected is None else selected
    rules = program(selected) if rules is None else rules
    # This patch changes only the old fixture's contract INPUT producer.
    # Compilation, history, admission and replay use their real implementations.
    with monkeypatch.context() as patch:
        patch.setattr(
            fixtures,
            "_effective",
            lambda **kwargs: _effective(machine_payload=rules, **kwargs),
        )
        history, *_ = fixtures._anchored_history(tmp_path, contract_source=source)
    fixtures._anchor(
        history,
        fixtures._event(
            "ARTIFACT_REGISTERED",
            artifact_id="selected-history-profile",
            artifact_identity=selected.identity,
        ),
        selected.canonical_bytes,
        "RETAINED_EVIDENCE",
    )
    return history


def change(history, name, kind="State", *, prior=None, include_profile=True):
    event = kind == "Occurrence"
    operation = api.KnowledgeOperation(
        ordinal=0,
        operation_id=f"op:{name}",
        operation_type="CREATE_EVENT" if event else "CREATE_ENTITY",
        record_type=kind,
        record_id=name,
        properties={"event_type": "OBSERVED"} if event else {},
        depends_on=(),
        supersedes_record_id=prior,
    )
    return history.compose_change_set(
        change_set_id=f"change:{name}",
        source_record_ids=("source-generic",),
        evidence_record_ids=("selected-history-profile",)
        if include_profile
        else ("evidence-generic",),
        operations=(operation,),
        valid_time=api.KnowledgeValidTime("ORDER_ONLY", name),
        supersedes=(),
    )


def events(history, candidate):
    # Deliberately supplied SATISFIED attestations cannot override the pure guard.
    return fixtures._protocol_events(
        candidate,
        history.replay().machine_state.identity,
        identifier_suffix=candidate.change_set_id,
    )


def admit(history, candidate):
    return history.admit(
        change_set=candidate,
        machine_events=events(history, candidate),
        transaction_time=fixtures.TRANSACTION_TIME,
        actor_id="actor:test",
    )


def assert_refused_unchanged(history, candidate, reason):
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as caught:
        admit(history, candidate)
    assert caught.value.reason.name == reason
    assert history.path.read_bytes() == before
    return caught.value


def test_rule_gate_allowed_replacement_event_addition_and_replay(tmp_path, monkeypatch):
    history = setup_history(tmp_path, monkeypatch)
    admit(history, change(history, "s1"))
    reader = api.KnowledgeHistoryProjection.open(history.path)
    admit(history, change(history, "e1", "Occurrence"))
    final = admit(history, change(history, "s2", prior="s1"))
    assert final.record_history["s1"].superseded_by == "s2"
    assert final.graph.get_node("s2") is not None
    assert final.graph.get_node("e1") is not None
    assert_parity(reader.refresh(**coordinates(final)), final)
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert_parity(reopened, final)
    assert (
        reopened.partial_contract.normative_profile.protocol_machine_program.data[
            "admission_rules"
        ]["history_profile_identity"]
        == profile().identity
    )


def test_low_level_admission_refuses_event_replacement_despite_satisfied_checks(
    tmp_path, monkeypatch
):
    history = setup_history(tmp_path, monkeypatch)
    admit(history, change(history, "e1", "Occurrence"))
    refused = assert_refused_unchanged(
        history,
        change(history, "e2", "Occurrence", prior="e1"),
        "TRANSITION_RULE_REFUSAL",
    )
    assert "REPLACEMENT_OUTSIDE_SELECTED_ROLE" in refused.detail
    assert "0" in refused.detail and "e2" in refused.detail


@pytest.mark.parametrize("role,accepted", [("state", False), ("event", True)])
def test_changing_only_rule_changes_verdict(tmp_path, monkeypatch, role, accepted):
    selected = profile()
    history = setup_history(tmp_path, monkeypatch, rules=program(selected, role=role))
    admit(history, change(history, "e1", "Occurrence"))
    candidate = change(history, "e2", "Occurrence", prior="e1")
    if accepted:
        assert admit(history, candidate).record_history["e1"].superseded_by == "e2"
    else:
        assert_refused_unchanged(history, candidate, "TRANSITION_RULE_REFUSAL")


@pytest.mark.parametrize("match,accepted", [("EXACT", False), ("SUBTYPE", True)])
def test_type_matching_is_explicit(tmp_path, monkeypatch, match, accepted):
    selected = profile()
    history = setup_history(tmp_path, monkeypatch, rules=program(selected, match=match))
    admit(history, change(history, "s1", "LeafState"))
    candidate = change(history, "s2", "LeafState", prior="s1")
    if accepted:
        assert admit(history, candidate).graph.get_node("s2") is not None
    else:
        assert_refused_unchanged(history, candidate, "TRANSITION_RULE_REFUSAL")


def test_role_names_resolve_contract_types_without_core_domain_branches(
    tmp_path, monkeypatch
):
    selected = profile(state="RenamedState")
    source = SOURCE.replace(b"State", b"RenamedState")
    history = setup_history(tmp_path, monkeypatch, selected=selected, source=source)
    admit(history, change(history, "s1", "RenamedState"))
    assert admit(history, change(history, "s2", "RenamedState", prior="s1"))


@pytest.mark.parametrize(
    "problem", ["absent", "wrong-profile", "unknown-role", "unknown-type"]
)
def test_required_binding_refuses_even_without_replacements(
    tmp_path, monkeypatch, problem
):
    selected = profile(state="Unknown" if problem == "unknown-type" else "State")
    rules = program(selected, role="unknown" if problem == "unknown-role" else "state")
    if problem == "wrong-profile":
        rules["admission_rules"]["history_profile_identity"] = "sha256:" + "0" * 64
    history = setup_history(tmp_path, monkeypatch, selected=selected, rules=rules)
    assert_refused_unchanged(
        history,
        change(history, "s1", include_profile=problem != "absent"),
        "TRANSITION_BINDING_REFUSAL",
    )


def test_empty_selected_role_does_not_turn_into_fallback(tmp_path, monkeypatch):
    history = setup_history(tmp_path, monkeypatch, selected=profile(state=""))
    admit(history, change(history, "s1"))
    assert_refused_unchanged(
        history, change(history, "s2", prior="s1"), "TRANSITION_RULE_REFUSAL"
    )


@pytest.mark.parametrize(
    "field",
    [
        "base_ledger_head",
        "base_ledger_event_count",
        "base_acceptance_head",
        "base_materialization_head",
        "base_accepted_state_digest",
        "contract_identity",
    ],
)
def test_stale_selected_transition_preserves_admission_bytes(
    tmp_path, monkeypatch, field
):
    history = setup_history(tmp_path, monkeypatch)
    payload = json.loads(change(history, "s1").canonical_bytes)
    payload[field] = 999 if field == "base_ledger_event_count" else "sha256:" + "0" * 64
    candidate = api.KnowledgeChangeSet.from_bytes(_canonical(payload))
    assert_refused_unchanged(history, candidate, "STALE_BASE")


@pytest.mark.parametrize(
    "field,value",
    [
        ("opcode", "CALL_PYTHON"),
        ("selection", "ALL"),
        ("match", "GUESS"),
        ("role", ""),
        ("refusal", ""),
        ("callback", "escape"),
    ],
)
def test_closed_rule_instruction(field, value):
    data = program(profile())
    api.ProtocolMachineProgram.from_bytes(_canonical(data))
    data["admission_rules"]["instructions"][0][field] = value
    with pytest.raises(api.ProtocolMachineProgramRefusal):
        api.ProtocolMachineProgram.from_bytes(_canonical(data))


def test_explicit_machine_epoch_and_capabilities_remain_closed():
    data = program(profile())
    api.ProtocolMachineProgram.from_bytes(_canonical(data))
    for malformed in (
        {**data, "grammar": "malleus.protocol-machine/private-v0"},
        {key: value for key, value in data.items() if key != "admission_rules"},
        {**data, "capabilities": ["arbitrary-callback"]},
        {**data, "admission_rules": {**data["admission_rules"], "instructions": []}},
    ):
        with pytest.raises(api.ProtocolMachineProgramRefusal):
            api.ProtocolMachineProgram.from_bytes(_canonical(malformed))
    old = api.ProtocolMachineProgram.from_bytes(_canonical(_program_payload()))
    assert old.canonical_bytes == _canonical(_program_payload())


def test_valid_hash_chain_cannot_hide_forbidden_transition_from_replay(
    tmp_path, monkeypatch
):
    history = setup_history(tmp_path, monkeypatch)
    before = admit(history, change(history, "e1", "Occurrence"))
    reader = api.KnowledgeHistoryProjection.open(history.path)
    candidate = change(history, "e2", "Occurrence", prior="e1")
    payloads = [
        {
            "event_type": "KNOWLEDGE_CHANGE_SET_RETAINED",
            "payload": {
                "change_set_bytes_base64": b64encode(candidate.canonical_bytes).decode(
                    "ascii"
                ),
                "change_set_id": candidate.change_set_id,
                "change_set_identity": candidate.identity,
            },
        },
        *(json.loads(event) for event in events(history, candidate)),
    ]
    # Deliberately bypass the history writer while keeping the envelope chain valid.
    history._ledger.append_many(
        [
            {
                **value,
                "event_id": f"hostile:{index}",
                "actor_id": "actor:test",
                "transaction_time": fixtures.TRANSACTION_TIME,
            }
            for index, value in enumerate(payloads)
        ],
        validate=lambda _: None,
    )
    envelopes = history._ledger.read()
    for read in (
        history.replay,
        lambda: api.KnowledgeChangeHistory.reopen(history.path),
        lambda: reader.refresh(
            expected_head_hash=envelopes[-1]["event_hash"],
            expected_event_count=len(envelopes),
        ),
    ):
        with pytest.raises(api.KnowledgeChangeRefusal) as caught:
            read()
        assert caught.value.reason.name == "TRANSITION_RULE_REFUSAL"
    assert_parity(reader.current(**coordinates(before)), before)


def structural_program(*, match="SUBTYPE"):
    data = json.loads(
        api.STRUCTURAL_HISTORY_BUNDLE.protocol_machine_program.canonical_bytes
    )
    data["grammar"] = "malleus.protocol-machine/private-v1"
    data["admission_rules"] = program(api.STATE_VERSION_PROFILE, match=match)[
        "admission_rules"
    ]
    return data


@pytest.mark.parametrize("match,accepted", [("EXACT", False), ("SUBTYPE", True)])
def test_public_shop_preparation_and_core_owned_checks(tmp_path, match, accepted):
    compiled = public._compiled_shop(api)
    selected = api.ProtocolMachineProgram.from_bytes(
        _canonical(structural_program(match=match))
    )
    history = api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=compiled,
        transition_program=selected,
        transaction_time=fixtures.TRANSACTION_TIME,
        actor_id="actor:test",
    )
    source = (
        public.SHOP_FIXTURE / "input/sources/supplier-order-history.jsonl"
    ).read_bytes()
    history.append_anchors(
        anchors=api.structural_source_anchors(
            content=source,
            source_id="source:supplier-order-history",
            artifact_id="artifact:supplier-order-source",
            media_type="application/jsonl",
        ),
        transaction_time=fixtures.TRANSACTION_TIME,
        actor_id="actor:test",
    )
    for occurrence in ("e4", "e7"):
        plan = public._plan(api, history.partial_contract, source, occurrence)
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=api.STATE_VERSION_PROFILE,
            retention_events=public._retention_events(api, plan, occurrence == "e4"),
            transaction_time=fixtures.TRANSACTION_TIME,
            actor_id="actor:test",
        )
        before = history.path.read_bytes()
        if occurrence == "e7" and not accepted:
            with pytest.raises(api.KnowledgeChangeRefusal) as caught:
                api.admit_structural_change(
                    history=history,
                    preparation=prepared,
                    transaction_time=fixtures.TRANSACTION_TIME,
                    actor_id="actor:test",
                )
            assert caught.value.reason.name == "TRANSITION_RULE_REFUSAL"
            assert history.path.read_bytes() == before
        else:
            api.admit_structural_change(
                history=history,
                preparation=prepared,
                transaction_time=fixtures.TRANSACTION_TIME,
                actor_id="actor:test",
            )
    replay = api.KnowledgeChangeHistory.reopen(history.path).replay()
    assert replay.graph.query("SupplierOrderState")[0]["ordered_quantity"] == (
        2 if accepted else 1
    )
    assert (
        replay.partial_contract.normative_profile.protocol_machine_program == selected
    )
    if accepted:
        assert (
            replay.record_history["supplier-order-state:B:e4"].superseded_by
            == "supplier-order-state:B:e7"
        )


def test_structural_helper_does_not_allow_other_machine_changes(tmp_path):
    compiled = public._compiled_shop(api)
    data = structural_program()
    data["events"]["ARTIFACT_REGISTERED"]["instructions"][0]["refusal"] = (
        "CHANGED_PROTOCOL"
    )
    selected = api.ProtocolMachineProgram.from_bytes(_canonical(data))
    path = tmp_path / "history.jsonl"
    with pytest.raises(api.KnowledgeChangeRefusal) as caught:
        api.create_structural_history(
            path,
            compilation=compiled,
            transition_program=selected,
            transaction_time=fixtures.TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert caught.value.reason.name == "IDENTITY_MISMATCH"
    assert not path.exists()

"""Pareto RED contract for a data-owned, generic protocol machine."""

from __future__ import annotations

import ast
from hashlib import sha256
import inspect
import json

import pytest

import malleus._contract_pipeline.machine as machine_module
from malleus._contract_pipeline.machine import (
    MachineArtifactRefusal,
    MachineArtifactRefusalReason,
    MachineState,
    NormativeAdmissionProfile,
    PartialEffectiveContract,
    PolicyProgram,
    ProtocolMachineProgram,
    ProtocolMachineProgramRefusal,
    ProtocolMachineProgramRefusalReason,
    compose_normative_profile,
    compose_partial_effective_contract,
    execute_event,
    replay_events,
)


MACHINE_GRAMMAR = "malleus.protocol-machine/private-v0"
POLICY_GRAMMAR = "malleus.policy-program/private-v0"
PROFILE_GRAMMAR = "malleus.normative-admission-profile/private-v0"
PARTIAL_EFFECTIVE_CONTRACT_GRAMMAR = "malleus.partial-effective-contract/private-v0"
VALIDATED_FACT_SET_SHA256 = "sha256:" + "1" * 64
POLICY_ID = "fixture-required-check-policy"
POLICY_REF = "required-check-verdict"
CHECKS = (
    ("check-contract-a", "sha256:" + "a" * 64),
    ("check-contract-b", "sha256:" + "b" * 64),
)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def _replace_exact(value: object, replacements: dict[str, str]) -> object:
    if isinstance(value, dict):
        return {
            replacements.get(key, key): _replace_exact(item, replacements)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_replace_exact(item, replacements) for item in value]
    if isinstance(value, str):
        return replacements.get(value, value)
    return value


def _record_schema(
    id_field: str,
    fields: dict[str, str],
    *,
    input_fields: list[str] | None = None,
) -> dict[str, object]:
    return {
        "fields": fields,
        "id_field": id_field,
        "input_fields": list(fields) if input_fields is None else input_fields,
    }


def _global_id_instruction(id_field: str) -> dict[str, str]:
    return {
        "id_field": id_field,
        "opcode": "REQUIRE_GLOBAL_ID_ABSENT",
        "refusal": "GLOBAL_RECORD_ID_EXISTS",
    }


def _program_payload() -> dict[str, object]:
    return {
        "capabilities": [],
        "events": {
            "ARTIFACT_REGISTERED": {
                "instructions": [
                    _global_id_instruction("artifact_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "ArtifactRecord",
                    },
                ],
                "record_type": "ArtifactRecord",
            },
            "ATOMIC_PAIR_REGISTERED": {
                "instructions": [
                    _global_id_instruction("pair_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "AtomicPairRecord",
                    },
                    {
                        "event_field": "source_id",
                        "opcode": "REQUIRE_REFERENCED_RECORD",
                        "record_type": "SourceRecord",
                        "refusal": "UNKNOWN_REFERENCE",
                    },
                ],
                "record_type": "AtomicPairRecord",
            },
            "CHECK_RECORDED": {
                "instructions": [
                    {
                        "event_field": "proposal_id",
                        "opcode": "REQUIRE_REFERENCED_RECORD",
                        "record_type": "ProposalRecord",
                        "refusal": "UNKNOWN_REFERENCE",
                    },
                    {
                        "check_contract_id_field": "check_contract_id",
                        "check_contract_identity_field": "check_contract_identity",
                        "check_owner_field": "proposal_id",
                        "check_policy_identity_field": "policy_identity",
                        "check_record_type": "CheckRecord",
                        "duplicate_refusal": "DUPLICATE_REQUIRED_CHECK_RECEIPT",
                        "invalid_outcome_refusal": "UNACCEPTED_CHECK_OUTCOME",
                        "opcode": "REQUIRE_POLICY_CHECK_OUTPUT",
                        "policy_mismatch_refusal": "POLICY_MISMATCH",
                        "policy_ref": POLICY_REF,
                        "proposal_id_field": "proposal_id",
                        "proposal_policy_identity_field": "policy_identity",
                        "proposal_record_type": "ProposalRecord",
                        "unrequired_refusal": "UNREQUIRED_CHECK_RECEIPT",
                    },
                    _global_id_instruction("receipt_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "CheckRecord",
                    },
                ],
                "record_type": "CheckRecord",
            },
            "CHANGE_PROPOSED": {
                "instructions": [
                    {
                        "event_field": "expected_machine_state_identity",
                        "opcode": "REQUIRE_MACHINE_STATE_IDENTITY",
                        "refusal": "STALE_MACHINE_STATE",
                    },
                    {
                        "opcode": "REQUIRE_PROFILE_POLICY",
                        "policy_id_field": "policy_id",
                        "policy_identity_field": "policy_identity",
                        "policy_ref": POLICY_REF,
                        "refusal": "POLICY_MISMATCH",
                    },
                    _global_id_instruction("proposal_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "ProposalRecord",
                    },
                ],
                "record_type": "ProposalRecord",
            },
            "SOURCE_REGISTERED": {
                "instructions": [
                    {
                        "event_field": "artifact_id",
                        "opcode": "REQUIRE_REFERENCED_RECORD",
                        "record_type": "ArtifactRecord",
                        "refusal": "UNKNOWN_REFERENCE",
                    },
                    _global_id_instruction("source_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "SourceRecord",
                    },
                ],
                "record_type": "SourceRecord",
            },
            "VERDICT_RECORDED": {
                "instructions": [
                    {
                        "event_field": "proposal_id",
                        "opcode": "REQUIRE_REFERENCED_RECORD",
                        "record_type": "ProposalRecord",
                        "refusal": "UNKNOWN_REFERENCE",
                    },
                    {
                        "event_field": "proposal_id",
                        "index": "decision-by-proposal",
                        "opcode": "REQUIRE_INDEX_ABSENT",
                        "refusal": "TERMINAL_DECISION_EXISTS",
                    },
                    {
                        "check_contract_id_field": "check_contract_id",
                        "check_contract_identity_field": "check_contract_identity",
                        "check_outcome_field": "outcome",
                        "check_owner_field": "proposal_id",
                        "check_policy_identity_field": "policy_identity",
                        "check_record_type": "CheckRecord",
                        "duplicate_refusal": "DUPLICATE_REQUIRED_CHECK_RECEIPT",
                        "missing_refusal": "MISSING_REQUIRED_CHECK",
                        "opcode": "SELECT_POLICY_VERDICT",
                        "policy_mismatch_refusal": "POLICY_MISMATCH",
                        "policy_ref": POLICY_REF,
                        "proposal_id_field": "proposal_id",
                        "proposal_policy_identity_field": "policy_identity",
                        "proposal_record_type": "ProposalRecord",
                        "target_field": "verdict",
                        "unrequired_refusal": "UNREQUIRED_CHECK_RECEIPT",
                    },
                    _global_id_instruction("decision_id"),
                    {
                        "opcode": "STORE_EVENT_RECORD",
                        "record_type": "DecisionRecord",
                    },
                ],
                "record_type": "DecisionRecord",
            },
        },
        "grammar": MACHINE_GRAMMAR,
        "indexes": {
            "decision-by-proposal": {
                "field": "proposal_id",
                "record_type": "DecisionRecord",
                "unique": True,
            }
        },
        "record_schemas": {
            "ArtifactRecord": _record_schema(
                "artifact_id",
                {
                    "artifact_id": "STRING",
                    "artifact_identity": "DIGEST",
                },
            ),
            "AtomicPairRecord": _record_schema(
                "pair_id",
                {"pair_id": "STRING", "source_id": "STRING"},
            ),
            "CheckRecord": _record_schema(
                "receipt_id",
                {
                    "check_contract_id": "STRING",
                    "check_contract_identity": "DIGEST",
                    "outcome": "STRING",
                    "policy_identity": "DIGEST",
                    "proposal_id": "STRING",
                    "receipt_id": "STRING",
                },
            ),
            "DecisionRecord": _record_schema(
                "decision_id",
                {
                    "decision_id": "STRING",
                    "proposal_id": "STRING",
                    "verdict": "VERDICT",
                },
                input_fields=["decision_id", "proposal_id"],
            ),
            "ProposalRecord": _record_schema(
                "proposal_id",
                {
                    "expected_machine_state_identity": "DIGEST",
                    "knowledge_change_set_identity": "DIGEST",
                    "policy_id": "STRING",
                    "policy_identity": "DIGEST",
                    "proposal_id": "STRING",
                },
            ),
            "SourceRecord": _record_schema(
                "source_id",
                {
                    "artifact_id": "STRING",
                    "source_id": "STRING",
                    "source_identity": "DIGEST",
                },
            ),
        },
    }


def _policy_payload() -> dict[str, object]:
    # This exact table is one fixture-local policy, not universal Malleus
    # semantics. The generic interpreter must execute the identified artifact.
    return {
        "grammar": POLICY_GRAMMAR,
        "outcome_verdicts": {
            "SATISFIED": "ACCEPT",
            "UNKNOWN": "DEFER",
            "VIOLATED": "REJECT",
        },
        "policy_id": POLICY_ID,
        "precedence": ["REJECT", "DEFER", "ACCEPT"],
        "required_checks": [
            {
                "check_contract_id": check_id,
                "check_contract_identity": check_identity,
            }
            for check_id, check_identity in CHECKS
        ],
    }


def _load_program(
    payload: dict[str, object] | None = None,
) -> ProtocolMachineProgram:
    return ProtocolMachineProgram.from_bytes(_canonical(payload or _program_payload()))


def _load_policy(payload: dict[str, object] | None = None) -> PolicyProgram:
    return PolicyProgram.from_bytes(_canonical(payload or _policy_payload()))


def _profile(
    machine_payload: dict[str, object] | None = None,
    policy_payload: dict[str, object] | None = None,
) -> NormativeAdmissionProfile:
    return compose_normative_profile(
        protocol_machine_program=_load_program(machine_payload),
        policy_programs={POLICY_REF: _load_policy(policy_payload)},
        capability_refs=(),
    )


def _effective(
    machine_payload: dict[str, object] | None = None,
    policy_payload: dict[str, object] | None = None,
    *,
    validated_fact_set_sha256: str = VALIDATED_FACT_SET_SHA256,
) -> PartialEffectiveContract:
    return compose_partial_effective_contract(
        validated_fact_set_sha256=validated_fact_set_sha256,
        normative_profile=_profile(machine_payload, policy_payload),
    )


def _event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def _proposal_event(
    state: MachineState,
    *,
    proposal_id: str = "proposal-a",
    policy_id: str = POLICY_ID,
    policy_identity: str | None = None,
) -> bytes:
    return _event(
        "CHANGE_PROPOSED",
        expected_machine_state_identity=state.identity,
        knowledge_change_set_identity="sha256:" + "6" * 64,
        policy_id=policy_id,
        policy_identity=policy_identity or _load_policy().identity,
        proposal_id=proposal_id,
    )


def _check_event(
    index: int,
    outcome: str,
    *,
    proposal_id: str = "proposal-a",
    receipt_id: str | None = None,
    check_contract_id: str | None = None,
    check_contract_identity: str | None = None,
    policy_identity: str | None = None,
) -> bytes:
    required_id, required_identity = CHECKS[index]
    return _event(
        "CHECK_RECORDED",
        check_contract_id=check_contract_id or required_id,
        check_contract_identity=check_contract_identity or required_identity,
        outcome=outcome,
        policy_identity=policy_identity or _load_policy().identity,
        proposal_id=proposal_id,
        receipt_id=receipt_id or f"receipt-{index}",
    )


def _apply(
    effective: PartialEffectiveContract,
    state: MachineState,
    event: bytes,
) -> MachineState:
    result = execute_event(effective, state, event)
    assert result.receipt.outcome == "APPLIED"
    assert result.receipt.refusal_code is None
    return result.state


def _assert_unchanged(result, before: MachineState) -> None:
    assert result.state.identity == before.identity
    assert result.state.canonical_bytes == before.canonical_bytes


def _proposal_state(effective: PartialEffectiveContract) -> MachineState:
    empty = MachineState.empty(effective.identity)
    return _apply(effective, empty, _proposal_event(empty))


def _program_refusal(
    payload: dict[str, object],
    reason: ProtocolMachineProgramRefusalReason,
) -> None:
    with pytest.raises(ProtocolMachineProgramRefusal) as refusal:
        _load_program(payload)
    assert refusal.value.reason is reason


def test_machine_program_is_canonical_immutable_and_capability_free() -> None:
    payload = _program_payload()
    source = _canonical(payload)
    program = ProtocolMachineProgram.from_bytes(source)

    assert program.canonical_bytes == source
    assert program.identity == _digest(source)
    assert program.capabilities == ()
    assert program.event_names == frozenset(payload["events"])
    assert program.data["indexes"]["decision-by-proposal"] == {
        "field": "proposal_id",
        "record_type": "DecisionRecord",
        "unique": True,
    }
    with pytest.raises(AttributeError):
        program.identity = "sha256:" + "0" * 64
    with pytest.raises(TypeError):
        program.data["events"]["EXTRA"] = {}

    noncanonical = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    with pytest.raises(ProtocolMachineProgramRefusal) as refusal:
        ProtocolMachineProgram.from_bytes(noncanonical)
    assert (
        refusal.value.reason is ProtocolMachineProgramRefusalReason.NONCANONICAL_PROGRAM
    )


def test_closed_program_refuses_unknown_grammar_opcode_capability_and_escape() -> None:
    payload = _program_payload()
    payload["grammar"] = "unknown"
    _program_refusal(payload, ProtocolMachineProgramRefusalReason.UNSUPPORTED_GRAMMAR)

    payload = _program_payload()
    payload["events"]["ARTIFACT_REGISTERED"]["instructions"][0]["opcode"] = (
        "UNKNOWN_OPCODE"
    )
    _program_refusal(payload, ProtocolMachineProgramRefusalReason.UNSUPPORTED_OPCODE)

    payload = _program_payload()
    payload["capabilities"] = ["CALL_PYTHON"]
    _program_refusal(
        payload, ProtocolMachineProgramRefusalReason.UNSUPPORTED_CAPABILITY
    )

    for field in ("callback", "python_expression", "profile"):
        payload = _program_payload()
        payload[field] = "forbidden"
        _program_refusal(payload, ProtocolMachineProgramRefusalReason.MALFORMED_PROGRAM)


def test_profile_and_partial_contract_bind_all_normative_identities() -> None:
    program = _load_program()
    policy = _load_policy()
    assert policy.canonical_bytes == _canonical(_policy_payload())
    assert policy.identity == _digest(policy.canonical_bytes)
    with pytest.raises(AttributeError):
        policy.identity = "sha256:" + "0" * 64

    profile = compose_normative_profile(
        protocol_machine_program=program,
        policy_programs={POLICY_REF: policy},
        capability_refs=(),
    )
    profile_payload = json.loads(profile.canonical_bytes)

    assert profile_payload == {
        "capability_refs": [],
        "grammar": PROFILE_GRAMMAR,
        "protocol_machine_program": json.loads(program.canonical_bytes),
        "protocol_machine_program_identity": program.identity,
        "policy_programs": [
            {
                "policy_program": json.loads(policy.canonical_bytes),
                "policy_program_identity": policy.identity,
                "ref": POLICY_REF,
            }
        ],
    }
    assert profile.identity == _digest(profile.canonical_bytes)
    assert NormativeAdmissionProfile.from_bytes(profile.canonical_bytes) == profile
    assert profile.capability_refs == ()

    effective = compose_partial_effective_contract(
        validated_fact_set_sha256=VALIDATED_FACT_SET_SHA256,
        normative_profile=profile,
    )
    assert json.loads(effective.canonical_bytes) == {
        "grammar": PARTIAL_EFFECTIVE_CONTRACT_GRAMMAR,
        "normative_profile": profile_payload,
        "normative_profile_identity": profile.identity,
        "validated_fact_set_sha256": VALIDATED_FACT_SET_SHA256,
    }
    assert effective.identity == _digest(effective.canonical_bytes)
    assert PartialEffectiveContract.from_bytes(effective.canonical_bytes) == effective
    with pytest.raises(AttributeError):
        effective.identity = "sha256:" + "0" * 64

    changed_policy_payload = _policy_payload()
    changed_policy_payload["precedence"] = ["DEFER", "REJECT", "ACCEPT"]
    changed_policy = _effective(policy_payload=changed_policy_payload)
    changed_contract = _effective(validated_fact_set_sha256="sha256:" + "2" * 64)
    assert (
        len({effective.identity, changed_policy.identity, changed_contract.identity})
        == 3
    )


def test_embedded_identity_tampering_and_unbound_policy_ref_refuse() -> None:
    profile_payload = json.loads(_profile().canonical_bytes)
    profile_payload["protocol_machine_program_identity"] = "sha256:" + "0" * 64
    with pytest.raises(MachineArtifactRefusal) as machine_tamper:
        NormativeAdmissionProfile.from_bytes(_canonical(profile_payload))
    assert machine_tamper.value.reason is MachineArtifactRefusalReason.IDENTITY_MISMATCH

    profile_payload = json.loads(_profile().canonical_bytes)
    profile_payload["policy_programs"][0]["policy_program_identity"] = (
        "sha256:" + "0" * 64
    )
    with pytest.raises(MachineArtifactRefusal) as policy_tamper:
        NormativeAdmissionProfile.from_bytes(_canonical(profile_payload))
    assert policy_tamper.value.reason is MachineArtifactRefusalReason.IDENTITY_MISMATCH

    partial_payload = json.loads(_effective().canonical_bytes)
    partial_payload["normative_profile_identity"] = "sha256:" + "0" * 64
    with pytest.raises(MachineArtifactRefusal) as profile_tamper:
        PartialEffectiveContract.from_bytes(_canonical(partial_payload))
    assert profile_tamper.value.reason is MachineArtifactRefusalReason.IDENTITY_MISMATCH

    program_payload = _replace_exact(
        _program_payload(), {POLICY_REF: "unbound-policy-ref"}
    )
    with pytest.raises(MachineArtifactRefusal) as unbound:
        compose_normative_profile(
            protocol_machine_program=_load_program(program_payload),
            policy_programs={POLICY_REF: _load_policy()},
            capability_refs=(),
        )
    assert unbound.value.reason is MachineArtifactRefusalReason.UNBOUND_POLICY_REFERENCE


def test_generic_interpreter_has_no_profile_names_or_arbitrary_code_escape() -> None:
    source = inspect.getsource(machine_module)
    tree = ast.parse(source)
    fixture_literals = {
        "ARTIFACT_REGISTERED",
        "ATOMIC_PAIR_REGISTERED",
        "CHECK_RECORDED",
        "CHANGE_PROPOSED",
        "SOURCE_REGISTERED",
        "VERDICT_RECORDED",
        "ArtifactRecord",
        "AtomicPairRecord",
        "CheckRecord",
        "DecisionRecord",
        "ProposalRecord",
        "SourceRecord",
        "StoredObject",
        POLICY_ID,
        POLICY_REF,
        "OBJECT_ID_EXISTS",
        "OBJECT_RETAINED",
        "artifact_id",
        "artifact_identity",
        "check-contract-a",
        "check-contract-b",
        "check_contract_id",
        "check_contract_identity",
        "decision_id",
        "decision-by-proposal",
        "expected_machine_state_identity",
        "knowledge_change_set_identity",
        "outcome",
        "object_id",
        "object_identity",
        "pair_id",
        "policy_id",
        "policy_identity",
        "proposal_id",
        "receipt_id",
        "source_id",
        "source_identity",
        "verdict",
        "DUPLICATE_REQUIRED_CHECK_RECEIPT",
        "GLOBAL_RECORD_ID_EXISTS",
        "MISSING_REQUIRED_CHECK",
        "POLICY_MISMATCH",
        "STALE_MACHINE_STATE",
        "TERMINAL_DECISION_EXISTS",
        "UNACCEPTED_CHECK_OUTCOME",
        "UNKNOWN_REFERENCE",
        "UNREQUIRED_CHECK_RECEIPT",
    }
    fixture_literals.update(identity for _, identity in CHECKS)
    string_literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }

    assert fixture_literals.isdisjoint(string_literals)
    assert {"eval", "exec", "compile", "__import__"}.isdisjoint(called_names)
    assert {"KnowledgeGraph", "KnowledgeChangeSet"}.isdisjoint(loaded_names)
    assert tuple(inspect.signature(execute_event).parameters) == (
        "partial_contract",
        "state",
        "event_bytes",
    )
    assert tuple(inspect.signature(replay_events).parameters) == (
        "partial_contract",
        "event_bytes",
    )
    for forbidden in ("callback", "handler", "policy", "profile"):
        assert forbidden not in inspect.signature(execute_event).parameters
        assert forbidden not in inspect.signature(replay_events).parameters


def test_registration_vocabulary_and_refusal_are_machine_data() -> None:
    renamed = _replace_exact(
        _program_payload(),
        {
            "ARTIFACT_REGISTERED": "OBJECT_RETAINED",
            "ArtifactRecord": "StoredObject",
            "artifact_id": "object_id",
            "artifact_identity": "object_identity",
        },
    )
    assert isinstance(renamed, dict)
    renamed["events"]["OBJECT_RETAINED"]["instructions"][0]["refusal"] = (
        "OBJECT_ID_EXISTS"
    )
    partial_contract = _effective(machine_payload=renamed)
    empty = MachineState.empty(partial_contract.identity)
    event = _event(
        "OBJECT_RETAINED",
        object_id="object-a",
        object_identity="sha256:" + "3" * 64,
    )
    recorded = execute_event(partial_contract, empty, event)

    assert recorded.receipt.outcome == "APPLIED"
    assert recorded.state.get_record("StoredObject", "object-a") == {
        "object_id": "object-a",
        "object_identity": "sha256:" + "3" * 64,
    }
    duplicate = execute_event(partial_contract, recorded.state, event)
    assert duplicate.receipt.refusal_code == "OBJECT_ID_EXISTS"
    _assert_unchanged(duplicate, recorded.state)


def test_artifact_source_and_global_record_identity_are_atomic() -> None:
    effective = _effective()
    empty = MachineState.empty(effective.identity)
    artifact = _event(
        "ARTIFACT_REGISTERED",
        artifact_id="shared-id",
        artifact_identity="sha256:" + "3" * 64,
    )
    registered = execute_event(effective, empty, artifact)

    assert registered.receipt.outcome == "APPLIED"
    assert empty.get_record("ArtifactRecord", "shared-id") is None
    assert registered.state.get_record("ArtifactRecord", "shared-id") == {
        "artifact_id": "shared-id",
        "artifact_identity": "sha256:" + "3" * 64,
    }

    duplicate = execute_event(effective, registered.state, artifact)
    assert duplicate.receipt.refusal_code == "GLOBAL_RECORD_ID_EXISTS"
    _assert_unchanged(duplicate, registered.state)

    cross_type = execute_event(
        effective,
        registered.state,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="shared-id",
            source_id="shared-id",
            source_identity="sha256:" + "4" * 64,
        ),
    )
    assert cross_type.receipt.refusal_code == "GLOBAL_RECORD_ID_EXISTS"
    _assert_unchanged(cross_type, registered.state)
    assert cross_type.state.get_record("SourceRecord", "shared-id") is None

    sourced = execute_event(
        effective,
        registered.state,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="shared-id",
            source_id="source-a",
            source_identity="sha256:" + "4" * 64,
        ),
    )
    assert sourced.receipt.outcome == "APPLIED"
    assert sourced.state.get_record("SourceRecord", "source-a") == {
        "artifact_id": "shared-id",
        "source_id": "source-a",
        "source_identity": "sha256:" + "4" * 64,
    }


def test_future_change_is_opaque_and_proposal_pins_the_exact_policy() -> None:
    effective = _effective()
    empty = MachineState.empty(effective.identity)
    proposal_state = _apply(effective, empty, _proposal_event(empty))

    assert proposal_state.get_record("ProposalRecord", "proposal-a") == {
        "expected_machine_state_identity": empty.identity,
        "knowledge_change_set_identity": "sha256:" + "6" * 64,
        "policy_id": POLICY_ID,
        "policy_identity": _load_policy().identity,
        "proposal_id": "proposal-a",
    }
    assert not hasattr(machine_module, "KnowledgeChangeSet")

    wrong_policy = execute_event(
        effective,
        proposal_state,
        _proposal_event(
            proposal_state,
            proposal_id="proposal-wrong-policy",
            policy_identity="sha256:" + "0" * 64,
        ),
    )
    assert wrong_policy.receipt.refusal_code == "POLICY_MISMATCH"
    _assert_unchanged(wrong_policy, proposal_state)

    wrong_policy_id = execute_event(
        effective,
        proposal_state,
        _proposal_event(
            proposal_state,
            proposal_id="proposal-wrong-policy-id",
            policy_id="wrong-policy-id",
        ),
    )
    assert wrong_policy_id.receipt.refusal_code == "POLICY_MISMATCH"
    _assert_unchanged(wrong_policy_id, proposal_state)

    stale = execute_event(
        effective,
        proposal_state,
        _event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity="sha256:" + "0" * 64,
            knowledge_change_set_identity="sha256:" + "7" * 64,
            policy_id=POLICY_ID,
            policy_identity=_load_policy().identity,
            proposal_id="proposal-stale",
        ),
    )
    assert stale.receipt.refusal_code == "STALE_MACHINE_STATE"
    _assert_unchanged(stale, proposal_state)


@pytest.mark.parametrize(
    ("outcomes", "expected"),
    [
        (("SATISFIED", "SATISFIED"), "ACCEPT"),
        (("SATISFIED", "VIOLATED"), "REJECT"),
        (("SATISFIED", "UNKNOWN"), "DEFER"),
        (("VIOLATED", "UNKNOWN"), "REJECT"),
    ],
)
def test_verdict_comes_from_the_exact_policy_program(
    outcomes: tuple[str, str], expected: str
) -> None:
    effective = _effective()
    state = _proposal_state(effective)
    for index, outcome in enumerate(outcomes):
        state = _apply(effective, state, _check_event(index, outcome))
    decided = execute_event(
        effective,
        state,
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-a",
            proposal_id="proposal-a",
        ),
    )

    assert decided.receipt.outcome == "APPLIED"
    assert decided.state.get_record("DecisionRecord", "decision-a") == {
        "decision_id": "decision-a",
        "proposal_id": "proposal-a",
        "verdict": expected,
    }


def test_missing_extra_duplicate_and_policy_mismatched_checks_refuse() -> None:
    effective = _effective()

    missing_state = _proposal_state(effective)
    missing_state = _apply(effective, missing_state, _check_event(0, "SATISFIED"))
    missing = execute_event(
        effective,
        missing_state,
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-missing",
            proposal_id="proposal-a",
        ),
    )
    assert missing.receipt.refusal_code == "MISSING_REQUIRED_CHECK"
    _assert_unchanged(missing, missing_state)
    assert missing.state.get_record("DecisionRecord", "decision-missing") is None

    proposal_state = _proposal_state(effective)
    extra = execute_event(
        effective,
        proposal_state,
        _check_event(
            0,
            "SATISFIED",
            check_contract_id="unrequired-check",
            check_contract_identity="sha256:" + "c" * 64,
            receipt_id="receipt-extra",
        ),
    )
    assert extra.receipt.refusal_code == "UNREQUIRED_CHECK_RECEIPT"
    _assert_unchanged(extra, proposal_state)

    one_check = _apply(effective, proposal_state, _check_event(0, "SATISFIED"))
    duplicate = execute_event(
        effective,
        one_check,
        _check_event(0, "SATISFIED", receipt_id="receipt-duplicate"),
    )
    assert duplicate.receipt.refusal_code == "DUPLICATE_REQUIRED_CHECK_RECEIPT"
    _assert_unchanged(duplicate, one_check)

    mismatched = execute_event(
        effective,
        one_check,
        _check_event(
            1,
            "SATISFIED",
            policy_identity="sha256:" + "0" * 64,
        ),
    )
    assert mismatched.receipt.refusal_code == "POLICY_MISMATCH"
    _assert_unchanged(mismatched, one_check)

    wrong_contract_identity = execute_event(
        effective,
        one_check,
        _check_event(
            1,
            "SATISFIED",
            check_contract_identity="sha256:" + "0" * 64,
        ),
    )
    assert wrong_contract_identity.receipt.refusal_code == "POLICY_MISMATCH"
    _assert_unchanged(wrong_contract_identity, one_check)

    invalid_outcome = execute_event(
        effective,
        one_check,
        _check_event(1, "UNACCEPTED"),
    )
    assert invalid_outcome.receipt.refusal_code == "UNACCEPTED_CHECK_OUTCOME"
    _assert_unchanged(invalid_outcome, one_check)


def test_receipt_for_another_proposal_does_not_satisfy_required_coverage() -> None:
    effective = _effective()
    state = _proposal_state(effective)
    state = _apply(
        effective,
        state,
        _proposal_event(state, proposal_id="proposal-b"),
    )
    for index in range(len(CHECKS)):
        state = _apply(
            effective,
            state,
            _check_event(index, "SATISFIED", proposal_id="proposal-b"),
        )
    result = execute_event(
        effective,
        state,
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-a",
            proposal_id="proposal-a",
        ),
    )

    assert result.receipt.refusal_code == "MISSING_REQUIRED_CHECK"
    _assert_unchanged(result, state)
    assert result.state.get_record("DecisionRecord", "decision-a") is None


def test_policy_data_controls_verdict_and_terminal_decision_is_unique() -> None:
    policy_payload = _policy_payload()
    policy_payload["precedence"] = ["DEFER", "REJECT", "ACCEPT"]
    effective = _effective(policy_payload=policy_payload)
    policy_identity = _load_policy(policy_payload).identity
    empty = MachineState.empty(effective.identity)
    state = _apply(
        effective,
        empty,
        _proposal_event(empty, policy_identity=policy_identity),
    )
    for index, outcome in enumerate(("VIOLATED", "UNKNOWN")):
        state = _apply(
            effective,
            state,
            _check_event(index, outcome, policy_identity=policy_identity),
        )
    decided = _apply(
        effective,
        state,
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-a",
            proposal_id="proposal-a",
        ),
    )
    assert decided.get_record("DecisionRecord", "decision-a")["verdict"] == "DEFER"

    second = execute_event(
        effective,
        decided,
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-b",
            proposal_id="proposal-a",
        ),
    )
    assert second.receipt.refusal_code == "TERMINAL_DECISION_EXISTS"
    _assert_unchanged(second, decided)
    assert second.state.get_record("DecisionRecord", "decision-b") is None


def test_effects_are_staged_and_failure_rolls_back_the_whole_event() -> None:
    effective = _effective()
    empty = MachineState.empty(effective.identity)
    result = execute_event(
        effective,
        empty,
        _event(
            "ATOMIC_PAIR_REGISTERED",
            pair_id="pair-a",
            source_id="absent",
        ),
    )

    assert result.receipt.outcome == "REFUSED"
    assert result.receipt.refusal_code == "UNKNOWN_REFERENCE"
    _assert_unchanged(result, empty)
    assert result.state.get_record("AtomicPairRecord", "pair-a") is None


def test_unknown_or_malformed_event_refuses_without_state_change() -> None:
    effective = _effective()
    empty = MachineState.empty(effective.identity)
    cases = (
        (_event("UNKNOWN_EVENT", value="x"), "UNKNOWN_EVENT"),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="artifact-a",
                artifact_identity="sha256:" + "3" * 64,
                extra="x",
            ),
            "MALFORMED_EVENT",
        ),
        (
            json.dumps(
                {
                    "event_type": "ARTIFACT_REGISTERED",
                    "payload": {
                        "artifact_id": "artifact-a",
                        "artifact_identity": "sha256:" + "3" * 64,
                    },
                },
                indent=2,
                sort_keys=True,
            ).encode("utf-8"),
            "NONCANONICAL_EVENT",
        ),
    )

    for event_bytes, refusal_code in cases:
        result = execute_event(effective, empty, event_bytes)
        assert result.receipt.outcome == "REFUSED"
        assert result.receipt.refusal_code == refusal_code
        _assert_unchanged(result, empty)


def test_replay_is_deterministic_from_empty_immutable_state() -> None:
    effective = _effective()
    empty = MachineState.empty(effective.identity)
    prefix_events = (
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="artifact-a",
            artifact_identity="sha256:" + "3" * 64,
        ),
        _event(
            "SOURCE_REGISTERED",
            artifact_id="artifact-a",
            source_id="source-a",
            source_identity="sha256:" + "4" * 64,
        ),
    )
    prefix = replay_events(effective, prefix_events)
    proposal = _event(
        "CHANGE_PROPOSED",
        expected_machine_state_identity=prefix.state.identity,
        knowledge_change_set_identity="sha256:" + "6" * 64,
        policy_id=POLICY_ID,
        policy_identity=_load_policy().identity,
        proposal_id="proposal-a",
    )
    events = (
        *prefix_events,
        proposal,
        _check_event(0, "SATISFIED"),
        _check_event(1, "SATISFIED"),
        _event(
            "VERDICT_RECORDED",
            decision_id="decision-a",
            proposal_id="proposal-a",
        ),
    )

    first = replay_events(effective, events)
    second = replay_events(effective, events)

    assert (
        empty.canonical_bytes == MachineState.empty(effective.identity).canonical_bytes
    )
    assert first.state.canonical_bytes == second.state.canonical_bytes
    assert first.state.identity == second.state.identity
    assert tuple(receipt.canonical_bytes for receipt in first.receipts) == tuple(
        receipt.canonical_bytes for receipt in second.receipts
    )
    assert all(receipt.outcome == "APPLIED" for receipt in first.receipts)

"""Private data-driven protocol-machine experiment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Mapping


_MACHINE_GRAMMAR = "malleus.protocol-machine/private-v0"
_POLICY_GRAMMAR = "malleus.policy-program/private-v0"
_PROFILE_GRAMMAR = "malleus.normative-admission-profile/private-v0"
_PARTIAL_CONTRACT_GRAMMAR = "malleus.partial-effective-contract/private-v0"
_HEX = frozenset("0123456789abcdef")
_VERDICTS = frozenset({"ACCEPT", "CONTEST", "DEFER", "REJECT"})


class ProtocolMachineProgramRefusalReason(Enum):
    MALFORMED_PROGRAM = auto()
    UNSUPPORTED_GRAMMAR = auto()
    UNSUPPORTED_OPCODE = auto()
    UNSUPPORTED_CAPABILITY = auto()
    NONCANONICAL_PROGRAM = auto()


class ProtocolMachineProgramRefusal(ValueError):
    def __init__(
        self, reason: ProtocolMachineProgramRefusalReason, detail: str
    ) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


class MachineArtifactRefusalReason(Enum):
    MALFORMED_ARTIFACT = auto()
    UNSUPPORTED_GRAMMAR = auto()
    UNSUPPORTED_CAPABILITY = auto()
    NONCANONICAL_ARTIFACT = auto()
    IDENTITY_MISMATCH = auto()
    UNBOUND_POLICY_REFERENCE = auto()


class MachineArtifactRefusal(ValueError):
    def __init__(self, reason: MachineArtifactRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


class _DecodeProblem(ValueError):
    def __init__(self, detail: str, *, noncanonical: bool = False) -> None:
        self.detail = detail
        self.noncanonical = noncanonical
        super().__init__(detail)


class _ExecutionRefusal(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _canonical(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as error:
        raise _DecodeProblem("value is not canonical JSON") from error


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.startswith("sha256:")
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _decode(source: bytes) -> dict[str, object]:
    if not isinstance(source, bytes):
        raise _DecodeProblem("artifact input must be bytes")

    def reject_constant(value: str) -> None:
        raise _DecodeProblem(f"non-finite JSON constant: {value}")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        answer: dict[str, object] = {}
        for key, value in pairs:
            if key in answer:
                raise _DecodeProblem(f"duplicate JSON key: {key}")
            answer[key] = value
        return answer

    try:
        text = source.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except _DecodeProblem:
        raise
    except (UnicodeError, json.JSONDecodeError) as error:
        raise _DecodeProblem("malformed JSON") from error
    if not isinstance(value, dict):
        raise _DecodeProblem("artifact root must be an object")
    if _canonical(value) != source:
        raise _DecodeProblem("artifact bytes are not canonical", noncanonical=True)
    return value


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _object(value: object, detail: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(detail)
    return value


def _array(value: object, detail: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(detail)
    return value


def _text(value: object, detail: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(detail)
    return value


_ROOT_FIELDS = frozenset(
    {"capabilities", "events", "grammar", "indexes", "record_schemas"}
)
_RECORD_SCHEMA_FIELDS = frozenset({"fields", "id_field", "input_fields"})
_EVENT_FIELDS = frozenset({"instructions", "record_type"})
_INDEX_FIELDS = frozenset({"field", "record_type", "unique"})
_FIELD_TYPES = frozenset({"DIGEST", "STRING", "VERDICT"})
_INSTRUCTION_FIELDS = {
    "REQUIRE_GLOBAL_ID_ABSENT": frozenset({"id_field", "opcode", "refusal"}),
    "STORE_EVENT_RECORD": frozenset({"opcode", "record_type"}),
    "REQUIRE_REFERENCED_RECORD": frozenset(
        {"event_field", "opcode", "record_type", "refusal"}
    ),
    "REQUIRE_MACHINE_STATE_IDENTITY": frozenset({"event_field", "opcode", "refusal"}),
    "REQUIRE_PROFILE_POLICY": frozenset(
        {
            "opcode",
            "policy_id_field",
            "policy_identity_field",
            "policy_ref",
            "refusal",
        }
    ),
    "REQUIRE_INDEX_ABSENT": frozenset({"event_field", "index", "opcode", "refusal"}),
    "REQUIRE_POLICY_CHECK_OUTPUT": frozenset(
        {
            "check_contract_id_field",
            "check_contract_identity_field",
            "check_outcome_field",
            "check_owner_field",
            "check_policy_identity_field",
            "check_record_type",
            "duplicate_refusal",
            "invalid_outcome_refusal",
            "opcode",
            "policy_mismatch_refusal",
            "policy_ref",
            "proposal_id_field",
            "proposal_policy_identity_field",
            "proposal_record_type",
            "unrequired_refusal",
        }
    ),
    "SELECT_POLICY_VERDICT": frozenset(
        {
            "check_contract_id_field",
            "check_contract_identity_field",
            "check_outcome_field",
            "check_owner_field",
            "check_policy_identity_field",
            "check_record_type",
            "duplicate_refusal",
            "invalid_outcome_refusal",
            "missing_refusal",
            "opcode",
            "policy_mismatch_refusal",
            "policy_ref",
            "proposal_id_field",
            "proposal_policy_identity_field",
            "proposal_record_type",
            "target_field",
            "unrequired_refusal",
        }
    ),
}

_OPERAND_ROLES = {
    "REQUIRE_GLOBAL_ID_ABSENT": (("id_field", "event_id"),),
    "STORE_EVENT_RECORD": (("record_type", "event_record_type"),),
    "REQUIRE_REFERENCED_RECORD": (
        ("event_field", "event_input"),
        ("record_type", "record_type"),
    ),
    "REQUIRE_MACHINE_STATE_IDENTITY": (("event_field", "event_input"),),
    "REQUIRE_PROFILE_POLICY": (
        ("policy_id_field", "event_input"),
        ("policy_identity_field", "event_input"),
        ("policy_ref", "policy_ref"),
    ),
    "REQUIRE_INDEX_ABSENT": (
        ("event_field", "event_input"),
        ("index", "index"),
    ),
    "REQUIRE_POLICY_CHECK_OUTPUT": (
        ("check_record_type", "event_record_type"),
        ("proposal_record_type", "record_type"),
        ("check_contract_id_field", "check_input"),
        ("check_contract_identity_field", "check_input"),
        ("check_outcome_field", "check_input"),
        ("check_owner_field", "check_input"),
        ("check_policy_identity_field", "check_input"),
        ("proposal_id_field", "bound_record_id"),
        ("proposal_policy_identity_field", "proposal_field"),
        ("policy_ref", "policy_ref"),
    ),
    "SELECT_POLICY_VERDICT": (
        ("check_record_type", "record_type"),
        ("proposal_record_type", "record_type"),
        ("check_contract_id_field", "check_field"),
        ("check_contract_identity_field", "check_field"),
        ("check_outcome_field", "check_field"),
        ("check_owner_field", "check_and_event_input"),
        ("check_policy_identity_field", "check_field"),
        ("proposal_id_field", "bound_record_id"),
        ("proposal_policy_identity_field", "proposal_field"),
        ("target_field", "derived_field"),
        ("policy_ref", "policy_ref"),
    ),
}


def _resolve_operands(
    instruction: dict[str, object],
    event_record_type: str,
    schemas: dict[str, object],
    indexes: dict[str, object],
) -> frozenset[str]:
    event_schema = _object(schemas[event_record_type], "event schema is malformed")
    event_fields = set(_object(event_schema["fields"], "event fields are malformed"))
    event_inputs = set(
        _array(event_schema["input_fields"], "event inputs are malformed")
    )

    def record_fields(key: str, *, inputs: bool = False) -> set[object]:
        record_type = instruction[key]
        if record_type not in schemas:
            raise ValueError("instruction references an unknown record type")
        schema = _object(schemas[record_type], "record schema is malformed")
        name = "input_fields" if inputs else "fields"
        values = schema[name]
        return set(values if isinstance(values, (dict, list)) else ())

    refs: set[str] = set()
    for key, role in _OPERAND_ROLES[instruction["opcode"]]:
        value = instruction[key]
        resolved = False
        if role == "event_id":
            resolved = value == event_schema["id_field"] and value in event_inputs
        elif role == "event_record_type":
            resolved = value == event_record_type
        elif role == "event_input":
            resolved = value in event_inputs
        elif role == "derived_field":
            resolved = value in event_fields and value not in event_inputs
        elif role == "record_type":
            resolved = value in schemas
        elif role == "index":
            resolved = value in indexes
        elif role == "check_input":
            resolved = value in event_inputs and value in record_fields(
                "check_record_type", inputs=True
            )
        elif role == "check_field":
            resolved = value in record_fields("check_record_type")
        elif role == "check_and_event_input":
            resolved = value in event_inputs and value in record_fields(
                "check_record_type"
            )
        elif role == "bound_record_id":
            proposal = _object(
                schemas[instruction["proposal_record_type"]],
                "proposal schema is malformed",
            )
            resolved = value == proposal["id_field"]
        elif role == "proposal_field":
            resolved = value in record_fields("proposal_record_type")
        elif role == "policy_ref":
            refs.add(value)
            resolved = True
        if not resolved:
            raise ValueError(f"unresolved {instruction['opcode']} operand: {key}")
    return frozenset(refs)


def _validate_machine(data: dict[str, object]) -> frozenset[str]:
    if set(data) != _ROOT_FIELDS:
        raise ValueError("machine root fields are not closed")
    if data.get("grammar") != _MACHINE_GRAMMAR:
        raise ProtocolMachineProgramRefusal(
            ProtocolMachineProgramRefusalReason.UNSUPPORTED_GRAMMAR,
            "unsupported machine grammar",
        )
    capabilities = _array(data["capabilities"], "capabilities must be an array")
    if capabilities:
        raise ProtocolMachineProgramRefusal(
            ProtocolMachineProgramRefusalReason.UNSUPPORTED_CAPABILITY,
            "this private slice declares no capabilities",
        )

    schemas = _object(data["record_schemas"], "record_schemas must be an object")
    if not schemas:
        raise ValueError("at least one record schema is required")
    for name, raw_schema in schemas.items():
        _text(name, "record type must be a string")
        schema = _object(raw_schema, "record schema must be an object")
        if set(schema) != _RECORD_SCHEMA_FIELDS:
            raise ValueError("record schema fields are not closed")
        fields = _object(schema["fields"], "record fields must be an object")
        if not fields:
            raise ValueError("record fields cannot be empty")
        for field_name, field_type in fields.items():
            _text(field_name, "field name must be a string")
            if field_type not in _FIELD_TYPES:
                raise ValueError("unsupported field type")
        identifier = _text(schema["id_field"], "id_field must be a string")
        inputs = _array(schema["input_fields"], "input_fields must be an array")
        if identifier not in fields or not all(item in fields for item in inputs):
            raise ValueError("record field reference is not declared")
        if len(inputs) != len(set(inputs)):
            raise ValueError("input fields must be unique")

    indexes = _object(data["indexes"], "indexes must be an object")
    for name, raw_index in indexes.items():
        _text(name, "index name must be a string")
        index = _object(raw_index, "index must be an object")
        if set(index) != _INDEX_FIELDS or index["unique"] is not True:
            raise ValueError("index definition is malformed")
        record_type = _text(index["record_type"], "index record type is required")
        field = _text(index["field"], "index field is required")
        if record_type not in schemas or field not in schemas[record_type]["fields"]:
            raise ValueError("index references an unknown record field")

    events = _object(data["events"], "events must be an object")
    if not events:
        raise ValueError("at least one event is required")
    policy_refs: set[str] = set()
    for event_name, raw_event in events.items():
        _text(event_name, "event name must be a string")
        event = _object(raw_event, "event rule must be an object")
        if set(event) != _EVENT_FIELDS:
            raise ValueError("event fields are not closed")
        record_type = _text(event["record_type"], "event record type is required")
        if record_type not in schemas:
            raise ValueError("event references an unknown record type")
        instructions = _array(
            event["instructions"], "event instructions must be an array"
        )
        if not instructions:
            raise ValueError("event instructions cannot be empty")
        stored = False
        guarded = False
        for raw_instruction in instructions:
            instruction = _object(raw_instruction, "instruction must be an object")
            opcode = _text(instruction.get("opcode"), "opcode is required")
            expected = _INSTRUCTION_FIELDS.get(opcode)
            if expected is None:
                raise ProtocolMachineProgramRefusal(
                    ProtocolMachineProgramRefusalReason.UNSUPPORTED_OPCODE,
                    f"unsupported opcode: {opcode}",
                )
            if set(instruction) != expected:
                raise ValueError("instruction fields are not closed")
            for value in instruction.values():
                if not isinstance(value, str) or not value:
                    raise ValueError("instruction values must be strings")
            policy_refs.update(
                _resolve_operands(instruction, record_type, schemas, indexes)
            )
            if opcode == "REQUIRE_GLOBAL_ID_ABSENT":
                guarded = True
            if opcode == "STORE_EVENT_RECORD":
                if not guarded:
                    raise ValueError("record store lacks its global identity guard")
                stored = True
        if not stored:
            raise ValueError("event does not store its declared record")
    return frozenset(policy_refs)


@dataclass(frozen=True, slots=True)
class ProtocolMachineProgram:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]
    capabilities: tuple[str, ...]
    event_names: frozenset[str]
    policy_refs: frozenset[str]

    @classmethod
    def from_bytes(cls, source: bytes) -> ProtocolMachineProgram:
        try:
            data = _decode(source)
        except _DecodeProblem as error:
            reason = (
                ProtocolMachineProgramRefusalReason.NONCANONICAL_PROGRAM
                if error.noncanonical
                else ProtocolMachineProgramRefusalReason.MALFORMED_PROGRAM
            )
            raise ProtocolMachineProgramRefusal(reason, error.detail) from error
        try:
            refs = _validate_machine(data)
        except ProtocolMachineProgramRefusal:
            raise
        except (KeyError, TypeError, ValueError) as error:
            raise ProtocolMachineProgramRefusal(
                ProtocolMachineProgramRefusalReason.MALFORMED_PROGRAM, str(error)
            ) from error
        return cls(
            canonical_bytes=source,
            identity=_digest(source),
            data=_freeze(data),
            capabilities=(),
            event_names=frozenset(data["events"]),
            policy_refs=refs,
        )


@dataclass(frozen=True, slots=True)
class PolicyProgram:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]
    identifier: str
    required_checks: tuple[tuple[str, str], ...]
    outcome_verdicts: Mapping[str, str]
    precedence: tuple[str, ...]

    @classmethod
    def from_bytes(cls, source: bytes) -> PolicyProgram:
        try:
            data = _decode(source)
            fixed = {"grammar", "outcome_verdicts", "precedence", "required_checks"}
            identifier_keys = set(data).difference(fixed)
            if (
                set(data).difference(identifier_keys) != fixed
                or len(identifier_keys) != 1
            ):
                raise ValueError("policy fields are not closed")
            if data["grammar"] != _POLICY_GRAMMAR:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.UNSUPPORTED_GRAMMAR,
                    "unsupported policy grammar",
                )
            identifier_key = next(iter(identifier_keys))
            identifier = _text(data[identifier_key], "policy identifier is required")
            mappings = _object(
                data["outcome_verdicts"], "outcome mapping must be an object"
            )
            if not mappings or not all(
                isinstance(key, str)
                and key
                and isinstance(value, str)
                and value in _VERDICTS
                for key, value in mappings.items()
            ):
                raise ValueError("outcome mapping is malformed")
            precedence = _array(data["precedence"], "precedence must be an array")
            if len(precedence) != len(set(precedence)) or set(precedence) != set(
                mappings.values()
            ):
                raise ValueError("precedence must order every mapped verdict once")
            checks: list[tuple[str, str]] = []
            for raw_check in _array(
                data["required_checks"], "required_checks must be an array"
            ):
                check = _object(raw_check, "required check must be an object")
                if len(check) != 2:
                    raise ValueError("required check must bind an ID and digest")
                values = tuple(check.values())
                identities = tuple(value for value in values if _is_digest(value))
                names = tuple(
                    value
                    for value in values
                    if isinstance(value, str) and value and not _is_digest(value)
                )
                if len(identities) != 1 or len(names) != 1:
                    raise ValueError("required check must bind an ID and digest")
                checks.append((names[0], identities[0]))
            if not checks or len(checks) != len({name for name, _ in checks}):
                raise ValueError("required checks must be nonempty and unique")
        except MachineArtifactRefusal:
            raise
        except _DecodeProblem as error:
            reason = (
                MachineArtifactRefusalReason.NONCANONICAL_ARTIFACT
                if error.noncanonical
                else MachineArtifactRefusalReason.MALFORMED_ARTIFACT
            )
            raise MachineArtifactRefusal(reason, error.detail) from error
        except (KeyError, TypeError, ValueError) as error:
            raise MachineArtifactRefusal(
                MachineArtifactRefusalReason.MALFORMED_ARTIFACT, str(error)
            ) from error
        return cls(
            canonical_bytes=source,
            identity=_digest(source),
            data=_freeze(data),
            identifier=identifier,
            required_checks=tuple(checks),
            outcome_verdicts=MappingProxyType(dict(mappings)),
            precedence=tuple(precedence),
        )


@dataclass(frozen=True, slots=True)
class NormativeAdmissionProfile:
    canonical_bytes: bytes
    identity: str
    protocol_machine_program: ProtocolMachineProgram
    policy_programs: tuple[tuple[str, PolicyProgram], ...]
    capability_refs: tuple[str, ...]

    def policy(self, reference: str) -> PolicyProgram:
        for candidate, program in self.policy_programs:
            if candidate == reference:
                return program
        raise KeyError(reference)

    @classmethod
    def from_bytes(cls, source: bytes) -> NormativeAdmissionProfile:
        try:
            data = _decode(source)
            expected = {
                "capability_refs",
                "grammar",
                "protocol_machine_program",
                "protocol_machine_program_identity",
                "policy_programs",
            }
            if set(data) != expected:
                raise ValueError("profile fields are not closed")
            if data["grammar"] != _PROFILE_GRAMMAR:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.UNSUPPORTED_GRAMMAR,
                    "unsupported profile grammar",
                )
            capabilities = _array(
                data["capability_refs"], "capability_refs must be an array"
            )
            if capabilities:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.UNSUPPORTED_CAPABILITY,
                    "this private slice declares no capabilities",
                )
            machine = ProtocolMachineProgram.from_bytes(
                _canonical(data["protocol_machine_program"])
            )
            if data["protocol_machine_program_identity"] != machine.identity:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.IDENTITY_MISMATCH,
                    "embedded machine identity does not match",
                )
            policies: dict[str, PolicyProgram] = {}
            for raw_binding in _array(
                data["policy_programs"], "policy_programs must be an array"
            ):
                binding = _object(raw_binding, "policy binding must be an object")
                if set(binding) != {
                    "policy_program",
                    "policy_program_identity",
                    "ref",
                }:
                    raise ValueError("policy binding fields are not closed")
                reference = _text(binding["ref"], "policy reference is required")
                if reference in policies:
                    raise ValueError("policy references must be unique")
                program = PolicyProgram.from_bytes(
                    _canonical(binding["policy_program"])
                )
                if binding["policy_program_identity"] != program.identity:
                    raise MachineArtifactRefusal(
                        MachineArtifactRefusalReason.IDENTITY_MISMATCH,
                        "embedded policy identity does not match",
                    )
                policies[reference] = program
            rebuilt = compose_normative_profile(
                protocol_machine_program=machine,
                policy_programs=policies,
                capability_refs=(),
            )
            if rebuilt.canonical_bytes != source:
                raise ValueError("profile order or content is not canonical")
            return rebuilt
        except MachineArtifactRefusal:
            raise
        except _DecodeProblem as error:
            reason = (
                MachineArtifactRefusalReason.NONCANONICAL_ARTIFACT
                if error.noncanonical
                else MachineArtifactRefusalReason.MALFORMED_ARTIFACT
            )
            raise MachineArtifactRefusal(reason, error.detail) from error
        except ProtocolMachineProgramRefusal as error:
            raise MachineArtifactRefusal(
                MachineArtifactRefusalReason.MALFORMED_ARTIFACT, str(error)
            ) from error
        except (KeyError, TypeError, ValueError) as error:
            raise MachineArtifactRefusal(
                MachineArtifactRefusalReason.MALFORMED_ARTIFACT, str(error)
            ) from error


def _validated_artifact(value: object, artifact_type: type) -> object:
    if not isinstance(value, artifact_type):
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.MALFORMED_ARTIFACT,
            "content-addressed artifact has the wrong type",
        )
    try:
        rebuilt = artifact_type.from_bytes(value.canonical_bytes)
    except ValueError as error:
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.IDENTITY_MISMATCH,
            "content-addressed artifact cannot be reproduced from its bytes",
        ) from error
    if rebuilt != value:
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.IDENTITY_MISMATCH,
            "content-addressed artifact fields do not match its bytes",
        )
    return rebuilt


def compose_normative_profile(
    *,
    protocol_machine_program: ProtocolMachineProgram,
    policy_programs: Mapping[str, PolicyProgram],
    capability_refs: tuple[str, ...],
) -> NormativeAdmissionProfile:
    if capability_refs:
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.UNSUPPORTED_CAPABILITY,
            "this private slice declares no capabilities",
        )
    machine = _validated_artifact(protocol_machine_program, ProtocolMachineProgram)
    assert isinstance(machine, ProtocolMachineProgram)
    if set(policy_programs) != set(machine.policy_refs):
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.UNBOUND_POLICY_REFERENCE,
            "machine policy references must match bound policy programs",
        )
    if not all(
        isinstance(reference, str) and reference for reference in policy_programs
    ):
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.MALFORMED_ARTIFACT,
            "policy bindings are malformed",
        )
    bindings = tuple(
        sorted(
            (
                reference,
                _validated_artifact(program, PolicyProgram),
            )
            for reference, program in policy_programs.items()
        )
    )
    data = {
        "capability_refs": [],
        "grammar": _PROFILE_GRAMMAR,
        "protocol_machine_program": _thaw(machine.data),
        "protocol_machine_program_identity": machine.identity,
        "policy_programs": [
            {
                "policy_program": _thaw(program.data),
                "policy_program_identity": program.identity,
                "ref": reference,
            }
            for reference, program in bindings
        ],
    }
    source = _canonical(data)
    return NormativeAdmissionProfile(
        canonical_bytes=source,
        identity=_digest(source),
        protocol_machine_program=machine,
        policy_programs=bindings,
        capability_refs=(),
    )


@dataclass(frozen=True, slots=True)
class PartialEffectiveContract:
    canonical_bytes: bytes
    identity: str
    validated_fact_set_sha256: str
    normative_profile: NormativeAdmissionProfile

    @classmethod
    def from_bytes(cls, source: bytes) -> PartialEffectiveContract:
        try:
            data = _decode(source)
            if set(data) != {
                "grammar",
                "normative_profile",
                "normative_profile_identity",
                "validated_fact_set_sha256",
            }:
                raise ValueError("partial contract fields are not closed")
            if data["grammar"] != _PARTIAL_CONTRACT_GRAMMAR:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.UNSUPPORTED_GRAMMAR,
                    "unsupported partial contract grammar",
                )
            profile = NormativeAdmissionProfile.from_bytes(
                _canonical(data["normative_profile"])
            )
            if data["normative_profile_identity"] != profile.identity:
                raise MachineArtifactRefusal(
                    MachineArtifactRefusalReason.IDENTITY_MISMATCH,
                    "embedded profile identity does not match",
                )
            rebuilt = compose_partial_effective_contract(
                validated_fact_set_sha256=data["validated_fact_set_sha256"],
                normative_profile=profile,
            )
            if rebuilt.canonical_bytes != source:
                raise ValueError("partial contract content is not canonical")
            return rebuilt
        except MachineArtifactRefusal:
            raise
        except _DecodeProblem as error:
            reason = (
                MachineArtifactRefusalReason.NONCANONICAL_ARTIFACT
                if error.noncanonical
                else MachineArtifactRefusalReason.MALFORMED_ARTIFACT
            )
            raise MachineArtifactRefusal(reason, error.detail) from error
        except (KeyError, TypeError, ValueError) as error:
            raise MachineArtifactRefusal(
                MachineArtifactRefusalReason.MALFORMED_ARTIFACT, str(error)
            ) from error


def compose_partial_effective_contract(
    *,
    validated_fact_set_sha256: str,
    normative_profile: NormativeAdmissionProfile,
) -> PartialEffectiveContract:
    if not _is_digest(validated_fact_set_sha256):
        raise MachineArtifactRefusal(
            MachineArtifactRefusalReason.MALFORMED_ARTIFACT,
            "validated fact set digest and normative profile are required",
        )
    profile = _validated_artifact(normative_profile, NormativeAdmissionProfile)
    assert isinstance(profile, NormativeAdmissionProfile)
    data = {
        "grammar": _PARTIAL_CONTRACT_GRAMMAR,
        "normative_profile": json.loads(profile.canonical_bytes.decode("utf-8")),
        "normative_profile_identity": profile.identity,
        "validated_fact_set_sha256": validated_fact_set_sha256,
    }
    source = _canonical(data)
    return PartialEffectiveContract(
        canonical_bytes=source,
        identity=_digest(source),
        validated_fact_set_sha256=validated_fact_set_sha256,
        normative_profile=profile,
    )


@dataclass(frozen=True, slots=True)
class _StoredRecord:
    record_type: str
    record_id: str
    fields: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class MachineState:
    partial_contract_identity: str
    records: tuple[_StoredRecord, ...]
    canonical_bytes: bytes
    identity: str

    @classmethod
    def empty(cls, partial_contract_identity: str) -> MachineState:
        if not _is_digest(partial_contract_identity):
            raise ValueError("partial contract identity must be a SHA-256 digest")
        return cls._build(partial_contract_identity, ())

    @classmethod
    def _build(
        cls,
        partial_contract_identity: str,
        records: tuple[_StoredRecord, ...],
    ) -> MachineState:
        ordered = tuple(sorted(records, key=lambda record: record.record_id))
        data = {
            "contract": partial_contract_identity,
            "records": [
                {
                    "fields": _thaw(record.fields),
                    "id": record.record_id,
                    "type": record.record_type,
                }
                for record in ordered
            ],
        }
        source = _canonical(data)
        return cls(
            partial_contract_identity=partial_contract_identity,
            records=ordered,
            canonical_bytes=source,
            identity=_digest(source),
        )

    def get_record(
        self, record_type: str, record_id: str
    ) -> Mapping[str, object] | None:
        for record in self.records:
            if record.record_type == record_type and record.record_id == record_id:
                return record.fields
        return None


def _validated_state(value: object, program: ProtocolMachineProgram) -> MachineState:
    if not isinstance(value, MachineState):
        raise ValueError("machine state is required")
    if not _is_digest(value.partial_contract_identity) or not isinstance(
        value.records, tuple
    ):
        raise ValueError("machine state envelope is malformed")
    seen: set[str] = set()
    sanitized: list[_StoredRecord] = []
    schemas = program.data["record_schemas"]
    for record in value.records:
        if not isinstance(record, _StoredRecord):
            raise ValueError("machine state member is malformed")
        if (
            not isinstance(record.record_type, str)
            or not record.record_type
            or not isinstance(record.record_id, str)
            or not record.record_id
        ):
            raise ValueError("machine state record name or ID is malformed")
        if record.record_type not in schemas or record.record_id in seen:
            raise ValueError("machine state record type or ID is invalid")
        if not isinstance(record.fields, MappingProxyType):
            raise ValueError("machine state record fields are mutable")
        schema = schemas[record.record_type]
        fields = schema["fields"]
        if (
            set(record.fields) != set(fields)
            or record.fields[schema["id_field"]] != record.record_id
            or not all(
                _validate_value(field_type, record.fields[name])
                for name, field_type in fields.items()
            )
        ):
            raise ValueError("machine state record does not match its schema")
        seen.add(record.record_id)
        sanitized.append(
            _StoredRecord(
                record_type=record.record_type,
                record_id=record.record_id,
                fields=_freeze(dict(record.fields)),
            )
        )
    rebuilt = MachineState._build(value.partial_contract_identity, tuple(sanitized))
    if (
        rebuilt.canonical_bytes != value.canonical_bytes
        or rebuilt.identity != value.identity
        or rebuilt.partial_contract_identity != value.partial_contract_identity
        or tuple(record.record_id for record in rebuilt.records)
        != tuple(record.record_id for record in value.records)
    ):
        raise ValueError("machine state fields do not match its canonical identity")
    return rebuilt


@dataclass(frozen=True, slots=True)
class MachineReceipt:
    outcome: str
    refusal_code: str | None
    canonical_bytes: bytes


@dataclass(frozen=True, slots=True)
class MachineExecutionResult:
    state: MachineState
    receipt: MachineReceipt


@dataclass(frozen=True, slots=True)
class MachineReplayResult:
    state: MachineState
    receipts: tuple[MachineReceipt, ...]


def _receipt(
    result: str,
    refusal: str | None,
    before: MachineState,
    after: MachineState,
    event_bytes: bytes,
) -> MachineReceipt:
    source = _canonical(
        {
            "after": after.identity,
            "before": before.identity,
            "event": _digest(event_bytes),
            "refusal": refusal,
            "result": result,
        }
    )
    return MachineReceipt(
        outcome=result,
        refusal_code=refusal,
        canonical_bytes=source,
    )


def _record_schema(
    program: ProtocolMachineProgram, record_type: str
) -> Mapping[str, object]:
    return program.data["record_schemas"][record_type]


def _validate_value(field_type: str, value: object) -> bool:
    if field_type == "DIGEST":
        return _is_digest(value)
    if field_type == "STRING":
        return isinstance(value, str) and bool(value)
    if field_type == "VERDICT":
        return isinstance(value, str) and value in _VERDICTS
    return False


def _event_data(
    program: ProtocolMachineProgram, event_bytes: bytes
) -> tuple[Mapping[str, object], Mapping[str, object]]:
    try:
        data = _decode(event_bytes)
    except _DecodeProblem as error:
        code = "NONCANONICAL_EVENT" if error.noncanonical else "MALFORMED_EVENT"
        raise _ExecutionRefusal(code) from error
    if set(data) != {"event_type", "payload"}:
        raise _ExecutionRefusal("MALFORMED_EVENT")
    event_type = data["event_type"]
    payload = data["payload"]
    if not isinstance(event_type, str) or not isinstance(payload, dict):
        raise _ExecutionRefusal("MALFORMED_EVENT")
    if event_type not in program.data["events"]:
        raise _ExecutionRefusal("UNKNOWN_EVENT")
    rule = program.data["events"][event_type]
    schema = _record_schema(program, rule["record_type"])
    inputs = tuple(schema["input_fields"])
    if set(payload) != set(inputs):
        raise _ExecutionRefusal("MALFORMED_EVENT")
    fields = schema["fields"]
    if not all(_validate_value(fields[name], payload[name]) for name in inputs):
        raise _ExecutionRefusal("MALFORMED_EVENT")
    return MappingProxyType(payload), rule


def _find(
    records: Mapping[str, _StoredRecord], record_type: str, record_id: object
) -> _StoredRecord | None:
    if not isinstance(record_id, str):
        return None
    record = records.get(record_id)
    return record if record is not None and record.record_type == record_type else None


def _bound_policy(
    partial_contract: PartialEffectiveContract, instruction: Mapping[str, object]
) -> PolicyProgram:
    try:
        return partial_contract.normative_profile.policy(instruction["policy_ref"])
    except KeyError as error:
        raise _ExecutionRefusal("MALFORMED_EVENT") from error


def _proposal_and_policy(
    partial_contract: PartialEffectiveContract,
    records: Mapping[str, _StoredRecord],
    payload: Mapping[str, object],
    instruction: Mapping[str, object],
) -> tuple[_StoredRecord, PolicyProgram]:
    owner_field = instruction["check_owner_field"]
    proposal = _find(
        records,
        instruction["proposal_record_type"],
        payload[owner_field],
    )
    if proposal is None:
        raise _ExecutionRefusal("MALFORMED_EVENT")
    if proposal.fields[instruction["proposal_id_field"]] != proposal.record_id:
        raise _ExecutionRefusal("MALFORMED_EVENT")
    policy = _bound_policy(partial_contract, instruction)
    if (
        proposal.fields[instruction["proposal_policy_identity_field"]]
        != policy.identity
    ):
        raise _ExecutionRefusal(instruction["policy_mismatch_refusal"])
    return proposal, policy


def _check_pair(
    fields: Mapping[str, object], instruction: Mapping[str, object]
) -> tuple[object, object]:
    return (
        fields[instruction["check_contract_id_field"]],
        fields[instruction["check_contract_identity_field"]],
    )


def _require_policy_check(
    partial_contract: PartialEffectiveContract,
    records: Mapping[str, _StoredRecord],
    payload: Mapping[str, object],
    instruction: Mapping[str, object],
) -> None:
    proposal, policy = _proposal_and_policy(
        partial_contract, records, payload, instruction
    )
    if payload[instruction["check_policy_identity_field"]] != policy.identity:
        raise _ExecutionRefusal(instruction["policy_mismatch_refusal"])
    pair = _check_pair(payload, instruction)
    required_by_name = dict(policy.required_checks)
    if pair[0] not in required_by_name:
        raise _ExecutionRefusal(instruction["unrequired_refusal"])
    if required_by_name[pair[0]] != pair[1]:
        raise _ExecutionRefusal(instruction["policy_mismatch_refusal"])
    if payload[instruction["check_outcome_field"]] not in policy.outcome_verdicts:
        raise _ExecutionRefusal(instruction["invalid_outcome_refusal"])
    for record in records.values():
        if (
            record.record_type == instruction["check_record_type"]
            and record.fields[instruction["check_owner_field"]] == proposal.record_id
            and _check_pair(record.fields, instruction)[0] == pair[0]
        ):
            raise _ExecutionRefusal(instruction["duplicate_refusal"])


def _select_verdict(
    partial_contract: PartialEffectiveContract,
    records: Mapping[str, _StoredRecord],
    payload: Mapping[str, object],
    instruction: Mapping[str, object],
) -> str:
    proposal, policy = _proposal_and_policy(
        partial_contract, records, payload, instruction
    )
    required = dict(policy.required_checks)
    observed: dict[object, str] = {}
    for record in records.values():
        if (
            record.record_type != instruction["check_record_type"]
            or record.fields[instruction["check_owner_field"]] != proposal.record_id
        ):
            continue
        if record.fields[instruction["check_policy_identity_field"]] != policy.identity:
            raise _ExecutionRefusal(instruction["policy_mismatch_refusal"])
        pair = _check_pair(record.fields, instruction)
        if pair[0] not in required:
            raise _ExecutionRefusal(instruction["unrequired_refusal"])
        if required[pair[0]] != pair[1]:
            raise _ExecutionRefusal(instruction["policy_mismatch_refusal"])
        if pair[0] in observed:
            raise _ExecutionRefusal(instruction["duplicate_refusal"])
        outcome = record.fields[instruction["check_outcome_field"]]
        if not isinstance(outcome, str) or outcome not in policy.outcome_verdicts:
            raise _ExecutionRefusal(instruction["invalid_outcome_refusal"])
        observed[pair[0]] = outcome
    if set(observed) != set(required):
        raise _ExecutionRefusal(instruction["missing_refusal"])
    verdicts = {policy.outcome_verdicts[value] for value in observed.values()}
    return next(value for value in policy.precedence if value in verdicts)


def _execute_instruction(
    partial_contract: PartialEffectiveContract,
    before: MachineState,
    records: dict[str, _StoredRecord],
    payload: Mapping[str, object],
    instruction: Mapping[str, object],
    derived: dict[str, object],
) -> None:
    opcode = instruction["opcode"]
    program = partial_contract.normative_profile.protocol_machine_program
    if opcode == "REQUIRE_GLOBAL_ID_ABSENT":
        if payload[instruction["id_field"]] in records:
            raise _ExecutionRefusal(instruction["refusal"])
    elif opcode == "REQUIRE_REFERENCED_RECORD":
        if (
            _find(
                records,
                instruction["record_type"],
                payload[instruction["event_field"]],
            )
            is None
        ):
            raise _ExecutionRefusal(instruction["refusal"])
    elif opcode == "REQUIRE_MACHINE_STATE_IDENTITY":
        if payload[instruction["event_field"]] != before.identity:
            raise _ExecutionRefusal(instruction["refusal"])
    elif opcode == "REQUIRE_PROFILE_POLICY":
        policy = _bound_policy(partial_contract, instruction)
        if (
            payload[instruction["policy_id_field"]] != policy.identifier
            or payload[instruction["policy_identity_field"]] != policy.identity
        ):
            raise _ExecutionRefusal(instruction["refusal"])
    elif opcode == "REQUIRE_INDEX_ABSENT":
        index = program.data["indexes"][instruction["index"]]
        value = payload[instruction["event_field"]]
        if any(
            record.record_type == index["record_type"]
            and record.fields[index["field"]] == value
            for record in records.values()
        ):
            raise _ExecutionRefusal(instruction["refusal"])
    elif opcode == "REQUIRE_POLICY_CHECK_OUTPUT":
        _require_policy_check(partial_contract, records, payload, instruction)
    elif opcode == "SELECT_POLICY_VERDICT":
        derived[instruction["target_field"]] = _select_verdict(
            partial_contract, records, payload, instruction
        )
    elif opcode == "STORE_EVENT_RECORD":
        record_type = instruction["record_type"]
        schema = _record_schema(program, record_type)
        fields = {**payload, **derived}
        if set(fields) != set(schema["fields"]) or not all(
            _validate_value(field_type, fields[name])
            for name, field_type in schema["fields"].items()
        ):
            raise _ExecutionRefusal("MALFORMED_EVENT")
        record_id = fields[schema["id_field"]]
        records[record_id] = _StoredRecord(
            record_type=record_type,
            record_id=record_id,
            fields=_freeze(fields),
        )
    else:
        raise _ExecutionRefusal("MALFORMED_EVENT")


def execute_event(
    partial_contract: PartialEffectiveContract,
    state: MachineState,
    event_bytes: bytes,
) -> MachineExecutionResult:
    if not isinstance(event_bytes, bytes):
        raise ValueError("event input must be bytes")
    contract = _validated_artifact(partial_contract, PartialEffectiveContract)
    assert isinstance(contract, PartialEffectiveContract)
    before = _validated_state(
        state, contract.normative_profile.protocol_machine_program
    )
    if before.partial_contract_identity != contract.identity:
        raise ValueError("partial contract and machine state do not match")
    try:
        payload, rule = _event_data(
            contract.normative_profile.protocol_machine_program,
            event_bytes,
        )
        records = {record.record_id: record for record in before.records}
        derived: dict[str, object] = {}
        for instruction in rule["instructions"]:
            _execute_instruction(
                contract,
                before,
                records,
                payload,
                instruction,
                derived,
            )
        after = MachineState._build(
            before.partial_contract_identity, tuple(records.values())
        )
    except _ExecutionRefusal as refusal:
        return MachineExecutionResult(
            state=before,
            receipt=_receipt("REFUSED", refusal.code, before, before, event_bytes),
        )
    return MachineExecutionResult(
        state=after,
        receipt=_receipt("APPLIED", None, before, after, event_bytes),
    )


def replay_events(
    partial_contract: PartialEffectiveContract,
    event_bytes: tuple[bytes, ...],
) -> MachineReplayResult:
    contract = _validated_artifact(partial_contract, PartialEffectiveContract)
    assert isinstance(contract, PartialEffectiveContract)
    state = MachineState.empty(contract.identity)
    receipts: list[MachineReceipt] = []
    for source in event_bytes:
        result = execute_event(contract, state, source)
        state = result.state
        receipts.append(result.receipt)
    return MachineReplayResult(state=state, receipts=tuple(receipts))


__all__ = [
    "MachineArtifactRefusal",
    "MachineArtifactRefusalReason",
    "MachineExecutionResult",
    "MachineReceipt",
    "MachineReplayResult",
    "MachineState",
    "NormativeAdmissionProfile",
    "PartialEffectiveContract",
    "PolicyProgram",
    "ProtocolMachineProgram",
    "ProtocolMachineProgramRefusal",
    "ProtocolMachineProgramRefusalReason",
    "compose_normative_profile",
    "compose_partial_effective_contract",
    "execute_event",
    "replay_events",
]

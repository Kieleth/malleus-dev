"""Pure finite check producers. Loading local implementation resources is separate.

No history authentication, append, clock or effect capability is supplied here.
The owning history must bind these exact programs and validate their retained
outputs. It recomputes policy control, not producer execution, during replay.
"""

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import ValidationError

from malleus.compiler import load_validated_contract_artifact
from malleus.control import monitor_specification_digest
from malleus.ledger import GENESIS, canonical_json, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.executor import (
    ExecutionRefusal,
    VALUE_VALIDATOR,
    FORMATS,
    execute_program,
)
from research.action_history_contract_freeze.programs.packet_validator import (
    validate_interval,
)


HERE = Path(__file__).parent


class CheckRefusal(ValueError):
    """Malformed, misbound or unsupported check input, not a computed verdict."""


def _digest(source):
    return "sha256:" + sha256(source).hexdigest()


def _at(value, path):
    for field in path:
        value = value[field]
    return value


def _shape(value):
    """Instantiate operand shapes only. VALIDATE_RECORD still checks the ontology.

    This is not a contract inferred from example values. The fixed check steps
    and compiled contract decide validity; these shapes enable the existing
    finite path checker on one exact invocation, including extra domain slots.
    """
    if type(value) is dict:
        return {
            "type": "object",
            "properties": {k: _shape(v) for k, v in value.items()},
            "required": list(value),
            "additionalProperties": False,
        }
    if type(value) is list:
        schemas = [_shape(v) for v in value]
        if schemas and any(s != schemas[0] for s in schemas[1:]):
            raise CheckRefusal(
                "heterogeneous operand array requires an explicit variant"
            )
        return {
            "type": "array",
            "items": schemas[0] if schemas else {"type": "string"},
            "minItems": len(value),
        }
    kinds = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        type(None): "null",
    }
    if type(value) not in kinds:
        raise CheckRefusal("operand is not a JSON value")
    return {"type": kinds[type(value)]}


def _program(predicate, bindings):
    schemas = {
        root: {name: _shape(value) for name, value in names.items()}
        for root, names in bindings.items()
    }
    for step in predicate["steps"]:
        if step["opcode"] == "REQUIRE_COMPARE" and step["value_kind"] in {
            "DIGEST",
            "INSTANT",
            "HEAD",
        }:
            for side in ("left", "right"):
                operand = step[side]
                schema = schemas[operand["root"]][operand["name"]]
                for part in operand["path"]:
                    schema = (
                        schema["properties"][part]
                        if type(part) is str
                        else schema["items"]
                    )
                schema["format"] = {
                    "DIGEST": "sha256",
                    "INSTANT": "aware-instant",
                    "HEAD": "ledger-head",
                }[step["value_kind"]]
    return {
        "name": predicate["name"],
        "inputs": schemas,
        "required_capabilities": [],
        "introductions": [],
        "steps": predicate["steps"],
    }


@dataclass(frozen=True)
class CheckExecution:
    canonical_bytes: bytes

    @property
    def data(self):
        return json.loads(self.canonical_bytes)


@dataclass(frozen=True)
class CheckExecutor:
    definition_bytes: bytes
    implementation_bytes: bytes

    def __post_init__(self):
        if self.implementation_bytes != _IMPLEMENTATION_BYTES:
            raise CheckRefusal(
                "unavailable implementation: bytes do not name this loaded producer"
            )
        try:
            if type(self.definition_bytes) is not bytes:
                raise ValueError("exact definition bytes required")
            value = json.loads(self.definition_bytes)
            if canonical_json(value).encode() != self.definition_bytes:
                raise ValueError("canonical definition bytes required")
            if (
                value["rules"]["closure_order"]
                != "INVOCATION_ROLES_THEN_MONITOR_THEN_STATIC_INPUTS_FIRST_OCCURRENCE"
            ):
                raise ValueError("unsupported closure order")
        except (ValueError, KeyError, TypeError) as error:
            raise CheckRefusal(str(error)) from error

    @property
    def implementation_reference(self):
        definition = json.loads(self.definition_bytes)
        return {
            **definition["rules"]["implementation"],
            "bytes_sha256": _digest(self.implementation_bytes),
        }

    def execute(self, *, invocation, records, retained_bytes, contract_bytes):
        """Compute actual predicates and full output records without any I/O."""
        try:
            return self._execute(invocation, records, retained_bytes, contract_bytes)
        except CheckRefusal:
            raise
        except (ValueError, KeyError, TypeError, ValidationError) as error:
            raise CheckRefusal(str(error)) from error

    def _execute(self, invocation, records, retained_bytes, contract_bytes):
        invocation, records, retained_bytes = deepcopy(
            (invocation, records, retained_bytes)
        )
        definition = json.loads(self.definition_bytes)
        VALUE_VALIDATOR(
            definition["invocation_schema"], format_checker=FORMATS
        ).validate(invocation)
        if invocation["implementation"] != self.implementation_reference:
            raise CheckRefusal(
                "invocation does not identify the loaded check implementation"
            )
        if type(contract_bytes) is not bytes:
            raise CheckRefusal("exact compiled record-contract bytes required")
        view = load_validated_contract_artifact(contract_bytes)
        binding = definition["bindings"]
        kind = invocation["kind"]
        if any(not v.strip() for v in invocation["output_ids"].values()):
            raise CheckRefusal("output IDs must be nonblank")
        ids = list(invocation["output_ids"].values())
        if len(set(ids)) != len(ids) or any(i in records for i in ids):
            raise CheckRefusal("distinct unused output IDs required")

        def record(reference, root, *, check_shape=True):
            identifier = reference["id"]
            wrapper = records[identifier]
            if set(wrapper) != {"record_type", "record"}:
                raise CheckRefusal("full typed record wrapper required")
            rkind, value = wrapper["record_type"], wrapper["record"]
            rtype = view.get_type(rkind)
            if rtype.abstract or rtype.is_mixin or not view.is_subtype_of(rkind, root):
                raise CheckRefusal("record has the wrong concrete role")
            if value["id"] != identifier or value["content_hash"] != record_hash(
                rkind, value
            ):
                raise CheckRefusal("record identity differs from supplied bytes")
            if (
                "record_hash" in reference
                and reference["record_hash"] != value["content_hash"]
            ):
                raise CheckRefusal("input record reference hash differs")
            if check_shape and view.validate_instance(rkind, value):
                raise CheckRefusal("input record shape differs from contract")
            for ancestor, fields in binding["required_collections"].items():
                if view.is_subtype_of(rkind, ancestor):
                    if any(type(value[f]) is not list for f in fields):
                        raise CheckRefusal("required record collection is not a list")
            return value

        def source(reference):
            value = record(reference, binding["carrier"]["record_type"])
            content = retained_bytes[reference["id"]]
            if (
                type(content) is not bytes
                or value["artifact_kind"] != binding["carrier"]["artifact_kind"]
            ):
                raise CheckRefusal("exact SourceArtifact bytes required")
            expected = source_artifact_fields(
                artifact_id=value["id"],
                artifact_version=value["artifact_version"],
                source_bytes=content,
                media_type=value["source_media_type"],
                locator=value["source_locator"],
            )
            if any(value[k] != v for k, v in expected.items()):
                raise CheckRefusal("source bytes or semantic identity differ")
            if "bytes_sha256" in reference and reference["bytes_sha256"] != _digest(
                content
            ):
                raise CheckRefusal("input byte reference differs")
            return content

        monitor = record(invocation["monitor"], "MonitorSpecificationArtifact")
        expected_kind = definition["outputs"]["variants"][
            "type_result" if kind == "TYPE" else "authority_result"
        ]["constants"]["assessment_kind"]
        if (
            monitor["assessment_kind"] != expected_kind
            or monitor["monitor_implementation_hash"]
            != self.implementation_reference["bytes_sha256"]
        ):
            raise CheckRefusal("monitor does not bind the selected real producer")
        if monitor["artifact_hash"] != monitor_specification_digest(
            schema_version=monitor["monitor_schema_version"],
            monitor_id=monitor["id"],
            monitor_version=monitor["artifact_version"],
            assessment_kind=monitor["assessment_kind"],
            implementation_hash=monitor["monitor_implementation_hash"],
            input_artifact_ids=monitor["input_artifact_ids"],
            input_artifact_record_hashes=monitor["input_artifact_record_hashes"],
        ):
            raise CheckRefusal("monitor semantic identity differs")
        static_ids = monitor["input_artifact_ids"]
        if static_ids != sorted(set(static_ids)):
            raise CheckRefusal("canonical monitor input IDs required")
        static = [
            source({"id": i, "record_hash": h})
            for i, h in zip(
                static_ids, monitor["input_artifact_record_hashes"], strict=True
            )
        ]
        if len(static) != 2 or set(static) != {
            self.definition_bytes,
            self.implementation_bytes,
        }:
            raise CheckRefusal(
                "monitor must retain exact definition and implementation bytes"
            )
        values = {"records": {"monitor": monitor}, "inputs": {}, "contents": {}}
        inputs = {"applied_record": {}, "artifact": {}, "event": {}}
        input_ids = []
        for item in invocation["inputs"]:
            role, reference = item["role"], item["value"]
            if role in binding["scalar_inputs"]:
                values["inputs"][role] = reference
                inputs["event"][role] = {"value": reference}
                continue
            input_ids.append(reference["id"])
            if role in binding["record_inputs"]:
                value = record(
                    reference,
                    binding["record_inputs"][role],
                    check_shape=not (kind == "TYPE" and role in {"proposal", "action"}),
                )
                values["records"][role] = value
                inputs["applied_record"][role] = {"record": value}
                inputs["artifact"][role + "_contract"] = {
                    "value": {
                        "contract_identity": _digest(contract_bytes),
                        "record_type": records[reference["id"]]["record_type"],
                    }
                }
                continue
            content = source(reference)
            content_kind = binding["byte_inputs"][role]
            if content_kind == "compiled-record-contract":
                if content != contract_bytes:
                    raise CheckRefusal(
                        "TYPE record contract differs from selected bytes"
                    )
                continue
            value = json.loads(content)
            if canonical_json(value).encode() != content:
                raise CheckRefusal("input content must be canonical JSON")
            if content_kind == "interval":
                validate_interval(value)
            elif content_kind == "original-context":
                VALUE_VALIDATOR(
                    definition["contexts_schema"], format_checker=FORMATS
                ).validate(value)
                if value["schema"] != binding["content_tags"][content_kind]:
                    raise CheckRefusal("original-context variant required")
            else:
                schema = {
                    **definition["contents_schema"],
                    "$ref": f"#/$defs/{content_kind}",
                }
                VALUE_VALIDATOR(schema, format_checker=FORMATS).validate(value)
            values["contents"][role] = value
            inputs["artifact"][role] = {"value": value}
        if kind == "DIRECT_GRANT":
            grant = values["records"]["grant"]
            interval_fields = definition["rules"]["grant_interval_fields"]
            interval = {"start": grant[interval_fields["start"]]}
            if interval_fields["end"] in grant:
                interval["end"] = grant[interval_fields["end"]]
            validate_interval(interval)
            inputs["artifact"]["grant_interval"] = {"value": interval}
            inputs["artifact"]["no_subdelegation"] = {
                "value": definition["rules"]["constants"]["no_subdelegation"]
            }
            values["current"] = values["contents"]["current_context"]
        closure = list(dict.fromkeys([*input_ids, monitor["id"], *static_ids]))
        values.update(
            invocation=invocation,
            closure={"input_record_ids": closure, "source_record_ids": closure},
        )
        checked, violated, programs = [], [], []
        failure = None
        try:
            for predicate in definition["rules"][kind]:
                program = _program(predicate, inputs)
                checked.append(predicate["name"])
                programs.append(program)
                try:
                    execute_program(
                        program=program,
                        profile={"targets": {}, "capabilities": []},
                        instruction_schema=definition["instructions_schema"],
                        inputs=inputs,
                        applied_records={},
                        state={"protocol": {}, "action_acceptance_head": GENESIS},
                        record_contract_bytes=contract_bytes,
                    )
                except ExecutionRefusal as error:
                    if error.step is None or error.reason not in {
                        s["refusal"] for s in predicate["steps"]
                    }:
                        raise CheckRefusal(
                            f"check instruction cannot execute: {error}"
                        ) from error
                    violated.append(predicate["name"])
        except RuntimeError as error:
            failure = {**definition["rules"]["failure"], "error_message": str(error)}
            failure["reason_codes"] = [failure["error_code"]]
        completed = definition["rules"]["completed"]
        values["computed"] = {
            "completed": {
                "outcome": completed["violated"]
                if violated
                else completed["satisfied"],
                "reason_codes": violated if violated else [completed["success_reason"]],
                "rationale": completed["rationale"],
                "checked_predicates": checked,
                "violated_predicates": violated,
            },
            "failure": failure,
        }
        prefix = "type" if kind == "TYPE" else "authority"
        variants = (
            [prefix + "_result"]
            if failure is None
            else [prefix + "_failure", prefix + "_unavailable"]
        )
        result = []
        for name in variants:
            variant = definition["outputs"]["variants"][name]
            value = deepcopy(variant["constants"])
            groups = [definition["outputs"]["groups"][g] for g in variant["groups"]] + [
                variant["fields"]
            ]
            for group in groups:
                if value.keys() & group.keys():
                    raise CheckRefusal("output field has multiple owners")
                value.update(
                    {
                        field: deepcopy(_at(values, path))
                        for field, path in group.items()
                    }
                )
            value["content_hash"] = record_hash(variant["record_type"], value)
            if view.validate_instance(variant["record_type"], value):
                raise CheckRefusal(
                    "computed output does not conform to compiled contract"
                )
            result.append({"record_type": variant["record_type"], "record": value})
            if failure is not None and name.endswith("_failure"):
                values["closure"]["source_record_ids"] = [*closure, value["id"]]
        return CheckExecution(
            canonical_json(
                {
                    "records": result,
                    "programs": programs,
                    "definition_identity": _digest(self.definition_bytes),
                    "implementation": self.implementation_reference,
                    "runtime_executed": True,
                    "history_authenticated": False,
                }
            ).encode()
        )


def load_check_executor():
    """Load only this implementation's declared local resources, before pure use.

    The source capsule contains actual producer/kernel/checker source, not a
    specification digest standing in for an absent implementation. It is not a
    self-contained Python environment or a claim of OS-enforced code identity.
    """
    paths = {
        "bindings": "input-bindings.json",
        "invocation_schema": "invocation.schema.json",
        "contexts_schema": "../contexts.schema.json",
        "contents_schema": "contents.schema.json",
        "outputs": "monitor-output-fields.json",
        "instructions_schema": "../instructions.schema.json",
        "rules": "check-rules.json",
    }
    definition = {
        key: json.loads((HERE / path).read_bytes()) for key, path in paths.items()
    }
    return CheckExecutor(canonical_json(definition).encode(), _IMPLEMENTATION_BYTES)


# Loaded once with the implementation, not reread during a pure invocation.
# Trusted Python process, not an OS or in-memory monkeypatch attestation.
_IMPLEMENTATION_BYTES = canonical_json(
    {
        name: (HERE / name).read_text()
        for name in (
            "check_executor.py",
            "executor.py",
            "packet_validator.py",
            "control_executor.py",
        )
    }
).encode()

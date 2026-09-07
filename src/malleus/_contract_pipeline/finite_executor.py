"""Pure reference execution of the research finite instruction subset.

This kernel has no writer, clock, resolver callback or effect adapter. Its
inputs are explicit snapshots, not authenticated histories. Owning-history
integration must supply and verify those snapshots before committing a result.
"""

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError, validators

from .view import load_validated_contract_artifact
from malleus.ledger import (
    GENESIS,
    LedgerError,
    aware_datetime,
    canonical_json,
    content_digest,
    record_hash,
    require_digest,
)
from .finite_program import (
    PacketRefusal,
    validate_interval,
    validate_program,
)
from .finite_control import (
    CAPABILITIES,
    require_coverage,
    select_control,
)


class ExecutionRefusal(ValueError):
    def __init__(self, reason, detail, *, step=None):
        self.reason, self.detail, self.step = reason, detail, step
        super().__init__(f"{reason}: {detail}")


# Definition data is loaded with the installed interpreter, never fetched or
# replaced by an invocation. Pure execution below performs no I/O.
_INSTRUCTION_SCHEMA_CANONICAL = canonical_json(
    json.loads(Path(__file__).with_name("finite-instructions.json").read_bytes())
)


def validate_instruction_schema(schema):
    if canonical_json(schema) != _INSTRUCTION_SCHEMA_CANONICAL:
        raise ExecutionRefusal(
            "UNSUPPORTED_INSTRUCTION_SCHEMA",
            "the installed finite interpreter requires its exact instruction grammar",
        )


@dataclass(frozen=True)
class ProgramExecution:
    canonical_bytes: bytes

    @property
    def data(self):
        return json.loads(self.canonical_bytes)


FORMATS = FormatChecker(formats=[])
VALUE_VALIDATOR = validators.extend(
    Draft202012Validator,
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine(
        "integer", lambda checker, value: type(value) is int
    ),
)


@FORMATS.checks("sha256", raises=LedgerError)
def _digest(value):
    require_digest(value, "identity")
    return True


@FORMATS.checks("aware-instant", raises=LedgerError)
def _instant(value):
    aware_datetime(value, "instant")
    return True


@FORMATS.checks("ledger-head", raises=LedgerError)
def _head(value):
    return value == GENESIS or _digest(value)


@FORMATS.checks("nonblank")
def _nonblank(value):
    # Predicate only. The input and therefore its identity remain unchanged.
    return type(value) is str and bool(value.strip())


def _formats(schema):
    if isinstance(schema, dict):
        if (
            "type" in schema
            and type(schema["type"]) is str
            and "format" in schema
            and schema["format"] not in FORMATS.checkers
        ):
            raise ExecutionRefusal("UNSUPPORTED_FORMAT", str(schema["format"]))
        for item in schema.values():
            _formats(item)
    elif isinstance(schema, list):
        for item in schema:
            _formats(item)


def _validate(schema, value):
    _formats(schema)
    VALUE_VALIDATOR(schema, format_checker=FORMATS).validate(value)


def _path(value, path):
    for part in path:
        if type(value) is dict and type(part) is str:
            value = value[part]
        elif type(value) is list and type(part) is int and 0 <= part < len(value):
            value = value[part]
        else:
            raise ValueError(f"cannot resolve path component {part!r}")
    return value


def _state(value, profile):
    if type(value) is not dict or set(value) != {"protocol", "action_acceptance_head"}:
        raise ValueError("explicit protocol indexes and action head are required")
    if type(value["protocol"]) is not dict or not _head(
        value["action_acceptance_head"]
    ):
        raise ValueError("invalid protocol state")
    for name, entries in value["protocol"].items():
        if type(name) is not str or not name or type(entries) is not list:
            raise ValueError("invalid index")
        keys = set()
        for entry in entries:
            if type(entry) is not dict or set(entry) != {"keys", "value"}:
                raise ValueError("index entries require keys and value")
            if (
                type(entry["keys"]) is not list
                or not entry["keys"]
                or any(type(k) is not str for k in entry["keys"])
            ):
                raise ValueError("index keys must be a nonempty string list")
            key = tuple(entry["keys"])
            if key in keys:
                raise ValueError("duplicate index key")
            keys.add(key)
            if name in profile["targets"]:
                declaration = profile["targets"][name]
                if declaration["target"] != "PROTOCOL_INDEX" or len(key) != len(
                    declaration["key_schemas"]
                ):
                    raise ValueError("index declaration mismatch")
                for item, schema in zip(key, declaration["key_schemas"], strict=True):
                    _validate(schema, item)
                _validate(declaration["value_schema"], entry["value"])


def _typed_record(view, wrapper):
    if type(wrapper) is not dict or set(wrapper) != {"record_type", "record"}:
        raise ValueError("full typed record wrapper required")
    kind, record = wrapper["record_type"], wrapper["record"]
    definition = view.get_type(kind)
    if definition.abstract or definition.is_mixin or type(record) is not dict:
        raise ValueError("concrete complete record required")
    errors = view.validate_instance(kind, record)
    if errors:
        raise ValueError(f"record contract: {errors}")
    return record


def _resolve(view, records, identifier, digest, kind):
    if identifier not in records:
        raise ValueError(f"record not applied: {identifier}")
    wrapper = records[identifier]
    value = _typed_record(view, wrapper)
    if not view.is_subtype_of(wrapper["record_type"], kind):
        raise ValueError("record type differs")
    if (
        value["id"] != identifier
        or record_hash(wrapper["record_type"], value) != digest
        or value["content_hash"] != digest
    ):
        raise ValueError("record identity differs")
    return value


def _inside(inner, outer):
    validate_interval(inner)
    validate_interval(outer)
    if aware_datetime(inner["start"], "inner") < aware_datetime(
        outer["start"], "outer"
    ):
        return False
    if "end" not in outer:
        return True
    return "end" in inner and aware_datetime(
        inner["end"], "inner end"
    ) <= aware_datetime(outer["end"], "outer end")


def execute_program(
    *,
    program,
    profile,
    instruction_schema,
    inputs,
    applied_records,
    state,
    record_contract_bytes,
):
    """Run exact instructions and return private staged state, or typed refusal.

    ``record_contract_bytes`` are the compiled artifact, not a digest-shaped
    assertion. VALIDATE_RECORD's contract_identity is SHA-256 of those bytes.
    No caller object is mutated. No success authenticates supplied history.
    """
    try:
        if type(record_contract_bytes) is not bytes:
            raise ValueError("exact compiled record-contract bytes required")
        validate_instruction_schema(instruction_schema)
        program, profile, inputs, applied_records, state = deepcopy(
            (program, profile, inputs, applied_records, state)
        )
        canonical_json([program, profile, inputs, applied_records, state])
        validate_program(
            program, instruction_schema=instruction_schema, profile=profile
        )
        if set(program["required_capabilities"]) - CAPABILITIES.keys():
            raise ExecutionRefusal(
                "UNSUPPORTED_CAPABILITY",
                "no producer invocation runs inside this kernel",
            )
        _formats(program["inputs"])
        _formats(profile)
        if type(inputs) is not dict or set(inputs) != set(program["inputs"]):
            raise ValueError("input roots differ from program")
        for root, declarations in program["inputs"].items():
            if type(inputs[root]) is not dict or set(inputs[root]) != set(declarations):
                raise ValueError(f"input bindings differ: {root}")
            for name, schema in declarations.items():
                _validate(schema, inputs[root][name])
        if type(applied_records) is not dict:
            raise ValueError("explicit applied-record map required")
        _state(state, profile)
        view = load_validated_contract_artifact(record_contract_bytes)
        contract_identity = "sha256:" + sha256(record_contract_bytes).hexdigest()
    except ExecutionRefusal:
        raise
    except (PacketRefusal, ValueError, TypeError, KeyError, ValidationError) as error:
        raise ExecutionRefusal("INPUT_SHAPE", str(error)) from error

    results, introduced = {}, {}

    def resolve(operand):
        container = results if operand["root"] == "result" else inputs[operand["root"]]
        return _path(container[operand["name"]], operand["path"])

    for ordinal, step in enumerate(program["steps"]):
        try:
            values = {
                name: resolve(value)
                for name, value in step.items()
                if type(value) is dict
            }
            opcode, output = step["opcode"], None
            if opcode == "VALIDATE_RECORD":
                reference = values["contract"]
                if (
                    set(reference) != {"contract_identity", "record_type"}
                    or reference["contract_identity"] != contract_identity
                ):
                    raise ValueError("compiled record contract mismatch")
                output = _typed_record(
                    view,
                    {
                        "record_type": reference["record_type"],
                        "record": values["record"],
                    },
                )
            elif opcode == "HASH":
                if step["recipe"] == "VALUE":
                    output = content_digest(values["value"])
                elif step["recipe"] == "RECORD":
                    output = record_hash(values["record_type"], values["value"])
                else:
                    raise ExecutionRefusal(
                        "UNSUPPORTED_HASH_RECIPE",
                        "use an explicitly bound VALUE preimage",
                        step=ordinal,
                    )
            elif opcode == "REQUIRE_COMPARE":
                left, right = values["left"], values["right"]
                if step["value_kind"] == "INSTANT":
                    left, right = (
                        aware_datetime(left, "left"),
                        aware_datetime(right, "right"),
                    )
                operation = step["comparison"]
                accepted = (
                    left == right
                    if operation == "EQ"
                    else left != right
                    if operation == "NE"
                    else left < right
                    if operation == "LT"
                    else left <= right
                )
                if not accepted:
                    raise ValueError("comparison failed")
            elif opcode == "REQUIRE_MEMBER":
                if values["value"] not in values["members"]:
                    raise ValueError("value is not a member")
            elif opcode == "REQUIRE_SORTED_UNIQUE_STRINGS":
                members = values["values"]
                if (
                    type(members) is not list
                    or any(type(v) is not str for v in members)
                    or any(a >= b for a, b in zip(members, members[1:]))
                ):
                    raise ValueError("list is not strictly increasing")
            elif opcode == "RESOLVE_RECORD":
                records = (
                    applied_records
                    if step["scope"] == "APPLIED"
                    else {**applied_records, **introduced}
                )
                output = _resolve(
                    view,
                    records,
                    values["record_id"],
                    values["record_hash"],
                    values["record_type"],
                )
                _validate(profile["record_schemas"][values["record_type"]], output)
            elif opcode == "REQUIRE_UNIQUE":
                keys = [
                    tuple(_path(record, path) for path in step["key_paths"])
                    for record in values["records"]
                ]
                if len(keys) != len(set(keys)):
                    raise ValueError("duplicate supplied key")
                if "target_index" in step and step["target_index"] in state["protocol"]:
                    prior = {
                        tuple(entry["keys"])
                        for entry in state["protocol"][step["target_index"]]
                    }
                    if prior.intersection(keys):
                        raise ValueError("key already exists")
            elif opcode == "REQUIRE_INTERVAL":
                if not _inside(values["inner"], values["outer"]):
                    raise ValueError("interval is not contained")
            elif opcode in {"REQUIRE_COVERAGE", "SELECT_CONTROL"}:
                if values["context"]["recipe"] not in program["required_capabilities"]:
                    raise ExecutionRefusal(
                        "UNDECLARED_CAPABILITY",
                        values["context"]["recipe"],
                        step=ordinal,
                    )
                if opcode == "REQUIRE_COVERAGE":
                    require_coverage(
                        values["required"], values["outputs"], values["context"]
                    )
                else:
                    output = select_control(
                        values["policy"], values["outputs"], values["context"]
                    )
                    # Existing result dataclasses use tuples. The artifact uses JSON lists.
                    output = json.loads(canonical_json(output))
                    _validate(profile["control_result_schema"], output)
            elif opcode == "INTRODUCE_RECORDS":
                dependencies = values["dependencies"]
                if (
                    type(dependencies) is not list
                    or any(type(v) is not str for v in dependencies)
                    or len(set(dependencies)) != len(dependencies)
                ):
                    raise ValueError("explicit unique dependency IDs required")
                required = set()
                for wrapper in values["records"]:
                    value = _typed_record(view, wrapper)
                    identifier, sources = value["id"], value["source_record_ids"]
                    if (
                        not _nonblank(identifier)
                        or identifier in applied_records
                        or identifier in introduced
                    ):
                        raise ValueError("record ID is blank or reused")
                    if value["content_hash"] != record_hash(
                        wrapper["record_type"], value
                    ):
                        raise ValueError("record hash differs")
                    if (
                        type(sources) is not list
                        or any(type(v) is not str for v in sources)
                        or len(set(sources)) != len(sources)
                    ):
                        raise ValueError("explicit unique provenance IDs required")
                    if set(sources) - applied_records.keys() - introduced.keys():
                        raise ValueError("provenance is not applied or earlier-staged")
                    for source in sources:
                        prior = (
                            introduced if source in introduced else applied_records
                        )[source]
                        _resolve(
                            view,
                            {source: prior},
                            source,
                            prior["record"]["content_hash"],
                            prior["record_type"],
                        )
                    required.update(sources)
                    introduced[identifier] = wrapper
                if required != set(dependencies):
                    raise ValueError("dependency list does not equal record provenance")
                output = values["records"]
            elif opcode == "SET_PROTOCOL_STATE":
                declaration = profile["targets"][step["name"]]
                _validate(declaration["value_schema"], values["value"])
                if step["target"] == "ACTION_ACCEPTANCE_HEAD":
                    state["action_acceptance_head"] = values["value"]
                else:
                    keys = [resolve(key) for key in step["keys"]]
                    for key, schema in zip(
                        keys, declaration["key_schemas"], strict=True
                    ):
                        _validate(schema, key)
                    name = step["name"]
                    entries = (
                        state["protocol"][name] if name in state["protocol"] else []
                    )
                    entries = [entry for entry in entries if entry["keys"] != keys]
                    entries.append({"keys": keys, "value": values["value"]})
                    state["protocol"][name] = sorted(
                        entries, key=lambda entry: entry["keys"]
                    )
            else:
                raise ExecutionRefusal("UNSUPPORTED_INSTRUCTION", opcode, step=ordinal)
            if "result" in step:
                results[step["result"]] = {"value": deepcopy(output)}
        except ExecutionRefusal:
            raise
        except (
            ValueError,
            KeyError,
            TypeError,
            ValidationError,
            PacketRefusal,
        ) as error:
            raise ExecutionRefusal(step["refusal"], str(error), step=ordinal) from error
    return ProgramExecution(
        canonical_json(
            {
                "program_identity": content_digest(
                    {
                        "program": program,
                        "profile": profile,
                        "instruction_schema": instruction_schema,
                        "record_contract_identity": contract_identity,
                    }
                ),
                "runtime_executed": True,
                "history_authenticated": False,
                "state": state,
                "introductions": list(introduced.values()),
                "results": results,
            }
        ).encode()
    )

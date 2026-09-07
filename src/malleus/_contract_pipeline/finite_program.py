"""Research-only definition checker. No instruction executes or state persists.

Program inputs are closed JSON Schemas, not trusted runtime objects. A successful
static check establishes declared path/type closure only. Local content and
monitor schemas are explicit dependencies of this research packet.
"""

from copy import deepcopy

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError

from malleus.ledger import LedgerError, aware_datetime, require_digest


ROOTS = {"event", "applied_record", "original", "current", "artifact"}
SCALAR_TYPES = {
    "STRING": "string",
    "DIGEST": "string",
    "HEAD": "string",
    "INTEGER": "integer",
    "BOOLEAN": "boolean",
    "INSTANT": "string",
}
FORMATS = FormatChecker()


class PacketRefusal(ValueError):
    def __init__(self, reason, detail):
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")


@FORMATS.checks("sha256", raises=LedgerError)
def _digest(value):
    require_digest(value, "identity")
    return True


@FORMATS.checks("aware-instant", raises=LedgerError)
def _instant(value):
    aware_datetime(value, "instant")
    return True


def _refuse(reason, detail):
    raise PacketRefusal(reason, detail)


def _closed(value, required, optional=()):
    if (
        not isinstance(value, dict)
        or not set(required) <= value.keys()
        or set(value) - set(required) - set(optional)
    ):
        _refuse("DEFINITION_SHAPE", f"expected fields {sorted(required)}")


def _names(value):
    if (
        not isinstance(value, list)
        or any(not isinstance(v, str) or not v for v in value)
        or len(value) != len(set(value))
    ):
        _refuse("DEFINITION_SHAPE", "expected unique nonempty names")


def _local_references(schema):
    if isinstance(schema, dict):
        if "$ref" in schema and (
            not isinstance(schema["$ref"], str) or not schema["$ref"].startswith("#")
        ):
            _refuse("DEFINITION_SCHEMA", "schema references must be local")
        for child in schema.values():
            _local_references(child)
    elif isinstance(schema, list):
        for child in schema:
            _local_references(child)


def _schema(schema):
    _local_references(schema)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise PacketRefusal("DEFINITION_SCHEMA", error.message) from error
    if not isinstance(schema, dict) or not isinstance(schema.get("type"), str):
        _refuse("DEFINITION_SCHEMA", "a single explicit type is required")
    if schema["type"] not in {
        "object",
        "array",
        "string",
        "integer",
        "boolean",
        "number",
        "null",
    }:
        _refuse("DEFINITION_SCHEMA", "a single explicit type is required")
    if "$ref" in schema or any(k in schema for k in ("oneOf", "anyOf", "allOf", "if")):
        _refuse("DEFINITION_SCHEMA", "expand variants before static path checking")
    if "prefixItems" in schema:
        _refuse("DEFINITION_SCHEMA", "positional arrays are outside this static subset")
    if schema["type"] == "object":
        if (
            schema.get("additionalProperties") is not False
            or "properties" not in schema
            or "required" not in schema
        ):
            _refuse("DEFINITION_SCHEMA", "object bindings must explicitly close fields")
        if not set(schema["required"]) <= schema["properties"].keys():
            _refuse("DEFINITION_SCHEMA", "required field has no declaration")
        for child in schema["properties"].values():
            _schema(child)
    if schema["type"] == "array" and "items" in schema:
        _schema(schema["items"])
    if "const" in schema:
        try:
            Draft202012Validator(schema, format_checker=FORMATS).validate(
                schema["const"]
            )
        except ValidationError as error:
            raise PacketRefusal("DEFINITION_SCHEMA", error.message) from error


def _path(schema, path):
    for part in path:
        if schema["type"] == "object" and isinstance(part, str):
            if part not in schema["properties"] or part not in schema["required"]:
                _refuse("UNRESOLVED_PATH", f"field {part!r} is not guaranteed")
            schema = schema["properties"][part]
        elif schema["type"] == "array" and type(part) is int:
            if (
                "items" not in schema
                or "minItems" not in schema
                or not 0 <= part < schema["minItems"]
            ):
                _refuse("UNRESOLVED_PATH", f"index {part!r} is not guaranteed")
            schema = schema["items"]
        else:
            _refuse("UNRESOLVED_PATH", f"cannot resolve {part!r}")
    return schema


def _same_type(actual, expected):
    if actual["type"] != expected["type"]:
        _refuse("OPERAND_TYPE", f"{actual['type']} is not {expected['type']}")
    if "format" in expected and actual.get("format") != expected["format"]:
        _refuse("OPERAND_TYPE", f"expected format {expected['format']}")
    left, right = actual.get("x-coordinate"), expected.get("x-coordinate")
    if left != right:
        _refuse("COORDINATE_DOMAIN", f"{left!r} is not {right!r}")


def _dependencies(introductions):
    if not isinstance(introductions, list):
        _refuse("DEFINITION_SHAPE", "introductions must be a list")
    graph = {}
    for item in introductions:
        _closed(item, {"name", "depends_on"})
        _names([item["name"]])
        _names(item["depends_on"])
        if item["name"] in graph:
            _refuse("REUSED_INTRODUCTION", item["name"])
        graph[item["name"]] = item["depends_on"]
    for dependencies in graph.values():
        if set(dependencies) - graph.keys():
            _refuse("UNRESOLVED_DEPENDENCY", "dependency is not declared")
    pending = dict(graph)
    while pending:
        roots = [
            name for name, deps in pending.items() if not set(deps) & pending.keys()
        ]
        if not roots:
            _refuse("CYCLIC_DEPENDENCY", "introductions form a cycle")
        for name in roots:
            del pending[name]
    earlier = set()
    for name, deps in graph.items():
        if not set(deps) <= earlier:
            _refuse("FORWARD_DEPENDENCY", name)
        earlier.add(name)


def _target(profile, name, target):
    if name not in profile["targets"]:
        _refuse("UNDECLARED_TARGET", name)
    declaration = profile["targets"][name]
    if declaration["target"] != target:
        _refuse("UNDECLARED_TARGET", f"wrong target category for {name}")
    return declaration["value_schema"]


def _index_keys(profile, name, actual):
    expected = profile["targets"][name]["key_schemas"]
    if len(actual) != len(expected):
        _refuse("INDEX_KEY_ARITY", f"{name} requires {len(expected)} ordered keys")
    for key, schema in zip(actual, expected, strict=True):
        _same_type(key, schema)


def validate_program(program, *, instruction_schema, profile):
    """Check finite declarations only; never authenticate inputs or run steps."""
    _local_references(instruction_schema)
    program, profile = deepcopy(program), deepcopy(profile)
    _closed(
        program, {"name", "inputs", "required_capabilities", "introductions", "steps"}
    )
    _closed(
        profile,
        {"targets", "capabilities"},
        {"record_schemas", "control_result_schema"},
    )
    _names([program["name"]])
    _names(program["required_capabilities"])
    _names(profile["capabilities"])
    if set(program["required_capabilities"]) - set(profile["capabilities"]):
        _refuse("UNKNOWN_CAPABILITY", "required capability has no definition")
    if not isinstance(program["inputs"], dict) or set(program["inputs"]) - ROOTS:
        _refuse("INPUT_ROOT", "only declared non-result roots may be inputs")
    for names in program["inputs"].values():
        if not isinstance(names, dict):
            _refuse("DEFINITION_SHAPE", "bindings must be named")
        for name, schema in names.items():
            _names([name])
            _schema(schema)
    if not isinstance(profile["targets"], dict):
        _refuse("DEFINITION_SHAPE", "targets must be named")
    for name, declaration in profile["targets"].items():
        fields = {"target", "storage_path", "value_schema"}
        _closed(declaration, fields, {"key_schemas"})
        expected = (
            ["protocol", name]
            if declaration["target"] == "PROTOCOL_INDEX"
            else ["action_acceptance_head"]
        )
        if (
            declaration["target"] not in {"PROTOCOL_INDEX", "ACTION_ACCEPTANCE_HEAD"}
            or declaration["storage_path"] != expected
        ):
            _refuse("DOMAIN_STATE_TARGET", name)
        if declaration["target"] == "PROTOCOL_INDEX":
            _closed(declaration, fields | {"key_schemas"})
            keys = declaration["key_schemas"]
            if not isinstance(keys, list) or not keys:
                _refuse("DEFINITION_SHAPE", "index key schemas must be a nonempty list")
            for key in keys:
                _schema(key)
                if key["type"] != "string":
                    _refuse("DEFINITION_SHAPE", "index keys must be strings")
        else:
            _closed(declaration, fields)
        _schema(declaration["value_schema"])
    _dependencies(program["introductions"])
    if not isinstance(program["steps"], list) or not program["steps"]:
        _refuse("DEFINITION_SHAPE", "program requires finite nonempty steps")
    try:
        Draft202012Validator.check_schema(instruction_schema)
    except SchemaError as error:
        raise PacketRefusal("DEFINITION_SCHEMA", error.message) from error
    instruction_validator = Draft202012Validator(instruction_schema)
    results = {}

    def resolve(operand):
        root, name = operand["root"], operand["name"]
        if root == "result":
            if name not in results:
                _refuse("FORWARD_RESULT", name)
            schema = results[name]
        else:
            if root not in program["inputs"] or name not in program["inputs"][root]:
                _refuse("UNDECLARED_BINDING", f"{root}.{name}")
            schema = program["inputs"][root][name]
        return _path(schema, operand["path"])

    def require(value, kind):
        if value["type"] != kind:
            _refuse("OPERAND_TYPE", f"expected {kind}, got {value['type']}")

    for ordinal, step in enumerate(program["steps"]):
        if not instruction_validator.is_valid(step):
            _refuse("INSTRUCTION_SHAPE", f"step {ordinal}")
        values = {
            key: resolve(value)
            for key, value in step.items()
            if isinstance(value, dict)
        }
        opcode = step["opcode"]
        result_schema = None
        if opcode == "HASH":
            if step["recipe"] == "RECORD":
                require(values["record_type"], "string")
                require(values["value"], "object")
            elif step["recipe"] == "ARTIFACT":
                require(values["artifact_contract"], "object")
            result_schema = {"type": "string", "format": "sha256"}
        elif opcode == "REQUIRE_COMPARE":
            require(values["left"], SCALAR_TYPES[step["value_kind"]])
            require(values["right"], SCALAR_TYPES[step["value_kind"]])
            formats = {
                "DIGEST": "sha256",
                "HEAD": "ledger-head",
                "INSTANT": "aware-instant",
            }
            if step["value_kind"] in formats:
                for value in values.values():
                    if value.get("format") != formats[step["value_kind"]]:
                        _refuse(
                            "OPERAND_TYPE",
                            f"expected format {formats[step['value_kind']]}",
                        )
            _same_type(values["left"], values["right"])
        elif opcode == "REQUIRE_MEMBER":
            require(values["value"], "string")
            require(values["members"], "array")
            if "items" not in values["members"]:
                _refuse("UNRESOLVED_PATH", "membership list has no item schema")
            require(values["members"]["items"], "string")
            _same_type(values["value"], values["members"]["items"])
        elif opcode == "REQUIRE_SORTED_UNIQUE_STRINGS":
            require(values["values"], "array")
            if "items" not in values["values"]:
                _refuse("UNRESOLVED_PATH", "canonical list has no item schema")
            require(values["values"]["items"], "string")
        elif opcode == "VALIDATE_RECORD":
            require(values["record"], "object")
            require(values["contract"], "object")
            result_schema = values["record"]
        elif opcode == "RESOLVE_RECORD":
            for key in ("record_id", "record_hash", "record_type"):
                require(values[key], "string")
            type_schema = values["record_type"]
            if (
                "const" not in type_schema
                or "record_schemas" not in profile
                or type_schema["const"] not in profile["record_schemas"]
            ):
                _refuse(
                    "UNBOUND_RECORD_SCHEMA", "resolve a finite declared type variant"
                )
            result_schema = profile["record_schemas"][type_schema["const"]]
            _schema(result_schema)
        elif opcode == "REQUIRE_UNIQUE":
            require(values["records"], "array")
            if "items" not in values["records"]:
                _refuse("UNRESOLVED_PATH", "unique list has no item schema")
            keys = [
                _path(values["records"]["items"], path) for path in step["key_paths"]
            ]
            for key in keys:
                if key["type"] in {
                    "object",
                    "array",
                }:
                    _refuse("OPERAND_TYPE", "unique key must be scalar")
            if "target_index" in step:
                _target(profile, step["target_index"], "PROTOCOL_INDEX")
                _index_keys(profile, step["target_index"], keys)
        elif opcode in {"REQUIRE_COVERAGE", "SELECT_CONTROL"}:
            require(values["outputs"], "array")
            require(values["context"], "object")
            require(
                values["required"]
                if opcode == "REQUIRE_COVERAGE"
                else values["policy"],
                "array" if opcode == "REQUIRE_COVERAGE" else "object",
            )
            if opcode == "SELECT_CONTROL":
                if "control_result_schema" not in profile:
                    _refuse(
                        "UNBOUND_CONTROL_SCHEMA", "control output contract required"
                    )
                result_schema = profile["control_result_schema"]
                _schema(result_schema)
        elif opcode == "REQUIRE_INTERVAL":
            for value in values.values():
                require(value, "object")
                require(_path(value, ["start"]), "string")
        elif opcode == "INTRODUCE_RECORDS":
            require(values["records"], "array")
            require(values["dependencies"], "array")
            result_schema = values["records"]
        elif opcode == "SET_PROTOCOL_STATE":
            expected = _target(profile, step["name"], step["target"])
            if step["target"] == "PROTOCOL_INDEX":
                _index_keys(
                    profile, step["name"], [resolve(key) for key in step["keys"]]
                )
            _same_type(values["value"], expected)
        else:
            _refuse("UNKNOWN_INSTRUCTION", opcode)
        if "result" in step:
            if step["result"] in results:
                _refuse("REUSED_RESULT", step["result"])
            if result_schema is None:
                _refuse("UNBOUND_RESULT", step["result"])
            results[step["result"]] = {
                "type": "object",
                "properties": {"value": result_schema},
                "required": ["value"],
                "additionalProperties": False,
            }
    return {
        "status": "STATIC_VALID",
        "steps": len(program["steps"]),
        "runtime_executed": False,
    }


def validate_interval(value):
    """Validate half-open interval contents; absent end alone means unbounded."""
    try:
        _closed(value, {"start"}, {"end"})
        start = aware_datetime(value["start"], "interval start")
        if "end" in value and aware_datetime(value["end"], "interval end") <= start:
            _refuse("INVALID_INTERVAL", "end must be strictly later than start")
    except (LedgerError, PacketRefusal) as error:
        raise PacketRefusal("INVALID_INTERVAL", str(error)) from error

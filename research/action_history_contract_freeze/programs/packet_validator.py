"""Fixture content loaders; finite program validation is owned by Core."""

import json
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from malleus._contract_pipeline.finite_program import (
    FORMATS,
    PacketRefusal,
    _local_references,
    _refuse,
    validate_interval,
    validate_program,
)

HERE = Path(__file__).parent

__all__ = [
    "PacketRefusal",
    "validate_interval",
    "validate_program",
    "validate_content",
    "validate_monitor_contract",
    "_local_references",
]


def validate_content(kind, value):
    schema = json.loads((HERE / "contents.schema.json").read_bytes())
    if kind not in schema["$defs"] or kind not in {"scope", "current"}:
        _refuse("UNKNOWN_CONTENT", kind)
    selected = {**schema, "$ref": f"#/$defs/{kind}"}
    try:
        Draft202012Validator(selected, format_checker=FORMATS).validate(value)
    except ValidationError as error:
        raise PacketRefusal("CONTENT_REFUSAL", error.message) from error


def validate_monitor_contract(value):
    schema = json.loads((HERE / "monitor-contract.schema.json").read_bytes())
    try:
        Draft202012Validator(schema).validate(value)
    except ValidationError as error:
        raise PacketRefusal("MONITOR_CONTRACT", error.message) from error

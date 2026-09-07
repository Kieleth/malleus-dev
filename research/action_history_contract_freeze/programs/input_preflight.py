"""Research input-specimen inspection, not a history resolver or check producer.

Inputs are caller-supplied records/bytes. Success establishes internal reference,
shape and byte consistency for invocation.inputs only. Monitor/implementation
references are shape-checked, not resolved. It cannot establish applied-prefix membership,
policy validity, currentness, complete provenance or an executed assessment.
"""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

import malleus.compiler as api
from malleus.ledger import canonical_json, record_hash
from malleus.source import SourceError, source_artifact_fields
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_content,
    validate_interval,
)


HERE = Path(__file__).parent


def _record(reference, root, records, view, binding):
    record_id = reference["id"]
    if record_id not in records:
        raise PacketRefusal("INPUT_NOT_SUPPLIED", record_id)
    wrapper = records[record_id]
    if type(wrapper) is not dict or set(wrapper) != {"record_type", "record"}:
        raise PacketRefusal("INPUT_RECORD_SHAPE", record_id)
    kind, value = wrapper["record_type"], wrapper["record"]
    try:
        definition = view.get_type(kind)
        compatible = view.is_subtype_of(kind, root)
    except (KeyError, TypeError, ValueError) as error:
        raise PacketRefusal("INPUT_RECORD_TYPE", record_id) from error
    if definition.abstract or definition.is_mixin or not compatible:
        raise PacketRefusal(
            "INPUT_RECORD_TYPE", f"{record_id}: expected concrete {root}"
        )
    if type(value) is not dict:
        raise PacketRefusal("INPUT_RECORD_SHAPE", record_id)
    errors = view.validate_instance(kind, value)
    for ancestor, required in binding["required_presence"].items():
        if view.is_subtype_of(kind, ancestor):
            errors.extend(
                f"missing {field}" for field in required if field not in value
            )
    if errors:
        raise PacketRefusal("INPUT_RECORD_SHAPE", f"{record_id}: {errors}")
    if value["id"] != record_id:
        raise PacketRefusal("INPUT_RECORD_ID", record_id)
    digest = record_hash(kind, value)
    if value["content_hash"] != digest:
        raise PacketRefusal("INPUT_RECORD_HASH", record_id)
    if "record_hash" in reference and reference["record_hash"] != digest:
        raise PacketRefusal("INPUT_RECORD_HASH", record_id)
    return value


def _content(kind, content, contract_bytes, binding):
    try:
        if kind == "compiled-record-contract":
            api.load_validated_contract_artifact(content)
            if content != contract_bytes:
                raise PacketRefusal(
                    "INPUT_CONTRACT_MISMATCH", "record contract bytes differ"
                )
            return
        value = json.loads(content)
        if canonical_json(value).encode() != content:
            raise ValueError("role content must be canonical JSON")
        if kind in {"scope", "current"}:
            validate_content(kind, value)
        elif kind == "interval":
            validate_interval(value)
        elif kind == "original-context":
            schema = json.loads((HERE.parent / "contexts.schema.json").read_bytes())
            Draft202012Validator(schema, format_checker=FORMATS).validate(value)
            if value["schema"] != binding["content_tags"][kind]:
                raise ValueError("wrong context variant")
        else:
            raise ValueError(f"undeclared content parser: {kind}")
    except PacketRefusal as error:
        if error.reason == "INPUT_CONTRACT_MISMATCH":
            raise
        raise PacketRefusal("INPUT_CONTENT", str(error)) from error
    except (api.ArtifactRefusal, ValueError, TypeError, ValidationError) as error:
        raise PacketRefusal("INPUT_CONTENT", str(error)) from error


def validate_input_specimen(*, invocation, records, retained_bytes, contract_bytes):
    """Inspect supplied bytes only. Never call a monitor, fetch a locator or write."""
    if any(type(value) is not dict for value in (invocation, records, retained_bytes)):
        raise PacketRefusal("INPUT_SPECIMEN_SHAPE", "explicit dict inputs required")
    invocation, records, retained_bytes = deepcopy(
        (invocation, records, retained_bytes)
    )
    binding = json.loads((HERE / "input-bindings.json").read_bytes())
    schema = json.loads((HERE / "invocation.schema.json").read_bytes())
    try:
        Draft202012Validator(schema, format_checker=FORMATS).validate(invocation)
    except ValidationError as error:
        raise PacketRefusal("INVOCATION_SHAPE", error.message) from error
    if type(contract_bytes) is not bytes:
        raise PacketRefusal("INPUT_CONTRACT", "exact contract bytes required")
    try:
        view = api.load_validated_contract_artifact(contract_bytes)
    except (api.ArtifactRefusal, TypeError, ValueError) as error:
        raise PacketRefusal("INPUT_CONTRACT", str(error)) from error
    for entry in invocation["inputs"]:
        role, reference = entry["role"], entry["value"]
        if role in binding["scalar_inputs"]:
            continue  # The closed invocation schema validates the literal scalar.
        if role in binding["record_inputs"]:
            _record(reference, binding["record_inputs"][role], records, view, binding)
            continue
        if role not in binding["byte_inputs"]:
            raise PacketRefusal("INPUT_ROLE", role)
        carrier = _record(
            reference, binding["carrier"]["record_type"], records, view, binding
        )
        if carrier["artifact_kind"] != binding["carrier"]["artifact_kind"]:
            raise PacketRefusal("INPUT_RECORD_TYPE", role)
        record_id = reference["id"]
        if record_id not in retained_bytes:
            raise PacketRefusal("INPUT_NOT_SUPPLIED", f"bytes: {record_id}")
        content = retained_bytes[record_id]
        if type(content) is not bytes:
            raise PacketRefusal(
                "INPUT_BYTE_BINDING", f"exact bytes required: {record_id}"
            )
        try:
            expected = source_artifact_fields(
                artifact_id=record_id,
                artifact_version=carrier["artifact_version"],
                source_bytes=content,
                media_type=carrier["source_media_type"],
                locator=carrier["source_locator"],
            )
        except SourceError as error:
            raise PacketRefusal("INPUT_BYTE_BINDING", str(error)) from error
        digest_field = binding["identity_fields"]["reference_bytes_sha256"]
        if reference["bytes_sha256"] != expected[digest_field] or any(
            carrier[key] != value for key, value in expected.items()
        ):
            raise PacketRefusal("INPUT_BYTE_BINDING", record_id)
        _content(binding["byte_inputs"][role], content, contract_bytes, binding)
    return {
        "status": "STATIC_INPUTS_VALID",
        "scope": "INVOCATION_ROLE_INPUTS",
        "retention_verified": False,
        "runtime_executed": False,
        "roles": [entry["role"] for entry in invocation["inputs"]],
    }

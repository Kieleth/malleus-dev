"""SourceArtifact records bind real bytes through the owning transaction."""

from copy import deepcopy

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.lifecycle.test_initialization import (
    packet,
)
from research.action_history_contract_freeze.programs.test_packet_validator import (
    obj,
    operand,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import (
    api,
    canonical,
    specimen,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _anchored_history,
    _evidence_anchor,
    TRANSACTION_TIME,
)


TIME = "2026-09-07T00:00:00Z"


def source_bundle():
    bundle, _ = specimen()
    old = packet("source-registration")
    program = old["program"]
    record_schema = program["inputs"]["event"]["records"]["properties"]["value"][
        "items"
    ]["properties"]["record"]
    for field in old["semantic_hash_contract"]["field_checks"]["nonblank_fields"]:
        record_schema["properties"][field]["format"] = "nonblank"
    mapping = old["semantic_hash_contract"]["preimage_fields"]
    preimage_schema = obj(
        **{k: deepcopy(record_schema["properties"][v]) for k, v in mapping.items()}
    )
    old_inputs = deepcopy(program["inputs"])
    header = deepcopy(
        bundle["transactions"]["register-pair"]["program"]["inputs"]["event"]["0"][
            "properties"
        ]["header"]
    )
    metadata = obj(
        record_id={"type": "string"},
        identity={"type": "string", "format": "sha256"},
        byte_length={"type": "integer", "minimum": 0},
        media_type={"type": "string"},
        role={"type": "string", "const": "SOURCE_ARTIFACT"},
        encoding={"type": "string", "const": "BYTES"},
    )
    constants = {
        "record_contract": {
            "value": {
                "contract_identity": bundle["constants"]["record_contract"]["value"][
                    "contract_identity"
                ],
                "record_type": "SourceArtifact",
            }
        },
        "constants": {"registrar_role": "registrar"},
    }
    program["inputs"] = {
        "event": {
            "0": obj(
                header=header,
                data=obj(
                    records=old_inputs["event"]["records"],
                    dependencies=old_inputs["event"]["dependencies"],
                    preimage=preimage_schema,
                ),
                retained=obj(source=metadata),
            )
        },
        "current": deepcopy(
            bundle["transactions"]["register-pair"]["program"]["inputs"]["current"]
        ),
        "artifact": {
            "constants": obj(
                value=obj(
                    record_contract=old_inputs["artifact"]["record_contract"],
                    constants=old_inputs["artifact"]["constants"],
                )
            )
        },
    }
    transformed = []
    for step in program["steps"]:
        step = deepcopy(step)
        if step["opcode"] == "HASH" and step["recipe"] == "ARTIFACT":
            for projected, field in mapping.items():
                transformed.append(
                    {
                        "opcode": "REQUIRE_COMPARE",
                        "comparison": "EQ",
                        "value_kind": "INTEGER"
                        if field == "source_byte_length"
                        else "STRING",
                        "left": operand("event", "0", "data", "preimage", projected),
                        "right": operand(
                            "event", "0", "data", "records", "value", 0, "record", field
                        ),
                        "refusal": "SOURCE_PREIMAGE_MISMATCH",
                    }
                )
            step = {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": operand("event", "0", "data", "preimage"),
                "result": step["result"],
                "refusal": step["refusal"],
            }
        else:
            for value in step.values():
                if type(value) is not dict or set(value) != {"root", "name", "path"}:
                    continue
                root, name, path = value["root"], value["name"], value["path"]
                if root == "event":
                    value.update(
                        name="0",
                        path=(["header"] if name == "header" else ["data", name])
                        + path,
                    )
                elif root == "artifact" and name == "retention":
                    value.update(
                        root="event",
                        name="0",
                        path=[
                            "retained",
                            "source",
                            "identity" if path == ["bytes_sha256"] else "byte_length",
                        ],
                    )
                elif root == "artifact":
                    value.update(name="constants", path=["value", name] + path)
        transformed.append(step)
    transformed.insert(
        -1,
        {
            "opcode": "REQUIRE_COMPARE",
            "comparison": "EQ",
            "value_kind": "STRING",
            "left": operand(
                "event", "0", "data", "records", "value", 0, "record", "id"
            ),
            "right": operand("event", "0", "retained", "source", "record_id"),
            "refusal": "SOURCE_RETAINED_ID_MISMATCH",
        },
    )
    transformed.insert(
        -1,
        {
            "opcode": "REQUIRE_COMPARE",
            "comparison": "EQ",
            "value_kind": "STRING",
            "left": operand(
                "event",
                "0",
                "data",
                "records",
                "value",
                0,
                "record",
                "source_media_type",
            ),
            "right": operand("event", "0", "retained", "source", "media_type"),
            "refusal": "SOURCE_MEDIA_TYPE_MISMATCH",
        },
    )
    program["steps"] = transformed
    bundle.update(
        constants=constants,
        profile=old["profile"],
        transactions={
            "source": {"event_types": ["SOURCE_RECORDED"], "program": program}
        },
    )
    return bundle, mapping


def setup(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle, mapping = source_bundle()
    history.append_anchors(
        anchors=(_evidence_anchor("source-program", canonical(bundle)),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="source-program",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="select-source",
        actor_id="actor:registrar",
        transaction_time=TIME,
    )
    content = b"actual retained source bytes\n"
    record = make_record(
        "SourceArtifact",
        id="source:actual",
        event_id="event:source:actual",
        generated_at=TIME,
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=[],
        artifact_kind="SOURCE",
        artifact_version="v1",
        **source_artifact_fields(
            artifact_id="source:actual",
            artifact_version="v1",
            source_bytes=content,
            media_type="text/plain",
            locator="urn:retained:source:actual",
        ),
    )
    draft = {
        "event_id": record["generation_event_id"],
        "event_type": "SOURCE_RECORDED",
        "actor_id": record["responsible_actor_id"],
        "transaction_time": TIME,
        "data": {
            "records": {"value": [{"record_type": "SourceArtifact", "record": record}]},
            "dependencies": {"value": []},
            "preimage": {k: record[v] for k, v in mapping.items()},
        },
        "retained": {
            "source": {
                "record_id": record["id"],
                "content": content,
                "media_type": "text/plain",
                "role": "SOURCE_ARTIFACT",
                "encoding": "BYTES",
            }
        },
    }
    return history, draft


def append(history, draft):
    base = history.replay()
    return history.append_protocol_events(
        transaction="source",
        events=(draft,),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
    )


def test_retained_source_and_typed_protocol_record_are_bound_by_the_program(tmp_path):
    history, draft = setup(tmp_path)
    before = history.replay()
    result = append(history, draft)
    assert (
        result.retained_bytes("source:actual") == draft["retained"]["source"]["content"]
    )
    record = result.protocol_replay.data["records"]["source:actual"]["record"]
    assert record["source_content_digest"] == api().digest(
        result.retained_bytes(record["id"])
    )
    assert (
        record["content_hash"]
        != record["artifact_hash"]
        != record["source_content_digest"]
    )
    assert result.graph.state_digest() == before.graph.state_digest()
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.receipt == result.receipt
    assert reopened.retained_bytes("source:actual") == result.retained_bytes(
        "source:actual"
    )


@pytest.mark.parametrize(
    "fault",
    [
        "bytes",
        "length",
        "record_id",
        "role",
        "media_type",
        "semantic_hash",
        "preimage",
        "extra_retention",
        "duplicate_id",
        "unknown_encoding",
    ],
)
def test_byte_record_and_role_mismatches_refuse_before_append(tmp_path, fault):
    history, draft = setup(tmp_path)
    before = history.path.read_bytes()
    retained = draft["retained"]["source"]
    record = draft["data"]["records"]["value"][0]["record"]
    if fault == "bytes":
        retained["content"] = retained["content"].replace(b"actual", b"forged")
    elif fault == "length":
        retained["content"] += b"extra"
    elif fault == "record_id":
        retained["record_id"] = "wrong:source"
    elif fault == "role":
        retained["role"] = "RETAINED_SOURCE"
    elif fault == "media_type":
        retained["media_type"] = "application/json"
    elif fault == "semantic_hash":
        record["artifact_hash"] = content_digest("forged")
        record["content_hash"] = record_hash("SourceArtifact", record)
    elif fault == "preimage":
        draft["data"]["preimage"]["source_locator"] = "urn:another"
    elif fault in {"extra_retention", "duplicate_id"}:
        draft["retained"]["extra"] = deepcopy(retained)
        if fault == "extra_retention":
            draft["retained"]["extra"]["record_id"] = "unintroduced"
    else:
        retained["encoding"] = "EXECUTE_PYTHON"
    with pytest.raises(api().ProtocolProgramRefusal):
        append(history, draft)
    assert history.path.read_bytes() == before
    assert "source:actual" not in history.replay().protocol_replay.data["records"]

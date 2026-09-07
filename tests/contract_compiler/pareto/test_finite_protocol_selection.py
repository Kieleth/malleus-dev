"""Programs compare declared initialization inputs with their real owner."""

from copy import deepcopy

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest
from tests.contract_compiler.pareto.test_finite_protocol_history import (
    api, append, canonical, drafts, obj, operand, specimen,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _anchored_history, _evidence_anchor, TRANSACTION_TIME,
)


def selected_history(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle, args = specimen()
    fields = ("bundle_identity", "record_contract_identity", "profile_identity",
              "instruction_schema_identity", "history_binding_identity")
    schema = obj(**{k: {"type": "string", "format": "sha256"} for k in fields})
    program = bundle["transactions"]["register-pair"]["program"]
    program["inputs"]["artifact"]["selection"] = obj(value=schema)
    data = program["inputs"]["event"]["0"]["properties"]["data"]
    data["properties"]["selection"] = deepcopy(schema)
    data["required"].append("selection")
    program["steps"][:0] = [
        {"opcode": "REQUIRE_COMPARE", "value_kind": "DIGEST", "comparison": "EQ",
         "left": operand("event", "0", "data", "selection", k),
         "right": operand("artifact", "selection", "value", k),
         "refusal": "WRONG_SELECTED_DEFINITION"} for k in fields
    ]
    source = canonical(bundle)
    history.append_anchors(anchors=(_evidence_anchor("finite-bundle", source),),
                           transaction_time=TRANSACTION_TIME, actor_id="actor:test")
    base = history.replay()
    history.select_protocol_programs(
        record_id="finite-bundle", identity=api().digest(source),
        expected_head=base.ledger_head, expected_count=base.ledger_event_count,
        event_id="select:1", transaction_time=TRANSACTION_TIME, actor_id="actor:test")
    values = {
        "bundle_identity": api().digest(source),
        "record_contract_identity": api().digest(args["record_contract_bytes"]),
        "profile_identity": content_digest(bundle["profile"]),
        "instruction_schema_identity": content_digest(bundle["instruction_schema"]),
        "history_binding_identity": history.binding.identity,
    }
    events = drafts(history, args)
    events[0]["data"]["selection"] = values
    return history, events


def test_selected_definitions_come_from_retained_bundle_and_owner_binding(tmp_path):
    history, events = selected_history(tmp_path)
    replay = append(history, events)
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == replay.receipt


@pytest.mark.parametrize("field", ["bundle_identity", "record_contract_identity",
    "profile_identity", "instruction_schema_identity", "history_binding_identity"])
def test_forged_selected_definition_refuses_before_append(tmp_path, field):
    history, events = selected_history(tmp_path)
    before = history.path.read_bytes()
    events[0]["data"]["selection"][field] = content_digest("other definition")
    with pytest.raises(api().ProtocolProgramRefusal, match="WRONG_SELECTED_DEFINITION"):
        append(history, events)
    assert history.path.read_bytes() == before

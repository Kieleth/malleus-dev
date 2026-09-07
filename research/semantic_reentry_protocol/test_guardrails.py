"""Review counterexamples: exact lineage, bound projection, typed shapes."""

from copy import deepcopy
import json

import pytest

from research.semantic_reentry_protocol import consumer
from research.semantic_reentry_protocol.test_consumer import assess, bundle, edit_plan
from research.semantic_reentry_protocol.test_integration import stage
from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR, E4, E7, MAPPING, TIME, artifact, canonical, compilation, digest, shop,
)


def test_valid_but_wrong_row_citation_cannot_justify_e7(shop):
    request = bundle(shop[0])
    edit_plan(request, lambda plan: plan["derivations"][2].update({"locator": "row:0:quantity"}))
    with pytest.raises(consumer.ReentryRefusal) as refusal:
        assess(consumer, request)
    assert refusal.value.reason is consumer.Reason.SOURCE_DISAGREEMENT


def test_missing_binding_cannot_hide_a_fabricated_property(shop):
    history, path = shop
    mapping = json.loads(history.replay().retained_bytes(MAPPING))
    mapping["state_bindings"] = [member for member in mapping["state_bindings"]
                                 if member["source_field"] != "quantity"]
    mapping["changes"][1]["operations"][0]["properties"]["ordered_quantity"] = 999
    mapping_bytes = canonical(mapping)
    record_id = "artifact:negative-test:incomplete-bindings"
    history.append_anchors(anchors=(artifact(record_id, mapping_bytes),),
                           transaction_time=TIME, actor_id=ACTOR)
    request = bundle(history)
    request["mapping_bytes"] = mapping_bytes
    request["contract"]["request"].update({"mapping_id": record_id,
                                          "mapping_sha256": digest(mapping_bytes)})

    def alter(plan):
        plan["records"]["entities"][0]["properties"]["ordered_quantity"] = 999
        plan["evidence"] = [{"evidence_id": record_id, "sha256": digest(mapping_bytes)}]

    edit_plan(request, alter)
    before = path.read_bytes()
    with pytest.raises(consumer.ReentryRefusal) as refusal:
        assess(consumer, request)
    assert refusal.value.reason is consumer.Reason.SOURCE_DISAGREEMENT
    assert path.read_bytes() == before


def test_rebound_projection_cannot_fabricate_a_satisfied_accepted_state(shop):
    history, path = shop
    _, (implementation, _, _, replay, inputs) = stage(history)
    view = json.loads(inputs["view_bytes"])
    plan = json.loads(inputs["plan_bytes"])
    view["records"]["entities"] = [
        deepcopy(plan["records"]["entities"][0]) if record["id"] == E4 else record
        for record in view["records"]["entities"]
    ]
    view["record_history"][E4]["superseded_by"] = E7
    view["record_history"][E7] = {"supersedes_record_id": E4, "superseded_by": None,
                                  "valid_from": plan["valid_time"]}
    inputs["view_bytes"] = canonical(view)
    contract = json.loads(inputs["contract"].canonical_bytes)
    contract["projection_sha256"] = digest(inputs["view_bytes"])
    inputs["contract"] = consumer.ReentryContract.from_bytes(canonical(contract))
    before = path.read_bytes()
    assert replay.graph.has_node(E4) and not replay.graph.has_node(E7)
    with pytest.raises(consumer.ReentryRefusal) as refusal:
        implementation.synthesize(**inputs)
    assert refusal.value.reason is consumer.Reason.STALE_BASE
    assert path.read_bytes() == before


def test_malformed_nested_projection_has_a_typed_refusal(shop):
    request = bundle(shop[0])
    view = json.loads(request["view_bytes"])
    view["records"] = []
    request["view_bytes"] = canonical(view)
    request["contract"]["projection_sha256"] = digest(request["view_bytes"])
    with pytest.raises(consumer.ReentryRefusal) as refusal:
        assess(consumer, request)
    assert refusal.value.reason is consumer.Reason.MALFORMED_INPUT

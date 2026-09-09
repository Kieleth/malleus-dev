"""Connected public history, not another isolated replacement-policy probe."""

from copy import deepcopy
import importlib
import json
from pathlib import Path

import pytest
import malleus.compiler as api


MODULE = (
    "research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run"
)


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(MODULE)


@pytest.fixture(scope="module")
def executed(subject, tmp_path_factory):
    path = tmp_path_factory.mktemp("connected-shop") / "history.jsonl"
    original = Path.read_bytes

    def read(path):
        if path.name == "source_expectations.json":
            pytest.fail("The producer must not read its independent answer key")
        return original(path)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(Path, "read_bytes", read)
        return path, subject.run_story(path)


def test_state_role_is_one_ontology_category(subject):
    compiled = subject.compile_shop()
    profile, program = subject.history_configuration()
    assert json.loads(profile.canonical_bytes)["ontology_roles"]["state"] == [
        "RecordedOrderState"
    ]
    instruction = json.loads(program.canonical_bytes)["admission_rules"]["instructions"]
    assert instruction == [
        {
            "opcode": "REQUIRE_TYPES_IN_ROLE",
            "selection": "REPLACEMENTS",
            "role": "state",
            "match": "SUBTYPE",
            "refusal": "REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE",
        }
    ]
    view = compiled.view
    for name in ("SalesOrderState", "SupplierOrderState"):
        assert view.is_subtype_of(name, "RecordedOrderState")
    for name in ("InventoryUnit", "ShopOccurrence", "SupplierOrder"):
        assert not view.is_subtype_of(name, "RecordedOrderState")


def test_all_source_rows_fields_and_occurrences_are_accounted(subject, executed):
    _, result = executed
    graph = result.graph
    rows, boundary = subject.load_sources(subject.HERE)
    assert {r["id"] for r in graph.query("ShopOccurrence")} == set(
        boundary["selected_event_ids"]
    )
    assert len(result.change_sets) == len(rows) == 21
    covered = set()
    for ordinal, row in enumerate(rows):
        # Read authoritative retained plans, not mapper output.
        plan = json.loads(
            result.retained_bytes(f"plan:shop-connected:{row['event_id']}")
        )
        for item in plan["derivations"] + plan["gaps"]:
            if item["source_id"] == subject.SOURCE_ID:
                covered.add(item["locator"].split("[", 1)[0])
        assert graph.get_node(row["event_id"])["time_text"] == row["time_text"]
        assert f"row:{ordinal}:event_id" in covered
    expected = {f"row:{i}:{field}" for i, row in enumerate(rows) for field in row}
    assert covered == expected
    assert len(expected) == 123
    for record_id in result.record_history:
        trace = api.trace_population_record(result, record_id)
        assert (
            next(x.content for x in trace.sources if x.record_id == subject.SOURCE_ID)
            == (subject.HERE / "sources/table-1.jsonl").read_bytes()
        )


def test_order_state_changes_without_erasing_occurrences_or_units(subject, executed):
    _, result = executed
    graph = result.graph
    assert {
        (r["order_id"], r["product_code"], r["ordered_quantity"])
        for r in graph.query("SalesOrderState")
    } == {
        ("order:O1", "X", 2),
        ("order:O1", "Y", 1),
        ("order:O2", "X", 1),
        ("order:O2", "Y", 1),
    }
    assert {
        (r["order_id"], r["product_code"], r["ordered_quantity"])
        for r in graph.query("SupplierOrderState")
    } == {("supplier-order:A", "X", 3), ("supplier-order:B", "Y", 2)}
    assert result.record_history["state:supplier-order:B:Y:e4"].superseded_by == (
        "state:supplier-order:B:Y:e7"
    )
    for record_id in ("e4", "e7", "item:Y1", "item:Y2"):
        assert result.record_history[record_id].superseded_by is None
    assert {r["source_identifier"] for r in graph.query("InventoryUnit")} == {
        "X1",
        "X2",
        "X3",
        "Y1",
        "Y2",
    }


def test_reader_joins_the_connected_story_without_inventing_invoice_values(
    subject, executed
):
    _, result = executed
    account = subject.explain(result)
    assert account["invoice_orders"] == {"I1": ["O1"], "I2": ["O2"]}
    assert account["payment_invoices"] == {"P1": ["I1", "I2"]}
    assert account["packed_units"] == {"O1": ["X1", "X2", "Y1"], "O2": ["X3", "Y2"]}
    assert account["received_units"] == {"A": ["X1", "X2", "X3"], "B": ["Y1", "Y2"]}
    assert account["invoice_updates"] == [{"event_id": "e9", "invoices": ["I2"]}]
    assert account["packing_witnesses"] == {"O1": ["e27"], "O2": ["e33"]}
    assert account["shipment_eligibility"] == "NOT_EVALUATED"
    assert len(account["source_gaps"]) == 3
    assert {x["kind"] for x in account["source_gaps"]} == {
        "INTERVAL_NOT_EXPRESSIBLE",
        "REQUIRED_FIELD_ABSENT_IN_SOURCE",
    }
    assert len(result.graph.query_event_participations(event_id="e27")) == 5
    for invoice in result.graph.query("Invoice"):
        assert "amount" not in invoice


def test_reopen_incremental_and_repeat_preserve_exact_account(
    subject, executed, tmp_path
):
    path, result = executed
    reopened = api.KnowledgeChangeHistory.reopen(path).replay()
    reader = api.KnowledgeHistoryProjection.open(path)
    maintained = reader.refresh(
        expected_head_hash=result.ledger_head,
        expected_event_count=result.ledger_event_count,
    )
    for replay in (reopened, maintained):
        assert replay.receipt == result.receipt
        assert replay.record_history == result.record_history
        assert subject.explain(replay) == subject.explain(result)
    second = tmp_path / "repeat.jsonl"
    repeated = subject.run_story(second)
    assert second.read_bytes() == path.read_bytes()
    assert subject.explain(repeated) == subject.explain(result)


@pytest.mark.parametrize("text", ["one Y", "1·Y, 2·Y", "0·Y", "1·", "1.5·Y"])
def test_quantity_grammar_refuses_ambiguity_without_regex(subject, text):
    with pytest.raises(ValueError, match="quantity"):
        subject.parse_quantities(text)


def test_occurrence_replacement_refuses_at_real_admission_boundary(
    subject, executed, tmp_path
):
    source_path, _ = executed
    path = tmp_path / "refusal.jsonl"
    path.write_bytes(source_path.read_bytes())
    history = api.KnowledgeChangeHistory.reopen(path)
    before = history.replay()
    plan = json.loads(before.retained_bytes("plan:shop-connected:e9"))
    plan["plan_id"] = "plan:hostile:replace-e9"
    plan["records"]["entities"] = []
    replacements = {
        record["id"]: record["id"] + ":hostile"
        for family in ("events", "event_participations")
        for record in plan["records"][family]
    }
    for family in ("events", "event_participations"):
        for record in plan["records"][family]:
            record["id"] = replacements[record["id"]]
            if "event_id" in record["properties"]:
                record["properties"]["event_id"] = replacements["e9"]
    plan["derivations"] = [
        dict(deepcopy(item), record_id=replacements[item["record_id"]])
        for item in plan["derivations"]
        if item["record_id"] in replacements
    ]
    plan["supersessions"] = [
        {"record_id": new, "supersedes_record_id": old}
        for old, new in replacements.items()
    ]
    prepared = subject.prepare(history, plan)
    admission_bytes = path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time=subject.TIME,
            actor_id=subject.ACTOR,
        )
    assert refused.value.reason.name == "TRANSITION_RULE_REFUSAL"
    assert path.read_bytes() == admission_bytes
    after = api.KnowledgeChangeHistory.reopen(path).replay()
    assert after.graph.snapshot() == before.graph.snapshot()
    assert after.change_sets == before.change_sets

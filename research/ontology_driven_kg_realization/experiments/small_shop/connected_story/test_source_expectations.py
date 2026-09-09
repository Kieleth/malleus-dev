"""Check the independently written source answer key, not a graph's answers."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    inspect_sources,
    load_sources,
)


DIRECTORY = Path(__file__).parent


def _inputs():
    rows, boundary = load_sources(DIRECTORY)
    inspect_sources(rows, boundary)
    context = [
        json.loads(line)
        for line in (DIRECTORY / "sources/context.jsonl").read_bytes().splitlines()
    ]
    answers = json.loads((DIRECTORY / "source_expectations.json").read_bytes())
    return answers, {"table": rows, "context": context}


def _check_witnesses(answers, sources):
    ids = [case["id"] for case in answers["cases"]]
    assert len(set(ids)) == len(ids), "repeated answer case"
    for case in answers["cases"]:
        assert case["question"] and case["expected"] and case["witnesses"]
        for witness in case["witnesses"]:
            kind, ordinal, field = witness["locator"].split(":")
            assert kind == "row" and ordinal.isdecimal(), "invalid witness locator"
            rows = sources[witness["source"]]
            index = int(ordinal)
            assert index < len(rows), "witness row absent"
            row = rows[index]
            assert field in row, "witness field absent"
            assert row[field] == witness["value"], "witness bytes/value differ"


def test_answer_key_is_source_bound_and_explicitly_not_a_graph_result():
    answers, sources = _inputs()
    _check_witnesses(answers, sources)
    assert answers["status"] == "SOURCE_EXPECTATIONS_NOT_GRAPH_RESULTS"
    assert answers["human_ratification"] == "PENDING"
    assert answers["scope"] == "shop-connected-table1-v1"
    assert {case["id"] for case in answers["cases"]} == {
        "requested-items",
        "supplier-quantity-correction",
        "physical-unit-routing",
        "invoice-ownership",
        "payment-clearing",
        "invoice-update-gap",
        "shared-customer-policy",
        "unresolved-time",
        "multi-object-packing",
    }


def test_joined_business_expectations_are_independent_literals():
    answers, _ = _inputs()
    cases = {case["id"]: case["expected"] for case in answers["cases"]}
    assert cases["requested-items"] == {"O1": {"X": 2, "Y": 1}, "O2": {"X": 1, "Y": 1}}
    assert cases["supplier-quantity-correction"] == {
        "A/e3": {"X": 3},
        "B/e4": {"Y": 1},
        "B/e7": {"Y": 2},
        "interpretation": "B/e7 corrects B/e4, not a second independent order",
    }
    assert cases["invoice-ownership"] == {"I1": "O1", "I2": "O2"}
    assert cases["payment-clearing"] == {
        "payment": "P1",
        "received_at": "e29",
        "cleared_at": "e30",
        "invoices": ["I1", "I2"],
        "amount": "NOT_STATED",
    }
    assert cases["physical-unit-routing"]["packed_for"] == {
        "O1/e27": ["X1", "X2", "Y1"],
        "O2/e33": ["X3", "Y2"],
    }
    assert cases["physical-unit-routing"]["unit_replacements"] == []


def test_gaps_and_policy_are_not_filled_from_absence():
    answers, _ = _inputs()
    cases = {case["id"]: case["expected"] for case in answers["cases"]}
    assert cases["invoice-update-gap"] == {
        "event": "e9",
        "invoice": "I2",
        "changed_field": "NOT_STATED",
        "new_value": "NOT_STATED",
        "replacement_value_record": "NOT_JUSTIFIED",
    }
    assert cases["shared-customer-policy"]["customer_identifier"] == "NOT_STATED"
    assert (
        cases["shared-customer-policy"]["unpaid_count_from_missing_payment"]
        == "NOT_JUSTIFIED"
    )
    assert (
        cases["shared-customer-policy"]["shipment_authorization"] == "NOT_ESTABLISHED"
    )
    assert cases["unresolved-time"] == {
        "year": "NOT_STATED",
        "timezone": "NOT_STATED",
        "e6": "00-01 10:00",
        "e8": "00-01 10:30",
        "domain_order_from_row_number": "NOT_JUSTIFIED",
        "elapsed_duration": "NOT_COMPUTED",
    }


@pytest.mark.parametrize(
    "mutation", ["missing-row", "missing-field", "wrong-value", "duplicate-case"]
)
def test_broken_answer_key_witnesses_do_not_pass(mutation):
    answers, sources = _inputs()
    broken = deepcopy(answers)
    witness = broken["cases"][0]["witnesses"][0]
    if mutation == "missing-row":
        witness["locator"] = "row:21:order_ids"
    elif mutation == "missing-field":
        witness["locator"] = "row:0:invented_invoice_amount"
    elif mutation == "wrong-value":
        witness["value"] = ["O2"]
    else:
        broken["cases"].append(deepcopy(broken["cases"][0]))
    with pytest.raises(AssertionError):
        _check_witnesses(broken, sources)

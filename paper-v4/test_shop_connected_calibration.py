"""The connected Shop figures in the manuscript are read from a fresh chain run."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper-v4/manuscript-v4-working.md"
SHOP = "research.ontology_driven_kg_realization.experiments.small_shop"
STORY = f"{SHOP}.connected_story"
FIGURE_14 = "source:connected-shop:figure-14"

STAGE_PROBE = """
import json, sys
import malleus.compiler as api

replay = api.KnowledgeChangeHistory.reopen(sys.argv[1]).replay()
families = replay.graph.export_records()
current = {record["id"] for family in families.values() for record in family}
states = [r for r in families["entities"] if r["type"].endswith("OrderState")]
revisions = [json.loads(r.canonical_bytes) for r in replay.contract_revisions]
print(json.dumps({
    "changes": len(replay.change_sets),
    "ledger_events": replay.ledger_event_count,
    "contract_revisions": len(revisions),
    "contract_identity": replay.partial_contract.identity,
    "historical_records": len(replay.record_history),
    "current_records": len(current),
    "counts": {family: len(records) for family, records in families.items()},
    "superseded_records": [i for i in replay.record_history if i not in current],
    "states": states,
    "occurrence_ids": sorted(r["id"] for r in families["events"]),
    "revision_changes": [c for r in revisions for c in r["changes"]],
    "revision_kinds": [sorted({c["kind"] for c in r["changes"]}) for r in revisions],
    "revision_from": [r["from_contract_identity"] for r in revisions],
    "retained": {i.record_id: i.media_type for i in replay.retained_inputs},
    "retained_source_rows": {
        name: len(replay.retained_bytes(name).splitlines())
        for name in sys.argv[2:]
    },
}))
"""

REFUSAL_PROBE = f"""
from copy import deepcopy
import json, sys
from pathlib import Path
import malleus.compiler as api
from {STORY} import run as subject

path = Path(sys.argv[1])
history = api.KnowledgeChangeHistory.reopen(path)
before = history.replay()
plan = json.loads(before.retained_bytes("plan:shop-connected:e9"))
plan["plan_id"] = "plan:hostile:replace-e9"
plan["records"]["entities"] = []
families = ("events", "event_participations")
new_ids = {{
    record["id"]: record["id"] + ":hostile"
    for family in families
    for record in plan["records"][family]
}}
for family in families:
    for record in plan["records"][family]:
        record["id"] = new_ids[record["id"]]
        if "event_id" in record["properties"]:
            record["properties"]["event_id"] = new_ids["e9"]
plan["derivations"] = [
    dict(deepcopy(item), record_id=new_ids[item["record_id"]])
    for item in plan["derivations"]
    if item["record_id"] in new_ids
]
plan["supersessions"] = [
    {{"record_id": new, "supersedes_record_id": old}} for old, new in new_ids.items()
]
opened = path.read_bytes()
prepared = subject.prepare(history, plan)
snapshot = path.read_bytes()
try:
    api.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=subject.TIME,
        actor_id=subject.ACTOR,
    )
except api.KnowledgeChangeRefusal as refused:
    reason, detail = refused.reason.name, refused.detail
else:
    raise SystemExit("The occurrence replacement was admitted")
code, operations = detail.split(": operations ", 1)
after = api.KnowledgeChangeHistory.reopen(path).replay()
print(json.dumps({{
    "candidate_plan_id": plan["plan_id"],
    "change_sets_unchanged": after.change_sets == before.change_sets,
    "graph_unchanged": after.graph.snapshot() == before.graph.snapshot(),
    "ledger_unchanged": path.read_bytes() == snapshot,
    "preparation_retained_evidence": len(snapshot) > len(opened),
    "reason": reason,
    "refusal_code": code,
    "refused_record_ids": [record for _, record in json.loads(operations)],
}}))
"""


def shop_process(*args):
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env={
            "PYTHONPATH": f"{ROOT}:{ROOT / 'src'}",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PATH": os.environ["PATH"],
        },
        capture_output=True,
        text=True,
    )


def shop_python(*args):
    completed = shop_process(*args)
    assert completed.returncode == 0, completed.stderr[-2000:]
    return completed.stdout


def run_module(name, *args):
    return shop_python("-m", name, *args)


def json_tail(text):
    return json.loads(text[text.index("{") :])


def queue_pairs(queue, outcome):
    return [pair for pair in queue["pairs"] if pair["outcome"] == outcome]


def run_chain(tmp_path):
    """Rebuild the connected history from empty, in its documented order."""
    history = tmp_path / "history.jsonl"
    table_1 = json_tail(run_module(f"{STORY}.run", str(history)))
    baseline = tmp_path / "table-1.jsonl"
    shutil.copyfile(history, baseline)
    baseline_bytes = baseline.stat().st_size
    views = json_tail(run_module(f"{STORY}.object_timelines", str(history)))
    table_1_probe = json_tail(shop_python("-c", STAGE_PROBE, str(history)))
    supplier_b = next(
        state
        for state in table_1_probe["states"]
        if state["properties"]["order_id"] == "supplier-order:B"
    )
    warehouse = json_tail(
        run_module(f"{STORY}.warehouse.run", str(history), "--append")
    )
    warehouse_report = json_tail(
        run_module(f"{STORY}.warehouse.run", str(history), "--reopen")
    )
    warehouse_probe = json_tail(shop_python("-c", STAGE_PROBE, str(history), FIGURE_14))
    ordering = json_tail(run_module(f"{STORY}.warehouse.ordering", str(history)))
    warehouse_bytes = history.stat().st_size
    shipments = json_tail(
        run_module(f"{STORY}.partial_shipments.run", str(history), "--append")
    )
    shipments_probe = json_tail(shop_python("-c", STAGE_PROBE, str(history)))
    wrong_prefixes = {
        # The shipment extension expects the warehouse history, not Table 1 alone.
        f"{STORY}.partial_shipments.run": baseline,
        # The warehouse extension expects Table 1, not a history already extended.
        f"{STORY}.warehouse.run": history,
    }
    refused_appends = {}
    for module, source in wrong_prefixes.items():
        target = tmp_path / f"wrong-{module.rsplit('.', 2)[1]}.jsonl"
        shutil.copyfile(source, target)
        before = target.stat().st_size
        attempt = shop_process("-m", module, str(target), "--append")
        refused_appends[module] = {
            "returncode": attempt.returncode,
            "wrote_nothing": target.stat().st_size == before,
        }
    refusal = json_tail(
        shop_python(
            "-c", REFUSAL_PROBE, str(shutil.copy(baseline, tmp_path / "r.jsonl"))
        )
    )
    policy = (
        json_tail(
            run_module(
                f"{SHOP}.shipment_policy.run", "--history", str(tmp_path / "p.jsonl")
            )
        )
        if shutil.which("swipl")
        else None
    )
    checkpoints = shipments["checkpoints"]
    x1 = warehouse_report["objects"]["item:X1"]
    return {
        "table_1": {
            "changes": table_1["changes"],
            "ledger_events": table_1["ledger_events"],
            "contract_revisions": table_1_probe["contract_revisions"],
            "contract_identity": table_1_probe["contract_identity"],
            "historical_records": table_1["historical_records"],
            "current_records": table_1_probe["current_records"],
            "objects": len(views["objects"]),
            "occurrences": table_1_probe["counts"]["events"],
            "participations": table_1_probe["counts"]["event_participations"],
            "superseded_records": table_1_probe["superseded_records"],
            "current_supplier_b": {
                "id": supplier_b["id"],
                "ordered_quantity": supplier_b["properties"]["ordered_quantity"],
            },
            "retained_occurrences": [
                event
                for event in table_1_probe["occurrence_ids"]
                if event in {"e4", "e7"}
            ],
            "source_gaps": len(table_1["account"]["source_gaps"]),
            "bytes": baseline_bytes,
            "history_sha256": table_1["history_sha256"],
            "object_views": views["objects"],
        },
        "retained": warehouse_probe["retained"],
        "wrong_prefix_appends": refused_appends,
        "source_inventory": json_tail(run_module(f"{STORY}.source_boundary")),
        "warehouse": {
            "changes": warehouse["changes"],
            "contract_revisions": warehouse["contract_revisions"],
            "protocol_events": warehouse["protocol_events"],
            "historical_records": warehouse["historical_records"],
            "objects": len(warehouse_report["objects"]),
            "occurrences": warehouse_probe["counts"]["events"],
            "participations": warehouse_probe["counts"]["event_participations"],
            "baseline_prefix_preserved": warehouse["baseline_prefix_preserved"],
            "baseline_bytes": baseline_bytes,
            "baseline_digest_matches": warehouse["baseline_history_sha256"]
            == table_1["history_sha256"],
            "revision_from_table_1": warehouse_probe["revision_from"]
            == [table_1_probe["contract_identity"]],
            "new_activity_values": sorted(
                change["value"]
                for change in warehouse_probe["revision_changes"]
                if change["kind"] == "ADD_ENUM_VALUE"
            ),
            "revision_change_kinds": sorted(
                {change["kind"] for change in warehouse_probe["revision_changes"]}
            ),
            "history_bytes": warehouse["history_bytes"],
            "history_sha256": warehouse["history_sha256"],
            "warehouse_source_rows": warehouse_probe["retained_source_rows"][FIGURE_14],
            "x1_path": [
                [
                    warehouse_report["events"][event]["event_type"],
                    event,
                    warehouse_report["events"][event]["time_text"],
                ]
                for group in x1["printed_sequence"]
                for event in group
            ],
        },
        "ordering": {
            "units": ordering["units"],
            "counts": {
                name: queue["counts"] for name, queue in ordering["queues"].items()
            },
            "reversed_pairs": {
                name: [pair["units"] for pair in queue_pairs(queue, "REVERSED")]
                for name, queue in ordering["queues"].items()
                if queue_pairs(queue, "REVERSED")
            },
            "undetermined_reasons": {
                name: {
                    issue["reason"]
                    for pair in queue_pairs(queue, "UNDETERMINED")
                    for issue in pair["issues"]
                }
                for name, queue in ordering["queues"].items()
            },
            "undetermined_units": {
                name: sorted(
                    set.intersection(
                        *(
                            set(pair["units"])
                            for pair in queue_pairs(queue, "UNDETERMINED")
                        )
                    )
                )[0]
                for name, queue in ordering["queues"].items()
            },
            "observations": {
                event: [
                    report["event_type"],
                    report["units"][0],
                    report["time_text"],
                ]
                for event, report in ordering["observations"].items()
                if event in {"e8", "e20", "e21", "e24", "e26"}
            },
        },
        "e12_report": ordering["observations"]["e12"],
        "shipments": {
            "changes": shipments["changes"],
            "contract_revisions": shipments["contract_revisions"],
            "protocol_events": shipments["protocol_events"],
            "historical_records": shipments["historical_records"],
            "baseline_prefix_preserved": shipments["baseline_prefix_preserved"],
            "baseline_bytes": warehouse_bytes,
            "baseline_digest_matches": shipments["baseline_history_sha256"]
            == warehouse["history_sha256"],
            "duplicate_assignment_rule": shipments["duplicate_assignment_rule"],
            "revision_kinds": shipments_probe["revision_kinds"],
            "history_sha256": shipments["history_sha256"],
            "remaining_units": [
                len(checkpoints[name]["remaining_units"])
                for name in (
                    "after_order",
                    "after_first_shipment",
                    "after_second_shipment",
                )
            ],
        },
        "refusal": refusal,
        "policy": policy,
    }


def manuscript_text():
    return MANUSCRIPT.read_text()


def manuscript_prose():
    """One line, so an assertion binds a claim and not a line break."""
    return " ".join(MANUSCRIPT.read_text().split())


def printed_sections():
    """Section 3 and Appendix B, the two regions this chain's figures print in."""
    body = manuscript_text()
    # Section 3 gained a second subsection on 2026-09-18 (the Shop staged
    # reconsideration), so its heading no longer says "with no model"; the
    # connected chain's own figures print in 3.1 and in Appendix B.
    section_3 = body.split("## 3. Results on the Small Shop", 1)[1].split("\n## 4. ", 1)[0]
    return section_3 + "\n\n" + body.split("## Appendix B.", 1)[1]


def appendix_exhibits():
    appendix = manuscript_text().split("## Appendix B.", 1)[1]
    return [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", appendix, re.S)]


@pytest.fixture(scope="module")
def chain(tmp_path_factory):
    return run_chain(tmp_path_factory.mktemp("connected-shop"))


def test_table_1_stage_row_matches_a_fresh_run(chain):
    stage = chain["table_1"]
    assert stage["changes"] == 21 and stage["contract_revisions"] == 0
    assert stage["ledger_events"] == 121
    assert stage["historical_records"] == 107 and stage["current_records"] == 106
    assert stage["objects"] == 17
    assert stage["occurrences"] == 21 and stage["participations"] == 62
    assert stage["superseded_records"] == ["state:supplier-order:B:Y:e4"]
    assert stage["current_supplier_b"] == {
        "id": "state:supplier-order:B:Y:e7",
        "ordered_quantity": 2,
    }
    assert stage["retained_occurrences"] == ["e4", "e7"]
    assert stage["source_gaps"] == 3
    assert stage["bytes"] == 895097
    assert "| Table 1 population | 21 / 0 | 121 |" in manuscript_text()
    assert "895,097 bytes" in manuscript_text()


def test_source_inventory_accounts_for_every_field(chain):
    inventory = chain["source_inventory"]
    assert inventory["selected_rows"] == 21
    assert inventory["nonempty_fields"] == 123
    assert inventory["unaccounted_fields"] == []
    assert "disposition to each of the 123 nonempty fields in those 21 rows" in (
        manuscript_prose()
    )


def test_both_sources_and_their_images_are_retained(chain):
    retained = chain["retained"]
    assert retained["source:connected-shop:table-1"] == "application/x-ndjson"
    assert retained[FIGURE_14] == "application/x-ndjson"
    assert retained["artifact:connected-shop:table-image"] == "image/png"
    assert retained["artifact:connected-shop:figure-14-image"] == "image/png"
    assert (
        "retained in the history with their exact bytes and with the" in manuscript_prose()
    )


def test_each_extension_refuses_a_prefix_it_does_not_expect(chain):
    attempts = chain["wrong_prefix_appends"]
    assert len(attempts) == 2
    for module, attempt in attempts.items():
        assert attempt["returncode"] != 0, module
        assert attempt["wrote_nothing"] is True, module
    assert "a wrong prefix refuses before any write" in manuscript_prose()


def test_warehouse_stage_row_matches_a_fresh_run(chain):
    stage = chain["warehouse"]
    assert stage["changes"] == 34 and stage["contract_revisions"] == 1
    assert stage["protocol_events"] == 193
    assert stage["historical_records"] == 133
    assert stage["objects"] == 17
    assert stage["occurrences"] == 34 and stage["participations"] == 75
    assert stage["baseline_prefix_preserved"] is True
    assert stage["baseline_digest_matches"] is True
    assert stage["baseline_bytes"] == 895097
    assert stage["revision_change_kinds"] == ["ADD_ENUM_VALUE"]
    assert stage["new_activity_values"] == ["RETRIEVE", "SCAN", "STORE"]
    assert stage["revision_from_table_1"] is True
    assert stage["history_bytes"] == 1646836
    assert stage["warehouse_source_rows"] == 13
    assert "| Figure 14 warehouse extension | 34 / 1 | 193 |" in manuscript_text()
    assert "1,646,836 bytes" in manuscript_text()
    assert "13 warehouse observations" in manuscript_prose()


def test_unit_x1_path_matches_a_fresh_run(chain):
    assert chain["warehouse"]["x1_path"] == [
        ["UNPACK", "e10", "04-05 11:00"],
        ["SCAN", "e12", "04-05 13:00"],
        ["STORE", "e13", "04-05 13:15"],
        ["RETRIEVE", "e22", "07-05 11:15"],
        ["PACK_SHIPMENT", "e27", "07-05 17:00"],
    ]
    assert (
        "Unpack e10 at 04-05 11:00, Scan e12 at 13:00, "
        "Store e13 at 13:15, Retrieve e22 at 07-05 11:15, Pack e27 at 17:00"
    ) in manuscript_prose()


def test_invoice_i2_view_matches_a_fresh_run(chain):
    views = chain["table_1"]["object_views"]
    assert len(views) == 17
    assert views["invoice:I2"]["printed_sequence"] == [["e5"], ["e9"], ["e30"]]
    for name in ("invoice:I1", "payment:P1"):
        assert "e30" in views[name]["event_ids"]
    assert "creation e5, update e9 and clearing e30" in manuscript_prose()


def test_ordering_comparison_matches_a_fresh_run(chain):
    ordering = chain["ordering"]
    assert ordering["units"] == ["item:X1", "item:X2", "item:X3", "item:Y1", "item:Y2"]
    assert ordering["counts"] == {
        "UNPACK:SCAN": {"PRESERVED": 5, "REVERSED": 1, "UNDETERMINED": 4},
        "SCAN:STORE": {"PRESERVED": 6, "REVERSED": 0, "UNDETERMINED": 4},
        "STORE:RETRIEVE": {"PRESERVED": 6, "REVERSED": 0, "UNDETERMINED": 4},
    }
    assert ordering["reversed_pairs"] == {"UNPACK:SCAN": [["item:Y1", "item:Y2"]]}
    assert ordering["undetermined_reasons"] == {
        "UNPACK:SCAN": {"UNPLACED_TIME"},
        "SCAN:STORE": {"MISSING_OBSERVATION"},
        "STORE:RETRIEVE": {"MISSING_OBSERVATION"},
    }
    assert ordering["undetermined_units"] == {
        "UNPACK:SCAN": "item:X3",
        "SCAN:STORE": "item:Y1",
        "STORE:RETRIEVE": "item:Y1",
    }
    assert ordering["observations"] == {
        "e8": ["UNPACK", "item:X3", "00-01 10:30"],
        "e20": ["UNPACK", "item:Y1", "07-05 10:45"],
        "e21": ["UNPACK", "item:Y2", "07-05 11:00"],
        "e24": ["SCAN", "item:Y2", "07-05 13:00"],
        "e26": ["SCAN", "item:Y1", "07-05 15:00"],
    }
    text = manuscript_prose()
    assert (
        "preserves the order in 5 pairs, reverses it in 1 and cannot compare 4" in text
    )
    assert "each preserve 6 and cannot compare 4" in text
    assert "Y1 was unpacked at 07-05 10:45 and scanned at 15:00" in text
    assert "Y2 was unpacked at 11:00 and scanned at 13:00" in text
    assert "printed 00-01 10:30 and is unusable" in text
    assert "no retained Store or Retrieve observation" in text


def test_shipment_stage_row_matches_a_fresh_run(chain):
    stage = chain["shipments"]
    assert stage["changes"] == 37 and stage["contract_revisions"] == 2
    assert stage["protocol_events"] == 216
    assert stage["historical_records"] == 144
    assert stage["baseline_prefix_preserved"] is True
    assert stage["baseline_digest_matches"] is True
    assert stage["baseline_bytes"] == 1646836
    assert stage["remaining_units"] == [2, 1, 0]
    assert stage["duplicate_assignment_rule"] == "NOT_SELECTED"
    assert stage["revision_kinds"] == [["ADD_ENUM_VALUE"], ["ADD_CLASS", "ADD_SLOT"]]
    assert "| Synthetic partial shipments | 37 / 2 | 216 |" in manuscript_text()
    assert "queried after each step as 2, 1, then 0" in manuscript_prose()
    assert (
        "four synthetic shipment classes and two slots through a second"
        in manuscript_prose()
    )
    assert "does not reject a duplicate unit assignment" in manuscript_prose()


def test_ledger_digests_in_the_appendix_match_a_fresh_run(chain):
    text = manuscript_text()
    for stage in ("table_1", "warehouse", "shipments"):
        digest = chain[stage]["history_sha256"].removeprefix("sha256:")
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert digest in text


def test_record_trace_exhibit_matches_a_fresh_run(chain):
    observed = chain["e12_report"]
    own = [w for w in observed["witnesses"] if w["record_id"] == "e12"]
    other = [w for w in observed["witnesses"] if w["record_id"] != "e12"]
    assert len(observed["witnesses"]) == 6 and len(other) == 3
    assert {w["record_id"] for w in other} == {"participation:e12:item:X1"}
    assert {w["source_id"] for w in observed["witnesses"]} == {FIGURE_14}
    assert appendix_exhibits()[0] == {"e12": {**observed, "witnesses": own}}
    assert "six witnesses" in manuscript_prose()


def test_occurrence_replacement_refusal_exhibit_matches_a_fresh_run(chain):
    refusal = chain["refusal"]
    assert refusal["reason"] == "TRANSITION_RULE_REFUSAL"
    assert refusal["refusal_code"] == "REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE"
    assert refusal["ledger_unchanged"] is True
    assert refusal["graph_unchanged"] is True
    assert refusal["change_sets_unchanged"] is True
    assert refusal["preparation_retained_evidence"] is True
    assert len(refusal["refused_record_ids"]) == 3
    assert appendix_exhibits()[1] == {"occurrence_replacement": refusal}
    text = manuscript_prose()
    assert (
        "TRANSITION_RULE_REFUSAL under the rule REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE"
        in text
    )
    assert "the three refused record identifiers named" in text
    assert "retains its evidence in an earlier separate transaction" in text


@pytest.mark.skipif(shutil.which("swipl") is None, reason="SWI-Prolog is not on PATH")
def test_shipment_policy_refusal_exhibit_matches_a_fresh_run(chain):
    report = chain["policy"]
    assert report["accepted_changes"] == 3 and report["event_count"] == 31
    assert report["duplicate_unit"]["outcome"] == "VIOLATED"
    assert report["duplicate_unit"]["ledger_unchanged"] is True
    assert appendix_exhibits()[2] == {"duplicate_unit": report["duplicate_unit"]}
    assert "3 accepted changes and 31 ledger events" in manuscript_prose()


def test_the_abstract_sentence_matches_a_fresh_chain(chain):
    """The one abstract sentence about the Small Shop, against the same run."""
    rows = chain["source_inventory"]["selected_rows"]
    warehouse, shipments = chain["warehouse"], chain["shipments"]
    assert rows == 21 and warehouse["warehouse_source_rows"] == 13
    assert warehouse["contract_revisions"] == 1
    assert shipments["contract_revisions"] == 2
    assert warehouse["revision_change_kinds"] == ["ADD_ENUM_VALUE"]
    assert shipments["revision_kinds"][1] == ["ADD_CLASS", "ADD_SLOT"]
    assert warehouse["baseline_prefix_preserved"] is True
    assert shipments["baseline_prefix_preserved"] is True
    assert len(chain["table_1"]["superseded_records"]) == 1
    assert chain["refusal"]["ledger_unchanged"] is True
    abstract = " ".join(
        manuscript_text().split("## Abstract", 1)[1].split("## 1. ", 1)[0].split()
    )
    assert (
        "With no model in the loop, a transcribed published example crosses the "
        f"whole path as one connected history: {rows} table rows, then "
        f"{warehouse['warehouse_source_rows']} warehouse observations of the objects "
        "those rows created and a labelled synthetic shipment cohort, each of the "
        "two extensions entering through an additive contract revision and leaving "
        "the earlier ledger as an exact prefix, with a correction retained rather "
        "than rewritten and a candidate that would replace an admitted occurrence "
        "refused with the ledger unchanged."
    ) in abstract


def test_the_printed_sections_fit_the_submission_builder():
    body = printed_sections()
    tables = [block for block in body.split("\n\n") if block.startswith("|")]
    assert tables
    for table in tables:
        rows = [line.strip().strip("|").split("|") for line in table.splitlines()]
        assert len(rows[0]) in {4, 8}
        assert all(len(row) == len(rows[0]) for row in rows)
    assert not re.search(r"(?m)^(?:[-*] |\d+\. )", body)
    separators = {line for table in tables for line in table.splitlines()}
    assert not [
        line for line in body.splitlines() if "--" in line and line not in separators
    ]

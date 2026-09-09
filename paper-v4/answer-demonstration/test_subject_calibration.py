"""A query-only intervention must preserve knowledge and expose exact records."""

import json

from calibration import BASE
from review_packet import digest


RUN = BASE.parent / "sol-calibration-01/b"
QUERY = RUN / "subject-query-01"
CHANGED = {"CQ-T3-02", "CQ-T3-03", "CQ-T5-02", "CQ-C-05"}


def test_executed_method_is_the_approved_existing_reader():
    method = json.loads((QUERY / "method.json").read_bytes())
    assert method["code"] == {
        "answers.py": "sha256:1ace62715e813125fce9ec5b38278faae25018468069b22c52bf2d87ea1bbdb1",
        "subject_answers.py": "sha256:5c6d4506fbaa690a5c3b6995a83950c1c299cb56d54973a2991688f28e8e16d0",
        "subject_query.py": "sha256:337b8d3654597950b63b4ab8722c4051043d0448cac6595400f394b48f82d0dc",
        "binding.py": "sha256:c2390d9fcfcf28f922c0b42bf8f49db9bc26b6636a84f60154feab723785b6f9",
    }
    for name, identity in method["code"].items():
        assert digest((QUERY / name).read_bytes()) == identity
    assert (
        digest((RUN / "attempt-01/query-result.json").read_bytes())
        == (method["original_query_result_sha256"])
    )


def test_only_four_outputs_change_and_every_old_row_and_path_survives():
    old = json.loads((RUN / "attempt-01/query-result.json").read_bytes())
    new = json.loads((QUERY / "query-result.json").read_bytes())
    changes = set()
    added = []
    for before, after in zip(old["queries"], new["queries"], strict=True):
        assert before["question_id"] == after["question_id"]
        assert before["paths"] == after["paths"]
        assert all(row in after["rows"] for row in before["rows"])
        if before != after:
            changes.add(after["question_id"])
            assert len(after["rows"]) == len(before["rows"]) + 4
            added.extend(row for row in after["rows"] if row not in before["rows"])
    assert changes == CHANGED
    assert len(old["queries"]) == 30
    assert len(added) == 16
    assert len({row["witness"]["record_id"] for row in added}) == 8

    exported = json.loads((RUN / "attempt-01/export-records.json").read_bytes())
    nodes = {node["id"]: node for node in exported["entities"]}
    for row in added:
        witness = row["witness"]
        assert row["record"] == nodes[witness["record_id"]]["properties"]
        assert row["subject"] == nodes[witness["subject_id"]]["properties"]


def test_subject_pass_retains_the_same_accepted_state_and_zero_forbidden_reads():
    original = json.loads((RUN / "attempt-01/run-result.json").read_bytes())
    result = json.loads((QUERY / "query-result.json").read_bytes())
    for key in ("ledger_head", "replay_receipt_sha256"):
        assert result["inputs"][key] == original[key]
    assert result["historical_replay_matches"] is True
    assert result["ledger_bytes_unchanged"] is True
    assert result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert digest((RUN / "attempt-01/ledger/history.jsonl").read_bytes()) == (
        "sha256:7c92d1a6955a7e9e3ef6e80702234bad17df44259060e2e46d4158971bee8d1b"
    )
    assert (
        digest((RUN / "attempt-01/export-records.json").read_bytes())
        == (original["export_records_sha256"])
    )


def test_repeat_differs_only_in_declared_method_execution_timestamp():
    repeated = RUN / "subject-query-reproduction-01"
    left = {p.name: p.read_bytes() for p in QUERY.iterdir() if p.is_file()}
    right = {p.name: p.read_bytes() for p in repeated.iterdir() if p.is_file()}
    assert set(left) == set(right)
    assert len(left) == 8
    a, b = json.loads(left.pop("method.json")), json.loads(right.pop("method.json"))
    assert a.pop("frozen_at") != b.pop("frozen_at")
    assert a == b
    assert left == right


def test_common_witnesses_have_identical_review_projections():
    old = json.loads((RUN / "review-01/review-docket.json").read_bytes())
    new = json.loads((RUN / "subject-review-01/review-docket.json").read_bytes())
    a = {w["witness_key"]: w["projections"] for w in old["witnesses"]}
    b = {w["witness_key"]: w["projections"] for w in new["witnesses"]}
    assert len(a) == 28
    assert len(b) == 36
    assert set(a) < set(b)
    assert all(a[key] == b[key] for key in a)


def test_review_disagreement_is_not_counted_as_retrieval_gain():
    from selective_review import validate

    before = RUN / "review-01"
    after = RUN / "subject-review-01"
    a = validate(before, before / "review-record.md")
    b = validate(after, after / "review-record.md")
    comparison = json.loads((RUN / "subject-review-comparison.json").read_bytes())
    assert (
        digest((before / "review-record.md").read_bytes())
        == (comparison["before_review_sha256"])
    )
    assert (
        digest((after / "review-record.md").read_bytes())
        == (comparison["after_review_sha256"])
    )
    assert b["ratification"]["disposition"] == "PENDING"
    assert len(b["questions"]) == 30
    assert len(b["witnesses"]) == 36
    assert sum(len(q["coverage"]) for q in b["questions"]) == 121
    old_rows = {
        q["question_id"]: q
        for q in json.loads((before / "query-result.json").read_bytes())["queries"]
    }
    new_rows = {
        q["question_id"]: q
        for q in json.loads((after / "query-result.json").read_bytes())["queries"]
    }
    added_row_gains, unchanged_query_gains = 0, []
    for old, new, item in zip(
        a["questions"], b["questions"], comparison["questions"], strict=True
    ):
        key = old["question_id"]
        assert key == new["question_id"] == item["question_id"]
        assert item["before"] == old["question_responsiveness"]
        assert item["after"] == new["question_responsiveness"]
        assert item["query_changed"] == (old_rows[key] != new_rows[key])
        for left, right in zip(old["coverage"], new["coverage"], strict=True):
            assert left["semantic"] == right["semantic"]
            if left["row_index"] is None and right["row_index"] is not None:
                row = new_rows[key]["rows"][right["row_index"]]
                if row not in old_rows[key]["rows"]:
                    added_row_gains += 1
                if old_rows[key] == new_rows[key]:
                    unchanged_query_gains.append((key, right["semantic"]))
    assert added_row_gains == comparison["newly_covered_on_added_rows"] == 12
    assert (
        len(unchanged_query_gains)
        == comparison["newly_covered_on_unchanged_query"]
        == 2
    )
    assert unchanged_query_gains == [
        ("CQ-T3-04", "bounded_quantity"),
        ("CQ-T3-04", "length_unit"),
    ]

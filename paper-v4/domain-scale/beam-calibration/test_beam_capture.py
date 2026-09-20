"""Check the frozen result, including known defects, without repairing it.

These evidence tests do not certify semantic quality. They preserve a failed
numeric witness beside successful controls and independently rerun public replay.
"""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "private/beam-weather-calibration-01"
WORK = RUN / "producer/work"


def test_reopened_history_reproduces_records_and_receipt_without_ledger_changes(
    tmp_path,
):
    original = (WORK / "history.jsonl").read_bytes()
    assert hashlib.sha256(original).hexdigest() == (
        "1acc1efdc2160470697fcdc160dc0567592e47a66f3affe353d4616a5d1e06eb"
    )
    ledger = tmp_path / "history.jsonl"
    ledger.write_bytes(original)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.compiler_cli",
            "replay",
            "--ledger",
            str(ledger),
            "--records-out",
            str(tmp_path / "records.json"),
            "--receipt-out",
            str(tmp_path / "replay-receipt.json"),
        ],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(RUN / "runtime/src"),
        },
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode()
    for name in ("records.json", "replay-receipt.json"):
        assert (tmp_path / name).read_bytes() == (WORK / name).read_bytes()
    assert ledger.read_bytes() == original
    assert (WORK / "history.jsonl").read_bytes() == original


def test_frozen_numeric_failure_and_successful_controls_remain_inspectable():
    population = json.loads((WORK / "attempts/population-01.json").read_bytes())
    graph = json.loads((WORK / "records.json").read_bytes())
    entities = {record["id"]: record for record in graph["entities"]}
    assertions = {item["id"]: item for item in population["capture"]["assertions"]}
    wrong = entities["quantity:beam:1178"]["properties"]
    evidence = assertions[wrong["assertion_locator"]]
    assert evidence["block"] == "beam:100K:2:message:66"
    assert "1,200 calls per day" in evidence["statement"]
    assert wrong["reported_value_text"] == "200 calls per day"
    assert wrong["value_lower"] == wrong["value_upper"] == 200
    assert wrong["value_lower"] != 1200
    # A matching locator and statement digest did not prevent the wrong value.
    assert wrong["statement_sha256"] == (
        "sha256:" + hashlib.sha256(evidence["statement"].encode()).hexdigest()
    )
    for record_id, field, expected, block in (
        ("quantity:beam:544", "value_lower", 250, 38),
        ("quantity:beam:1382", "value_lower", 280, 80),
        ("ratio:beam:2273", "ratio_value", 0.78, 128),
    ):
        properties = entities[record_id]["properties"]
        assert properties[field] == expected
        assert assertions[properties["assertion_locator"]]["block"] == (
            f"beam:100K:2:message:{block}"
        )

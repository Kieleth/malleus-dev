"""A current producer must not silently rewrite an earlier evidence generation."""

from hashlib import sha256
import json
from pathlib import Path

import pytest


HERE = Path(__file__).parent
CURRENT = HERE / "evidence_2026_09_06"
HISTORICAL = {
    "correction/evidence-role-v1/explanation.json": "d55a5206d1114d77e02b66c6e0c55770ac69cb95d1afd209ad23d8435d7b31bf",
    "correction/evidence-role-v1/graph.json": "52652ddb7425562e36cd7f430a3c483b761067320a4eba30b8195fabcebe1645",
    "correction/evidence-role-v1/receipt.json": "1fe8f7f7f431d279dcebabf0c8c83093c7d0a8ed194d55f9dcfc0f0230228c6f",
    "object_event/evidence.json": "f504d6ef5fd6d742792280f04fb8e1cf7604f13425f8a99774f54f1b2179a57b",
    "showcase/evidence/explanation.json": "90497272ff3ffb5ae2572b4fede11e43336166c92a8fe22e0d3d298fd87c9254",
    "showcase/evidence/graph.json": "b92787c8bb07e977416c7b4996ef5dd60544becbe0ca7a39b9075756ba43a6a0",
    "showcase/evidence/queries.json": "86e24272e9de1e3fc3c70648e61b80a9ba0f6ce55e8ad3d0fb22880f1b55b86e",
    "showcase/evidence/receipt.json": "09b81985d03c810678704178fa3fb4c26f76b2b0077eb3bf9a3456e0d675ad41",
}


@pytest.mark.parametrize("path,expected", HISTORICAL.items())
def test_historical_evidence_remains_exact(path, expected):
    assert sha256((HERE / path).read_bytes()).hexdigest() == expected


@pytest.mark.parametrize(
    "group,previous", [("correction", "evidence-role-v1"), ("showcase", "evidence")]
)
def test_new_receipts_preserve_exact_graphs(group, previous):
    assert (CURRENT / group / "graph.json").read_bytes() == (
        HERE / group / previous / "graph.json"
    ).read_bytes()
    old = json.loads((HERE / group / previous / "receipt.json").read_bytes())
    new = json.loads((CURRENT / group / "receipt.json").read_bytes())
    changed = {key for key in old if old[key] != new[key]}
    assert changed == {
        "knowledge_change_set_identity",
        "ledger_head",
        "machine_state_identity",
    }
    assert old.keys() == new.keys()


def test_new_occurrence_evidence_changes_only_history_fingerprints():
    old = json.loads((HERE / "object_event/evidence.json").read_bytes())
    new = json.loads((CURRENT / "object_event/evidence.json").read_bytes())
    assert old.keys() == new.keys()
    assert {key for key in old if old[key] != new[key]} == {"history"}
    assert old["history"].keys() == new["history"].keys()
    assert {
        key for key in old["history"] if old["history"][key] != new["history"][key]
    } == {"ledger_head", "ledger_sha256", "receipt_identity"}

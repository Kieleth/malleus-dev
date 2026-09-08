"""Two valid histories, one current KG. No action or alternate genesis policy."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import malleus.compiler as api
import pytest

from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR,
    E4,
    E7,
    SOURCE,
    TIME,
    admit,
    artifact,
    canonical,
    complement,
    digest,
    load_plan,
    prepare,
)


CORE_COMMIT = "2af45e03ee7d7bf528cef8db42c0798e6d99685b"
CORE_PRODUCER = (
    "sha256:51c019d49c3cd7d75330e02c5d728a873254cc4b56ca122dda078b15c25bcb3f"
)


def require_runtime_origin(root, module_file):
    if not Path(module_file).resolve().is_relative_to(root / "src/malleus"):
        raise ValueError(
            f"Core origin mismatch: {module_file}; expected {root}/src/malleus"
        )


@pytest.fixture(scope="session", autouse=True)
def bound_runtime():
    if "MALLEUS_REENTRY_CORE_ROOT" not in os.environ:
        raise ValueError("Set MALLEUS_REENTRY_CORE_ROOT to the audited Core checkout")
    root = Path(os.environ["MALLEUS_REENTRY_CORE_ROOT"]).resolve()
    require_runtime_origin(root, api.__file__)
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] == "malleus" and getattr(module, "__file__", None):
            require_runtime_origin(root, module.__file__)
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    if head != CORE_COMMIT:
        raise ValueError(f"Core commit mismatch: {head}; expected {CORE_COMMIT}")
    subprocess.run(["git", "diff", "--exit-code", "HEAD"], cwd=root, check=True)
    return root


def test_runtime_origin_guard_rejects_another_checkout(bound_runtime, tmp_path):
    with pytest.raises(ValueError, match="Core origin mismatch"):
        require_runtime_origin(
            bound_runtime, tmp_path / "another/src/malleus/compiler.py"
        )


def test_distinct_histories_share_a_replayed_graph_but_not_context(shop, tmp_path):
    history, path = shop
    initial = history.replay()
    producer = json.loads(initial.contract_view.artifact_bytes)["evidence"]["producer"][
        "sha256"
    ]
    assert producer == CORE_PRODUCER
    prepared = prepare(history, load_plan(history, "supplier-e7"))
    admit(history, prepared)

    short_dir = tmp_path / "short-ledger-only"
    short_dir.mkdir()
    short_path = short_dir / "history.jsonl"
    shutil.copyfile(path, short_path)
    original_bytes = short_path.read_bytes()

    note_id = "artifact:replay-noninvertibility:conformance-note"
    note = canonical(
        {
            "classification": "CONFORMANCE_FIXTURE",
            "meaning": "Authored evidence-only note, not an external observation",
        }
    )
    history.append_anchors(
        anchors=(artifact(note_id, note),), transaction_time=TIME, actor_id=ACTOR
    )
    long_dir = tmp_path / "long-ledger-only"
    long_dir.mkdir()
    long_path = long_dir / "history.jsonl"
    shutil.copyfile(path, long_path)
    extended_bytes = long_path.read_bytes()

    short = api.KnowledgeChangeHistory.reopen(short_path).replay()
    long = api.KnowledgeChangeHistory.reopen(long_path).replay()
    for directory in (short_dir, long_dir):
        assert sorted(p.name for p in directory.iterdir()) == ["history.jsonl"]
    assert short_path.read_bytes() == original_bytes
    assert extended_bytes.startswith(original_bytes)
    assert extended_bytes != original_bytes
    assert long.ledger_event_count == short.ledger_event_count + 1
    assert long.ledger_head != short.ledger_head
    assert long.receipt.identity != short.receipt.identity

    assert long.partial_contract == short.partial_contract
    assert long.binding == short.binding
    assert long.acceptance_head == short.acceptance_head
    assert long.materialization_head == short.materialization_head
    assert long.change_sets == short.change_sets
    assert long.record_history == short.record_history
    assert long.graph.export_records() == short.graph.export_records()
    assert long.graph.state_digest() == short.graph.state_digest()
    assert complement(long) == complement(short) == complement(initial)
    assert long.retained_bytes(SOURCE) == short.retained_bytes(SOURCE)
    assert note_id not in {item.record_id for item in short.retained_inputs}
    assert long.retained_bytes(note_id) == note

    expected = [
        {
            "id": E7,
            "type": "SupplierOrderState",
            "supplier_order_id": "B",
            "product_code": "Y",
            "source_occurrence_id": "e7",
            "ordered_quantity": 2,
        }
    ]
    for replay in (short, long):
        assert (
            replay.graph.query("SupplierOrderState", supplier_order_id="B") == expected
        )
        assert replay.record_history[E4].superseded_by == E7
        assert replay.record_history[E7].supersedes_record_id == E4
        for change in replay.change_sets:
            parsed = api.KnowledgeChangeSet.from_bytes(change.canonical_bytes)
            assert parsed == change
            assert parsed.canonical_bytes == change.canonical_bytes

    print(
        json.dumps(
            {
                "claim": "DISTINCT_VALID_HISTORIES_SAME_CURRENT_GRAPH",
                "classification": "CONFORMANCE_FIXTURE",
                "method": "Existing accepted correction plus one authored evidence-only append",
                "compiler_import": api.__file__,
                "compiler_producer": producer,
                "contract_identity": short.partial_contract.identity,
                "history_binding_identity": short.binding.identity,
                "graph_state_digest": short.graph.state_digest(),
                "graph_export_sha256": digest(canonical(short.graph.export_records())),
                "source_sha256": digest(short.retained_bytes(SOURCE)),
                "acceptance_head": short.acceptance_head,
                "materialization_head": short.materialization_head,
                "accepted_change_identities": [
                    change.identity for change in short.change_sets
                ],
                "short": {
                    "ledger_head": short.ledger_head,
                    "event_count": short.ledger_event_count,
                    "ledger_sha256": digest(original_bytes),
                    "receipt_identity": short.receipt.identity,
                },
                "long": {
                    "ledger_head": long.ledger_head,
                    "event_count": long.ledger_event_count,
                    "ledger_sha256": digest(extended_bytes),
                    "receipt_identity": long.receipt.identity,
                },
                "note_identity": digest(note),
                "kcs_round_trip": True,
                "jsonl_only_reopen": True,
                "external_action_executed": False,
            },
            sort_keys=True,
        )
    )

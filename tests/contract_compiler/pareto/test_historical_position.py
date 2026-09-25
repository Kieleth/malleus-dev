"""T2 RED: exact historical context, not an old graph with future evidence."""

import json

import pytest

import malleus.compiler as api
from malleus.ledger import JsonlLedger, canonical_json, event_hash
from tests.contract_compiler.pareto import test_temporal_history as controls

TX = controls.TX
compilation = controls.compilation
episode = controls.episode
history = controls.history


def arguments(selected, containing):
    return {
        "ledger_head": selected.ledger_head,
        "ledger_event_count": selected.ledger_event_count,
        "expected_head_hash": containing.ledger_head,
        "expected_event_count": containing.ledger_event_count,
    }


def read(history, **kwargs):
    method = getattr(history, "replay_at", None)
    assert callable(method), "Core has no public complete historical-position read"
    return method(**kwargs)


def test_old_receipt_records_and_sources_reconstruct_without_writes(episode):
    history, before, after = episode
    original_bytes = history.path.read_bytes()
    result = read(history, **arguments(before, after))
    assert result.receipt == before.receipt
    assert result.record_history == before.record_history
    assert result.graph.snapshot() == before.graph.snapshot()
    assert result.retained_inputs == before.retained_inputs
    assert result.change_sets == before.change_sets
    with pytest.raises(KeyError):
        result.retained_bytes("source:price:new")
    reopened = api.KnowledgeChangeHistory.reopen(history.path)
    assert read(reopened, **arguments(before, after)).receipt == before.receipt
    assert history.path.read_bytes() == original_bytes


def test_current_position_equals_replay_and_returned_graph_is_independent(episode):
    history, _, after = episode
    result = read(history, **arguments(after, after))
    assert result.receipt == after.receipt
    result.graph.create_entity("PriceState", "caller:only", {"price_cents": 1})
    assert (
        read(history, **arguments(after, after)).graph.get_node("caller:only") is None
    )


def test_one_read_snapshot_and_explicit_same_timestamp_position(episode, monkeypatch):
    history, before, after = episode
    calls = []
    original_read = JsonlLedger.read

    def observed_read(ledger, **kwargs):
        calls.append(ledger.path)
        return original_read(ledger, **kwargs)

    monkeypatch.setattr(JsonlLedger, "read", observed_read)
    selected = read(history, **arguments(before, after))
    assert calls == [history.path]
    assert selected.receipt == before.receipt
    times = {
        json.loads(row)["transaction_time"]
        for row in history.path.read_bytes().splitlines()
    }
    assert times == {TX}


@pytest.mark.parametrize(
    "missing",
    [
        "ledger_head",
        "ledger_event_count",
        "expected_head_hash",
        "expected_event_count",
    ],
)
def test_every_coordinate_is_required(episode, missing):
    history, before, after = episode
    request = arguments(before, after)
    del request[missing]
    with pytest.raises(TypeError, match=missing):
        read(history, **request)


@pytest.mark.parametrize(
    "field,value",
    [
        ("ledger_head", "sha256:" + "0" * 64),
        ("expected_head_hash", "sha256:" + "0" * 64),
        ("ledger_event_count", 99999),
        ("ledger_event_count", -1),
        ("ledger_event_count", True),
        ("ledger_event_count", 1.0),
        ("ledger_event_count", "1"),
        ("expected_event_count", True),
        ("expected_event_count", None),
    ],
)
def test_wrong_coordinates_refuse_without_writes(episode, field, value):
    history, before, after = episode
    request = arguments(before, after)
    request[field] = value
    original = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as failure:
        read(history, **request)
    assert failure.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == original


def test_prefix_cannot_hide_truncated_containing_ledger(episode):
    history, before, after = episode
    rows = history.path.read_bytes().splitlines(keepends=True)
    truncated = b"".join(rows[: before.ledger_event_count])
    history.path.write_bytes(truncated)
    with pytest.raises(api.KnowledgeChangeRefusal) as failure:
        read(history, **arguments(before, after))
    assert failure.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == truncated


def test_valid_hashes_cannot_hide_semantically_corrupt_later_evidence(episode):
    history, before, after = episode
    rows = [json.loads(row) for row in history.path.read_bytes().splitlines()]
    changed = before.ledger_event_count
    assert "retained_bytes_base64" in rows[changed]["payload"]
    rows[changed]["payload"]["retained_bytes_base64"] = "eA=="
    for index in range(changed, len(rows)):
        rows[index]["previous_event_hash"] = rows[index - 1]["event_hash"]
        rows[index]["event_hash"] = event_hash(rows[index])
    corrupted = ("\n".join(canonical_json(row) for row in rows) + "\n").encode()
    history.path.write_bytes(corrupted)
    request = arguments(before, after)
    request["expected_head_hash"] = rows[-1]["event_hash"]
    with pytest.raises(api.KnowledgeChangeRefusal):
        read(history, **request)
    assert history.path.read_bytes() == corrupted


@pytest.mark.parametrize("position", ["bootstrap", "admission"])
def test_incomplete_selected_position_refuses(episode, position):
    history, before, after = episode
    rows = [json.loads(row) for row in history.path.read_bytes().splitlines()]
    count = 1 if position == "bootstrap" else before.ledger_event_count - 1
    request = arguments(before, after)
    request.update(ledger_head=rows[count - 1]["event_hash"], ledger_event_count=count)
    with pytest.raises(api.KnowledgeChangeRefusal) as failure:
        read(history, **request)
    assert failure.value.reason is (
        api.KnowledgeChangeRefusalReason.MALFORMED_HISTORY
        if position == "bootstrap"
        else api.KnowledgeChangeRefusalReason.INCOMPLETE_ADMISSION
    )


def test_evidence_only_position_has_no_future_source(episode):
    history, _, after = episode
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="later:evidence",
                content=b"later",
                media_type="text/plain",
            ),
        ),
        transaction_time=TX,
        actor_id="actor:test",
    )
    latest = history.replay()
    selected = read(history, **arguments(after, latest))
    assert selected.receipt == after.receipt
    with pytest.raises(KeyError):
        selected.retained_bytes("later:evidence")


def test_selected_contract_is_old_contract_not_current_contract(tmp_path):
    from tests.contract_compiler.pareto.test_contract_revision import (
        ADD_CLASS_SOURCE,
        _compose_revision,
        _history,
    )

    history, _, _ = _history(tmp_path)
    before = history.replay()
    revision, _, _ = _compose_revision(history, ADD_CLASS_SOURCE)
    history.record_contract_revision(
        revision=revision, transaction_time=TX, actor_id="actor:test"
    )
    after = history.replay()
    assert before.partial_contract.identity != after.partial_contract.identity
    selected = read(history, **arguments(before, after))
    assert selected.receipt == before.receipt
    assert selected.contract_view.artifact_bytes == before.contract_view.artifact_bytes
    assert selected.contract_revisions == ()


def test_cut_inside_finite_transaction_refuses(tmp_path):
    from tests.contract_compiler.pareto.test_finite_protocol_history import (
        append,
        drafts,
        selected_history,
    )

    history, args = selected_history(tmp_path)
    append(history, drafts(history, args))
    after = history.replay()
    rows = [json.loads(row) for row in history.path.read_bytes().splitlines()]
    request = arguments(after, after)
    request.update(ledger_head=rows[-2]["event_hash"], ledger_event_count=len(rows) - 1)
    with pytest.raises(ValueError, match="incomplete logical transaction"):
        read(history, **request)

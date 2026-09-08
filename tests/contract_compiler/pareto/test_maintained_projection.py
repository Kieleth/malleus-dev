"""A maintained reader must equal full replay without refolding its prefix."""

import json

import pytest

import malleus.compiler as api
import malleus._contract_pipeline.knowledge as knowledge
from malleus.kg import KnowledgeGraph
from malleus.ledger import JsonlLedger, canonical_json, event_hash
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _admit_record_change,
    _anchored_history,
    _evidence_anchor,
    _record_change,
)


def coordinates(replay):
    return dict(
        expected_head_hash=replay.ledger_head,
        expected_event_count=replay.ledger_event_count,
    )


def assert_parity(actual, expected):
    assert actual.receipt == expected.receipt
    assert actual.graph.snapshot() == expected.graph.snapshot()
    assert actual.machine_state == expected.machine_state
    assert actual.record_history == expected.record_history
    assert actual.retained_inputs == expected.retained_inputs
    assert actual.change_sets == expected.change_sets
    assert actual.contract_revisions == expected.contract_revisions
    assert actual.protocol_replay == expected.protocol_replay
    assert actual.acceptance_head == expected.acceptance_head
    assert actual.materialization_head == expected.materialization_head
    for change in expected.change_sets:
        assert actual.graph_at_change(change.change_set_id).snapshot() == (
            expected.graph_at_change(change.change_set_id).snapshot()
        )


@pytest.fixture
def sequence(tmp_path):
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    prefixes = [history.path.read_bytes()]
    for index in range(3):
        change = _record_change(
            history,
            partial,
            source,
            evidence,
            change_set_id=f"change:{index}",
            record_id=f"left:{index}",
            label=f"value {index}",
            order=f"order:{index}",
            supersedes_record_id="left:1" if index == 2 else None,
        )
        _admit_record_change(history, change, suffix=f":{index}")
        prefixes.append(history.path.read_bytes())
    return history, prefixes


def test_suffix_only_fold_and_new_records_only_with_defensive_reads(
    sequence, monkeypatch
):
    history, prefixes = sequence
    expected = history.replay()
    history.path.write_bytes(prefixes[1])
    view = api.KnowledgeHistoryProjection.open(history.path)
    prior = history.replay()
    folded, created, decoded = [], [], []
    execute, create = knowledge.execute_event, KnowledgeGraph.create_entity
    decode = JsonlLedger._decode_bytes

    def spy_decode(raw):
        decoded.append(raw)
        return decode(raw)

    def spy_execute(contract, state, event):
        folded.append(json.loads(event))
        return execute(contract, state, event)

    def spy_create(graph, kind, identifier, properties=None):
        created.append(identifier)
        return create(graph, kind, identifier, properties)

    def forbidden(*args, **kwargs):
        pytest.fail("refresh used full ledger decode/replay")

    history.path.write_bytes(prefixes[-1])
    with monkeypatch.context() as patch:
        patch.setattr(knowledge, "execute_event", spy_execute)
        patch.setattr(KnowledgeGraph, "create_entity", spy_create)
        patch.setattr(JsonlLedger, "_decode_bytes", staticmethod(spy_decode))
        patch.setattr(JsonlLedger, "read", forbidden)
        patch.setattr(api.KnowledgeChangeHistory, "replay", forbidden)
        actual = view.refresh(**coordinates(expected))
        assert created == ["left:1", "left:2"]
        assert len(folded) == 8  # two proposals, four checks, two decisions
        assert decoded == [prefixes[-1][len(prefixes[1]) :]]
        actual.graph.create_entity("LeftObject", "caller-only", {"label": "local"})
        folded.clear()
        created.clear()
        assert_parity(view.current(**coordinates(expected)), expected)
        assert_parity(view.refresh(**coordinates(expected)), expected)
        assert folded == created == []
    with pytest.raises(api.KnowledgeChangeRefusal, match="STALE_BASE"):
        view.current(**coordinates(prior))
    assert history.path.read_bytes() == prefixes[-1]


def test_publication_failure_keeps_graph_indexes_and_cursor(sequence, monkeypatch):
    history, prefixes = sequence
    expected = history.replay()
    history.path.write_bytes(prefixes[1])
    prior = history.replay()
    view = api.KnowledgeHistoryProjection.open(history.path)
    history.path.write_bytes(prefixes[-1])
    original = KnowledgeGraph.state_projection

    def interrupted(graph):
        if graph.get_node("left:2") is not None:
            raise OSError("injected copy interruption")
        return original(graph)

    with monkeypatch.context() as patch:
        patch.setattr(KnowledgeGraph, "state_projection", interrupted)
        with pytest.raises(api.KnowledgeChangeRefusal, match="copy interruption"):
            view.refresh(**coordinates(expected))
    assert_parity(view.current(**coordinates(prior)), prior)
    assert_parity(view.refresh(**coordinates(expected)), expected)


def test_partial_action_transaction_never_publishes(tmp_path):
    from tests.contract_compiler.pareto.test_finite_protocol_history import (
        append,
        drafts,
        selected_history,
    )

    history, arguments = selected_history(tmp_path)
    prior_bytes = history.path.read_bytes()
    prior = history.replay()
    view = api.KnowledgeHistoryProjection.open(history.path)
    append(history, drafts(history, arguments))
    complete = history.path.read_bytes()
    expected = history.replay()
    rows = complete.splitlines(keepends=True)
    history.path.write_bytes(b"".join(rows[:-1]))
    last = json.loads(rows[-2])
    with pytest.raises(ValueError, match="incomplete logical transaction"):
        view.refresh(
            expected_head_hash=last["event_hash"], expected_event_count=last["sequence"]
        )
    assert_parity(view.current(**coordinates(prior)), prior)
    history.path.write_bytes(complete)
    assert complete.startswith(prior_bytes)
    assert_parity(view.refresh(**coordinates(expected)), expected)


def test_evidence_only_advance_does_not_materialize_domain_records(
    sequence, monkeypatch
):
    history, _ = sequence
    prior = history.replay()
    view = api.KnowledgeHistoryProjection.open(history.path)
    history.append_anchors(
        anchors=(_evidence_anchor("later:evidence", b"later evidence"),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    expected = history.replay()
    with pytest.raises(api.KnowledgeChangeRefusal, match="STALE_BASE"):
        view.current(**coordinates(expected))

    def forbidden(*args, **kwargs):
        pytest.fail("evidence-only refresh applied a domain change")

    monkeypatch.setattr(api.KnowledgeChangeHistory, "_apply_change", forbidden)
    actual = view.refresh(**coordinates(expected))
    assert_parity(actual, expected)
    assert actual.acceptance_head == prior.acceptance_head
    assert actual.materialization_head == prior.materialization_head
    assert actual.ledger_head != prior.ledger_head


@pytest.mark.parametrize(
    "failure",
    [
        "truncated",
        "replaced",
        "gap",
        "duplicate",
        "bad_tail",
        "incomplete",
        "wrong_head",
    ],
)
def test_failed_refresh_preserves_entire_published_state(sequence, failure):
    history, prefixes = sequence
    complete = history.replay()
    history.path.write_bytes(prefixes[1])
    prior = history.replay()
    view = api.KnowledgeHistoryProjection.open(history.path)
    rows = [json.loads(line) for line in prefixes[-1].splitlines()]
    if failure == "truncated":
        raw = prefixes[0]
    elif failure == "replaced":
        raw = prefixes[-1].replace(b"actor:test", b"actor:evil", 1)
    elif failure == "bad_tail":
        raw = prefixes[-1] + b"{"
    elif failure == "incomplete":
        raw = b"\n".join(prefixes[-1].splitlines()[:-1]) + b"\n"
    elif failure in {"gap", "duplicate"}:
        index = prior.ledger_event_count
        rows[index]["sequence" if failure == "gap" else "event_id"] = (
            index + 2 if failure == "gap" else rows[0]["event_id"]
        )
        for position in range(index, len(rows)):
            rows[position]["previous_event_hash"] = rows[position - 1]["event_hash"]
            rows[position]["event_hash"] = event_hash(rows[position])
        raw = ("\n".join(map(canonical_json, rows)) + "\n").encode()
    else:
        raw = prefixes[-1]
    history.path.write_bytes(raw)
    target = coordinates(complete)
    if failure in {"gap", "duplicate", "incomplete"}:
        final_row = json.loads(raw.splitlines()[-1])
        target = dict(
            expected_head_hash=final_row["event_hash"],
            expected_event_count=len(raw.splitlines()),
        )
    if failure == "wrong_head":
        target["expected_head_hash"] = "sha256:" + "0" * 64
    with pytest.raises(api.KnowledgeChangeRefusal):
        view.refresh(**target)
    assert_parity(view.current(**coordinates(prior)), prior)
    assert history.path.read_bytes() == raw
    history.path.write_bytes(prefixes[-1])
    assert_parity(view.refresh(**coordinates(complete)), complete)


def test_supplier_episode_protocol_and_supersession_converge(tmp_path, monkeypatch):
    assert "KnowledgeHistoryProjection" in api.__all__
    from types import SimpleNamespace
    from research.semantic_reentry_external_design import supplier_initialization
    from research.semantic_reentry_external_design.supplier_walkthrough import run

    parser = supplier_initialization.datetime.fromisoformat

    def python310_datetime(value):
        if value.endswith("Z"):
            raise ValueError("Python 3.10 requires an explicit UTC offset")
        return parser(value)

    monkeypatch.setattr(
        supplier_initialization, "datetime",
        SimpleNamespace(fromisoformat=python310_datetime),
    )
    output = tmp_path / "supplier"
    run(output)
    report = json.loads((output / "walkthrough.json").read_bytes())
    raw = (output / "history.jsonl").read_bytes()
    path = tmp_path / "reader.jsonl"
    view = None
    for step in report["checkpoints"]:
        path.write_bytes(raw[: step["ledger_byte_length"]])
        expected = api.KnowledgeChangeHistory.reopen(path).replay()
        if view is None:
            view = api.KnowledgeHistoryProjection.open(path)
        assert_parity(view.refresh(**coordinates(expected)), expected)
        assert (
            expected.graph.query("SupplierOrderState")[0]["ordered_quantity"]
            == step["accepted_quantity"]
        )
    assert expected.protocol_replay is not None
    assert (
        expected.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:reentry-amendment-1"
    )


def test_partial_shipments_revision_and_recovery_converge(tmp_path):
    assert "KnowledgeHistoryProjection" in api.__all__
    from research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments.run import (
        ACTOR,
        TIME,
        admit_plan,
        revise,
        start,
    )

    history = start(tmp_path / "shop")
    view = api.KnowledgeHistoryProjection.open(history.path)
    for action in (
        lambda: admit_plan(history, "order", transaction_time=TIME, actor_id=ACTOR),
        lambda: revise(history, transaction_time=TIME, actor_id=ACTOR),
        lambda: admit_plan(
            history, "shipment-1", transaction_time=TIME, actor_id=ACTOR
        ),
        lambda: admit_plan(
            history, "shipment-2", transaction_time=TIME, actor_id=ACTOR
        ),
    ):
        action()
        expected = history.replay()
        assert_parity(view.refresh(**coordinates(expected)), expected)
    recovered = api.KnowledgeHistoryProjection.open(history.path)
    assert_parity(recovered.current(**coordinates(expected)), expected)

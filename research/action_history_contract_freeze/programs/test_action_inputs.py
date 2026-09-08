"""The reference producer starts from a supplied history, never from Shop."""

import ast
from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import content_digest
from malleus._contract_pipeline.protocol_runtime import (
    ProtocolProgramRefusal,
    canonical,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    add_initialization,
)
from research.action_history_contract_freeze.programs.proposal_bundle import (
    add_context_proposal,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    build_registration_bundle,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    compiled,
    prerequisites,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _anchored_history,
    _base_payload,
    _load_change,
    _protocol_events,
)


MODULE = "research.action_history_contract_freeze.programs.action_inputs"
TIME = "2026-09-07T00:01:00Z"
SOURCE_IDS = {
    name: "bench:definition:" + name
    for name in ("profile", "record_contract", "machine", "history_binding")
}
POLICY_IDS = {name: "policy:" + name for name in ("epistemic", "authorization")}
INPUT_IDS = {
    name: "bench:input:" + name
    for name in ("goal", "preservation", "mapping", "pre_state_source")
}
INPUT_BYTES = {
    "goal": b'{"target":"record an inspection"}',
    "preservation": b'{"protected":["left-1","right-1"]}',
    "mapping": b'{"reading":"caller-defined inspection input"}',
    "pre_state_source": b'{"available":true,"count":1}',
}


def api():
    return import_module(MODULE)


def metadata(identifier, when=TIME):
    return dict(
        event_id="event:" + identifier,
        transaction_time=when,
        actor_id="actor:bench-registrar",
        role="registrar",
        artifact_version="bench-v1",
        media_type="application/json",
        locator="urn:bench:" + identifier,
    )


def append(history, transaction, events):
    before = history.replay()
    return history.append_protocol_events(
        transaction=transaction,
        events=events,
        expected_head=before.ledger_head,
        expected_count=before.ledger_event_count,
    )


@pytest.fixture(scope="module")
def prefix(tmp_path_factory):
    producer = api()
    directory = tmp_path_factory.mktemp("nonshop-action-inputs")
    history, _, partial, _, source, evidence = _anchored_history(directory)
    change = _load_change(_base_payload(history, partial, source, evidence))
    history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change, history.replay().machine_state.identity
        ),
        transaction_time="2026-09-06T00:00:00Z",
        actor_id="actor:bench",
    )
    contract = compiled().artifact_bytes
    bundle = add_context_proposal(
        add_initialization(
            build_registration_bundle(contract),
            source_ids=SOURCE_IDS,
            policy_ids=POLICY_IDS,
        )
    )
    history.append_anchors(
        anchors=(
            core.structural_evidence_anchor(
                record_id="bench:programs",
                content=canonical(bundle),
                media_type="application/json",
            ),
        ),
        transaction_time="2026-09-07T00:00:00Z",
        actor_id="actor:bench",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="bench:programs",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="bench:select",
        transaction_time="2026-09-07T00:00:00Z",
        actor_id="actor:bench",
    )
    # Input fixture only. The isolated consumer below cannot import this builder.
    prerequisites(history)
    for name, content in {
        "profile": canonical(bundle["profile"]),
        "record_contract": contract,
        "machine": canonical(bundle),
        "history_binding": history.binding.canonical_bytes,
    }.items():
        event = producer.source_event(
            SOURCE_IDS[name],
            content,
            source_record_ids=(),
            **metadata(SOURCE_IDS[name]),
        )
        append(history, "source", (event,))
    return history.path.read_bytes()


def open_prefix(tmp_path, content):
    path = tmp_path / "history.jsonl"
    path.write_bytes(content)
    return core.KnowledgeChangeHistory.reopen(path)


def initialize(history):
    producer = api()
    checkpoint, references = producer.initialization_checkpoint(
        history,
        record_id="bench:initialization",
        source_ids=SOURCE_IDS,
        policy_ids=POLICY_IDS,
    )
    event = producer.initialization_event(
        checkpoint, references, **metadata(checkpoint["id"])
    )
    append(history, "initialize", (event,))
    for name, content in INPUT_BYTES.items():
        append(
            history,
            "source",
            (
                producer.source_event(
                    INPUT_IDS[name],
                    content,
                    source_record_ids=(),
                    **metadata(INPUT_IDS[name]),
                ),
            ),
        )


def arguments(history):
    checkpoint = json.loads(history.replay().retained_bytes("bench:initialization"))
    action = make_record(
        "LocalAction",
        id="bench:action",
        event_id="bench:proposal-event",
        generated_at="2026-09-07T00:02:00Z",
        actor_id="actor:bench-proposer",
        role="proposer",
        source_record_ids=["bench:context", POLICY_IDS["authorization"]],
        action_type="LOCAL_ACTION",
        action_payload_hash="sha256:" + sha256(INPUT_BYTES["mapping"]).hexdigest(),
        action_key="bench:inspection",
        revision=1,
        authorization_policy_id=POLICY_IDS["authorization"],
        authorization_policy_hash=checkpoint["authorization_policy"]["record_hash"],
    )
    return dict(
        initialization_id="bench:initialization",
        source_ids=INPUT_IDS,
        context_id="bench:context",
        context_metadata=metadata("bench:context", "2026-09-07T00:02:00Z"),
        action={"record_type": "LocalAction", "record": action},
        proposal_id="bench:proposal",
        proposal_key="bench:proposal-key",
        episode_key="bench:episode",
        payload_source_id=None,
    )


def test_module_has_no_fixture_or_test_imports():
    producer = api()
    assert set(producer.__all__) == {
        "source_event",
        "initialization_checkpoint",
        "initialization_event",
        "context_proposal",
    }
    tree = ast.parse(Path(producer.__file__).read_text())
    imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    imports += [
        a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names
    ]
    assert not any(
        name and (name.startswith("tests") or ".test_" in name or "small_shop" in name)
        for name in imports
    )
    assert "run_full_shop" not in Path(producer.__file__).read_text()


def test_existing_nonshop_history_initializes_and_proposes_in_isolation(
    tmp_path, prefix
):
    history = open_prefix(tmp_path, prefix)
    before = history.replay()
    # Prepare explicit input data, not a captured expected answer or replacement state.
    packet = {
        "source_ids": SOURCE_IDS,
        "policy_ids": POLICY_IDS,
        "input_ids": INPUT_IDS,
        "input_bytes": {k: v.decode() for k, v in INPUT_BYTES.items()},
    }
    script = """
import importlib.abc, json, sys
class NoFixture(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.startswith('tests') or '.test_' in fullname or 'small_shop' in fullname:
            raise AssertionError('fixture import: ' + fullname)
sys.meta_path.insert(0, NoFixture())
from malleus.compiler import KnowledgeChangeHistory
from malleus.assent import make_record
from malleus.ledger import content_digest
from hashlib import sha256
from research.action_history_contract_freeze.programs import action_inputs as p
h = KnowledgeChangeHistory.reopen(sys.argv[1])
inputs = json.loads(sys.argv[2])
def origin(i):
    return dict(event_id='event:'+i, transaction_time='2026-09-07T00:01:00Z', actor_id='actor:isolated', role='registrar', artifact_version='bench-v1', media_type='application/json', locator='urn:bench:'+i)
def append(name, events):
    r=h.replay()
    return h.append_protocol_events(transaction=name, events=events, expected_head=r.ledger_head, expected_count=r.ledger_event_count)
c, refs=p.initialization_checkpoint(h, record_id='bench:initialization', source_ids=inputs['source_ids'], policy_ids=inputs['policy_ids'])
append('initialize', (p.initialization_event(c, refs, **origin(c['id'])),))
for role, text in inputs['input_bytes'].items():
    i=inputs['input_ids'][role]
    append('source', (p.source_event(i, text.encode(), source_record_ids=(), **origin(i)),))
a=make_record('LocalAction', id='bench:action', event_id='bench:proposal-event', generated_at='2026-09-07T00:02:00Z', actor_id='actor:isolated-proposer', role='proposer', source_record_ids=['bench:context', inputs['policy_ids']['authorization']], action_type='LOCAL_ACTION', action_payload_hash='sha256:'+sha256(inputs['input_bytes']['mapping'].encode()).hexdigest(), action_key='bench:inspection', revision=1, authorization_policy_id=inputs['policy_ids']['authorization'], authorization_policy_hash=c['authorization_policy']['record_hash'])
events=p.context_proposal(h, initialization_id=c['id'], source_ids=inputs['input_ids'], context_id='bench:context', context_metadata=origin('bench:context'), action={'record_type':'LocalAction','record':a}, proposal_id='bench:proposal', proposal_key='bench:proposal-key', episode_key='bench:episode', payload_source_id=None)
append('context-proposal', events)
r=KnowledgeChangeHistory.reopen(sys.argv[1]).replay()
print(json.dumps([r.ledger_head,r.ledger_event_count,r.graph.state_digest()]))
"""
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [sys.executable, "-c", script, str(history.path), json.dumps(packet)],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONPATH": str(root) + os.pathsep + str(root / "src"),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    after = core.KnowledgeChangeHistory.reopen(history.path).replay()
    assert json.loads(result.stdout) == [
        after.ledger_head,
        after.ledger_event_count,
        after.graph.state_digest(),
    ]
    assert after.ledger_event_count == before.ledger_event_count + 7
    assert after.graph.export_records() == before.graph.export_records()
    assert after.acceptance_head == before.acceptance_head
    assert after.change_sets == before.change_sets
    assert set(after.record_history) == {"left-1", "right-1", "link:left-1:right-1"}
    for name, content in INPUT_BYTES.items():
        assert after.retained_bytes(INPUT_IDS[name]) == content
    records = after.protocol_replay.data["records"]
    assert (
        records["bench:action"]["record"]["responsible_actor_id"]
        == "actor:isolated-proposer"
    )
    assert (
        records["bench:proposal"]["record"]["generation_event_id"]
        == "bench:proposal-event"
    )
    context = json.loads(after.retained_bytes("bench:context"))
    assert context["episode_key"] == "bench:episode"
    assert (
        context["domain"]["effective_contract_identity"]
        == before.partial_contract.identity
    )


@pytest.mark.parametrize(
    "fault", ["missing-source-role", "unknown-source", "wrong-policy-type"]
)
def test_checkpoint_requires_explicit_applied_inputs(tmp_path, prefix, fault):
    history = open_prefix(tmp_path, prefix)
    sources, policies = dict(SOURCE_IDS), dict(POLICY_IDS)
    if fault == "missing-source-role":
        del sources["profile"]
    elif fault == "unknown-source":
        sources["profile"] = "not-registered"
    else:
        policies["epistemic"] = SOURCE_IDS["profile"]
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal) as caught:
        api().initialization_checkpoint(
            history, record_id="bench:init", source_ids=sources, policy_ids=policies
        )
    assert caught.value.reason == (
        "WRONG_ACTION_INPUT_TYPE"
        if fault == "wrong-policy-type"
        else "MISSING_ACTION_INPUT"
    )
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("fault", ["stale", "malformed-proposal"])
def test_proposal_refusal_is_atomic(tmp_path, prefix, fault):
    history = open_prefix(tmp_path, prefix)
    initialize(history)
    inputs = arguments(history)
    saved = deepcopy(inputs)
    before = history.path.read_bytes()
    events = api().context_proposal(history, **inputs)
    assert inputs == saved
    assert history.path.read_bytes() == before
    if fault == "stale":
        append(
            history,
            "source",
            (
                api().source_event(
                    "bench:later",
                    b"{}",
                    source_record_ids=(),
                    **metadata("bench:later"),
                ),
            ),
        )
    else:
        events[1]["data"]["proposal"]["value"][0]["record"]["content_hash"] = (
            content_digest("wrong")
        )
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal):
        append(history, "context-proposal", events)
    assert history.path.read_bytes() == before
    assert "bench:context" not in history.replay().protocol_replay.data["records"]


def test_source_event_binds_actual_media_bytes_and_origin(tmp_path, prefix):
    history = open_prefix(tmp_path, prefix)
    origin = metadata("binary")
    origin["media_type"] = "application/octet-stream"
    content = bytes([0, 255, 17])
    event = api().source_event("binary", content, source_record_ids=(), **origin)
    record = event["data"]["records"]["value"][0]["record"]
    assert event["retained"]["source"]["content"] == content
    assert event["retained"]["source"]["media_type"] == origin["media_type"]
    assert record["source_content_digest"] == "sha256:" + sha256(content).hexdigest()
    assert record["generated_at"] == origin["transaction_time"]
    append(history, "source", (event,))
    reopened = core.KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.retained_bytes("binary") == content

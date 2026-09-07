"""Real owning-ledger transactions, not the completed action-profile claim."""

from base64 import b64encode
from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import canonical_json, content_digest
from research.action_history_contract_freeze.programs.test_executor import grant
from research.action_history_contract_freeze.programs.test_packet_validator import (
    obj,
    operand,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchored_history,
    _evidence_anchor,
    _record_change,
    _protocol_events,
)


def api():
    return import_module("malleus._contract_pipeline.protocol_runtime")


def canonical(value):
    return canonical_json(value).encode()


def context(replay):
    return {
        "ledger_head": replay.ledger_head,
        "ledger_event_count": replay.ledger_event_count,
        "contract_identity": replay.partial_contract.identity,
        "acceptance_head": replay.acceptance_head,
        "materialization_head": replay.materialization_head,
        "graph_state_digest": replay.graph.state_digest(),
        "action_acceptance_head": "GENESIS",
    }


def specimen():
    args = grant()
    program, profile = args["program"], args["profile"]
    original_inputs = deepcopy(program["inputs"])
    header = original_inputs["event"]["header"]
    head = {"type": "string", "format": "ledger-head"}
    digest = {"type": "string", "format": "sha256"}
    coordinates = obj(
        ledger_head=head,
        ledger_event_count={"type": "integer", "minimum": 0},
        contract_identity=digest,
        acceptance_head=head,
        materialization_head=head,
        graph_state_digest=digest,
        action_acceptance_head=head,
    )
    frame_header = obj(
        **header["properties"],
        sequence={"type": "integer"},
        previous_event_hash=head,
        event_hash=digest,
    )
    constants = {
        "record_contract": args["inputs"]["artifact"]["record_contract"],
        "constants": args["inputs"]["artifact"]["constants"],
    }
    program["inputs"] = {
        "event": {
            "0": obj(header=frame_header, data=obj(base=coordinates), retained=obj()),
            "1": obj(
                header=frame_header,
                data=obj(
                    records=original_inputs["event"]["records"],
                    dependencies=original_inputs["event"]["dependencies"],
                ),
                retained=obj(),
            ),
        },
        "current": {"context": obj(value=coordinates)},
        "artifact": {"constants": obj(value=obj(**original_inputs["artifact"]))},
    }

    def rewrite(value):
        if isinstance(value, dict):
            if set(value) == {"root", "name", "path"}:
                if value["root"] == "event":
                    name = value["name"]
                    prefix = ["header"] if name == "header" else ["data", name]
                    value.update(name="1", path=prefix + value["path"])
                elif value["root"] == "artifact":
                    value.update(
                        name="constants", path=["value", value["name"]] + value["path"]
                    )
            else:
                for item in value.values():
                    rewrite(item)
        elif isinstance(value, list):
            for item in value:
                rewrite(item)

    rewrite(program["steps"])
    guards = [
        {
            "opcode": "REQUIRE_COMPARE",
            "comparison": "EQ",
            "value_kind": "INTEGER" if name == "ledger_event_count" else "STRING",
            "left": operand("event", "0", "data", "base", name),
            "right": operand("current", "context", "value", name),
            "refusal": "STALE_OR_FORGED_CONTEXT",
        }
        for name in coordinates["properties"]
    ]
    program["steps"] = guards + program["steps"]
    bundle = {
        "grammar": "malleus.finite-protocol-bundle/private-v0",
        "record_contract_base64": b64encode(args["record_contract_bytes"]).decode(),
        "instruction_schema": args["instruction_schema"],
        "profile": profile,
        "constants": constants,
        "transactions": {
            "register-pair": {
                "event_types": ["CONTEXT_STAGED", "GRANT_RECORDED"],
                "program": program,
            }
        },
    }
    return bundle, args


def selected_history(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle, args = specimen()
    source = canonical(bundle)
    history.append_anchors(
        anchors=(_evidence_anchor("finite-bundle", source),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="finite-bundle",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="select:1",
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    return history, args


def drafts(history, args):
    record_event = args["inputs"]["event"]
    return (
        {
            "event_id": "context:1",
            "event_type": "CONTEXT_STAGED",
            "actor_id": "actor:registrar",
            "transaction_time": TRANSACTION_TIME,
            "data": {"base": context(history.replay())},
            "retained": {},
        },
        {
            **record_event["header"],
            "event_type": "GRANT_RECORDED",
            "data": {
                "records": record_event["records"],
                "dependencies": record_event["dependencies"],
            },
            "retained": {},
        },
    )


def append(history, events, **overrides):
    base = history.replay()
    kwargs = dict(
        transaction="register-pair",
        events=events,
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
    )
    kwargs.update(overrides)
    return history.append_protocol_events(**kwargs)


def test_private_kernel_imports_no_research_runtime():
    import ast
    from pathlib import Path

    kernel = import_module("malleus._contract_pipeline.finite_executor")
    for module in (
        kernel,
        import_module("malleus._contract_pipeline.finite_program"),
        import_module("malleus._contract_pipeline.finite_control"),
    ):
        tree = ast.parse(Path(module.__file__).read_text())
        assert not any(
            isinstance(n, ast.ImportFrom)
            and n.module
            and n.module.startswith(("research", "tests"))
            for n in ast.walk(tree)
        )


def test_declared_package_closure_contains_every_finite_history_dependency():
    from pathlib import Path
    import tomllib

    root = Path(__file__).resolve().parents[3]
    includes = tomllib.loads((root / "pyproject.toml").read_text())["tool"]["hatch"]["build"]["include"]
    required = {f"/src/malleus/_contract_pipeline/{name}" for name in (
        "finite_program.py", "finite_executor.py", "finite_control.py",
        "protocol_runtime.py", "finite-instructions.json",
    )}
    assert required <= set(includes)


def test_real_pair_appends_and_reopens_without_a_second_log(tmp_path):
    history, args = selected_history(tmp_path)
    before = history.replay()
    result = append(history, drafts(history, args))
    assert result.ledger_event_count == before.ledger_event_count + 2
    assert result.graph.export_records() == before.graph.export_records()
    assert result.acceptance_head == before.acceptance_head
    assert result.materialization_head == before.materialization_head
    assert result.change_sets == before.change_sets
    identifier = args["inputs"]["event"]["records"]["value"][0]["record"]["id"]
    assert (
        result.protocol_replay.data["records"][identifier]["record_type"]
        == "AuthorityGrant"
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.receipt == result.receipt
    assert reopened.protocol_replay == result.protocol_replay
    assert tuple(tmp_path.iterdir()) == (history.path,)
    assert history.composition_context().base_ledger_head == result.ledger_head


@pytest.mark.parametrize(
    "fault",
    [
        "missing_half",
        "reversed",
        "wrong_type",
        "bad_record",
        "forged_context",
        "stale_head",
        "stale_count",
        "extra_event",
        "injected_current",
    ],
)
def test_transaction_refuses_without_any_append(tmp_path, fault):
    history, args = selected_history(tmp_path)
    before, replay = history.path.read_bytes(), history.replay()
    events = list(drafts(history, args))
    changes = {}
    if fault == "missing_half":
        events.pop()
    elif fault == "reversed":
        events.reverse()
    elif fault == "wrong_type":
        events[1]["event_type"] = "OTHER"
    elif fault == "bad_record":
        events[1]["data"]["records"]["value"][0]["record"]["grantor_id"] = "not-actor"
    elif fault == "forged_context":
        events[0]["data"]["base"]["graph_state_digest"] = content_digest("fake")
    elif fault == "stale_head":
        changes["expected_head"] = "GENESIS"
    elif fault == "stale_count":
        changes["expected_count"] = replay.ledger_event_count - 1
    elif fault == "extra_event":
        events.append(deepcopy(events[0]))
    else:
        events[0]["current"] = {"trusted": True}
    with pytest.raises((api().ProtocolProgramRefusal, ValueError)):
        append(history, tuple(events), **changes)
    assert history.path.read_bytes() == before
    assert history.replay().receipt == replay.receipt


def test_selection_is_explicit_and_cannot_be_replaced(tmp_path):
    history, _ = selected_history(tmp_path)
    before, replay = history.path.read_bytes(), history.replay()
    with pytest.raises(api().ProtocolProgramRefusal, match="already selected"):
        history.select_protocol_programs(
            record_id="finite-bundle",
            identity=replay.protocol_replay.data["bundle_identity"],
            expected_head=replay.ledger_head,
            expected_count=replay.ledger_event_count,
            event_id="select:2",
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert history.path.read_bytes() == before


def test_unselected_history_keeps_existing_receipt_shape(tmp_path):
    history = _anchored_history(tmp_path)[0]
    replay = history.replay()
    assert replay.protocol_replay is None
    assert "protocol_replay_identity" not in json.loads(replay.receipt.canonical_bytes)


def test_protocol_transaction_and_later_kcs_share_the_verified_full_prefix(tmp_path):
    history, args = selected_history(tmp_path)
    protocol = append(history, drafts(history, args))
    change = _record_change(
        history,
        protocol.partial_contract,
        api().digest(protocol.retained_bytes("source-generic")),
        api().digest(protocol.retained_bytes("evidence-generic")),
        change_set_id="change:after-action",
        record_id="domain:after-action",
        label="later ordinary domain knowledge",
        order="later",
    )
    change = history.compose_change_set(
        change_set_id=change.change_set_id,
        operations=change.operations,
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        valid_time=change.valid_time,
        supersedes=(),
    )
    assert change.base_ledger_head == protocol.ledger_head
    assert change.base_ledger_event_count == protocol.ledger_event_count
    accepted = history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change, protocol.machine_state.identity, identifier_suffix=":after-action"
        ),
        transaction_time="2026-09-07T00:00:01Z",
        actor_id="actor:test",
    )
    assert accepted.graph.get_node("domain:after-action") is not None
    assert accepted.protocol_replay == protocol.protocol_replay
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.receipt == accepted.receipt
    assert reopened.protocol_replay == protocol.protocol_replay


@pytest.mark.parametrize(
    "fault", ["orphan", "interleaved", "wrong_ordinal", "forged_identity"]
)
def test_owner_replay_rejects_partial_or_tampered_transaction_even_below_helper(
    tmp_path, fault
):
    history, args = selected_history(tmp_path)
    before, replay = history.path.read_bytes(), history.replay()
    entries = list(
        api().transaction_entries(
            bundle_identity=replay.protocol_replay.data["bundle_identity"],
            transaction="register-pair",
            events=drafts(history, args),
            expected_head=replay.ledger_head,
            expected_count=replay.ledger_event_count,
        )
    )
    if fault == "orphan":
        entries.pop()
    elif fault == "interleaved":
        entries.insert(
            1,
            {
                "event_id": "interruption",
                "event_type": "UNRELATED",
                "actor_id": "actor:registrar",
                "transaction_time": TRANSACTION_TIME,
                "payload": {},
            },
        )
    elif fault == "wrong_ordinal":
        entries[1]["payload"]["ordinal"] = 0
    else:
        for entry in entries:
            entry["payload"]["transaction_identity"] = content_digest("fabricated")
    with pytest.raises(api().ProtocolProgramRefusal):
        history._ledger.append_many(entries, validate=history._validate_candidate)
    assert history.path.read_bytes() == before


def test_reopen_does_not_call_a_check_producer(tmp_path, monkeypatch):
    history, args = selected_history(tmp_path)
    result = append(history, drafts(history, args))
    from research.action_history_contract_freeze.programs.check_executor import (
        CheckExecutor,
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("replay must not rerun checks")

    monkeypatch.setattr(CheckExecutor, "execute", forbidden)
    assert (
        KnowledgeChangeHistory.reopen(history.path).replay().receipt == result.receipt
    )

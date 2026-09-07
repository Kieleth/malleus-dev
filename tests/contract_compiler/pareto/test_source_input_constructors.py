"""The default bundle's convenience inputs preserve the existing event bytes."""

from dataclasses import replace
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto.test_public_compiler import _compiled_shop


def _source(**changes):
    arguments = dict(
        source_id="source:input",
        artifact_id="artifact:input",
        content=b"retained source\n",
        media_type="text/plain",
    )
    arguments.update(changes)
    return api.structural_source_anchors(**arguments)


def _evidence(**changes):
    arguments = dict(
        record_id="evidence:input",
        content=b"retained source\n",
        media_type="text/plain",
    )
    arguments.update(changes)
    return api.structural_evidence_anchor(**arguments)


def test_constructors_are_public_pure_and_byte_exact(monkeypatch):
    assert {"structural_source_anchors", "structural_evidence_anchor"} <= set(
        api.__all__
    )
    assert set(inspect.signature(api.structural_source_anchors).parameters) == {
        "source_id",
        "artifact_id",
        "content",
        "media_type",
    }
    assert set(inspect.signature(api.structural_evidence_anchor).parameters) == {
        "record_id",
        "content",
        "media_type",
    }

    def forbidden(*args, **kwargs):
        pytest.fail("input construction attempted I/O or persistence")

    with monkeypatch.context() as guard:
        guard.setattr(Path, "open", forbidden)
        guard.setattr("builtins.open", forbidden)
        guard.setattr(api.KnowledgeChangeHistory, "append_anchors", forbidden)
        pair, evidence = _source(), _evidence()
        assert pair == _source() and evidence == _evidence()
        assert _source(content=b"changed")[0].machine_event != pair[0].machine_event
        assert _evidence(content=b"").retained_bytes == b""

    identity = "sha256:" + sha256(b"retained source\n").hexdigest()
    expected = (
        (
            "ARTIFACT_REGISTERED",
            {"artifact_id": "artifact:input", "artifact_identity": identity},
            "SOURCE_ARTIFACT",
        ),
        (
            "SOURCE_REGISTERED",
            {
                "artifact_id": "artifact:input",
                "source_id": "source:input",
                "source_identity": identity,
            },
            "RETAINED_SOURCE",
        ),
        (
            "ARTIFACT_REGISTERED",
            {"artifact_id": "evidence:input", "artifact_identity": identity},
            "RETAINED_EVIDENCE",
        ),
    )
    assert type(pair) is tuple and len(pair) == 2
    for anchor, (event_type, payload, role) in zip(
        (*pair, evidence), expected, strict=True
    ):
        assert isinstance(anchor, api.KnowledgeAnchorInput)
        assert (
            anchor.machine_event
            == json.dumps(
                {"event_type": event_type, "payload": payload},
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        )
        assert anchor.retained_bytes == b"retained source\n"
        assert anchor.media_type == "text/plain" and anchor.role == role


@pytest.mark.parametrize(
    "constructor,changes",
    [
        (_source, {"content": "not bytes"}),
        (_source, {"source_id": ""}),
        (_source, {"artifact_id": None}),
        (_source, {"media_type": ""}),
        (_evidence, {"content": bytearray(b"mutable")}),
        (_evidence, {"record_id": ""}),
        (_evidence, {"media_type": None}),
    ],
)
def test_missing_or_mutable_inputs_refuse_without_defaults(constructor, changes):
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        constructor(**changes)
    assert error.value.reason is api.KnowledgeChangeRefusalReason.MALFORMED_HISTORY


def test_existing_ledger_owns_atomic_refusal_and_reopen(tmp_path):
    history = api.create_structural_history(
        tmp_path / "history.jsonl",
        compilation=_compiled_shop(api),
        transaction_time="2026-09-06T01:00:00Z",
        actor_id="actor:source-test",
    )
    pair, evidence = _source(), _evidence()
    before = history.path.read_bytes()
    for anchors in (
        (*pair, replace(evidence, retained_bytes=b"wrong bytes")),
        (*pair, pair[0]),
    ):
        with pytest.raises(api.KnowledgeChangeRefusal):
            history.append_anchors(
                anchors=anchors,
                transaction_time="2026-09-06T01:00:00Z",
                actor_id="actor:source-test",
            )
        assert history.path.read_bytes() == before
    history.append_anchors(
        anchors=(*pair, evidence),
        transaction_time="2026-09-06T01:00:00Z",
        actor_id="actor:source-test",
    )
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()
    for record_id in ("artifact:input", "source:input", "evidence:input"):
        assert reopened.retained_bytes(record_id) == b"retained source\n"
    assert not reopened.change_sets and not reopened.record_history


def test_consumers_remove_handwritten_default_retention_events():
    root = Path(__file__).resolve().parents[3]
    paths = (
        "src/malleus/compiler_cli.py",
        "research/ontology_driven_kg_realization/experiments/small_shop/default_admission/run.py",
        "research/ontology_driven_kg_realization/experiments/small_shop/fresh_import/run.py",
    )
    for path in paths:
        source = (root / path).read_text()
        assert "structural_source_anchors(" in source
        assert "structural_evidence_anchor(" in source
        assert "SOURCE_REGISTERED" not in source
        assert "ARTIFACT_REGISTERED" not in source

"""Per-assertion time remains retained evidence, not batch valid time."""

from __future__ import annotations

from importlib import import_module
import json
from pathlib import Path

import pytest

from tests.contract_compiler.pareto.test_document_assertion_adapter import (
    _canonical,
    _inputs,
)
from tests.contract_compiler.pareto.test_population_trace import _document_replay


ASSERTION_TIMES = {
    "asr:001": {
        "assertion_time": "2026-03-03T09:00:00Z",
        "domain_time": "2026-03-02",
    },
    "asr:002": {
        "assertion_time": "2026-03-03T09:05:00Z",
        "domain_time": "2026-03-01",
    },
    "asr:003": {
        "assertion_time": "2026-03-03T09:10:00Z",
    },
}


def _api():
    return import_module("malleus.compiler")


def test_committed_capture_contains_distinct_and_absent_assertion_times() -> None:
    _, capture, _, _ = _inputs()
    by_id = {item["id"]: item for item in capture["assertions"]}

    for assertion_id, expected in ASSERTION_TIMES.items():
        for field, value in expected.items():
            assert by_id[assertion_id][field] == value
    assert "domain_time" not in by_id["asr:003"]


def test_document_adapter_retains_distinct_and_absent_assertion_times() -> None:
    api = _api()
    reading, capture, plan, _ = _inputs()

    result = api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        records=plan["records"],
        supersessions=plan["supersessions"],
    )

    retained = json.loads(result.capture_bytes)
    by_id = {item["id"]: item for item in retained["assertions"]}
    assert by_id["asr:001"]["domain_time"] == "2026-03-02"
    assert by_id["asr:002"]["domain_time"] == "2026-03-01"
    assert "domain_time" not in by_id["asr:003"]


def test_public_trace_reaches_each_assertions_own_time_or_absence(
    tmp_path: Path,
) -> None:
    api = _api()
    _, replay = _document_replay(tmp_path)

    trace = api.trace_population_record(replay, "inspection-of:P-7:2026-03-02")
    capture = json.loads(
        next(
            item.content
            for item in trace.evidence
            if item.record_id == "capture:inspection-note"
        )
    )
    by_id = {item["id"]: item for item in capture["assertions"]}

    assert by_id["asr:001"]["assertion_time"] != by_id["asr:002"]["assertion_time"]
    assert by_id["asr:001"]["domain_time"] != by_id["asr:002"]["domain_time"]
    assert "domain_time" not in by_id["asr:003"]
    assert trace.change_set.valid_time.kind == "ORDER_ONLY"
    assert trace.change_set.valid_time.value == "capture:inspection-note"


@pytest.mark.parametrize(
    ("field", "value"),
    (("assertion_time", ""), ("domain_time", 17)),
)
def test_document_adapter_refuses_malformed_assertion_time(
    field: str,
    value: object,
) -> None:
    api = _api()
    reading, capture, plan, _ = _inputs()
    capture["assertions"][0][field] = value

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        api.adapt_document_assertions(
            reading_bytes=_canonical(reading),
            capture_bytes=_canonical(capture),
            capture_id="capture:inspection-note",
            plan_id=str(plan["plan_id"]),
            contract_identity=str(plan["contract_identity"]),
            records=plan["records"],
            supersessions=plan["supersessions"],
        )

    assert refusal.value.reason is api.DocumentAssertionRefusalReason.MALFORMED_CAPTURE

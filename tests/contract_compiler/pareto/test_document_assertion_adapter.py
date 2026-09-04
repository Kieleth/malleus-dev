"""Public contract for the optional document-assertion population adapter."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "handover/2026-09-03-core-population-v2/examples"


def _api():
    return import_module("malleus.compiler")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _load(name: str) -> object:
    return json.loads((EXAMPLES / name).read_bytes())


def _inputs() -> tuple[dict[str, object], ...]:
    reading = _load("reading.json")
    capture = _load("document-capture.json")
    plan = _load("document-plan.json")
    census = _load("document-census.json")
    assert isinstance(reading, dict)
    assert isinstance(capture, dict)
    assert isinstance(plan, dict)
    assert isinstance(census, dict)
    capture["reading_sha256"] = _digest(_canonical(reading))
    return reading, capture, plan, census


def _adapt(
    *,
    reading: dict[str, object] | None = None,
    capture: dict[str, object] | None = None,
):
    api = _api()
    fixture_reading, fixture_capture, plan, _ = _inputs()
    reading = fixture_reading if reading is None else reading
    capture = fixture_capture if capture is None else capture
    return api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        records=plan["records"],
        supersessions=plan["supersessions"],
        valid_time=plan["valid_time"],
    )


def test_document_adapter_is_public_and_emits_the_exact_neutral_plan() -> None:
    api = _api()
    required = {
        "DOCUMENT_ASSERTION_ADAPTER",
        "DOCUMENT_CAPTURE_GRAMMAR",
        "DocumentAssertionCompilation",
        "DocumentAssertionRefusal",
        "DocumentAssertionRefusalReason",
        "adapt_document_assertions",
    }
    assert required <= set(api.__all__)
    package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert (
        "/src/malleus/_contract_pipeline/document.py"
        in package["tool"]["hatch"]["build"]["include"]
    )

    reading, capture, expected_plan, expected_census = _inputs()
    capture_bytes = _canonical(capture)
    result = _adapt(reading=reading, capture=capture)

    assert isinstance(result, api.DocumentAssertionCompilation)
    assert result.capture_id == "capture:inspection-note"
    assert result.capture_bytes == capture_bytes
    assert result.capture_identity == _digest(capture_bytes)
    assert result.reading_identity == _digest(_canonical(reading))
    assert result.canonical_plan_bytes == _canonical(expected_plan)
    assert result.canonical_census_bytes == _canonical(expected_census)
    assert (
        json.loads(result.canonical_plan_bytes)["records"] == expected_plan["records"]
    )
    assert not any(
        record["type"].endswith("Assertion")
        for records in expected_plan["records"].values()
        for record in records
    )


@pytest.mark.parametrize(
    ("case", "reason"),
    (
        ("reading-mismatch", "READING_MISMATCH"),
        ("unknown-block", "UNKNOWN_BLOCK"),
        ("not-verbatim", "NOT_VERBATIM"),
        ("unknown-modality", "UNKNOWN_MODALITY"),
        ("gap-required", "GAP_REQUIRED"),
        ("unknown-target", "UNKNOWN_FORMALIZATION_TARGET"),
        ("unknown-gap-kind", "UNKNOWN_GAP_KIND"),
    ),
)
def test_document_adapter_refuses_each_semantic_boundary(
    case: str, reason: str
) -> None:
    api = _api()
    reading, capture, _, _ = _inputs()
    if case == "reading-mismatch":
        capture["reading_sha256"] = "sha256:" + "0" * 64
    elif case == "unknown-block":
        capture["nothing_assertable"].append("page:9:block:999")
    elif case == "not-verbatim":
        capture["assertions"][0]["statement"] = "Pump P-7 was fine."
    elif case == "unknown-modality":
        capture["assertions"][0]["modality"] = "VIBES"
    elif case == "gap-required":
        capture["assertions"][1]["gaps"] = []
    elif case == "unknown-target":
        capture["assertions"][0]["formalized_by"].append(
            {"record_id": "asset:P-7", "path": ["properties", "mass"]}
        )
    elif case == "unknown-gap-kind":
        capture["assertions"][1]["gaps"][0]["kind"] = "SHRUG"

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt(reading=reading, capture=capture)

    assert refusal.value.reason is getattr(api.DocumentAssertionRefusalReason, reason)


def test_document_adapter_accepts_verbatim_text_after_whitespace_normalisation() -> (
    None
):
    reading, capture, _, _ = _inputs()
    capture["assertions"][0]["statement"] = "Pump  P-7 was\ninspected on 2026-03-02."

    result = _adapt(reading=reading, capture=capture)

    assert json.loads(result.canonical_plan_bytes)["derivations"][0]["locator"] == (
        "asr:001"
    )


@pytest.mark.parametrize(
    ("case", "reason"),
    (
        ("capture-field", "FIELDS_NOT_CLOSED"),
        ("capture-grammar", "UNSUPPORTED_GRAMMAR"),
        ("malformed-reading", "MALFORMED_READING"),
        ("malformed-capture", "MALFORMED_CAPTURE"),
    ),
)
def test_document_adapter_refuses_malformed_or_open_inputs(
    case: str, reason: str
) -> None:
    api = _api()
    reading, capture, plan, _ = _inputs()
    reading_bytes = _canonical(reading)
    capture_bytes = _canonical(capture)
    if case == "capture-field":
        capture["extra"] = True
        capture_bytes = _canonical(capture)
    elif case == "capture-grammar":
        capture["schema"] = "another-capture/v1"
        capture_bytes = _canonical(capture)
    elif case == "malformed-reading":
        reading_bytes = b"{"
    elif case == "malformed-capture":
        capture_bytes = b"[]"

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        api.adapt_document_assertions(
            reading_bytes=reading_bytes,
            capture_bytes=capture_bytes,
            capture_id="capture:inspection-note",
            plan_id=str(plan["plan_id"]),
            contract_identity=str(plan["contract_identity"]),
            records=plan["records"],
            supersessions=plan["supersessions"],
            valid_time=plan["valid_time"],
        )

    assert refusal.value.reason is getattr(api.DocumentAssertionRefusalReason, reason)


def test_document_census_keeps_review_and_formalisation_separate() -> None:
    reading, capture, _, _ = _inputs()
    capture["nothing_assertable"] = []

    result = _adapt(reading=reading, capture=capture)
    census = json.loads(result.canonical_census_bytes)

    assert census["blocks"] == {
        "page:1:block:001": "REVIEWED",
        "page:1:block:002": "REVIEWED",
        "page:1:block:003": "UNTOUCHED",
    }
    assert census["assertions"] == {
        "FULLY_FORMALIZED": 1,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 2,
    }


def test_document_adapter_can_emit_a_gaps_only_plan() -> None:
    reading, capture, plan, _ = _inputs()
    capture["assertions"] = [deepcopy(capture["assertions"][1])]
    capture["nothing_assertable"] = [
        "page:1:block:002",
        "page:1:block:003",
    ]

    api = _api()
    result = api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note:gaps-only",
        plan_id="plan:inspection-note:gaps-only",
        contract_identity=str(plan["contract_identity"]),
        records={"entities": [], "relations": []},
        supersessions=[],
        valid_time=plan["valid_time"],
    )
    emitted = json.loads(result.canonical_plan_bytes)

    assert emitted["records"] == {"entities": [], "relations": []}
    assert emitted["derivations"] == []
    assert emitted["gaps"] == [
        {
            "kind": "INTERVAL_NOT_EXPRESSIBLE",
            "locator": "asr:002",
            "source_id": "source:inspection-note",
            "statement": (
                "VibrationReading.vibration_mm_s is a single float; "
                "the source states a range"
            ),
        }
    ]

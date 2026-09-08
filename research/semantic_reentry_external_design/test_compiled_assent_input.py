"""CONFORMANCE_FIXTURE for the action contract's existing Assent input.

Claim: the compiler-enabled OPTIONAL_PROFILE preserves all five declared
ValidTime forms through public compilation and source-free artifact reload.
Observation: valid forms pass; omitted required or present forbidden fields
refuse. Reuse the exact shipped ontology and public compiler/artifact reader.
Exclude action execution, temporal truth, source faithfulness and KG changes.
These synthetic values are validation probes, not supplier observations.
"""

from hashlib import sha256
from importlib.resources import files
from pathlib import Path

import pytest

from malleus import OntologyRegistry
import malleus.compiler as api


CASES = (
    {
        "valid_time_precision": "EXACT_TIMESTAMP",
        "exact_timestamp": "2026-09-07T00:00:00Z",
    },
    {
        "valid_time_precision": "CALENDAR_DAY",
        "calendar_date": "2026-09-07",
        "timezone": "UTC",
        "timezone_database_version": "2026c",
        "indeterminacy_reason": "Only the calendar day is known",
    },
    {
        "valid_time_precision": "BOUNDED_INTERVAL",
        "earliest_possible": "2026-09-07T00:00:00Z",
        "latest_possible": "2026-09-07T01:00:00Z",
        "indeterminacy_reason": "Only the interval is known",
    },
    {
        "valid_time_precision": "ORDER_ONLY",
        "order_scope": "scope:compiled-assent-input-probe",
        "order_index": 1,
        "indeterminacy_reason": "Only the order is known",
    },
    {
        "valid_time_precision": "UNRESOLVED_PRIOR_BOUNDARY",
        "indeterminacy_reason": "The prior boundary is unresolved",
    },
)
FIELDS = frozenset().union(*(record.keys() for record in CASES))


@pytest.fixture(scope="module")
def compiled_assent_bytes():
    root = Path(api.__file__).resolve().parents[2]
    sources = {
        "assent": (root / "ontology/assent.yaml").read_bytes(),
        "malleus": (root / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": files("linkml_runtime")
        .joinpath("linkml_model/model/schema/types.yaml")
        .read_bytes(),
    }
    expected = {
        "assent": "90830170573b52d7c73debb83c89bb278087607880675964e670d68fd7a1e234",
        "malleus": "5b737c212a5893ceebb22be207a09f3eb09ebab269898d354bb1dacdaad0aff3",
        "linkml:types": "1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00",
    }
    assert {
        name: sha256(value).hexdigest() for name, value in sources.items()
    } == expected
    return api.compile_linkml_contract(
        root_locator="assent", sources=sources
    ).artifact.artifact_bytes


@pytest.fixture
def reloaded_assent(compiled_assent_bytes, monkeypatch):
    def unavailable(*args, **kwargs):
        raise AssertionError("Runtime contract validation reached source or registry")

    monkeypatch.setattr(Path, "read_bytes", unavailable)
    monkeypatch.setattr(OntologyRegistry, "__init__", unavailable)
    return api.load_validated_contract_artifact(compiled_assent_bytes)


@pytest.mark.parametrize(
    "record", CASES, ids=lambda record: record["valid_time_precision"]
)
def test_all_declared_time_forms_survive_reload(reloaded_assent, record):
    assert reloaded_assent.validate_instance("ValidTime", record) == []


@pytest.mark.parametrize(
    "record", CASES, ids=lambda record: record["valid_time_precision"]
)
def test_each_required_component_stays_required(reloaded_assent, record):
    for field in record:
        missing = {key: value for key, value in record.items() if key != field}
        assert reloaded_assent.validate_instance("ValidTime", missing), field


@pytest.mark.parametrize(
    "record", CASES, ids=lambda record: record["valid_time_precision"]
)
def test_other_forms_fields_stay_absent_even_when_null(reloaded_assent, record):
    for field in sorted(FIELDS - record.keys()):
        for value in (None, "unexpected"):
            assert reloaded_assent.validate_instance(
                "ValidTime", {**record, field: value}
            ), (field, value)


def test_calendar_day_keeps_its_declared_database_pin(reloaded_assent):
    day = next(
        record for record in CASES if record["valid_time_precision"] == "CALENDAR_DAY"
    )
    assert reloaded_assent.validate_instance(
        "ValidTime", {**day, "timezone_database_version": "other"}
    )

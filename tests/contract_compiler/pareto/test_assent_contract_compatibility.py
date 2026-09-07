"""Exact Assent imports and record semantics, not action execution."""

from copy import deepcopy
from datetime import date
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest
import yaml

import malleus.compiler as api
from malleus.assent import make_record


ROOT = Path(__file__).resolve().parents[3]
DATE = "https://w3id.org/linkml/types/date"
FIXTURE = ROOT / "research/action_history_contract_freeze"


def _sources():
    return {
        "assent": (ROOT / "ontology/assent.yaml").read_bytes(),
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": files("linkml_runtime")
        .joinpath("linkml_model/model/schema/types.yaml")
        .read_bytes(),
        "action-probe": (FIXTURE / "action-probe.yaml").read_bytes(),
    }


def _compile(root="action-probe"):
    return api.compile_linkml_contract(root_locator=root, sources=_sources())


def _calendar(range_name="date"):
    sources = _sources()
    sources["calendar"] = (
        "id: https://example.org/calendar\nname: calendar\n"
        "imports: [linkml:types]\n"
        "classes:\n  Calendar:\n    slots: [day]\n"
        f"slots:\n  day:\n    range: {range_name}\n    required: true\n"
    ).encode()
    return api.compile_linkml_contract(root_locator="calendar", sources=sources)


@pytest.mark.parametrize("root", ["assent", "action-probe"])
def test_exact_assent_closure_compiles_without_dropping_declarations(root):
    sources = _sources()
    before = deepcopy(sources)
    compiled = api.compile_linkml_contract(root_locator=root, sources=sources)
    for name in yaml.safe_load(sources["assent"])["classes"]:
        assert compiled.view.has_type(name)
    assert (
        compiled.view.get_slot_constraint("ValidTime", "calendar_date").range_id == DATE
    )
    assert compiled.view.get_enum_values("AuthorizationVerdict") == {
        "AUTHORIZE",
        "BLOCK",
        "CLARIFY",
    }
    assert sources == before
    if root == "action-probe":
        assert compiled.view.is_subtype_of("LocalAction", "ActionProposal")
        assert not compiled.view.get_type("LocalAction").abstract
        assert compiled.view.get_type("ActionProposal").abstract


@pytest.mark.parametrize("value", ["2024-02-29", "2026-09-07", "0001-01-01"])
def test_date_preserves_its_distinct_range_and_accepts_real_calendar_dates(value):
    compiled = _calendar()
    assert compiled.view.get_slot_constraint("Calendar", "day").range_id == DATE
    assert compiled.view.validate_instance("Calendar", {"day": value}) == []
    loaded = api.load_validated_contract_artifact(compiled.artifact.artifact_bytes)
    assert loaded.validate_instance("Calendar", {"day": value}) == []


@pytest.mark.parametrize(
    "value",
    [
        "2025-02-29",
        "2026-13-01",
        "20260907",
        "2026-W37-1",
        "2026-09-07T00:00:00Z",
        "tomorrow",
        20260907,
        True,
        date(2026, 9, 7),
    ],
)
def test_date_rejects_invalid_dates_and_implicit_coercion(value):
    errors = _calendar().view.validate_instance("Calendar", {"day": value})
    assert any("date" in error for error in errors)


def test_date_extension_does_not_reinterpret_the_old_metamodel():
    dated, text = _calendar(), _calendar("string")
    date_payload = json.loads(dated.artifact.artifact_bytes)
    text_payload = json.loads(text.artifact.artifact_bytes)
    assert dated.content_hash != text.content_hash
    assert date_payload["metamodel"] != text_payload["metamodel"]
    date_payload["metamodel"] = text_payload["metamodel"]
    # Rebind the outer identity so rejection must inspect the metamodel/facts.
    identity = {
        "canonicalization_profile": date_payload["canonicalization"]["id"],
        "domain": "malleus.contract-fact-set/candidate-v0",
        "facts_sha256": date_payload["facts_sha256"].removeprefix("sha256:"),
        "metamodel": date_payload["metamodel"]["id"],
        "symbol_policy": date_payload["symbol_policy"]["id"],
    }
    date_payload["validated_fact_set_sha256"] = _digest(_json(identity))
    with pytest.raises(api.ArtifactRefusal) as caught:
        api.load_validated_contract_artifact(_json(date_payload))
    assert caught.value.reason.name == "INVALID_FACT_SET"


def _json(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def _digest(value):
    return "sha256:" + sha256(value).hexdigest()


def _record(kind, **fields):
    return {
        "id": "record:1",
        **make_record(
            kind,
            event_id="event:1",
            generated_at="2026-09-07T00:00:00Z",
            actor_id="actor:1",
            role="proposer",
            **fields,
        ),
    }


def _assessment(kind):
    return dict(
        proposal_id="proposal:1",
        proposal_content_hash=_digest(b"proposal"),
        base_acceptance_head=_digest(b"head"),
        assessment_kind=kind,
        assessment_outcome="SATISFIED",
        monitor_id="monitor:1",
        monitor_version="test-v1",
        monitor_hash=_digest(b"monitor"),
        input_record_ids=["input:1"],
        reason_codes=["MATCH"],
        rationale="Fixture",
    )


def _records():
    return [
        (
            "LocalAction",
            _record(
                "LocalAction",
                action_type="LOCAL_ACTION",
                action_payload_hash=_digest(b"payload"),
                action_key="action:1",
                revision=1,
                authorization_policy_id="policy:1",
                authorization_policy_hash=_digest(b"policy"),
            ),
            "revision",
            True,
        ),
        (
            "TypeAssessment",
            _record("TypeAssessment", **_assessment("TYPE")),
            "assessment_kind",
            "AUTHORITY",
        ),
        (
            "AuthorityAssessment",
            _record(
                "AuthorityAssessment",
                **_assessment("AUTHORITY"),
                action_proposal_id="action:1",
                action_content_hash=_digest(b"action"),
                evaluated_actor_id="actor:1",
                authority_policy_id="policy:1",
                authority_policy_hash=_digest(b"policy"),
                checked_policy_predicates=["scope"],
            ),
            "checked_policy_predicates",
            "scope",
        ),
        (
            "AuthorityGrant",
            _record(
                "AuthorityGrant",
                artifact_kind="AUTHORITY_GRANT",
                artifact_version="test-v1",
                artifact_hash=_digest(b"grant"),
                grantor_actor_id="actor:1",
                grantee_actor_id="actor:2",
                permitted_action_types=["LOCAL_ACTION"],
                scope_record_id="scope:1",
                may_subdelegate=False,
                grant_valid_from="2026-09-07T00:00:00Z",
            ),
            "may_subdelegate",
            "false",
        ),
    ]


@pytest.mark.parametrize("kind,record,field,bad", _records())
def test_selected_action_records_remain_structured_and_constrained(
    kind, record, field, bad
):
    view = _compile().view
    assert view.validate_instance(kind, record) == []
    assert view.validate_instance(kind, {**record, field: bad})
    assert view.validate_instance(kind, {**record, "undeclared": "value"})
    missing = dict(record)
    del missing[field]
    assert view.validate_instance(kind, missing)


def test_assent_valid_time_union_survives_source_free_artifact_reload(monkeypatch):
    artifact = _compile().artifact.artifact_bytes

    def forbidden(*args, **kwargs):
        raise AssertionError("compiled runtime reached source or registry")

    from malleus import OntologyRegistry

    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(OntologyRegistry, "__init__", forbidden)
    view = api.load_validated_contract_artifact(artifact)
    day = dict(
        valid_time_precision="CALENDAR_DAY",
        calendar_date="2026-09-07",
        timezone="UTC",
        timezone_database_version="2026c",
        indeterminacy_reason="Only a day is known",
    )
    assert view.validate_instance("ValidTime", day) == []
    assert view.validate_instance(
        "ValidTime", {**day, "exact_timestamp": "2026-09-07T00:00:00Z"}
    )
    assert view.validate_instance(
        "ValidTime", {**day, "timezone_database_version": "other"}
    )
    assert view.validate_instance("ValidTime", {**day, "calendar_date": "2026-02-30"})

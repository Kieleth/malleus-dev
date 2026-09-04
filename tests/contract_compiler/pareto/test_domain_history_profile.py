"""Full adopter-owned domain-history contract."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
SHOP_PLANS = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/small_shop"
    / "public_population/plans"
)
PROFILE_GRAMMAR = "malleus.domain-history-profile/private-v1"
PROFILE_FIELDS = {
    "change_semantics",
    "genesis",
    "grammar",
    "grounding",
    "ontology_roles",
    "origin",
    "profile_id",
    "projection_rule_family",
    "semantic_unit",
    "time_semantics",
}

SOURCE_ASSERTION_PROFILE_DATA = {
    "change_semantics": {
        "addition": "ADD_FORMALIZATION",
        "correction": "SUPERSEDE_FORMALIZATION",
        "retraction": "NOT_ADMITTED",
        "transition": "NOT_APPLICABLE",
    },
    "genesis": {
        "boundary": "RETAINED_PARTIAL_IMPORT",
        "completeness_scope": "DECLARED_CAPTURE_ONLY",
    },
    "grammar": PROFILE_GRAMMAR,
    "grounding": {
        "citations": [
            "Clark, Ciccarese, and Goble (2014), Micropublications",
            "Nanopublications",
        ],
        "taxonomy": "source-attributed assertion",
    },
    "ontology_roles": {
        "claim": [],
        "entity": ["Entity"],
        "event": ["Event"],
        "state": [],
    },
    "origin": "PARTIAL_IMPORT",
    "profile_id": "source-assertion",
    "projection_rule_family": (
        "CURRENT_NON_SUPERSEDED_RECORDS_WITH_RETAINED_ASSERTION_TRACE"
    ),
    "semantic_unit": "ASSERTION",
    "time_semantics": {
        "assertion_time": "RETAINED_CAPTURE_ATTRIBUTION",
        "domain_time": "KNOWLEDGE_VALID_TIME",
        "transaction_time": "LEDGER_TRANSACTION_TIME",
    },
}

STATE_VERSION_PROFILE_DATA = {
    "change_semantics": {
        "addition": "ADD_STATE_VERSION",
        "correction": "SUPERSEDE_STATE_VERSION",
        "retraction": "NOT_ADMITTED",
        "transition": "SUPERSEDE_STATE_VERSION",
    },
    "genesis": {
        "boundary": "FIRST_ACCEPTED_CHANGE_SET_OVER_EMPTY_GRAPH",
        "completeness_scope": "DECLARED_SOURCES_ONLY",
    },
    "grammar": PROFILE_GRAMMAR,
    "grounding": {
        "citations": ["Temporal database versioning"],
        "taxonomy": "versioned domain state",
    },
    "ontology_roles": {
        "claim": [],
        "entity": ["Entity"],
        "event": [],
        "state": ["Entity"],
    },
    "origin": "EMPTY",
    "profile_id": "state-version",
    "projection_rule_family": "CURRENT_NON_SUPERSEDED_RECORDS",
    "semantic_unit": "STATE_VERSION",
    "time_semantics": {
        "assertion_time": "NOT_REPRESENTED",
        "domain_time": "KNOWLEDGE_VALID_TIME",
        "transaction_time": "LEDGER_TRANSACTION_TIME",
    },
}

OBJECT_EVENT_PROFILE_DATA = {
    "change_semantics": {
        "addition": "APPEND_IMMUTABLE_EVENT",
        "correction": "APPEND_CORRECTING_EVENT",
        "retraction": "APPEND_RETRACTING_EVENT",
        "transition": "DERIVE_FROM_EVENT_ORDER",
    },
    "genesis": {
        "boundary": "FIRST_ACCEPTED_CHANGE_SET_OVER_EMPTY_GRAPH",
        "completeness_scope": "DECLARED_EVENT_SOURCES_ONLY",
    },
    "grammar": PROFILE_GRAMMAR,
    "grounding": {
        "citations": ["OCEL 2.0"],
        "taxonomy": "object-centric event log",
    },
    "ontology_roles": {
        "claim": [],
        "entity": ["Entity"],
        "event": ["Event"],
        "state": [],
    },
    "origin": "EMPTY",
    "profile_id": "object-event",
    "projection_rule_family": "CURRENT_STATE_DERIVED_FROM_EVENTS",
    "semantic_unit": "OCCURRENCE",
    "time_semantics": {
        "assertion_time": "NOT_REPRESENTED",
        "domain_time": "KNOWLEDGE_VALID_TIME",
        "transaction_time": "LEDGER_TRANSACTION_TIME",
    },
}

PROFILES = (
    ("SOURCE_ASSERTION_PROFILE", SOURCE_ASSERTION_PROFILE_DATA),
    ("STATE_VERSION_PROFILE", STATE_VERSION_PROFILE_DATA),
    ("OBJECT_EVENT_PROFILE", OBJECT_EVENT_PROFILE_DATA),
)


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


def _digest(value: object) -> str:
    return "sha256:" + sha256(_canonical(value)).hexdigest()


@pytest.mark.parametrize(("symbol", "data"), PROFILES)
def test_three_full_profiles_are_public_canonical_and_explicit(
    symbol: str, data: dict[str, object]
) -> None:
    api = _api()
    profile = getattr(api, symbol)

    assert symbol in api.__all__
    assert profile == api.DomainHistoryProfile.from_data(deepcopy(data))
    assert profile.canonical_bytes == _canonical(data)
    assert profile.identity == _digest(data)
    assert set(profile.data) == PROFILE_FIELDS
    assert profile.genesis == data["genesis"]
    assert profile.time_semantics == data["time_semantics"]
    assert profile.change_semantics == data["change_semantics"]
    assert profile.ontology_roles == {
        role: tuple(types) for role, types in data["ontology_roles"].items()
    }
    assert profile.projection_rule_family == data["projection_rule_family"]
    with pytest.raises(TypeError):
        profile.time_semantics["domain_time"] = "changed"


def test_source_assertion_profile_keeps_claims_in_evidence_and_requires_trace() -> None:
    profile = _api().SOURCE_ASSERTION_PROFILE

    assert profile.ontology_roles["claim"] == ()
    assert profile.time_semantics["assertion_time"] == ("RETAINED_CAPTURE_ATTRIBUTION")
    assert profile.projection_rule_family.endswith("RETAINED_ASSERTION_TRACE")


def test_state_version_profile_names_the_small_shop_history_rules() -> None:
    profile = _api().STATE_VERSION_PROFILE

    assert profile.semantic_unit == "STATE_VERSION"
    assert profile.change_semantics == {
        "addition": "ADD_STATE_VERSION",
        "correction": "SUPERSEDE_STATE_VERSION",
        "retraction": "NOT_ADMITTED",
        "transition": "SUPERSEDE_STATE_VERSION",
    }
    assert profile.projection_rule_family == "CURRENT_NON_SUPERSEDED_RECORDS"


def test_object_event_profile_is_declared_without_claiming_event_admission() -> None:
    profile = _api().OBJECT_EVENT_PROFILE

    assert profile.semantic_unit == "OCCURRENCE"
    assert profile.ontology_roles["event"] == ("Event",)
    assert profile.projection_rule_family == "CURRENT_STATE_DERIVED_FROM_EVENTS"


@pytest.mark.parametrize(
    "mutation",
    (
        "missing-section",
        "extra-nested-field",
        "wrong-genesis-boundary",
        "empty-semantics",
        "duplicate-role",
        "unsorted-role",
    ),
)
def test_full_profile_refuses_ambiguous_or_incomplete_meaning(mutation: str) -> None:
    api = _api()
    value = deepcopy(STATE_VERSION_PROFILE_DATA)
    if mutation == "missing-section":
        del value["change_semantics"]
    elif mutation == "extra-nested-field":
        value["time_semantics"]["timezone"] = "UTC"
    elif mutation == "wrong-genesis-boundary":
        value["genesis"]["boundary"] = "RETAINED_SNAPSHOT"
    elif mutation == "empty-semantics":
        value["change_semantics"]["correction"] = ""
    elif mutation == "duplicate-role":
        value["ontology_roles"]["state"] = ["Entity", "Entity"]
    elif mutation == "unsorted-role":
        value["ontology_roles"]["entity"] = ["Zed", "Entity"]
    else:
        raise AssertionError(mutation)

    with pytest.raises(api.PopulationPlanRefusal):
        api.DomainHistoryProfile.from_data(value)


def test_small_shop_plans_bind_the_exact_full_state_version_profile() -> None:
    expected = {
        "profile_id": "state-version",
        "sha256": _digest(STATE_VERSION_PROFILE_DATA),
    }

    plans = tuple(
        json.loads(path.read_bytes()) for path in sorted(SHOP_PLANS.glob("*.json"))
    )

    assert len(plans) == 5
    assert all(plan["history_profile"] == expected for plan in plans)

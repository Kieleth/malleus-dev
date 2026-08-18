"""Precision-aware valid time rejects false precision and explains uncertainty."""

from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import pytest
from tzdata import IANA_VERSION

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from malleus.valid_time import (
    BoundaryRelation,
    TZDATA_PACKAGE_VERSION,
    TZDATA_VERSION,
    ValidTime,
    ValidTimeError,
    transition_cannot_follow,
)


def point(value: str) -> datetime:
    return datetime.fromisoformat(value)


def test_timezone_database_runtime_and_dependency_pin_cannot_drift():
    project = tomllib.loads(
        (Path(__file__).parent.parent / "pyproject.toml").read_text()
    )
    assert f"tzdata=={TZDATA_PACKAGE_VERSION}" in project["project"]["dependencies"]
    assert version("tzdata") == TZDATA_PACKAGE_VERSION
    assert IANA_VERSION == TZDATA_VERSION


def test_exact_timestamp_preserves_half_open_transition_semantics():
    boundary = ValidTime.exact("2026-01-27T12:00:00-08:00")
    assert boundary.relation_at(point("2026-01-27T11:59:59-08:00")) is BoundaryRelation.BEFORE
    assert boundary.relation_at(point("2026-01-27T12:00:00-08:00")) is BoundaryRelation.AFTER
    assert boundary.reason_code is None
    assert boundary.as_dict() == {
        "valid_time_precision": "EXACT_TIMESTAMP",
        "exact_timestamp": "2026-01-27T12:00:00-08:00",
    }


def test_exact_timestamp_rejects_naive_and_noncanonical_values():
    with pytest.raises(ValidTimeError, match="timezone offset"):
        ValidTime.exact("2026-01-27T12:00:00")
    with pytest.raises(ValidTimeError, match="canonical ISO 8601"):
        ValidTime.exact("2026-01-27T20:00:00Z")


def test_calendar_day_requires_an_installed_iana_timezone():
    for timezone in ("PST", "/usr/share/zoneinfo/UTC"):
        with pytest.raises(ValidTimeError, match="installed IANA zone"):
            ValidTime.calendar_day(
                "2026-01-27",
                timezone=timezone,
                indeterminacy_reason="The source establishes only the service date.",
            )


def test_calendar_day_is_a_zoned_window_not_a_midnight_transition():
    boundary = ValidTime.calendar_day(
        "2026-03-08",
        timezone="America/Los_Angeles",
        indeterminacy_reason="The invoice establishes the day but no installation time.",
    )
    assert boundary.display_bounds() == (
        "2026-03-08T00:00:00-08:00",
        "2026-03-09T00:00:00-07:00",
    )
    assert boundary.relation_at(point("2026-03-08T07:59:59+00:00")) is BoundaryRelation.BEFORE
    assert boundary.relation_at(point("2026-03-08T12:00:00+00:00")) is BoundaryRelation.INDETERMINATE
    assert boundary.relation_at(point("2026-03-09T07:00:00+00:00")) is BoundaryRelation.AFTER
    assert boundary.reason_code == "CALENDAR_DAY_TRANSITION_WINDOW"
    assert boundary.as_dict()["timezone_database_version"] == "2026c"


@pytest.mark.parametrize("stored_version", ["2025b", "2026d"])
def test_calendar_day_rejects_an_unsupported_stored_timezone_database_version(
    stored_version,
):
    with pytest.raises(ValidTimeError, match="timezone_database_version must equal '2026c'"):
        ValidTime.from_value({
            "valid_time_precision": "CALENDAR_DAY",
            "calendar_date": "2026-01-27",
            "timezone": "America/Los_Angeles",
            "timezone_database_version": stored_version,
            "indeterminacy_reason": "The source establishes only the day.",
        })


def test_calendar_day_canonical_replay_is_stable_under_the_pinned_database():
    boundary = ValidTime.calendar_day(
        "2026-03-08",
        timezone="America/Los_Angeles",
        indeterminacy_reason="The source establishes only the day.",
    )
    stored = boundary.as_dict()
    replayed = ValidTime.from_value(stored)

    assert replayed == boundary
    assert replayed.as_dict() == stored
    assert replayed.display_bounds() == boundary.display_bounds()


@pytest.mark.parametrize(
    "value",
    [
        {"valid_time_precision": []},
        {"valid_time_precision": "EXACT_TIMESTAMP", "exact_timestamp": []},
        {
            "valid_time_precision": "CALENDAR_DAY",
            "calendar_date": [],
            "timezone": "UTC",
            "timezone_database_version": "2026c",
            "indeterminacy_reason": "The source establishes only the day.",
        },
        {
            "valid_time_precision": "CALENDAR_DAY",
            "calendar_date": "2026-01-27",
            "timezone": [],
            "timezone_database_version": "2026c",
            "indeterminacy_reason": "The source establishes only the day.",
        },
        {
            "valid_time_precision": "CALENDAR_DAY",
            "calendar_date": "2026-01-27",
            "timezone": "UTC",
            "timezone_database_version": {},
            "indeterminacy_reason": "The source establishes only the day.",
        },
        {
            "valid_time_precision": "BOUNDED_INTERVAL",
            "earliest_possible": [],
            "latest_possible": "2026-01-28T00:00:00+00:00",
            "indeterminacy_reason": "The source establishes only bounds.",
        },
        {
            "valid_time_precision": "BOUNDED_INTERVAL",
            "earliest_possible": "2026-01-27T00:00:00+00:00",
            "latest_possible": {},
            "indeterminacy_reason": "The source establishes only bounds.",
        },
        {
            "valid_time_precision": "ORDER_ONLY",
            "order_scope": [],
            "order_index": 1,
            "indeterminacy_reason": "The source establishes only order.",
        },
        {
            "valid_time_precision": "ORDER_ONLY",
            "order_scope": "service:1",
            "order_index": [],
            "indeterminacy_reason": "The source establishes only order.",
        },
        {
            "valid_time_precision": "UNRESOLVED_PRIOR_BOUNDARY",
            "indeterminacy_reason": [],
        },
    ],
)
def test_every_malformed_variant_field_raises_typed_valid_time_error(value):
    with pytest.raises(ValidTimeError):
        ValidTime.from_value(value)


def test_every_nonexact_boundary_requires_the_extracted_reason():
    with pytest.raises(ValidTimeError, match="indeterminacy_reason"):
        ValidTime.calendar_day(
            "2026-01-27",
            timezone="America/Los_Angeles",
            indeterminacy_reason="",
        )
    with pytest.raises(ValidTimeError, match="indeterminacy_reason"):
        ValidTime.unresolved_prior_boundary(indeterminacy_reason=" ")


def test_bounded_interval_exposes_its_reason_and_bounds():
    boundary = ValidTime.bounded_interval(
        "2026-01-27T09:00:00-08:00",
        "2026-01-27T17:00:00-08:00",
        indeterminacy_reason="The work order establishes opening and closing bounds only.",
    )
    assert boundary.reason_code == "BOUNDED_TRANSITION_WINDOW"
    assert boundary.relation_at(point("2026-01-27T08:59:59-08:00")) is BoundaryRelation.BEFORE
    assert boundary.relation_at(point("2026-01-27T12:00:00-08:00")) is BoundaryRelation.INDETERMINATE
    assert boundary.relation_at(point("2026-01-27T17:00:00-08:00")) is BoundaryRelation.AFTER


def test_order_only_and_unresolved_boundaries_remain_explained():
    ordered = ValidTime.order_only(
        order_scope="service:114430",
        order_index=2,
        indeterminacy_reason="The invoice establishes operation order but no physical time.",
    )
    unresolved = ValidTime.unresolved_prior_boundary(
        indeterminacy_reason="The removed component has no established installation boundary."
    )
    query = point("2026-08-17T12:00:00-07:00")
    assert ordered.relation_at(query) is BoundaryRelation.INDETERMINATE
    assert unresolved.relation_at(query) is BoundaryRelation.INDETERMINATE
    assert ordered.reason_code == "ORDER_ONLY_WITHOUT_ABSOLUTE_BOUNDARY"
    assert unresolved.reason_code == "UNRESOLVED_PRIOR_BOUNDARY"


def test_canonical_object_rejects_the_removed_exact_string_path():
    with pytest.raises(ValidTimeError, match="precision-aware object"):
        ValidTime.from_value("2026-01-27T12:00:00-08:00")
    with pytest.raises(ValidTimeError, match="omit null fields"):
        ValidTime.from_value({
            "valid_time_precision": "EXACT_TIMESTAMP",
            "exact_timestamp": "2026-01-27T12:00:00-08:00",
            "indeterminacy_reason": None,
        })


def test_declared_order_rejects_mechanical_contradictions_only():
    first = ValidTime.order_only(
        order_scope="service:114430",
        order_index=2,
        indeterminacy_reason="Only relative order was recorded.",
    )
    later = ValidTime.order_only(
        order_scope="service:114430",
        order_index=3,
        indeterminacy_reason="Only relative order was recorded.",
    )
    assert not transition_cannot_follow(first, later)
    assert transition_cannot_follow(later, first)
    assert transition_cannot_follow(
        ValidTime.exact("2026-02-01T00:00:00+00:00"),
        ValidTime.exact("2026-01-01T00:00:00+00:00"),
    )

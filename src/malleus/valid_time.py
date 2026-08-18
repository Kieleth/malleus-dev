"""Precision-aware valid-time boundaries and three-valued query semantics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from typing import Any, Mapping
from zoneinfo import ZoneInfo


TZDATA_PACKAGE_VERSION = "2026.3"
TZDATA_VERSION = "2026c"


class ValidTimeError(ValueError):
    """A valid-time value states an invalid or incomplete temporal fact."""


class ValidTimePrecision(str, Enum):
    EXACT_TIMESTAMP = "EXACT_TIMESTAMP"
    CALENDAR_DAY = "CALENDAR_DAY"
    BOUNDED_INTERVAL = "BOUNDED_INTERVAL"
    ORDER_ONLY = "ORDER_ONLY"
    UNRESOLVED_PRIOR_BOUNDARY = "UNRESOLVED_PRIOR_BOUNDARY"


class BoundaryRelation(str, Enum):
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    INDETERMINATE = "INDETERMINATE"


class TemporalRecordState(str, Enum):
    DEFINITELY_PRESENT = "DEFINITELY_PRESENT"
    DEFINITELY_ABSENT = "DEFINITELY_ABSENT"
    INDETERMINATE = "INDETERMINATE"


class ValidTimeViewState(str, Enum):
    DETERMINATE = "DETERMINATE"
    INDETERMINATE = "INDETERMINATE"


_REASON_CODES = {
    ValidTimePrecision.CALENDAR_DAY: "CALENDAR_DAY_TRANSITION_WINDOW",
    ValidTimePrecision.BOUNDED_INTERVAL: "BOUNDED_TRANSITION_WINDOW",
    ValidTimePrecision.ORDER_ONLY: "ORDER_ONLY_WITHOUT_ABSOLUTE_BOUNDARY",
    ValidTimePrecision.UNRESOLVED_PRIOR_BOUNDARY: "UNRESOLVED_PRIOR_BOUNDARY",
}


@dataclass(frozen=True)
class ValidTime:
    """One transition boundary without invented temporal precision."""

    valid_time_precision: ValidTimePrecision | str
    exact_timestamp: str | None = None
    calendar_date: str | None = None
    timezone: str | None = None
    timezone_database_version: str | None = None
    earliest_possible: str | None = None
    latest_possible: str | None = None
    order_scope: str | None = None
    order_index: int | None = None
    indeterminacy_reason: str | None = None

    def __post_init__(self) -> None:
        try:
            precision = ValidTimePrecision(self.valid_time_precision)
        except (TypeError, ValueError) as error:
            valid = [item.value for item in ValidTimePrecision]
            raise ValidTimeError(
                f"valid_time_precision must be one of {valid}"
            ) from error
        object.__setattr__(self, "valid_time_precision", precision)

        populated = {
            name
            for name in (
                "exact_timestamp",
                "calendar_date",
                "timezone",
                "timezone_database_version",
                "earliest_possible",
                "latest_possible",
                "order_scope",
                "order_index",
                "indeterminacy_reason",
            )
            if getattr(self, name) is not None
        }
        required = {
            ValidTimePrecision.EXACT_TIMESTAMP: {"exact_timestamp"},
            ValidTimePrecision.CALENDAR_DAY: {
                "calendar_date",
                "timezone",
                "timezone_database_version",
                "indeterminacy_reason",
            },
            ValidTimePrecision.BOUNDED_INTERVAL: {
                "earliest_possible",
                "latest_possible",
                "indeterminacy_reason",
            },
            ValidTimePrecision.ORDER_ONLY: {
                "order_scope",
                "order_index",
                "indeterminacy_reason",
            },
            ValidTimePrecision.UNRESOLVED_PRIOR_BOUNDARY: {
                "indeterminacy_reason",
            },
        }[precision]
        if populated != required:
            missing = sorted(required - populated)
            forbidden = sorted(populated - required)
            details = []
            if missing:
                details.append("missing " + ", ".join(missing))
            if forbidden:
                details.append("forbids " + ", ".join(forbidden))
            raise ValidTimeError(f"{precision.value}: {'; '.join(details)}")

        if precision is ValidTimePrecision.EXACT_TIMESTAMP:
            _stored_datetime(self.exact_timestamp, "exact_timestamp")
        elif precision is ValidTimePrecision.CALENDAR_DAY:
            _stored_date(self.calendar_date, "calendar_date")
            _zone(self.timezone, self.timezone_database_version)
            _reason(self.indeterminacy_reason)
            self.bounds()
        elif precision is ValidTimePrecision.BOUNDED_INTERVAL:
            earliest = _stored_datetime(self.earliest_possible, "earliest_possible")
            latest = _stored_datetime(self.latest_possible, "latest_possible")
            if _utc(latest) <= _utc(earliest):
                raise ValidTimeError("latest_possible must be later than earliest_possible")
            _reason(self.indeterminacy_reason)
        elif precision is ValidTimePrecision.ORDER_ONLY:
            _canonical_text(self.order_scope, "order_scope")
            if (
                not isinstance(self.order_index, int)
                or isinstance(self.order_index, bool)
                or self.order_index < 1
            ):
                raise ValidTimeError("order_index must be a positive integer")
            _reason(self.indeterminacy_reason)
        else:
            _reason(self.indeterminacy_reason)

    @classmethod
    def exact(cls, timestamp: str) -> "ValidTime":
        return cls(ValidTimePrecision.EXACT_TIMESTAMP, exact_timestamp=timestamp)

    @classmethod
    def calendar_day(
        cls,
        calendar_date: str,
        *,
        timezone: str,
        indeterminacy_reason: str,
    ) -> "ValidTime":
        return cls(
            ValidTimePrecision.CALENDAR_DAY,
            calendar_date=calendar_date,
            timezone=timezone,
            timezone_database_version=TZDATA_VERSION,
            indeterminacy_reason=indeterminacy_reason,
        )

    @classmethod
    def bounded_interval(
        cls,
        earliest_possible: str,
        latest_possible: str,
        *,
        indeterminacy_reason: str,
    ) -> "ValidTime":
        return cls(
            ValidTimePrecision.BOUNDED_INTERVAL,
            earliest_possible=earliest_possible,
            latest_possible=latest_possible,
            indeterminacy_reason=indeterminacy_reason,
        )

    @classmethod
    def order_only(
        cls,
        *,
        order_scope: str,
        order_index: int,
        indeterminacy_reason: str,
    ) -> "ValidTime":
        return cls(
            ValidTimePrecision.ORDER_ONLY,
            order_scope=order_scope,
            order_index=order_index,
            indeterminacy_reason=indeterminacy_reason,
        )

    @classmethod
    def unresolved_prior_boundary(cls, *, indeterminacy_reason: str) -> "ValidTime":
        return cls(
            ValidTimePrecision.UNRESOLVED_PRIOR_BOUNDARY,
            indeterminacy_reason=indeterminacy_reason,
        )

    @classmethod
    def from_value(cls, value: Any, context: str = "valid time") -> "ValidTime":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ValidTimeError(f"{context} must be a precision-aware object")
        if any(not isinstance(key, str) for key in value):
            raise ValidTimeError(f"{context} keys must be strings")
        known = set(cls.__dataclass_fields__)
        unknown = sorted(set(value) - known)
        if unknown:
            raise ValidTimeError(f"{context} has unknown fields: {', '.join(unknown)}")
        if "valid_time_precision" not in value:
            raise ValidTimeError(f"{context} is missing valid_time_precision")
        nulls = sorted(name for name, item in value.items() if item is None)
        if nulls:
            raise ValidTimeError(f"{context} must omit null fields: {', '.join(nulls)}")
        try:
            result = cls(**dict(value))
        except ValidTimeError as error:
            raise ValidTimeError(f"{context}: {error}") from error
        if result.as_dict() != dict(value):
            raise ValidTimeError(f"{context} must use the canonical variant shape")
        return result

    @property
    def reason_code(self) -> str | None:
        return _REASON_CODES.get(self.valid_time_precision)

    def bounds(self) -> tuple[datetime | None, datetime | None]:
        if self.valid_time_precision is ValidTimePrecision.EXACT_TIMESTAMP:
            point = _stored_datetime(self.exact_timestamp, "exact_timestamp")
            return point, point
        if self.valid_time_precision is ValidTimePrecision.CALENDAR_DAY:
            day = _stored_date(self.calendar_date, "calendar_date")
            zone = _zone(self.timezone, self.timezone_database_version)
            try:
                following = day + timedelta(days=1)
            except OverflowError as error:
                raise ValidTimeError("calendar_date has no following day") from error
            earliest = datetime.combine(day, time.min, zone)
            latest = datetime.combine(following, time.min, zone)
            if _utc(latest) <= _utc(earliest):
                raise ValidTimeError(
                    "calendar_date does not denote a positive interval in timezone"
                )
            return earliest, latest
        if self.valid_time_precision is ValidTimePrecision.BOUNDED_INTERVAL:
            return (
                _stored_datetime(self.earliest_possible, "earliest_possible"),
                _stored_datetime(self.latest_possible, "latest_possible"),
            )
        return None, None

    def relation_at(self, point: datetime) -> BoundaryRelation:
        if not isinstance(point, datetime) or point.tzinfo is None or point.utcoffset() is None:
            raise ValidTimeError("as-of point must be a timezone-aware datetime")
        earliest, latest = self.bounds()
        if earliest is None or latest is None:
            return BoundaryRelation.INDETERMINATE
        if _utc(point) < _utc(earliest):
            return BoundaryRelation.BEFORE
        if _utc(point) >= _utc(latest):
            return BoundaryRelation.AFTER
        return BoundaryRelation.INDETERMINATE

    def display_bounds(self) -> tuple[str | None, str | None]:
        earliest, latest = self.bounds()
        return (
            earliest.isoformat() if earliest is not None else None,
            latest.isoformat() if latest is not None else None,
        )

    def as_dict(self) -> dict[str, Any]:
        result = {"valid_time_precision": self.valid_time_precision.value}
        for name in (
            "exact_timestamp",
            "calendar_date",
            "timezone",
            "timezone_database_version",
            "earliest_possible",
            "latest_possible",
            "order_scope",
            "order_index",
            "indeterminacy_reason",
        ):
            value = getattr(self, name)
            if value is not None:
                result[name] = value
        return result


def transition_cannot_follow(prior: ValidTime, replacement: ValidTime) -> bool:
    """Return true only when the two declarations mechanically contradict order."""
    if (
        prior.valid_time_precision is ValidTimePrecision.ORDER_ONLY
        and replacement.valid_time_precision is ValidTimePrecision.ORDER_ONLY
        and prior.order_scope == replacement.order_scope
        and replacement.order_index <= prior.order_index
    ):
        return True
    prior_earliest, _ = prior.bounds()
    _, replacement_latest = replacement.bounds()
    return (
        prior_earliest is not None
        and replacement_latest is not None
        and _utc(replacement_latest) <= _utc(prior_earliest)
    )


def _canonical_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidTimeError(f"{name} must be a nonblank string")
    if value != value.strip():
        raise ValidTimeError(f"{name} must not contain surrounding whitespace")
    return value


def _reason(value: Any) -> str:
    return _canonical_text(value, "indeterminacy_reason")


def _stored_date(value: Any, name: str) -> date:
    if not isinstance(value, str):
        raise ValidTimeError(f"{name} must be an ISO 8601 calendar date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValidTimeError(f"{name} must be an ISO 8601 calendar date") from error
    if parsed.isoformat() != value:
        raise ValidTimeError(f"{name} must use canonical ISO 8601 encoding")
    return parsed


def _stored_datetime(value: Any, name: str) -> datetime:
    if not isinstance(value, str):
        raise ValidTimeError(f"{name} must be a timezone-aware ISO 8601 datetime")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValidTimeError(f"{name} must be an ISO 8601 datetime") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidTimeError(f"{name} must include a timezone offset")
    if parsed.isoformat() != value:
        raise ValidTimeError(f"{name} must use canonical ISO 8601 encoding")
    return parsed


def _zone(value: Any, database_version: Any) -> ZoneInfo:
    name = _canonical_text(value, "timezone")
    declared_version = _canonical_text(
        database_version,
        "timezone_database_version",
    )
    return _cached_zone(name, declared_version)


@lru_cache(maxsize=None)
def _cached_zone(name: str, declared_version: str) -> ZoneInfo:
    if declared_version != TZDATA_VERSION:
        raise ValidTimeError(
            f"timezone_database_version must equal '{TZDATA_VERSION}'"
        )
    try:
        installed_version = version("tzdata")
    except PackageNotFoundError as error:
        raise ValidTimeError(
            f"tzdata=={TZDATA_PACKAGE_VERSION} is required"
        ) from error
    if installed_version != TZDATA_PACKAGE_VERSION:
        raise ValidTimeError(
            f"tzdata=={TZDATA_PACKAGE_VERSION} is required, found {installed_version}"
        )
    try:
        from tzdata import IANA_VERSION
    except (ImportError, AttributeError) as error:
        raise ValidTimeError(
            f"tzdata=={TZDATA_PACKAGE_VERSION} must expose its IANA database version"
        ) from error
    if IANA_VERSION != TZDATA_VERSION:
        raise ValidTimeError(
            f"IANA timezone database must equal '{TZDATA_VERSION}', found '{IANA_VERSION}'"
        )
    parts = name.split("/")
    if any(not part or part in {".", ".."} for part in parts):
        raise ValidTimeError(f"timezone is not an installed IANA zone: '{name}'")
    try:
        resource = files("tzdata.zoneinfo").joinpath(*parts)
        with resource.open("rb") as stream:
            return ZoneInfo.from_file(stream, key=name)
    except (FileNotFoundError, IsADirectoryError, ModuleNotFoundError, ValueError) as error:
        raise ValidTimeError(f"timezone is not an installed IANA zone: '{name}'") from error


def _utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc)

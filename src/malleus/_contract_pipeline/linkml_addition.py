"""One rule for composing an additive LinkML fragment onto a root source.

A proposal is born a fragment. Core composes it onto the retained root itself,
which is what lets a proposer hold no compiler and lets Core check the addition
against the source it actually compiled, not against a contract someone handed
it.

The rule has no options. A fragment may carry only the five keys in
:data:`LINKML_ADDITION_KEYS`, and under them it may only add:

* ``classes`` and ``slots``: every named entry must be absent from the base.
  A fragment that names an existing class refuses, including one that carries
  nothing but ``slot_usage`` for it, because narrowing an existing class is a
  change to it and not an addition.
* ``enums``: a new enum arrives whole; an existing one admits new
  ``permissible_values`` keys and nothing else.
* ``imports``: literals not already imported.
* ``prefixes``: prefix names not already bound.

The output is deterministic. The base's key order survives, additions are
appended in the fragment's own order, and one fixed serialiser writes the
result, so the same two inputs give the same bytes every time.

On the serialiser: the compiled validated contract does not depend on YAML
style or on key order. Compiling
``research/.../small_shop/partial_shipments/small-shop-with-shipments.yaml`` and
compiling its round trip through ``yaml.safe_dump`` give the same
``validated_fact_set_sha256`` under ``sort_keys`` both false and true, and under
both flow styles. So re-serialising the base is not a semantic act, and the form
chosen here is the one the compiler treats identically to the authored file.
Comments do not survive, which costs the retained source its prose and costs the
contract nothing.
"""

from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto
from typing import Mapping

import yaml
from yaml.tokens import (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    DocumentEndToken,
    DocumentStartToken,
    TagToken,
)


LINKML_ADDITION_KEYS = ("classes", "enums", "imports", "prefixes", "slots")
"""The only top-level keys an additive fragment may carry."""

_NAMED_SECTIONS = ("classes", "slots")
_PERMISSIBLE_VALUES = "permissible_values"
_FORBIDDEN_TOKENS = (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    DocumentEndToken,
    DocumentStartToken,
    TagToken,
)


class LinkMLAdditionRefusalReason(Enum):
    """Every way an additive composition fails closed."""

    MALFORMED_BASE = auto()
    MALFORMED_FRAGMENT = auto()
    UNSUPPORTED_FRAGMENT_KEY = auto()
    EXISTING_CLASS = auto()
    EXISTING_SLOT = auto()
    EXISTING_ENUM_FIELD = auto()
    EXISTING_PERMISSIBLE_VALUE = auto()
    EXISTING_IMPORT = auto()
    EXISTING_PREFIX = auto()


class LinkMLAdditionRefusal(ValueError):
    def __init__(self, reason: LinkMLAdditionRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _refuse(reason: LinkMLAdditionRefusalReason, detail: str) -> LinkMLAdditionRefusal:
    return LinkMLAdditionRefusal(reason, detail)


class _UniqueKeyLoader(yaml.SafeLoader):
    """A safe loader that refuses a repeated mapping key."""

    def construct_mapping(self, node, deep=False):  # type: ignore[no-untyped-def]
        seen: set[object] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise yaml.YAMLError(f"duplicate key {key!r}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


class _PlainDumper(yaml.SafeDumper):
    """One fixed serialiser: no anchors, block style, the given key order."""

    def ignore_aliases(self, data):  # type: ignore[no-untyped-def]
        return True


def _parse(source: object, reason: LinkMLAdditionRefusalReason) -> dict[str, object]:
    if type(source) is not bytes:
        raise _refuse(reason, "input must be exact bytes")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _refuse(reason, "input is not valid UTF-8") from error
    if text.startswith("﻿"):
        raise _refuse(reason, "input must not carry a byte-order mark")
    try:
        for token in yaml.scan(text, Loader=yaml.SafeLoader):
            if isinstance(token, _FORBIDDEN_TOKENS):
                raise yaml.YAMLError(f"rejected token {type(token).__name__}")
        data = yaml.load(text, Loader=_UniqueKeyLoader)  # noqa: S506
    except yaml.YAMLError as error:
        raise _refuse(reason, f"input is not strict YAML: {error}") from error
    if not isinstance(data, dict) or not data:
        raise _refuse(reason, "input must be a nonempty YAML mapping")
    if any(not isinstance(key, str) or not key for key in data):
        raise _refuse(reason, "mapping keys must be nonempty strings")
    return data


def _section(
    data: Mapping[str, object], key: str, reason: LinkMLAdditionRefusalReason
) -> dict[str, object]:
    value = data.get(key)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise _refuse(reason, f"{key} must be a mapping")
    return value


def _fragment_mapping(fragment: Mapping[str, object], key: str) -> dict[str, object]:
    value = fragment[key]
    if not isinstance(value, dict) or not value:
        raise _refuse(
            LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT,
            f"fragment {key} must be a nonempty mapping",
        )
    if any(not isinstance(name, str) or not name for name in value):
        raise _refuse(
            LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT,
            f"fragment {key} names must be nonempty strings",
        )
    return value


def _add_named(
    composed: dict[str, object],
    base: Mapping[str, object],
    fragment: Mapping[str, object],
    key: str,
    reason: LinkMLAdditionRefusalReason,
) -> None:
    existing = _section(base, key, LinkMLAdditionRefusalReason.MALFORMED_BASE)
    additions = _fragment_mapping(fragment, key)
    for name, definition in additions.items():
        if name in existing:
            raise _refuse(reason, f"{key} already declares {name}")
    target = composed.setdefault(key, {})
    assert isinstance(target, dict)
    for name, definition in additions.items():
        target[name] = deepcopy(definition)


def _add_enums(
    composed: dict[str, object],
    base: Mapping[str, object],
    fragment: Mapping[str, object],
) -> None:
    existing = _section(base, "enums", LinkMLAdditionRefusalReason.MALFORMED_BASE)
    additions = _fragment_mapping(fragment, "enums")
    target = composed.setdefault("enums", {})
    assert isinstance(target, dict)
    for name, definition in additions.items():
        if name not in existing:
            target[name] = deepcopy(definition)
            continue
        if not isinstance(definition, dict) or set(definition) != {_PERMISSIBLE_VALUES}:
            raise _refuse(
                LinkMLAdditionRefusalReason.EXISTING_ENUM_FIELD,
                f"enum {name} exists; only new {_PERMISSIBLE_VALUES} may be added",
            )
        values = definition[_PERMISSIBLE_VALUES]
        if not isinstance(values, dict) or not values:
            raise _refuse(
                LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT,
                f"enum {name} must add a nonempty {_PERMISSIBLE_VALUES} mapping",
            )
        declared = existing[name]
        current = (
            declared.get(_PERMISSIBLE_VALUES) if isinstance(declared, dict) else None
        )
        current = current if isinstance(current, dict) else {}
        for value_name in values:
            if value_name in current:
                raise _refuse(
                    LinkMLAdditionRefusalReason.EXISTING_PERMISSIBLE_VALUE,
                    f"enum {name} already declares {value_name}",
                )
        slot = target.setdefault(name, {})
        assert isinstance(slot, dict)
        into = slot.setdefault(_PERMISSIBLE_VALUES, {})
        assert isinstance(into, dict)
        for value_name, value in values.items():
            into[value_name] = deepcopy(value)


def _add_imports(
    composed: dict[str, object],
    base: Mapping[str, object],
    fragment: Mapping[str, object],
) -> None:
    existing = base.get("imports") or []
    if not isinstance(existing, list):
        raise _refuse(
            LinkMLAdditionRefusalReason.MALFORMED_BASE, "imports must be a sequence"
        )
    additions = fragment["imports"]
    if not isinstance(additions, list) or not additions:
        raise _refuse(
            LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT,
            "fragment imports must be a nonempty sequence",
        )
    for literal in additions:
        if not isinstance(literal, str) or not literal:
            raise _refuse(
                LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT,
                "each import literal must be a nonempty string",
            )
        if literal in existing:
            raise _refuse(
                LinkMLAdditionRefusalReason.EXISTING_IMPORT,
                f"imports already carry {literal}",
            )
    target = composed.setdefault("imports", [])
    assert isinstance(target, list)
    target.extend(additions)


def _add_prefixes(
    composed: dict[str, object],
    base: Mapping[str, object],
    fragment: Mapping[str, object],
) -> None:
    existing = _section(base, "prefixes", LinkMLAdditionRefusalReason.MALFORMED_BASE)
    additions = _fragment_mapping(fragment, "prefixes")
    for name in additions:
        if name in existing:
            raise _refuse(
                LinkMLAdditionRefusalReason.EXISTING_PREFIX,
                f"prefixes already bind {name}",
            )
    target = composed.setdefault("prefixes", {})
    assert isinstance(target, dict)
    for name, value in additions.items():
        target[name] = deepcopy(value)


def compose_linkml_addition(base_root_bytes: object, fragment_bytes: object) -> bytes:
    """Compose one additive fragment onto one LinkML root, or refuse.

    Returns the composed root's exact bytes. Nothing is read from disk, no
    import is resolved, and no compiler runs: this is the source the caller
    then compiles.
    """

    base = _parse(base_root_bytes, LinkMLAdditionRefusalReason.MALFORMED_BASE)
    fragment = _parse(fragment_bytes, LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT)
    unsupported = [key for key in fragment if key not in LINKML_ADDITION_KEYS]
    if unsupported:
        raise _refuse(
            LinkMLAdditionRefusalReason.UNSUPPORTED_FRAGMENT_KEY,
            "an addition may carry only "
            + ", ".join(LINKML_ADDITION_KEYS)
            + f"; this one carries {sorted(unsupported)[0]}",
        )
    composed = deepcopy(base)
    for key in fragment:
        if key in _NAMED_SECTIONS:
            _add_named(
                composed,
                base,
                fragment,
                key,
                LinkMLAdditionRefusalReason.EXISTING_CLASS
                if key == "classes"
                else LinkMLAdditionRefusalReason.EXISTING_SLOT,
            )
        elif key == "enums":
            _add_enums(composed, base, fragment)
        elif key == "imports":
            _add_imports(composed, base, fragment)
        else:
            _add_prefixes(composed, base, fragment)
    return yaml.dump(
        composed,
        Dumper=_PlainDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=4096,
    ).encode("utf-8")


__all__ = (
    "LINKML_ADDITION_KEYS",
    "LinkMLAdditionRefusal",
    "LinkMLAdditionRefusalReason",
    "compose_linkml_addition",
)

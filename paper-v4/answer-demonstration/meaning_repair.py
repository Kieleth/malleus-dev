"""Scope guard for one context amendment. Source review is a separate gate."""

from copy import deepcopy
import json

from meaning_audit import indexed, references, replacement_closure, unique


CONTEXT_FIELDS = frozenset(
    {
        "statement",
        "description",
        "subject",
        "count_scope",
        "duration",
        "assertion_locator",
        "statement_sha256",
    }
)


def exact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_scope(base, candidate, surface, *, targets):
    try:
        return _check(base, candidate, surface, targets)
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(f"missing or malformed amendment: {error}") from error


def _check(base, candidate, surface, targets):
    proposed = candidate["records"]
    require(set(proposed) == set(base), "record family closure differs")
    old, new = indexed(base), indexed(proposed)
    require(bool(new) and not old.keys() & new.keys(), "fresh replacement IDs required")
    require(set(targets) <= old.keys(), "unknown amendment target")
    pairs = unique(candidate["supersessions"], "supersedes_record_id")
    mapping = {key: pair["record_id"] for key, pair in pairs.items()}
    require(
        mapping.keys() <= old.keys()
        and len(mapping) == len(new)
        and set(mapping.values()) == new.keys(),
        "one-to-one replacement closure required",
    )
    selected = set(mapping) & set(targets)
    refs = references(base, surface)
    require(
        bool(selected) and set(mapping) == replacement_closure(selected, refs),
        "exact declared dependency closure required",
    )
    old_families = {r["id"]: f for f, rows in base.items() for r in rows}
    new_families = {r["id"]: f for f, rows in proposed.items() for r in rows}
    types = unique(surface["record_types"], "name")
    for prior, current in mapping.items():
        before, after = old[prior], new[current]
        require(
            old_families[prior] == new_families[current]
            and old_families[prior] in {"entities", "relations"}
            and before["type"] == after["type"],
            "family and exact type must survive",
        )
        expected = deepcopy(before)
        expected["id"] = current
        for ref in refs:
            if ref["record_id"] == prior and ref["target_id"] in mapping:
                parent = expected
                for part in ref["path"][:-1]:
                    parent = parent[part]
                parent[ref["path"][-1]] = mapping[ref["target_id"]]
        if prior not in selected:
            require(
                exact(after) == exact(expected),
                "dependant may only retarget references",
            )
            continue
        require(
            old_families[prior] == "entities",
            "meaning changes require selected entities",
        )
        require(
            exact({k: v for k, v in expected.items() if k != "properties"})
            == exact({k: v for k, v in after.items() if k != "properties"}),
            "entity header must survive",
        )
        left, right = expected["properties"], after["properties"]
        changed = {
            key
            for key in left.keys() | right.keys()
            if (key in left) != (key in right)
            or (key in left and key in right and exact(left[key]) != exact(right[key]))
        }
        declared = {slot["name"] for slot in types[before["type"]]["slots"]}
        require(
            bool(changed) and changed <= CONTEXT_FIELDS & declared,
            "only declared context fields may change; values and hypothesis status are fixed",
        )
        require(
            any(
                key not in {"assertion_locator", "statement_sha256"} for key in changed
            ),
            "evidence-only replacement is not a meaning amendment",
        )
        for key in changed & right.keys():
            require(
                type(right[key]) is str and bool(right[key].strip()),
                "nonblank context text required",
            )
    projected = {
        family: [r for r in rows if r["id"] not in mapping] + proposed[family]
        for family, rows in base.items()
    }
    references(projected, surface)
    return mapping

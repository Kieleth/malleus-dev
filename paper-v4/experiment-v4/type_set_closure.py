"""Refuse a type set that lists a type without its surface subtypes.

The v4.9 executor projects every reached record by its own type and refuses a
type the binding never names (``native_query.py``, ``_own_fields``). The
facade's typed query returns a type's records and its subtypes', so a set that
lists a parent and not a surface subtype binds a query the executor refuses
after admission: run-21's first binding reached an AnalyticalMethod record
through Method with no projection for it (E-0196). This reads the closure the
runner will use, the validated contract's ``rdfs:subClassOf`` facts, and
refuses at acceptance instead, where the evaluator can still correct the set
without a row in existence. The surface carries no ancestry; nothing here
reads the ontology source.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SUBCLASS_OF = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
REASON = "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES"


def ancestors(contract: dict) -> dict[str, set[str]]:
    """Every class's transitive superclasses, by qualified name."""

    parents: dict[str, set[str]] = {}
    for fact in contract["facts"]:
        if fact["predicate"] == SUBCLASS_OF:
            parents.setdefault(fact["subject"], set()).add(fact["object"])
    closure: dict[str, set[str]] = {}

    def climb(name: str) -> set[str]:
        if name not in closure:
            closure[name] = set()
            for parent in parents.get(name, ()):
                closure[name] |= {parent} | climb(parent)
        return closure[name]

    for name in list(parents):
        climb(name)
    return closure


def omissions(surface: dict, contract: dict, type_sets: dict) -> dict[str, list[str]]:
    """Per question, the surface subtypes of a listed type that the set omits."""

    qualified = {item["name"]: item["qualified_name"] for item in surface["record_types"]}
    above = ancestors(contract)
    result: dict[str, list[str]] = {}
    for question, listed in type_sets.items():
        absent = [name for name in listed if name not in qualified]
        if absent:
            raise ValueError(f"{question}: type not on the surface: {', '.join(absent)}")
        listed_qualified = {qualified[name] for name in listed}
        missing = sorted(
            name
            for name, qualified_name in qualified.items()
            if name not in listed and above.get(qualified_name, set()) & listed_qualified
        )
        if missing:
            result[question] = missing
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--surface", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--type-sets", type=Path, required=True)
    arguments = parser.parse_args(argv)
    found = omissions(
        json.loads(arguments.surface.read_bytes()),
        json.loads(arguments.contract.read_bytes()),
        json.loads(arguments.type_sets.read_bytes()),
    )
    print(
        json.dumps(
            {
                "status": "REFUSED" if found else "ACCEPTED",
                "reason": REASON if found else None,
                "omissions": found,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())

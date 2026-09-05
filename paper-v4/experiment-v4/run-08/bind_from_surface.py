"""Expand one file of type sets into the exhaustive run-08 query binding.

Run-04's binding was chosen after its row counts were seen: a hand-picked draft
returned no row for one question and was replaced, and a second draft's type set
was edited once its 75 citation rows were visible (deep sweep D-01, and the
``bound_by`` text run-04's own binding carries). The selection between bindings
was therefore conditioned on the result.

Run-08 moves the whole binding to ontology acceptance, before phase two exists.
The evaluator writes one file of type sets per question, read from the accepted
population surface and nothing else. This script expands it mechanically: every
ordered pair of a question's types under every relation type on the surface,
with a fixed field projection per type made of that type's non-housekeeping
slots. No row, no record identifier, no graph size and no answer value can enter,
because none of them exists yet. The producer never sees the file.

The receipt argument is ``PENDING`` at acceptance and the replay receipt digest
after the replay is frozen. Only that one field differs between the two runs;
``cases_sha256`` digests the queries alone, so the binding that executes is
provably the binding whose digest the launch log recorded at acceptance.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v2"
SURFACE_SCHEMA = "malleus.paper-v4.population-surface/v2"
BOUND_AT_STAGE = "ONTOLOGY_ACCEPTANCE"
PENDING = "PENDING"

# The graph's own bookkeeping, by qualified name. Everything a record type
# carries beyond this set projects, so the projection is a property of the
# surface rather than a per-question judgement.
HOUSEKEEPING_SLOTS = frozenset(
    {
        "https://malleus.dev/schema/created_at",
        "https://malleus.dev/schema/id",
        "https://malleus.dev/schema/source_id",
        "https://malleus.dev/schema/tags",
        "https://malleus.dev/schema/target_id",
        "https://malleus.dev/schema/updated_at",
    }
)

BOUND_BY = (
    "paper evaluator, at ontology acceptance and before phase two, from the"
    " accepted population surface only. The evaluator's one judgement is each"
    " question's type set; this script expands it into every ordered pair of"
    " those types under every relation type on the surface, projecting each"
    " type's non-housekeeping slots. No population, admission, replay, row or"
    " row count existed when the type sets were written, so no binding here was"
    " selected against a result. Run-04's binding was revised twice after its"
    " rows were seen (deep sweep D-01); this is the change that closes it."
)


class BindingRefusal(ValueError):
    """The surface or the type sets do not support an exhaustive binding."""


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


def _projection(record_type: dict[str, object]) -> list[str]:
    return [
        str(slot["name"])
        for slot in record_type["slots"]
        if str(slot["qualified_name"]) not in HOUSEKEEPING_SLOTS
    ]


def load_surface(source: bytes) -> dict[str, dict[str, object]]:
    surface = json.loads(source)
    if surface.get("schema") != SURFACE_SCHEMA:
        raise BindingRefusal(f"population surface must declare {SURFACE_SCHEMA}")
    by_name: dict[str, dict[str, object]] = {}
    for record_type in surface["record_types"]:
        name = str(record_type["name"])
        if name in by_name:
            raise BindingRefusal(f"surface names one record type twice: {name}")
        by_name[name] = record_type
    return by_name


def _relation_types(by_name: dict[str, dict[str, object]]) -> list[str]:
    relations = sorted(
        name for name, item in by_name.items() if item["family"] == "RELATION"
    )
    if not relations:
        raise BindingRefusal("the surface carries no RELATION record type")
    return relations


def build(
    *, surface_source: bytes, type_sets: dict[str, list[str]], replay_receipt: str
) -> dict[str, object]:
    by_name = load_surface(surface_source)
    relations = _relation_types(by_name)
    if not type_sets:
        raise BindingRefusal("the type-set file names no question")

    queries: list[dict[str, object]] = []
    resolved: dict[str, list[str]] = {}
    for question_id in sorted(type_sets):
        types = sorted(set(type_sets[question_id]))
        if not types:
            raise BindingRefusal(f"question {question_id} carries no type")
        absent = [name for name in types if name not in by_name]
        if absent:
            raise BindingRefusal(
                f"question {question_id} names types absent from the surface:"
                f" {', '.join(absent)}"
            )
        resolved[question_id] = types
        projections = {name: _projection(by_name[name]) for name in types}
        relation_projections = {name: _projection(by_name[name]) for name in relations}
        cases: list[dict[str, object]] = []
        for source_type in types:
            for relation_type in relations:
                for target_type in types:
                    cases.append(
                        {
                            "ordinal": len(cases) + 1,
                            "output_fields": {
                                "relation": relation_projections[relation_type],
                                "source": projections[source_type],
                                "target": projections[target_type],
                            },
                            "relation_record_type": relation_type,
                            "source_record_type": source_type,
                            "target_record_type": target_type,
                        }
                    )
        expected = len(types) * len(types) * len(relations)
        if len(cases) != expected:
            raise BindingRefusal(
                f"question {question_id} expanded to {len(cases)} cases,"
                f" not the exhaustive {expected}"
            )
        queries.append(
            {
                "id": f"NQ-{question_id}",
                "question_id": question_id,
                "cases": cases,
            }
        )

    return {
        "schema": BINDING_SCHEMA,
        "status": "FROZEN_AT_ONTOLOGY_ACCEPTANCE",
        "bound_at_stage": BOUND_AT_STAGE,
        "bound_by": BOUND_BY,
        "bound_after_replay_receipt_sha256": replay_receipt,
        "cases_sha256": _digest(_canonical(queries)),
        "expansion": {
            "housekeeping_slots": sorted(HOUSEKEEPING_SLOTS),
            "producer_visibility": "WITHHELD",
            "relation_record_types": relations,
            "rule": (
                "every ordered pair of a question's types under every relation"
                " type on the surface, each type projecting its"
                " non-housekeeping slots"
            ),
        },
        "population_surface_sha256": _digest(surface_source),
        "type_sets": resolved,
        "queries": queries,
    }


def execute(arguments: argparse.Namespace) -> dict[str, object]:
    output = Path(arguments.output)
    if output.exists():
        raise BindingRefusal(f"binding already exists: {output}")
    receipt = str(arguments.replay_receipt)
    if receipt != PENDING and not receipt.startswith("sha256:"):
        raise BindingRefusal(
            f"--replay-receipt must be {PENDING} or a sha256: digest, not {receipt}"
        )
    type_sets = json.loads(Path(arguments.type_sets).read_bytes())
    if not isinstance(type_sets, dict):
        raise BindingRefusal("the type-set file must map question id to type list")
    binding = build(
        surface_source=Path(arguments.surface).read_bytes(),
        type_sets=type_sets,
        replay_receipt=receipt,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical(binding) + b"\n")
    return binding


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", required=True, help="accepted population surface")
    parser.add_argument(
        "--type-sets", required=True, help="question id to surface type list"
    )
    parser.add_argument(
        "--replay-receipt",
        required=True,
        help=f"{PENDING} at acceptance, the replay receipt digest after replay",
    )
    parser.add_argument("--output", required=True, help="binding file to write")
    arguments = parser.parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(
            f"bind-from-surface: {type(error).__name__}: {error}", file=sys.stderr
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

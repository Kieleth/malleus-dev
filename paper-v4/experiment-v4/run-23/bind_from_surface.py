"""Expand one file of type sets into the exhaustive run-23 query binding.

Run-08 moved the whole binding to ontology acceptance, before phase two exists,
and expanded the evaluator's type sets into every ordered pair of a question's
types under every relation type on the surface. That is still what a RELATION
case is and this script still writes it at the same stage from the same input.
Run-09 added two type-only kinds beside it, ENTITY and SUBJECT, and reached the
records that carry no relation at all.

What v4.4 changes is one line of the ENTITY expansion and nothing else. Run-09
emitted an ENTITY case for every type in a question's set, which returns every
admitted record of every one of those types. 1,061 of its 1,466 rows came back
that way: 1,052 of them supported, none of them an answer, and the review cost
1.21 million tokens across four sessions against 322 thousand for run-04 (the
v4.3 RCA, section 5). The restriction:

* ``ENTITY`` is emitted only for the types in a question's set that do **not**
  carry ``subject`` on the surface. A source-asserted record reaches a question
  through its subject; one that is unattached reaches nothing, which is the
  honest outcome the coverage census already counts.
* ``SUBJECT`` and ``RELATION`` expansion is unchanged, so every subject-bearing
  record that is attached is still returned, projecting the thing it is about.

What v4.12 adds is a fourth case kind and a refusal. ``ENTITY_NO_SUBJECT`` is
emitted for every subject-bearing type in a question's set and returns the
records of that type whose ``subject`` slot is absent, each of them an
``ENTITY`` row witnessed by itself, so a record about nothing the producer
stated is reached once instead of not at all. Run-21 carried 237 such records
and CQ-01's answer, the instrument count, was two of them (E-0197). A record
that does carry a subject is still reached through it and never here, so
nothing the v4.4 restriction excluded on purpose comes back.

The refusal is the closure check. ``type_set_closure.omissions`` runs against
the gate's validated contract before the binding is written, so a set that
lists a type without its surface subtypes is refused where the evaluator can
still correct it. v4.11 shipped that check as a step the procedure ran by hand;
a step run by hand is a step that can be skipped, and the artefact it guards is
the one this script writes (E-0196, E-0198).

What v4.13 adds is a fifth case kind. ``SUBJECT_ANY`` pairs every
subject-bearing type in a question's set with every entity type the surface
declares, and not with the entity types the set happens to list, so a record of
a listed type that names a subject is returned whatever that subject's type is.
Run-22's CQ-T4-01 listed the claim type alone: the export carried 124 claims, 63
of them with a subject, and the question returned the 61 subject-less ones and
none of the claims that state the preferred explanation (E-0342, and the run-22
RCA's cause 1, which took the same items out of CQ-T4-02, CQ-T4-03 and
CQ-T5-01). A listed subject-bearing type now reaches its subject-less records
once, through ``ENTITY_NO_SUBJECT``, and its subject-carrying records once,
through ``SUBJECT_ANY``, whatever the subject's type. The typed ``SUBJECT`` case
does not move and is a subset of the new one; a record both reach is one row
with two ordinals, because rows already dedupe by witness.

The expansion stays mechanical and the evaluator's one judgement stays the type
set per question. ``cases_sha256`` still digests the queries alone, so the
binding that executes after the replay is provably the binding whose digest the
launch log recorded at acceptance; only
``bound_after_replay_receipt_sha256`` moves. No row, record identifier, graph
size or answer value can enter, because none of them exists yet, and the
producer never sees the file.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v6"
SURFACE_SCHEMA = "malleus.paper-v4.population-surface/v2"
BOUND_AT_STAGE = "ONTOLOGY_ACCEPTANCE"
PENDING = "PENDING"
CLOSURE_CHECK = "TYPE_SET_CLOSED_UNDER_THE_SURFACES_SUBTYPES_AT_BIND_TIME"

# The five case kinds, sorted, which is also the order the expansion emits
# them. All five are type-only: a case names record types and projected field
# names and nothing else. ``ENTITY_NO_SUBJECT`` is v4.12's addition and is
# emitted directly after ``ENTITY``, so a question's ordinals keep the two
# entity kinds first and the rows keep their order. ``SUBJECT_ANY`` is v4.13's
# and is emitted last, after the typed SUBJECT cases whose pairing it widens.
CASE_KINDS = (
    "ENTITY",
    "ENTITY_NO_SUBJECT",
    "RELATION",
    "SUBJECT",
    "SUBJECT_ANY",
)
ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"
SUBJECT_ANY = "SUBJECT_ANY"

# The reference a source-asserted record carries to the entity it is about
# (Core-13, the research pack's SourceAsserted mixin). A surface type that
# carries this slot is a SUBJECT case's first type, and from v4.4 it is not an
# ENTITY case at all: it is reached through its subject or it is not reached.
# From v4.12 the second half of that sentence has one exception. A record of a
# bearing type whose ``subject`` is absent is reached by an ENTITY_NO_SUBJECT
# case, which is the only case whose selection reads a record at all, and reads
# exactly one thing: whether the slot is there. From v4.13 a record of a bearing
# type that does carry a subject is reached by a SUBJECT_ANY case whatever the
# subject's own type is, so a type set decides what a question is about and
# never which of that type's records survive.
SUBJECT_SLOT = "subject"
ENTITY_FAMILY = "ENTITY"

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
    " question's type set; this script expands it into four kinds of case,"
    " every one of them type-only: one ENTITY case per type in the set that"
    " carries no subject on the surface, one ENTITY_NO_SUBJECT case per type in"
    " the set that does carry it, returning the records of that type whose"
    " subject slot is absent, one RELATION case per ordered pair of"
    " those types under every relation type on the surface, and one SUBJECT"
    " case per ordered pair of a subject-bearing type with an entity type in the"
    " set, and one SUBJECT_ANY case per ordered pair of a subject-bearing type"
    " in the set with an entity type the surface declares. Each"
    " type projects its non-housekeeping slots. No population, admission,"
    " replay, row or row count existed when the type sets were written, so no"
    " binding here was selected against a result. Run-04's binding was revised"
    " twice after its rows were seen (deep sweep D-01); run-08 closed that and"
    " reached nothing but relations; run-09 reached every record of every type"
    " and returned 1,061 supported non-answers; this reaches a source-asserted"
    " record through the thing it is about, and an unattached one not at all."
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


def _slot_names(record_type: dict[str, object]) -> set[str]:
    return {str(slot["name"]) for slot in record_type["slots"]}


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


def subject_bearing_types(by_name: dict[str, dict[str, object]]) -> list[str]:
    """Surface types carrying the ``subject`` reference, sorted."""
    return sorted(
        name for name, item in by_name.items() if SUBJECT_SLOT in _slot_names(item)
    )


def entity_types(by_name: dict[str, dict[str, object]]) -> list[str]:
    return sorted(
        name for name, item in by_name.items() if item["family"] == ENTITY_FAMILY
    )


def _cases(
    *,
    types: list[str],
    relations: list[str],
    by_name: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    """Every case of the five kinds a question's type set expands to.

    The v4.4 restriction is the first loop: a type that carries ``subject`` is
    reached through its subject or not at all, and gets no ENTITY case. The
    v4.12 addition is the second: the same type gets one ENTITY_NO_SUBJECT
    case, which returns the records of it that carry no subject and nothing
    else. The v4.13 addition is the last loop: the same type is paired with
    every entity type the surface declares, so a record of it that does carry a
    subject is returned whatever that subject's type is and the evaluator
    cannot lose it by leaving the subject's type out of the set.
    """

    entities_on_surface = entity_types(by_name)
    projections = {
        name: _projection(by_name[name])
        for name in [*types, *entities_on_surface]
    }
    relation_projections = {name: _projection(by_name[name]) for name in relations}
    bearing = [name for name in types if SUBJECT_SLOT in _slot_names(by_name[name])]
    unattached = [name for name in types if name not in set(bearing)]
    entities = [name for name in types if by_name[name]["family"] == ENTITY_FAMILY]
    cases: list[dict[str, object]] = []

    for record_type in unattached:
        cases.append(
            {
                "kind": "ENTITY",
                "ordinal": len(cases) + 1,
                "output_fields": {"record": projections[record_type]},
                "record_type": record_type,
            }
        )
    for record_type in bearing:
        cases.append(
            {
                "kind": ENTITY_NO_SUBJECT,
                "ordinal": len(cases) + 1,
                "output_fields": {"record": projections[record_type]},
                "record_type": record_type,
            }
        )
    for source_type in types:
        for relation_type in relations:
            for target_type in types:
                cases.append(
                    {
                        "kind": "RELATION",
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
    for record_type in bearing:
        for subject_type in entities:
            cases.append(
                {
                    "kind": "SUBJECT",
                    "ordinal": len(cases) + 1,
                    "output_fields": {
                        "record": projections[record_type],
                        "subject": projections[subject_type],
                    },
                    "record_type": record_type,
                    "subject_record_type": subject_type,
                }
            )

    for record_type in bearing:
        for subject_type in entities_on_surface:
            cases.append(
                {
                    "kind": SUBJECT_ANY,
                    "ordinal": len(cases) + 1,
                    "output_fields": {
                        "record": projections[record_type],
                        "subject": projections[subject_type],
                    },
                    "record_type": record_type,
                    "subject_record_type": subject_type,
                }
            )

    expected = (
        len(unattached)
        + len(bearing)
        + len(types) * len(types) * len(relations)
        + len(bearing) * len(entities)
        + len(bearing) * len(entities_on_surface)
    )
    if len(cases) != expected:
        raise BindingRefusal(
            f"the type set expanded to {len(cases)} cases, not the exhaustive"
            f" {expected}"
        )
    return cases


def _type_set_closure():
    """The shared closure reader, loaded by path from the experiment root.

    It lives beside the cells and not inside one, because every cell from v4.11
    on reads the same rule from the same file. Loading it by path is how the
    procedure already runs it.
    """

    path = Path(__file__).resolve().parents[1] / "type_set_closure.py"
    specification = importlib.util.spec_from_file_location(
        "paper_v4_type_set_closure", path
    )
    if specification is None or specification.loader is None:
        raise BindingRefusal(f"the closure reader is not readable: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def refuse_unclosed(
    *, surface: dict[str, object], contract: dict[str, object], type_sets: dict
) -> None:
    """Refuse a type set that lists a type without its surface subtypes.

    The facade's typed query returns a type's records and its subtypes', and the
    v4.9 executor projects every reached record by its own type and refuses a
    type the binding never names. A set that lists a parent and not a surface
    subtype therefore binds a query that is refused after the rows exist, which
    is what run-21's first binding did (E-0196). Here it is refused before the
    binding is written, with the reason and the omitted names the shared reader
    returns.
    """

    closure = _type_set_closure()
    found = closure.omissions(surface, contract, type_sets)
    if found:
        detail = "; ".join(
            f"{question} omits {', '.join(names)}"
            for question, names in sorted(found.items())
        )
        raise BindingRefusal(f"{closure.REASON}: {detail}")


def build(
    *,
    surface_source: bytes,
    type_sets: dict[str, list[str]],
    replay_receipt: str,
    contract_source: bytes,
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
        queries.append(
            {
                "id": f"NQ-{question_id}",
                "question_id": question_id,
                "cases": _cases(types=types, relations=relations, by_name=by_name),
            }
        )

    refuse_unclosed(
        surface=json.loads(surface_source),
        contract=json.loads(contract_source),
        type_sets=resolved,
    )
    return {
        "schema": BINDING_SCHEMA,
        "status": "FROZEN_AT_ONTOLOGY_ACCEPTANCE",
        "bound_at_stage": BOUND_AT_STAGE,
        "bound_by": BOUND_BY,
        "bound_after_replay_receipt_sha256": replay_receipt,
        "cases_sha256": _digest(_canonical(queries)),
        "expansion": {
            "case_kinds": list(CASE_KINDS),
            "closure_checked": CLOSURE_CHECK,
            "entity_case_scope": "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT",
            "entity_no_subject_case_scope": (
                "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_RESTRICTED_TO_RECORDS"
                "_WHOSE_SUBJECT_SLOT_IS_ABSENT"
            ),
            "entity_record_types": entity_types(by_name),
            "housekeeping_slots": sorted(HOUSEKEEPING_SLOTS),
            "producer_visibility": "WITHHELD",
            "relation_record_types": relations,
            "rule": (
                "one ENTITY case per type in a question's set that carries no"
                " subject on the surface; one ENTITY_NO_SUBJECT case per type"
                " in the set that does carry subject, returning the records of"
                " that type whose subject slot is absent; every ordered pair of"
                " the set's types"
                " under every relation type on the surface as a RELATION case;"
                " every ordered pair of a subject-bearing type in the set with"
                " an entity type in the set as a SUBJECT case; every ordered"
                " pair of a subject-bearing type in the set with an entity type"
                " the surface declares as a SUBJECT_ANY case; each type"
                " projecting its non-housekeeping slots"
            ),
            "subject_any_case_scope": (
                "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_PAIRED_WITH_EVERY_ENTITY"
                "_TYPE_THE_SURFACE_DECLARES_AND_NOT_ONLY_THE_SETS"
            ),
            "subject_bearing_record_types": subject_bearing_types(by_name),
            "subject_slot": SUBJECT_SLOT,
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
        contract_source=Path(arguments.contract).read_bytes(),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical(binding) + b"\n")
    return binding


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", required=True, help="accepted population surface")
    parser.add_argument(
        "--contract",
        required=True,
        help="the gate's validated contract, read for the surface's subtypes",
    )
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

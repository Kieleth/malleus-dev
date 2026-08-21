"""Toy 1 — the kitchen. Mise en place as a rule over a domain ordinal.

Two graphs. `sketch_writes()` is GEDANKEN's table transcribed row for row.
`sound_writes()` is a negative control that was not in the sketch: without it
the rule is only ever observed firing, which cannot tell a working rule from
one that fires on everything.
"""

from __future__ import annotations

from malleus.staging import ProposedOperation as Op

try:
    from drivers.common import check, report
except ImportError:  # direct execution
    from common import check, report

TOY = "kitchen"


def _pantry() -> list[Op]:
    return [
        Op.entity("Ingredient", "onion", {"name": "onion"}),
        Op.entity("Ingredient", "garlic", {"name": "garlic"}),
        Op.entity("Ingredient", "tomato", {"name": "tomato"}),
        Op.entity("Ingredient", "oil", {"name": "olive oil"}),
        Op.entity("Vessel", "pan", {"name": "pan"}),
        Op.entity("Dish", "sofrito", {"name": "sofrito"}),
    ]


def _uses(edge_id: str, step: str, ingredient: str) -> Op:
    return Op.relation("UsesRelation", edge_id, step, ingredient, {"relation_type": "USES"})


def _into(edge_id: str, step: str, vessel: str) -> Op:
    return Op.relation("IntoRelation", edge_id, step, vessel, {"relation_type": "INTO"})


def _yields(edge_id: str, step: str, dish: str) -> Op:
    return Op.relation("YieldsRelation", edge_id, step, dish, {"relation_type": "YIELDS"})


def sketch_writes() -> list[Op]:
    """GEDANKEN.md:63-73, transcribed exactly. The tomato is never prepped."""
    return [
        *_pantry(),
        Op.entity("PrepStep", "s1", {"step_index": 1, "prep_kind": "CHOP"}),
        Op.entity("PrepStep", "s2", {"step_index": 2, "prep_kind": "CHOP"}),
        Op.entity("CombineStep", "s3", {"step_index": 3}),
        Op.entity("CombineStep", "s4", {"step_index": 4}),
        Op.entity("CombineStep", "s5", {"step_index": 5}),
        Op.entity("CombineStep", "s6", {"step_index": 6}),
        Op.entity("CookStep", "s7", {"step_index": 7}),
        _uses("u1", "s1", "onion"),
        _uses("u2", "s2", "garlic"),
        _uses("u3", "s3", "oil"),
        _uses("u4", "s4", "onion"),
        _uses("u5", "s5", "garlic"),
        _uses("u6", "s6", "tomato"),
        _into("i3", "s3", "pan"),
        _into("i4", "s4", "pan"),
        _into("i5", "s5", "pan"),
        _into("i6", "s6", "pan"),
        _into("i7", "s7", "pan"),
        _yields("y7", "s7", "sofrito"),
    ]


def sound_writes() -> list[Op]:
    """The same recipe with every ingredient prepped before it is combined."""
    return [
        *_pantry(),
        Op.entity("PrepStep", "p1", {"step_index": 1, "prep_kind": "CHOP"}),
        Op.entity("PrepStep", "p2", {"step_index": 2, "prep_kind": "CHOP"}),
        Op.entity("PrepStep", "p3", {"step_index": 3, "prep_kind": "WASH"}),
        Op.entity("PrepStep", "p4", {"step_index": 4, "prep_kind": "MEASURE"}),
        Op.entity("CombineStep", "c1", {"step_index": 5}),
        Op.entity("CombineStep", "c2", {"step_index": 6}),
        Op.entity("CombineStep", "c3", {"step_index": 7}),
        Op.entity("CombineStep", "c4", {"step_index": 8}),
        Op.entity("CookStep", "k1", {"step_index": 9}),
        _uses("u1", "p1", "onion"),
        _uses("u2", "p2", "garlic"),
        _uses("u3", "p3", "tomato"),
        _uses("u4", "p4", "oil"),
        _uses("u5", "c1", "oil"),
        _uses("u6", "c2", "onion"),
        _uses("u7", "c3", "garlic"),
        _uses("u8", "c4", "tomato"),
        _into("i1", "c1", "pan"),
        _into("i2", "c2", "pan"),
        _into("i3", "c3", "pan"),
        _into("i4", "c4", "pan"),
        _into("i5", "k1", "pan"),
        _yields("y1", "k1", "sofrito"),
    ]


def main() -> None:
    report("toy 1, sketch graph (GEDANKEN table verbatim)", check(TOY, sketch_writes()))
    report("toy 1, sound graph (negative control)", check(TOY, sound_writes()))


if __name__ == "__main__":
    main()

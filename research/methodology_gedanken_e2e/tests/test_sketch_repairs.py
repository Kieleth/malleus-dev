"""The repairs the sketches needed, each shown as the refusal that forced it.

A repair recorded in prose is a claim. A repair recorded as the exact error the
library raises is evidence.
"""

from __future__ import annotations

import pytest

from malleus.ontology import OntologyError, OntologyRegistry

SKETCH_AS_WRITTEN = """
id: https://malleus.dev/schema/gedanken-kitchen-as-sketched
name: gedanken_kitchen_as_sketched
imports:
  - linkml:types
  - malleus
default_range: string
enums:
  PrepKind:
    permissible_values:
      CHOP:
  KitchenRelationType:
    permissible_values:
      USES:
classes:
  Ingredient:
    is_a: Entity
  PrepStep:
    is_a: Event
    slots:
      - step_index
      - prep_kind
    slot_usage:
      step_index:
        required: true
      prep_kind:
        required: true
  UsesRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: KitchenRelationType
        required: true
        equals_string: USES
      source_id:
        range: PrepStep
      target_id:
        range: Ingredient
slots:
  step_index:
    range: integer
  prep_kind:
    range: PrepKind
"""


def test_the_sketch_ontology_is_refused_at_load(tmp_path):
    """GEDANKEN.md:46-51 types the recipe steps as Events. The registry says no.

    This is the one repair every toy needed. It is not a write-time rejection
    that a caller could inspect and route around: `OntologyRegistry` refuses to
    construct at all, so the schema never reaches a KnowledgeGraph.
    src/malleus/ontology.py:718-722.
    """
    path = tmp_path / "sketch.yaml"
    path.write_text(SKETCH_AS_WRITTEN, encoding="utf-8")
    with pytest.raises(OntologyError) as error:
        OntologyRegistry(path)
    assert str(error.value) == (
        "Concrete relation 'UsesRelation' source_id range 'PrepStep' "
        "must be an Entity subtype"
    )


def test_demoting_the_step_to_an_entity_is_what_makes_it_load(tmp_path):
    """The minimal edit, and its cost: the kind discriminator goes flat."""
    path = tmp_path / "repaired.yaml"
    path.write_text(
        SKETCH_AS_WRITTEN.replace("PrepStep:\n    is_a: Event", "PrepStep:\n    is_a: Entity"),
        encoding="utf-8",
    )
    registry = OntologyRegistry(path)
    assert registry.is_subtype_of("PrepStep", "Entity")
    assert not registry.is_subtype_of("PrepStep", "Event")

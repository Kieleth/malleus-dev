"""RED contract for additive LinkML composition: one rule, one pure function.

A proposal is born a fragment. Core composes it onto the retained root itself,
so no proposer hands Core a compiled artifact and no proposer needs a compiler.
The composition is one rule with no options: the fragment may only add, the
base's own key order survives, and the same two inputs give the same bytes.

The compiled proof is the one that matters. A composed source is worth nothing
unless the contract it compiles to differs from the base's by exactly the
change kinds the fragment declared.
"""

from __future__ import annotations

import pytest
import yaml

import malleus.compiler as compiler
from malleus._contract_pipeline.revision import compile_contract_revision
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _generic_compilation,
)
from tests.contract_compiler.pareto.test_protocol_machine import _effective


BASE = b"""\
id: https://example.malleus.dev/pareto-history
name: pareto_history
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  test: https://example.malleus.dev/pareto-history/
imports:
  - linkml:types
  - malleus
enums:
  LinkKind:
    permissible_values:
      LINKS:
slots:
  label:
    range: string
classes:
  LeftObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  RightObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  ObjectLink:
    is_a: Relation
    slot_usage:
      relation_type:
        range: LinkKind
        required: true
        equals_string: LINKS
      source_id:
        range: LeftObject
        required: true
      target_id:
        range: RightObject
        required: true
"""

CLASS_FRAGMENT = b"""\
classes:
  CustomerObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
"""

MIXED_FRAGMENT = b"""\
slots:
  customer_reference:
    range: string
enums:
  LinkKind:
    permissible_values:
      SERVES:
classes:
  CustomerObject:
    is_a: Entity
    slots:
      - label
      - customer_reference
    slot_usage:
      label:
        required: true
"""


def _compose(base: bytes = BASE, fragment: bytes = CLASS_FRAGMENT) -> bytes:
    return compiler.compose_linkml_addition(base, fragment)


def _refusal(fragment: bytes, base: bytes = BASE):
    with pytest.raises(compiler.LinkMLAdditionRefusal) as caught:
        compiler.compose_linkml_addition(base, fragment)
    return caught.value.reason


def _change_kinds(composed: bytes) -> list[str]:
    """The change kinds a revision from the base to the composed source names."""

    current = _generic_compilation(BASE)
    target = _generic_compilation(composed)
    revision = compile_contract_revision(
        revision_id="revision:composition",
        base_ledger_head="GENESIS",
        base_ledger_event_count=0,
        base_acceptance_head="GENESIS",
        base_materialization_head="GENESIS",
        base_accepted_state_digest="sha256:" + "0" * 64,
        current_validated_contract_bytes=current.artifact.artifact_bytes,
        current_partial_contract_bytes=_effective(
            validated_fact_set_sha256=current.artifact.validated_fact_set_sha256
        ).canonical_bytes,
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=_effective(
            validated_fact_set_sha256=target.artifact.validated_fact_set_sha256
        ).canonical_bytes,
        reason="the composed source adds what the fragment declared",
        issued_at="2026-09-21T00:00:00Z",
    )
    return sorted(change.kind for change in revision.changes)


# --- the rule ----------------------------------------------------------------


def test_the_addition_keys_are_the_five_a_fragment_may_carry() -> None:
    assert compiler.LINKML_ADDITION_KEYS == (
        "classes",
        "enums",
        "imports",
        "prefixes",
        "slots",
    )


def test_composition_keeps_the_base_key_order_and_appends_the_addition() -> None:
    composed = _compose()

    data = yaml.safe_load(composed.decode("utf-8"))
    assert list(data) == list(yaml.safe_load(BASE.decode("utf-8")))
    assert list(data["classes"]) == [
        "LeftObject",
        "RightObject",
        "ObjectLink",
        "CustomerObject",
    ]
    assert data["classes"]["CustomerObject"]["is_a"] == "Entity"


def test_the_same_two_inputs_give_the_same_bytes_twice() -> None:
    assert _compose() == _compose()
    assert _compose(fragment=MIXED_FRAGMENT) == _compose(fragment=MIXED_FRAGMENT)


def test_the_composed_source_carries_no_anchor_and_no_alias() -> None:
    composed = _compose(fragment=MIXED_FRAGMENT)

    tokens = list(yaml.scan(composed.decode("utf-8"), Loader=yaml.SafeLoader))
    forbidden = (yaml.tokens.AnchorToken, yaml.tokens.AliasToken)
    assert not [token for token in tokens if isinstance(token, forbidden)]


def test_a_second_fragment_composes_onto_the_first_result() -> None:
    once = _compose()

    twice = compiler.compose_linkml_addition(
        once,
        b"slots:\n  customer_reference:\n    range: string\n",
    )

    data = yaml.safe_load(twice.decode("utf-8"))
    assert "CustomerObject" in data["classes"]
    assert list(data["slots"]) == ["label", "customer_reference"]


# --- the compiled proof ------------------------------------------------------


def test_a_class_fragment_compiles_to_exactly_one_added_class() -> None:
    assert _change_kinds(_compose()) == ["ADD_CLASS"]


def test_a_mixed_fragment_compiles_to_exactly_what_it_declared() -> None:
    kinds = _change_kinds(_compose(fragment=MIXED_FRAGMENT))

    assert kinds == ["ADD_CLASS", "ADD_ENUM_VALUE", "ADD_SLOT"]


def test_a_new_enum_is_an_addition() -> None:
    composed = _compose(
        fragment=b"enums:\n  ShipKind:\n    permissible_values:\n      SHIPS:\n"
    )

    data = yaml.safe_load(composed.decode("utf-8"))
    assert list(data["enums"]) == ["LinkKind", "ShipKind"]


def test_a_new_permissible_value_joins_an_existing_enum() -> None:
    composed = _compose(
        fragment=b"enums:\n  LinkKind:\n    permissible_values:\n      SERVES:\n"
    )

    data = yaml.safe_load(composed.decode("utf-8"))
    assert list(data["enums"]["LinkKind"]["permissible_values"]) == ["LINKS", "SERVES"]


def test_a_new_prefix_joins_the_prefix_map() -> None:
    composed = _compose(fragment=b"prefixes:\n  extra: https://example.org/extra/\n")

    data = yaml.safe_load(composed.decode("utf-8"))
    assert list(data["prefixes"])[-1] == "extra"


def test_a_new_import_joins_the_import_list() -> None:
    composed = _compose(fragment=b"imports:\n  - extra\n")

    data = yaml.safe_load(composed.decode("utf-8"))
    assert data["imports"] == ["linkml:types", "malleus", "extra"]


# --- the refusal matrix ------------------------------------------------------


def test_a_fragment_key_outside_the_five_refuses() -> None:
    assert (
        _refusal(b"default_range: integer\n")
        == compiler.LinkMLAdditionRefusalReason.UNSUPPORTED_FRAGMENT_KEY
    )
    assert (
        _refusal(b"types:\n  weird:\n    base: str\n")
        == compiler.LinkMLAdditionRefusalReason.UNSUPPORTED_FRAGMENT_KEY
    )


def test_an_existing_class_refuses() -> None:
    assert (
        _refusal(b"classes:\n  LeftObject:\n    is_a: Entity\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_CLASS
    )


def test_slot_usage_on_an_existing_class_refuses() -> None:
    assert (
        _refusal(
            b"classes:\n"
            b"  LeftObject:\n"
            b"    slot_usage:\n"
            b"      label:\n"
            b"        required: false\n"
        )
        == compiler.LinkMLAdditionRefusalReason.EXISTING_CLASS
    )


def test_an_existing_slot_refuses() -> None:
    assert (
        _refusal(b"slots:\n  label:\n    range: integer\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_SLOT
    )


def test_anything_but_a_permissible_value_on_an_existing_enum_refuses() -> None:
    assert (
        _refusal(b"enums:\n  LinkKind:\n    description: renamed\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_ENUM_FIELD
    )


def test_an_existing_permissible_value_refuses() -> None:
    assert (
        _refusal(b"enums:\n  LinkKind:\n    permissible_values:\n      LINKS:\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_PERMISSIBLE_VALUE
    )


def test_an_existing_import_refuses() -> None:
    assert (
        _refusal(b"imports:\n  - malleus\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_IMPORT
    )


def test_an_existing_prefix_refuses() -> None:
    assert (
        _refusal(b"prefixes:\n  malleus: https://example.org/other/\n")
        == compiler.LinkMLAdditionRefusalReason.EXISTING_PREFIX
    )


def test_a_fragment_that_is_not_a_mapping_refuses() -> None:
    assert (
        _refusal(b"- classes\n")
        == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    )
    assert (
        _refusal(b"") == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    )
    assert (
        _refusal(b"classes: {}\n")
        == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    )


def test_an_anchor_or_alias_refuses_in_either_input() -> None:
    aliased = (
        b"classes:\n"
        b"  CustomerObject: &base\n"
        b"    is_a: Entity\n"
        b"  OtherObject: *base\n"
    )
    assert _refusal(aliased) == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    assert (
        _refusal(CLASS_FRAGMENT, base=BASE + b"# trailing\n--- {}\n")
        == compiler.LinkMLAdditionRefusalReason.MALFORMED_BASE
    )


def test_a_duplicate_key_refuses() -> None:
    assert (
        _refusal(
            b"classes:\n"
            b"  CustomerObject:\n"
            b"    is_a: Entity\n"
            b"  CustomerObject:\n"
            b"    is_a: Entity\n"
        )
        == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    )


def test_input_that_is_not_exact_bytes_refuses() -> None:
    with pytest.raises(compiler.LinkMLAdditionRefusal) as caught:
        compiler.compose_linkml_addition(BASE.decode("utf-8"), CLASS_FRAGMENT)
    assert caught.value.reason == compiler.LinkMLAdditionRefusalReason.MALFORMED_BASE
    with pytest.raises(compiler.LinkMLAdditionRefusal) as caught:
        compiler.compose_linkml_addition(BASE, CLASS_FRAGMENT.decode("utf-8"))
    assert (
        caught.value.reason == compiler.LinkMLAdditionRefusalReason.MALFORMED_FRAGMENT
    )


def test_a_base_that_is_not_a_mapping_refuses() -> None:
    assert (
        _refusal(CLASS_FRAGMENT, base=b"- id\n")
        == compiler.LinkMLAdditionRefusalReason.MALFORMED_BASE
    )

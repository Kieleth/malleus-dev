"""The compiled view executes retained class conditions, not named domain rules."""

from copy import deepcopy
from importlib.resources import files
from pathlib import Path

import pytest
import yaml

import malleus.compiler as api


SOURCE = b"""id: https://example.org/alternatives
name: alternatives
imports: [linkml:types]
classes:
  Variant:
    slots: [kind, text, number]
    exactly_one_of:
      - slot_conditions:
          kind: {equals_string: TEXT}
          text: {required: true}
          number: {value_presence: ABSENT}
      - slot_conditions:
          kind: {equals_string: NUMBER}
          number: {value_presence: PRESENT}
          text: {value_presence: ABSENT}
  Tagged:
    mixin: true
    slots: [tag]
    exactly_one_of:
      - slot_conditions:
          tag: {equals_string: CHECKED}
  Child:
    is_a: Variant
    mixins: [Tagged]
    slots: [items]
    exactly_one_of:
      - slot_conditions:
          items: {required: true, equals_string: ok}
  Envelope:
    slots: [children]
  Overlap:
    slots: [text, number]
    exactly_one_of:
      - slot_conditions:
          text: {required: true}
      - slot_conditions:
          number: {required: true}
  Required:
    slots: [text]
    slot_usage:
      text: {required: true}
    exactly_one_of:
      - slot_conditions:
          text: {required: false}
slots:
  kind: {range: string}
  text: {range: string}
  number: {range: integer}
  tag: {range: string}
  items: {range: string, multivalued: true}
  children: {range: Child, inlined: true, multivalued: true}
"""


def _compile(source=SOURCE):
    return api.compile_linkml_contract(
        root_locator="fixture",
        sources={
            "fixture": source,
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


@pytest.fixture(scope="module")
def compiled():
    return _compile()


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"kind": "TEXT"},
        {"kind": "TEXT", "text": None},
        {"kind": "TEXT", "text": ""},
        {"kind": "TEXT", "text": "ok", "number": None},
        {"kind": "TEXT", "text": "ok", "number": 2},
        {"kind": "NUMBER"},
        {"kind": "NUMBER", "number": None},
        {"kind": "UNKNOWN", "number": 1},
    ],
)
def test_conditions_refuse_missing_equal_required_present_and_absent_fields(
    compiled, record
):
    before = deepcopy(record)
    errors = compiled.view.validate_instance("Variant", record)
    assert any("exactly one" in error and "matched 0" in error for error in errors)
    assert record == before


@pytest.mark.parametrize(
    "record", [{"kind": "TEXT", "text": "ok"}, {"kind": "NUMBER", "number": 0}]
)
def test_exclusive_alternatives_accept_each_branch_and_zero_is_present(
    compiled, record
):
    assert compiled.view.validate_instance("Variant", record) == []


@pytest.mark.parametrize("record,count", [({}, 0), ({"text": "ok", "number": 1}, 2)])
def test_exactly_one_refuses_zero_and_multiple_matching_alternatives(
    compiled, record, count
):
    errors = compiled.view.validate_instance("Overlap", record)
    assert any(f"matched {count}" in error for error in errors)


@pytest.mark.parametrize(
    "change",
    [{"kind": "OTHER"}, {"tag": "OTHER"}, {"items": []}, {"items": ["wrong"]}],
)
def test_parent_mixin_and_local_groups_all_apply_inside_inlined_records(
    compiled, change
):
    child = {"kind": "TEXT", "text": "ok", "tag": "CHECKED", "items": ["ok"]}
    assert compiled.view.validate_instance("Child", child) == []
    assert compiled.view.validate_instance("Envelope", {"children": [child]}) == []
    invalid = {**child, **change}
    assert compiled.view.validate_instance("Child", invalid)
    assert compiled.view.validate_instance("Envelope", {"children": [child, invalid]})


def test_condition_cannot_weaken_an_existing_required_slot(compiled):
    assert compiled.view.validate_instance("Required", {"text": "ok"}) == []
    assert compiled.view.validate_instance("Required", {})


def test_qualified_properties_and_source_free_reload_use_the_same_rules(
    compiled, monkeypatch
):
    def forbidden(*args, **kwargs):
        raise AssertionError("compiled validation consulted source machinery")

    from malleus import OntologyRegistry

    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(OntologyRegistry, "__init__", forbidden)
    view = api.load_validated_contract_artifact(compiled.artifact.artifact_bytes)
    prefix = "https://example.org/alternatives/"
    assert (
        view.validate_instance(
            prefix + "Variant", {prefix + "kind": "NUMBER", prefix + "number": 0}
        )
        == []
    )
    errors = view.validate_instance(prefix + "Variant", {prefix + "kind": "NUMBER"})
    assert errors and any("number" in error for error in errors)


def test_alternative_source_order_cannot_change_results_or_diagnostics(compiled):
    source = yaml.safe_load(SOURCE)
    source["classes"]["Variant"]["exactly_one_of"].reverse()
    reordered = _compile(yaml.safe_dump(source).encode())
    assert reordered.content_hash == compiled.content_hash
    for record in ({}, {"kind": "TEXT", "text": "ok"}, {"kind": "NUMBER"}):
        assert reordered.view.validate_instance(
            "Variant", record
        ) == compiled.view.validate_instance("Variant", record)

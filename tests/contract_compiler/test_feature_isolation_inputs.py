"""Fixed CC-013 feature-isolation input corpus."""

from __future__ import annotations

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from typing import Any


REPOSITORY = Path(__file__).resolve().parents[2]
INPUT_ROOT = (
    REPOSITORY
    / "conformance"
    / "contract_kernel"
    / "v0"
    / "feature_cases"
    / "inputs"
)
X01_CASES_PATH = (
    REPOSITORY
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "linkml_legacy_divergence"
    / "cases.json"
)
REQUIREMENTS_PATH = (
    REPOSITORY
    / "conformance"
    / "contract_kernel"
    / "v0"
    / "requirements"
    / "scenarios.json"
)

CASE_FILES = {
    "attribute-slot-usage": ("x01/attribute_slot_usage.json",),
    "conflicting-duplicate": (
        "duplicate_conflict/owner.json",
        "duplicate_conflict/redeclaration.json",
    ),
    "conflicting-mixins-order": (
        "x01/conflicting_mixins_ab.json",
        "x01/conflicting_mixins_ba.json",
    ),
    "default-range-equivalence": (
        "metamorphic/default_range_explicit.json",
        "x01/default_range.json",
    ),
    "explicit-adoption": (
        "explicit_adoption/adopter.json",
        "explicit_adoption/owner.json",
    ),
    "explicit-false-boundary": (
        "positive/valid_explicit_false.json",
        "x01/explicit_false.json",
    ),
    "numeric-bounds-lexemes": (
        "metamorphic/numeric_bounds_equivalent_lexemes.json",
        "x01/numeric_bounds.json",
    ),
    "parent-mixin-precedence": ("x01/parent_mixin_precedence.json",),
    "presentation-only-change": (
        "metamorphic/presentation_baseline.json",
        "metamorphic/presentation_changed.json",
    ),
    "repeated-mixin": ("x01/repeated_mixin.json",),
    "simple-parity": ("x01/simple_parity.json",),
}
CASE_REQUIREMENTS = {
    "attribute-slot-usage": ("linkml-profile-positive",),
    "conflicting-duplicate": ("linkml-profile-refusal",),
    "conflicting-mixins-order": (
        "linkml-profile-metamorphic",
        "linkml-profile-refusal",
    ),
    "default-range-equivalence": (
        "linkml-profile-metamorphic",
        "linkml-profile-positive",
    ),
    "explicit-adoption": ("linkml-profile-positive",),
    "explicit-false-boundary": (
        "linkml-profile-positive",
        "linkml-profile-refusal",
    ),
    "numeric-bounds-lexemes": (
        "linkml-profile-metamorphic",
        "linkml-profile-positive",
    ),
    "parent-mixin-precedence": ("linkml-profile-positive",),
    "presentation-only-change": ("linkml-profile-metamorphic",),
    "repeated-mixin": ("linkml-profile-refusal",),
    "simple-parity": ("linkml-profile-parity",),
}
X01_FILES = {
    "attribute_slot_usage": "x01/attribute_slot_usage.json",
    "conflicting_mixins_ab": "x01/conflicting_mixins_ab.json",
    "conflicting_mixins_ba": "x01/conflicting_mixins_ba.json",
    "default_range": "x01/default_range.json",
    "explicit_false": "x01/explicit_false.json",
    "numeric_bounds": "x01/numeric_bounds.json",
    "parent_mixin_precedence": "x01/parent_mixin_precedence.json",
    "repeated_mixin": "x01/repeated_mixin.json",
    "simple_parity": "x01/simple_parity.json",
}
FORBIDDEN_OUTPUT_KEYS = {
    "artifact",
    "diagnostic",
    "expected",
    "facts",
    "oracle",
    "outcome",
}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON number: {value}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
        parse_float=Decimal,
        parse_int=Decimal,
    )
    assert isinstance(value, dict)
    return value


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key for item in value.values() for key in _all_keys(item)
        }
    if isinstance(value, list):
        return {key for item in value for key in _all_keys(item)}
    return set()


def _without_presentation(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)

    def visit(item: Any) -> None:
        if isinstance(item, dict):
            item.pop("description", None)
            item.pop("title", None)
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)

    visit(result)
    return result


def test_fixed_case_and_file_inventory_is_complete_and_input_only() -> None:
    assert list(CASE_FILES) == sorted(CASE_FILES)
    assert len(CASE_FILES) == 11
    expected_files = {
        relative_path
        for paths in CASE_FILES.values()
        for relative_path in paths
    }
    assert len(expected_files) == 18
    assert len(expected_files) == sum(len(paths) for paths in CASE_FILES.values())

    actual_files = {
        path.relative_to(INPUT_ROOT).as_posix()
        for path in INPUT_ROOT.rglob("*")
        if path.is_file()
    }
    assert actual_files == expected_files
    assert all(
        path.is_file() and not path.is_symlink()
        for path in (INPUT_ROOT / item for item in actual_files)
    )
    assert all(tuple(paths) == tuple(sorted(paths)) for paths in CASE_FILES.values())


def test_retained_x01_sources_are_preserved_byte_for_byte() -> None:
    retained = _load_json(X01_CASES_PATH)
    retained_cases = {case["case_id"]: case for case in retained["cases"]}
    assert set(retained_cases) == set(X01_FILES)

    for case_id, relative_path in X01_FILES.items():
        case = retained_cases[case_id]
        source = (INPUT_ROOT / relative_path).read_bytes()
        assert source == case["source_text"].encode("utf-8")
        assert len(source) == case["source_byte_length"]
        assert "sha256:" + hashlib.sha256(source).hexdigest() == case["source_sha256"]


def test_cases_bind_only_existing_cc018_linkml_requirements() -> None:
    requirements = _load_json(REQUIREMENTS_PATH)
    requirement_scenarios = {
        requirement["requirement_id"]: scenario["scenario_id"]
        for scenario in requirements["scenarios"]
        for requirement in scenario["requirements"]
    }

    assert set(CASE_REQUIREMENTS) == set(CASE_FILES)
    assert all(
        references == tuple(sorted(set(references)))
        for references in CASE_REQUIREMENTS.values()
    )
    referenced = {
        requirement_id
        for references in CASE_REQUIREMENTS.values()
        for requirement_id in references
    }
    assert referenced == {
        "linkml-profile-metamorphic",
        "linkml-profile-parity",
        "linkml-profile-positive",
        "linkml-profile-refusal",
    }
    assert referenced <= set(requirement_scenarios)
    assert {
        requirement_scenarios[requirement_id] for requirement_id in referenced
    } == {"linkml-support-profile"}


def test_all_members_are_strict_source_objects_without_oracle_payloads() -> None:
    for paths in CASE_FILES.values():
        for relative_path in paths:
            document = _load_json(INPUT_ROOT / relative_path)
            assert isinstance(document.get("id"), str) and document["id"]
            assert isinstance(document.get("name"), str) and document["name"]
            assert not (_all_keys(document) & FORBIDDEN_OUTPUT_KEYS)


def test_metamorphic_inputs_change_only_the_named_source_dimension() -> None:
    numeric_path = INPUT_ROOT / "x01/numeric_bounds.json"
    numeric_lexeme_path = (
        INPUT_ROOT / "metamorphic/numeric_bounds_equivalent_lexemes.json"
    )
    numeric = _load_json(numeric_path)
    numeric_lexemes = _load_json(numeric_lexeme_path)
    assert numeric_lexemes == numeric
    assert numeric_lexeme_path.read_bytes() != numeric_path.read_bytes()
    numeric_lexeme_bytes = numeric_lexeme_path.read_bytes()
    for token in (b"0e0", b"5.0", b"1e1", b"9e1", b"9.5e1", b"1e2"):
        assert token in numeric_lexeme_bytes

    defaulted = _load_json(INPUT_ROOT / "x01/default_range.json")
    explicit = _load_json(INPUT_ROOT / "metamorphic/default_range_explicit.json")
    expected_explicit = copy.deepcopy(defaulted)
    expected_explicit["slots"]["value"]["range"] = "integer"
    assert explicit == expected_explicit

    presentation_baseline = _load_json(
        INPUT_ROOT / "metamorphic/presentation_baseline.json"
    )
    presentation_changed = _load_json(
        INPUT_ROOT / "metamorphic/presentation_changed.json"
    )
    assert presentation_baseline != presentation_changed
    assert _without_presentation(presentation_baseline) == _without_presentation(
        presentation_changed
    )


def test_explicit_adoption_and_conflicting_duplicate_are_isolated() -> None:
    owner = _load_json(INPUT_ROOT / "explicit_adoption/owner.json")
    adopter = _load_json(INPUT_ROOT / "explicit_adoption/adopter.json")
    owner_slot = owner["slots"]["shared_value"]
    adopter_slot = copy.deepcopy(adopter["slots"]["shared_value"])
    assert adopter["imports"] == [owner["id"]]
    assert adopter_slot.pop("annotations") == {"adopts": True}
    owner_slot = copy.deepcopy(owner_slot)
    owner_slot.pop("description")
    adopter_slot.pop("description")
    assert adopter_slot == owner_slot

    conflict_owner = _load_json(INPUT_ROOT / "duplicate_conflict/owner.json")
    redeclaration = _load_json(
        INPUT_ROOT / "duplicate_conflict/redeclaration.json"
    )
    assert redeclaration["imports"] == [conflict_owner["id"]]
    assert "annotations" not in redeclaration["slots"]["shared_value"]
    assert (
        redeclaration["slots"]["shared_value"]["range"]
        != conflict_owner["slots"]["shared_value"]["range"]
    )
    assert (
        redeclaration["slots"]["shared_value"]
        != conflict_owner["slots"]["shared_value"]
    )


def test_valid_explicit_false_stimulus_preserves_authored_booleans() -> None:
    document = _load_json(INPUT_ROOT / "positive/valid_explicit_false.json")
    expected = {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
    }
    global_slot = document["slots"]["value"]
    slot_use = document["classes"]["Record"]["slot_usage"]["value"]
    assert {key: global_slot[key] for key in expected} == expected
    assert slot_use == expected

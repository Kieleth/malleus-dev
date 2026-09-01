"""Fixed private answer-key checks for the feature-isolation corpus."""

from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Callable

import pytest


REPOSITORY = Path(__file__).resolve().parents[2]
INPUT_ROOT = (
    REPOSITORY / "conformance" / "contract_kernel" / "v0" / "feature_cases" / "inputs"
)
ORACLE_PATH = INPUT_ROOT.parent / "oracle" / "feature_cases.json"

CONFIGURATION = {
    "capabilities": "TEST_ONLY_CC014_REPOSITORY_FILE_NETWORK_DENIED_V0",
    "media_type": "TEST_ONLY_CC014_JSON_SOURCE_V0",
    "profile": "TEST_ONLY_CC014_LINKML_1_11_1_PROFILE_V0",
    "resolver": "TEST_ONLY_CC014_STRICT_RESOLVER_V0",
}
SOURCE_DESCRIPTORS = (
    (
        "duplicate_conflict/owner.json",
        142,
        "9a59cd18d040be262b729609405bf6ac4e04c83426be7788286afd17c6b2cd11",
    ),
    (
        "duplicate_conflict/redeclaration.json",
        210,
        "f6762a2754b75175e152b58492e61ce3f8ba54edf484cb9bff9fbb6cdd36744d",
    ),
    (
        "explicit_adoption/adopter.json",
        277,
        "1983347e771638c41dea08a1771bcea11cf155a552691393c1e816c588bf7232",
    ),
    (
        "explicit_adoption/owner.json",
        192,
        "b397043c3ab3b603ae59c3af4c68f9fe203af7fdd1eec891f3609a7dbe4801b5",
    ),
    (
        "metamorphic/default_range_explicit.json",
        177,
        "c4bd65697241cfa5f1e539ca204723c2c3feaf6bb5f216a1229b21287d588454",
    ),
    (
        "metamorphic/numeric_bounds_equivalent_lexemes.json",
        350,
        "7c96f5477ec81d6f300574e2874255f7f241b1362b695b8b75c4365216c66175",
    ),
    (
        "metamorphic/presentation_baseline.json",
        340,
        "9fab5e8553dddbc02b4816967d7a1d6d09452c26fe393aa561b6550e05239918",
    ),
    (
        "metamorphic/presentation_changed.json",
        336,
        "f8e59eb6eda21006ab1b95e55b41116376eb37f53db15556ad560488e2a79006",
    ),
    (
        "positive/valid_explicit_false.json",
        358,
        "1ebe5f0dc472c57ba8868aea8798fe8c870616e936617e6e452d899269d479ab",
    ),
    (
        "x01/attribute_slot_usage.json",
        301,
        "3bb785cb41ca321076fc9e345f72e98e66fd456864904b2b74170fbb78e90bbd",
    ),
    (
        "x01/conflicting_mixins_ab.json",
        345,
        "360a04667c2358ee9ea5a59ede7208fb1b8ddb5a97a3b5800cd24e4ae0fc71fc",
    ),
    (
        "x01/conflicting_mixins_ba.json",
        345,
        "f5abfc71242cd22e14ed8a83073c908c569690ce0cb50811d1d39ef72c4b81aa",
    ),
    (
        "x01/default_range.json",
        160,
        "114309aa47a174861e091d6ce4454f46a21982b9cdc01cb295d8bf26e4318866",
    ),
    (
        "x01/explicit_false.json",
        317,
        "b6067d9ed6d57d5c2d59324990ed151975c66f826d4596bb7fb6d8dca0bc7a8c",
    ),
    (
        "x01/numeric_bounds.json",
        341,
        "310927cfee843803cced8933ada89d678f3cef385c7a9393f8b882e6c6e0921b",
    ),
    (
        "x01/parent_mixin_precedence.json",
        378,
        "058dba6e97e138ccdf75f0ae928f289b261f6cd21f89f6f0f9ceb464032f0d37",
    ),
    (
        "x01/repeated_mixin.json",
        246,
        "0d39ee50aa8f475c1abdacbba395520014a5d95341734ee96b069598df6a3b1b",
    ),
    (
        "x01/simple_parity.json",
        166,
        "88b64ac3d7bff49d8a04d7b9b428aa1fddb57311ffdece661c5b01e1ef64efbe",
    ),
)


def _slot(
    range_: str,
    *,
    required: bool = False,
    multivalued: bool = False,
    identifier: bool = False,
    inlined: bool = False,
    minimum: str | None = None,
    maximum: str | None = None,
) -> dict[str, bool | str]:
    result: dict[str, bool | str] = {
        "identifier": identifier,
        "inlined": inlined,
        "multivalued": multivalued,
        "range": range_,
        "required": required,
    }
    if maximum is not None:
        result["maximum"] = maximum
    if minimum is not None:
        result["minimum"] = minimum
    return dict(sorted(result.items()))


def _class(
    *,
    is_a: str | None = None,
    mixins: tuple[str, ...] = (),
    is_mixin: bool = False,
) -> dict[str, Any]:
    result: dict[str, Any] = {"abstract": False, "is_mixin": is_mixin}
    if is_a is not None:
        result["is_a"] = is_a
    if mixins:
        result["mixins"] = list(mixins)
    return dict(sorted(result.items()))


STRING_OPTIONAL = _slot("string")
STRING_REQUIRED = _slot("string", required=True)
INTEGER_OPTIONAL = _slot("integer")
INTEGER_REQUIRED = _slot("integer", required=True)
FLOAT_OPTIONAL = _slot("float")
FLOAT_REQUIRED = _slot("float", required=True)

SIMPLE_PROJECTION = {
    "classes": {"Thing": _class()},
    "global_slots": {"value": STRING_REQUIRED},
    "slot_uses": {"Thing.value": STRING_REQUIRED},
}
DEFAULT_RANGE_PROJECTION = {
    "classes": {"Thing": _class()},
    "global_slots": {"value": INTEGER_OPTIONAL},
    "slot_uses": {"Thing.value": INTEGER_OPTIONAL},
}
PRESENTATION_PROJECTION = {
    "classes": {"Thing": _class()},
    "global_slots": {"value": STRING_REQUIRED},
    "slot_uses": {"Thing.value": STRING_REQUIRED},
}
EXPLICIT_FALSE_PROJECTION = {
    "classes": {"Record": _class()},
    "global_slots": {"value": STRING_OPTIONAL},
    "slot_uses": {"Record.value": STRING_OPTIONAL},
}
ADOPTION_PROJECTION = {
    "classes": {},
    "global_slots": {"shared_value": STRING_REQUIRED},
    "slot_uses": {},
    "slot_owners": {
        "shared_value": (
            "https://example.malleus.dev/cc013/adoption-owner/shared_value"
        )
    },
}
CONFLICT_OWNER_PROJECTION = {
    "classes": {},
    "global_slots": {"shared_value": STRING_REQUIRED},
    "slot_uses": {},
}
ATTRIBUTE_PROJECTION = {
    "classes": {"Thing": _class()},
    "global_slots": {"global_value": STRING_OPTIONAL},
    "local_slots": {"Thing.value": INTEGER_REQUIRED},
    "slot_uses": {
        "Thing.global_value": FLOAT_REQUIRED,
        "Thing.value": INTEGER_REQUIRED,
    },
}
PARENT_MIXIN_PROJECTION = {
    "classes": {
        "Child": _class(is_a="Parent", mixins=("MixinA",)),
        "MixinA": _class(is_mixin=True),
        "Parent": _class(),
    },
    "global_slots": {"value": STRING_OPTIONAL},
    "slot_uses": {
        "Child.value": _slot("float", required=True, multivalued=True),
        "MixinA.value": _slot("float", multivalued=True),
        "Parent.value": INTEGER_REQUIRED,
    },
}
NUMERIC_PROJECTION = {
    "classes": {"Child": _class(is_a="Parent"), "Parent": _class()},
    "global_slots": {"value": _slot("float", minimum="0", maximum="100")},
    "slot_uses": {
        "Child.value": _slot("float", minimum="10", maximum="90"),
        "Parent.value": _slot("float", minimum="10", maximum="90"),
    },
}

EXPECTED_SOURCES = [
    {
        "byte_length": Decimal(byte_length),
        "path": path,
        "source_blob": f"TEST_ONLY_CC014_SOURCE_BLOB_SHA256_{digest}",
    }
    for path, byte_length, digest in SOURCE_DESCRIPTORS
]
REFUSE = {"outcome": "REFUSE"}
EXPECTED_OUTCOMES = {
    "duplicate_conflict/owner.json": "ACCEPT",
    "duplicate_conflict/redeclaration.json": REFUSE,
    "explicit_adoption/adopter.json": "ACCEPT",
    "explicit_adoption/owner.json": "ACCEPT",
    "metamorphic/default_range_explicit.json": "ACCEPT",
    "metamorphic/numeric_bounds_equivalent_lexemes.json": "ACCEPT",
    "metamorphic/presentation_baseline.json": "ACCEPT",
    "metamorphic/presentation_changed.json": "ACCEPT",
    "positive/valid_explicit_false.json": "ACCEPT",
    "x01/attribute_slot_usage.json": "ACCEPT",
    "x01/conflicting_mixins_ab.json": REFUSE,
    "x01/conflicting_mixins_ba.json": REFUSE,
    "x01/default_range.json": "ACCEPT",
    "x01/explicit_false.json": REFUSE,
    "x01/numeric_bounds.json": "ACCEPT",
    "x01/parent_mixin_precedence.json": "ACCEPT",
    "x01/repeated_mixin.json": REFUSE,
    "x01/simple_parity.json": "ACCEPT",
}
EXPECTED_PROJECTIONS = {
    "duplicate_conflict/owner.json": CONFLICT_OWNER_PROJECTION,
    "explicit_adoption/adopter.json": ADOPTION_PROJECTION,
    "explicit_adoption/owner.json": ADOPTION_PROJECTION,
    "metamorphic/default_range_explicit.json": DEFAULT_RANGE_PROJECTION,
    "metamorphic/numeric_bounds_equivalent_lexemes.json": NUMERIC_PROJECTION,
    "metamorphic/presentation_baseline.json": PRESENTATION_PROJECTION,
    "metamorphic/presentation_changed.json": PRESENTATION_PROJECTION,
    "positive/valid_explicit_false.json": EXPLICIT_FALSE_PROJECTION,
    "x01/attribute_slot_usage.json": ATTRIBUTE_PROJECTION,
    "x01/default_range.json": DEFAULT_RANGE_PROJECTION,
    "x01/numeric_bounds.json": NUMERIC_PROJECTION,
    "x01/parent_mixin_precedence.json": PARENT_MIXIN_PROJECTION,
    "x01/simple_parity.json": SIMPLE_PROJECTION,
}


def _relation(
    case_id: str,
    left: str,
    right: str,
    *,
    outcome: str,
    facts: str,
    validated: str,
    contract: str,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "dimensions": {
            "compilation_outcome": outcome,
            "compiled_facts": facts,
            "effective_contract": contract,
            "logical_artifact": "NOT_CLAIMED",
            "raw_source": "DIFFERENT",
            "source_attestation": "DIFFERENT",
            "validated_fact_set": validated,
        },
        "left": left,
        "right": right,
    }


EXPECTED_RELATIONS = [
    _relation(
        "conflicting-mixins-order",
        "x01/conflicting_mixins_ab.json",
        "x01/conflicting_mixins_ba.json",
        outcome="SAME",
        facts="NOT_CLAIMED",
        validated="NOT_CLAIMED",
        contract="NOT_CLAIMED",
    ),
    _relation(
        "default-range-equivalence",
        "x01/default_range.json",
        "metamorphic/default_range_explicit.json",
        outcome="SAME",
        facts="SAME",
        validated="SAME",
        contract="SAME",
    ),
    _relation(
        "numeric-bounds-lexemes",
        "x01/numeric_bounds.json",
        "metamorphic/numeric_bounds_equivalent_lexemes.json",
        outcome="SAME",
        facts="SAME",
        validated="SAME",
        contract="SAME",
    ),
    _relation(
        "presentation-only-change",
        "metamorphic/presentation_baseline.json",
        "metamorphic/presentation_changed.json",
        outcome="SAME",
        facts="SAME",
        validated="SAME",
        contract="SAME",
    ),
]
EXPECTED_GROUPS = {
    "attribute-slot-usage": ["x01/attribute_slot_usage.json"],
    "conflicting-duplicate": [
        "duplicate_conflict/owner.json",
        "duplicate_conflict/redeclaration.json",
    ],
    "conflicting-mixins-order": [
        "x01/conflicting_mixins_ab.json",
        "x01/conflicting_mixins_ba.json",
    ],
    "default-range-equivalence": [
        "metamorphic/default_range_explicit.json",
        "x01/default_range.json",
    ],
    "explicit-adoption": [
        "explicit_adoption/adopter.json",
        "explicit_adoption/owner.json",
    ],
    "explicit-false-boundary": [
        "positive/valid_explicit_false.json",
        "x01/explicit_false.json",
    ],
    "numeric-bounds-lexemes": [
        "metamorphic/numeric_bounds_equivalent_lexemes.json",
        "x01/numeric_bounds.json",
    ],
    "parent-mixin-precedence": ["x01/parent_mixin_precedence.json"],
    "presentation-only-change": [
        "metamorphic/presentation_baseline.json",
        "metamorphic/presentation_changed.json",
    ],
    "repeated-mixin": ["x01/repeated_mixin.json"],
    "simple-parity": ["x01/simple_parity.json"],
}
EXPECTED_PROVENANCE = {
    "accepted_decisions": ["OD-002", "OD-003", "OD-005", "OD-008"],
    "adoption": {
        "adopter": "explicit_adoption/adopter.json",
        "authoritative_owner": "explicit_adoption/owner.json",
        "marker": "TEST_ONLY_CC014_AUTHORED_BOOLEAN_TRUE",
        "semantic_fact_emitted_for_marker": False,
    },
    "default_range": {
        "metamorphic/default_range_explicit.json": ("TEST_ONLY_CC014_AUTHORED_VALUE"),
        "x01/default_range.json": "TEST_ONLY_CC014_SCHEMA_DEFAULT_VALUE",
    },
    "derivation": "TEST_ONLY_CC014_HAND_AUTHORED_WITHOUT_IMPLEMENTATION_OUTPUT",
    "input_evidence": "CC-013",
    "numeric_lexemes": {
        "metamorphic/numeric_bounds_equivalent_lexemes.json": {
            "classes.Child.slot_usage.value.maximum_value": "9.5e1",
            "classes.Child.slot_usage.value.minimum_value": "5.0",
            "classes.Parent.slot_usage.value.maximum_value": "9e1",
            "classes.Parent.slot_usage.value.minimum_value": "1e1",
            "slots.value.maximum_value": "1e2",
            "slots.value.minimum_value": "0e0",
        },
        "x01/numeric_bounds.json": {
            "classes.Child.slot_usage.value.maximum_value": "95",
            "classes.Child.slot_usage.value.minimum_value": "5",
            "classes.Parent.slot_usage.value.maximum_value": "90",
            "classes.Parent.slot_usage.value.minimum_value": "10",
            "slots.value.maximum_value": "100",
            "slots.value.minimum_value": "0",
        },
    },
}
EXPECTED_NONCLAIMS = {
    "canonical_fact_bytes": "NOT_CLAIMED",
    "compiler_implementation_conformance": "NOT_CLAIMED",
    "diagnostic_identifiers": "NOT_CLAIMED",
    "effective_contract_identity": "NOT_CLAIMED",
    "logical_artifact_wire_format": "NOT_CLAIMED",
    "public_compatibility": "NOT_CLAIMED",
    "runtime_conformance": "NOT_CLAIMED",
}
EXPECTED_ORACLE = {
    "configuration": CONFIGURATION,
    "groups": EXPECTED_GROUPS,
    "nonclaims": EXPECTED_NONCLAIMS,
    "outcomes": EXPECTED_OUTCOMES,
    "projections": EXPECTED_PROJECTIONS,
    "provenance": EXPECTED_PROVENANCE,
    "relations": EXPECTED_RELATIONS,
    "sources": EXPECTED_SOURCES,
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


def _load_oracle() -> dict[str, Any]:
    return _load_json(ORACLE_PATH)


def _validate_oracle(value: dict[str, Any]) -> None:
    _assert_exact_json_types(EXPECTED_ORACLE, value)
    assert value == EXPECTED_ORACLE
    assert set(value) == {
        "configuration",
        "groups",
        "nonclaims",
        "outcomes",
        "projections",
        "provenance",
        "relations",
        "sources",
    }
    assert set(value["outcomes"]) == {item["path"] for item in value["sources"]}
    assert set(value["outcomes"]) == {
        path for paths in value["groups"].values() for path in paths
    }
    assert set(value["projections"]) == {
        path for path, outcome in value["outcomes"].items() if outcome == "ACCEPT"
    }
    assert all(
        outcome == "ACCEPT" or outcome == {"outcome": "REFUSE"}
        for outcome in value["outcomes"].values()
    )
    assert all(
        relation in {"SAME", "DIFFERENT", "NOT_CLAIMED"}
        for comparison in value["relations"]
        for relation in comparison["dimensions"].values()
    )


def _assert_exact_json_types(expected: Any, actual: Any) -> None:
    assert type(actual) is type(expected)
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for key, expected_value in expected.items():
            _assert_exact_json_types(expected_value, actual[key])
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for expected_value, actual_value in zip(expected, actual, strict=True):
            _assert_exact_json_types(expected_value, actual_value)
    elif isinstance(expected, Decimal):
        assert actual.as_tuple() == expected.as_tuple()
    else:
        assert actual == expected


def test_oracle_is_one_strict_private_member() -> None:
    actual = {
        path.relative_to(ORACLE_PATH.parent).as_posix()
        for path in ORACLE_PATH.parent.rglob("*")
        if path.is_file()
    }
    assert actual == {"feature_cases.json"}
    _validate_oracle(_load_oracle())


def test_source_descriptors_bind_exact_cc013_input_bytes() -> None:
    oracle = _load_oracle()
    assert oracle["sources"] == EXPECTED_SOURCES
    for path, byte_length, digest in SOURCE_DESCRIPTORS:
        source = (INPUT_ROOT / path).read_bytes()
        assert len(source) == byte_length
        assert sha256(source).hexdigest() == digest


def test_outcomes_are_exact_and_explicit_false_is_split() -> None:
    outcomes = _load_oracle()["outcomes"]
    assert outcomes == EXPECTED_OUTCOMES
    assert outcomes["positive/valid_explicit_false.json"] == "ACCEPT"
    assert outcomes["x01/explicit_false.json"] == {"outcome": "REFUSE"}
    assert all(
        result == "ACCEPT" or result == {"outcome": "REFUSE"}
        for result in outcomes.values()
    )


def test_accepted_feature_projections_are_exact_and_refusals_emit_none() -> None:
    oracle = _load_oracle()
    assert oracle["projections"] == EXPECTED_PROJECTIONS
    accepted = {
        path for path, outcome in oracle["outcomes"].items() if outcome == "ACCEPT"
    }
    refused = set(oracle["outcomes"]) - accepted
    assert set(oracle["projections"]) == accepted
    assert refused.isdisjoint(oracle["projections"])


def test_all_four_metamorphic_relations_are_exact() -> None:
    relations = _load_oracle()["relations"]
    assert relations == EXPECTED_RELATIONS
    assert [item["case_id"] for item in relations] == sorted(
        item["case_id"] for item in relations
    )
    assert {item["case_id"] for item in relations} == {
        "conflicting-mixins-order",
        "default-range-equivalence",
        "numeric-bounds-lexemes",
        "presentation-only-change",
    }


def test_all_eleven_input_groups_are_closed_without_invented_relations() -> None:
    oracle = _load_oracle()
    assert oracle["groups"] == EXPECTED_GROUPS
    assert list(oracle["groups"]) == sorted(oracle["groups"])
    assert len(oracle["groups"]) == 11
    compared = {relation["case_id"] for relation in oracle["relations"]}
    assert compared == {
        "conflicting-mixins-order",
        "default-range-equivalence",
        "numeric-bounds-lexemes",
        "presentation-only-change",
    }
    assert compared <= set(oracle["groups"])


def test_provenance_and_nonclaims_are_exact() -> None:
    oracle = _load_oracle()
    assert oracle["provenance"] == EXPECTED_PROVENANCE
    assert oracle["nonclaims"] == EXPECTED_NONCLAIMS
    assert set(oracle["nonclaims"].values()) == {"NOT_CLAIMED"}


def test_answer_key_has_no_forbidden_execution_dependency() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert not (
        imports
        & {
            "importlib",
            "linkml",
            "linkml_runtime",
            "malleus._contract_compiler",
            "malleus.registry",
            "runpy",
            "subprocess",
        }
    )
    forbidden_calls = {"__import__", "eval", "exec", "import_module", "importorskip"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
        elif isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_calls
    assert not any(
        isinstance(node, (ast.Assign, ast.AnnAssign))
        and any(
            isinstance(target, ast.Name) and target.id == "pytest_plugins"
            for target in (
                node.targets if isinstance(node, ast.Assign) else [node.target]
            )
        )
        for node in ast.walk(tree)
    )
    oracle_text = ORACLE_PATH.read_text(encoding="utf-8")
    assert "greenhouse" not in oracle_text.lower()
    assert "quiet_bell" not in oracle_text.lower()
    assert "Ontology" + "Registry" not in source


def _mutate_configuration(value: dict[str, Any]) -> None:
    value["configuration"]["resolver"] = "public-looking-resolver"


def _mutate_outcome(value: dict[str, Any]) -> None:
    value["outcomes"]["x01/repeated_mixin.json"] = "ACCEPT"


def _mutate_projection(value: dict[str, Any]) -> None:
    value["projections"]["x01/numeric_bounds.json"]["slot_uses"]["Child.value"][
        "maximum"
    ] = "95"


def _mutate_relation(value: dict[str, Any]) -> None:
    value["relations"][2]["dimensions"]["derivation_provenance"] = "SAME"


def _mutate_provenance(value: dict[str, Any]) -> None:
    value["provenance"]["accepted_decisions"].append("OD-999")


def _mutate_nonclaim(value: dict[str, Any]) -> None:
    value["nonclaims"]["public_compatibility"] = "SAME"


def _mutate_boolean_type(value: dict[str, Any]) -> None:
    value["provenance"]["adoption"]["semantic_fact_emitted_for_marker"] = Decimal(0)


def _mutate_integer_lexeme(value: dict[str, Any]) -> None:
    value["sources"][0]["byte_length"] = Decimal("142.0")


@pytest.mark.parametrize(
    "mutation",
    (
        _mutate_configuration,
        _mutate_outcome,
        _mutate_projection,
        _mutate_relation,
        _mutate_provenance,
        _mutate_nonclaim,
        _mutate_boolean_type,
        _mutate_integer_lexeme,
    ),
)
def test_corruption_controls_reject_each_semantic_section(
    mutation: Callable[[dict[str, Any]], None],
) -> None:
    corrupted = deepcopy(EXPECTED_ORACLE)
    mutation(corrupted)
    with pytest.raises(AssertionError):
        _validate_oracle(corrupted)

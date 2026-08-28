"""Fixed semantic scenario requirements derived from OD-005, OD-006, and OD-008."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator


REPOSITORY = Path(__file__).resolve().parents[2]
REQUIREMENTS_PATH = (
    REPOSITORY
    / "conformance"
    / "contract_kernel"
    / "v0"
    / "requirements"
    / "scenarios.json"
)
SCHEMA_PATH = (
    REPOSITORY / "conformance" / "contract_kernel" / "v0" / "corpus.schema.json"
)

EXPECTED_REQUIREMENTS = {
    "schema": "malleus.contract-kernel.scenarios/v0",
    "scenarios": [
        {
            "requirements": [
                {
                    "decision_anchors": ["OD-005"],
                    "kind": "POSITIVE",
                    "requirement_id": "atomic-fact-positive",
                    "statement": (
                        "A complete fact set over the closed Class, Slot, SlotUse, Enum, "
                        "and Scalar seed consists of exact three-member "
                        "subject-predicate-object records whose subjects and predicates "
                        "are full absolute identifiers and whose objects have the "
                        "predicate-declared type; it accepts atomically and canonicalizes "
                        "to one order-independent compact UTF-8 JSON array."
                    ),
                },
                {
                    "decision_anchors": ["OD-005"],
                    "kind": "REFUSAL",
                    "requirement_id": "atomic-fact-refusal",
                    "statement": (
                        "An unknown member, kind, or predicate, a wrong object or target "
                        "kind, an unresolved non-seed target, incomplete required structure, "
                        "a duplicate, a cardinality conflict, a contradiction, a declared "
                        "cycle, or a noncanonical value refuses the whole fact set without "
                        "accepting a subset."
                    ),
                },
            ],
            "scenario_id": "atomic-fact-contract",
        },
        {
            "requirements": [
                {
                    "decision_anchors": ["OD-006"],
                    "kind": "COMPOSITION_DELTA",
                    "requirement_id": "closed-composition-delta",
                    "statement": (
                        "A presentation-only or provenance-only change preserves all "
                        "role, composition, and epoch identities; a semantic change to "
                        "one role leaves the other two role identities unchanged, changes "
                        "that role identity and the composition, and starts a new "
                        "accepted-temporal epoch; a standalone governed-graph change "
                        "changes only its role and structural-state identity, with no "
                        "ledger epoch."
                    ),
                },
                {
                    "decision_anchors": ["OD-006"],
                    "kind": "POSITIVE",
                    "requirement_id": "closed-composition-positive",
                    "statement": (
                        "A full accepted-temporal contract contains exactly one complete "
                        "ProtocolRecordContract, GovernedGraphContract, and "
                        "GovernanceContract, with each role bound by the fixed v0 role "
                        "identity inputs and one composition binding exactly those roles. "
                        "A standalone structural graph instead binds exactly one "
                        "GovernedGraphContract and one structural-state identity, with no "
                        "protocol or governance role, composition, accepted-temporal "
                        "marker, or ledger."
                    ),
                },
                {
                    "decision_anchors": ["OD-006"],
                    "kind": "REFUSAL",
                    "requirement_id": "closed-composition-refusal",
                    "statement": (
                        "A missing, duplicate, extra, unknown, swapped, incomplete, ambient, "
                        "independently advanced, or mixed-composition role; a wrong role or "
                        "composition token, tag, version, or identity domain; equal payload "
                        "used interchangeably across roles; an inferred current or latest "
                        "role or composition; an unbound semantic replacement; role misuse; "
                        "accepted-temporal state bound only to the domain role; or "
                        "structural-only and full-composition confusion refuses the whole "
                        "composition without continuing the prior epoch."
                    ),
                },
            ],
            "scenario_id": "closed-contract-composition",
        },
        {
            "requirements": [
                {
                    "decision_anchors": ["OD-005", "OD-008"],
                    "kind": "METAMORPHIC",
                    "requirement_id": "linkml-profile-metamorphic",
                    "statement": (
                        "Reordering semantically unordered source members, declarations, "
                        "branches, conditions, or fact records preserves the semantic "
                        "facts and candidate identities. Equivalent explicit and defaulted "
                        "values preserve them while provenance differs, equivalent supported "
                        "numeric source lexemes converge to the same canonical decimal fact, "
                        "and changing only classified presentation fields preserves them "
                        "while source attestation changes."
                    ),
                },
                {
                    "decision_anchors": ["OD-005", "OD-008"],
                    "kind": "PARITY",
                    "requirement_id": "linkml-profile-parity",
                    "statement": (
                        "A supported LinkML source, its independently owned direct-fact "
                        "input, and its independent oracle yield identical "
                        "metamodel-valid atomic facts and exact canonical fact bytes."
                    ),
                },
                {
                    "decision_anchors": ["OD-008"],
                    "kind": "POSITIVE",
                    "requirement_id": "linkml-profile-positive",
                    "statement": (
                        "A source using only the closed exact-location LinkML v0 profile "
                        "maps enforced fields, exact defaults, authoritative symbols, and "
                        "the one flat exactly-one extension into the active atomic-fact "
                        "metamodel, preserves authored false, produces deterministic "
                        "effective SlotUse semantics, and retains provenance separately."
                    ),
                },
                {
                    "decision_anchors": ["OD-008"],
                    "kind": "REFUSAL",
                    "requirement_id": "linkml-profile-refusal",
                    "statement": (
                        "An unlisted or wrong-location field or annotation, malformed or "
                        "ambiguous declaration, unsupported builtin or expression, invalid "
                        "default or reference, or contradictory effective constraint "
                        "refuses the whole compilation; parser acceptance never expands "
                        "the profile."
                    ),
                },
            ],
            "scenario_id": "linkml-support-profile",
        },
    ],
}

FIXED_KINDS = {
    "COMPOSITION_DELTA",
    "METAMORPHIC",
    "PARITY",
    "POSITIVE",
    "REFUSAL",
}
FIXED_ANCHORS = {"OD-005", "OD-006", "OD-008"}
IDENTIFIER_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
)
ALLOWED_KEYS = {
    "decision_anchors",
    "kind",
    "requirement_id",
    "requirements",
    "scenario_id",
    "scenarios",
    "schema",
    "statement",
}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON number: {value}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
    )
    assert isinstance(value, dict)
    return value


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in _all_keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in _all_keys(item)}
    return set()


def _requirements(document: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        requirement
        for scenario in document["scenarios"]
        for requirement in scenario["requirements"]
    ]


def test_registry_matches_the_fixed_semantic_requirements() -> None:
    document = _load_json(REQUIREMENTS_PATH)
    schema = _load_json(SCHEMA_PATH)

    Draft202012Validator(schema).validate(document)
    assert document == EXPECTED_REQUIREMENTS


def test_registry_identities_and_anchors_are_stable_unique_and_sorted() -> None:
    document = _load_json(REQUIREMENTS_PATH)
    scenario_ids = [scenario["scenario_id"] for scenario in document["scenarios"]]
    requirements = _requirements(document)
    requirement_ids = [requirement["requirement_id"] for requirement in requirements]

    assert scenario_ids == sorted(scenario_ids)
    assert len(scenario_ids) == len(set(scenario_ids))
    assert len(requirement_ids) == len(set(requirement_ids))
    assert {
        anchor
        for requirement in requirements
        for anchor in requirement["decision_anchors"]
    } == FIXED_ANCHORS
    identifiers = [
        *scenario_ids,
        *requirement_ids,
        *(
            anchor
            for requirement in requirements
            for anchor in requirement["decision_anchors"]
        ),
    ]
    assert all(
        identifier
        and identifier.isascii()
        and all(character in IDENTIFIER_CHARACTERS for character in identifier)
        for identifier in identifiers
    )
    for scenario in document["scenarios"]:
        ids = [requirement["requirement_id"] for requirement in scenario["requirements"]]
        assert ids == sorted(ids)
    for requirement in requirements:
        anchors = requirement["decision_anchors"]
        assert anchors == sorted(anchors)
        assert len(anchors) == len(set(anchors))


def test_registry_covers_each_fixed_obligation_kind() -> None:
    assert {
        requirement["kind"]
        for requirement in _requirements(_load_json(REQUIREMENTS_PATH))
    } == FIXED_KINDS


def test_registry_contains_only_the_semantic_requirement_surface() -> None:
    document = _load_json(REQUIREMENTS_PATH)

    assert _all_keys(document) == ALLOWED_KEYS
    serialized = json.dumps(document, sort_keys=True)
    assert "Quiet Bell" not in serialized
    assert "themed_" not in serialized
    assert "source_path" not in serialized
    assert "expected_facts" not in serialized
    assert "expected_artifact" not in serialized
    assert "diagnostic_code" not in serialized
    assert "operation_trace" not in serialized


@pytest.mark.parametrize(
    ("source", "duplicate"),
    [
        ('{"schema":"first","schema":"second"}', "schema"),
        ('{"outer":{"kind":"first","kind":"second"}}', "kind"),
    ],
)
def test_loader_refuses_duplicate_root_and_nested_keys(
    tmp_path: Path, source: str, duplicate: str
) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError) as captured:
        _load_json(path)

    assert str(captured.value) == f"duplicate JSON key: {duplicate}"


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_loader_refuses_nonfinite_json_numbers(
    tmp_path: Path, constant: str
) -> None:
    path = tmp_path / "nonfinite.json"
    path.write_text(f'{{"value":{constant}}}', encoding="utf-8")

    with pytest.raises(ValueError) as captured:
        _load_json(path)

    assert str(captured.value) == f"nonfinite JSON number: {constant}"

"""Executable Greenhouse proof for the private LinkML compiler boundary."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from malleus._contract_compiler import ContractCompileError, compile_linkml_contract


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = (
    ROOT / "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse"
)
ORACLE = json.loads(
    (
        ROOT
        / "conformance/contract_kernel/v0/neutral_domain/oracle/greenhouse.json"
    ).read_text(encoding="utf-8")
)
IMPLEMENTATION = ROOT / "src/malleus/_contract_compiler.py"
PROFILE = ROOT / "src/malleus/_contract_compiler_profile.json"


def _expected_compilations() -> dict[str, dict[str, object]]:
    return {
        Path(compilation["source_path"]).name: compilation
        for compilation in ORACLE["compilations"]
    }


def _compile(name: str):
    path = SOURCE_ROOT / name
    return compile_linkml_contract(path.read_bytes(), locator=path.as_uri())


def _fact_dicts(result) -> tuple[dict[str, object], ...]:
    return tuple(fact.as_dict() for fact in result.facts)


def _fact_set(result) -> set[tuple[tuple[str, object], ...]]:
    return {tuple(sorted(fact.as_dict().items())) for fact in result.facts}


@pytest.mark.parametrize("name", sorted(_expected_compilations()))
def test_greenhouse_compiles_to_the_independent_answer_key(name: str) -> None:
    expected = _expected_compilations()[name]
    result = _compile(name)

    assert _fact_dicts(result) == tuple(ORACLE["baseline_facts"]) or name == "semantic-change.yaml"
    if name == "semantic-change.yaml":
        baseline = set(
            json.dumps(fact, sort_keys=True) for fact in ORACLE["baseline_facts"]
        )
        expected_facts = baseline.difference(
            json.dumps(fact, sort_keys=True)
            for fact in ORACLE["semantic_change"]["removed_facts"]
        ).union(
            json.dumps(fact, sort_keys=True)
            for fact in ORACLE["semantic_change"]["added_facts"]
        )
        assert _fact_dicts(result) == tuple(
            json.loads(fact) for fact in sorted(expected_facts)
        )

    assert len(result.facts) == expected["fact_count"]
    assert len(result.canonical_facts) == expected["canonical_fact_byte_length"]
    expected_digest = expected["canonical_facts_sha256"].removeprefix(
        "TEST_ONLY_CANONICAL_FACTS_SHA256_"
    )
    assert hashlib.sha256(result.canonical_facts).hexdigest() == expected_digest


def test_greenhouse_semantic_equivalence_and_real_delta_are_visible() -> None:
    baseline = _compile("baseline.yaml")

    for name in (
        "explicit-defaults.yaml",
        "numeric-equivalent.yaml",
        "presentation-only.yaml",
        "reordered.yaml",
    ):
        assert _compile(name).canonical_facts == baseline.canonical_facts

    changed = _compile("semantic-change.yaml")
    assert changed.canonical_facts != baseline.canonical_facts
    assert _fact_set(changed) - _fact_set(baseline) == {
        tuple(sorted(fact.items()))
        for fact in ORACLE["semantic_change"]["added_facts"]
    }
    assert _fact_set(baseline) - _fact_set(changed) == {
        tuple(sorted(fact.items()))
        for fact in ORACLE["semantic_change"]["removed_facts"]
    }


def test_unknown_root_field_refuses_the_whole_source() -> None:
    source = (SOURCE_ROOT / "baseline.yaml").read_bytes() + b"instances: {}\n"

    with pytest.raises(ContractCompileError, match="schema root.*instances"):
        compile_linkml_contract(source, locator="memory:unknown-root-field")


def test_compiler_is_bytes_in_and_does_not_import_the_legacy_registry() -> None:
    tree = ast.parse(IMPLEMENTATION.read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "malleus.ontology" not in imports
    assert "OntologyRegistry" not in imports


def test_compiler_policy_is_machine_readable_and_domain_neutral() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert profile["schema"] == "malleus.contract-compiler.linkml-profile/v0"
    assert profile["linkml_runtime_version"] == "1.11.1"
    assert set(profile) >= {
        "builtins",
        "defaults",
        "field_classification",
        "predicates",
        "structural_identities",
    }

    implementation = IMPLEMENTATION.read_text(encoding="utf-8")
    policy = PROFILE.read_text(encoding="utf-8")
    for fixture_literal in (
        "greenhouse",
        "Observation",
        "PlantState",
        "specimen_id",
        "temperature",
    ):
        assert fixture_literal not in implementation
        assert fixture_literal not in policy

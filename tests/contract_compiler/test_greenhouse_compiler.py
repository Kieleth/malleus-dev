"""Executable Greenhouse proof for the private LinkML compiler boundary."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tomllib
import zipfile

import pytest

import malleus
from malleus._contract_compiler import ContractCompileError, compile_linkml_contract


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse"
ORACLE = json.loads(
    (
        ROOT / "conformance/contract_kernel/v0/neutral_domain/oracle/greenhouse.json"
    ).read_text(encoding="utf-8")
)
IMPLEMENTATION = ROOT / "src/malleus/_contract_compiler.py"
PROFILE = ROOT / "src/malleus/_contract_compiler_profile.json"
MINIMAL_SOURCE = b"""\
id: https://example.org/minimal
name: minimal
imports:
  - linkml:types
default_range: string
"""


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

    assert (
        _fact_dicts(result) == tuple(ORACLE["baseline_facts"])
        or name == "semantic-change.yaml"
    )
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
        tuple(sorted(fact.items())) for fact in ORACLE["semantic_change"]["added_facts"]
    }
    assert _fact_set(baseline) - _fact_set(changed) == {
        tuple(sorted(fact.items()))
        for fact in ORACLE["semantic_change"]["removed_facts"]
    }


def test_result_attests_the_exact_caller_supplied_source() -> None:
    path = SOURCE_ROOT / "baseline.yaml"
    source = path.read_bytes()
    result = compile_linkml_contract(source, locator=path.as_uri())

    assert result.source.locator == path.as_uri()
    assert result.source.byte_length == len(source)
    assert result.source.sha256 == hashlib.sha256(source).hexdigest()
    assert result.facts_sha256 == hashlib.sha256(result.canonical_facts).hexdigest()
    assert result.implementation.linkml_runtime_version == "1.11.1"
    assert (
        result.implementation.support_profile
        == "malleus.linkml/greenhouse-bootstrap-v0"
    )
    assert (
        result.implementation.profile_sha256
        == hashlib.sha256(PROFILE.read_bytes()).hexdigest()
    )
    assert (
        result.implementation.executor_sha256
        == hashlib.sha256(IMPLEMENTATION.read_bytes()).hexdigest()
    )


def test_result_exposes_the_neutral_contract_before_fact_encoding() -> None:
    result = _compile("baseline.yaml")

    assert result.contract.declarations
    assert {declaration.kind for declaration in result.contract.declarations} >= {
        "https://malleus.dev/contract-facts/Class",
        "https://malleus.dev/contract-facts/Enum",
        "https://malleus.dev/contract-facts/Scalar",
        "https://malleus.dev/contract-facts/Slot",
    }
    assert {declaration.identifier for declaration in result.contract.declarations} == {
        fact.subject for fact in result.facts
    }


def test_unknown_root_field_refuses_the_whole_source() -> None:
    source = (SOURCE_ROOT / "baseline.yaml").read_bytes() + b"instances: {}\n"

    with pytest.raises(ContractCompileError, match="schema root.*instances"):
        compile_linkml_contract(source, locator="memory:unknown-root-field")


@pytest.mark.parametrize(
    "name,source",
    (
        (
            "duplicate-key",
            (SOURCE_ROOT / "baseline.yaml").read_bytes()
            + b"id: https://example.invalid/duplicate\n",
        ),
        (
            "quoted-number",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"maximum_value: 60", b'maximum_value: "60"'),
        ),
        (
            "yaml-only-boolean",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"identifier: true", b"identifier: TRUE"),
        ),
        (
            "unresolved-import",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"linkml:types", b"unresolved-module"),
        ),
    ),
)
def test_raw_profile_refuses_before_linkml_coercion(name: str, source: bytes) -> None:
    with pytest.raises(ContractCompileError):
        compile_linkml_contract(source, locator=f"memory:{name}")


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
        "lowering_plan",
        "node_shapes",
        "predicates",
        "range_resolution",
        "structural_identities",
        "symbol_policy",
    }

    implementation = IMPLEMENTATION.read_text(encoding="utf-8")
    semantic_policy = deepcopy(profile)
    semantic_policy["support_profile"] = ""
    policy = json.dumps(semantic_policy, ensure_ascii=False, sort_keys=True)
    for fixture_literal in (
        "greenhouse",
        "Observation",
        "PlantState",
        "specimen_id",
        "temperature",
    ):
        assert fixture_literal not in implementation
        assert fixture_literal not in policy


def test_profile_classifications_and_defaults_are_executed() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    annotation_profile = deepcopy(profile)
    annotation_profile["node_shapes"]["class"]["fields"]["abstract"] = {
        "classification": "ANNOTATION_ONLY",
        "parser": "boolean",
    }
    identity_profile = deepcopy(profile)
    identity_profile["node_shapes"]["slot"]["fields"]["maximum_value"][
        "classification"
    ] = "IDENTITY_ONLY"
    default_profile = deepcopy(profile)
    default_profile["defaults"]["class"]["abstract"] = True

    ordinary = _compile("baseline.yaml")
    without_abstract = compile_linkml_contract(
        (SOURCE_ROOT / "baseline.yaml").read_bytes(),
        locator="memory:annotation-profile",
        profile=annotation_profile,
    )
    abstract_by_default = compile_linkml_contract(
        (SOURCE_ROOT / "baseline.yaml").read_bytes(),
        locator="memory:default-profile",
        profile=default_profile,
    )
    assert without_abstract.canonical_facts != ordinary.canonical_facts
    assert not any(
        fact.predicate.endswith("/abstract") for fact in without_abstract.facts
    )
    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:identity-profile",
            profile=identity_profile,
        )
    assert (
        without_abstract.implementation.profile_sha256
        == hashlib.sha256(
            json.dumps(
                annotation_profile,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
    )
    assert abstract_by_default.canonical_facts != ordinary.canonical_facts
    assert any(
        fact.predicate.endswith("/abstract") and fact.object is True
        for fact in abstract_by_default.facts
    )


def test_non_enforced_rule_operand_refuses_the_profile() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["node_shapes"]["slot"]["fields"]["required"]["classification"] = (
        "ANNOTATION_ONLY"
    )

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:non-enforced-rule-operand",
            profile=profile,
        )


def test_non_enforced_field_refuses_stale_fact_policy() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["node_shapes"]["class"]["fields"]["abstract"]["classification"] = (
        "ANNOTATION_ONLY"
    )

    with pytest.raises(ContractCompileError, match="predicate is unread"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:non-enforced-default",
            profile=profile,
        )


def test_condition_range_rule_reads_its_profile_operands() -> None:
    source = (
        (SOURCE_ROOT / "baseline.yaml")
        .read_bytes()
        .replace(b"    range: PlantState\n", b"    range: float\n")
    )
    with pytest.raises(ContractCompileError, match="string or enum range"):
        compile_linkml_contract(source, locator="memory:string-condition-on-float")

    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["lowering_plan"][-1]["string_builtin"] = "float"
    result = compile_linkml_contract(
        source,
        locator="memory:profile-selected-condition-range",
        profile=profile,
    )

    assert result.facts


def test_derived_predicates_are_lowering_operands() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["lowering_plan"][-2]["on_class_predicate"] = "subclass_of"

    result = compile_linkml_contract(
        (SOURCE_ROOT / "baseline.yaml").read_bytes(),
        locator="memory:profile-selected-derived-predicate",
        profile=profile,
    )

    assert result.canonical_facts != _compile("baseline.yaml").canonical_facts
    assert not any(
        fact.predicate.endswith("/onClass")
        and fact.subject.startswith("urn:malleus:contract-structure:slot-use:")
        for fact in result.facts
    )


@pytest.mark.parametrize(
    "name,source",
    (
        (
            "prefixes",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"name: greenhouse\n",
                b"name: greenhouse\nprefixes:\n  ex: https://example.invalid/\n",
            ),
        ),
        (
            "adoption",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"    identifier: true\n",
                b"    identifier: true\n    annotations:\n      adopts: true\n",
            ),
        ),
        (
            "slot-usage",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"    slots:\n      - specimen_id\n",
                b"    slot_usage:\n      temperature:\n        required: true\n"
                b"    slots:\n      - specimen_id\n",
            ),
        ),
        (
            "class-valued-range",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"    range: PlantState\n", b"    range: Sample\n"),
        ),
        (
            "scalar-cycle",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"    typeof: float\n", b"    typeof: Celsius\n"),
        ),
        (
            "scalar-inlined",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"    identifier: true\n",
                b"    identifier: true\n    inlined: true\n",
            ),
        ),
        (
            "unsupported-builtin-range",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(b"    range: PlantState\n", b"    range: date\n"),
        ),
        (
            "slot-level-constraint",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"    range: PlantState\n",
                b"    range: PlantState\n    equals_string: HEALTHY\n",
            ),
        ),
        (
            "condition-required",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"            equals_string: HEALTHY\n",
                b"            required: true\n",
            ),
        ),
        (
            "compound-condition",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"            equals_string: HEALTHY\n",
                b"            equals_string: HEALTHY\n"
                b"            value_presence: PRESENT\n",
            ),
        ),
        (
            "two-conditions",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"          state:\n            equals_string: HEALTHY\n",
                b"          state:\n            equals_string: HEALTHY\n"
                b"          temperature:\n            value_presence: PRESENT\n",
            ),
        ),
        (
            "namespace-collision",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"classes:\n  Sample:\n",
                b"classes:\n  state:\n"
                b"    description: Collides with the global state slot.\n"
                b"  Sample:\n",
            ),
        ),
        (
            "inherited-slot",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"  Sample:\n    description: A greenhouse sample.\n",
                b"  Sample:\n    description: A greenhouse sample.\n"
                b"    slots:\n      - specimen_id\n",
            ),
        ),
        (
            "multiple-mixins",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"  Observation:\n",
                b"  Auditable:\n    mixin: true\n  Observation:\n",
            )
            .replace(
                b"    mixins:\n      - Traceable\n",
                b"    mixins:\n      - Traceable\n      - Auditable\n",
            ),
        ),
        (
            "semantic-parent",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"  Sample:\n    description: A greenhouse sample.\n",
                b"  Sample:\n    description: A greenhouse sample.\n"
                b"    mixins:\n      - Traceable\n",
            ),
        ),
        (
            "derived-mixin",
            (SOURCE_ROOT / "baseline.yaml")
            .read_bytes()
            .replace(
                b"    mixin: true\n",
                b"    mixin: true\n    is_a: Sample\n",
            ),
        ),
    ),
)
def test_greenhouse_bootstrap_refuses_unproved_linkml_branches(
    name: str, source: bytes
) -> None:
    with pytest.raises(ContractCompileError):
        compile_linkml_contract(source, locator=f"memory:{name}")


def test_profile_rejects_unknown_interpreter_operations() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["node_shapes"]["slot"]["fields"]["maximum_value"]["classification"] = (
        "MAGIC"
    )

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:unknown-profile-operation",
            profile=profile,
        )


@pytest.mark.parametrize(
    "shape,field",
    (
        ("schema", "id"),
        ("type", "typeof"),
        ("enum", "permissible_values"),
        ("class", "slots"),
        ("class", "attributes"),
        ("class", "exactly_one_of"),
    ),
)
def test_classification_controls_structural_lowering(shape: str, field: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["node_shapes"][shape]["fields"][field]["classification"] = "ANNOTATION_ONLY"
    baseline = _compile("baseline.yaml").canonical_facts

    try:
        result = compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator=f"memory:annotation-{shape}-{field}",
            profile=profile,
        )
    except ContractCompileError:
        return
    assert result.canonical_facts != baseline


@pytest.mark.parametrize("location", ("root", "field"))
def test_profile_refuses_unread_policy_members(location: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if location == "root":
        profile["unread_policy"] = True
    else:
        profile["node_shapes"]["slot"]["fields"]["maximum_value"]["unread_policy"] = (
            True
        )

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator=f"memory:unread-profile-{location}",
            profile=profile,
        )


@pytest.mark.parametrize(
    "path,value",
    (
        (("defaults", "slot", "required"), float("nan")),
        (("defaults", "slot", "required"), "false"),
        (("predicates", "type"), []),
        (("kinds", "class"), []),
        (("builtins", "float"), 3),
        (("adapter",), "java"),
        (("canonicalization",), "unknown"),
        (("node_shapes", "class", "fields", "mixins", "max_items"), -1),
    ),
)
def test_profile_refuses_invalid_semantic_values(
    path: tuple[str, ...], value: object
) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    target = profile
    for member in path[:-1]:
        target = target[member]
    target[path[-1]] = value

    expected = _compile("baseline.yaml").canonical_facts
    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:invalid-profile-value",
            profile=profile,
        )
    assert _compile("baseline.yaml").canonical_facts == expected


@pytest.mark.parametrize("record", ("rule", "constraint", "identity", "lowering"))
def test_profile_refuses_incomplete_operation_records(record: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if record == "rule":
        profile["node_shapes"]["slot"]["rules"][0].pop("then_field")
    elif record == "constraint":
        profile["node_shapes"]["slot"]["constraints"][1].pop("range")
    elif record == "identity":
        profile["structural_identities"]["slot_use"]["member_roles"] = {
            "class": "class"
        }
    else:
        profile["lowering_plan"][0]["op"] = "unknown"

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator=f"memory:invalid-profile-{record}",
            profile=profile,
        )


@pytest.mark.parametrize(
    "case",
    (
        "annotation-mapping-parser",
        "missing-declaration-kind",
        "non-enforced-scalar-operand",
        "non-enforced-enum-operand",
        "wrong-identity-roles",
        "unread-field-member",
        "unread-shape-identity",
        "unread-shape-kind",
        "unread-shape-constraint",
        "unread-direct-default",
        "unconsumed-enforced-field",
        "identity-outside-schema",
        "condition-member-slot-alias",
        "condition-member-duplicate",
        "condition-cardinality-gap",
        "incompatible-schema-default",
        "decimal-default",
        "ordered-bounds-typed-operands",
        "namespace-noncollection",
        "enum-value-body-policy",
        "collection-predicate",
        "foreign-enum-values-predicate",
        "resolver-parser-mismatch",
    ),
)
def test_profile_grammar_is_closed_before_source_coverage(case: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if case == "annotation-mapping-parser":
        profile["node_shapes"]["schema"]["fields"]["prefixes"]["classification"] = (
            "ANNOTATION_ONLY"
        )
    elif case == "missing-declaration-kind":
        profile["node_shapes"]["type"].pop("kind")
    elif case == "non-enforced-scalar-operand":
        profile["node_shapes"]["type"]["fields"]["typeof"] = {
            "classification": "ANNOTATION_ONLY",
            "parser": "nonempty_string",
        }
    elif case == "non-enforced-enum-operand":
        profile["node_shapes"]["enum"]["fields"]["permissible_values"] = {
            "classification": "ANNOTATION_ONLY",
            "item_shape": "permissible_value",
            "parser": "enum_values",
        }
    elif case == "wrong-identity-roles":
        profile["structural_identities"]["alternative_semantics"]["member_roles"] = {
            "bogus": "bogus"
        }
    elif case == "unread-field-member":
        profile["node_shapes"]["slot"]["fields"]["maximum_value"]["member"] = "maximum"
    elif case == "unread-shape-identity":
        profile["node_shapes"]["class"]["use_identity"] = "slot_use"
    elif case == "unread-shape-kind":
        profile["node_shapes"]["schema"]["kind"] = "class"
    elif case == "unread-shape-constraint":
        profile["node_shapes"]["schema"]["constraints"] = [
            {
                "field": "default_range",
                "op": "equals",
                "value": "string",
            }
        ]
    elif case == "unread-direct-default":
        profile["node_shapes"]["type"]["fields"]["typeof"]["default"] = "slot.range"
    elif case == "unconsumed-enforced-field":
        profile["node_shapes"]["schema"]["fields"]["name"]["classification"] = (
            "ENFORCED"
        )
    elif case == "identity-outside-schema":
        profile["node_shapes"]["class"]["fields"]["description"] = {
            "classification": "IDENTITY_ONLY",
            "identity_role": "module",
            "parser": "module_iri",
            "required": True,
        }
    elif case == "condition-member-slot-alias":
        profile["node_shapes"]["condition"]["fields"]["equals_string"]["member"] = (
            "slot"
        )
    elif case == "condition-member-duplicate":
        profile["node_shapes"]["condition"]["fields"]["value_presence"]["member"] = (
            "equalsString"
        )
    elif case == "condition-cardinality-gap":
        profile["node_shapes"]["alternative"]["fields"]["slot_conditions"][
            "max_items"
        ] = 2
    elif case == "incompatible-schema-default":
        profile["node_shapes"]["slot"]["fields"]["required"]["schema_default"] = (
            "default_range"
        )
    elif case == "decimal-default":
        profile["node_shapes"]["slot"]["fields"]["minimum_value"]["default"] = (
            "slot.range"
        )
    elif case == "ordered-bounds-typed-operands":
        bounds = profile["node_shapes"]["slot"]["constraints"][1]
        bounds["minimum"] = "required"
        bounds["maximum"] = "multivalued"
        bounds["allowed_builtin_ranges"] = ["float", "string"]
    elif case == "namespace-noncollection":
        profile["lowering_plan"][1]["collections"] = ["name"]
    elif case == "enum-value-body-policy":
        profile["node_shapes"]["enum"]["fields"]["permissible_values"]["item_shape"] = (
            "condition"
        )
    elif case == "collection-predicate":
        profile["node_shapes"]["class"]["fields"]["exactly_one_of"]["predicate"] = (
            "enum_value"
        )
    elif case == "foreign-enum-values-predicate":
        profile["node_shapes"]["slot"]["fields"]["annotations"] = {
            "classification": "ENFORCED",
            "item_shape": "permissible_value",
            "parser": "enum_values",
            "predicate": "enum_value",
        }
    else:
        profile["node_shapes"]["slot"]["fields"]["required"]["resolver"] = "mixin_list"

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            MINIMAL_SOURCE,
            locator=f"memory:closed-profile-{case}",
            profile=profile,
        )


@pytest.mark.parametrize(
    "case",
    (
        "invalid-term",
        "term-collision",
        "relative-structural-prefix",
        "invalid-module-role",
        "non-boolean-rule",
        "builtin-kind-collision",
        "field-predicate-alias",
        "derived-predicate-alias",
        "derived-kind-alias",
        "unsupported-symbol-separator",
    ),
)
def test_profile_cannot_emit_malformed_or_collapsed_facts(case: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if case == "invalid-term":
        profile["predicates"]["maximum_value"]["value"] = "bad predicate"
    elif case == "term-collision":
        profile["predicates"]["maximum_value"] = deepcopy(
            profile["predicates"]["minimum_value"]
        )
    elif case == "relative-structural-prefix":
        profile["structural_identities"]["slot_use"]["prefix"] = "relative-"
    elif case == "invalid-module-role":
        module = profile["node_shapes"]["schema"]["fields"]["id"]
        module.pop("identity_role")
        module["classification"] = "ANNOTATION_ONLY"
        name = profile["node_shapes"]["schema"]["fields"]["name"]
        name["classification"] = "IDENTITY_ONLY"
        name["identity_role"] = "module"
    elif case == "non-boolean-rule":
        rule = profile["node_shapes"]["slot"]["rules"][0]
        rule["then_field"] = "range"
        rule["then_value"] = "float"
    elif case == "builtin-kind-collision":
        profile["builtins"]["float"] = deepcopy(profile["kinds"]["class"])
    elif case == "field-predicate-alias":
        profile["node_shapes"]["slot"]["fields"]["maximum_value"]["predicate"] = (
            "minimum_value"
        )
    elif case == "derived-predicate-alias":
        profile["lowering_plan"][-2]["uses_slot_predicate"] = "on_class"
    elif case == "derived-kind-alias":
        profile["lowering_plan"][-1]["alternative_kind"] = "exactly_one_group"
    else:
        profile["symbol_policy"]["separator"] = "#"

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            MINIMAL_SOURCE,
            locator=f"memory:safe-profile-{case}",
            profile=profile,
        )


def test_generated_subject_cannot_alias_a_semantic_resource() -> None:
    baseline = _compile("baseline.yaml")
    generated = next(
        declaration.identifier
        for declaration in baseline.contract.declarations
        if declaration.identifier.startswith(
            "urn:malleus:contract-structure:slot-use:v0:sha256:"
        )
    )
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["kinds"]["class"] = {"form": "ABSOLUTE", "value": generated}

    with pytest.raises(ContractCompileError, match="aliases semantic resource"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:generated-resource-alias",
            profile=profile,
        )


def test_absolute_urn_predicate_is_not_rewritten_as_a_local_term() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["predicates"]["required"] = {
        "form": "ABSOLUTE",
        "value": "urn:example:required",
    }

    result = compile_linkml_contract(
        (SOURCE_ROOT / "explicit-defaults.yaml").read_bytes(),
        locator="memory:absolute-urn-predicate",
        profile=profile,
    )

    assert any(fact.predicate == "urn:example:required" for fact in result.facts)
    assert not any(
        fact.predicate.endswith("/urn:example:required") for fact in result.facts
    )


def test_bootstrap_is_private_and_excluded_from_the_distribution(
    tmp_path: Path,
) -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    excluded = project["tool"]["hatch"]["build"]["exclude"]

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--sdist",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(tmp_path),
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    wheels = tuple(tmp_path.glob("*.whl"))
    sdists = tuple(tmp_path.glob("*.tar.gz"))
    assert len(wheels) == 1
    assert len(sdists) == 1
    with zipfile.ZipFile(wheels[0]) as archive:
        members = set(archive.namelist())
    with tarfile.open(sdists[0], mode="r:gz") as archive:
        source_members = set(archive.getnames())

    assert "/src/malleus/_contract_compiler.py" in excluded
    assert "/src/malleus/_contract_compiler_profile.json" in excluded
    assert "malleus/_contract_compiler.py" not in members
    assert "malleus/_contract_compiler_profile.json" not in members
    assert not any(
        member.endswith("/src/malleus/_contract_compiler.py")
        or member.endswith("/src/malleus/_contract_compiler_profile.json")
        for member in source_members
    )
    assert "compile_linkml_contract" not in malleus.__all__

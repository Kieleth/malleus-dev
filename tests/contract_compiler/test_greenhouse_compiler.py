"""Executable Greenhouse proof for the private LinkML compiler boundary."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
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
        "structural_identities",
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
    annotation_profile["node_shapes"]["slot"]["fields"]["maximum_value"][
        "classification"
    ] = "ANNOTATION_ONLY"
    identity_profile = deepcopy(profile)
    identity_profile["node_shapes"]["slot"]["fields"]["maximum_value"][
        "classification"
    ] = "IDENTITY_ONLY"
    default_profile = deepcopy(profile)
    default_profile["defaults"]["class"]["abstract"] = True

    ordinary = _compile("baseline.yaml")
    without_maximum = compile_linkml_contract(
        (SOURCE_ROOT / "baseline.yaml").read_bytes(),
        locator="memory:annotation-profile",
        profile=annotation_profile,
    )
    abstract_by_default = compile_linkml_contract(
        (SOURCE_ROOT / "baseline.yaml").read_bytes(),
        locator="memory:default-profile",
        profile=default_profile,
    )
    assert without_maximum.canonical_facts != ordinary.canonical_facts
    assert not any(
        fact.predicate.endswith("/maximum") for fact in without_maximum.facts
    )
    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator="memory:identity-profile",
            profile=identity_profile,
        )
    assert (
        without_maximum.implementation.profile_sha256
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
        profile["structural_identities"]["slot_use"]["members"] = ["class"]
    else:
        profile["lowering_plan"][0]["op"] = "unknown"

    with pytest.raises(ContractCompileError, match="profile"):
        compile_linkml_contract(
            (SOURCE_ROOT / "baseline.yaml").read_bytes(),
            locator=f"memory:invalid-profile-{record}",
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
    assert len(wheels) == 1
    with zipfile.ZipFile(wheels[0]) as archive:
        members = set(archive.namelist())

    assert "/src/malleus/_contract_compiler.py" in excluded
    assert "/src/malleus/_contract_compiler_profile.json" in excluded
    assert "malleus/_contract_compiler.py" not in members
    assert "malleus/_contract_compiler_profile.json" not in members
    assert "compile_linkml_contract" not in malleus.__all__

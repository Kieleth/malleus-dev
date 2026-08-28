from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
KERNEL = ROOT / "conformance" / "contract_kernel" / "v0"
SOURCES = KERNEL / "neutral_domain" / "sources"
OPERATIONS = KERNEL / "neutral_domain" / "traces" / "input"
REQUIREMENTS = KERNEL / "requirements" / "scenarios.json"

SOURCE_NAMES = (
    "greenhouse/baseline.yaml",
    "greenhouse/explicit-defaults.yaml",
    "greenhouse/numeric-equivalent.yaml",
    "greenhouse/presentation-only.yaml",
    "greenhouse/reordered.yaml",
    "greenhouse/semantic-change.yaml",
)
OPERATION_CASES = {
    "closed-composition-semantic-change/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "closed-composition-delta",
        "scenario_id": "closed-contract-composition",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "semantic-change.yaml"
        ),
    },
    "linkml-profile-baseline/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-positive",
        "scenario_id": "linkml-support-profile",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "baseline.yaml"
        ),
    },
    "linkml-profile-explicit-defaults/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "explicit-defaults.yaml"
        ),
    },
    "linkml-profile-numeric-equivalent/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "numeric-equivalent.yaml"
        ),
    },
    "linkml-profile-presentation-only/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "presentation-only.yaml"
        ),
    },
    "linkml-profile-reordered/operation.json": {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": (
            "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/"
            "reordered.yaml"
        ),
    },
}

FORBIDDEN_RESULT_KEYS = {
    "decision",
    "diagnostic",
    "digest",
    "expected",
    "expected_artifact",
    "expected_facts",
    "facts",
    "outcome",
    "result",
    "state_digest",
}


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[str, Any]:
    keys: set[Any] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key == "<<":
            raise ValueError("YAML merge key is forbidden")
        if key in keys:
            raise ValueError(f"duplicate YAML member: {key}")
        keys.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _assert_json_shaped(value: Any) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        assert math.isfinite(value)
        return
    if isinstance(value, list):
        for item in value:
            _assert_json_shaped(item)
        return
    assert isinstance(value, dict)
    for key, item in value.items():
        assert isinstance(key, str)
        _assert_json_shaped(item)


def _load_yaml(name: str) -> dict[str, Any]:
    raw = (SOURCES / name).read_text(encoding="utf-8")
    assert raw.endswith("\n")
    assert "\r" not in raw
    assert "\t" not in raw
    forbidden_tokens = (
        yaml.tokens.AliasToken,
        yaml.tokens.AnchorToken,
        yaml.tokens.DocumentEndToken,
        yaml.tokens.DocumentStartToken,
        yaml.tokens.DirectiveToken,
        yaml.tokens.TagToken,
    )
    assert not any(isinstance(token, forbidden_tokens) for token in yaml.scan(raw))
    value = yaml.load(raw, Loader=_UniqueKeyLoader)
    assert isinstance(value, dict)
    _assert_json_shaped(value)
    return value


def _load_json(path: Path) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON member: {key}")
            value[key] = item
        return value

    raw = path.read_text(encoding="utf-8")
    assert raw.endswith("\n")
    assert "\r" not in raw
    assert "\t" not in raw
    value = json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON number: {token}")
        ),
    )
    assert isinstance(value, dict)
    return value


def _relative_files(root: Path) -> tuple[str, ...]:
    if not root.exists():
        return ()
    return tuple(
        sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    )


def _without_presentation(value: Any, *, root: bool = True) -> Any:
    if isinstance(value, dict):
        omitted = {"description"}
        if root:
            omitted.update({"name", "title", "version"})
        return {
            key: _without_presentation(item, root=False)
            for key, item in value.items()
            if key not in omitted
        }
    if isinstance(value, list):
        return [_without_presentation(item, root=False) for item in value]
    return value


def _without_branch_order(value: Any, *, parent: str | None = None) -> Any:
    if isinstance(value, dict):
        return {key: _without_branch_order(item, parent=key) for key, item in value.items()}
    if isinstance(value, list):
        normalized = [_without_branch_order(item) for item in value]
        if parent == "exactly_one_of":
            return sorted(
                normalized,
                key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")),
            )
        return normalized
    return value


def _pop_path(value: dict[str, Any], path: tuple[str, ...], expected: Any) -> None:
    parent: dict[str, Any] = value
    for member in path[:-1]:
        child = parent[member]
        assert isinstance(child, dict)
        parent = child
    assert parent.pop(path[-1]) == expected


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(_all_keys(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(_all_keys(item) for item in value), set())
    return set()


def test_neutral_input_inventory_is_exact() -> None:
    assert _relative_files(SOURCES) == SOURCE_NAMES
    assert _relative_files(OPERATIONS) == tuple(OPERATION_CASES)


def test_compile_source_operations_are_input_only() -> None:
    observed = {
        name: _load_json(OPERATIONS / name)
        for name in sorted(OPERATION_CASES)
    }
    assert observed == OPERATION_CASES
    assert not set().union(*(_all_keys(value) for value in observed.values())).intersection(
        FORBIDDEN_RESULT_KEYS
    )
    scenarios = _load_json(REQUIREMENTS)["scenarios"]
    declared_requirements = {
        (scenario["scenario_id"], requirement["requirement_id"])
        for scenario in scenarios
        for requirement in scenario["requirements"]
    }
    for value in observed.values():
        assert (value["scenario_id"], value["requirement_id"]) in declared_requirements
        source = ROOT / value["source_path"]
        assert source.is_file()
        assert source.resolve().is_relative_to(SOURCES.resolve())


def test_greenhouse_baseline_exercises_the_neutral_profile() -> None:
    source = _load_yaml("greenhouse/baseline.yaml")
    assert set(source) == {
        "classes",
        "default_range",
        "description",
        "enums",
        "id",
        "imports",
        "name",
        "slots",
        "title",
        "types",
        "version",
    }
    assert source["id"] == "https://example.malleus.dev/greenhouse"
    assert source["imports"] == ["linkml:types"]
    assert source["default_range"] == "string"
    assert source["types"] == {
        "Celsius": {
            "description": "Temperature measured in degrees Celsius.",
            "typeof": "float",
        }
    }
    assert set(source["enums"]["PlantState"]["permissible_values"]) == {
        "HEALTHY",
        "STRESSED",
    }
    assert source["classes"]["Traceable"]["mixin"] is True
    assert source["classes"]["Observation"]["is_a"] == "Sample"
    assert source["classes"]["Observation"]["mixins"] == ["Traceable"]
    assert set(source["classes"]["Observation"]["attributes"]) == {"note"}
    assert source["slots"]["specimen_id"]["identifier"] is True
    assert source["slots"]["temperature"]["minimum_value"] == -20
    assert source["slots"]["temperature"]["maximum_value"] == 60
    assert source["classes"]["Observation"]["exactly_one_of"] == [
        {"slot_conditions": {"state": {"equals_string": "HEALTHY"}}},
        {"slot_conditions": {"temperature": {"value_presence": "PRESENT"}}},
    ]


def test_source_variants_are_bounded_stimuli_not_oracles() -> None:
    baseline = _load_yaml("greenhouse/baseline.yaml")

    reordered = _load_yaml("greenhouse/reordered.yaml")
    assert (SOURCES / "greenhouse/reordered.yaml").read_bytes() != (
        SOURCES / "greenhouse/baseline.yaml"
    ).read_bytes()
    assert _without_branch_order(reordered) == _without_branch_order(baseline)

    presentation = _load_yaml("greenhouse/presentation-only.yaml")
    assert presentation["name"] == "greenhouse_presentation"
    assert presentation["version"] == "presentation-2"
    assert _without_presentation(presentation) == _without_presentation(baseline)

    numeric = _load_yaml("greenhouse/numeric-equivalent.yaml")
    numeric_text = (SOURCES / "greenhouse/numeric-equivalent.yaml").read_text(
        encoding="utf-8"
    )
    assert "    minimum_value: -20.0\n" in numeric_text
    assert "    maximum_value: 6e1\n" in numeric_text
    numeric["slots"]["temperature"]["minimum_value"] = -20
    numeric["slots"]["temperature"]["maximum_value"] = 60
    assert numeric == baseline

    semantic = _load_yaml("greenhouse/semantic-change.yaml")
    assert semantic["slots"]["temperature"]["maximum_value"] == 55
    semantic["slots"]["temperature"]["maximum_value"] = 60
    assert semantic == baseline

    explicit = copy.deepcopy(_load_yaml("greenhouse/explicit-defaults.yaml"))
    explicit_defaults = {
        ("classes", "Observation", "abstract"): False,
        ("classes", "Observation", "mixin"): False,
        ("classes", "Sample", "abstract"): False,
        ("classes", "Sample", "mixin"): False,
        ("classes", "Traceable", "abstract"): False,
        ("classes", "Observation", "attributes", "note", "identifier"): False,
        ("classes", "Observation", "attributes", "note", "inlined"): False,
        ("classes", "Observation", "attributes", "note", "multivalued"): False,
        ("classes", "Observation", "attributes", "note", "range"): "string",
        ("classes", "Observation", "attributes", "note", "required"): False,
        ("slots", "specimen_id", "inlined"): False,
        ("slots", "specimen_id", "multivalued"): False,
        ("slots", "specimen_id", "range"): "string",
        ("slots", "state", "identifier"): False,
        ("slots", "state", "inlined"): False,
        ("slots", "state", "multivalued"): False,
        ("slots", "state", "required"): False,
        ("slots", "temperature", "identifier"): False,
        ("slots", "temperature", "inlined"): False,
        ("slots", "temperature", "multivalued"): False,
        ("slots", "temperature", "required"): False,
    }
    for path, expected in explicit_defaults.items():
        _pop_path(explicit, path, expected)
    assert explicit == baseline

    serialized = json.dumps(
        [baseline, reordered, presentation, numeric, semantic, explicit],
        sort_keys=True,
    )
    assert not FORBIDDEN_RESULT_KEYS.intersection(_all_keys(json.loads(serialized)))
    for themed_word in ("bell", "dossier", "folio", "quiet"):
        assert themed_word not in serialized.lower()

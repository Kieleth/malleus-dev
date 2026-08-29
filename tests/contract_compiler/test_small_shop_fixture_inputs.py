from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
INPUT_ROOT = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment"
    / "input"
)
REPORT = ROOT / "conformance" / "contract_compiler" / "v0" / "evidence" / "CC-021.json"
TEST_PATH = Path(__file__).resolve()
BASE_COMMIT = "927ab183e33de09d62a3a6dba834306d54f35962"
BASE_COMMIT_TIME = datetime(2026, 8, 29, 5, 3, 43, tzinfo=timezone.utc)

MEMBERS = (
    "configuration/ret-010-selection.json",
    "configuration/time-context.json",
    "manifest.json",
    "sources/inventory-units.csv",
    "sources/warehouse.jsonl",
    "tbox/small-shop-description-only.yaml",
    "tbox/small-shop-root-instances.yaml",
    "tbox/small-shop.yaml",
)
NON_MANIFEST_MEMBERS = {
    "configuration/ret-010-selection.json": (
        "SCENARIO_SELECTION",
        "application/json",
    ),
    "configuration/time-context.json": (
        "SOURCE_TIME_CONTEXT",
        "application/json",
    ),
    "sources/inventory-units.csv": ("DOMAIN_REFERENCE_DATA", "text/csv"),
    "sources/warehouse.jsonl": (
        "SOURCE_OCCURRENCE_TRANSCRIPTION",
        "application/x-ndjson",
    ),
    "tbox/small-shop-description-only.yaml": (
        "LINKML_DESCRIPTION_VARIANT",
        "application/yaml",
    ),
    "tbox/small-shop-root-instances.yaml": (
        "LINKML_ROOT_INSTANCES_VECTOR",
        "application/yaml",
    ),
    "tbox/small-shop.yaml": ("LINKML_TBOX", "application/yaml"),
}

BASELINE_TBOX: dict[str, Any] = {
    "id": "https://malleus.dev/schema/small-shop-fulfilment",
    "name": "small_shop_fulfilment",
    "version": "0.1.0",
    "title": "Small Shop Fulfilment TBox",
    "description": ("Controlled TBox for the OKG-FX001 Small Shop Fulfilment fixture."),
    "default_range": "string",
    "prefixes": {
        "linkml": "https://w3id.org/linkml/",
        "malleus": "https://malleus.dev/schema/",
        "shop": "https://malleus.dev/schema/small-shop-fulfilment/",
    },
    "imports": ["linkml:types", "malleus"],
    "enums": {
        "ShopRelationKind": {
            "permissible_values": {"ORDER_CONTAINS_UNIT": None},
        }
    },
    "slots": {
        "order_number": {"range": "string"},
        "product_code": {"range": "string"},
    },
    "classes": {
        "SalesOrder": {
            "is_a": "Entity",
            "slots": ["order_number"],
            "slot_usage": {"order_number": {"required": True}},
        },
        "InventoryUnit": {
            "is_a": "Entity",
            "slots": ["product_code"],
            "slot_usage": {"product_code": {"required": True}},
        },
        "OrderContainsUnit": {
            "is_a": "Relation",
            "slot_usage": {
                "relation_type": {
                    "range": "ShopRelationKind",
                    "required": True,
                    "equals_string": "ORDER_CONTAINS_UNIT",
                },
                "source_id": {"range": "SalesOrder", "required": True},
                "target_id": {"range": "InventoryUnit", "required": True},
            },
        },
    },
}

WAREHOUSE_RECORD = {
    "event_id": "e27",
    "activity": "Pack Shipment",
    "time": "07-05 17:00",
    "actor": "R4",
    "order": "O1",
    "items": ["X1", "X2", "Y1"],
}

SELECTION = {
    "schema": "malleus.small-shop.selection/v1",
    "selection_id": "RET-010",
    "source_member": "sources/warehouse.jsonl",
    "source_record_ordinal": 1,
    "event_id": "e27",
    "order_id": "O1",
    "inventory_unit_id": "X1",
}

TIME_CONTEXT = {
    "schema": "malleus.small-shop.time-context/v1",
    "context_id": "ret-010-fixture-time-v1",
    "source_member": "sources/warehouse.jsonl",
    "source_field": "time",
    "source_format": "%d-%m %H:%M",
    "calendar": "PROLEPTIC_GREGORIAN",
    "fixture_year": 2000,
    "timezone": "UTC",
    "timezone_semantics": "FIXED_UTC_NO_DST",
    "ambiguous_local_time": "REFUSE",
    "nonexistent_local_time": "REFUSE",
    "derived_value_classification": "FIXTURE_DERIVED",
}

FORBIDDEN_INPUT_KEYS = {
    "accepted_graph",
    "candidate",
    "diagnostic",
    "expected",
    "facts",
    "ledger",
    "normalized_timestamp",
    "outcome",
    "prompt",
    "proposed_operations",
    "protocol_event",
    "result",
}
FORBIDDEN_TBOX_ROOT_KEYS = {
    "identity_policy",
    "instances",
    "invocation",
    "mapping",
    "outputs",
    "prior_graph",
    "recipe",
    "transformation",
}
ALLOWED_TBOX_ROOT_KEYS = {
    "classes",
    "default_range",
    "description",
    "enums",
    "id",
    "imports",
    "name",
    "prefixes",
    "slots",
    "title",
    "version",
}


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[str, Any]:
    keys: set[Any] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key == "<<":
            raise ValueError("YAML merge keys are forbidden")
        if key in keys:
            raise ValueError(f"duplicate YAML member: {key}")
        keys.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _assert_text_bytes(raw: bytes) -> str:
    assert not raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8", errors="strict")
    assert "\r" not in text
    assert text.endswith("\n")
    assert not text.endswith("\n\n")
    return text


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


def _load_json_text(text: str) -> Any:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON member: {key}")
            value[key] = item
        return value

    return json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON number: {token}")
        ),
    )


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_text(_assert_text_bytes(path.read_bytes()))
    assert isinstance(value, dict)
    _assert_json_shaped(value)
    return value


def _load_yaml_text(text: str) -> dict[str, Any]:
    forbidden_tokens = (
        yaml.tokens.AliasToken,
        yaml.tokens.AnchorToken,
        yaml.tokens.DocumentEndToken,
        yaml.tokens.DocumentStartToken,
        yaml.tokens.DirectiveToken,
        yaml.tokens.TagToken,
    )
    try:
        tokens = tuple(yaml.scan(text))
        if any(isinstance(token, forbidden_tokens) for token in tokens):
            raise ValueError("forbidden YAML syntax")
        documents = list(yaml.load_all(text, Loader=_UniqueKeyLoader))
    except yaml.YAMLError as error:
        raise ValueError("malformed YAML") from error
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise ValueError("one YAML mapping document is required")
    _assert_json_shaped(documents[0])
    return documents[0]


def _load_yaml(path: Path) -> dict[str, Any]:
    return _load_yaml_text(_assert_text_bytes(path.read_bytes()))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    text = _assert_text_bytes(path.read_bytes())
    lines = text.splitlines()
    assert lines
    records = [_load_json_text(line) for line in lines]
    assert all(isinstance(record, dict) for record in records)
    for record in records:
        _assert_json_shaped(record)
    return records


def _load_csv(path: Path) -> list[list[str]]:
    text = _assert_text_bytes(path.read_bytes())
    rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    assert rows
    assert all(row and all(isinstance(cell, str) for cell in row) for row in rows)
    return rows


def _relative_files(root: Path) -> tuple[str, ...]:
    if not root.exists():
        return ()
    return tuple(
        sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def _digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _walk(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for key, item in value.items():
            values.extend((key, *_walk(item)))
    elif isinstance(value, list):
        for item in value:
            values.extend(_walk(item))
    return values


def _assert_no_oracle_surface(value: Any) -> None:
    for member in _walk(value):
        if not isinstance(member, str):
            continue
        normalized = member.casefold().replace("-", "_")
        assert normalized not in FORBIDDEN_INPUT_KEYS
        assert normalized not in {"generated_candidate", "model"}


def test_exact_eight_member_inventory_and_text_integrity() -> None:
    assert _relative_files(INPUT_ROOT) == MEMBERS
    assert all(not path.is_symlink() for path in INPUT_ROOT.rglob("*"))
    for member in MEMBERS:
        _assert_text_bytes((INPUT_ROOT / member).read_bytes())


def test_strict_test_only_loaders_refuse_malformed_inputs() -> None:
    bad_json = (
        '{"schema":"one","schema":"two"}\n',
        '{"value":NaN}\n',
        '{"value":Infinity}\n',
        '{"value":-Infinity}\n',
    )
    for text in bad_json:
        with pytest.raises(ValueError):
            _load_json_text(text)

    bad_yaml = (
        "id: one\nid: two\n",
        "1: value\n",
        "%YAML 1.2\nid: one\n",
        "---\nid: one\n",
        "id: one\n...\n",
        "id: !custom one\n",
        "id: &identity one\ncopy: *identity\n",
        "base: &base\n  id: one\ncopy:\n  <<: *base\n",
        "id: one\n---\nid: two\n",
        "value: .nan\n",
    )
    for text in bad_yaml:
        with pytest.raises((AssertionError, ValueError)):
            _load_yaml_text(text)


def test_manifest_binds_every_nonmanifest_member_exactly_once() -> None:
    manifest = _load_json(INPUT_ROOT / "manifest.json")
    assert set(manifest) == {
        "schema",
        "fixture_id",
        "input_set_id",
        "members",
        "source_attribution",
        "limitations",
    }
    assert manifest["schema"] == "malleus.small-shop.input-set/v1"
    assert manifest["fixture_id"] == "OKG-FX001"
    assert manifest["input_set_id"] == "small-shop-ret-000-ret-010-v1"
    assert manifest["source_attribution"] == {
        "doi": "10.1007/978-3-031-08848-3_9",
        "work_title": "Event Knowledge Graphs",
        "source_locator": "Table 1",
        "event_id": "e27",
        "transcription_classification": "CONTROLLED_FIXTURE_TRANSCRIPTION",
    }
    assert manifest["limitations"] == [
        "Only the one retained e27 source row and one X1 reference row are in scope.",
        "The source time omits year and timezone; separate fixture context records both assumptions.",
        "These members contain inputs only and make no compiler or runtime result claim.",
    ]

    members = manifest["members"]
    assert isinstance(members, list)
    assert [member["path"] for member in members] == sorted(NON_MANIFEST_MEMBERS)
    assert len({member["path"] for member in members}) == len(members)
    assert {member["role"] for member in members} == {
        role for role, _ in NON_MANIFEST_MEMBERS.values()
    }
    for member in members:
        assert set(member) == {
            "path",
            "role",
            "media_type",
            "byte_length",
            "sha256",
        }
        path_text = member["path"]
        path = PurePosixPath(path_text)
        assert not path.is_absolute()
        assert path.as_posix() == path_text
        assert "." not in path.parts
        assert ".." not in path.parts
        assert "\\" not in path_text
        assert NON_MANIFEST_MEMBERS[path_text] == (
            member["role"],
            member["media_type"],
        )
        target = INPUT_ROOT / path_text
        assert target.is_file()
        assert not target.is_symlink()
        assert member["byte_length"] == len(target.read_bytes())
        assert member["sha256"] == _digest(target)


def test_tbox_is_exact_closed_od008_input_surface() -> None:
    baseline = _load_yaml(INPUT_ROOT / "tbox/small-shop.yaml")

    assert baseline == BASELINE_TBOX
    assert set(baseline) == ALLOWED_TBOX_ROOT_KEYS
    assert not set(baseline) & FORBIDDEN_TBOX_ROOT_KEYS
    assert baseline["imports"] == ["linkml:types", "malleus"]
    assert baseline["enums"] == {
        "ShopRelationKind": {
            "permissible_values": {"ORDER_CONTAINS_UNIT": None},
        }
    }
    assert baseline["slots"] == {
        "order_number": {"range": "string"},
        "product_code": {"range": "string"},
    }
    relation = baseline["classes"]["OrderContainsUnit"]
    assert relation == {
        "is_a": "Relation",
        "slot_usage": {
            "relation_type": {
                "range": "ShopRelationKind",
                "required": True,
                "equals_string": "ORDER_CONTAINS_UNIT",
            },
            "source_id": {"range": "SalesOrder", "required": True},
            "target_id": {"range": "InventoryUnit", "required": True},
        },
    }


def test_description_and_root_instances_vectors_have_only_authored_delta() -> None:
    baseline = _load_yaml(INPUT_ROOT / "tbox/small-shop.yaml")
    description_variant = _load_yaml(
        INPUT_ROOT / "tbox/small-shop-description-only.yaml"
    )
    root_instances = _load_yaml(INPUT_ROOT / "tbox/small-shop-root-instances.yaml")

    assert set(description_variant) == ALLOWED_TBOX_ROOT_KEYS
    assert description_variant["description"] == (
        "Presentation-only description variant for the OKG-FX001 controlled TBox."
    )
    baseline_without_description = copy.deepcopy(baseline)
    variant_without_description = copy.deepcopy(description_variant)
    del baseline_without_description["description"]
    del variant_without_description["description"]
    assert variant_without_description == baseline_without_description

    assert set(root_instances) == ALLOWED_TBOX_ROOT_KEYS | {"instances"}
    assert root_instances["instances"] == {}
    without_instances = copy.deepcopy(root_instances)
    del without_instances["instances"]
    assert without_instances == baseline


def test_e27_transcription_and_inventory_lookup_are_exact_raw_inputs() -> None:
    records = _load_jsonl(INPUT_ROOT / "sources/warehouse.jsonl")
    rows = _load_csv(INPUT_ROOT / "sources/inventory-units.csv")

    assert records == [WAREHOUSE_RECORD]
    assert rows == [["inventory_unit_id", "product_code"], ["X1", "X"]]
    assert set(records[0]) == {
        "event_id",
        "activity",
        "time",
        "actor",
        "order",
        "items",
    }
    assert records[0]["items"] == ["X1", "X2", "Y1"]
    assert sum(row[0] == "X1" for row in rows[1:]) == 1


def test_selection_resolves_source_row_order_and_unit_without_semantic_output() -> None:
    selection = _load_json(INPUT_ROOT / "configuration/ret-010-selection.json")
    records = _load_jsonl(INPUT_ROOT / selection["source_member"])
    rows = _load_csv(INPUT_ROOT / "sources/inventory-units.csv")

    assert selection == SELECTION
    record = records[selection["source_record_ordinal"] - 1]
    assert record["event_id"] == selection["event_id"]
    assert record["order"] == selection["order_id"]
    assert selection["inventory_unit_id"] in record["items"]
    assert sum(row[0] == selection["inventory_unit_id"] for row in rows[1:]) == 1
    selection_text = (INPUT_ROOT / "configuration/ret-010-selection.json").read_text(
        encoding="utf-8"
    )
    assert "OrderContainsUnit" not in selection_text
    assert "ORDER_CONTAINS_UNIT" not in selection_text


def test_time_context_contains_only_the_approved_derivation_parameters() -> None:
    context = _load_json(INPUT_ROOT / "configuration/time-context.json")
    record = _load_jsonl(INPUT_ROOT / context["source_member"])[0]

    assert context == TIME_CONTEXT
    assert context["source_field"] in record
    assert record[context["source_field"]] == "07-05 17:00"
    assert "tzdata" not in context
    assert "normalized_timestamp" not in context


def test_every_input_role_is_closed_and_oracle_free() -> None:
    values = [
        _load_json(INPUT_ROOT / "manifest.json"),
        _load_yaml(INPUT_ROOT / "tbox/small-shop.yaml"),
        _load_yaml(INPUT_ROOT / "tbox/small-shop-description-only.yaml"),
        _load_yaml(INPUT_ROOT / "tbox/small-shop-root-instances.yaml"),
        *_load_jsonl(INPUT_ROOT / "sources/warehouse.jsonl"),
        _load_json(INPUT_ROOT / "configuration/ret-010-selection.json"),
        _load_json(INPUT_ROOT / "configuration/time-context.json"),
    ]
    for value in values:
        _assert_no_oracle_surface(value)

    assert set(values[4]) == {"event_id", "activity", "time", "actor", "order", "items"}
    assert set(values[5]) == set(SELECTION)
    assert set(values[6]) == set(TIME_CONTEXT)


def test_cc021_verification_report_binds_exact_scope_and_claims() -> None:
    report = _load_json(REPORT)
    expected_artifacts = {
        *(INPUT_ROOT / member for member in MEMBERS),
        TEST_PATH,
    }
    artifact_paths = {
        (ROOT / artifact["path"]).resolve(): artifact
        for artifact in report["artifacts"]
    }

    assert set(report) == {
        "schema",
        "workstream_id",
        "recorded_at",
        "base_commit",
        "artifacts",
        "checks",
        "limitations",
    }
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-021"
    assert report["base_commit"] == BASE_COMMIT
    assert datetime.fromisoformat(report["recorded_at"]) > BASE_COMMIT_TIME
    assert set(artifact_paths) == expected_artifacts
    assert REPORT.resolve() not in artifact_paths
    for path, artifact in artifact_paths.items():
        assert set(artifact) == {"path", "byte_length", "sha256"}
        assert artifact["byte_length"] == len(path.read_bytes())
        assert artifact["sha256"] == _digest(path)

    checks = report["checks"]
    assert {check["check_id"] for check in checks} == {
        "cc021-red",
        "cc021-green",
        "cc021-ruff",
        "cc021-inventory-hash",
        "cc021-tbox-input",
        "cc021-authored-deltas",
        "cc021-e27-transcription",
        "cc021-selection-lookup-time",
        "cc021-oracle-free",
        "cc021-affected",
        "cc021-package",
    }
    assert all(
        set(check) == {"check_id", "method", "observed", "result"} for check in checks
    )
    assert all(check["result"] == "PASS" for check in checks)
    assert all(check["method"] and check["observed"] for check in checks)
    package = next(check for check in checks if check["check_id"] == "cc021-package")
    assert "PACKAGE NOT_APPLICABLE" in package["observed"]

    limitations = "\n".join(report["limitations"])
    for phrase in (
        "controlled transcription",
        "synthetic year 2000 and fixed UTC",
        "X2 and Y1",
        "raw input parameters",
        "no normalized value",
        "no corpus or checksum",
        "no public API, package, or release",
    ):
        assert phrase in limitations

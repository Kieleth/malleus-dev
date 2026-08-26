#!/usr/bin/env python3
"""Record CC-X02 raw declarations without resolving imports or choosing policy."""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

import yaml


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
OUTPUT = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "bundled_declaration_scan.json"
)
KINDS = ("types", "enums", "slots", "classes")
KIND_ORDER = {kind: index for index, kind in enumerate(KINDS)}


class DuplicateScanError(RuntimeError):
    """A required CC-X02 input or retained observation is invalid."""


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: _UniqueKeyLoader, node: yaml.Node, deep: bool = False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as error:
            raise DuplicateScanError(f"Unhashable YAML mapping key: {key!r}") from error
        if duplicate:
            raise DuplicateScanError(f"Duplicate YAML key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _unique_mapping,
)


def canonical_json(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as error:
        raise DuplicateScanError(f"Value is not exact JSON-compatible data: {error}") from error
    return (rendered + "\n").encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + hashlib.sha256(source).hexdigest()


def _read_bytes(path: Path, subject: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise DuplicateScanError(f"Cannot read {subject} '{path}': {error}") from error


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise DuplicateScanError(f"Module path escapes source root: {path}") from error


def _mapping(value: Any, subject: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise DuplicateScanError(f"{subject} must be a mapping")
    if any(not isinstance(key, str) for key in value):
        raise DuplicateScanError(f"{subject} must use string keys")
    return value


def _text(value: Any, subject: str) -> str:
    if not isinstance(value, str) or not value:
        raise DuplicateScanError(f"{subject} must be a nonempty string")
    return value


def load_yaml_module(path: Path) -> dict[str, Any]:
    source = _read_bytes(path, "ontology module")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise DuplicateScanError(f"Ontology module '{path}' is not UTF-8: {error}") from error
    try:
        value = yaml.load(text, Loader=_UniqueKeyLoader)
    except DuplicateScanError:
        raise
    except yaml.YAMLError as error:
        raise DuplicateScanError(f"Ontology module '{path}' is not valid YAML: {error}") from error
    module = dict(_mapping(value, f"Ontology module '{path}'"))
    canonical_json(module)
    return module


def _module_identity(module: Mapping[str, Any], path: Path, root: Path) -> dict[str, Any]:
    relative = _relative_path(path, root)
    source = _read_bytes(path, "ontology module")
    imports = module.get("imports")
    if not isinstance(imports, list) or any(not isinstance(item, str) for item in imports):
        raise DuplicateScanError(f"Ontology module '{relative}' imports must be a list of strings")
    return {
        "path": relative,
        "id": _text(module.get("id"), f"Ontology module '{relative}' id"),
        "name": _text(module.get("name"), f"Ontology module '{relative}' name"),
        "version": _text(module.get("version"), f"Ontology module '{relative}' version"),
        "source_byte_length": len(source),
        "source_sha256": _digest(source),
        "imports": list(imports),
    }


def _adopts(definition: Mapping[str, Any], subject: str) -> dict[str, Any]:
    if "annotations" not in definition or definition["annotations"] is None:
        return {"state": "ABSENT"}
    annotations = _mapping(definition["annotations"], f"{subject} annotations")
    if "adopts" not in annotations:
        return {"state": "ABSENT"}
    value = annotations["adopts"]
    if value is None:
        return {"state": "NULL"}
    canonical_json(value)
    return {"state": "VALUE", "value": value}


def scan_module(path: Path, root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    module = load_yaml_module(path)
    identity = _module_identity(module, path, root)
    counts = {}
    declarations = []
    for kind in KINDS:
        raw_declarations = module.get(kind, {})
        if raw_declarations is None:
            raw_declarations = {}
        raw_declarations = _mapping(
            raw_declarations,
            f"Ontology module '{identity['path']}' {kind}",
        )
        counts[kind] = len(raw_declarations)
        for symbol, raw_definition in raw_declarations.items():
            definition = _mapping(
                raw_definition,
                f"Ontology module '{identity['path']}' {kind}.{symbol}",
            )
            canonical_json(definition)
            declarations.append(
                {
                    "kind": kind,
                    "symbol": symbol,
                    "module": dict(identity),
                    "raw_definition": dict(definition),
                    "adopts": _adopts(
                        definition,
                        f"Ontology module '{identity['path']}' {kind}.{symbol}",
                    ),
                }
            )
    module_record = {
        **identity,
        "declaration_counts": counts,
        "declaration_count": sum(counts.values()),
    }
    return module_record, declarations


def _shared_data(pyproject: Mapping[str, Any]) -> Mapping[str, Any]:
    try:
        value = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["shared-data"]
    except (KeyError, TypeError) as error:
        raise DuplicateScanError(
            "pyproject.toml lacks tool.hatch.build.targets.wheel.shared-data"
        ) from error
    return _mapping(value, "wheel shared-data")


def discover_module_paths(pyproject_path: Path) -> list[Path]:
    source = _read_bytes(pyproject_path, "pyproject")
    try:
        pyproject = tomllib.loads(source.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise DuplicateScanError(f"pyproject '{pyproject_path}' is invalid TOML: {error}") from error
    shared_data = _shared_data(pyproject)
    relative_paths = []
    for source_path, destination in shared_data.items():
        if not isinstance(source_path, str) or not isinstance(destination, str):
            raise DuplicateScanError("wheel shared-data paths must be strings")
        relative = Path(source_path)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or not relative.parts
            or relative.parts[0] != "ontology"
            or relative.suffix != ".yaml"
        ):
            continue
        relative_paths.append(relative)
    if len(relative_paths) != 6:
        raise DuplicateScanError(
            f"Expected exactly six packaged ontology YAML modules, found {len(relative_paths)}"
        )
    if len(set(relative_paths)) != len(relative_paths):
        raise DuplicateScanError("Packaged ontology YAML module paths must be unique")
    return [pyproject_path.parent / relative for relative in sorted(relative_paths)]


def _duplicate_groups(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = defaultdict(list)
    for declaration in declarations:
        grouped[(declaration["kind"], declaration["symbol"])].append(declaration)
    result = []
    for (kind, symbol), occurrences in sorted(
        grouped.items(), key=lambda item: (KIND_ORDER[item[0][0]], item[0][1])
    ):
        if len(occurrences) < 2:
            continue
        retained = [
            {
                "module_path": occurrence["module"]["path"],
                "adopts": occurrence["adopts"],
            }
            for occurrence in occurrences
        ]
        retained.sort(key=lambda occurrence: occurrence["module_path"])
        result.append(
            {
                "kind": kind,
                "symbol": symbol,
                "occurrence_count": len(retained),
                "occurrences": retained,
            }
        )
    return result


def _cross_kind_repeats(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = defaultdict(list)
    for declaration in declarations:
        grouped[declaration["symbol"]].append(declaration)
    result = []
    for symbol, occurrences in sorted(grouped.items()):
        kinds = sorted({item["kind"] for item in occurrences}, key=KINDS.index)
        if len(kinds) < 2:
            continue
        result.append(
            {
                "symbol": symbol,
                "kinds": kinds,
                "occurrences": [
                    {"kind": item["kind"], "module_path": item["module"]["path"]}
                    for item in sorted(
                        occurrences,
                        key=lambda item: (
                            KIND_ORDER[item["kind"]],
                            item["module"]["path"],
                        ),
                    )
                ],
            }
        )
    return result


def build_scan(pyproject_path: Path = PYPROJECT) -> dict[str, Any]:
    pyproject_path = pyproject_path.resolve()
    root = pyproject_path.parent
    pyproject_source = _read_bytes(pyproject_path, "pyproject")
    modules = []
    declarations = []
    for path in discover_module_paths(pyproject_path):
        module, module_declarations = scan_module(path, root)
        modules.append(module)
        declarations.extend(module_declarations)
    modules.sort(key=lambda item: item["path"])
    declarations.sort(
        key=lambda item: (
            KIND_ORDER[item["kind"]],
            item["symbol"],
            item["module"]["path"],
        )
    )
    duplicate_groups = _duplicate_groups(declarations)
    cross_kind_repeats = _cross_kind_repeats(declarations)
    return {
        "schema": "malleus.contract-compiler.bundled-declaration-scan/v1",
        "workstream_id": "CC-X02",
        "pyproject": {
            "path": "pyproject.toml",
            "source_byte_length": len(pyproject_source),
            "source_sha256": _digest(pyproject_source),
        },
        "modules": modules,
        "declarations": declarations,
        "duplicate_groups": duplicate_groups,
        "cross_kind_repeats": cross_kind_repeats,
        "summary": {
            "module_count": len(modules),
            "declaration_count": len(declarations),
            "duplicate_group_count": len(duplicate_groups),
            "duplicate_occurrence_count": sum(
                item["occurrence_count"] for item in duplicate_groups
            ),
            "adopts_value_occurrence_count": sum(
                item["adopts"]["state"] == "VALUE" for item in declarations
            ),
            "cross_kind_repeat_count": len(cross_kind_repeats),
        },
    }


def render_scan(pyproject_path: Path = PYPROJECT) -> bytes:
    return canonical_json(build_scan(pyproject_path))


def check_scan(pyproject_path: Path = PYPROJECT, output_path: Path = OUTPUT) -> None:
    retained = _read_bytes(output_path, "retained CC-X02 scan")
    current = render_scan(pyproject_path)
    if retained != current:
        raise DuplicateScanError(
            f"Current bundled declarations do not match retained scan '{output_path}'"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--pyproject", type=Path, default=PYPROJECT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args(argv)
    try:
        if arguments.check:
            check_scan(arguments.pyproject, arguments.output)
            print("CC-X02 bundled declaration scan matches retained bytes")
        else:
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            arguments.output.write_bytes(render_scan(arguments.pyproject))
            print(f"Wrote CC-X02 bundled declaration scan to {arguments.output}")
    except (DuplicateScanError, OSError) as error:
        print(f"CC-X02 error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

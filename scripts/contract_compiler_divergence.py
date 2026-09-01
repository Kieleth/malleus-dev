#!/usr/bin/env python3
"""Record CC-X01 observations without choosing semantic policy."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
CORPUS = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "linkml_legacy_divergence"
)
CASES_PATH = CORPUS / "cases.json"
OBSERVATIONS_PATH = CORPUS / "observations.json"
ENVIRONMENT = (
    ROOT / "conformance" / "contract_compiler" / "v0" / "compiler_environment"
)
ENVIRONMENT_MANIFEST = ENVIRONMENT / "manifest.json"
ENVIRONMENT_LOCK = ENVIRONMENT / "requirements.lock"
ONTOLOGY_IMPLEMENTATION = ROOT / "src" / "malleus" / "ontology.py"

BASELINE = {"linkml": "1.11.1", "linkml-runtime": "1.11.1"}
CASE_IDS = [
    "simple_parity",
    "parent_mixin_precedence",
    "repeated_mixin",
    "conflicting_mixins_ab",
    "conflicting_mixins_ba",
    "numeric_bounds",
    "explicit_false",
    "default_range",
    "attribute_slot_usage",
]
ENGINE_IDS = ["linkml", "ontology_registry"]
CLASS_FIELDS = ("parent", "mixins", "slots")
CONSTRAINT_FIELDS = (
    "range",
    "required",
    "multivalued",
    "identifier",
    "inlined",
    "minimum_value",
    "maximum_value",
)
SLOT_PROBE_KINDS = {
    "attribute",
    "effective_slot",
    "global_slot",
    "slot_usage",
}
FORBIDDEN_DECISION_KEYS = {
    "classification",
    "comparison",
    "decision",
    "preferred",
    "recommendation",
    "verdict",
    "winner",
}
WHEEL_BINDINGS = {
    "linkml": {
        "filename": "linkml-1.11.1-py3-none-any.whl",
        "sha256": "sha256:d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed",
        "version": "1.11.1",
    },
    "linkml-runtime": {
        "filename": "linkml_runtime-1.11.1-py3-none-any.whl",
        "sha256": "sha256:b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da",
        "version": "1.11.1",
    },
}
SOURCE_BINDINGS = {
    "linkml": {
        "filename": "linkml-1.11.1.tar.gz",
        "sha256": "sha256:2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524",
    },
    "linkml-runtime": {
        "filename": "linkml_runtime-1.11.1.tar.gz",
        "sha256": "sha256:e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754",
    },
}
_MISSING = object()


class DivergenceError(RuntimeError):
    """A CC-X01 corpus or retained baseline is not the exact measured input."""


@dataclass(frozen=True)
class BaselineWheel:
    distribution: str
    version: str
    filename: str
    sha256: str
    path: Path


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, allow_nan=False, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def _digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _digest_file(path: Path) -> str:
    try:
        return _digest_bytes(path.read_bytes())
    except OSError as error:
        raise DivergenceError(f"Cannot read required CC-X01 input '{path}': {error}") from error


def _unique_mapping(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DivergenceError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _decode_json(text: str, subject: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_unique_mapping)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise DivergenceError(f"{subject} is not valid UTF-8 JSON: {error}") from error


def _read_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise DivergenceError(f"Cannot read required CC-X01 JSON '{path}': {error}") from error
    return _decode_json(text, str(path))


def _require_mapping(value: Any, subject: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise DivergenceError(f"{subject} must be a mapping")
    return value


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], subject: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise DivergenceError(f"{subject} keys differ; missing={missing}, extra={extra}")


def _require_nonempty_text(value: Any, subject: str) -> str:
    if not isinstance(value, str) or not value:
        raise DivergenceError(f"{subject} must be a nonempty string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise DivergenceError(f"{subject} must be UTF-8 encodable") from error
    return value


def _ordered_ids(value: Any, key: str, subject: str) -> list[Any]:
    if not isinstance(value, list):
        raise DivergenceError(f"{subject} must be a list")
    result = []
    for index, item in enumerate(value):
        item = _require_mapping(item, f"{subject} {index}")
        if key not in item:
            raise DivergenceError(f"{subject} {index} requires {key}")
        result.append(item[key])
    return result


def _walk_mappings(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def _reject_policy_fields(value: Any, subject: str) -> None:
    for mapping in _walk_mappings(value):
        forbidden = sorted(FORBIDDEN_DECISION_KEYS & set(mapping))
        if forbidden:
            raise DivergenceError(f"{subject} contains policy fields: {forbidden}")


def validate_cases(document: Any) -> None:
    root = _require_mapping(document, "CC-X01 cases")
    _require_exact_keys(root, {"schema", "workstream_id", "baseline", "cases"}, "CC-X01 cases")
    if root["schema"] != "malleus.contract-compiler.divergence-cases/v1":
        raise DivergenceError("CC-X01 cases schema is not v1")
    if root["workstream_id"] != "CC-X01":
        raise DivergenceError("CC-X01 cases workstream_id is not CC-X01")
    if root["baseline"] != BASELINE:
        raise DivergenceError(
            "CC-X01 baseline must contain exactly linkml 1.11.1 and linkml-runtime 1.11.1"
        )
    cases = root["cases"]
    if not isinstance(cases, list):
        raise DivergenceError("CC-X01 cases must be a list")
    if [case["case_id"] if isinstance(case, dict) and "case_id" in case else None for case in cases] != CASE_IDS:
        raise DivergenceError(f"CC-X01 case IDs and order must be exactly {CASE_IDS}")

    for case in cases:
        case_id = case["case_id"]
        _require_exact_keys(
            case,
            {
                "case_id",
                "target_class",
                "logical_locator",
                "source_text",
                "source_byte_length",
                "source_sha256",
                "probes",
            },
            f"case {case_id}",
        )
        target = _require_nonempty_text(case["target_class"], f"case {case_id} target_class")
        expected_locator = f"cc-x01/{case_id}.json"
        if case["logical_locator"] != expected_locator:
            raise DivergenceError(
                f"case {case_id} logical_locator must be {expected_locator!r}"
            )
        source_text = _require_nonempty_text(case["source_text"], f"case {case_id} source_text")
        source_bytes = source_text.encode("utf-8")
        if isinstance(case["source_byte_length"], bool) or not isinstance(
            case["source_byte_length"], int
        ):
            raise DivergenceError(f"case {case_id} source_byte_length must be an integer")
        if case["source_byte_length"] != len(source_bytes):
            raise DivergenceError(f"case {case_id} source_byte_length does not match source_text")
        if case["source_sha256"] != _digest_bytes(source_bytes):
            raise DivergenceError(f"case {case_id} source_sha256 does not match source_text")
        source = _require_mapping(_decode_json(source_text, expected_locator), expected_locator)
        if "imports" in source:
            raise DivergenceError(f"case {case_id} must be a single module without imports")
        if "classes" not in source or not isinstance(source["classes"], dict):
            raise DivergenceError(f"case {case_id} source requires classes")
        if target not in source["classes"]:
            raise DivergenceError(f"case {case_id} source does not declare target class {target!r}")

        probes = case["probes"]
        if not isinstance(probes, list) or not probes:
            raise DivergenceError(f"case {case_id} probes must be a nonempty list")
        probe_ids: list[str] = []
        for index, probe in enumerate(probes):
            probe = _require_mapping(probe, f"case {case_id} probe {index}")
            kind = probe["kind"] if "kind" in probe else None
            expected_keys = {"probe_id", "kind", "fields"}
            if kind in SLOT_PROBE_KINDS:
                expected_keys.add("slot")
            _require_exact_keys(probe, expected_keys, f"case {case_id} probe {index}")
            if kind != "class" and kind not in SLOT_PROBE_KINDS:
                raise DivergenceError(f"case {case_id} probe {index} has unknown kind {kind!r}")
            probe_id = _require_nonempty_text(
                probe["probe_id"], f"case {case_id} probe {index} probe_id"
            )
            probe_ids.append(probe_id)
            fields = probe["fields"]
            allowed = CLASS_FIELDS if kind == "class" else CONSTRAINT_FIELDS
            if (
                not isinstance(fields, list)
                or not fields
                or any(field not in allowed for field in fields)
                or len(fields) != len(set(fields))
            ):
                raise DivergenceError(f"case {case_id} probe {probe_id} fields are invalid")
            if kind in SLOT_PROBE_KINDS:
                _require_nonempty_text(probe["slot"], f"case {case_id} probe {probe_id} slot")
        if len(probe_ids) != len(set(probe_ids)):
            raise DivergenceError(f"case {case_id} probe IDs must be unique")
    _reject_policy_fields(root, "CC-X01 cases")


def load_cases(path: Path = CASES_PATH) -> dict[str, Any]:
    document = _read_json(path)
    validate_cases(document)
    return document


def locked_requirements(path: Path = ENVIRONMENT_LOCK) -> dict[str, dict[str, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise DivergenceError(f"Cannot read compiler lock '{path}': {error}") from error

    locked: dict[str, dict[str, str]] = {}
    for line_number, line in enumerate(lines, start=1):
        requirement, separator, digest = line.partition(" --hash=sha256:")
        distribution, pin, version = requirement.partition("==")
        if pin != "==" or not distribution or not version:
            raise DivergenceError(f"lock line {line_number} must be exactly pinned")
        if not separator or not digest:
            raise DivergenceError(f"lock line {line_number} requires one sha256 hash")
        name = distribution.casefold().replace("_", "-")
        if name in locked:
            raise DivergenceError(f"lock contains duplicate distribution {name!r}")
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise DivergenceError(f"lock line {line_number} has an invalid sha256 hash")
        locked[name] = {"sha256": "sha256:" + digest, "version": version}
    return locked


def _retained_artifact_records(
    manifest: Mapping[str, Any],
    environment: Path,
) -> dict[str, dict[str, Any]]:
    retained: dict[str, dict[str, Any]] = {}
    for section, directory in (
        ("roots", "roots"),
        ("build_inputs", "build-inputs"),
        ("derivative_inputs", "derivative-inputs"),
        ("built", "built"),
    ):
        value = _require_mapping(manifest.get(section), f"CC-002 {section}")
        artifacts = value.get("artifacts")
        if not isinstance(artifacts, list):
            raise DivergenceError(f"CC-002 {section} artifacts must be a list")
        for index, item in enumerate(artifacts):
            item = _require_mapping(item, f"CC-002 {section} artifact {index}")
            for field in ("filename", "byte_length", "sha256"):
                if field not in item:
                    raise DivergenceError(f"CC-002 {section} artifact {index} requires {field}")
            filename = _require_nonempty_text(
                item["filename"], f"CC-002 {section} artifact {index} filename"
            )
            if filename in retained:
                raise DivergenceError(f"retained artifact filename is duplicated: {filename}")
            path = environment / directory / filename
            try:
                source = path.read_bytes()
            except OSError as error:
                raise DivergenceError(f"Cannot read retained artifact '{path}': {error}") from error
            if item["byte_length"] != len(source) or item["sha256"] != _digest_bytes(source):
                raise DivergenceError(f"retained artifact bytes differ: {filename}")
            retained[filename] = dict(item)
    return retained


def retained_baseline(
    manifest: Any,
    environment: Path = ENVIRONMENT,
) -> tuple[BaselineWheel, BaselineWheel]:
    root = _require_mapping(manifest, "CC-002 environment manifest")
    if "schema" not in root or root["schema"] != "malleus.cc002.compiler-environment/v4":
        raise DivergenceError("CC-002 environment manifest is not the retained v4 schema")
    lock_record = _require_mapping(root.get("lock"), "CC-002 lock record")
    lock_path = environment / str(lock_record.get("filename", ""))
    try:
        lock_source = lock_path.read_bytes()
    except OSError as error:
        raise DivergenceError(f"Cannot read compiler lock '{lock_path}': {error}") from error
    if (
        lock_record.get("filename") != "requirements.lock"
        or lock_record.get("byte_length") != len(lock_source)
        or lock_record.get("sha256") != _digest_bytes(lock_source)
    ):
        raise DivergenceError("CC-002 lock record does not match requirements.lock")
    locked = locked_requirements(lock_path)
    retained = _retained_artifact_records(root, environment)

    selected: list[BaselineWheel] = []
    for distribution in ("linkml", "linkml-runtime"):
        expected = WHEEL_BINDINGS[distribution]
        if locked.get(distribution) != {
            "sha256": expected["sha256"],
            "version": expected["version"],
        }:
            raise DivergenceError(f"locked {distribution} does not match CC-X01 baseline")
        item = retained.get(expected["filename"])
        if item is None or item.get("sha256") != expected["sha256"]:
            raise DivergenceError(f"retained {distribution} direct root does not match CC-X01 baseline")
        source = SOURCE_BINDINGS[distribution]
        source_item = retained.get(source["filename"])
        if source_item is None or source_item.get("sha256") != source["sha256"]:
            raise DivergenceError(f"retained {distribution} source root does not match CC-X01 baseline")
        path = environment / "roots" / expected["filename"]
        if _digest_file(path) != expected["sha256"]:
            raise DivergenceError(f"retained {distribution} direct root bytes do not match CC-X01 baseline")
        selected.append(
            BaselineWheel(
                distribution=distribution,
                version=expected["version"],
                filename=expected["filename"],
                sha256=expected["sha256"],
                path=path,
            )
        )
    return selected[0], selected[1]


def _state(value: Any = _MISSING) -> dict[str, Any]:
    if value is _MISSING:
        return {"state": "ABSENT"}
    if value is None:
        return {"state": "NULL"}
    if isinstance(value, tuple):
        value = list(value)
    return {"state": "VALUE", "value": value}


def _normalize_error_argument(
    value: Any,
    replacements: tuple[tuple[str, str], ...],
) -> Any:
    if isinstance(value, str):
        for original, replacement in replacements:
            value = value.replace(original, replacement)
        return value
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, (list, tuple)):
        return [_normalize_error_argument(item, replacements) for item in value]
    raise DivergenceError(
        f"exception argument type {type(value).__name__!r} is not a deterministic scalar"
    )


def _error_value(error: Exception, replacements: tuple[tuple[str, str], ...] = ()) -> dict[str, Any]:
    message = str(error)
    for original, replacement in replacements:
        message = message.replace(original, replacement)
    return {
        "arguments": [_normalize_error_argument(item, replacements) for item in error.args],
        "error_type": type(error).__name__,
        "message": message,
    }


def _observed_fields(
    value: Any,
    fields: list[str],
    aliases: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    aliases = aliases or {}
    observed: dict[str, Any] = {}
    for field in fields:
        attribute = aliases[field] if field in aliases else field
        if not hasattr(value, attribute):
            observed[field] = _state()
        else:
            observed[field] = _state(getattr(value, attribute))
    return observed


def _probe_result(probe_id: str, value: Any, fields: list[str], aliases=None) -> dict[str, Any]:
    if value is _MISSING:
        result = _state()
    else:
        result = _state(_observed_fields(value, fields, aliases))
    return {"probe_id": probe_id, "result": result}


def _failed_probe(probe_id: str, error: Exception) -> dict[str, Any]:
    return {"probe_id": probe_id, "result": _state(_error_value(error))}


def _linkml_probe(view: Any, target: str, probe: Mapping[str, Any]) -> dict[str, Any]:
    probe_id = probe["probe_id"]
    fields = probe["fields"]
    kind = probe["kind"]
    try:
        cls = view.get_class(target, imports=False, strict=True)
        aliases = None
        if kind == "class":
            value = cls
            aliases = {"parent": "is_a"}
        elif kind == "attribute":
            value = cls.attributes[probe["slot"]] if probe["slot"] in cls.attributes else _MISSING
        elif kind == "global_slot":
            value = view.get_slot(probe["slot"], imports=False, attributes=False)
            if value is None:
                value = _MISSING
        elif kind == "slot_usage":
            value = cls.slot_usage[probe["slot"]] if probe["slot"] in cls.slot_usage else _MISSING
        else:
            value = view.induced_slot(probe["slot"], target, imports=False)
        return _probe_result(probe_id, value, fields, aliases)
    except Exception as error:
        return _failed_probe(probe_id, error)


def _linkml_case(case: Mapping[str, Any]) -> dict[str, Any]:
    try:
        from linkml_runtime.linkml_model.meta import SchemaDefinition
        from linkml_runtime.loaders import yaml_loader
        from linkml_runtime.utils.schemaview import SchemaView

        schema = yaml_loader.loads(case["source_text"], target_class=SchemaDefinition)
        view = SchemaView(schema)
    except Exception as error:
        return {
            "engine_id": "linkml",
            "construction": _state(_error_value(error)),
            "probes": [],
        }
    return {
        "engine_id": "linkml",
        "construction": _state("CONSTRUCTED"),
        "probes": [_linkml_probe(view, case["target_class"], probe) for probe in case["probes"]],
    }


def _legacy_probe(registry: Any, target: str, probe: Mapping[str, Any]) -> dict[str, Any]:
    probe_id = probe["probe_id"]
    fields = probe["fields"]
    kind = probe["kind"]
    try:
        typedef = registry.get_type(target)
        if kind == "class":
            value = typedef
        elif kind == "attribute":
            value = _MISSING
        elif kind == "global_slot":
            value = registry._slots[probe["slot"]] if probe["slot"] in registry._slots else _MISSING
        elif kind == "slot_usage":
            value = typedef.slot_usage[probe["slot"]] if probe["slot"] in typedef.slot_usage else _MISSING
        else:
            value = registry.effective_slots(target)
            value = value[probe["slot"]] if probe["slot"] in value else _MISSING
        return _probe_result(probe_id, value, fields)
    except Exception as error:
        return _failed_probe(probe_id, error)


def _legacy_case(
    case: Mapping[str, Any],
    directory: Path,
    registry_class: Any,
) -> dict[str, Any]:
    locator = case["logical_locator"]
    path = directory / Path(locator).name
    path.write_bytes(case["source_text"].encode("utf-8"))
    replacements = ((str(path), locator), (str(directory), "<CASE_DIR>"))
    try:
        registry = registry_class(path)
    except Exception as error:
        return {
            "engine_id": "ontology_registry",
            "construction": _state(_error_value(error, replacements)),
            "probes": [],
        }
    return {
        "engine_id": "ontology_registry",
        "construction": _state("CONSTRUCTED"),
        "probes": [_legacy_probe(registry, case["target_class"], probe) for probe in case["probes"]],
    }


def _bound_ontology_registry() -> Any:
    source_root = str((ROOT / "src").resolve())
    if not sys.path or sys.path[0] != source_root:
        sys.path.insert(0, source_root)
    from malleus import ontology

    origin = Path(ontology.__file__).resolve()
    if origin != ONTOLOGY_IMPLEMENTATION.resolve():
        raise DivergenceError(
            f"OntologyRegistry loaded from '{origin}', not exact bound source "
            f"'{ONTOLOGY_IMPLEMENTATION.resolve()}'"
        )
    return ontology.OntologyRegistry


def _module_origin(module_name: str) -> str:
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise DivergenceError(f"exact baseline module {module_name!r} is unavailable")
    return spec.origin


def _require_origin(module_name: str, wheel: Path) -> None:
    origin = _module_origin(module_name)
    prefix = str(wheel.resolve()) + os.sep
    if not origin.startswith(prefix):
        raise DivergenceError(f"exact baseline module {module_name!r} did not load from {wheel.name}")


def _verify_linkml_process(linkml_wheel: Path, runtime_wheel: Path) -> None:
    from importlib.metadata import version

    if version("linkml") != "1.11.1" or version("linkml-runtime") != "1.11.1":
        raise DivergenceError("baseline process did not load LinkML/linkml-runtime 1.11.1")
    _require_origin("linkml.generators", linkml_wheel)
    _require_origin("linkml_runtime", runtime_wheel)


def _linkml_subprocess(
    cases: list[dict[str, Any]],
    wheels: tuple[BaselineWheel, ...],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_distribution = {wheel.distribution: wheel for wheel in wheels}
    linkml_wheel = by_distribution["linkml"]
    runtime_wheel = by_distribution["linkml-runtime"]
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            str(Path(__file__).resolve()),
            "_linkml",
            str(linkml_wheel.path),
            str(runtime_wheel.path),
        ],
        input=canonical_json({"cases": cases}),
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise DivergenceError(f"exact LinkML baseline process failed: {detail}")
    result = _decode_json(completed.stdout.decode("utf-8"), "LinkML baseline output")
    result = _require_mapping(result, "LinkML baseline output")
    _require_exact_keys(
        result,
        {"execution_context", "observations"},
        "LinkML baseline output",
    )
    observations = result["observations"]
    if not isinstance(observations, list) or len(observations) != len(cases):
        raise DivergenceError("LinkML baseline output has the wrong case count")
    context = _require_mapping(result["execution_context"], "LinkML execution context")
    return observations, dict(context)


def _measure(cases_document: dict[str, Any]) -> dict[str, Any]:
    manifest = _read_json(ENVIRONMENT_MANIFEST)
    wheels = retained_baseline(manifest)
    cases = cases_document["cases"]
    linkml_observations, execution_context = _linkml_subprocess(cases, wheels)
    registry_class = _bound_ontology_registry()
    with tempfile.TemporaryDirectory(prefix="malleus-cc-x01-") as temporary:
        directory = Path(temporary)
        legacy_observations = [
            _legacy_case(case, directory, registry_class) for case in cases
        ]

    observations = []
    for index, case in enumerate(cases):
        observations.append(
            {
                "case_id": case["case_id"],
                "engines": [linkml_observations[index], legacy_observations[index]],
            }
        )
    return {
        "schema": "malleus.contract-compiler.divergence-observations/v1",
        "workstream_id": "CC-X01",
        "cases_sha256": _digest_bytes(canonical_json(cases_document)),
        "environment_manifest_sha256": _digest_file(ENVIRONMENT_MANIFEST),
        "execution_context": execution_context,
        "baseline": dict(BASELINE),
        "engines": [
            {
                "engine_id": "linkml",
                "interface": "linkml_runtime.utils.schemaview.SchemaView",
                "wheels": [
                    {
                        "distribution": wheel.distribution,
                        "filename": wheel.filename,
                        "sha256": wheel.sha256,
                        "version": wheel.version,
                    }
                    for wheel in wheels
                ],
            },
            {
                "engine_id": "ontology_registry",
                "implementation": "malleus.ontology.OntologyRegistry",
                "implementation_sha256": _digest_file(ONTOLOGY_IMPLEMENTATION),
            },
        ],
        "observations": observations,
    }


def _validate_state(value: Any, subject: str) -> None:
    state = _require_mapping(value, subject)
    if "state" not in state or state["state"] not in {"ABSENT", "NULL", "VALUE"}:
        raise DivergenceError(f"{subject} has an invalid state")
    expected = {"state", "value"} if state["state"] == "VALUE" else {"state"}
    _require_exact_keys(state, expected, subject)


def validate_observations(document: Any) -> None:
    root = _require_mapping(document, "CC-X01 observations")
    _require_exact_keys(
        root,
        {
            "schema",
            "workstream_id",
            "cases_sha256",
            "environment_manifest_sha256",
            "baseline",
            "engines",
            "execution_context",
            "observations",
        },
        "CC-X01 observations",
    )
    if root["schema"] != "malleus.contract-compiler.divergence-observations/v1":
        raise DivergenceError("CC-X01 observations schema is not v1")
    if root["workstream_id"] != "CC-X01" or root["baseline"] != BASELINE:
        raise DivergenceError("CC-X01 observations bind the wrong workstream or baseline")
    cases = load_cases()
    if root["cases_sha256"] != _digest_bytes(canonical_json(cases)):
        raise DivergenceError("CC-X01 observations bind the wrong cases")
    if root["environment_manifest_sha256"] != _digest_file(ENVIRONMENT_MANIFEST):
        raise DivergenceError("CC-X01 observations bind the wrong CC-002 environment manifest")
    context = _require_mapping(root["execution_context"], "CC-X01 execution context")
    _require_exact_keys(context, {"platform", "python", "pyyaml"}, "CC-X01 execution context")
    _require_exact_keys(
        _require_mapping(context["python"], "CC-X01 Python context"),
        {"implementation", "version"},
        "CC-X01 Python context",
    )
    _require_exact_keys(
        _require_mapping(context["platform"], "CC-X01 platform context"),
        {"architecture", "operating_system"},
        "CC-X01 platform context",
    )
    pyyaml = _require_mapping(context["pyyaml"], "CC-X01 PyYAML context")
    _require_exact_keys(pyyaml, {"distribution", "version"}, "CC-X01 PyYAML context")
    if pyyaml["distribution"] != "PyYAML":
        raise DivergenceError("CC-X01 PyYAML distribution identity differs")
    engines = root["engines"]
    if _ordered_ids(engines, "engine_id", "CC-X01 engines") != ENGINE_IDS:
        raise DivergenceError(f"CC-X01 engines must be exactly {ENGINE_IDS}")
    _require_exact_keys(engines[0], {"engine_id", "interface", "wheels"}, "LinkML engine")
    if engines[0]["interface"] != "linkml_runtime.utils.schemaview.SchemaView":
        raise DivergenceError("CC-X01 LinkML engine interface differs")
    expected_wheels = [
        {"distribution": name, **WHEEL_BINDINGS[name]}
        for name in ("linkml", "linkml-runtime")
    ]
    if engines[0]["wheels"] != expected_wheels:
        raise DivergenceError("CC-X01 LinkML engine wheels differ")
    _require_exact_keys(
        engines[1],
        {"engine_id", "implementation", "implementation_sha256"},
        "OntologyRegistry engine",
    )
    if engines[1]["implementation"] != "malleus.ontology.OntologyRegistry":
        raise DivergenceError("CC-X01 OntologyRegistry implementation differs")
    if engines[1]["implementation_sha256"] != _digest_file(ONTOLOGY_IMPLEMENTATION):
        raise DivergenceError("CC-X01 OntologyRegistry implementation bytes differ")
    observations = root["observations"]
    if _ordered_ids(observations, "case_id", "CC-X01 observations") != CASE_IDS:
        raise DivergenceError(f"CC-X01 observations must contain exactly {CASE_IDS}")
    for case_index, case in enumerate(observations):
        _require_exact_keys(case, {"case_id", "engines"}, f"observation {case['case_id']}")
        case_engines = case["engines"]
        if _ordered_ids(
            case_engines,
            "engine_id",
            f"observation {case['case_id']} engines",
        ) != ENGINE_IDS:
            raise DivergenceError(f"observation {case['case_id']} engines differ")
        for engine in case_engines:
            subject = f"observation {case['case_id']} engine {engine['engine_id']}"
            _require_exact_keys(engine, {"engine_id", "construction", "probes"}, subject)
            _validate_state(engine["construction"], subject + " construction")
            if not isinstance(engine["probes"], list):
                raise DivergenceError(subject + " probes must be a list")
            construction = engine["construction"]
            constructed = construction == {"state": "VALUE", "value": "CONSTRUCTED"}
            if constructed:
                expected_probe_ids = [probe["probe_id"] for probe in cases["cases"][case_index]["probes"]]
                actual_probe_ids = [
                    probe["probe_id"] if isinstance(probe, dict) and "probe_id" in probe else None
                    for probe in engine["probes"]
                ]
                if actual_probe_ids != expected_probe_ids:
                    raise DivergenceError(subject + " probe IDs differ from the case contract")
            else:
                failure = construction["value"] if construction["state"] == "VALUE" else None
                failure = _require_mapping(failure, subject + " construction failure")
                _require_exact_keys(
                    failure,
                    {"arguments", "error_type", "message"},
                    subject + " construction failure",
                )
                if engine["probes"]:
                    raise DivergenceError(subject + " must not retain probes after construction failure")
            for probe in engine["probes"]:
                _require_exact_keys(probe, {"probe_id", "result"}, subject + " probe")
                _validate_state(probe["result"], subject + f" probe {probe['probe_id']}")
            for expected_probe, actual_probe in zip(
                cases["cases"][case_index]["probes"],
                engine["probes"],
            ):
                result = actual_probe["result"]
                if result["state"] != "VALUE":
                    continue
                value = _require_mapping(
                    result["value"], subject + f" probe {actual_probe['probe_id']} value"
                )
                if set(value) == {"arguments", "error_type", "message"}:
                    continue
                _require_exact_keys(
                    value,
                    set(expected_probe["fields"]),
                    subject + f" probe {actual_probe['probe_id']} fields",
                )
                for field in expected_probe["fields"]:
                    _validate_state(
                        value[field],
                        subject + f" probe {actual_probe['probe_id']} field {field}",
                    )
    for index, state in enumerate(
        mapping for mapping in _walk_mappings(observations) if "state" in mapping
    ):
        _validate_state(state, f"CC-X01 nested observation state {index}")
    _reject_policy_fields(root, "CC-X01 observations")


def render_observations(cases_document: dict[str, Any]) -> bytes:
    validate_cases(cases_document)
    result = _measure(cases_document)
    validate_observations(result)
    return canonical_json(result)


def semantic_observations(document: Mapping[str, Any]) -> dict[str, Any]:
    """The replay surface, excluding host metadata retained as evidence."""
    return {key: value for key, value in document.items() if key != "execution_context"}


def check_observations(
    cases_path: Path = CASES_PATH,
    observations_path: Path = OBSERVATIONS_PATH,
) -> None:
    cases = load_cases(cases_path)
    expected = _read_json(observations_path)
    validate_observations(expected)
    actual = _decode_json(
        render_observations(cases).decode("utf-8"),
        "fresh CC-X01 observations",
    )
    try:
        retained = observations_path.read_bytes()
    except OSError as error:
        raise DivergenceError(f"Cannot read retained observations '{observations_path}': {error}") from error
    if retained != canonical_json(expected):
        raise DivergenceError("retained observations are not canonical JSON")
    if semantic_observations(actual) != semantic_observations(expected):
        raise DivergenceError("fresh CC-X01 semantic observations do not match retained bytes")


def _child_main(linkml_wheel: Path, runtime_wheel: Path) -> int:
    sys.path[:0] = [str(linkml_wheel), str(runtime_wheel)]
    _verify_linkml_process(linkml_wheel, runtime_wheel)
    payload = _decode_json(sys.stdin.buffer.read().decode("utf-8"), "CC-X01 child input")
    payload = _require_mapping(payload, "CC-X01 child input")
    _require_exact_keys(payload, {"cases"}, "CC-X01 child input")
    cases = payload["cases"]
    if not isinstance(cases, list):
        raise DivergenceError("CC-X01 child cases must be a list")
    from importlib.metadata import version

    result = {
        "execution_context": {
            "platform": {
                "architecture": platform.machine(),
                "operating_system": platform.system(),
            },
            "python": {
                "implementation": platform.python_implementation(),
                "version": platform.python_version(),
            },
            "pyyaml": {
                "distribution": "PyYAML",
                "version": version("PyYAML"),
            },
        },
        "observations": [_linkml_case(case) for case in cases],
    }
    sys.stdout.buffer.write(canonical_json(result))
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "_linkml":
        if len(arguments) != 3:
            raise DivergenceError("LinkML child requires exactly two retained wheel paths")
        return _child_main(Path(arguments[1]), Path(arguments[2]))
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="compare a fresh replay with retained bytes")
    action.add_argument("--render", action="store_true", help="write a fresh replay to standard output")
    options = parser.parse_args(arguments)
    if options.render:
        sys.stdout.buffer.write(render_observations(load_cases()))
        return 0
    check_observations()
    print("CC-X01 semantic observations match retained observations")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DivergenceError as error:
        print(f"CC-X01: {error}", file=sys.stderr)
        raise SystemExit(1) from error

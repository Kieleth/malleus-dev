#!/usr/bin/env python3
"""Offline validator for the frozen OD-012 baseline candidate inventory."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "compiler_baseline_candidates.json"
)
REPOSITORY = "https://github.com/linkml/linkml"
PATHS = {"linkml": "packages/linkml", "linkml-runtime": "packages/linkml_runtime"}
AUDITED_IDENTITY = (
    "sha256:71319ecb9827143ab41961b329ca1e838a4487772d3e55664f24c1e2eab8a85c"
)
MOVING = {"head", "latest", "main", "master"}
GOVERNANCE = {
    "preference",
    "preferred",
    "rank",
    "ranking",
    "recommendation",
    "recommended",
    "selected",
    "selection",
}


class InventoryError(ValueError):
    """The inventory is malformed or differs from the audited research facts."""


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise InventoryError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value: str) -> None:
    raise InventoryError(f"non-finite JSON number: {value}")


def _key_words(key: str) -> set[str]:
    return set(
        "".join(
            character if character.isalnum() else " " for character in key.lower()
        ).split()
    )


def _deny_governance_fields(value: Any, context: str = "inventory") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if GOVERNANCE & _key_words(key):
                raise InventoryError(f"{context}: forbidden governance field: {key}")
            _deny_governance_fields(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _deny_governance_fields(item, f"{context}[{index}]")


def _shape(value: Any, spec: Any, context: str) -> None:
    if spec is str:
        if not isinstance(value, str) or not value.strip():
            raise InventoryError(f"{context}: expected non-empty string")
        return
    if spec is int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise InventoryError(f"{context}: expected positive integer")
        return
    if spec is list:
        if not isinstance(value, list):
            raise InventoryError(f"{context}: expected array")
        return
    if isinstance(spec, list):
        if not isinstance(value, list):
            raise InventoryError(f"{context}: expected array")
        for index, item in enumerate(value):
            _shape(item, spec[0], f"{context}[{index}]")
        return
    if not isinstance(value, dict):
        raise InventoryError(f"{context}: expected object")
    missing = sorted(spec.keys() - value.keys())
    unknown = sorted(value.keys() - spec.keys())
    if missing:
        raise InventoryError(f"{context}: missing field(s): {', '.join(missing)}")
    if unknown:
        raise InventoryError(f"{context}: unknown field(s): {', '.join(unknown)}")
    for key, child in spec.items():
        _shape(value[key], child, f"{context}.{key}")


REF = {"id": str, "kind": str}
PROVENANCE = {
    "commit": str,
    "evidence_source_id": str,
    "repository": str,
    "state": str,
    "tag": str,
}
ARTIFACT = {
    "artifact_id": str,
    "artifact_target": str,
    "byte_length": int,
    "evidence_source_id": str,
    "filename": str,
    "kind": str,
    "provenance_url": str,
    "provision": str,
    "sha256": str,
    "url": str,
}
RELEASE_DISTRIBUTION = {
    "advertised_python_minors": [str],
    "artifacts": [ARTIFACT],
    "dependency_constraints": [{"name": str, "specifier": str}],
    "name": str,
    "provenance": PROVENANCE,
    "requires_python": str,
    "source_path": str,
    "version": str,
}
BUILD_TARGET = {
    "artifact_id": str,
    "identity_state": str,
    "kind": str,
    "limitation": str,
    "provision": str,
    "required_identity_fields": [str],
    "target_python_candidate_ids": [str],
}
SOURCE_DISTRIBUTION = {"name": str, "source_path": str, "wheel_target": BUILD_TARGET}
FEASIBILITY = {
    "missing_inputs": [REF],
    "present_inputs": [REF],
    "remaining_probe": str,
    "state": str,
}
COMMON_CANDIDATE = {
    "candidate_id": str,
    "kind": str,
    "limitations": [str],
    "lock_feasibility": FEASIBILITY,
    "python_candidate_ids": [str],
}
RELEASE_CANDIDATE = COMMON_CANDIDATE | {
    "distributions": [RELEASE_DISTRIBUTION],
    "source": {
        "archive": {"artifact_ids": [str], "identity_state": str},
        "commit": str,
        "coordinate_url": str,
        "evidence_source_ids": [str],
        "repository": str,
        "tag": str,
    },
}
SOURCE_CANDIDATE = COMMON_CANDIDATE | {
    "distributions": [SOURCE_DISTRIBUTION],
    "source": {
        "archive": {
            "archive_id": str,
            "evidence_source_id": str,
            "identity_state": str,
            "limitation": str,
            "locator": str,
            "required_identity_fields": [str],
        },
        "commit": str,
        "coordinate_url": str,
        "evidence_source_ids": [str],
        "repository": str,
    },
}
PYTHON_CANDIDATE = {
    "abi": str,
    "architecture": str,
    "artifact_target": str,
    "basis_source_id": str,
    "candidate_id": str,
    "implementation": str,
    "limitation": str,
    "operating_system": str,
    "version": str,
}
SOURCE_COMMON = {"kind": str, "publisher": str, "source_id": str, "url": str}
SOURCE_SCHEMAS = {
    "GITHUB_COMMIT": SOURCE_COMMON | {"commit": str, "repository": str},
    "GITHUB_RELEASE": SOURCE_COMMON | {"commit": str, "repository": str, "tag": str},
    "PYPI_PROVENANCE": SOURCE_COMMON
    | {
        "commit": str,
        "project": str,
        "repository": str,
        "tag": str,
        "version": str,
    },
    "PYPI_RELEASE": SOURCE_COMMON | {"project": str, "version": str},
    "PYTHON_RELEASE": SOURCE_COMMON | {"implementation": str, "version": str},
}
ROOT_SPEC = {
    "audit_date": str,
    "authority": {"decision_authority": str, "production_artifact_authority": str},
    "candidates": list,
    "decision_id": str,
    "limitations": [str],
    "python_candidates": [PYTHON_CANDIDATE],
    "repository": {
        "distributions": [{"name": str, "source_path": str}],
        "layout": str,
        "url": str,
    },
    "schema": str,
    "scope": str,
    "sources": list,
}


def _hex(value: str, size: int, context: str) -> None:
    if len(value) != size or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise InventoryError(
            f"{context}: expected {size} lowercase hexadecimal characters"
        )


def _commit(value: str, context: str) -> str:
    if value.lower() in MOVING:
        raise InventoryError(f"{context}: immutable commit required")
    _hex(value, 40, context)
    return value


def _version(value: str, context: str, parts: int = 3) -> str:
    pieces = value.split(".")
    if len(pieces) != parts or any(not piece.isdigit() for piece in pieces):
        label = "three-part" if parts == 3 else "two-part"
        raise InventoryError(f"{context}: expected exact {label} version")
    return value


def _tag(value: str, context: str) -> str:
    if value.lower() in MOVING:
        raise InventoryError(f"{context}: immutable release tag required")
    version = _version(value.removeprefix("v"), context)
    if value != "v" + version:
        raise InventoryError(f"{context}: immutable release tag required")
    return version


def _url(value: str, context: str) -> None:
    if not value.startswith("https://") or any(
        character.isspace() for character in value
    ):
        raise InventoryError(f"{context}: expected HTTPS URL")
    segments = set(value.replace("?", "/").replace("#", "/").lower().split("/"))
    if MOVING & segments:
        raise InventoryError(f"{context}: immutable coordinate required")


def _unique(values: list[str], context: str, minimum: int = 1) -> set[str]:
    if len(values) < minimum or len(values) != len(set(values)):
        raise InventoryError(f"{context}: missing or duplicate values")
    return set(values)


def _refs(
    items: list[dict[str, str]], expected: set[tuple[str, str]], context: str
) -> None:
    actual = [(item["kind"], item["id"]) for item in items]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise InventoryError(f"{context}: typed input references mismatch")


def _source_for(
    sources: dict[str, dict[str, Any]],
    source_id: str,
    kind: str,
    context: str,
    **subject: str,
) -> None:
    source = sources.get(source_id)
    if (
        source is None
        or source["kind"] != kind
        or any(source[key] != value for key, value in subject.items())
    ):
        raise InventoryError(f"{context}: evidence source subject mismatch")


def _fields(
    value: dict[str, Any],
    expected: dict[str, Any],
    context: str,
    mismatch: str = "subject mismatch",
) -> None:
    if any(value[key] != item for key, item in expected.items()):
        raise InventoryError(f"{context}: {mismatch}")


def _candidate_python_ids(
    candidate: dict[str, Any], python_ids: set[str], context: str
) -> set[str]:
    result = _unique(
        candidate["python_candidate_ids"], f"{context}.python_candidate_ids"
    )
    if not result <= python_ids:
        raise InventoryError(f"{context}.python_candidate_ids: unknown Python tuple")
    return result


def _validate_feasibility(
    candidate: dict[str, Any],
    state: str,
    present: set[tuple[str, str]],
    missing: set[tuple[str, str]],
    context: str,
) -> None:
    feasibility = candidate["lock_feasibility"]
    if feasibility["state"] in {"VERIFIED_FEASIBLE", "VERIFIED_INFEASIBLE"}:
        raise InventoryError(f"{context}: verified feasibility is not claimable")
    if feasibility["state"] != state:
        raise InventoryError(f"{context}: unsupported lock feasibility state")
    _refs(feasibility["present_inputs"], present, f"{context}.{state} present inputs")
    _refs(feasibility["missing_inputs"], missing, f"{context}.{state} missing inputs")


def _map_distributions(items: list[dict[str, Any]], context: str) -> dict[str, Any]:
    mapped = {item["name"]: item for item in items}
    if len(items) != 2 or set(mapped) != set(PATHS):
        raise InventoryError(f"{context}: expected exactly linkml and linkml-runtime")
    return mapped


def _normalize_valid(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["candidates"].sort(
        key=lambda item: {"RELEASE": 0, "SOURCE_COMMIT": 1}[item["kind"]]
    )
    result["python_candidates"].sort(key=lambda item: item["candidate_id"])
    result["repository"]["distributions"].sort(key=lambda item: item["name"])
    result["sources"].sort(key=lambda item: (item["kind"], item["url"]))
    for candidate in result["candidates"]:
        candidate["distributions"].sort(key=lambda item: item["name"])
        candidate["python_candidate_ids"].sort()
        candidate["source"]["evidence_source_ids"].sort()
        archive = candidate["source"]["archive"]
        if candidate["kind"] == "RELEASE":
            archive["artifact_ids"].sort()
        else:
            archive["required_identity_fields"].sort()
        feasibility = candidate["lock_feasibility"]
        feasibility["present_inputs"].sort(key=lambda item: (item["kind"], item["id"]))
        feasibility["missing_inputs"].sort(key=lambda item: (item["kind"], item["id"]))
        for distribution in candidate["distributions"]:
            if candidate["kind"] == "RELEASE":
                distribution["artifacts"].sort(
                    key=lambda item: {"WHEEL": 0, "SDIST": 1}[item["kind"]]
                )
                distribution["advertised_python_minors"].sort(
                    key=lambda item: tuple(int(part) for part in item.split("."))
                )
                distribution["dependency_constraints"].sort(
                    key=lambda item: (item["name"], item["specifier"])
                )
            else:
                target = distribution["wheel_target"]
                target["required_identity_fields"].sort()
                target["target_python_candidate_ids"].sort()
    return result


def _identity(value: dict[str, Any]) -> str:
    canonical = json.dumps(
        _normalize_valid(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


def _validate_sources(items: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list) or not items:
        raise InventoryError("sources: non-empty array required")
    ids: list[str] = []
    for index, source in enumerate(items):
        context = f"sources[{index}]"
        kind = source.get("kind") if isinstance(source, dict) else None
        if not isinstance(kind, str) or kind not in SOURCE_SCHEMAS:
            raise InventoryError(f"{context}.kind: unsupported source kind")
        _shape(source, SOURCE_SCHEMAS[kind], context)
        publisher = (
            "GitHub"
            if kind.startswith("GITHUB_")
            else "PyPI"
            if kind.startswith("PYPI_")
            else "Python Software Foundation"
        )
        if source["publisher"] != publisher:
            raise InventoryError(f"{context}.publisher: official publisher mismatch")
        ids.append(source["source_id"])
        _url(source["url"], f"{context}.url")
        if "commit" in source:
            _commit(source["commit"], f"{context}.commit")
        if "version" in source:
            _version(source["version"], f"{context}.version")
        if "tag" in source:
            _tag(source["tag"], f"{context}.tag")
        if kind == "GITHUB_COMMIT":
            expected_id = f"github-linkml-{source['commit'][:8]}-commit"
            expected_url = f"{REPOSITORY}/commit/{source['commit']}"
            bound = source["repository"] == REPOSITORY
        elif kind == "GITHUB_RELEASE":
            expected_id = f"github-linkml-{source['tag']}-release"
            expected_url = f"{REPOSITORY}/releases/tag/{source['tag']}"
            bound = source["repository"] == REPOSITORY
        elif kind in {"PYPI_RELEASE", "PYPI_PROVENANCE"}:
            project = source["project"]
            suffix = "metadata" if kind == "PYPI_RELEASE" else "provenance"
            expected_id = f"pypi-{project}-{source['version']}-{suffix}"
            route = "pypi" if kind == "PYPI_RELEASE" else "project"
            ending = "json" if kind == "PYPI_RELEASE" else ""
            expected_url = (
                f"https://pypi.org/{route}/{project}/{source['version']}/{ending}"
            )
            bound = project in PATHS
            if kind == "PYPI_PROVENANCE":
                bound = (
                    bound
                    and source["repository"] == REPOSITORY
                    and _tag(source["tag"], f"{context}.tag") == source["version"]
                )
        else:
            compact = source["version"].replace(".", "")
            expected_id = f"python-{source['version']}-release"
            expected_url = f"https://www.python.org/downloads/release/python-{compact}/"
            bound = source["implementation"] == "CPython"
        if (
            not bound
            or source["source_id"] != expected_id
            or source["url"] != expected_url
        ):
            raise InventoryError(f"{context}: official source subject mismatch")
    _unique(ids, "sources")
    return {source_id: source for source_id, source in zip(ids, items, strict=True)}


def _validate_published_distribution(
    project: str,
    distribution: dict[str, Any],
    version: str,
    commit: str,
    tag: str,
    sources: dict[str, dict[str, Any]],
    context: str,
) -> tuple[set[str], set[str]]:
    _fields(
        distribution,
        {
            "source_path": PATHS[project],
            "version": version,
            "requires_python": ">=3.10",
        },
        context,
    )
    minors = _unique(
        distribution["advertised_python_minors"],
        f"{context}.advertised_python_minors",
    )
    if minors != {"3.10", "3.11", "3.12", "3.13"}:
        raise InventoryError(f"{context}: advertised Python minors mismatch")
    kinds = _unique([item["kind"] for item in distribution["artifacts"]], context)
    if kinds != {"WHEEL", "SDIST"}:
        raise InventoryError(f"{context}: one wheel and one sdist required")

    artifact_ids: set[str] = set()
    metadata_id = f"pypi-{project}-{version}-metadata"
    filename_project = project.replace("-", "_")
    for artifact in distribution["artifacts"]:
        kind = artifact["kind"]
        filename = (
            f"{filename_project}-{version}-py3-none-any.whl"
            if kind == "WHEEL"
            else f"{filename_project}-{version}.tar.gz"
        )
        artifact_id = f"pypi:{project}:{version}:{kind.lower()}"
        _fields(
            artifact,
            {
                "artifact_id": artifact_id,
                "artifact_target": "py3-none-any" if kind == "WHEEL" else "source",
                "evidence_source_id": metadata_id,
                "filename": filename,
                "provenance_url": f"https://pypi.org/integrity/{project}/{version}/{filename}/provenance",
                "provision": "PUBLISHED",
            },
            f"{context}.artifacts.{kind}",
            "published artifact mismatch",
        )
        if not artifact["url"].startswith(
            "https://files.pythonhosted.org/packages/"
        ) or not artifact["url"].endswith("/" + filename):
            raise InventoryError(f"{context}: published artifact URL mismatch")
        _hex(artifact["sha256"], 64, f"{context}.sha256")
        _url(artifact["url"], f"{context}.url")
        _url(artifact["provenance_url"], f"{context}.provenance_url")
        artifact_ids.add(artifact_id)
    _source_for(
        sources,
        metadata_id,
        "PYPI_RELEASE",
        context,
        project=project,
        version=version,
    )

    provenance = distribution["provenance"]
    provenance_id = f"pypi-{project}-{version}-provenance"
    _fields(
        provenance,
        {
            "commit": commit,
            "evidence_source_id": provenance_id,
            "repository": REPOSITORY,
            "state": "PYPI_ATTESTED",
            "tag": tag,
        },
        f"{context}.provenance",
    )
    _commit(provenance["commit"], f"{context}.provenance.commit")
    _tag(provenance["tag"], f"{context}.provenance.tag")
    _source_for(
        sources,
        provenance_id,
        "PYPI_PROVENANCE",
        f"{context}.provenance",
        commit=commit,
        project=project,
        repository=REPOSITORY,
        tag=tag,
        version=version,
    )
    expected_constraints = (
        [{"name": "linkml-runtime", "specifier": ">=1.10.0,<2.0.0"}]
        if project == "linkml"
        else []
    )
    if distribution["dependency_constraints"] != expected_constraints:
        raise InventoryError(f"{context}: dependency constraint mismatch")
    return artifact_ids, {metadata_id, provenance_id}


def _validate_release(
    candidate: dict[str, Any],
    context: str,
    sources: dict[str, dict[str, Any]],
    python_ids: set[str],
) -> set[str]:
    _shape(candidate, RELEASE_CANDIDATE, context)
    if not candidate["limitations"]:
        raise InventoryError(f"{context}.limitations: non-empty array required")
    source = candidate["source"]
    commit = _commit(source["commit"], f"{context}.source.commit")
    version = _tag(source["tag"], f"{context}.source.tag")
    if (
        source["repository"] != REPOSITORY
        or source["coordinate_url"] != f"{REPOSITORY}/commit/{commit}"
        or candidate["candidate_id"] != f"linkml-release-v{version}-{commit[:8]}"
    ):
        raise InventoryError(f"{context}.source: immutable release subject mismatch")
    source_ids = {
        f"github-linkml-{commit[:8]}-commit",
        f"github-linkml-{source['tag']}-release",
    }
    if _unique(source["evidence_source_ids"], f"{context}.source") != source_ids:
        raise InventoryError(f"{context}.source: evidence source subject mismatch")
    _source_for(
        sources,
        f"github-linkml-{commit[:8]}-commit",
        "GITHUB_COMMIT",
        f"{context}.source",
        commit=commit,
        repository=REPOSITORY,
    )
    _source_for(
        sources,
        f"github-linkml-{source['tag']}-release",
        "GITHUB_RELEASE",
        f"{context}.source",
        commit=commit,
        repository=REPOSITORY,
        tag=source["tag"],
    )
    if source["archive"]["identity_state"] != "OBSERVED_PUBLISHED_SDISTS":
        raise InventoryError(
            f"{context}.source.archive: observed archive identity required"
        )
    distributions = _map_distributions(
        candidate["distributions"], f"{context}.distributions"
    )
    artifact_ids: set[str] = set()
    distribution_source_ids: set[str] = set()
    for project, distribution in distributions.items():
        artifacts, evidence = _validate_published_distribution(
            project,
            distribution,
            version,
            commit,
            source["tag"],
            sources,
            f"{context}.distributions.{project}",
        )
        artifact_ids |= artifacts
        distribution_source_ids |= evidence
    sdist_ids = {
        artifact_id for artifact_id in artifact_ids if artifact_id.endswith(":sdist")
    }
    if (
        _unique(
            source["archive"]["artifact_ids"], f"{context}.source.archive.artifact_ids"
        )
        != sdist_ids
    ):
        raise InventoryError(
            f"{context}.source.archive: published sdist binding mismatch"
        )
    candidate_python_ids = _candidate_python_ids(candidate, python_ids, context)
    _validate_feasibility(
        candidate,
        "PROBE_READY",
        {("EVIDENCE_SOURCE", item) for item in source_ids | distribution_source_ids}
        | {("PUBLISHED_ARTIFACT", item) for item in artifact_ids}
        | {("PYTHON_CANDIDATE", item) for item in candidate_python_ids},
        set(),
        f"{context}.lock_feasibility",
    )
    return source_ids | distribution_source_ids


def _validate_build_distribution(
    project: str,
    distribution: dict[str, Any],
    commit: str,
    python_ids: set[str],
    context: str,
) -> str:
    target = distribution["wheel_target"]
    build_id = f"build:{commit}:{project}:wheel"
    _fields(
        target,
        {
            "artifact_id": build_id,
            "identity_state": "REQUIRED_FROM_BUILD",
            "kind": "WHEEL",
            "provision": "SOURCE_BUILD_TARGET",
        },
        context,
        "source build target mismatch",
    )
    required = _unique(
        target["required_identity_fields"], f"{context}.required_identity_fields"
    )
    targets = _unique(
        target["target_python_candidate_ids"], f"{context}.target_python_candidate_ids"
    )
    if (
        distribution["source_path"] != PATHS[project]
        or required != {"filename", "wheel_tags", "sha256", "byte_length"}
        or targets != python_ids
    ):
        raise InventoryError(f"{context}: source build target mismatch")
    return build_id


def _validate_source_commit(
    candidate: dict[str, Any],
    context: str,
    sources: dict[str, dict[str, Any]],
    python_ids: set[str],
) -> set[str]:
    _shape(candidate, SOURCE_CANDIDATE, context)
    if not candidate["limitations"]:
        raise InventoryError(f"{context}.limitations: non-empty array required")
    source = candidate["source"]
    commit = _commit(source["commit"], f"{context}.source.commit")
    if (
        source["repository"] != REPOSITORY
        or source["coordinate_url"] != f"{REPOSITORY}/commit/{commit}"
        or candidate["candidate_id"] != f"linkml-source-{commit[:8]}"
    ):
        raise InventoryError(f"{context}.source: immutable source subject mismatch")
    evidence_id = f"github-linkml-{commit[:8]}-commit"
    if source["evidence_source_ids"] != [evidence_id]:
        raise InventoryError(f"{context}.source: evidence source subject mismatch")
    _source_for(
        sources,
        evidence_id,
        "GITHUB_COMMIT",
        f"{context}.source",
        commit=commit,
        repository=REPOSITORY,
    )
    archive = source["archive"]
    if (
        archive["identity_state"] != "REQUIRED_UNOBSERVED"
        or archive["archive_id"] != f"archive:{commit}"
        or archive["evidence_source_id"] != evidence_id
        or archive["locator"] != f"{REPOSITORY}/archive/{commit}.tar.gz"
        or _unique(
            archive["required_identity_fields"],
            f"{context}.source.archive.required_identity_fields",
        )
        != {"sha256", "byte_length"}
    ):
        raise InventoryError(
            f"{context}.source.archive: observed archive or immutable binding mismatch"
        )
    distributions = _map_distributions(
        candidate["distributions"], f"{context}.distributions"
    )
    candidate_python_ids = _candidate_python_ids(candidate, python_ids, context)
    build_ids: set[str] = set()
    for project, distribution in distributions.items():
        build_ids.add(
            _validate_build_distribution(
                project,
                distribution,
                commit,
                candidate_python_ids,
                f"{context}.distributions.{project}",
            )
        )
    _validate_feasibility(
        candidate,
        "PROBE_BLOCKED",
        {("EVIDENCE_SOURCE", evidence_id), ("SOURCE_COMMIT", commit)}
        | {("PYTHON_CANDIDATE", item) for item in candidate_python_ids}
        | {("SOURCE_PATH", item) for item in PATHS.values()},
        {("SOURCE_ARCHIVE_IDENTITY", archive["archive_id"])}
        | {("SOURCE_BUILD_IDENTITY", item) for item in build_ids},
        f"{context}.lock_feasibility",
    )
    return {evidence_id}


def validate_inventory(value: Any) -> None:
    """Validate one parsed inventory, raising ``InventoryError`` on drift."""
    _deny_governance_fields(value)
    _shape(value, ROOT_SPEC, "inventory")
    if (
        value["schema"] != "malleus.contract-compiler.baseline-candidates/v1"
        or value["decision_id"] != "OD-012"
        or value["scope"] != "RESEARCH_INVENTORY"
        or value["authority"]
        != {"decision_authority": "NONE", "production_artifact_authority": "NONE"}
    ):
        raise InventoryError("inventory: exact research-only authority required")
    try:
        if date.fromisoformat(value["audit_date"]).isoformat() != value["audit_date"]:
            raise ValueError
    except ValueError as error:
        raise InventoryError("inventory.audit_date: exact ISO date required") from error
    if not value["limitations"]:
        raise InventoryError("inventory.limitations: non-empty array required")
    sources = _validate_sources(value["sources"])
    repository = value["repository"]
    if repository["url"] != REPOSITORY or repository["layout"] != "MONOREPO":
        raise InventoryError("repository: exact LinkML monorepo required")
    repository_distributions = _map_distributions(
        repository["distributions"], "repository.distributions"
    )
    if any(
        item["source_path"] != PATHS[name]
        for name, item in repository_distributions.items()
    ):
        raise InventoryError("repository.distributions: source path mismatch")
    python_ids: list[str] = []
    referenced_source_ids: set[str] = set()
    for index, item in enumerate(value["python_candidates"]):
        context = f"python_candidates[{index}]"
        version = _version(item["version"], f"{context}.version")
        expected_id = (
            f"cpython-{version}-{item['operating_system'].lower()}-"
            f"{item['architecture']}-{item['abi']}"
        )
        if item["implementation"] != "CPython" or item["candidate_id"] != expected_id:
            raise InventoryError(f"{context}: exact CPython tuple mismatch")
        basis_id = f"python-{version}-release"
        if item["basis_source_id"] != basis_id:
            raise InventoryError(f"{context}.basis_source_id: source subject mismatch")
        _source_for(
            sources,
            basis_id,
            "PYTHON_RELEASE",
            context,
            implementation="CPython",
            version=version,
        )
        referenced_source_ids.add(basis_id)
        python_ids.append(item["candidate_id"])
    python_id_set = _unique(python_ids, "python_candidates")
    candidates = value["candidates"]
    if len(candidates) != 2 or any(not isinstance(item, dict) for item in candidates):
        raise InventoryError(
            "candidates: expected exactly one RELEASE and one SOURCE_COMMIT"
        )
    kinds = [item.get("kind") for item in candidates]
    if kinds.count("RELEASE") != 1 or kinds.count("SOURCE_COMMIT") != 1:
        raise InventoryError(
            "candidates: expected exactly one RELEASE and one SOURCE_COMMIT"
        )
    for index, candidate in enumerate(candidates):
        if candidate["kind"] == "RELEASE":
            referenced_source_ids |= _validate_release(
                candidate, f"candidates[{index}]", sources, python_id_set
            )
        else:
            referenced_source_ids |= _validate_source_commit(
                candidate, f"candidates[{index}]", sources, python_id_set
            )
    if referenced_source_ids != set(sources):
        raise InventoryError("sources: unreferenced or missing official source record")
    if _identity(value) != AUDITED_IDENTITY:
        raise InventoryError(
            "inventory content does not match the audited CC-X00 facts"
        )


def normalize_inventory(value: Any) -> dict[str, Any]:
    """Return the validated value with every declared unordered list sorted."""
    validate_inventory(value)
    return _normalize_valid(value)


def inventory_identity(value: Any) -> str:
    """Return the SHA-256 identity of normalized compact canonical JSON."""
    validate_inventory(value)
    return _identity(value)


def _canonical_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()


def load_inventory(path: Path = DEFAULT_INVENTORY) -> dict[str, Any]:
    """Read and validate canonical inventory bytes without network or writes."""
    try:
        source = path.read_bytes()
        value = json.loads(source, object_pairs_hook=_pairs, parse_constant=_nonfinite)
    except InventoryError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InventoryError(f"{path}: invalid JSON: {error}") from error
    validate_inventory(value)
    normalized = _normalize_valid(value)
    if source != _canonical_bytes(normalized):
        raise InventoryError(f"{path}: inventory bytes are not in canonical order")
    return normalized


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="validate an offline baseline inventory")
    check.add_argument("path", nargs="?", type=Path, default=DEFAULT_INVENTORY)
    arguments = parser.parse_args(argv)
    try:
        inventory = load_inventory(arguments.path)
    except InventoryError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"OK {arguments.path} {inventory_identity(inventory)} "
        f"candidates={len(inventory['candidates'])} "
        f"python_tuples={len(inventory['python_candidates'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

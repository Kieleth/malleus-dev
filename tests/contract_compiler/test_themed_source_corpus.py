"""Source-owner contract for the Quiet Bell Archive LinkML corpus.

These tests validate authored input bytes and their planned semantic deltas. They
do not compile the sources or assert facts, artifacts, diagnostics, or outcomes.
"""

from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
from typing import Any

import pytest
import yaml
from yaml.tokens import (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    DocumentEndToken,
    DocumentStartToken,
    TagToken,
)


REPOSITORY = Path(__file__).resolve().parents[2]
SOURCE_ROOT = (
    REPOSITORY / "conformance" / "contract_kernel" / "v0" / "themed_fixture" / "sources"
)
REQUIREMENTS_PATH = (
    REPOSITORY
    / "conformance"
    / "contract_kernel"
    / "v0"
    / "requirements"
    / "scenarios.json"
)
CC_D14_EVIDENCE_PATH = (
    REPOSITORY / "design" / "contract_compiler" / "overseer" / "evidence" / "CC-D14.json"
)

EXPECTED_SOURCE_FILES = (
    "modules/activity.yaml",
    "modules/entities.yaml",
    "modules/foundation.yaml",
    "v1.0.0/quiet_bell.yaml",
    "v1.0.1/quiet_bell.yaml",
    "v1.1.0/quiet_bell.yaml",
)
VERSION_ROOTS = {
    "1.0.0": "v1.0.0/quiet_bell.yaml",
    "1.0.1": "v1.0.1/quiet_bell.yaml",
    "1.1.0": "v1.1.0/quiet_bell.yaml",
}
EXPECTED_LOCAL_IMPORTS = {
    "modules/activity.yaml": (
        "modules/entities.yaml",
        "modules/foundation.yaml",
    ),
    "modules/entities.yaml": ("modules/foundation.yaml",),
    "modules/foundation.yaml": (),
    "v1.0.0/quiet_bell.yaml": (
        "modules/activity.yaml",
        "modules/entities.yaml",
    ),
    "v1.0.1/quiet_bell.yaml": (
        "modules/activity.yaml",
        "modules/entities.yaml",
    ),
    "v1.1.0/quiet_bell.yaml": (
        "modules/activity.yaml",
        "modules/entities.yaml",
    ),
}
EXTERNAL_IMPORTS = {"linkml:types", "malleus"}
EXPECTED_CONCEPTS = {
    "ArchiveExaminer",
    "CitesFolioRelation",
    "EvidenceFolio",
    "EvidenceLocator",
    "InquiryDossier",
    "SealDiscrepancySignal",
    "SealReviewEvent",
}
SOURCE_CONTRIBUTION_REQUIREMENTS = {
    "closed-composition-delta",
    "linkml-profile-metamorphic",
    "linkml-profile-positive",
}
ATTESTATION = (
    "Luis Guzman Lorenzo is the author and rights holder for the original "
    "Quiet Bell text/data, licensed Apache-2.0"
)
REFUSED_YAML_TOKENS = (
    AliasToken,
    AnchorToken,
    DirectiveToken,
    DocumentEndToken,
    DocumentStartToken,
    TagToken,
)
PRESENTATION_KEYS = {
    "class_uri",
    "description",
    "name",
    "title",
    "uri",
    "version",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that refuses duplicate and non-string mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _assert_json_shaped(value: Any) -> None:
    if isinstance(value, dict):
        if "<<" in value:
            raise ValueError("YAML merge keys are not supported")
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("YAML mapping keys must be strings")
            _assert_json_shaped(item)
        return
    if isinstance(value, list):
        for item in value:
            _assert_json_shaped(item)
        return
    if value is None or type(value) in {bool, int, str}:  # noqa: E721
        return
    if type(value) is float and math.isfinite(value):  # noqa: E721
        return
    raise ValueError(f"source value is not JSON-shaped: {type(value).__name__}")


def _load_source(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not supported")
    if b"\r" in raw:
        raise ValueError("source must use LF line endings")
    if b"\t" in raw:
        raise ValueError("tabs are not supported")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise ValueError("source must end in exactly one LF")

    source = raw.decode("utf-8")
    try:
        tokens = tuple(yaml.scan(source))
    except yaml.YAMLError as error:
        raise ValueError("invalid YAML syntax") from error
    if any(isinstance(token, REFUSED_YAML_TOKENS) for token in tokens):
        raise ValueError("YAML directives, boundaries, anchors, aliases, and tags refuse")

    try:
        documents = list(yaml.load_all(source, Loader=UniqueKeyLoader))
    except yaml.YAMLError as error:
        raise ValueError("invalid YAML syntax") from error
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise ValueError("source must contain exactly one mapping document")
    document = documents[0]
    _assert_json_shaped(document)
    return document


def _documents() -> dict[str, dict[str, Any]]:
    return {
        relative: _load_source(SOURCE_ROOT / relative)
        for relative in EXPECTED_SOURCE_FILES
    }


def _resolved_local_import(source: str, authored: str) -> str | None:
    if authored in EXTERNAL_IMPORTS:
        return None
    resolved = (SOURCE_ROOT / source).parent.joinpath(f"{authored}.yaml").resolve()
    relative = resolved.relative_to(SOURCE_ROOT.resolve())
    return relative.as_posix()


def _local_import_graph(
    documents: dict[str, dict[str, Any]],
) -> dict[str, tuple[str, ...]]:
    return {
        source: tuple(
            sorted(
                resolved
                for authored in document.get("imports", [])
                if (resolved := _resolved_local_import(source, authored)) is not None
            )
        )
        for source, document in documents.items()
    }


def _assert_acyclic(graph: dict[str, tuple[str, ...]]) -> None:
    visited: set[str] = set()
    active: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            raise AssertionError(f"import cycle at {node}")
        if node in visited:
            return
        active.add(node)
        for dependency in graph[node]:
            visit(dependency)
        active.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def _semantic_projection(value: Any, parent_key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {
            key: _semantic_projection(item, key)
            for key, item in value.items()
            if key not in PRESENTATION_KEYS
        }
    if isinstance(value, list):
        projected = [_semantic_projection(item, parent_key) for item in value]
        if parent_key in {"imports", "mixins", "slots"}:
            return sorted(projected)
        return projected
    return value


def _classes_for_baseline(
    documents: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    classes: dict[str, dict[str, Any]] = {}
    for source in (
        "modules/foundation.yaml",
        "modules/entities.yaml",
        "modules/activity.yaml",
        VERSION_ROOTS["1.0.0"],
    ):
        for name, declaration in documents[source].get("classes", {}).items():
            assert name not in classes
            classes[name] = declaration
    return classes


def test_themed_source_membership_and_raw_yaml_are_fixed() -> None:
    members = tuple(
        sorted(
            path.relative_to(SOURCE_ROOT).as_posix()
            for path in SOURCE_ROOT.rglob("*")
            if path.is_file()
        )
    )
    assert members == EXPECTED_SOURCE_FILES
    assert not any(path.is_symlink() for path in SOURCE_ROOT.rglob("*"))

    documents = _documents()
    assert set(documents) == set(EXPECTED_SOURCE_FILES)
    assert all(path.endswith(".yaml") for path in documents)
    assert all(document["id"].startswith("https://malleus.dev/") for document in documents.values())


def test_import_graph_is_one_closed_acyclic_nested_diamond() -> None:
    documents = _documents()
    graph = _local_import_graph(documents)

    assert graph == EXPECTED_LOCAL_IMPORTS
    _assert_acyclic(graph)
    for dependencies in graph.values():
        assert all(dependency in graph for dependency in dependencies)

    foundation = "modules/foundation.yaml"
    entities = "modules/entities.yaml"
    activity = "modules/activity.yaml"
    for root in VERSION_ROOTS.values():
        assert entities in graph[root]
        assert activity in graph[root]
        assert foundation in graph[entities]
        assert foundation in graph[activity]

    authored_external = {
        authored
        for document in documents.values()
        for authored in document.get("imports", [])
        if authored in EXTERNAL_IMPORTS
    }
    assert authored_external == EXTERNAL_IMPORTS


def test_baseline_models_only_the_accepted_quiet_bell_concepts() -> None:
    documents = _documents()
    classes = _classes_for_baseline(documents)

    assert set(classes) == EXPECTED_CONCEPTS
    assert classes["ArchiveExaminer"]["is_a"] == "Entity"
    assert classes["ArchiveExaminer"]["mixins"] == ["Agent"]

    locator = classes["EvidenceLocator"]
    assert locator["exactly_one_of"] == [
        {
            "slot_conditions": {
                "content_digest": {"value_presence": "ABSENT"},
                "shelfmark": {"required": True},
            }
        },
        {
            "slot_conditions": {
                "content_digest": {"required": True},
                "shelfmark": {"value_presence": "ABSENT"},
            }
        },
    ]
    assert classes["EvidenceFolio"]["attributes"]["locator"] == {
        "description": "The folio locator retained inside the folio record.",
        "inlined": True,
        "range": "EvidenceLocator",
        "required": True,
    }

    relation_usage = classes["CitesFolioRelation"]["slot_usage"]
    assert relation_usage["source_id"]["range"] == "InquiryDossier"
    assert relation_usage["target_id"]["range"] == "EvidenceFolio"
    assert relation_usage["relation_type"] == {
        "equals_string": "CITES_FOLIO",
        "range": "ArchiveRelationKind",
        "required": True,
    }
    assert classes["SealReviewEvent"]["slot_usage"]["reviewed_relation"] == {
        "range": "CitesFolioRelation",
        "required": True,
    }
    signal = classes["SealDiscrepancySignal"]
    assert "bearer_id" not in signal.get("slot_usage", {})
    assert signal["slot_usage"]["signal_type"] == {
        "equals_string": "SEAL_DISCREPANCY",
        "range": "ArchiveSignalKind",
        "required": True,
    }

    foundation = documents["modules/foundation.yaml"]
    assert foundation["types"]["ArchiveShelfmark"]["typeof"] == "string"
    assert foundation["enums"] == {
        "ArchiveEventKind": {"permissible_values": {"SEAL_REVIEW": None}},
        "ArchiveRelationKind": {"permissible_values": {"CITES_FOLIO": None}},
        "ArchiveSignalKind": {"permissible_values": {"SEAL_DISCREPANCY": None}},
    }
    assert foundation["slots"]["certainty"] == {
        "description": "Confidence assigned to a discrepancy on the closed zero-to-one scale.",
        "maximum_value": 1,
        "minimum_value": 0,
        "range": "float",
    }


def test_versions_encode_presentation_invariance_and_one_optional_field_delta() -> None:
    documents = _documents()
    baseline = documents[VERSION_ROOTS["1.0.0"]]
    presentation = documents[VERSION_ROOTS["1.0.1"]]
    additive = deepcopy(documents[VERSION_ROOTS["1.1.0"]])

    assert baseline["version"] == "1.0.0"
    assert presentation["version"] == "1.0.1"
    assert additive["version"] == "1.1.0"
    assert (SOURCE_ROOT / VERSION_ROOTS["1.0.0"]).read_bytes() != (
        SOURCE_ROOT / VERSION_ROOTS["1.0.1"]
    ).read_bytes()
    assert _semantic_projection(baseline) == _semantic_projection(presentation)

    assert additive["slots"].pop("marginal_note") == {
        "description": "Optional examiner note retained beside the dossier.",
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "range": "string",
        "required": False,
    }
    additive["classes"]["InquiryDossier"]["slots"].remove("marginal_note")
    assert _semantic_projection(baseline) == _semantic_projection(additive)


def test_source_contribution_is_bound_to_requirements_without_claiming_outcomes() -> None:
    requirements = json.loads(REQUIREMENTS_PATH.read_text(encoding="utf-8"))
    requirement_ids = {
        requirement["requirement_id"]
        for scenario in requirements["scenarios"]
        for requirement in scenario["requirements"]
    }
    assert SOURCE_CONTRIBUTION_REQUIREMENTS < requirement_ids

    serialized = json.dumps(_documents(), sort_keys=True)
    for forbidden in (
        "canonical_facts",
        "diagnostic_code",
        "expected_artifact",
        "expected_facts",
        "expected_outcome",
        "operation_trace",
        "oracle",
    ):
        assert forbidden not in serialized


def test_source_text_is_bound_to_the_accepted_authorship_boundary() -> None:
    evidence = json.loads(CC_D14_EVIDENCE_PATH.read_text(encoding="utf-8"))
    checks = {check["check_id"]: check for check in evidence["checks"]}

    assert checks["ccd14-attestation"] == {
        "check_id": "ccd14-attestation",
        "method": (
            "Compare the recorded operator attestation byte-for-byte across decision "
            "prose, conformance prose, and graph literal."
        ),
        "observed": ATTESTATION,
        "result": "PASS",
    }
    assert evidence["limitations"][0] == (
        "The attestation covers original Quiet Bell text/data only and no visual asset."
    )


@pytest.mark.parametrize(
    "source",
    [
        "id: https://malleus.dev/example\nid: https://malleus.dev/duplicate\n",
        "id: https://malleus.dev/example\nclasses:\n  Record: {}\n  Record: {}\n",
    ],
)
def test_test_loader_refuses_duplicate_root_and_nested_keys(
    tmp_path: Path, source: str
) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError, match="^duplicate YAML key: "):
        _load_source(path)


@pytest.mark.parametrize(
    "source",
    [
        "%YAML 1.2\nid: https://malleus.dev/example\n",
        "---\nid: https://malleus.dev/example\n",
        "id: &identity https://malleus.dev/example\nname: *identity\n",
        "id: !!str https://malleus.dev/example\n",
        "id: https://malleus.dev/example\ncreated: 2026-08-28\n",
    ],
)
def test_test_loader_refuses_non_json_yaml_features(
    tmp_path: Path, source: str
) -> None:
    path = tmp_path / "unsupported.yaml"
    path.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError):
        _load_source(path)

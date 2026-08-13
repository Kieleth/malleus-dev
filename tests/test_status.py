"""Mechanical checks for the published implementation boundary."""

import re
from pathlib import Path

import yaml

import malleus
from malleus.status import IMPLEMENTATION_STATUS


ROOT = Path(__file__).parent.parent


def test_package_runtime_and_project_versions_match():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = pyproject.split("[project]", 1)[1]
    version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)
    assert version is not None
    assert version.group(1) == malleus.__version__ == IMPLEMENTATION_STATUS.package_version


def test_stage_four_boundary_is_explicit():
    assert IMPLEMENTATION_STATUS.current_stage == "4"
    assert IMPLEMENTATION_STATUS.boundary == "stage-4-structural-staging"
    assert IMPLEMENTATION_STATUS.completed_stages == ("2", "3", "7a", "4")
    assert "isolated-proposed-subgraph-staging" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "assent-gated-materialization" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "general-graph-to-prolog-compilation" in IMPLEMENTATION_STATUS.pending_capabilities


def test_ontology_versions_match_status_boundary():
    root = yaml.safe_load((ROOT / "ontology" / "malleus.yaml").read_text(encoding="utf-8"))
    assent = yaml.safe_load((ROOT / "ontology" / "assent.yaml").read_text(encoding="utf-8"))
    assert root["version"] == IMPLEMENTATION_STATUS.root_ontology_version
    assert assent["version"] == IMPLEMENTATION_STATUS.assent_ontology_version


def test_status_document_names_current_version_and_boundary():
    document = (ROOT / "docs" / "IMPLEMENTATION_STATUS.md").read_text(encoding="utf-8")
    assert f"version `{IMPLEMENTATION_STATUS.package_version}`" in document
    assert f"`{IMPLEMENTATION_STATUS.boundary}`" in document
    for capability in IMPLEMENTATION_STATUS.pending_capabilities:
        assert f"`{capability}`" in document

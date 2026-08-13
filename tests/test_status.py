"""Mechanical checks for the published implementation boundary."""

import re
from pathlib import Path

import yaml

import malleus
from malleus.logic import LogicContract
from malleus.status import IMPLEMENTATION_STATUS


ROOT = Path(__file__).parent.parent


def test_package_runtime_and_project_versions_match():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = pyproject.split("[project]", 1)[1]
    version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)
    assert version is not None
    assert version.group(1) == malleus.__version__ == IMPLEMENTATION_STATUS.package_version


def test_stage_seven_b_boundary_is_explicit():
    assert IMPLEMENTATION_STATUS.current_stage == "7b"
    assert (
        IMPLEMENTATION_STATUS.boundary
        == "stage-7b-assent-gated-bitemporal-accepted-graph"
    )
    assert IMPLEMENTATION_STATUS.completed_stages == (
        "2",
        "3",
        "7a",
        "4",
        "5",
        "6",
        "7b",
    )
    assert "isolated-proposed-subgraph-staging" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "failure-atomic-ledger-replacement" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "general-graph-to-prolog-compilation" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "logic-monitor-failure-to-unknown" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "typed-monitor-specifications" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "proposal-bound-epistemic-policy" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "exact-required-monitor-coverage" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "single-output-per-monitor-context" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "single-logic-check-per-monitor-context" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "closed-core-assessment-contracts" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "deterministic-epistemic-control-selection" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "proposal-candidate-semantic-binding" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "atomic-assent-gated-materialization" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "accepted-graph-projection" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "bitemporal-as-of-replay" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "portable-graph-base-resolution" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "untrusted-rule-program-sandboxing" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "epistemic-policy-authority-and-scope" in IMPLEMENTATION_STATUS.pending_capabilities


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


def test_stage_five_example_contract_and_rules_remain_distribution_inputs():
    contract_path = ROOT / "prolog" / "cyp450_logic.yaml"
    rules_path = ROOT / "prolog" / "cyp450_rules.pl"
    assert contract_path.is_file()
    assert rules_path.is_file()
    contract = LogicContract.load(contract_path)
    assert contract.rules_path == rules_path.resolve()

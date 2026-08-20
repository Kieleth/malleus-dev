"""Mechanical checks for the published implementation boundary."""

import re
from pathlib import Path

import yaml

import malleus
from malleus.logic import LogicContract
from malleus.status import IMPLEMENTATION_STATUS


ROOT = Path(__file__).parent.parent


def test_suite_imports_malleus_from_this_checkout():
    package = Path(malleus.__file__).resolve()
    source = (ROOT / "src").resolve()
    assert package.is_relative_to(source), f"imported Malleus outside this checkout: {package}"


def test_package_runtime_and_project_versions_match():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = pyproject.split("[project]", 1)[1]
    version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)
    assert version is not None
    assert version.group(1) == malleus.__version__ == IMPLEMENTATION_STATUS.package_version


def test_stage_eight_c_boundary_is_explicit():
    assert IMPLEMENTATION_STATUS.current_stage == "8c"
    assert (
        IMPLEMENTATION_STATUS.boundary
        == "stage-8c-executable-provenance-and-effect-closure"
    )
    assert IMPLEMENTATION_STATUS.completed_stages == (
        "2",
        "3",
        "7a",
        "4",
        "5",
        "6",
        "7b",
        "7c",
        "8a",
        "8b",
        "8c",
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
    assert "precision-aware-valid-time-boundaries" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "iana-timezone-calendar-day-enforcement" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "three-valued-valid-time-projection" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "indeterminacy-reason-commitments" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "typed-authorization-policies" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "action-bound-authorization-policy" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "evidence-assertion-recording" in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "content-addressed-source-artifacts" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "epistemic-monitor-adapter-orchestration" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "authorized-action-dispatch-recording" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "independent-outcome-observation-recording" in (
        IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert (
        "deterministic-authorization-control-selection"
        in IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert (
        "authority-monitor-failure-to-clarify"
        in IMPLEMENTATION_STATUS.implemented_capabilities
    )
    assert "portable-graph-base-resolution" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "untrusted-rule-program-sandboxing" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "epistemic-policy-authority-and-scope" in IMPLEMENTATION_STATUS.pending_capabilities
    assert "authorization-policy-authority-and-scope" in (
        IMPLEMENTATION_STATUS.pending_capabilities
    )
    assert "exactly-once-effect-delivery-profile" in (
        IMPLEMENTATION_STATUS.pending_capabilities
    )


def test_011_release_keeps_the_core_stage_boundary():
    assert IMPLEMENTATION_STATUS.package_version == "0.13.1"
    assert IMPLEMENTATION_STATUS.current_stage == "8c"
    assert {
        "typed-literature-review-ledger",
        "evidence-linked-literature-comparison",
        "deterministic-recon-artifact-builds",
        "legacy-literature-kg-v1-import",
    } <= set(IMPLEMENTATION_STATUS.implemented_capabilities)
    assert "graph-recipe" not in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "contract-frontend" not in IMPLEMENTATION_STATUS.implemented_capabilities
    assert "historical-timezone-database-migration" in (
        IMPLEMENTATION_STATUS.pending_capabilities
    )
    assert "dependency-closed-valid-time-projection" in (
        IMPLEMENTATION_STATUS.pending_capabilities
    )


def test_capability_status_sets_are_unique_and_disjoint():
    implemented = IMPLEMENTATION_STATUS.implemented_capabilities
    pending = IMPLEMENTATION_STATUS.pending_capabilities
    assert len(implemented) == len(set(implemented))
    assert len(pending) == len(set(pending))
    assert set(implemented).isdisjoint(pending)


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


def test_readme_names_current_version_and_boundary():
    document = (ROOT / "README.md").read_text(encoding="utf-8")
    assert (
        f"Current package boundary: `{IMPLEMENTATION_STATUS.package_version}`, "
        f"`{IMPLEMENTATION_STATUS.boundary}`"
    ) in document


def test_stage_five_example_contract_and_rules_remain_distribution_inputs():
    contract_path = ROOT / "prolog" / "cyp450_logic.yaml"
    rules_path = ROOT / "prolog" / "cyp450_rules.pl"
    assert contract_path.is_file()
    assert rules_path.is_file()
    contract = LogicContract.load(contract_path)
    assert contract.rules_path == rules_path.resolve()

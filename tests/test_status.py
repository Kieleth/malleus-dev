"""Mechanical checks for the published implementation boundary."""

import re
from pathlib import Path

import yaml

import malleus
from malleus.assent import PAYLOAD_FIELDS, EventType, ProtocolLedger
from malleus.logic import LogicContract
from malleus.status import IMPLEMENTATION_STATUS


ROOT = Path(__file__).parent.parent
SKILL_ROOT = ROOT / ".claude" / "skills"


def _labelled_skill_items(text: str) -> dict[str, str]:
    """Read stable contract labels without depending on section prose."""
    items: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^(?:\d+\.|-) `([A-Z][A-Z0-9_]*)`: (.+)$", line)
        if match:
            current = match.group(1)
            assert current not in items, f"duplicate skill contract label: {current}"
            items[current] = [match.group(2)]
        elif current is not None and line.startswith(("  ", "   ")):
            items[current].append(line.strip())
        else:
            current = None
    return {label: " ".join(lines) for label, lines in items.items()}


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
    assert "review-report-recording" in IMPLEMENTATION_STATUS.implemented_capabilities
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
    assert IMPLEMENTATION_STATUS.package_version == "0.13.3"
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


def test_shipped_protocol_doors_cannot_remain_pending():
    """A machine-visible event door must agree with the status boundary."""
    shipped_doors = {
        "review-report-recording": (
            EventType.REVIEW_RECORDED,
            {"report", "findings"},
            "_review_report",
        ),
    }

    implemented = set(IMPLEMENTATION_STATUS.implemented_capabilities)
    pending = set(IMPLEMENTATION_STATUS.pending_capabilities)
    for capability, (event_type, payload_fields, handler_name) in shipped_doors.items():
        assert PAYLOAD_FIELDS[event_type] == payload_fields
        assert callable(getattr(ProtocolLedger, handler_name, None))
        assert capability in implemented
        assert capability not in pending


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
    assert "`review-report-recording`" in document
    assert "one atomic report" in document
    assert "`MigrationReceipt` records" in document
    assert "The receipt is not a protocol-ledger boundary event" in document


def test_readme_names_current_version_and_boundary():
    document = " ".join(
        (ROOT / "README.md").read_text(encoding="utf-8").split()
    )
    assert (
        "For maintainers, the current machine-checked package boundary is "
        f"`{IMPLEMENTATION_STATUS.package_version}`, "
        f"`{IMPLEMENTATION_STATUS.boundary}`"
    ) in document


def test_stage_five_example_contract_and_rules_remain_distribution_inputs():
    contract_path = ROOT / "prolog" / "cyp450_logic.yaml"
    rules_path = ROOT / "prolog" / "cyp450_rules.pl"
    assert contract_path.is_file()
    assert rules_path.is_file()
    contract = LogicContract.load(contract_path)
    assert contract.rules_path == rules_path.resolve()


def test_recon_skill_transfers_evidence_without_promoting_it():
    skill_dir = SKILL_ROOT / "malleus-recon"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(skill.split("---", 2)[1])
    agent = yaml.safe_load(
        (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )["interface"]
    items = _labelled_skill_items(skill)

    assert "literature-to-design" in metadata["description"].lower()
    assert all(
        disposition in skill
        for disposition in ("`ADOPT`", "`COMPOSE`", "`REFUSE`", "`DEFER`")
    )
    expected_items = (
        "SOURCE_MECHANISM",
        "ASSUMPTIONS_AND_THREAT_MODEL",
        "REUSABLE_TECHNIQUE",
        "FAILURE_BASELINE_OR_ORACLE",
        "TARGET_BOUNDARY",
        "EXCLUDED_TRANSFER",
        "SMALLEST_EMPIRICAL_TEST",
    )
    assert all(label in items for label in expected_items)
    source = items["SOURCE_MECHANISM"].lower()
    assert re.search(r"applicable work, claim, and evidence records", source)
    assert re.search(r"result record only when the source establishes one", source)
    assert re.search(r"no result was established, say so explicitly", source)
    boundary = items["TARGET_BOUNDARY"].lower()
    assert re.search(r"existing malleus role or boundary and current consumer", boundary)
    assert re.search(r"if neither exists.*inventing an extension point", boundary)
    prompt = agent["default_prompt"].lower()
    assert "$malleus-recon" in prompt
    assert all(word in prompt for word in ("adopt", "compose", "refuse", "defer"))


def test_malleus_dev_skill_gates_research_and_projection_claims():
    skill = (SKILL_ROOT / "malleus-dev" / "SKILL.md").read_text(encoding="utf-8")
    items = _labelled_skill_items(skill)

    assert all(
        category in items["USE_CLASSIFICATION"]
        for category in (
            "`DESIGN_CONSTRAINT`",
            "`BASELINE_OR_ORACLE`",
            "`CONFORMANCE_FIXTURE`",
            "`IMPLEMENTATION_CANDIDATE`",
            "`EXPLICIT_EXCLUSION`",
        )
    )
    assert all(
        state in items["MATURITY"]
        for state in ("`PROPOSED`", "`ACCEPTED`", "`IMPLEMENTED`")
    )
    role = items["ROLE_AND_CONSUMER"].lower()
    assert re.search(r"existing protocol role or boundary.*current concrete consumer", role)
    promotion = items["CORE_PROMOTION"].lower()
    assert re.search(r"generic core waits for a second independent consumer", promotion)

    inheritance = items["LITERATURE_INHERITANCE"].lower()
    assert all(
        role in inheritance
        for role in (
            "inherited foundations",
            "empirical corroboration",
            "sources of techniques and baselines",
        )
    )
    assert re.search(r"do not organize.*being first to.*ingredient", inheritance)
    assert all(
        contribution in inheritance
        for contribution in (
            "composed protocol",
            "component interactions",
            "measured results",
        )
    )

    integrity = items["MODULAR_INTEGRITY"].lower()
    assert re.search(
        r"replaceable integrity contract.*committed protocol-ledger head", integrity
    )
    assert all(
        layer in integrity
        for layer in (
            "ontology",
            "admission",
            "assent",
            "temporal projection",
            "kg semantics",
        )
    )
    assert re.search(r"must not couple", integrity)
    assert all(
        boundary in integrity
        for boundary in (
            "integrity profile",
            "persisted-wire epoch",
            "not a new semantic protocol",
        )
    )

    closure = items["DERIVATION_CLOSURE"].lower()
    closure_commitments = (
        "accepted canonical graph-state identity",
        "initial-empty-state identity and retained genesis change-set-set digest",
        "verified selected-prefix identity and checkpoint",
        "effective contract and composition",
        "reader identity",
        "projector implementation and projection profile",
        "interpretation profile",
        "declared side inputs",
        "transaction-time and valid-time coordinates",
        "output digest",
    )
    assert all(commitment in closure for commitment in closure_commitments)
    assert re.search(r"graph-state identity identifies accepted semantic state", closure)
    assert re.search(r"output digest identifies the derived projection result", closure)
    assert "keep them distinct" in closure
    assert "initial-base identity" not in closure

    authority = items["AUTHORITY"].lower()
    assert re.search(r"no independent governed write path", authority)
    assert re.search(r"define explicit reconciliation.*mere projection", authority)
    refusal = items["REFUSAL"].lower()
    assert re.search(r"typed refusal before any derived state", refusal)
    assert re.search(
        r"full replay and incremental replay converge.*canonical logical state",
        items["REPLAY_CONVERGENCE"].lower(),
    )
    assert re.search(
        r"deleting the derived store and rebuilding it.*same state",
        items["REBUILD_CONVERGENCE"].lower(),
    )
    assert re.search(
        r"different conforming projector.*same fixtures.*replaceability",
        items["REPLACEABILITY"].lower(),
    )

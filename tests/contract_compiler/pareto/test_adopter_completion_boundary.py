"""Installed guidance delivery and capture accounting, not semantic evaluation."""

from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as api
from malleus.inquisition.cli import main as inquisitor
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _generic_compilation,
)


ROOT = Path(__file__).resolve().parents[3]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def test_installed_coordinator_reaches_shared_adopter_completion_guidance(tmp_path):
    assert (
        inquisitor(["install-skills", "--agent", "codex", "--project", str(tmp_path)])
        == 0
    )
    skills = tmp_path / ".codex" / "skills"
    for name in ("malleus-dev", "malleus-acolyte"):
        assert (skills / name / "SKILL.md").read_bytes() == (
            ROOT / ".claude" / "skills" / name / "SKILL.md"
        ).read_bytes()
    coordinator = (skills / "malleus-dev" / "SKILL.md").read_text()
    prelaunch = coordinator.split("## Before you build: bind the slice", 1)[1].split(
        "\n## ", 1
    )[0]
    reference = "../malleus-acolyte/SKILL.md#outcome-and-permission-check"
    assert f"]({reference})" in prelaunch
    target, fragment = reference.split("#")
    instructions = (skills / "malleus-dev" / target).read_text()
    headings = {
        line.removeprefix("## ").lower().replace(" ", "-")
        for line in instructions.splitlines()
        if line.startswith("## ")
    }
    assert fragment in headings


def test_installed_guidance_delivers_progressive_review_obligations(tmp_path):
    # This protects instruction delivery only, not review behavior or truth.
    assert (
        inquisitor(["install-skills", "--agent", "codex", "--project", str(tmp_path)])
        == 0
    )
    installed = tmp_path / ".codex/skills/malleus-acolyte/SKILL.md"
    source = ROOT / ".claude/skills/malleus-acolyte/SKILL.md"
    assert installed.read_bytes() == source.read_bytes()
    text = installed.read_text()
    heading = "### Maintaining interpretations as evidence accumulates"
    assert text.count(heading) == 1
    section = text.split(heading, 1)[1].split("\n## ", 1)[0]
    prose = " ".join(section.split())
    for requirement in (
        "declared reading or evidence-change boundary",
        "bounded set of interpretation IDs and versions",
        "including interpretations previously considered complete",
        "review the whole declared set",
        "supported correction",
        "justified no-change",
        "conflict",
        "specific unresolved disposition",
        "Missing or stale required reviews prevent a completion claim",
        "does not resolve the knowledge gap",
        "Retry exhaustion and inventory completion are not semantic completion",
        "Evidence receipt and review alone change no accepted knowledge",
        "selected admission policy",
        "Reading order is not world time",
        "This guidance is not a mechanical completion checker",
    ):
        assert requirement in prose


def test_installed_acquisition_routes_share_one_review_rule(tmp_path):
    assert (
        inquisitor(["install-skills", "--agent", "codex", "--project", str(tmp_path)])
        == 0
    )
    skills = tmp_path / ".codex/skills"
    acolyte = (skills / "malleus-acolyte/SKILL.md").read_text()
    development = (skills / "malleus-dev/SKILL.md").read_text()
    fragment = "maintaining-interpretations-as-evidence-accumulates"
    local_link = f"](#{fragment})"
    document_loop = acolyte.split("9. **Grow only from recorded gaps.**", 1)[1].split(
        "10. **Stop honestly.**", 1
    )[0]
    structured = acolyte.split("### Current structured-source plan template", 1)[1]
    assert local_link in document_loop
    assert "structural schema growth, not the scope of interpretation review" in (
        " ".join(document_loop.split())
    )
    assert local_link in structured
    reference = f"../malleus-acolyte/SKILL.md#{fragment}"
    prelaunch = development.split("## Before you build: bind the slice", 1)[1].split(
        "\n## ", 1
    )[0]
    assert f"]({reference})" in prelaunch
    target, anchor = reference.split("#")
    resolved = (skills / "malleus-dev" / target).read_text()
    headings = {
        line.removeprefix("### ").lower().replace(" ", "-")
        for line in resolved.splitlines()
        if line.startswith("### ")
    }
    assert anchor in headings


def test_installed_guidance_names_the_real_optional_review_check(tmp_path):
    import inspect
    import malleus.acquisition as acquisition

    assert inquisitor(
        ["install-skills", "--agent", "codex", "--project", str(tmp_path)]
    ) == 0
    text = (tmp_path / ".codex/skills/malleus-acolyte/SKILL.md").read_text()
    section = text.split(
        "### Maintaining interpretations as evidence accumulates", 1
    )[1].split("\n## ", 1)[0]
    assert "malleus.acquisition.check_review_coverage" in section
    for argument in inspect.signature(acquisition.check_review_coverage).parameters:
        assert f"`{argument}`" in section
    assert "`result.require_complete()`" in section
    assert callable(acquisition.ReviewCoverage.require_complete)
    assert "REVIEW_COVERAGE_PROFILE" in section
    assert isinstance(acquisition.REVIEW_COVERAGE_PROFILE, bytes)
    assert "This does not judge the rationale" in section


def test_complete_block_inventory_can_still_be_an_unresolved_no_change_plan():
    # Task permissions are adopter input, not something this compiler checks.
    # This literal reason records the obstacle; it is not a new decision schema.
    gap = {
        "kind": "RELATION_ABSENT",
        "statement": (
            "ObjectLink(source_id=object:A, target_id=object:B) is unresolved. "
            "The source says A links to B, but this attempt prohibits relationship "
            "edits. Permission to add that relationship is required."
        ),
    }
    reading = canonical(
        {"pages": [{"blocks": [{"id": "b", "ordinal": 0, "text": "A links to B."}]}]}
    )
    capture = canonical(
        {
            "schema": api.DOCUMENT_CAPTURE_GRAMMAR,
            "reading_sha256": "sha256:" + sha256(reading).hexdigest(),
            "attribution": {
                "author": "Synthetic source",
                "date": "2026-01-01",
                "source_id": "source:neutral",
            },
            "nothing_assertable": [],
            "assertions": [
                {
                    "id": "assertion:link",
                    "block": "b",
                    "statement": "A links to B.",
                    "modality": "STATED",
                    "formalized_by": [],
                    "gaps": [gap],
                }
            ],
        }
    )
    compiled = _generic_compilation()
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    adapted = api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=capture,
        capture_id="capture:neutral",
        plan_id="plan:neutral",
        contract_identity=partial.identity,
        contract_view=compiled.view,
        records={"entities": [], "relations": []},
        supersessions=[],
    )
    census = json.loads(adapted.canonical_census_bytes)
    assert census["blocks_reviewed"] == 1
    assert census["assertions"] == {
        "FULLY_FORMALIZED": 0,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 1,
    }
    plan = json.loads(adapted.canonical_plan_bytes)
    assert len(plan["gaps"]) == 1
    assert {key: plan["gaps"][0][key] for key in gap} == gap
    assert adapted.capture_bytes == capture
    result = api.compile_population_plan(
        plan,
        partial_contract=partial,
        contract_view=compiled.view,
        base_state=api.PopulationBaseState.empty(),
        history_profile=api.SOURCE_ASSERTION_PROFILE,
    )
    assert result.status is api.PopulationPlanStatus.NO_DOMAIN_CHANGE
    assert result.operations == ()

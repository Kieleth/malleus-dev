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

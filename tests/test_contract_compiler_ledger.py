from __future__ import annotations

import hashlib
import json
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import yaml
from markdown_it import MarkdownIt
from rdflib import Graph, Literal, URIRef
from rdflib.exceptions import ParserError
from rdflib.plugins.parsers.notation3 import BadSyntax

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.contract_compiler_ledger import (  # noqa: E402
    LedgerValidationError,
    canonical_json,
    entry_hash,
    load_ledger,
    render_status,
    verify_evidence_snapshot,
)
from scripts.contract_compiler_integration import (  # noqa: E402
    validate_candidate_history,
)


OVERSEER = ROOT / "design" / "contract_compiler" / "overseer"
STEADY_STATE_WORKFLOWS = (
    ROOT / ".github" / "workflows" / "tests.yml",
    ROOT / ".github" / "workflows" / "release.yml",
)
CC002_CARD = (
    ROOT / "design" / "contract_compiler" / "workstreams" / "CC-002" / "manifest.json"
)
INTEGRATION = ROOT / "design" / "contract_compiler" / "integration.json"
GOVERNANCE_BASE_COMMIT = "6325bd962ecfd00bd4ca62b1d9febd07e3737357"
R3_GOVERNANCE_BASE_COMMIT = "a3d2d644fa92ae6d59bff0cc5a422557d35afe85"
CC002_CHECKPOINT_LINEAGE = (
    "a7a65ccfdd7afd7d42a40509631fcdfef49f135e",
    "4cbf79c287b7fdc3c21beda3869bd45b3835d8f4",
    "a48c754ae6a7aa904c3317d3cdde06de6db8ff98",
    GOVERNANCE_BASE_COMMIT,
)
CC002_SELECTION_COMMIT = "fc23888e012b0771289b5006ccd9a74945db2220"
CC002_LINEAGE_CONTRACT = (
    "Bind the four governed historical worker checkpoints as final-byte evidence "
    "only: a7a65ccfdd7afd7d42a40509631fcdfef49f135e, "
    "4cbf79c287b7fdc3c21beda3869bd45b3835d8f4, "
    "a48c754ae6a7aa904c3317d3cdde06de6db8ff98, and "
    "6325bd962ecfd00bd4ca62b1d9febd07e3737357."
)
FOUNDATION_PROJECTIONS = (
    ROOT / "design" / "PROTOCOL_FOUNDATION_GRAPH.md",
    ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md",
    ROOT / "design" / "GRAPH_RECIPE_OTTR_PROFILE.md",
    ROOT / "design" / "GRAPH_REALIZATION_SESSION_CHECKPOINT.md",
    ROOT / "design" / "GRAPH_RECIPE_TDD_EXPERIMENTS.md",
)
HISTORICAL_CCD12_PATHS = (
    "design/contract_compiler/overseer/entries/OVR-000050.json",
    "design/contract_compiler/overseer/entries/OVR-000053.json",
    "design/contract_compiler/overseer/entries/OVR-000054.json",
    "design/contract_compiler/overseer/evidence/CC-D12.json",
    "design/contract_compiler/workstreams/CC-D12/manifest.json",
)
HISTORICAL_R3_PATHS = (
    *(
        f"design/contract_compiler/overseer/entries/OVR-{sequence:06d}.json"
        for sequence in range(58, 69)
    ),
    "design/contract_compiler/overseer/evidence/CC-D12-R2.json",
    "design/contract_compiler/overseer/evidence/CC-002-progress-01.json",
)
OD005_HEADING = "### OD-005: logical fact record and canonical bytes"
OD005_NEXT_HEADING = "### OD-011: resolver and import policy"
OD005_SEED_TABLE_HEADER = (
    "Subject kind",
    "Predicate",
    "Object type or target",
    "Cardinality",
)
OD005_SEED_ROWS = (
    ("`Class`", "`rdf:type`", "exactly `Class`", "1"),
    ("`Class`", "`rdfs:subClassOf`", "`Class`", "0..1"),
    ("`Class`", "`cf:isMixin`", "Boolean", "1"),
    (
        "`Class`",
        "`cf:usesMixin`",
        "distinct `Class` with `isMixin=true`",
        "0..*",
    ),
    ("`Class`", "`cf:abstract`", "Boolean", "1"),
    ("`Slot`", "`rdf:type`", "exactly `Slot`", "1"),
    (
        "`Slot`, `SlotUse`",
        "`cf:valueRange`",
        "`Class`, `Enum`, `Scalar`, or `SeedPrimitive`",
        "1",
    ),
    ("`Slot`, `SlotUse`", "`cf:required`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:multivalued`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:identifier`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:inlined`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:equalsString`", "string", "0..1"),
    (
        "`Slot`, `SlotUse`",
        "`cf:minimum`",
        "canonical decimal lexical string",
        "0..1",
    ),
    (
        "`Slot`, `SlotUse`",
        "`cf:maximum`",
        "canonical decimal lexical string",
        "0..1",
    ),
    (
        "`Slot`, `SlotUse`",
        "`cf:valuePresence`",
        "string `PRESENT` or `ABSENT`",
        "0..1",
    ),
    ("`SlotUse`", "`rdf:type`", "exactly `SlotUse`", "1"),
    ("`SlotUse`", "`cf:onClass`", "`Class`", "1"),
    ("`SlotUse`", "`cf:usesSlot`", "`Slot`", "1"),
    ("`Enum`", "`rdf:type`", "exactly `Enum`", "1"),
    ("`Enum`", "`cf:enumValue`", "distinct string", "0..*"),
    ("`Scalar`", "`rdf:type`", "exactly `Scalar`", "1"),
    ("`Scalar`", "`cf:typeof`", "`Scalar` or `SeedPrimitive`", "1"),
)
OD005_SEED_PRIMITIVES = ("String", "Integer", "Float", "Boolean", "DateTime")
IMMUTABLE_R3_REFINEMENT_INPUTS = {
    "design/contract_compiler/overseer/entries/OVR-000069.json": "3f1f72dbb437fbbf2e1aad2dfaeec213884228f169330361e513c6af700ad910",
    "design/contract_compiler/overseer/entries/OVR-000070.json": "011f1ccef652b5299b23aa4588edd66dacc2802a0ed2fb0370669a6b5c1747ce",
    "design/contract_compiler/overseer/entries/OVR-000071.json": "62c93ddd39554c47af605923c4ab7f428ed87f5694c4600d834fbe70f31396e3",
    "design/contract_compiler/overseer/entries/OVR-000072.json": "095ceccda8ddc22a29cb3481da41bce52a9f53ea2a61b61c361db0a7ebcef0bb",
    "design/contract_compiler/overseer/entries/OVR-000073.json": "b5867998fafe3dc2649b251819145f032d456d7b54c07ee807de57c67e4694eb",
    "design/contract_compiler/overseer/entries/OVR-000074.json": "30de0203fee9a3c6ae25a0ede22b573e70c19f73b1bdd6601f88cab6a74cbc8f",
    "design/contract_compiler/overseer/entries/OVR-000075.json": "64b4d744cfe491df70dfa3c4d18d9944654a620eeb05ac888475cd2ab3a07da2",
    "design/contract_compiler/overseer/entries/OVR-000076.json": "fbac3bceeee378bd2f5fe5c9633fabedfc636170c2d212a9ce717ae09d4fdf41",
    "design/contract_compiler/overseer/entries/OVR-000077.json": "b57a83e46bb2e015a62715a02c251a763ec1c3ed4aace4394f9e85b320ab0cef",
    "design/contract_compiler/overseer/evidence/CC-D12-R3.json": "1f4e71eb7c0f3dac0be5bf6bd8e633dfc6975979e5756796631cf014320c3bd9",
}


def _od005_section(decisions: str) -> str:
    assert decisions.count(OD005_HEADING) == 1
    assert decisions.count(OD005_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD005_HEADING, 1)
    section, after = section_and_after.split(OD005_NEXT_HEADING, 1)
    assert OD005_NEXT_HEADING not in before
    assert OD005_HEADING not in after
    return section


def _od005_seed_table_rows(section: str) -> tuple[tuple[str, ...], ...]:
    tokens = MarkdownIt("commonmark").enable("table").parse(section)
    assert sum(token.type == "table_open" for token in tokens) == 1
    rows: list[tuple[str, ...]] = []
    row: list[str] | None = None
    in_table = False
    for token in tokens:
        if token.type == "table_open":
            in_table = True
        elif token.type == "table_close":
            in_table = False
        elif in_table and token.type == "tr_open":
            assert row is None
            row = []
        elif in_table and token.type == "inline":
            assert row is not None
            row.append(token.content)
        elif in_table and token.type == "tr_close":
            assert row is not None
            rows.append(tuple(row))
            row = None
    assert not in_table and row is None
    assert rows[0] == OD005_SEED_TABLE_HEADER
    assert all(len(current) == len(OD005_SEED_TABLE_HEADER) for current in rows)
    return tuple(rows[1:])


def _od005_seed_primitives(section: str) -> tuple[str, ...]:
    lead = "The five trusted `SeedPrimitive` target IRIs are exactly "
    tail = " under the seed namespace."
    paragraphs = tuple(" ".join(part.split()) for part in section.split("\n\n"))
    declarations = tuple(part for part in paragraphs if part.startswith(lead))
    assert len(declarations) == 1
    declaration = declarations[0].split(tail, 1)
    assert len(declaration) == 2
    assert declaration[1] == (
        " They are not XSD aliases and are not fact subjects requiring kind facts."
    )
    names_source = declaration[0].removeprefix(lead)
    assert names_source == "`String`, `Integer`, `Float`, `Boolean`, and `DateTime`"
    inline = MarkdownIt("commonmark").parseInline(names_source)[0]
    return tuple(
        child.content for child in inline.children or () if child.type == "code_inline"
    )


def _assert_od005_closed_seed(section: str) -> None:
    assert _od005_seed_table_rows(section) == OD005_SEED_ROWS
    assert _od005_seed_primitives(section) == OD005_SEED_PRIMITIVES


def _copy_ledger(tmp_path: Path) -> Path:
    copied = tmp_path / "overseer"
    shutil.copytree(OVERSEER, copied)
    return copied


def _rewrite_entry(path: Path, mutate, *, rehash: bool) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    if rehash:
        value["entry_hash"] = entry_hash(value)
    path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")


def _reseal(root: Path) -> None:
    previous = "GENESIS"
    paths = sorted((root / "entries").glob("*.json"))
    for sequence, path in enumerate(paths, start=1):
        value = json.loads(path.read_text(encoding="utf-8"))
        value["sequence"] = sequence
        value["entry_id"] = f"OVR-{sequence:06d}"
        value["previous_entry_hash"] = previous
        value["entry_hash"] = entry_hash(value)
        path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")
        previous = value["entry_hash"]
    head = json.loads((root / "head.json").read_text(encoding="utf-8"))
    head.update(
        entry_count=len(paths),
        head_entry_id=f"OVR-{len(paths):06d}",
        head_hash=previous,
    )
    (root / "head.json").write_text(
        canonical_json(head, indent=2) + "\n",
        encoding="utf-8",
    )


def _append_correction(
    root: Path,
    *,
    target_id: str,
    actor_type: str,
    replacement_required: bool,
) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    target = json.loads(
        (root / "entries" / f"{target_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        (
            datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
            + timedelta(minutes=1)
        )
        .isoformat()
        .replace("+00:00", "Z")
    )
    subject = target["subject"]
    references = [{"relation": "SUPERSEDES", "target": target_id, "type": "ENTRY"}]
    if subject["type"] != "PROGRAM":
        references.append(
            {"relation": "AFFECTS", "target": subject["id"], "type": subject["type"]}
        )
    entry = {
        "actor": {
            "id": "operator" if actor_type == "OPERATOR" else "overseer",
            "type": actor_type,
        },
        "data": {
            "affected_subject_ids": [subject["id"]],
            "replacement_required": replacement_required,
            "supersedes_entry_id": target_id,
        },
        "entry_hash": "sha256:" + "0" * 64,
        "entry_id": entry_id,
        "entry_type": "CORRECTION",
        "ledger": "overseer",
        "previous_entry_hash": "sha256:" + "0" * 64,
        "recorded_at": recorded_at,
        "references": references,
        "schema": "malleus.contract-compiler.ledger-entry/v1",
        "sequence": sequence,
        "subject": subject,
        "summary": f"Correct the recorded {subject['id']} entry.",
        "why": "Synthetic validation case for append-only correction authority.",
    }
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(entry, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def _append_replacement_workstream(root: Path, source_id: str) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    source = json.loads(
        (root / "entries" / f"{source_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        (
            datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
            + timedelta(minutes=1)
        )
        .isoformat()
        .replace("+00:00", "Z")
    )
    source.update(
        entry_id=entry_id,
        sequence=sequence,
        recorded_at=recorded_at,
        summary="Replace the corrected workstream state.",
        why="Synthetic positive case for an active typed replacement.",
    )
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(source, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def _workflow_run_blocks(path: Path) -> list[str]:
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [
        step["run"]
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if isinstance(step.get("run"), str)
    ]


def _workflow_commands(run_blocks: list[str]) -> list[list[str]]:
    return [
        shlex.split(line)
        for run_block in run_blocks
        for line in run_block.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def test_steady_state_workflows_do_not_revalidate_retained_overseer_evidence() -> None:
    for workflow in STEADY_STATE_WORKFLOWS:
        run_blocks = _workflow_run_blocks(workflow)
        assert all("verify-evidence" not in run_block for run_block in run_blocks)
        commands = _workflow_commands(run_blocks)
        assert [
            "python",
            "-m",
            "pytest",
            "-q",
            "tests/test_contract_compiler_ledger.py",
        ] in commands
        assert ["python", "scripts/contract_compiler_ledger.py", "check"] in commands


def test_cc002_integrated_candidate_binds_governed_checkpoint_lineage() -> None:
    card_source = CC002_CARD.read_bytes()
    card = json.loads(card_source)
    responsibility = card["responsibility"]
    assert CC002_LINEAGE_CONTRACT in responsibility
    assert "do not omit those paths from later candidate history" not in responsibility
    for checkpoint in CC002_CHECKPOINT_LINEAGE:
        assert responsibility.count(checkpoint) == 1

    resolved = [
        subprocess.run(
            ["git", "rev-parse", f"{checkpoint}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        for checkpoint in CC002_CHECKPOINT_LINEAGE
    ]
    assert resolved == list(CC002_CHECKPOINT_LINEAGE)
    for earlier, later in zip(resolved, resolved[1:], strict=False):
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", earlier, later],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        assert ancestry.returncode == 0, ancestry.stderr.decode(errors="replace")

    evidence_path = "conformance/contract_compiler/v0/evidence/CC-002.json"
    checkpoint_scopes = {
        scope["path"]
        for scope in card["scopes"]
        if scope["kind"] == "FILE" and scope["path"] != evidence_path
    }
    assert len(checkpoint_scopes) == 7
    changed_paths = {
        path
        for checkpoint in resolved
        for path in subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", checkpoint],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    }
    assert changed_paths == checkpoint_scopes

    candidate = card["candidate"]
    assert candidate["state"] == "INTEGRATED"
    completion = json.loads(
        (OVERSEER / "evidence" / "CC-002-completion.json").read_text(
            encoding="utf-8"
        )
    )
    assert completion["base_commit"] == candidate["head_commit"]
    worker_entries = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((CC002_CARD.parent / "ledger" / "entries").glob("*.json"))
    ]
    candidate_committed_at = datetime.fromisoformat(
        subprocess.run(
            ["git", "show", "-s", "--format=%cI", candidate["head_commit"]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    worker_recorded_at = [
        datetime.fromisoformat(
            entry["recorded_at"].removesuffix("Z") + "+00:00"
        )
        for entry in worker_entries
    ]
    completion_recorded_at = datetime.fromisoformat(
        completion["recorded_at"].removesuffix("Z") + "+00:00"
    )
    completion_revision = json.loads(
        (OVERSEER / "entries" / "OVR-000099.json").read_text(encoding="utf-8")
    )
    completion_fact = json.loads(
        (OVERSEER / "entries" / "OVR-000100.json").read_text(encoding="utf-8")
    )
    revision_recorded_at = datetime.fromisoformat(
        completion_revision["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert candidate_committed_at < worker_recorded_at[0]
    assert worker_recorded_at == sorted(worker_recorded_at)
    assert worker_recorded_at[-1] < completion_recorded_at
    assert completion_recorded_at < revision_recorded_at
    assert {
        entry["data"]["phase"]: entry["data"]["result"]
        for entry in worker_entries
        if entry["entry_type"] == "TDD_RESULT"
    } == {
        "RED": "EXPECTED_FAILURE",
        "GREEN": "PASS",
        "SLICE": "PASS",
        "DISPROOF": "PASS",
        "REGRESSION": "PASS",
        "PACKAGE": "NOT_APPLICABLE",
        "ATTEST": "PASS",
    }
    worker_tdd_check = next(
        check
        for check in completion["checks"]
        if check["check_id"] == "cc002-worker-tdd"
    )
    assert "PACKAGE not applicable" in worker_tdd_check["observed"]
    assert any(
        "PACKAGE not applicable" in claim for claim in completion_fact["data"]["claims"]
    )
    validate_candidate_history(
        ROOT,
        candidate,
        allowed_scopes=tuple(card["scopes"]),
        workstream_id="CC-002",
    )
    artifacts = {record["path"]: record for record in candidate["artifacts"]}
    retained_identity_paths = {
        "conformance/contract_compiler/v0/compiler_environment/manifest.json",
        "conformance/contract_compiler/v0/compiler_environment/requirements.lock",
        "conformance/contract_compiler/v0/compiler_environment/resolution-report.json",
        "conformance/contract_compiler/v0/compiler_environment/build-record.json",
        "conformance/contract_compiler/v0/compiler_environment/derivation-record.json",
        "conformance/contract_compiler/v0/compiler_environment/verification.json",
    }
    assert len(artifacts) == 13
    assert retained_identity_paths <= artifacts.keys()
    assert checkpoint_scopes <= artifacts.keys()
    for path in checkpoint_scopes:
        source = subprocess.run(
            ["git", "show", f"{candidate['head_commit']}:{path}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert artifacts[path] == {
            "byte_length": len(source),
            "path": path,
            "sha256": "sha256:" + hashlib.sha256(source).hexdigest(),
        }

    evidence_reference = next(
        record for record in candidate["evidence"] if record["path"] == evidence_path
    )
    evidence_source = subprocess.run(
        ["git", "show", f"{candidate['head_commit']}:{evidence_path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert evidence_reference == {
        "byte_length": len(evidence_source),
        "path": evidence_path,
        "result": "PASS",
        "sha256": "sha256:" + hashlib.sha256(evidence_source).hexdigest(),
    }
    evidence = json.loads(evidence_source)
    lineage_limitation = next(
        limitation
        for limitation in evidence["limitations"]
        if "candidate range" in limitation.casefold()
    )
    assert all(
        checkpoint in lineage_limitation for checkpoint in CC002_CHECKPOINT_LINEAGE
    )
    assert any(
        check["result"] == "PASS"
        and all(
            checkpoint in canonical_json(check)
            for checkpoint in CC002_CHECKPOINT_LINEAGE
        )
        for check in evidence["checks"]
    )

    ledger = load_ledger(OVERSEER)
    superseded = {
        entry["data"]["supersedes_entry_id"]
        for entry in ledger.entries
        if entry["entry_type"] == "CORRECTION"
    }
    cc002_state = next(
        entry
        for entry in reversed(ledger.entries)
        if entry["entry_id"] not in superseded
        and entry["entry_type"] == "WORKSTREAM_STATE"
        and entry["data"]["workstream_id"] == "CC-002"
    )
    integration = json.loads(INTEGRATION.read_text(encoding="utf-8"))
    assert cc002_state["entry_id"] == "OVR-000101"
    assert cc002_state["data"]["new_state"] == "COMPLETE"
    assert card["ledger"]["state"] == "RECORDED"
    selected_integration = json.loads(
        subprocess.run(
            [
                "git",
                "show",
                f"{CC002_SELECTION_COMMIT}:design/contract_compiler/integration.json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    assert selected_integration["authority"]["overseer_ledger"] == {
        "entry_count": 101,
        "head_entry_id": "OVR-000101",
        "head_hash": "sha256:e0eaf379e6f5b708952d63510fa0a98b16b05f457304244ac4cec20501f51c4d",
        "path": "design/contract_compiler/overseer",
    }
    assert integration["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    row = next(
        item for item in integration["workstreams"] if item["workstream_id"] == "CC-002"
    )
    assert row["depends_on"] == ["CC-000", "CC-D12"]
    selection_positions = {
        workstream_id: position
        for position, workstream_id in enumerate(integration["selections"])
    }
    assert selection_positions["CC-000"] < selection_positions["CC-002"]
    assert "CC-D12" not in selection_positions
    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-002/manifest.json",
        "sha256": "sha256:" + hashlib.sha256(card_source).hexdigest(),
        "state": "PRESENT",
    }
    assert card["authorization"]["dependency_bindings"] == [
        {
            "card_sha256": "sha256:4943b94cad90eeecac92944bd1bdca80618658b75744aec267bcbe13678f93b9",
            "completion_entry_hash": "sha256:d37f9eb77f572ee648f640171d9481800aaa6bc33f6f6553f21cd177188099b3",
            "completion_entry_id": "OVR-000016",
            "integrated_head": "09265cb4af2cec5ea8e1d3b063dce811952fcfe6",
            "workstream_id": "CC-000",
        },
        {
            "card_sha256": "sha256:46c8ee073c2d9537f512c579915ee49bc67c15d19c665c84df9d736deb9b3bd7",
            "completion_entry_hash": "sha256:089705dd93e3f892ae03a93896b44171f333e0d2cea0110c763d7f19a5f7795a",
            "completion_entry_id": "OVR-000084",
            "integrated_head": "d0eb42d42d5d4bd3f18d883eb26b2eb3806e2c72",
            "workstream_id": "CC-D12",
        },
    ]

    completion_commit = "1ae83e49ef1ae2432400978ffd77cde525719cbe"
    completion_tree = "3128b1d5155a0a71d7311f5c5b3968811c0bba4c"
    assert (
        subprocess.run(
            ["git", "rev-parse", f"{completion_commit}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == completion_commit
    )
    assert (
        subprocess.run(
            ["git", "rev-parse", f"{completion_commit}^{{tree}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == completion_tree
    )
    selection_report_path = OVERSEER / "evidence" / "CC-002.json"
    selection_report_source = subprocess.run(
        [
            "git",
            "show",
            f"{CC002_SELECTION_COMMIT}:design/contract_compiler/overseer/evidence/CC-002.json",
        ],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert selection_report_path.read_bytes() == selection_report_source
    selection_report = json.loads(selection_report_source)
    for artifact in selection_report["artifacts"]:
        source = subprocess.run(
            ["git", "show", f"{CC002_SELECTION_COMMIT}:{artifact['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == "sha256:" + hashlib.sha256(source).hexdigest()
    assert selection_report["base_commit"] == completion_commit
    selection_claims = canonical_json(selection_report)
    assert completion_commit in selection_claims
    assert completion_tree in selection_claims
    completion_committed_at = datetime.fromisoformat(
        subprocess.run(
            ["git", "show", "-s", "--format=%cI", completion_commit],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    selection_recorded_at = datetime.fromisoformat(
        selection_report["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert completion_committed_at < selection_recorded_at

    selection_revision = next(
        entry for entry in ledger.entries if entry["entry_id"] == "OVR-000102"
    )
    assert selection_revision["entry_id"] == "OVR-000102"
    assert selection_revision["entry_type"] == "DOCUMENT_REVISION"
    selection_fact = next(
        entry for entry in ledger.entries if entry["entry_id"] == "OVR-000103"
    )
    assert selection_fact["entry_id"] == "OVR-000103"
    assert selection_fact["entry_type"] == "VERIFIED_FACT"
    selection_revision_at = datetime.fromisoformat(
        selection_revision["recorded_at"].removesuffix("Z") + "+00:00"
    )
    selection_fact_at = datetime.fromisoformat(
        selection_fact["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert selection_recorded_at < selection_revision_at < selection_fact_at
    selection_entries = [
        entry
        for entry in ledger.entries
        if selection_revision["sequence"]
        <= entry["sequence"]
        <= selection_fact["sequence"]
    ]
    assert [entry["entry_id"] for entry in selection_entries] == [
        "OVR-000102",
        "OVR-000103",
    ]
    assert all(
        entry["entry_type"] != "WORKSTREAM_STATE" for entry in selection_entries
    )
    assert {
        "relation": "EVIDENCES",
        "target": completion_commit,
        "type": "COMMIT",
    } in selection_fact["references"]


def test_ccd12_r3_exact_wheel_derivation_authority_is_active() -> None:
    state = load_ledger(OVERSEER)
    active_corrections = [
        entry for entry in state.entries if entry["entry_type"] == "CORRECTION"
    ]
    superseded = {entry["data"]["supersedes_entry_id"] for entry in active_corrections}
    assert {
        "OVR-000050",
        "OVR-000053",
        "OVR-000054",
        "OVR-000061",
        "OVR-000064",
        "OVR-000065",
        "OVR-000072",
        "OVR-000075",
        "OVR-000076",
    } <= superseded
    for target in (
        "OVR-000050",
        "OVR-000053",
        "OVR-000054",
        "OVR-000061",
        "OVR-000064",
        "OVR-000065",
        "OVR-000072",
        "OVR-000075",
        "OVR-000076",
    ):
        correction = next(
            entry
            for entry in active_corrections
            if entry["data"]["supersedes_entry_id"] == target
        )
        assert correction["data"]["replacement_required"] is True
    decision_correction = next(
        entry
        for entry in active_corrections
        if entry["data"]["supersedes_entry_id"] == "OVR-000072"
    )
    assert decision_correction["actor"] == {"id": "operator", "type": "OPERATOR"}

    active_entries = [
        entry for entry in state.entries if entry["entry_id"] not in superseded
    ]
    decision = next(
        entry
        for entry in reversed(active_entries)
        if entry["entry_type"] == "DECISION"
        and entry["data"]["decision_id"] == "OD-012"
    )
    assert decision["entry_id"] == "OVR-000097"
    assert decision["actor"] == {"id": "operator", "type": "OPERATOR"}
    assert decision["data"]["supersedes_entry_id"] == "OVR-000081"
    assert decision["data"]["selected_option"] == (
        "Internal provisional CC-002 use of one exact embedded CFGraph 0.2.1 wheel"
    )
    assert decision["data"]["canonical_record_uris"] == []
    assert decision["data"]["satisfies_workstreams"] == ["CC-002"]
    assert {
        (reference["relation"], reference["type"], reference["target"])
        for reference in decision["references"]
    } >= {
        ("EVIDENCES", "ENTRY", "OVR-000081"),
        ("EVIDENCES", "ENTRY", "OVR-000093"),
        ("EVIDENCES", "ENTRY", "OVR-000095"),
        ("SATISFIES", "WORKSTREAM", "CC-002"),
    }

    exception_policy = canonical_json(decision["data"]).casefold()
    for required in (
        "cfgraph-0.2.1-py3-none-any.whl",
        "2256 bytes",
        "sha256:28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13",
        "name: cfgraph",
        "version: 0.2.1",
        "requires-dist: rdflib>=0.4.2",
        "generator: setuptools 83.0.0",
        "internal, non-release",
        "exact bytes and selected semantics fail closed",
        "wheel-only offline closure",
        "behavior smoke",
        "no reproducible-build",
        "license-sufficiency",
        "security",
        "vulnerability",
        "distribution",
        "public-release claim",
    ):
        assert required in exception_policy
    for deferred in (
        "deterministic double-build from exact source in the selected container",
        "authoritative license and notice bytes",
        "release-grade supply-chain, security, and vulnerability attestation",
        "retire this exception before any public or external release",
    ):
        assert deferred in exception_policy

    r3_refinement = next(
        entry for entry in state.entries if entry["entry_id"] == "OVR-000081"
    )
    assert r3_refinement["data"]["supersedes_entry_id"] == "OVR-000072"
    base_decision = next(
        entry for entry in state.entries if entry["entry_id"] == "OVR-000072"
    )
    policy = canonical_json(
        [base_decision["data"], r3_refinement["data"]]
    ).casefold()
    for required in (
        "antlr4-python3-runtime-4.9.3.tar.gz",
        "117034",
        "f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b",
        "https://files.pythonhosted.org/packages/3e/38/7859ff46355f76f8d19459005ca000b6e7012f2f1ca597746cbcd1fbfe5e/antlr4-python3-runtime-4.9.3.tar.gz",
        "setuptools-83.0.0-py3-none-any.whl",
        "1008090",
        "29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3",
        "https://files.pythonhosted.org/packages/5d/40/e1e72872c6354b306daef1703549e8e83b4d43cfea356311bf722a043752/setuptools-83.0.0-py3-none-any.whl",
        "source_date_epoch=315532800",
        "setuptools.build_meta:__legacy__",
        "two fresh",
        "byte-identical",
        "network denied",
        "wheel-only",
        "not rebuilt",
        "prefixcommons-0.1.12-py3-none-any.whl",
        "29482",
        "16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b",
        "https://files.pythonhosted.org/packages/31/e8/715b09df3dab02b07809d812042dc47a46236b5603d9d3a2572dbd1d8a97/prefixcommons-0.1.12-py3-none-any.whl",
        "0.1.12+malleus.1",
        "requires-dist: pytest-logging (>=2015.11.4,<2016.0.0)",
        "pytest-logging>=2015.11.4,<2016.0.0",
        "14 members",
        "109044 expanded bytes",
        "ten package code or data",
        "1500-byte",
        "3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4",
        "1960 bytes",
        "4c6cf90de54fa4ce46d1235551f75c021bacab34b8c9894fd50a8096441a5303",
        "83 bytes",
        "cb778389a15548d4cf6e0cdf367d27627e6d127d5c5fa5ab75eb43950338c56c",
        "generator: poetry 1.0.7",
        "every package code, resource, and license payload byte exactly",
        "generator: malleus-cc002 (wheel-derivation-v1)",
        "zip_stored",
        "two fresh",
        "stdlib-only",
        "derivative-inputs/prefixcommons-0.1.12-py3-none-any.whl",
        "prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
        "/built/prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
        "retain the derived wheel under built/",
        "build-record.json",
        "derivation-record.json",
        "malleus.cc002.wheel-derivation/v1",
        "malleus.cc002.acquire-result/v3",
        "malleus.cc002.verify-result/v3",
        "malleus.cc002.compiler-environment/v3",
        "malleus.cc002.internal-verification/v3",
        "malleus.cc002.container-verification/v1",
        "malleus.cc002.source-build/v1",
        "retain malleus.cc002.container-verification/v1 and malleus.cc002.source-build/v1 unchanged",
        "derivation_record_sha256",
        "eight retained inputs",
        "two produced artifacts",
        "1980-01-01 00:00:00",
        "unix create-system identity",
        "regular-file mode 0644",
        "empty archive/member comments and extra fields",
        "record is generated from the final member payloads and names",
        "its own hash/size cells stay empty",
        "never imports, extracts, or executes prefixcommons",
        "validate the exact input record",
        "exact whole-wheel identity",
        "duplicate/unsafe member names",
        "non-regular member types",
        "bsd 3-clause license",
        "no separate extracted license file",
        "direct resolver input",
        "official prefixcommons wheel absent",
        "pip check",
        "go:0008150",
        "http://purl.obolibrary.org/obo/go_0008150",
        "strict mode",
        "exactly [go:0008150]",
        "linkml_runtime.utils.namespaces.namespaces",
        "https://example.org/",
        "ex:item",
        "pytest, pytest-logging, and py",
        "maintenance and security review",
        "non-allowlisted payload change",
        "license loss",
        "unequal transform",
        "resolver substitution",
        "smoke that requires the removed plugin",
    ):
        assert required in policy

    refinement_policy = canonical_json(r3_refinement["data"]).casefold()
    for required in (
        "ovr-000072 unchanged",
        "ascending unicode code point",
        "final posix member names",
        "including the record member and its row",
        "every final zip filename is ascii",
        "utf-8 without bom",
        "exactly three fields",
        "comma delimiter",
        "ascii double-quote quotechar",
        "doublequote true",
        "quote_minimal",
        "no escapechar",
        "lf line terminator",
        "terminal lf",
        "url-safe base64 of the raw sha-256 digest",
        "without '=' padding",
        "decimal byte length",
        "record row's own hash and size fields empty",
        "date_time to 1980-01-01 00:00:00",
        "compress_type to zip_stored",
        "create_system=3",
        "create_version=20",
        "extract_version=20",
        "reserved=0",
        "flag_bits=0",
        "volume=0",
        "internal_attr=0",
        "external_attr=(0o100644 << 16)",
        "extra/comment empty",
        "archive comment empty",
        "disable zip64",
        "reject every input or output requiring it",
        "crc32, compressed and uncompressed sizes, and local-header offsets",
        "consequences of the exact payloads and member order",
        "set every selected record, zipinfo, and archive field explicitly",
        "reopen the written wheel and validate every selected field and byte",
        "must not rely on cpython defaults",
        "https://packaging.python.org/en/latest/specifications/recording-installed-packages/",
        "https://docs.python.org/3.12/library/zipfile.html",
        "complete canonical grammar above is a malleus choice",
        "do not claim those sources mandate every selected value",
    ):
        assert required in refinement_policy

    workstream_states = {
        entry["data"]["workstream_id"]: entry
        for entry in active_entries
        if entry["entry_type"] == "WORKSTREAM_STATE"
    }
    ccd12 = workstream_states["CC-D12"]
    cc002 = workstream_states["CC-002"]
    assert ccd12["entry_id"] != "OVR-000053"
    assert ccd12["data"]["new_state"] == "COMPLETE"
    assert cc002["entry_id"] != "OVR-000054"
    assert cc002["entry_id"] == "OVR-000101"
    assert cc002["data"]["new_state"] == "COMPLETE"

    card = json.loads(CC002_CARD.read_text(encoding="utf-8"))
    binding = next(
        item
        for item in card["authorization"]["dependency_bindings"]
        if item["workstream_id"] == "CC-D12"
    )
    assert binding["completion_entry_id"] == ccd12["entry_id"]
    assert binding["completion_entry_hash"] == ccd12["entry_hash"]
    responsibility = card["responsibility"].casefold()
    for required in (
        "malleus.cc002.acquire-result/v4",
        "malleus.cc002.verify-result/v4",
        "malleus.cc002.compiler-environment/v4",
        "malleus.cc002.internal-verification/v4",
        "nine governed inputs",
        "two produced artifacts",
        "406 adapter tests",
        "74 governance tests",
        "internal, non-release",
        "cfgraph-0.2.1-py3-none-any.whl",
        "sha256:28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13",
        "retire the exception before public or external release",
    ):
        assert required in responsibility
    for obsolete in (
        "malleus.cc002.acquire-result/v3",
        "malleus.cc002.verify-result/v3",
        "formal cfgraph gate",
        "keep candidate state none",
        "ledger state not_started",
    ):
        assert obsolete not in responsibility

    for relative in HISTORICAL_CCD12_PATHS:
        historical = subprocess.run(
            ["git", "show", f"{GOVERNANCE_BASE_COMMIT}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert (ROOT / relative).read_bytes() == historical
    for relative in HISTORICAL_R3_PATHS:
        historical = subprocess.run(
            ["git", "show", f"{R3_GOVERNANCE_BASE_COMMIT}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert (ROOT / relative).read_bytes() == historical
    for relative, expected in IMMUTABLE_R3_REFINEMENT_INPUTS.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_revision_16_graph_is_generated_from_all_turtle_projections() -> None:
    blocks = [
        token.content
        for path in FOUNDATION_PROJECTIONS
        for token in MarkdownIt("commonmark").parse(path.read_text(encoding="utf-8"))
        if token.type == "fence" and token.info.strip() == "turtle"
    ]
    assert len(blocks) == 28
    canonical_path = ROOT / "design" / "PROTOCOL_FOUNDATION_GRAPH.ttl"
    source = canonical_path.read_bytes()
    body = [
        line
        for line in source.decode("utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    projected = Graph().parse(data="\n".join(blocks), format="turtle")
    canonical = Graph().parse(data=source, format="nt")
    assert set(projected) == set(canonical)
    assert len(canonical) == 1510

    digest = hashlib.sha256(source).hexdigest()
    assert source.decode("utf-8").splitlines()[:9] == [
        "# Canonical Malleus protocol foundation design graph.",
        "#",
        "# Design graph revision: 16",
        "# Evidence cutoff: 2026-08-26",
        "# Authority: candidate and accepted design states recorded by author decisions.",
        "# Shipped capability remains controlled by src/malleus/status.py and tests.",
        "#",
        "# The Markdown tuple blocks are explanatory projections of this graph.",
        "# Semantic changes create new object revisions and supersedes edges.",
    ]
    marker = (
        "Canonical design graph: "
        "[`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),"
    )
    for path in FOUNDATION_PROJECTIONS:
        lines = path.read_text(encoding="utf-8").splitlines()
        index = lines.index(marker)
        assert lines[index : index + 3] == [
            marker,
            "revision 16,",
            f"`sha256:{digest}`",
        ]
    assert body == sorted(set(body))

    cc = "https://malleus.dev/contract-compiler/"
    mfg = "https://malleus.dev/foundation-graph/"
    selects = URIRef(f"{mfg}selects")
    decision_date = URIRef(f"{mfg}decisionDate")
    assert set(canonical.objects(URIRef(f"{cc}OD-012"), decision_date)) == {
        Literal("2026-08-25")
    }
    assert set(canonical.objects(URIRef(f"{cc}OD-012"), selects)) == {
        URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR3")
    }
    accepted = {
        "OD-002": "ExactSlotOnlyExplicitAdoptionProfile",
        "OD-003": "LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile",
        "OD-004": "TypedPersistedWireEpochHardBreakProfile",
        "OD-005": "AtomicOntologyPoweredCanonicalFactContract",
        "OD-011": "ExplicitSingleResolverProfileSelection",
        "OD-013": "SingleDistributionCompilerIncludedPackagingTopology",
        "OD-014": "QuietBellArchiveFixturePublicationBoundary",
    }
    for decision, selected in accepted.items():
        subject = URIRef(f"{cc}{decision}")
        assert set(canonical.objects(subject, decision_date)) == {
            Literal("2026-08-26")
        }
        assert set(canonical.objects(subject, selects)) == {URIRef(f"{mfg}{selected}")}

    binds = URIRef(f"{mfg}binds")
    required_bindings = {
        "ExactSlotOnlyExplicitAdoptionProfile": {
            "SlotDeclarationsOnlyAdoptionBoundary",
            "LiteralBooleanAdoptsTrueRequiredBoundary",
            "ImportedAncestorOwnerAuthoritativeBoundary",
            "ExactTypedSourceStructureBeforeDefaultsBoundary",
            "RemoveOnlyDescriptionAdoptsAndEmptyAnnotationsComparisonBoundary",
            "AdoptionDifferenceOrInvalidMarkerRefusalBoundary",
            "SourceOrderNeverCompositionWinnerBoundary",
        },
        "LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile": {
            "ReplaceableAdapterNeutralOutputContract",
            "GenericNeutralResultConformanceBoundary",
            "SourceLanguageSpecificNamedVersionedProfileAndCorpusBoundary",
            "LinkMLCorpusOnlyForLinkMLCompatibilityClaimBoundary",
            "NamedVersionedAdapterSupportAndDefaultProfileBoundary",
            "AppliedDefaultsExplicitWithProvenanceBoundary",
            "RuntimeNeverInfersFrontendDefaultsBoundary",
            "NoLegacyOntologyRegistryEmulationV0Boundary",
            "CCX01SimpleParityEqual",
            "CCX01ParentMixinPrecedenceLinkML",
            "CCX01RepeatedMixinRefused",
            "CCX01ConflictingMixinsABRefused",
            "CCX01ConflictingMixinsBARefused",
            "CCX01NumericBoundsLinkML",
            "CCX01ExplicitFalseEqual",
            "CCX01DefaultRangeLinkMLExplicit",
            "CCX01AttributeSlotUsageLinkML",
        },
        "TypedPersistedWireEpochHardBreakProfile": {
            "PersistedWireEpochCheckedBeforeSemanticDecodeBoundary",
            "ExactPublicDiagnosticIdentifierDeferredToCCW01Boundary",
            "LegacyOntologyHashNeverReinterpretedBoundary",
            "NoPersistedWireFallbackReceiptMigrationTranslationOrRewriteBoundary",
            "ReconProjectTypedHardBreak",
            "ReconRecordTypedHardBreak",
            "KnowledgeGraphSnapshotTypedHardBreak",
            "ProtocolEnvelopeTypedHardBreakBeforeReplay",
            "EmbeddedGraphBaseAndCandidateNotReached",
        },
        "AtomicOntologyPoweredCanonicalFactContract": {
            "ExactNonExpressionSeedContractMetamodel",
            "AtomicCanonicalJSONFactProfileV0",
            "AbsoluteIdentifierExactUnicodeSymbolPolicyV0",
            "ContractMetamodelSemanticAuthorityOverJSONBoundary",
            "ClosedThreeMemberCanonicalJSONFactWireBoundary",
            "CanonicalDecimalLexicalNumericObjectBoundary",
            "InternalCandidateDigestNotPublicIdentityBoundary",
            "StructuralIdentityAndExternalProvenanceBoundary",
            "FrontendDirectFactConformanceOnlyParityBoundary",
            "ExactSeedMetamodelBootstrapTrustBoundary",
            "ExpressionVocabularyDeferredToOD008Boundary",
            "AdmissionArtifactBundleAndPromotionSeparateAuthorityBoundary",
            "NoGenericDefaultValueOrRuntimeDefaultBoundary",
        },
        "ExactNonExpressionSeedContractMetamodel": {
            "ExactClassSeedFactRule",
            "ExactSlotAndSlotUseSeedFactRule",
            "ExactEnumSeedFactRule",
            "ExactScalarAndSeedPrimitiveFactRule",
            "ExactWholeSetSeedFactInvariant",
            "SourceToFactCompletenessSeparateConformanceBoundary",
        },
        "ExplicitSingleResolverProfileSelection": {
            "StrictMalleusResolverDefaultBoundary",
            "ExplicitNamedVersionedResolverAndConfigurationBoundary",
            "ResolverSoleByteSourceAdapterNoHiddenIOBoundary",
            "ResolverFileAndNetworkCapabilitiesDefaultDenyBoundary",
            "ResolverNeverTryNextFallbackBoundary",
            "ExactResolvedSourceAndImportEdgeProvenanceBoundary",
            "ExactResolvedLocatorStringModuleInstanceIdentityBoundary",
            "NoUniversalLocatorNormalizationBoundary",
            "RootRetainedSourceSeparateFromImportEdgeBoundary",
            "ImportEdgeCarriesParentOrdinalLiteralAndChildResolvedLocatorBoundary",
            "ResolvedIdentityDifferentBytesRefusalBoundary",
            "DifferentLocatorSameBytesDistinctObservationBoundary",
            "ImportOrderProvenanceOnlyBoundary",
            "AllImportCyclesRefusedWithLineageBoundary",
        },
        "SingleDistributionCompilerIncludedPackagingTopology": {
            "NormalMalleusInstallIncludesCompilerAndLinkMLBoundary",
            "NoCoreCompilerExtraOrSecondDistributionV0Boundary",
            "LeanInstallDeferredGovernedRevisionBoundary",
            "ArtifactBackedRuntimeLinkMLImportBlockedBoundary",
            "TargetTopologyNotCurrentPackagingClaimBoundary",
        },
        "QuietBellArchiveFixturePublicationBoundary": {
            "QuietBellVocabularyFixtureOnlyCoreNeutralBoundary",
            "QuietBellAttestationExcludesVisualAssetsBoundary",
            "FuturePublicAssetExactManifestBoundary",
            "CCPUB01ReviewBindsExactManifestDigestBoundary",
            "AssetOrManifestChangeInvalidatesPublicReviewBoundary",
            "DecisionCreatesNoFixtureAssetOrPublicationBoundary",
        },
    }
    for selected, expected in required_bindings.items():
        assert {
            str(value).removeprefix(mfg)
            for value in canonical.objects(URIRef(f"{mfg}{selected}"), binds)
        } == expected
    quiet_bell = URIRef(f"{mfg}QuietBellArchiveFixturePublicationBoundary")
    assert set(canonical.objects(quiet_bell, URIRef(f"{mfg}workingName"))) == {
        Literal("Quiet Bell Archive")
    }
    assert set(canonical.objects(quiet_bell, URIRef(f"{mfg}attestationText"))) == {
        Literal(
            "Luis Guzman Lorenzo is the author and rights holder for the original "
            "Quiet Bell text/data, licensed Apache-2.0"
        )
    }
    r3 = URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR3")
    assert (
        r3,
        URIRef(f"{mfg}supersedes"),
        URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR2"),
    ) in canonical
    for selected in (
        "Antlr4Python3Runtime4_9_3DeterministicWheelBuildProfile",
        "Prefixcommons0_1_12Malleus1WheelDerivationProfile",
        "CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR3",
        "RootSourceRetentionSeparateFromTransitiveBuildInputBoundary",
        "DerivativeInputSeparateFromBuildAndRuntimeBoundary",
        "TwoFreshBuildsByteIdenticalBoundary",
        "TwoFreshTransformsByteIdenticalBoundary",
        "FinalRuntimeClosureRemainsWheelOnlyBoundary",
        "RuntimeClosureExcludesPytestPytestLoggingAndPyBoundary",
        "MalleusDerivedPackagingMaintenanceAndSecurityOwnershipBoundary",
    ):
        assert (r3, binds, URIRef(f"{mfg}{selected}")) in canonical

    status = URIRef(f"{mfg}status")
    statuses: dict[object, set[object]] = {}
    for subject, _, object_ in canonical.triples((None, status, None)):
        statuses.setdefault(subject, set()).add(object_)
    assert len(statuses) == 302
    assert all(len(values) == 1 for values in statuses.values())
    realization = (
        ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md"
    ).read_text(encoding="utf-8")
    assert (
        f"4. All {len(statuses)} subjects carrying `mfg:status` have exactly one "
        "distinct status."
    ) in realization

    depends_on = URIRef(f"{mfg}dependsOn")
    edges = {
        (subject, object_)
        for subject, _, object_ in canonical.triples((None, depends_on, None))
    }
    nodes = {node for edge in edges for node in edge}
    assert len(nodes) == 103
    assert len(edges) == 105
    successors = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for dependent, prerequisite in edges:
        successors[prerequisite].add(dependent)
        indegree[dependent] += 1
    ready = [node for node, count in indegree.items() if count == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for successor in successors[node]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    assert visited == len(nodes)


def test_od005_seed_vocabulary_and_canonical_example_are_mechanical() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od005_section(decisions)
    prose = " ".join(section.split())

    assert "JSON and any future JSON Schema define syntax only." in prose
    assert "wire facts always carry the full absolute IRI" in prose
    assert "Only expression vocabulary remains with `OD-008`" in prose
    assert "final predicate inventory" not in prose
    assert "There is no generic `defaultValue` fact" in prose
    assert "not a public or second first-party authoring language" in prose
    assert "never the normative runtime wire" in prose
    assert "stable public fact ids remain blocked on `od-006`" in prose.casefold()
    for rule in (
        "The parent-plus-`usesMixin` graph is acyclic.",
        "Every `usesMixin` target has `isMixin=true`",
        "The Scalar `typeof` graph is acyclic and terminates in exactly one seed primitive.",
        "Every non-seed identifier target resolves in the same fact set.",
        "Bounds are legal only when `valueRange` resolves through a Scalar chain to `Integer` or `Float`",
        "`valuePresence=ABSENT` conflicts with `required=true` and with `equalsString`.",
        "deterministic qualified class-local declaration",
        "Source-to-fact completeness is separately proven by support-profile conformance and independent oracles.",
    ):
        assert rule in prose
    for forbidden in (
        "example.malleus.dev/archive",
        "ReviewState",
        "Shelfmark",
        "Quiet Bell",
        "NinthQuire",
        "http://www.w3.org/2001/XMLSchema",
    ):
        assert forbidden not in section

    _assert_od005_closed_seed(section)

    json_blocks = [
        token.content.removesuffix("\n")
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "json"
    ]
    fact_source = next(block for block in json_blocks if block.startswith("["))
    assert "\n" not in fact_source
    facts = json.loads(fact_source)
    assert len(facts) == 38
    assert canonical_json(facts) == fact_source
    records = [canonical_json(fact) for fact in facts]
    assert records == sorted(records)
    assert len(records) == len(set(records))
    assert all(set(fact) == {"subject", "predicate", "object"} for fact in facts)
    assert all(isinstance(fact["object"], (str, bool)) for fact in facts)
    source_bytes = fact_source.encode("utf-8")
    source_digest = hashlib.sha256(source_bytes).hexdigest()
    assert len(source_bytes) == 6244
    assert source_digest == (
        "31db4d651f7a90f86466141193d806a5af58f8e09afa20dba838224b9361ca74"
    )
    assert (
        f"The array contains {len(facts)} facts and {len(source_bytes):,} bytes. "
        "Its SHA-256 is"
    ) in section
    assert f"`{source_digest}`" in section
    assert f"produce the same {len(facts)} metamodel-valid facts" in section

    envelope_source = next(
        block
        for block in json_blocks
        if block.startswith('{"class":')
        and "malleus.contract-structure.slot-use/v0" in block
    )
    envelope = json.loads(envelope_source)
    assert canonical_json(envelope) == envelope_source
    slot_use = (
        "urn:malleus:contract-structure:slot-use:v0:sha256:"
        + hashlib.sha256(envelope_source.encode("utf-8")).hexdigest()
    )
    assert slot_use == (
        "urn:malleus:contract-structure:slot-use:v0:sha256:"
        "5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"
    )
    slot_use_facts = {
        fact["predicate"]: fact["object"]
        for fact in facts
        if fact["subject"] == slot_use
    }
    assert slot_use_facts == {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": (
            "https://malleus.dev/contract-facts/SlotUse"
        ),
        "https://malleus.dev/contract-facts/identifier": False,
        "https://malleus.dev/contract-facts/inlined": False,
        "https://malleus.dev/contract-facts/multivalued": False,
        "https://malleus.dev/contract-facts/onClass": (
            "https://example.malleus.dev/domain/Record"
        ),
        "https://malleus.dev/contract-facts/required": True,
        "https://malleus.dev/contract-facts/usesSlot": (
            "https://example.malleus.dev/domain/value"
        ),
        "https://malleus.dev/contract-facts/valuePresence": "PRESENT",
        "https://malleus.dev/contract-facts/valueRange": (
            "https://malleus.dev/contract-facts/String"
        ),
    }
    seed_primitives = {
        f"https://malleus.dev/contract-facts/{name}"
        for name in ("String", "Integer", "Float", "Boolean", "DateTime")
    }
    assert not seed_primitives & {fact["subject"] for fact in facts}
    assert not any(
        fact["predicate"] == "https://malleus.dev/contract-facts/defaultValue"
        for fact in facts
    )
    evidence_source = (
        ROOT
        / "design"
        / "contract_compiler"
        / "overseer"
        / "evidence"
        / "CC-D05.json"
    ).read_text(encoding="utf-8")
    evidence = json.loads(evidence_source)
    assert {check["check_id"] for check in evidence["checks"]} == {
        "ccd05-dependencies",
        "ccd05-seed-metamodel",
        "ccd05-canonical-bytes",
        "ccd05-graph",
        "ccd05-boundaries",
        "ccd05-zero-scope",
    }
    for forbidden in (
        "Quiet Bell",
        "NinthQuire",
        "ReviewState",
        "Shelfmark",
        "example.malleus.dev/archive",
    ):
        assert forbidden not in evidence_source


def test_od005_closed_seed_guard_rejects_adversarial_drift() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od005_section(decisions)
    row = "| `Scalar` | `cf:typeof` | `Scalar` or `SeedPrimitive` | 1 |"
    assert section.count(row) == 1
    mutations = (
        section.replace(
            row,
            row + "\n| `Scalar` | `cf:experimental` | string | 0..1 |",
            1,
        ),
        section.replace(row, "", 1),
        section.replace(row, row + "\n" + row, 1),
        section.replace(
            "and `DateTime` under the seed namespace",
            "`DateTime`, and `Decimal` under the seed namespace",
            1,
        ),
    )
    assert all(mutation != section for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_od005_closed_seed(mutation)


def test_revision_16_conformance_rows_guard_closed_decisions() -> None:
    rows = {
        cells[0]: line.casefold()
        for line in (
            ROOT / "design" / "contract_compiler" / "conformance.md"
        ).read_text(encoding="utf-8").splitlines()
        if line.startswith("| AT-")
        and (cells := [cell.strip() for cell in line.strip("|").split("|")])
    }

    for phrase in (
        "resolver failure never tries another profile",
        "same locator with different bytes",
        "different locators with identical bytes",
        "distinct module observations",
        "directed cycle refuse with retained lineage",
    ):
        assert phrase in rows["AT-001"]
    for phrase in (
        "adoption marker/equality refusal matrix",
        "literal boolean adoption marker",
        "exact pre-default equality",
        "every other matrix cell refuses",
    ):
        assert phrase in rows["AT-003"]
    for phrase in ("every applied default", "materialized", "provenance"):
        assert phrase in rows["AT-005"]
    for phrase in (
        "exact seed kinds and predicates",
        "complete reified slotuse",
        "seed subject",
        "invalid bound or range",
        "identical metamodel-valid atomic facts",
        "refuse atomically",
    ):
        assert phrase in rows["AT-007"]

    program = (
        ROOT / "design" / "contract_compiler" / "program.md"
    ).read_text(encoding="utf-8").casefold()
    cc_r01 = next(line for line in program.splitlines() if line.startswith("| cc-r01 "))
    for phrase in (
        "no try-next profile",
        "same-locator/different-bytes refusal",
        "different-locator/same-bytes distinction",
        "directed-cycle lineage refusal",
    ):
        assert phrase in cc_r01


def test_contract_compiler_docs_keep_public_adapter_promotion_gated() -> None:
    index = (ROOT / "docs" / "contract_compiler" / "index.md").read_text(
        encoding="utf-8"
    )
    prose = " ".join(index.split())

    assert "No public frontend adapter or adapter docstring exists yet." in prose
    assert "Pinned LinkML 1.11.1 is the selected v0 target adapter." in prose
    assert "CC-R02 may implement and characterize" in prose
    assert "it cannot authorize public exposure." in prose
    assert "remain governed by open CC-D09/OD-009." in prose
    assert "If CC-D09/OD-009 permits promotion," in prose
    assert "When CC-R02 exposes a public adapter," not in prose
    assert "CC-R02 owns future public adapter docstrings" not in prose
    assert "Each public frontend adapter documents" not in prose
    assert "The default first-party adapter is" not in prose


def test_rdf_guard_dependency_is_an_exact_direct_dev_pin() -> None:
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - Python 3.10
        import tomli as tomllib

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    rdf_dependencies = [
        dependency
        for dependency in project["project"]["optional-dependencies"]["dev"]
        if dependency.casefold().startswith("rdflib")
    ]
    assert rdf_dependencies == ["rdflib==7.6.0"]


def test_rdf_guard_rejects_invalid_iri_and_literal_escape() -> None:
    with pytest.raises(ParserError):
        Graph().parse(
            data="<https://example/s> <https://example/p> <bad iri> .",
            format="nt",
        )
    with pytest.raises(BadSyntax):
        Graph().parse(
            data='@prefix ex: <https://example/> . ex:s ex:p "\\q" .',
            format="turtle",
        )


def test_verified_facts_do_not_claim_future_artifact_bytes() -> None:
    state = load_ledger(OVERSEER)
    superseded: set[str] = set()
    for entry in state.entries:
        if entry["entry_id"] not in superseded and entry["entry_type"] == "CORRECTION":
            superseded.add(entry["data"]["supersedes_entry_id"])
    active = [entry for entry in state.entries if entry["entry_id"] not in superseded]
    test_path = Path(__file__).relative_to(ROOT).as_posix()
    chronology_boundary = min(
        entry["sequence"]
        for entry in active
        if entry["entry_type"] == "DOCUMENT_REVISION"
        and any(
            document["path"] == test_path and document["change"] == "MODIFIED"
            for document in entry["data"]["documents"]
        )
        and any(
            document["change"] == "CREATED"
            and any(
                reference["type"] == "EVIDENCE"
                and reference["target"] == document["path"]
                for reference in entry["references"]
            )
            for document in entry["data"]["documents"]
        )
    )

    provenance: dict[str, list[tuple[int, str]]] = {}
    entry_root = OVERSEER.relative_to(ROOT) / "entries"
    for entry in state.entries:
        entry_path = entry_root / f"{entry['entry_id']}.json"
        entry_source = (ROOT / entry_path).read_bytes()
        provenance.setdefault(entry_path.as_posix(), []).append(
            (entry["sequence"], "sha256:" + hashlib.sha256(entry_source).hexdigest())
        )
        if entry["entry_type"] == "DOCUMENT_REVISION":
            for document in entry["data"]["documents"]:
                provenance.setdefault(document["path"], []).append(
                    (entry["sequence"], document["after_digest"])
                )

    facts = [
        entry
        for entry in active
        if entry["entry_type"] == "VERIFIED_FACT"
        and entry["sequence"] > chronology_boundary
    ]
    assert facts
    for fact in facts:
        evidence = [
            reference
            for reference in fact["references"]
            if reference["type"] == "EVIDENCE"
        ]
        assert evidence
        for reference in evidence:
            prior_report = [
                sequence
                for sequence, digest in provenance.get(reference["target"], [])
                if sequence < fact["sequence"] and digest == reference["digest"]
            ]
            assert prior_report, (
                f"{fact['entry_id']} claims evidence bytes before a prior "
                f"document revision: {reference['target']}"
            )
            report = json.loads(
                (ROOT / reference["target"]).read_text(encoding="utf-8")
            )
            for artifact in report["artifacts"]:
                prior_artifact = [
                    sequence
                    for sequence, digest in provenance.get(artifact["path"], [])
                    if sequence < fact["sequence"] and digest == artifact["sha256"]
                ]
                assert prior_artifact, (
                    f"{fact['entry_id']} claims artifact bytes before their active "
                    f"create/revision entry: {artifact['path']}"
                )


def test_overseer_ledger_and_projection_are_current() -> None:
    state = load_ledger(OVERSEER)

    assert state.head["entry_count"] == len(state.entries)
    assert state.head["head_entry_id"] == state.entries[-1]["entry_id"]
    assert state.head["head_hash"] == state.entries[-1]["entry_hash"]
    rendered = render_status(state)
    assert rendered == (OVERSEER / "status.md").read_text(encoding="utf-8")
    assert all(not line.endswith(" ") for line in rendered.splitlines())


def test_suffix_truncation_is_caught_by_separate_local_head(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    (copied / "entries" / "OVR-000006.json").unlink()

    with pytest.raises(LedgerValidationError, match="entry_count"):
        load_ledger(copied)


def test_entry_tampering_breaks_the_hash_chain(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(target, lambda value: value.update(summary="tampered"), rehash=False)

    with pytest.raises(LedgerValidationError, match="entry_hash"):
        load_ledger(copied)


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace(
            '"ledger": "overseer"', '"ledger": "overseer",\n  "ledger": "overseer"'
        ),
        encoding="utf-8",
    )

    with pytest.raises(LedgerValidationError, match="duplicate JSON key"):
        load_ledger(copied)


def test_unknown_fields_fail_schema_validation(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target, lambda value: value.update(notes="unbounded escape hatch"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_only_the_operator_can_record_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["actor"].update(type="WORKER", id="worker:test"),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_completed_workstream_requires_decision_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(evidence_entry_ids=[]),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_entry_type_and_payload_are_discriminated(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target, lambda value: value.update(entry_type="OBSERVATION"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_workstream_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000005.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="CC-X03"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="workstream subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_decision_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="OD-002"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="decision subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_document_reference_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="/etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="repository-relative"):
        load_ledger(copied, repository=ROOT)


def test_canonical_reference_must_exist_in_graph(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][1].update(
            target="https://malleus.dev/not-a-canonical-record"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="absent from the canonical graph"):
        load_ledger(copied, repository=ROOT)


def test_entry_reference_must_point_backward(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="OVR-000003"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="point backward"):
        load_ledger(copied, repository=ROOT)


def test_observation_cannot_complete_a_workstream(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"

    def make_observation(value: dict) -> None:
        value["entry_type"] = "OBSERVATION"
        value["data"] = {
            "as_of": value["recorded_at"],
            "basis": ["Unverified reviewer observation."],
            "limitations": ["No retained mechanical evidence."],
        }

    _rewrite_entry(target, make_observation, rehash=False)
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="OBSERVATION cannot satisfy a gate"
    ):
        load_ledger(copied, repository=ROOT)


def test_nonbootstrap_transition_requires_projected_prior_state(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000006.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(bootstrap=False),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="previous_state"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_the_program_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000001",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_decision_correction_requires_operator_identity(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value["actor"].update(id="overseer"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_correction_subject_must_equal_target_subject(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value.update(subject={"id": "CC-X03", "type": "WORKSTREAM"}),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="same subject"):
        load_ledger(copied, repository=ROOT)


def test_correction_that_requires_replacement_fails_without_one(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_projected_state_correction_cannot_waive_replacement(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(
        LedgerValidationError, match="projected state requires a replacement"
    ):
        load_ledger(copied, repository=ROOT)


def test_required_replacement_must_remain_active(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    replacement_id = _append_replacement_workstream(copied, "OVR-000006")
    _append_correction(
        copied,
        target_id=replacement_id,
        actor_type="OVERSEER",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_correction_of_correction_restores_the_original_projection(
    tmp_path: Path,
) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_correction(
        copied,
        target_id=correction_id,
        actor_type="OVERSEER",
        replacement_required=False,
    )

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `COMPLETE` |" in render_status(state)


def test_active_typed_replacement_projects_normally(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000122",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_replacement_workstream(copied, "OVR-000122")

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `COMPLETE` |" in render_status(state)


def test_evidence_reference_must_target_immutable_evidence_area(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(
            target="design/PROTOCOL_FOUNDATION_GRAPH.ttl"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="immutable evidence"):
        load_ledger(copied, repository=ROOT)


def test_verified_fact_requires_immutable_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"].pop(0),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="requires immutable EVIDENCE"):
        load_ledger(copied, repository=ROOT)


def test_failed_verification_report_cannot_satisfy_a_gate(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    copied = repository / "design" / "contract_compiler" / "overseer"
    shutil.copytree(OVERSEER, copied)
    for relative in (
        "design/contract_compiler/program.md",
        "design/contract_compiler/decisions.md",
        "design/PROTOCOL_FOUNDATION_GRAPH.ttl",
    ):
        target = repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    for path in sorted((copied / "entries").glob("OVR-*.json"))[6:]:
        path.unlink()
    report_path = copied / "evidence" / "CC-D01.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["checks"][0]["result"] = "FAIL"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")
    report_digest = "sha256:" + hashlib.sha256(report_path.read_bytes()).hexdigest()
    _rewrite_entry(
        copied / "entries" / "OVR-000004.json",
        lambda value: value["references"][0].update(digest=report_digest),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="failed check cannot satisfy a gate"
    ):
        load_ledger(copied, repository=repository)


def test_evidence_sealing_checks_source_bytes(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("verified bytes\n", encoding="utf-8")
    digest = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    report = {
        "artifacts": [
            {
                "byte_length": len(artifact.read_bytes()),
                "path": "artifact.txt",
                "sha256": digest,
            }
        ],
        "base_commit": "0" * 40,
        "checks": [
            {
                "check_id": "fixture",
                "method": "Compare exact source bytes.",
                "observed": "Fixture matched.",
                "result": "PASS",
            }
        ],
        "limitations": [],
        "recorded_at": "2026-08-24T19:30:00Z",
        "schema": "malleus.contract-compiler.verification-report/v1",
        "workstream_id": "CC-D01",
    }
    report_path = tmp_path / "report.json"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")

    verify_evidence_snapshot(
        report_path,
        tmp_path,
        schema_path=OVERSEER / "ledger.schema.json",
    )
    artifact.write_text("tampered bytes\n", encoding="utf-8")
    with pytest.raises(
        LedgerValidationError, match="byte length mismatch|digest mismatch"
    ):
        verify_evidence_snapshot(
            report_path,
            tmp_path,
            schema_path=OVERSEER / "ledger.schema.json",
        )


def test_latest_document_revision_must_match_current_bytes(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000009.json"
    _rewrite_entry(
        target,
        lambda value: value["data"]["documents"][0].update(
            after_digest="sha256:" + "0" * 64
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="latest document digest mismatch"):
        load_ledger(copied, repository=ROOT)


def test_document_revision_path_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000007.json"
    _rewrite_entry(
        target,
        lambda value: value["data"]["documents"][0].update(path="../../etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="schema violation"):
        load_ledger(copied, repository=ROOT)

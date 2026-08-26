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
CC002_LINEAGE_CONTRACT = (
    "Treat a7a65ccfdd7afd7d42a40509631fcdfef49f135e, "
    "4cbf79c287b7fdc3c21beda3869bd45b3835d8f4, and "
    "a48c754ae6a7aa904c3317d3cdde06de6db8ff98, plus "
    "6325bd962ecfd00bd4ca62b1d9febd07e3737357 as governed CC-002 worker "
    "checkpoints. The final materialization candidate must use the commit that "
    "integrates the CC-D12-R3 correction as its base and record that then-known "
    "commit in CC-002 evidence. The final candidate must not claim that its "
    "range contains the earlier checkpoints; it must include the seven "
    "checkpoint paths as exact artifacts at the candidate head and record the "
    "four checkpoint commits and this range limitation in CC-002 evidence."
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


def test_cc002_final_candidate_binds_governed_checkpoint_lineage() -> None:
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
    if candidate["state"] in {"ELIGIBLE", "INTEGRATED"}:
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
            record
            for record in candidate["evidence"]
            if record["path"] == evidence_path
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
    assert integration["authority"]["overseer_ledger"] == {
        "entry_count": cc002_state["sequence"],
        "head_entry_id": cc002_state["entry_id"],
        "head_hash": cc002_state["entry_hash"],
        "path": "design/contract_compiler/overseer",
    }
    row = next(
        item for item in integration["workstreams"] if item["workstream_id"] == "CC-002"
    )
    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-002/manifest.json",
        "sha256": "sha256:" + hashlib.sha256(card_source).hexdigest(),
        "state": "PRESENT",
    }


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
    assert decision["entry_id"] == "OVR-000081"
    assert decision["data"]["supersedes_entry_id"] == "OVR-000072"
    base_decision = next(
        entry for entry in state.entries if entry["entry_id"] == "OVR-000072"
    )
    policy = canonical_json([base_decision["data"], decision["data"]]).casefold()
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

    refinement_policy = canonical_json(decision["data"]).casefold()
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
    assert cc002["data"]["new_state"] == "ACTIVE"

    card = json.loads(CC002_CARD.read_text(encoding="utf-8"))
    binding = next(
        item
        for item in card["authorization"]["dependency_bindings"]
        if item["workstream_id"] == "CC-D12"
    )
    assert binding["completion_entry_id"] == ccd12["entry_id"]
    assert binding["completion_entry_hash"] == ccd12["entry_hash"]
    responsibility = card["responsibility"].casefold()
    assert "docker daemon access" in responsibility
    assert "require final re-attestation" in responsibility
    assert "docker daemon availability" not in responsibility
    assert "external reachability as unproven" not in responsibility
    assert "0.1.12+malleus.1" in responsibility
    assert "/built/prefixcommons-0.1.12+malleus.1-py3-none-any.whl" in responsibility
    assert "malleus.cc002.wheel-derivation/v1" in responsibility
    assert "malleus.cc002.acquire-result/v3" in responsibility
    assert "malleus.cc002.verify-result/v3" in responsibility
    assert "malleus.cc002.compiler-environment/v3" in responsibility
    assert "malleus.cc002.internal-verification/v3" in responsibility
    assert "malleus.cc002.container-verification/v1" in responsibility
    assert "malleus.cc002.source-build/v1" in responsibility
    assert "build-record.json" in responsibility
    assert "derivation-record.json" in responsibility
    assert "no standalone or separately extracted license file" in responsibility
    assert "pytest, pytest-logging, and py" in responsibility
    assert "ascending unicode code-point order" in responsibility
    assert "quote_minimal" in responsibility
    assert "create_system=3" in responsibility
    assert "zip64" in responsibility
    assert "must not rely on cpython defaults" in responsibility

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


def test_ccd12_r3_graph_is_generated_from_all_turtle_projections() -> None:
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
    assert len(canonical) == 1338

    digest = hashlib.sha256(source).hexdigest()
    assert source.decode("utf-8").splitlines()[:9] == [
        "# Canonical Malleus protocol foundation design graph.",
        "#",
        "# Design graph revision: 14",
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
            "revision 14,",
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
        assert (r3, URIRef(f"{mfg}binds"), URIRef(f"{mfg}{selected}")) in canonical

    status = URIRef(f"{mfg}status")
    statuses: dict[object, set[object]] = {}
    for subject, _, object_ in canonical.triples((None, status, None)):
        statuses.setdefault(subject, set()).add(object_)
    assert len(statuses) == 266
    assert all(len(values) == 1 for values in statuses.values())

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

    assert "| `CC-X03` | `PAUSED` |" in render_status(state)


def test_active_typed_replacement_projects_normally(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_replacement_workstream(copied, "OVR-000006")

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `PAUSED` |" in render_status(state)


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

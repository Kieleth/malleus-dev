from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.contract_compiler_integration import (  # noqa: E402
    IntegrationValidationError,
    load_program_registry,
    validate_tdd_gate,
    validate_candidate_history,
    validate_integration,
)
from scripts.contract_compiler_ledger import load_ledger as load_overseer_ledger  # noqa: E402
import scripts.contract_compiler_integration as integration_module  # noqa: E402


CONTRACT = ROOT / "design" / "contract_compiler"
INTEGRATION = CONTRACT / "integration.json"
PROGRAM = CONTRACT / "program.md"
SMALL_SHOP_REANCHOR_BASE = "0d2070475b775d10cacb8481aeff448f6af7c377"


def _canonical_json(value: Any) -> str:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    )


def _digest(source: bytes) -> str:
    return "sha256:" + hashlib.sha256(source).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class _UniqueYamlLoader(yaml.SafeLoader):
    pass


def _unique_yaml_mapping(loader, node, deep=False):
    value = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in value:
            raise AssertionError(f"duplicate YAML key: {key}")
        value[key] = loader.construct_object(value_node, deep=deep)
    return value


_UniqueYamlLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _unique_yaml_mapping,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(_canonical_json(value), encoding="utf-8")


def _copy_manifest_bundle(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    bundle = tmp_path / "contract_compiler"
    bundle.mkdir()
    shutil.copytree(CONTRACT / "workstreams", bundle / "workstreams")
    manifest = copy.deepcopy(_read_json(INTEGRATION))
    path = bundle / "integration.json"
    _write_json(path, manifest)
    return path, manifest


def _registry_row(manifest: dict[str, Any], workstream_id: str) -> dict[str, Any]:
    return next(
        row for row in manifest["workstreams"] if row["workstream_id"] == workstream_id
    )


def _card_path(bundle_manifest: Path, row: dict[str, Any]) -> Path:
    assert row["card"]["state"] == "PRESENT"
    return bundle_manifest.parent / row["card"]["path"]


def _rewrite_card(
    manifest_path: Path,
    manifest: dict[str, Any],
    workstream_id: str,
    mutate,
) -> dict[str, Any]:
    row = _registry_row(manifest, workstream_id)
    path = _card_path(manifest_path, row)
    card = _read_json(path)
    mutate(card)
    source = _canonical_json(card).encode("utf-8")
    path.write_bytes(source)
    row["card"]["byte_length"] = len(source)
    row["card"]["sha256"] = _digest(source)
    _write_json(manifest_path, manifest)
    return card


def _register_blocked_card(
    manifest_path: Path,
    manifest: dict[str, Any],
    workstream_id: str,
    owner_id: str,
) -> None:
    template = _read_json(_card_path(manifest_path, _registry_row(manifest, "CC-R01")))
    template["workstream_id"] = workstream_id
    template["responsibility"] = f"Synthetic {workstream_id} ownership card."
    template["assignment"] = {
        "state": "ASSIGNED",
        "owner_id": owner_id,
        "task_id": f"task:{workstream_id.lower()}",
    }
    template["scopes"] = [
        {
            "kind": "TREE",
            "path": f"conformance/contract_kernel/v0/{workstream_id.lower()}",
        }
    ]
    relative = f"workstreams/{workstream_id}/manifest.json"
    path = manifest_path.parent / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    source = _canonical_json(template).encode("utf-8")
    path.write_bytes(source)
    _registry_row(manifest, workstream_id)["card"] = {
        "state": "PRESENT",
        "path": relative,
        "byte_length": len(source),
        "sha256": _digest(source),
    }
    _write_json(manifest_path, manifest)


def _assert_code(
    error: pytest.ExceptionInfo[IntegrationValidationError], code: str
) -> None:
    assert str(error.value).startswith(f"[{code}]"), str(error.value)


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _commit(repository: Path, message: str) -> str:
    _git(repository, "add", "-A")
    _git(repository, "commit", "-m", message)
    return _git(repository, "rev-parse", "HEAD")


def _candidate_repository(tmp_path: Path) -> tuple[Path, str, str]:
    repository = tmp_path / "candidate"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "CC-000 Test")
    _git(repository, "config", "user.email", "cc000@example.invalid")
    (repository / "README.md").write_text("fixture\n", encoding="utf-8")
    base = _commit(repository, "base")
    (repository / "allowed").mkdir()
    (repository / "allowed" / "result.txt").write_text("result\n", encoding="utf-8")
    (repository / "evidence").mkdir()
    artifact = (repository / "allowed" / "result.txt").read_bytes()
    _write_json(
        repository / "evidence" / "checks.json",
        {
            "artifacts": [
                {
                    "byte_length": len(artifact),
                    "path": "allowed/result.txt",
                    "sha256": _digest(artifact),
                }
            ],
            "base_commit": base,
            "checks": [
                {
                    "check_id": "synthetic-candidate",
                    "method": "Exercise the candidate evidence gate.",
                    "observed": "The synthetic result matched.",
                    "result": "PASS",
                }
            ],
            "limitations": [],
            "recorded_at": "2026-08-24T20:00:00Z",
            "schema": "malleus.contract-compiler.verification-report/v1",
            "workstream_id": "CC-TEST",
        },
    )
    head = _commit(repository, "candidate")
    return repository, base, head


def _candidate(repository: Path, base: str, head: str) -> dict[str, Any]:
    artifact = (repository / "allowed" / "result.txt").read_bytes()
    evidence = (repository / "evidence" / "checks.json").read_bytes()
    return {
        "state": "ELIGIBLE",
        "base_commit": base,
        "head_commit": head,
        "head_tree": _git(repository, "rev-parse", f"{head}^{{tree}}"),
        "artifacts": [
            {
                "path": "allowed/result.txt",
                "byte_length": len(artifact),
                "sha256": _digest(artifact),
            }
        ],
        "evidence": [
            {
                "path": "evidence/checks.json",
                "byte_length": len(evidence),
                "sha256": _digest(evidence),
                "result": "PASS",
            }
        ],
    }


ALLOWED_SCOPES = (
    {"kind": "TREE", "path": "allowed"},
    {"kind": "TREE", "path": "evidence"},
)


def _complete_tdd_results() -> list[dict[str, str]]:
    return [
        {
            "phase": phase,
            "result": "EXPECTED_FAILURE" if phase == "RED" else "PASS",
        }
        for phase in integration_module.TDD_PHASES
    ]


def _syntactic_candidate(state: str = "ELIGIBLE") -> dict[str, Any]:
    return {
        "artifacts": [
            {
                "byte_length": 1,
                "path": "candidate/result.txt",
                "sha256": "sha256:" + "0" * 64,
            }
        ],
        "base_commit": "0" * 40,
        "evidence": [
            {
                "byte_length": 1,
                "path": "candidate/evidence.json",
                "result": "PASS",
                "sha256": "sha256:" + "0" * 64,
            }
        ],
        "head_commit": "0" * 40,
        "head_tree": "0" * 40,
        "state": state,
    }


def _raw_overseer_state() -> SimpleNamespace:
    entries = tuple(
        _read_json(path)
        for path in sorted((CONTRACT / "overseer" / "entries").glob("*.json"))
    )
    return SimpleNamespace(entries=entries)


def test_program_registry_contains_the_exact_approved_69_workstreams() -> None:
    registry = load_program_registry(PROGRAM)

    assert len(registry) == 69
    assert registry["CC-000"] == ()
    assert registry["CC-001"] == ("CC-000",)
    assert registry["CC-D05"] == ("CC-D01", "CC-D02", "CC-D03")
    assert registry["CC-D06"] == ("CC-D05",)
    assert registry["CC-D08"] == ("CC-D02", "CC-D03", "CC-D05")
    assert registry["CC-R01"] == (
        "CC-000",
        "CC-X03",
        "CC-D11",
        "CC-010",
        "CC-011",
        "CC-012",
        "CC-013",
        "CC-014",
        "CC-015",
        "CC-016",
        "CC-021",
        "CC-022",
    )
    assert registry["CC-021"] == ("CC-010", "CC-D03", "CC-D08", "CC-D11")
    assert registry["CC-022"] == (
        "CC-010",
        "CC-D02",
        "CC-D03",
        "CC-D05",
        "CC-D06",
        "CC-D08",
        "CC-D10",
        "CC-D11",
        "CC-021",
    )
    for workstream_id in ("CC-R02", "CC-R03", "CC-R04", "CC-R05", "CC-R06", "CC-R07"):
        assert registry[workstream_id][-2:] == ("CC-021", "CC-022")
    assert registry["CC-R08"] == (
        "CC-R01",
        "CC-R02",
        "CC-R03",
        "CC-R04",
        "CC-R05",
        "CC-R06",
        "CC-R07",
    )
    assert registry["CC-R09"] == (
        "CC-R08",
        "CC-D07",
        "CC-D10",
        "CC-021",
        "CC-022",
    )
    assert registry["CC-P52"] == ("CC-P45", "CC-P51", "CC-PUB01")


def test_canonical_integration_manifest_is_valid() -> None:
    state = validate_integration(ROOT)
    x03 = state.cards["CC-X03"]
    ledger = load_overseer_ledger(CONTRACT / "overseer", repository=ROOT)
    workstream_states, _ = integration_module._workstream_states(ledger)

    assert len(state.workstreams) == 69
    assert state.cards["CC-000"]["authorization"]["class"] == "FORMAL"
    assert x03["assignment"] == {
        "owner_id": "worker:ccx03-red",
        "state": "ASSIGNED",
        "task_id": "/root/ccx03_red_worker",
    }
    assert x03["authorization"] == {
        "authorized_by": {"id": "overseer", "type": "OVERSEER"},
        "class": "EXPLORATION_ONLY",
    }
    assert x03["candidate"] == {
        "artifacts": [
            {
                "byte_length": 5224,
                "path": "conformance/contract_kernel/v0/source_boundary/test_source_boundary.py",
                "sha256": "sha256:0b905dc49c883ca56b1a9e2492d6b12ba36b6879edf64c18524aa6e5673183de",
            },
            {
                "byte_length": 6010,
                "path": "conformance/contract_kernel/v0/source_boundary/EXPLORATORY_LEDGER.md",
                "sha256": "sha256:0393d7c2e0edc963c34730635dda0a2b1d5da1a2223895d5857db7a51272be17",
            },
        ],
        "base_commit": "17c4c21ee02a80fd2b963f47ba0ff3e37fcfd270",
        "evidence": [
            {
                "byte_length": 5607,
                "path": "conformance/contract_compiler/v0/evidence/CC-X03.json",
                "result": "PASS",
                "sha256": "sha256:1d6891a9a915373318f53235c7edb4b79d9ae818bb0c39d4784feb9326b877fb",
            }
        ],
        "head_commit": "f2a69ada9c52a10cc9e9b75030a1bda0094baa73",
        "head_tree": "2cbdc7fae0bde752cb188f5a253f6f1d95be32d4",
        "state": "ELIGIBLE",
    }
    assert x03["ledger"] == {"state": "NOT_STARTED"}
    assert x03["scopes"] == [
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/source_boundary/test_source_boundary.py",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/source_boundary/EXPLORATORY_LEDGER.md",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-X03.json",
        },
    ]
    assert state.workstreams["CC-X03"] == ()
    assert workstream_states["CC-X03"] == "COMPLETE"
    assert "CC-X03" not in state.selections
    assert state.cards["CC-R01"]["authorization"]["class"] == "BLOCKED"

    decisions = {
        "CC-D01": (),
        "CC-D02": ("CC-X02",),
        "CC-D03": ("CC-X01",),
        "CC-D04": ("CC-X04",),
        "CC-D05": ("CC-D01", "CC-D02", "CC-D03"),
        "CC-D06": ("CC-D05",),
        "CC-D07": ("CC-D06",),
        "CC-D08": ("CC-D02", "CC-D03", "CC-D05"),
        "CC-D10": ("CC-D07",),
        "CC-D11": ("CC-X03",),
        "CC-D13": ("CC-D01",),
        "CC-D14": (),
    }
    assert len(state.cards) == 31
    for workstream_id, dependencies in decisions.items():
        card = state.cards[workstream_id]
        assert card["assignment"] == {
            "owner_id": "overseer",
            "state": "ASSIGNED",
            "task_id": "/root",
        }
        assert card["authorization"]["class"] == "FORMAL"
        assert (
            tuple(
                binding["workstream_id"]
                for binding in card["authorization"]["dependency_bindings"]
            )
            == dependencies
        )
        assert card["candidate"] == {"state": "NONE"}
        assert card["ledger"] == {"state": "NOT_STARTED"}
        assert card["scopes"] == []
        assert workstream_states[workstream_id] == "COMPLETE"
        assert workstream_id not in state.selections
    d05_responsibility = state.cards["CC-D05"]["responsibility"]
    for phrase in (
        "exact ontology-powered non-expression seed metamodel",
        "atomic subject-predicate-object fact record",
        "internal candidate digest envelopes",
        "zero-scope decision",
        "no compiler",
        "stable public fact ID",
    ):
        assert phrase in d05_responsibility
    d06_responsibility = state.cards["CC-D06"]["responsibility"]
    for phrase in (
        "exactly three named 1..1 semantic roles",
        "closed ContractComposition",
        "fixed conceptual v0 role and composition identity constructors",
        "one accepted-temporal composition per ledger epoch",
        "governed-graph-only standalone structural case",
        "zero-scope decision",
        "no implementation",
        "public identifier",
    ):
        assert phrase in d06_responsibility
    d07_responsibility = state.cards["CC-D07"]["responsibility"]
    for phrase in (
        "protected replay-derived governance partition",
        "ProtocolLedger as sole write authority",
        "pre-event authority state",
        "explicit external bootstrap root",
        "existing accepted-graph lineage and query surface",
        "GovernanceContract semantic change",
        "same-type Excluded superseding revision",
        "selected topology does not supersede it",
        "exact stateful admission remain with D10",
        "zero-scope decision",
        "no implementation",
        "record schema",
        "second graph",
    ):
        assert phrase in d07_responsibility
    d08_responsibility = state.cards["CC-D08"]["responsibility"]
    for phrase in (
        "closed exact-location LinkML v0 support profile",
        "immutable D05 seed",
        "flat exactly-one expression extension",
        "deterministic internal structural identities",
        "Sphinx-rendered internal expansion guide",
        "zero-scope decision",
        "no parser",
        "stable public fact identifier",
    ):
        assert phrase in d08_responsibility
    d10_responsibility = state.cards["CC-D10"]["responsibility"]
    for phrase in (
        "strong non-inlined class-valued references",
        "same exact D06 role and replay-derived D07 partition",
        "whole-candidate refusal",
        "Entity-only relation endpoints",
        "Entity-or-Relation signal bearers",
        "global graph-record ID namespace",
        "referentially closed temporal views",
        "zero-scope decision",
        "no runtime sort",
        "CC-R06 retains production admission TDD",
    ):
        assert phrase in d10_responsibility


def test_cc010_activation_boundary_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-010")
    assert row["card"]["state"] == "PRESENT"
    path = CONTRACT / row["card"]["path"]
    source = path.read_bytes()
    assert row["card"]["byte_length"] == len(source)
    assert row["card"]["sha256"] == _digest(source)
    card = _read_json(path)
    assert card["workstream_id"] == row["workstream_id"] == "CC-010"
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())
    dependencies = load_program_registry(PROGRAM)["CC-010"]

    assert card["assignment"] == {
        "owner_id": "worker:cc010-conformance-protocol",
        "state": "ASSIGNED",
        "task_id": "/root/cc010_conformance_protocol",
    }
    assert card["authorization"]["class"] == "FORMAL"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert (
        tuple(
            binding["workstream_id"]
            for binding in card["authorization"]["dependency_bindings"]
        )
        == dependencies
    )
    assert card["scopes"] == [
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/corpus.schema.json",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/corpus.json",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/stage-matrix.json",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/checksums.json",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-010.json",
        },
        {
            "kind": "FILE",
            "path": "tests/contract_compiler/test_conformance_protocol.py",
        },
        {
            "kind": "FILE",
            "path": "docs/contract_compiler/conformance_protocol.md",
        },
    ]
    assert workstream_states["CC-010"] in {"ACTIVE", "COMPLETE"}
    assert "CC-010" not in manifest["selections"]
    responsibility = card["responsibility"]
    for required in (
        "three-corpus protocol",
        "path and ownership conventions",
        "membership and checksum grammar",
        "fixed validation tests",
        "no source or oracle content",
        "implementation or compiler code",
        "generated expectations",
        "public API",
        "packaging",
        "Docker",
        "release",
        "CC-R01",
    ):
        assert required in responsibility


def test_cc018_activation_boundary_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-018")
    assert row["card"]["state"] == "PRESENT"
    path = CONTRACT / row["card"]["path"]
    source = path.read_bytes()
    assert row["card"]["byte_length"] == len(source)
    assert row["card"]["sha256"] == _digest(source)
    card = _read_json(path)
    assert card["workstream_id"] == row["workstream_id"] == "CC-018"
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())
    dependencies = load_program_registry(PROGRAM)["CC-018"]

    assert card["assignment"] == {
        "owner_id": "worker:cc018-semantic-scenarios",
        "state": "ASSIGNED",
        "task_id": "/root/cc018_semantic_scenarios",
    }
    assert card["authorization"]["class"] == "FORMAL"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert (
        tuple(
            binding["workstream_id"]
            for binding in card["authorization"]["dependency_bindings"]
        )
        == dependencies
    )
    assert card["scopes"] == [
        {
            "kind": "FILE",
            "path": "conformance/contract_kernel/v0/requirements/scenarios.json",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-018.json",
        },
        {
            "kind": "FILE",
            "path": "tests/contract_compiler/test_semantic_scenario_requirements.py",
        },
    ]
    assert manifest["owner_separations"] == [
        {"left": "CC-011", "right": "CC-012"},
        {"left": "CC-011", "right": "CC-018"},
        {"left": "CC-012", "right": "CC-018"},
        {"left": "CC-013", "right": "CC-014"},
        {"left": "CC-013", "right": "CC-018"},
        {"left": "CC-014", "right": "CC-018"},
        {"left": "CC-015", "right": "CC-016"},
        {"left": "CC-015", "right": "CC-018"},
        {"left": "CC-016", "right": "CC-018"},
        {"left": "CC-017", "right": "CC-018"},
        {"left": "CC-018", "right": "CC-019"},
        {"left": "CC-018", "right": "CC-020"},
        {"left": "CC-019", "right": "CC-020"},
        {"left": "CC-021", "right": "CC-022"},
        {"left": "CC-022", "right": "CC-R09"},
    ]
    assert (
        workstream_states["CC-018"],
        card["candidate"]["state"],
        card["ledger"]["state"],
    ) in {
        ("ACTIVE", "NONE", "NOT_STARTED"),
        ("COMPLETE", "ELIGIBLE", "RECORDED"),
    }
    assert "CC-018" not in manifest["selections"]
    responsibility = card["responsibility"]
    for required in (
        "Populate one neutral machine-readable registry",
        "OD-005, OD-006, and OD-008",
        "stable unique scenario and requirement identities",
        "decision anchors",
        "path, schema, ordering, identity, and kind grammar remain CC-010 authority",
        "POSITIVE",
        "REFUSAL",
        "METAMORPHIC",
        "PARITY",
        "COMPOSITION_DELTA",
        "no source bytes or paths",
        "LinkML encoding",
        "direct fact triples",
        "expected facts, artifacts, diagnostics, or digests",
        "operations, traces, or outcomes",
        "themed vocabulary",
        "compiler or runtime implementation",
        "public API",
        "package",
        "Docker",
        "release",
        "corpus or checksum publication",
        "CC-R work",
    ):
        assert required in responsibility


@pytest.mark.parametrize(
    ("workstream_id", "assignment", "scopes", "required_phrases"),
    (
        (
            "CC-011",
            {
                "owner_id": "worker:cc011-themed-sources",
                "state": "ASSIGNED",
                "task_id": "/root/cc011_themed_sources",
            },
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/themed_fixture/sources",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-011.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_themed_source_corpus.py",
                },
            ],
            (
                "Author only the themed vertical LinkML source corpus",
                "CC-010",
                "CC-018",
                "CC-D14",
                "no direct-input triples or operation traces",
                "oracle or expected output",
            ),
        ),
        (
            "CC-013",
            {
                "owner_id": "worker:cc013-feature-inputs",
                "state": "ASSIGNED",
                "task_id": "/root/cc013_feature_inputs",
            },
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/feature_cases/inputs",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-013.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_feature_isolation_inputs.py",
                },
            ],
            (
                "Author only feature-isolation sources and direct inputs",
                "CC-010",
                "CC-X01",
                "CC-X02",
                "CC-018",
                "no oracle or expected output",
            ),
        ),
        (
            "CC-015",
            {
                "owner_id": "worker:cc015-neutral-inputs",
                "state": "ASSIGNED",
                "task_id": "/root/cc015_neutral_inputs",
            },
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/neutral_domain/sources",
                },
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/neutral_domain/traces/input",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-015.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_neutral_domain_inputs.py",
                },
            ],
            (
                "Author only neutral-domain LinkML sources and operation inputs",
                "CC-010",
                "CC-D05",
                "CC-D08",
                "CC-018",
                "no oracle or expected output",
            ),
        ),
    ),
)
def test_input_workstream_activation_boundaries_are_exact(
    workstream_id: str,
    assignment: dict[str, str],
    scopes: list[dict[str, str]],
    required_phrases: tuple[str, ...],
) -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, workstream_id)
    assert row["card"]["state"] == "PRESENT"
    path = CONTRACT / row["card"]["path"]
    source = path.read_bytes()
    assert row["card"]["byte_length"] == len(source)
    assert row["card"]["sha256"] == _digest(source)
    card = _read_json(path)
    assert card["workstream_id"] == row["workstream_id"] == workstream_id
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())

    assert card["assignment"] == assignment
    assert card["authorization"]["class"] == "FORMAL"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert (
        tuple(
            binding["workstream_id"]
            for binding in card["authorization"]["dependency_bindings"]
        )
        == load_program_registry(PROGRAM)[workstream_id]
    )
    assert card["scopes"] == scopes
    assert (
        workstream_states[workstream_id],
        card["candidate"]["state"],
        card["ledger"]["state"],
    ) in {
        ("ACTIVE", "NONE", "NOT_STARTED"),
        ("COMPLETE", "ELIGIBLE", "RECORDED"),
    }
    assert workstream_id not in manifest["selections"]
    responsibility = card["responsibility"]
    for required in required_phrases + (
        "compiler or runtime implementation",
        "public API",
        "package",
        "Docker",
        "release",
        "corpus or checksum publication",
        "CC-R work",
    ):
        assert required in responsibility


@pytest.mark.parametrize(
    (
        "workstream_id",
        "assignment",
        "paired_input_id",
        "scopes",
        "required_phrases",
    ),
    (
        (
            "CC-012",
            {
                "owner_id": "worker:cc012-themed-oracles",
                "state": "ASSIGNED",
                "task_id": "/root/cc012_themed_oracles",
            },
            "CC-011",
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/themed_fixture/oracle",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-012.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_themed_compilation_oracles.py",
                },
            ],
            (
                "Author only independently derived themed expected compilation artifacts",
                "source descriptors",
                "import graph",
                "declarations",
                "bindings",
                "elaboration",
                "facts",
                "logical artifact expectations",
                "Create no source or trace input, runtime artifact bytes or wire grammar",
            ),
        ),
        (
            "CC-014",
            {
                "owner_id": "worker:cc014-feature-oracles",
                "state": "ASSIGNED",
                "task_id": "/root/cc014_feature_oracles",
            },
            "CC-013",
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/feature_cases/oracle",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-014.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_feature_case_oracles.py",
                },
            ],
            (
                "Author only independently derived feature-case expected values",
                "CC-013 inputs",
                "no input source",
            ),
        ),
        (
            "CC-016",
            {
                "owner_id": "worker:cc016-neutral-oracles",
                "state": "ASSIGNED",
                "task_id": "/root/cc016_neutral_oracles",
            },
            "CC-015",
            [
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/neutral_domain/oracle",
                },
                {
                    "kind": "TREE",
                    "path": "conformance/contract_kernel/v0/neutral_domain/traces/oracle",
                },
                {
                    "kind": "FILE",
                    "path": "conformance/contract_compiler/v0/evidence/CC-016.json",
                },
                {
                    "kind": "FILE",
                    "path": "tests/contract_compiler/test_neutral_domain_oracles.py",
                },
            ],
            (
                "Author only independently derived neutral-domain expected values",
                "source compilation",
                "operation outcomes",
                "no source or operation input",
            ),
        ),
    ),
)
def test_oracle_workstream_activation_boundaries_are_exact(
    workstream_id: str,
    assignment: dict[str, str],
    paired_input_id: str,
    scopes: list[dict[str, str]],
    required_phrases: tuple[str, ...],
) -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, workstream_id)
    assert row["card"]["state"] == "PRESENT"
    path = CONTRACT / row["card"]["path"]
    source = path.read_bytes()
    assert row["card"]["byte_length"] == len(source)
    assert row["card"]["sha256"] == _digest(source)
    card = _read_json(path)
    cards = {
        current_id: _read_json(
            _card_path(INTEGRATION, _registry_row(manifest, current_id))
        )
        for current_id in (
            paired_input_id,
            workstream_id,
            "CC-018",
        )
    }
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())

    assert card["workstream_id"] == row["workstream_id"] == workstream_id
    assert card["assignment"] == assignment
    assert card["authorization"]["class"] == "BLOCKED"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert len(
        {current["assignment"]["owner_id"] for current in cards.values()}
    ) == len(cards)
    assert card["scopes"] == scopes
    assert (
        workstream_states[workstream_id],
        card["candidate"]["state"],
        card["ledger"]["state"],
    ) == ("PAUSED", "NONE", "NOT_STARTED")
    assert workstream_id not in manifest["selections"]
    responsibility = card["responsibility"]
    for required in required_phrases + (
        "by hand",
        "LinkML",
        "OntologyRegistry",
        "implementation under test",
        "compiler or runtime implementation",
        "public API",
        "package",
        "Docker",
        "release",
        "corpus or checksum publication",
        "CC-R work",
    ):
        assert required in responsibility


@pytest.mark.parametrize("workstream_id", ("CC-012", "CC-014", "CC-016"))
def test_oracle_activation_report_follows_its_base_commit(
    workstream_id: str,
) -> None:
    report = _read_json(
        CONTRACT / "overseer" / "evidence" / f"{workstream_id}-activation.json"
    )
    base_commit = report["base_commit"]
    _git(ROOT, "cat-file", "-e", f"{base_commit}^{{commit}}")
    base_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", base_commit)
    )
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in _raw_overseer_state().entries
        if 203 <= entry["sequence"] <= 207
    )

    assert report_time > base_time
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )


def test_oracle_workstream_activation_transaction_is_exact() -> None:
    workstream_ids = ("CC-012", "CC-014", "CC-016")
    ledger = _raw_overseer_state()
    transaction = tuple(
        entry for entry in ledger.entries if 203 <= entry["sequence"] <= 207
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000203",
        "OVR-000204",
        "OVR-000205",
        "OVR-000206",
        "OVR-000207",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "oracle-workstreams-activation-boundary",
        "oracle-workstreams-activation-verification",
        *workstream_ids,
    )
    revision_paths = {
        document["path"] for document in transaction[0]["data"]["documents"]
    }
    assert revision_paths == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-012-activation.json",
        "design/contract_compiler/overseer/evidence/CC-014-activation.json",
        "design/contract_compiler/overseer/evidence/CC-016-activation.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "design/contract_compiler/workstreams/CC-014/manifest.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    forbidden_paths = (
        "conformance/contract_kernel/v0/corpus.json",
        "conformance/contract_kernel/v0/checksums.json",
        "conformance/contract_kernel/v0/themed_fixture/oracle",
        "conformance/contract_kernel/v0/feature_cases/oracle",
        "conformance/contract_kernel/v0/neutral_domain/oracle",
        "conformance/contract_kernel/v0/neutral_domain/traces/oracle",
        "conformance/contract_compiler/v0/evidence/CC-012.json",
        "conformance/contract_compiler/v0/evidence/CC-014.json",
        "conformance/contract_compiler/v0/evidence/CC-016.json",
        "tests/contract_compiler/test_themed_compilation_oracles.py",
        "tests/contract_compiler/test_feature_case_oracles.py",
        "tests/contract_compiler/test_neutral_domain_oracles.py",
    )
    assert revision_paths.isdisjoint(forbidden_paths)

    manifest = _read_json(INTEGRATION)
    owner_ids = {
        _read_json(_card_path(INTEGRATION, _registry_row(manifest, workstream_id)))[
            "assignment"
        ]["owner_id"]
        for workstream_id in workstream_ids
    }
    assert len(owner_ids) == len(workstream_ids)
    blockers = {
        "CC-012": [
            "Content production waits for operator approval of fixture-local private resolver, profile, configuration, media-type, and source-blob tokens; CC-R07 retains runtime artifact bytes and wire grammar."
        ],
        "CC-014": [
            "Content production waits for the operator to decide whether the CC-013 explicit-false boundary splits into separate positive and refusal cases and to approve minimal private refusal and relations JSON shapes."
        ],
        "CC-016": [
            "Content production waits for operator approval of minimal private refusal and relations JSON shapes."
        ],
    }
    for offset, workstream_id in enumerate(workstream_ids, start=2):
        transition = transaction[offset]
        assert transition["data"]["workstream_id"] == workstream_id
        assert transition["data"]["previous_state"] == "PLANNED"
        assert transition["data"]["new_state"] == "ACTIVE"
        assert transition["data"]["bootstrap"] is True
        assert transition["data"]["blockers"] == blockers[workstream_id]
        assert transition["data"]["evidence_entry_ids"] == [
            "OVR-000203",
            "OVR-000204",
        ]


def test_small_shop_input_activation_boundary_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-021")
    assert manifest["revision"] == 2
    assert manifest["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    assert row["card"]["state"] == "PRESENT"
    path = CONTRACT / row["card"]["path"]
    source = path.read_bytes()
    assert row["card"]["byte_length"] == len(source)
    assert row["card"]["sha256"] == _digest(source)
    card = _read_json(path)
    states, _ = integration_module._workstream_states(_raw_overseer_state())

    assert card["workstream_id"] == "CC-021"
    assert card["assignment"] == {
        "owner_id": "worker:cc021-small-shop-inputs",
        "state": "ASSIGNED",
        "task_id": "/root/cc021_small_shop_inputs",
    }
    assert card["authorization"]["class"] == "FORMAL"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert tuple(
        binding["workstream_id"]
        for binding in card["authorization"]["dependency_bindings"]
    ) == ("CC-010", "CC-D03", "CC-D08", "CC-D11")
    assert card["scopes"] == [
        {
            "kind": "TREE",
            "path": "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-021.json",
        },
        {
            "kind": "FILE",
            "path": "tests/contract_compiler/test_small_shop_fixture_inputs.py",
        },
    ]
    assert card["candidate"] == {"state": "NONE"}
    assert card["ledger"] == {"state": "NOT_STARTED"}
    assert states["CC-021"] == "ACTIVE"
    assert "CC-021" not in manifest["selections"]
    for relative in (
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input",
        "conformance/contract_compiler/v0/evidence/CC-021.json",
        "tests/contract_compiler/test_small_shop_fixture_inputs.py",
    ):
        assert not (ROOT / relative).exists()
    for phrase in (
        "controlled Small Shop Fulfilment input bytes only",
        "no expected facts",
        "mappings",
        "recipes",
        "ProposedOperation",
        "outcomes",
        "compiler or runtime implementation",
        "protocol or accepted knowledge-graph state",
    ):
        assert phrase in card["responsibility"]

    assert _registry_row(manifest, "CC-022")["card"] == {"state": "ABSENT"}
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}


@pytest.mark.parametrize(
    ("workstream_id", "old_blocker"),
    (
        (
            "CC-012",
            "Content production waits for operator approval of fixture-local private resolver, profile, configuration, media-type, and source-blob tokens; CC-R07 retains runtime artifact bytes and wire grammar.",
        ),
        (
            "CC-014",
            "Content production waits for the operator to decide whether the CC-013 explicit-false boundary splits into separate positive and refusal cases and to approve minimal private refusal and relations JSON shapes.",
        ),
        (
            "CC-016",
            "Content production waits for operator approval of minimal private refusal and relations JSON shapes.",
        ),
    ),
)
def test_oracle_controls_pause_without_rewriting_their_owned_semantics(
    workstream_id: str,
    old_blocker: str,
) -> None:
    manifest = _read_json(INTEGRATION)
    card_path = CONTRACT / _registry_row(manifest, workstream_id)["card"]["path"]
    card = _read_json(card_path)
    prior = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_REANCHOR_BASE}:{card_path.relative_to(ROOT)}",
        )
    )
    states, _ = integration_module._workstream_states(_raw_overseer_state())
    anchor_gate = (
        "Resume only after CC-021 controlled Small Shop inputs and CC-022 "
        "independent Small Shop oracle are complete and fresh dependency bindings "
        "are issued."
    )

    for key in (
        "assignment",
        "candidate",
        "ledger",
        "responsibility",
        "schema",
        "scopes",
        "workstream_id",
    ):
        assert card[key] == prior[key]
    assert card["authorization"] == {
        "authorized_by": prior["authorization"]["authorized_by"],
        "blockers": [old_blocker, anchor_gate],
        "class": "BLOCKED",
    }
    assert _registry_row(manifest, workstream_id)["depends_on"][-2:] == [
        "CC-021",
        "CC-022",
    ]
    assert states[workstream_id] == "PAUSED"
    activation_report = (
        CONTRACT / "overseer" / "evidence" / f"{workstream_id}-activation.json"
    )
    assert (
        activation_report.read_bytes()
        == subprocess.run(
            [
                "git",
                "show",
                f"{SMALL_SHOP_REANCHOR_BASE}:{activation_report.relative_to(ROOT)}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    )


def test_small_shop_program_boundary_is_exact() -> None:
    source = PROGRAM.read_text(encoding="utf-8")
    for exact in (
        "RET-000 | Ontology alone produces no ABox.",
        "RET-010 | Create `O1`, distinct physical item `X1`, and `OrderContainsUnit(O1, X1)`.",
        "RET-020 | After `I1` and `I2` exist, create `P1` and two invoice-settlement relations.",
        "RET-030 | Preserve the supplier-order `B` correction at `e7` and bounded invoice `I2` correction at `e9`.",
        "RET-040 | Refuse the `e27` Event-to-Entity correlation with a typed gap.",
        "RET-050 | Refuse per-entity Event ordering with a typed gap.",
        "RET-060 | Reproduce the accepted result deterministically under later source integration.",
        "Quiet Bell, feature-isolation, and Greenhouse remain independent conformance controls.",
        "future external proposal producer",
        "The deterministic compiler never invokes it.",
        "Replay never invokes it.",
        "this program authorizes no skill implementation",
    ):
        assert exact in source


def test_small_shop_reanchor_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 209 <= entry["sequence"] <= 214)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(209, 215)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "small-shop-compiler-reanchor-boundary",
        "small-shop-compiler-reanchor-verification",
        "CC-012",
        "CC-014",
        "CC-016",
        "CC-021",
    )
    expected_paths = {
        "design/contract_compiler/program.md",
        "design/contract_compiler/integration.schema.json",
        "scripts/contract_compiler_integration.py",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "design/contract_compiler/workstreams/CC-014/manifest.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "design/contract_compiler/workstreams/CC-R01/manifest.json",
        "design/contract_compiler/workstreams/CC-021/manifest.json",
        "design/contract_compiler/overseer/evidence/CC-021-activation.json",
        "tests/test_contract_compiler_integration.py",
    }
    assert {
        item["path"] for item in transaction[0]["data"]["documents"]
    } == expected_paths
    assert transaction[0]["data"]["affected_ids"] == [
        "CC-000",
        "CC-012",
        "CC-014",
        "CC-016",
        "CC-021",
        "CC-022",
        "CC-R01",
        "CC-R02",
        "CC-R03",
        "CC-R04",
        "CC-R05",
        "CC-R06",
        "CC-R07",
        "CC-R09",
    ]
    for transition, workstream_id in zip(
        transaction[2:5], ("CC-012", "CC-014", "CC-016")
    ):
        assert transition["data"]["workstream_id"] == workstream_id
        assert transition["data"]["previous_state"] == "ACTIVE"
        assert transition["data"]["new_state"] == "PAUSED"
        assert transition["data"]["bootstrap"] is False
        assert transition["data"]["evidence_entry_ids"] == [
            "OVR-000209",
            "OVR-000210",
        ]
    activation = transaction[5]
    assert activation["data"]["workstream_id"] == "CC-021"
    assert activation["data"]["previous_state"] == "PLANNED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is True
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000209",
        "OVR-000210",
    ]

    base_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", SMALL_SHOP_REANCHOR_BASE)
    )
    report = _read_json(CONTRACT / "overseer" / "evidence" / "CC-021-activation.json")
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert report_time > base_time
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )


def test_small_shop_reanchor_preserves_adjacent_authority() -> None:
    unchanged = (
        "conformance/contract_kernel/v0/corpus.json",
        "conformance/contract_kernel/v0/checksums.json",
        "conformance/contract_kernel/v0/themed_fixture",
        "conformance/contract_kernel/v0/feature_cases",
        "conformance/contract_kernel/v0/neutral_domain",
        "scripts/contract_compiler_environment.py",
        "src/malleus",
        "pyproject.toml",
        ".github/workflows/tests.yml",
        ".github/workflows/release.yml",
        "design/PROTOCOL_FOUNDATION_GRAPH.md",
        "design/PROTOCOL_FOUNDATION_GRAPH.ttl",
        "design/GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md",
    )
    assert (
        _git(
            ROOT,
            "diff",
            "--name-only",
            SMALL_SHOP_REANCHOR_BASE,
            "--",
            *unchanged,
        )
        == ""
    )
    canonical = (ROOT / "design" / "PROTOCOL_FOUNDATION_GRAPH.ttl").read_text(
        encoding="utf-8"
    )
    assert "# Design graph revision: 21" in canonical
    assert "<https://malleus.dev/ontology-kg-realization/OKG-FX001>" in canonical


def test_formal_workstream_cannot_be_paused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = integration_module._workstream_states

    def pause_cc021(ledger_state):
        states, entries = original(ledger_state)
        states["CC-021"] = "PAUSED"
        return states, entries

    monkeypatch.setattr(integration_module, "_workstream_states", pause_cc021)
    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT)

    _assert_code(error, "CC000_WORKSTREAM_STATE")


def test_cc018_completion_checkpoint_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-018")
    card = _read_json(CONTRACT / row["card"]["path"])
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())

    assert card["candidate"] == {
        "artifacts": [
            {
                "byte_length": 5314,
                "path": "conformance/contract_kernel/v0/requirements/scenarios.json",
                "sha256": "sha256:758d2e69fefcfd4c8476a0c04988fba1763e31a73b4f6865da4d071568f4b662",
            },
            {
                "byte_length": 12751,
                "path": "tests/contract_compiler/test_semantic_scenario_requirements.py",
                "sha256": "sha256:7df913fb88fae1c11bde9e6c93ab1df17b39114ca0c2250bd5c3e171c1a7fcdb",
            },
        ],
        "base_commit": "b073f7d4b44205231a81bb22f3ad9328cc1c7541",
        "evidence": [
            {
                "byte_length": 6410,
                "path": "conformance/contract_compiler/v0/evidence/CC-018.json",
                "result": "PASS",
                "sha256": "sha256:b5391902dba8560179bbb59d5bec4e0c148b1a491a3fc46da7b609c7776c3fa7",
            }
        ],
        "head_commit": "ce9e61499a590c8fe9a077b976b9616e619fe97f",
        "head_tree": "58a158ad51f80ee6052d4236b1d3939947198b06",
        "state": "ELIGIBLE",
    }
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": "CC-018-WRK-000007",
        "head_hash": "sha256:a15037736d81a57f920ba8690298863b739f930e3a862f41e0543c6fb9be6c49",
        "path": "workstreams/CC-018/ledger",
        "state": "RECORDED",
    }
    assert workstream_states["CC-018"] == "COMPLETE"
    assert "CC-018" not in manifest["selections"]


@pytest.mark.parametrize(
    (
        "workstream_id",
        "base_commit",
        "head_commit",
        "head_tree",
        "touched_path_count",
        "report_byte_length",
        "report_sha256",
        "ledger_head_hash",
    ),
    (
        (
            "CC-011",
            "388b610ef1d8bfb135db5f981d3acac6641e5d78",
            "c0644e54b8b2ce3f74e6e63bebf842c8fae91cab",
            "b318f4844d405126296d4892bfe34298dac5023e",
            8,
            8646,
            "sha256:f0b7e91744fcd40b6787f82a6675daa0cdd5e7f39226c2b60d00bf19e62cf2e6",
            "sha256:8533fb9c70fc6b15f99af64b3f9665d59a9e3d1760da38fdb9cf1decfca243f3",
        ),
        (
            "CC-013",
            "c0644e54b8b2ce3f74e6e63bebf842c8fae91cab",
            "515a5688aced52d949eec4632d04330e9317f78f",
            "858465a8fd662094f1f40a39a5625c0fe33bb7f6",
            20,
            9589,
            "sha256:5b4a6ffcb481ada888b83519f80973c9d8ffe8bbf24a7d3a162234e56dcf6796",
            "sha256:9dfd665cf718ad1537fab5316e022f23b92a9a69b2a6102b91ad996abb800ab9",
        ),
        (
            "CC-015",
            "515a5688aced52d949eec4632d04330e9317f78f",
            "6fbe13dd2fdea3a557e393fe3238ebe7ff1946c1",
            "86330922d45dd4fae35d32c4a0835b631dc23787",
            14,
            7680,
            "sha256:23a94fd39fa673049b4ef19051130caa5b5d61e63dadc2c0b30878d8f8e9841c",
            "sha256:df82b8b72ee70f1f08f4718cfa535f7f9289c7b1d2bc56dc7d990575d7b4f0a4",
        ),
    ),
)
def test_input_workstream_completion_checkpoints_are_exact(
    workstream_id: str,
    base_commit: str,
    head_commit: str,
    head_tree: str,
    touched_path_count: int,
    report_byte_length: int,
    report_sha256: str,
    ledger_head_hash: str,
) -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, workstream_id)
    card = _read_json(CONTRACT / row["card"]["path"])
    report_path = f"conformance/contract_compiler/v0/evidence/{workstream_id}.json"
    report = _read_json(ROOT / report_path)
    expected_candidate = {
        "artifacts": report["artifacts"],
        "base_commit": base_commit,
        "evidence": [
            {
                "byte_length": report_byte_length,
                "path": report_path,
                "result": "PASS",
                "sha256": report_sha256,
            }
        ],
        "head_commit": head_commit,
        "head_tree": head_tree,
        "state": "ELIGIBLE",
    }

    assert card["candidate"] == expected_candidate
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": f"{workstream_id}-WRK-000007",
        "head_hash": ledger_head_hash,
        "path": f"workstreams/{workstream_id}/ledger",
        "state": "RECORDED",
    }
    touched = validate_candidate_history(
        ROOT,
        card["candidate"],
        allowed_scopes=card["scopes"],
        workstream_id=workstream_id,
    )
    assert len(touched) == touched_path_count
    assert set(touched) == {
        *(artifact["path"] for artifact in report["artifacts"]),
        report_path,
    }
    workstream_states, _ = integration_module._workstream_states(_raw_overseer_state())
    assert workstream_states[workstream_id] == "COMPLETE"
    assert workstream_id not in manifest["selections"]


@pytest.mark.parametrize("mutation", ("reverse", "reorder"))
def test_owner_separation_order_is_canonical(
    tmp_path: Path,
    mutation: str,
) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    edges = manifest["owner_separations"]
    if mutation == "reverse":
        edges[1]["left"], edges[1]["right"] = edges[1]["right"], edges[1]["left"]
    else:
        edges[0], edges[1] = edges[1], edges[0]
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_OWNER_POLICY_DRIFT")


def test_registry_card_pointer_must_match_its_workstream_row(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-D07")["card"] = copy.deepcopy(
        _registry_row(manifest, "CC-D08")["card"]
    )
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_CARD_ID")


def test_formal_worker_scope_requires_canonical_evidence_file(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def remove_evidence_scope(card: dict[str, Any]) -> None:
        card["scopes"] = [
            scope
            for scope in card["scopes"]
            if scope
            != {
                "kind": "FILE",
                "path": "conformance/contract_compiler/v0/evidence/CC-001.json",
            }
        ]

    _rewrite_card(path, manifest, "CC-001", remove_evidence_scope)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_EVIDENCE_SCOPE")


def test_candidate_evidence_schema_accepts_result_but_no_unknown_fields() -> None:
    schema = _read_json(CONTRACT / "integration.schema.json")
    validator = Draft202012Validator(
        {"$ref": "#/$defs/evidence", "$defs": schema["$defs"]}
    )
    evidence = {
        "path": "evidence/result.json",
        "byte_length": 17,
        "sha256": "sha256:" + "0" * 64,
        "result": "PASS",
    }

    assert list(validator.iter_errors(evidence)) == []
    assert list(validator.iter_errors({**evidence, "claim": "unchecked"}))


def test_candidate_has_one_dependency_binding_authority() -> None:
    schema = _read_json(CONTRACT / "integration.schema.json")
    validator = Draft202012Validator(
        {"$ref": "#/$defs/integrableCandidate", "$defs": schema["$defs"]}
    )
    artifact = {
        "path": "result.txt",
        "byte_length": 1,
        "sha256": "sha256:" + "0" * 64,
    }
    candidate = {
        "state": "ELIGIBLE",
        "base_commit": "0" * 40,
        "head_commit": "1" * 40,
        "head_tree": "2" * 40,
        "artifacts": [artifact],
        "evidence": [{**artifact, "result": "PASS"}],
    }

    assert list(validator.iter_errors(candidate)) == []
    assert list(validator.iter_errors({**candidate, "dependency_bindings": []}))


def test_direct_cli_entry_point_validates_the_draft() -> None:
    manifest = _read_json(CONTRACT / "integration.json")
    present_cards = sum(
        row["card"]["state"] == "PRESENT" for row in manifest["workstreams"]
    )
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "contract_compiler_integration.py"),
            "check-draft",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert f"validated 69 workstreams, {present_cards} cards," in result.stdout


@pytest.mark.parametrize("workflow", ["tests.yml", "release.yml"])
def test_workflows_delegate_to_the_fixed_local_runner_with_full_history(
    workflow: str,
) -> None:
    path = ROOT / ".github" / "workflows" / workflow
    source = path.read_text(encoding="utf-8")
    value = yaml.load(source, Loader=_UniqueYamlLoader)
    jobs = value["jobs"]
    guarded = [
        job
        for job in jobs.values()
        if any(
            step.get("run") == "python scripts/ci.py test --require-clean"
            for step in job["steps"]
        )
    ]

    assert guarded
    for job in guarded:
        checkout = next(
            step for step in job["steps"] if step.get("uses") == "actions/checkout@v4"
        )
        assert checkout["with"]["fetch-depth"] == 0
    required = {
        "python scripts/ci.py test --require-clean",
        "python scripts/ci.py docs --require-clean",
    }
    if workflow == "tests.yml":
        required.add("python scripts/ci.py package --require-clean")
        job = guarded[0]
        assert job["strategy"]["matrix"]["python-version"] == [
            "3.10",
            "3.11",
            "3.12",
            "3.13",
        ]
        package_step = next(
            step
            for step in job["steps"]
            if step.get("run") == "python scripts/ci.py package --require-clean"
        )
        assert "if" not in package_step
    else:
        required.add(
            "python scripts/ci.py package --artifacts /tmp/malleus-dist --require-clean"
        )
        assert "path: /tmp/malleus-dist/" in source
    for command in required:
        assert source.count(command) == 1
    for replaced in (
        "run: pytest",
        "python -m pytest",
        "python -m sphinx",
        "python -m build",
        "contract_compiler_integration.py check",
    ):
        assert replaced not in source


def test_owned_governance_markdown_has_no_trailing_whitespace() -> None:
    paths = sorted(CONTRACT.rglob("*.md"))
    paths.append(ROOT / "handover" / "2026-08-24-contract-compiler-overseer.md")

    offenders = [
        f"{path.relative_to(ROOT)}:{line_number}"
        for path in paths
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        )
        if line.endswith((" ", "\t"))
    ]

    assert offenders == []


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    path = tmp_path / "integration.json"
    source = INTEGRATION.read_text(encoding="utf-8")
    path.write_text(
        source.replace(
            '"schema": "malleus.contract-compiler.integration/v1"',
            '"schema": "malleus.contract-compiler.integration/v1",\n'
            '  "schema": "malleus.contract-compiler.integration/v1"',
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_JSON_DUPLICATE_KEY")


def test_unknown_manifest_fields_fail_closed(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    manifest["escape_hatch"] = True
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_SCHEMA_UNKNOWN_FIELD")


@pytest.mark.parametrize("unsafe", ["../escape", "/absolute", "tree/*"])
def test_scope_paths_are_exact_safe_repository_paths(
    tmp_path: Path, unsafe: str
) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def mutate(card: dict[str, Any]) -> None:
        card["scopes"][0]["path"] = unsafe

    _rewrite_card(path, manifest, "CC-X03", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_PATH_UNSAFE")


def test_manifest_registry_cannot_omit_a_program_workstream(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    manifest["workstreams"] = [
        row for row in manifest["workstreams"] if row["workstream_id"] != "CC-P52"
    ]
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_REGISTRY_COUNT")


def test_manifest_dependency_set_cannot_drift_from_program(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-001")["depends_on"] = []
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_REGISTRY_DRIFT")


def test_unknown_dependency_is_rejected_before_drift_reporting(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-001")["depends_on"] = ["CC-NOTREAL"]
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_UNKNOWN")


def test_self_dependency_is_rejected_before_drift_reporting(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-001")["depends_on"] = ["CC-001"]
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_SELF")


def test_dependency_cycle_is_rejected_before_drift_reporting(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-000")["depends_on"] = ["CC-001"]
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_CYCLE")


def test_formal_activation_lists_incomplete_dependencies(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def mutate(card: dict[str, Any]) -> None:
        card["assignment"] = {
            "state": "ASSIGNED",
            "owner_id": "worker:synthetic-r01",
            "task_id": "task:synthetic-r01",
        }
        card["authorization"] = {
            "class": "FORMAL",
            "authorized_by": {"id": "operator", "type": "OPERATOR"},
            "dependency_bindings": [],
        }

    _rewrite_card(path, manifest, "CC-R01", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_INCOMPLETE")
    assert "CC-010" not in str(error.value)
    assert "CC-D11" not in str(error.value)
    assert "CC-016" in str(error.value)


def test_dependency_integrated_head_commit_must_resolve(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    _rewrite_card(
        path,
        manifest,
        "CC-D13",
        lambda card: card["authorization"]["dependency_bindings"][0].update(
            integrated_head="f" * 40
        ),
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_GIT_OBJECT_MISSING")


def test_integrated_dependency_binding_uses_candidate_head(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    wrong_existing_head = _git(ROOT, "rev-parse", "HEAD")

    _rewrite_card(
        path,
        manifest,
        "CC-X01",
        lambda card: card["authorization"]["dependency_bindings"][0].update(
            integrated_head=wrong_existing_head
        ),
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_INTEGRATED_HEAD")


def test_nonintegrated_dependency_binding_uses_first_completion_commit(
    tmp_path: Path,
) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    later_descendant = _git(ROOT, "rev-parse", "HEAD")

    _rewrite_card(
        path,
        manifest,
        "CC-D13",
        lambda card: card["authorization"]["dependency_bindings"][0].update(
            integrated_head=later_descendant
        ),
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_INTEGRATED_HEAD")


def test_non_overseer_card_cannot_claim_reserved_scope(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def mutate(card: dict[str, Any]) -> None:
        card["scopes"] = [
            {"kind": "FILE", "path": "design/contract_compiler/integration.json"}
        ]

    _rewrite_card(path, manifest, "CC-X03", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_SCOPE_RESERVED")


def test_concurrent_cards_cannot_hold_overlapping_scopes(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    x03 = _read_json(_card_path(path, _registry_row(manifest, "CC-X03")))

    def mutate(card: dict[str, Any]) -> None:
        card["assignment"] = {
            "state": "ASSIGNED",
            "owner_id": "worker:synthetic-r01",
            "task_id": "task:synthetic-r01",
        }
        card["authorization"] = {
            "class": "EXPLORATION_ONLY",
            "authorized_by": {"id": "overseer", "type": "OVERSEER"},
        }
        card["scopes"] = copy.deepcopy(x03["scopes"])

    _rewrite_card(path, manifest, "CC-R01", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_SCOPE_OVERLAP")


def test_source_and_oracle_roles_require_distinct_owners(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _register_blocked_card(path, manifest, "CC-011", "worker:same")
    _register_blocked_card(path, manifest, "CC-012", "worker:same")

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_OWNER_SEPARATION")


def test_worker_cannot_authorize_its_own_card(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def mutate(card: dict[str, Any]) -> None:
        card["authorization"]["authorized_by"] = {
            "id": card["assignment"]["owner_id"],
            "type": "WORKER",
        }

    _rewrite_card(path, manifest, "CC-X03", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_SELF_AUTHORIZATION")


def test_overseer_ledger_anchor_must_match_the_reviewed_prefix(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    manifest["authority"]["overseer_ledger"]["head_hash"] = "sha256:" + "0" * 64
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_LEDGER_ANCHOR")


def test_linear_candidate_with_exact_scopes_and_evidence_is_accepted(
    tmp_path: Path,
) -> None:
    repository, base, head = _candidate_repository(tmp_path)

    touched = validate_candidate_history(
        repository,
        _candidate(repository, base, head),
        allowed_scopes=ALLOWED_SCOPES,
    )

    assert touched == ("allowed/result.txt", "evidence/checks.json")


def test_candidate_coordinates_require_full_commit_ids(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["head_commit"] = head[:12]

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_GIT_COMMIT_ID")


def test_candidate_commit_must_resolve(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["head_commit"] = "f" * 40

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_GIT_OBJECT_MISSING")


def test_candidate_head_must_descend_from_base(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    tree = _git(repository, "rev-parse", f"{head}^{{tree}}")
    orphan = _git(repository, "commit-tree", tree, "-m", "unrelated")
    candidate["head_commit"] = orphan
    candidate["head_tree"] = tree

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_GIT_ANCESTRY")


def test_candidate_history_must_be_linear(tmp_path: Path) -> None:
    repository = tmp_path / "nonlinear"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "CC-000 Test")
    _git(repository, "config", "user.email", "cc000@example.invalid")
    (repository / "allowed").mkdir()
    (repository / "allowed" / "base.txt").write_text("base\n", encoding="utf-8")
    base = _commit(repository, "base")
    _git(repository, "checkout", "-b", "side")
    (repository / "allowed" / "side.txt").write_text("side\n", encoding="utf-8")
    _commit(repository, "side")
    _git(repository, "checkout", "main")
    (repository / "allowed" / "result.txt").write_text("result\n", encoding="utf-8")
    (repository / "evidence").mkdir()
    (repository / "evidence" / "checks.json").write_text(
        '{"result":"PASS"}\n', encoding="utf-8"
    )
    _commit(repository, "main")
    _git(repository, "merge", "--no-ff", "side", "-m", "merge")
    head = _git(repository, "rev-parse", "HEAD")
    candidate = _candidate(repository, base, head)

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=({"kind": "TREE", "path": "allowed"},),
        )

    _assert_code(error, "CC000_GIT_NONLINEAR")


def test_x03_history_union_catches_themed_paths_deleted_before_head(
    tmp_path: Path,
) -> None:
    repository, base, _ = _candidate_repository(tmp_path)
    themed = (
        "conformance/contract_kernel/v0/quiet_bell_archive/sources/v1.0.0/catalog/notices.yaml",
        "conformance/contract_kernel/v0/quiet_bell_archive/sources/v1.0.0/catalog/observations.yaml",
        "conformance/contract_kernel/v0/quiet_bell_archive/sources/v1.0.0/root.yaml",
        "conformance/contract_kernel/v0/quiet_bell_archive/sources/v1.0.0/shared/identity.yaml",
    )
    for relative in themed:
        path = repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("name: quarantined\n", encoding="utf-8")
    _commit(repository, "introduce unowned themed paths")
    for relative in themed:
        (repository / relative).unlink()
    head = _commit(repository, "delete unowned themed paths")
    candidate = _candidate(repository, base, head)

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_SCOPE_VIOLATION")
    assert all(relative in str(error.value) for relative in themed)


def test_candidate_head_tree_is_bound_exactly(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["head_tree"] = base

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_CANDIDATE_TREE")


def test_candidate_artifact_digest_is_verified_at_head(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["artifacts"][0]["sha256"] = "sha256:" + "0" * 64

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_ARTIFACT_DIGEST")


def test_failed_evidence_cannot_gate_candidate(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["evidence"][0]["result"] = "FAIL"

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_EVIDENCE_FAILED")


def test_top_level_pass_cannot_mask_a_failed_evidence_check(tmp_path: Path) -> None:
    repository, base, _ = _candidate_repository(tmp_path)
    report_path = repository / "evidence" / "checks.json"
    report = _read_json(report_path)
    report["result"] = "PASS"
    report["checks"][0]["result"] = "FAIL"
    _write_json(report_path, report)
    head = _commit(repository, "attempt evidence bypass")
    candidate = _candidate(repository, base, head)

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_EVIDENCE_INVALID")


def test_selected_workstream_must_be_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _copy_manifest_bundle(tmp_path)
    for row in manifest["workstreams"]:
        if row["workstream_id"] != "CC-000":
            row["card"] = {"state": "ABSENT"}
    result_commit = "55d9da3b58d77d49bdcf449c376a26231d410824"
    result_report = _git(
        ROOT,
        "show",
        f"{result_commit}:design/contract_compiler/workstreams/CC-000/evidence/result.json",
    )
    report_source = result_report.encode("utf-8")

    def integrate(card: dict[str, Any]) -> None:
        report = json.loads(result_report)
        card["candidate"] = {
            "artifacts": report["artifacts"],
            "base_commit": report["base_commit"],
            "evidence": [
                {
                    "byte_length": len(report_source),
                    "path": "design/contract_compiler/workstreams/CC-000/evidence/result.json",
                    "result": "PASS",
                    "sha256": _digest(report_source),
                }
            ],
            "head_commit": result_commit,
            "head_tree": _git(ROOT, "rev-parse", f"{result_commit}^{{tree}}"),
            "state": "INTEGRATED",
        }

    _rewrite_card(manifest_path, manifest, "CC-000", integrate)
    manifest["selections"] = ["CC-000"]
    _write_json(manifest_path, manifest)
    ledger = load_overseer_ledger(CONTRACT / "overseer", repository=ROOT)
    active_index = next(
        index
        for index, entry in enumerate(ledger.entries)
        if entry["entry_type"] == "WORKSTREAM_STATE"
        and entry["data"]["workstream_id"] == "CC-000"
        and entry["data"]["new_state"] == "ACTIVE"
    )
    active_entry = ledger.entries[active_index]
    manifest["authority"]["overseer_ledger"].update(
        {
            "entry_count": active_index + 1,
            "head_entry_id": active_entry["entry_id"],
            "head_hash": active_entry["entry_hash"],
        }
    )
    _write_json(manifest_path, manifest)
    active_prefix = replace(ledger, entries=ledger.entries[: active_index + 1])
    monkeypatch.setattr(
        integration_module, "load_ledger", lambda *args, **kwargs: active_prefix
    )
    monkeypatch.setattr(
        integration_module,
        "_validate_worker_ledger",
        lambda *args, **kwargs: {
            phase: {"result": "EXPECTED_FAILURE" if phase == "RED" else "PASS"}
            for phase in integration_module.TDD_PHASES
        },
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, manifest_path)

    _assert_code(error, "CC000_SELECTION_STATE")


def test_selected_workstream_must_be_formally_authorized(tmp_path: Path) -> None:
    manifest_path, manifest = _copy_manifest_bundle(tmp_path)
    result_commit = "55d9da3b58d77d49bdcf449c376a26231d410824"
    result_report = _git(
        ROOT,
        "show",
        f"{result_commit}:design/contract_compiler/workstreams/CC-000/evidence/result.json",
    )
    report_source = result_report.encode("utf-8")

    def integrate(card: dict[str, Any]) -> None:
        report = json.loads(result_report)
        card["candidate"] = {
            "artifacts": report["artifacts"],
            "base_commit": report["base_commit"],
            "evidence": [
                {
                    "byte_length": len(report_source),
                    "path": "design/contract_compiler/workstreams/CC-000/evidence/result.json",
                    "result": "PASS",
                    "sha256": _digest(report_source),
                }
            ],
            "head_commit": result_commit,
            "head_tree": _git(ROOT, "rev-parse", f"{result_commit}^{{tree}}"),
            "state": "INTEGRATED",
        }

    _rewrite_card(manifest_path, manifest, "CC-X03", integrate)
    x03_digest = _registry_row(manifest, "CC-X03")["card"]["sha256"]
    _rewrite_card(
        manifest_path,
        manifest,
        "CC-D11",
        lambda card: card["authorization"]["dependency_bindings"][0].update(
            card_sha256=x03_digest,
            integrated_head=result_commit,
        ),
    )
    d11_digest = _registry_row(manifest, "CC-D11")["card"]["sha256"]
    _rewrite_card(
        manifest_path,
        manifest,
        "CC-010",
        lambda card: next(
            binding
            for binding in card["authorization"]["dependency_bindings"]
            if binding["workstream_id"] == "CC-D11"
        ).update(card_sha256=d11_digest),
    )
    cc010_digest = _registry_row(manifest, "CC-010")["card"]["sha256"]
    _rewrite_card(
        manifest_path,
        manifest,
        "CC-018",
        lambda card: next(
            binding
            for binding in card["authorization"]["dependency_bindings"]
            if binding["workstream_id"] == "CC-010"
        ).update(card_sha256=cc010_digest),
    )
    cc018_digest = _registry_row(manifest, "CC-018")["card"]["sha256"]

    def rebind_active_input(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-018"]["card_sha256"] = cc018_digest

    for workstream_id in ("CC-011", "CC-013", "CC-015"):
        _rewrite_card(manifest_path, manifest, workstream_id, rebind_active_input)

    def rebind_small_shop_input(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-D11"]["card_sha256"] = d11_digest

    _rewrite_card(manifest_path, manifest, "CC-021", rebind_small_shop_input)
    manifest["selections"] = ["CC-X03"]
    _write_json(manifest_path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, manifest_path)

    _assert_code(error, "CC000_SELECTION_AUTHORIZATION")


def test_quarantined_candidate_cannot_gate_integration(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["state"] = "QUARANTINED"
    candidate["reason"] = "Exploratory history is not integration authority."

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(repository, candidate, allowed_scopes=ALLOWED_SCOPES)

    _assert_code(error, "CC000_CANDIDATE_STATE")


def test_research_tdd_phases_must_be_unique() -> None:
    results = _complete_tdd_results()
    results.insert(2, dict(results[1]))

    with pytest.raises(IntegrationValidationError) as error:
        validate_tdd_gate("CC-R01", results)

    _assert_code(error, "CC000_TDD_DUPLICATE")


def test_research_tdd_phases_must_follow_canonical_order() -> None:
    results = _complete_tdd_results()
    results[1], results[2] = results[2], results[1]

    with pytest.raises(IntegrationValidationError) as error:
        validate_tdd_gate("CC-R01", results)

    _assert_code(error, "CC000_TDD_ORDER")


@pytest.mark.parametrize(
    ("phase", "wrong_result"),
    [
        ("RED", "PASS"),
        ("RED", "NOT_APPLICABLE"),
        ("GREEN", "EXPECTED_FAILURE"),
        ("GREEN", "NOT_APPLICABLE"),
        ("SLICE", "EXPECTED_FAILURE"),
        ("SLICE", "NOT_APPLICABLE"),
        ("DISPROOF", "EXPECTED_FAILURE"),
        ("DISPROOF", "NOT_APPLICABLE"),
        ("REGRESSION", "EXPECTED_FAILURE"),
        ("REGRESSION", "NOT_APPLICABLE"),
        ("ATTEST", "EXPECTED_FAILURE"),
        ("ATTEST", "NOT_APPLICABLE"),
    ],
)
def test_research_tdd_result_matrix_is_exact(
    phase: str,
    wrong_result: str,
) -> None:
    results = _complete_tdd_results()
    next(result for result in results if result["phase"] == phase)["result"] = (
        wrong_result
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_tdd_gate("CC-R01", results)

    _assert_code(error, "CC000_TDD_RESULT")


@pytest.mark.parametrize("package_result", ["EXPECTED_FAILURE", "NOT_APPLICABLE"])
def test_research_package_phase_has_only_two_exact_results(
    package_result: str,
) -> None:
    results = _complete_tdd_results()
    package = next(result for result in results if result["phase"] == "PACKAGE")
    package["result"] = package_result

    if package_result == "NOT_APPLICABLE":
        validate_tdd_gate("CC-R01", results)
        return
    with pytest.raises(IntegrationValidationError) as error:
        validate_tdd_gate("CC-R01", results)

    _assert_code(error, "CC000_TDD_RESULT")


def test_worker_correction_replaces_a_tdd_result_without_reordering_it() -> None:
    entries = [
        {
            "data": {"phase": "RED", "result": "EXPECTED_FAILURE"},
            "entry_id": "CC-R01-WRK-000001",
            "entry_type": "TDD_RESULT",
        },
        {
            "data": {"phase": "GREEN", "result": "NOT_APPLICABLE"},
            "entry_id": "CC-R01-WRK-000002",
            "entry_type": "TDD_RESULT",
        },
        {
            "data": {
                "supersedes_entry_id": "CC-R01-WRK-000002",
                "reason": "Replace the malformed GREEN observation.",
            },
            "entry_id": "CC-R01-WRK-000003",
            "entry_type": "CORRECTION",
        },
        {
            "data": {"phase": "GREEN", "result": "PASS"},
            "entry_id": "CC-R01-WRK-000004",
            "entry_type": "TDD_RESULT",
        },
        *[
            {
                "data": {"phase": phase, "result": "PASS"},
                "entry_id": f"CC-R01-WRK-{sequence:06d}",
                "entry_type": "TDD_RESULT",
            }
            for sequence, phase in enumerate(
                integration_module.TDD_PHASES[2:],
                start=5,
            )
        ],
    ]

    active = integration_module._active_tdd_results(entries)

    assert [result["phase"] for result in active] == list(integration_module.TDD_PHASES)
    validate_tdd_gate("CC-R01", active)


@pytest.mark.parametrize("candidate_state", ["ELIGIBLE", "INTEGRATED"])
def test_research_candidate_cannot_reach_an_integration_gate_before_tdd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    candidate_state: str,
) -> None:
    manifest_path, manifest = _copy_manifest_bundle(tmp_path)
    _rewrite_card(
        manifest_path,
        manifest,
        "CC-R01",
        lambda card: card.update(candidate=_syntactic_candidate(candidate_state)),
    )
    monkeypatch.setattr(
        integration_module,
        "load_ledger",
        lambda *args, **kwargs: _raw_overseer_state(),
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, manifest_path)

    _assert_code(error, "CC000_TDD_INCOMPLETE")


def test_research_workstream_cannot_be_complete_before_tdd_gate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, _ = _copy_manifest_bundle(tmp_path)
    original = integration_module._workstream_states
    monkeypatch.setattr(
        integration_module,
        "load_ledger",
        lambda *args, **kwargs: _raw_overseer_state(),
    )

    def completed_r01(ledger_state):
        states, entries = original(ledger_state)
        states["CC-R01"] = "COMPLETE"
        return states, entries

    monkeypatch.setattr(integration_module, "_workstream_states", completed_r01)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, manifest_path)

    _assert_code(error, "CC000_TDD_INCOMPLETE")

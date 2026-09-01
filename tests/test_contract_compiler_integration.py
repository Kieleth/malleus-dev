from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tomllib
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
SMALL_SHOP_ACTIVATION_COMMIT = "37cf69d57ee85f8a5f936661f1cf5fbdb975573b"
SMALL_SHOP_OPERATOR_APPROVAL = "927ab183e33de09d62a3a6dba834306d54f35962"
SMALL_SHOP_PROVISIONAL_COMMIT = "9b2afa8327bac1dd18ddca281e10f736cb1337fc"
SMALL_SHOP_PROVISIONAL_TREE = "ae4a2468683ad681a96a66a4ef0a0005ebe510fb"
SMALL_SHOP_AUTHORITY_COMMIT = "f6b2bf96ae04351ec7ce29c080e57b58a8b7cea6"
SMALL_SHOP_CANDIDATE_COMMIT = "39f41544ff47c60663d1eed7b4ec8959165f37e4"
SMALL_SHOP_CANDIDATE_TREE = "4d50c14af6dd0f4c84dbd89c6407b02711d3bb35"
SMALL_SHOP_INPUT_COMPLETION_COMMIT = "e5535033d8f1886271d827ddeed4662196410cdf"
SMALL_SHOP_ORACLE_DECISION_COMMIT = "453e01fba105fd97cabef6c2b99777a2ade39538"
SMALL_SHOP_ORACLE_DECISION_TREE = "cb56d2f0079c8cfc4eff5b3fe42b7737fdb5346f"
SMALL_SHOP_ORACLE_DECISION_HASH = (
    "sha256:1b16128d623cc7b1348f98f636be83d7a1514011b63d112ad09dbb3946564d61"
)
SMALL_SHOP_ORACLE_ACTIVATION_COMMIT = "870c993fe2442b40fd1934edbf00003033c591b1"
SMALL_SHOP_ORACLE_CANDIDATE_COMMIT = "660cb408b0c28785d96731d976e6cbc1aeb9a69c"
SMALL_SHOP_ORACLE_CANDIDATE_TREE = "cc46360437de6a2ad07d875e4e54404b7e7ce06e"
QUIET_BELL_ORACLE_ACTIVATION_COMMIT = "c6e3616b292050ae0bbd0be9af40ca83ae9a91d1"
QUIET_BELL_REACTIVATION_BASE = "d56c30f85b92d7452ca126d488bf027b42ee67f5"
QUIET_BELL_REACTIVATION_COMMIT = "67560d41be90601e1d01235f3730e16f3e01cd91"
QUIET_BELL_REACTIVATION_REPAIR_COMMIT = "a8f87cb453f861bba611b9beff0e564a36c40a2b"
QUIET_BELL_REACTIVATION_ENTRY = "OVR-000236"
QUIET_BELL_AUTHORITY_HARDENING_COMMIT = "cba6de054bfc1241460998b8744efe02adce9ae4"
QUIET_BELL_AUTHORITY_HARDENING_ENTRY = "OVR-000240"
QUIET_BELL_CLEAN_BASE_HARDENING_COMMIT = "1afaef29ad20ec503721488c9edbef3bfdadbb18"
QUIET_BELL_CLEAN_BASE_CLOSURE_COMMIT = "1d17a613940a26fac70debbecbf6fab29e318cf7"
QUIET_BELL_CANDIDATE_BASE = "195a369636f9fe9ce1a0e8f4cb9d950836164e79"
QUIET_BELL_CANDIDATE_COMMIT = "9cc23c445711fa07df0103dac85c7196ada14d81"
QUIET_BELL_CANDIDATE_TREE = "24a63271ad701960c9257f75ee874078066631e6"
QUIET_BELL_COMPLETION_COMMIT = "8d04fc285070a0594aabccef0b926a8cec3bb132"
QUIET_BELL_CANDIDATE_PATHS = {
    "conformance/contract_compiler/v0/evidence/CC-012.json",
    "conformance/contract_kernel/v0/themed_fixture/oracle/quiet_bell.json",
    "tests/contract_compiler/test_themed_compilation_oracles.py",
}
QUIET_BELL_DEPENDENCIES = (
    "CC-010",
    "CC-D02",
    "CC-D03",
    "CC-D05",
    "CC-D06",
    "CC-D08",
    "CC-011",
    "CC-021",
    "CC-022",
)
QUIET_BELL_PRIVATE_TOKENS = (
    "TEST_ONLY_STRICT_MALLEUS_RESOLVER_V0",
    "TEST_ONLY_LINKML_V0_PROFILE",
    "TEST_ONLY_REPOSITORY_FILE_NETWORK_DENIED_V0",
    "TEST_ONLY_JSON_SHAPED_YAML",
    "TEST_ONLY_SOURCE_BLOB_SHA256_<64-lowercase-hex>",
    "ACCEPT",
    '{"outcome":"REFUSE"}',
    "SAME",
    "DIFFERENT",
    "NOT_CLAIMED",
)
QUIET_BELL_ORACLE_RESPONSIBILITY = (
    "Author only independently derived themed expected compilation artifacts under "
    "the exact CC-010 themed_fixture/oracle prefix, using the accepted decisions and "
    "completed CC-011 sources. Own source descriptors, import graph, declarations, "
    "bindings, elaboration, facts, logical artifact expectations, one canonical "
    "verification report, and one fixed oracle validation test. Represent expectations "
    "only as private fixture-local logical JSON with the closed test-only labels "
    "TEST_ONLY_STRICT_MALLEUS_RESOLVER_V0, TEST_ONLY_LINKML_V0_PROFILE, "
    "TEST_ONLY_REPOSITORY_FILE_NETWORK_DENIED_V0, TEST_ONLY_JSON_SHAPED_YAML, and "
    "TEST_ONLY_SOURCE_BLOB_SHA256_<64-lowercase-hex>. Allowed outcomes are ACCEPT or "
    'the minimal {"outcome":"REFUSE"}; allowed comparisons are SAME, DIFFERENT, '
    "and NOT_CLAIMED, where NOT_CLAIMED is an explicit nonassertion. These labels and "
    "JSON bytes are test-only, non-public, carry no compatibility contract, are never "
    "compiler input, and define no runtime artifact bytes or wire grammar. Write every "
    "oracle by hand from the exact Quiet Bell sources and accepted decisions, never "
    "generate or export it from LinkML, OntologyRegistry, or the implementation under "
    "test. The completed Small Shop answer key is process, representation, and testing "
    "precedent only; use no Small Shop domain values, facts, identifiers, or derivations. "
    "Do not assume every Quiet Bell source accepts; retain any contradiction as RED. "
    "Create no source or trace input, runtime artifact bytes or wire grammar, compiler "
    "or runtime implementation, public API, package, Docker, release, corpus or checksum "
    "publication, selection, integration, or CC-R work."
)
GREENHOUSE_REACTIVATION_BASE = "c12e52ea743d8809c91974653b62192b166753e9"
GREENHOUSE_ACTIVATION_ENTRY = "OVR-000263"
GREENHOUSE_CANDIDATE_BASE = "6969f193eb9e57f815bb73c38b7094a980e1642c"
GREENHOUSE_CANDIDATE_COMMIT = "f654d215a5877061512f8125147fe0f8f6a26db3"
GREENHOUSE_CANDIDATE_TREE = "760ca219e9b47ff7c70687b0dd4fe5caf7bbb00b"
GREENHOUSE_COMPLETION_COMMIT = "5f185469832a1ec1653f0e9ace2de697f3c4726d"
GREENHOUSE_CANDIDATE_PATHS = {
    "conformance/contract_compiler/v0/evidence/CC-016.json",
    "conformance/contract_kernel/v0/neutral_domain/oracle/greenhouse.json",
    "conformance/contract_kernel/v0/neutral_domain/traces/oracle/compile-source-outcomes.json",
    "tests/contract_compiler/test_neutral_domain_oracles.py",
}
GREENHOUSE_DEPENDENCIES = (
    "CC-010",
    "CC-D05",
    "CC-D06",
    "CC-D08",
    "CC-015",
    "CC-021",
    "CC-022",
)
GREENHOUSE_PRIVATE_TOKENS = (
    "ACCEPT",
    '{"outcome":"REFUSE"}',
    "SAME",
    "DIFFERENT",
    "NOT_CLAIMED",
)
GREENHOUSE_ORACLE_RESPONSIBILITY = (
    "Author only independently derived neutral-domain expected values under the exact "
    "CC-010 neutral_domain/oracle and neutral_domain/traces/oracle prefixes, using "
    "accepted decisions and completed CC-015 inputs. Own source compilation "
    "expectations, operation outcomes, one canonical verification report, and one "
    "fixed oracle validation test. Represent expectations only as private "
    "fixture-local logical JSON. Allowed outcomes are ACCEPT or the minimal "
    '{"outcome":"REFUSE"}; allowed relations are SAME, DIFFERENT, and NOT_CLAIMED, '
    "where NOT_CLAIMED is an explicit nonassertion. These labels and JSON bytes are "
    "test-only, non-public, carry no compatibility contract, are never compiler input, "
    "and define no runtime artifact bytes or wire grammar. Write every oracle by hand "
    "from the exact Greenhouse sources and accepted decisions, never generate or "
    "export it from LinkML, OntologyRegistry, or the implementation under test. The "
    "completed Quiet Bell answer key transfers process technique only; use no Quiet "
    "Bell expected value, fact, identifier, derivation, helper, interface, or semantic "
    "dependency. Do not assume every Greenhouse source accepts; retain any contradiction "
    "as RED. Create no source or operation input, themed vocabulary, compiler or runtime "
    "implementation, public API, package, Docker, release, corpus or checksum "
    "publication, selection, integration, or CC-R work."
)
SMALL_SHOP_INPUT_ROOT = (
    "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input"
)
SMALL_SHOP_ORACLE_ROOT = (
    "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/oracle"
)
SMALL_SHOP_CANDIDATE_PATHS = {
    "conformance/contract_compiler/v0/evidence/CC-021.json",
    f"{SMALL_SHOP_INPUT_ROOT}/configuration/ret-010-selection.json",
    f"{SMALL_SHOP_INPUT_ROOT}/configuration/time-context.json",
    f"{SMALL_SHOP_INPUT_ROOT}/manifest.json",
    "tests/contract_compiler/test_small_shop_fixture_inputs.py",
}
SMALL_SHOP_INHERITED_PATHS = {
    f"{SMALL_SHOP_INPUT_ROOT}/sources/inventory-units.csv",
    f"{SMALL_SHOP_INPUT_ROOT}/sources/warehouse.jsonl",
    f"{SMALL_SHOP_INPUT_ROOT}/tbox/small-shop-description-only.yaml",
    f"{SMALL_SHOP_INPUT_ROOT}/tbox/small-shop-root-instances.yaml",
    f"{SMALL_SHOP_INPUT_ROOT}/tbox/small-shop.yaml",
}
SMALL_SHOP_RESPONSIBILITY = (
    "Author controlled Small Shop Fulfilment ontology and domain source bytes under "
    "the exact research input prefix, declarative parameter members with manifest "
    "roles SCENARIO_SELECTION and SOURCE_TIME_CONTEXT, one canonical verification "
    "report, and one fixed input validation test. The parameter members may select "
    "the retained occurrence and entity tuple and declare fixture-local source "
    "format, calendar, synthetic year, and timezone. They are raw parameters, not "
    "mapping or transformation code, and must contain no normalized values or "
    "outputs. Inputs may contain no expected facts, mappings, transformations, "
    "identities, recipes, ProposedOperation values, candidates, evidence outcomes, "
    "compiler or runtime implementation, protocol or accepted knowledge-graph "
    "state, replay receipts, or research-journal findings. Create no CC-022 oracle "
    "or CC-R work, corpus or checksum publication, public API, package, Docker, or "
    "release change."
)
SMALL_SHOP_ORACLE_RESPONSIBILITY = (
    "Hand-author exactly two private fixture-local logical JSON answer-key members, "
    "tbox-expectations.json and ret-000-ret-010.json, plus one canonical verification "
    "report and one fixed oracle validation test. Bind the approved Small Shop oracle "
    "decision, accepted OD-002, OD-003, OD-005, OD-006, OD-008, OD-010, and OD-011, "
    "OKG-FX001, and completed CC-021 inputs. Never generate or export these bytes from "
    "LinkML, OntologyRegistry, compiler or runtime code, GraphRecipe, protocol state, or "
    "implementation. They are independently hand-authored test-only evidence, never "
    "compiler input, and define no public format or compatibility contract. Own only "
    "baseline ACCEPT; description-only ACCEPT with source DIFFERENT and semantic SAME; "
    "root-instances atomic REFUSE; ontology-only zero population and zero "
    "ProposedOperation values; accepted e27, O1, and X1; X1-to-X lookup; normalized "
    "fixture-derived time; logical O1, X1, and ORDER_CONTAINS_UNIT; passive exact review; "
    "closed derivation; and retained Event-correlation RED. Exclude a full imported-fact "
    "oracle, public tokens, mappings, transformations, final identities, public ABox, "
    "recipes, operation bytes or ordering, compiler or runtime implementation, staging, "
    "protocol, ledger, knowledge graph, replay, journal mutation, corpus or checksum "
    "publication, package, release, selection, integration, and all CC-R work."
)


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
    template["authorization"] = {
        "authorized_by": {"id": "overseer", "type": "OVERSEER"},
        "blockers": ["Synthetic ownership test."],
        "class": "BLOCKED",
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


def _git_bytes(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
    )
    return result.stdout


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


def _add_candidate_worker_ledger(
    repository: Path,
    candidate: dict[str, Any],
    workstream_id: str,
) -> tuple[dict[str, Any], integration_module.WorkerLedgerValidation]:
    ledger = (
        repository
        / "design"
        / "contract_compiler"
        / "workstreams"
        / workstream_id
        / "ledger"
    )
    entries = ledger / "entries"
    entries.mkdir(parents=True)
    entry = {
        "actor_id": f"worker:{workstream_id.lower()}",
        "data": {
            "artifacts": [],
            "command": "pytest -q",
            "observed": "One expected missing-implementation failure.",
            "phase": "RED",
            "result": "EXPECTED_FAILURE",
        },
        "entry_id": f"{workstream_id}-WRK-000001",
        "entry_type": "TDD_RESULT",
        "previous_entry_hash": "GENESIS",
        "recorded_at": "2026-01-01T00:00:00Z",
        "schema": "malleus.contract-compiler.worker-ledger-entry/v1",
        "sequence": 1,
        "summary": "Record RED.",
        "workstream_id": workstream_id,
    }
    entry["entry_hash"] = integration_module.worker_entry_hash(entry)
    entry_path = entries / f"{workstream_id}-WRK-000001.json"
    _write_json(entry_path, entry)
    head_static = {
        "canonicalization": "malleus-canonical-json-v1",
        "schema": "malleus.contract-compiler.worker-ledger-head/v1",
        "workstream_id": workstream_id,
    }
    _write_json(
        ledger / "head.json",
        {
            **head_static,
            "entry_count": 1,
            "head_entry_id": entry["entry_id"],
            "head_hash": entry["entry_hash"],
        },
    )
    head = _commit(repository, "record candidate worker ledger")
    updated = copy.deepcopy(candidate)
    updated["head_commit"] = head
    updated["head_tree"] = _git(repository, "rev-parse", f"{head}^{{tree}}")
    prefix = f"design/contract_compiler/workstreams/{workstream_id}/ledger"
    validation = integration_module.WorkerLedgerValidation(
        workstream_id=workstream_id,
        phase_results=(entry["data"],),
        head_path=f"{prefix}/head.json",
        head_static=head_static,
        entry_sources={f"{prefix}/entries/{entry_path.name}": entry_path.read_bytes()},
        entry_hashes=(entry["entry_hash"],),
    )
    return updated, validation


def _clean_base_candidate(
    tmp_path: Path,
    *,
    prebase_path: str | None = None,
    merge_prebase: bool = False,
    delete_prebase: bool = False,
    authority_path: str | None = None,
    revert_output: bool = False,
    candidate_helper: bool = False,
    root_authority: bool = False,
) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    repository = tmp_path / "clean-base-candidate"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "CC-000 Test")
    _git(repository, "config", "user.email", "cc000@example.invalid")
    authority = {
        "entry_id": "OVR-TEST-ACTIVE",
        "entry_type": "WORKSTREAM_STATE",
        "data": {
            "bootstrap": False,
            "new_state": "ACTIVE",
            "workstream_id": "CC-TEST",
        },
    }
    authority_file = (
        repository / "governance" / "entries" / f"{authority['entry_id']}.json"
    )
    (repository / "README.md").write_text("fixture\n", encoding="utf-8")
    if revert_output:
        root_result = repository / "allowed" / "result.txt"
        root_result.parent.mkdir(parents=True)
        root_result.write_text("base\n", encoding="utf-8")
    if not root_authority:
        _commit(repository, "root")
    authority_file.parent.mkdir(parents=True)
    _write_json(authority_file, authority)
    if authority_path is not None:
        bundled = repository / authority_path
        bundled.parent.mkdir(parents=True, exist_ok=True)
        bundled.write_text("bundled\n", encoding="utf-8")
    _commit(repository, "root authority" if root_authority else "active authority")

    if merge_prebase:
        _git(repository, "switch", "-c", "stale-scope")
    if prebase_path is not None:
        prebase = repository / prebase_path
        prebase.parent.mkdir(parents=True, exist_ok=True)
        prebase.write_text("stale\n", encoding="utf-8")
        _commit(repository, "prebase scope change")
        if delete_prebase:
            prebase.unlink()
            _commit(repository, "remove prebase scope change")
    if merge_prebase:
        _git(repository, "switch", "main")
        (repository / "main.txt").write_text("main\n", encoding="utf-8")
        _commit(repository, "main prebase")
        _git(repository, "merge", "--no-ff", "stale-scope", "-m", "merge stale scope")

    result = repository / "allowed" / "result.txt"
    result.parent.mkdir(parents=True, exist_ok=True)
    (repository / "base-marker.txt").write_text("candidate base\n", encoding="utf-8")
    base = _commit(repository, "candidate base")

    result.write_text("changed\n" if revert_output else "result\n", encoding="utf-8")
    if revert_output:
        _commit(repository, "change declared output")
        result.write_text("base\n", encoding="utf-8")
    if candidate_helper:
        (repository / "allowed" / "helper.py").write_text(
            "HELPER = True\n",
            encoding="utf-8",
        )
    artifact = result.read_bytes()
    evidence_path = repository / "evidence" / "checks.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(
        evidence_path,
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
                    "check_id": "clean-base",
                    "method": "Exercise strict candidate history admission.",
                    "observed": "The declared output matched its report.",
                    "result": "PASS",
                }
            ],
            "limitations": [],
            "recorded_at": "2026-08-29T20:00:00Z",
            "schema": "malleus.contract-compiler.verification-report/v1",
            "workstream_id": "CC-TEST",
        },
    )
    head = _commit(repository, "candidate output")
    candidate = _candidate(repository, base, head)
    return repository, candidate, authority


def _quiet_bell_history_candidate(
    tmp_path: Path,
    *,
    base_commit: str,
    copy_authority_entry: bool = False,
    descendant_base: bool = False,
) -> tuple[Path, dict[str, Any]]:
    repository = tmp_path / "quiet-bell-candidate"
    subprocess.run(
        ["git", "clone", "--quiet", str(ROOT), str(repository)],
        check=True,
        capture_output=True,
    )
    _git(repository, "config", "user.name", "CC-000 Test")
    _git(repository, "config", "user.email", "cc000@example.invalid")
    _git(repository, "checkout", "--detach", base_commit)

    authority_relative = (
        f"design/contract_compiler/overseer/entries/"
        f"{QUIET_BELL_REACTIVATION_ENTRY}.json"
    )
    authority_path = repository / authority_relative
    if copy_authority_entry:
        authority_path.parent.mkdir(parents=True, exist_ok=True)
        authority_path.write_bytes((ROOT / authority_relative).read_bytes())
        base_commit = _commit(repository, "copy authority bytes without ancestry")
    if descendant_base:
        (repository / "candidate-base.txt").write_text(
            "authorized descendant\n",
            encoding="utf-8",
        )
        base_commit = _commit(repository, "authorized descendant base")

    artifact_relative = (
        "conformance/contract_kernel/v0/themed_fixture/oracle/candidate.json"
    )
    artifact_path = repository / artifact_relative
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text('{"outcome":"REFUSE"}\n', encoding="utf-8")
    artifact = artifact_path.read_bytes()
    evidence_relative = "conformance/contract_compiler/v0/evidence/CC-012.json"
    evidence_path = repository / evidence_relative
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(
        evidence_path,
        {
            "artifacts": [
                {
                    "byte_length": len(artifact),
                    "path": artifact_relative,
                    "sha256": _digest(artifact),
                }
            ],
            "base_commit": base_commit,
            "checks": [
                {
                    "check_id": "cc012-synthetic-candidate",
                    "method": "Exercise candidate authority admission.",
                    "observed": "The private artifact matched its report.",
                    "result": "PASS",
                }
            ],
            "limitations": [],
            "recorded_at": "2026-08-29T18:00:00Z",
            "schema": "malleus.contract-compiler.verification-report/v1",
            "workstream_id": "CC-012",
        },
    )
    head_commit = _commit(repository, "candidate content")
    evidence = evidence_path.read_bytes()
    candidate = {
        "artifacts": [
            {
                "byte_length": len(artifact),
                "path": artifact_relative,
                "sha256": _digest(artifact),
            }
        ],
        "base_commit": base_commit,
        "evidence": [
            {
                "byte_length": len(evidence),
                "path": evidence_relative,
                "result": "PASS",
                "sha256": _digest(evidence),
            }
        ],
        "head_commit": head_commit,
        "head_tree": _git(repository, "rev-parse", f"{head_commit}^{{tree}}"),
        "state": "ELIGIBLE",
    }
    _git(repository, "checkout", "--detach", "main")
    return repository, candidate


def _quiet_bell_candidate_authority() -> tuple[list[dict[str, str]], dict[str, Any]]:
    card = _read_json(CONTRACT / "workstreams/CC-012/manifest.json")
    entry = _read_json(
        CONTRACT / "overseer" / "entries" / f"{QUIET_BELL_REACTIVATION_ENTRY}.json"
    )
    return card["scopes"], entry


def _greenhouse_candidate_authority() -> tuple[list[dict[str, str]], dict[str, Any]]:
    card = _read_json(CONTRACT / "workstreams/CC-016/manifest.json")
    entry = _read_json(
        CONTRACT / "overseer" / "entries" / f"{GREENHOUSE_ACTIVATION_ENTRY}.json"
    )
    return card["scopes"], entry


def _current_candidate_cards() -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    manifest = _read_json(INTEGRATION)
    rows = [row for row in manifest["workstreams"] if row["card"]["state"] == "PRESENT"]
    return (
        {
            row["workstream_id"]: _read_json(CONTRACT / row["card"]["path"])
            for row in rows
        },
        {row["workstream_id"]: row["card"]["path"] for row in rows},
    )


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


def _overseer_prefix(sequence: int) -> SimpleNamespace:
    return SimpleNamespace(
        entries=tuple(
            entry
            for entry in _raw_overseer_state().entries
            if entry["sequence"] <= sequence
        )
    )


def test_program_registry_contains_the_exact_approved_72_workstreams() -> None:
    registry = load_program_registry(PROGRAM)

    assert len(registry) == 72
    assert registry["CC-000"] == ()
    assert registry["CC-001"] == ("CC-000",)
    assert registry["CC-D05"] == ("CC-D01", "CC-D02", "CC-D03")
    assert registry["CC-D06"] == ("CC-D05",)
    assert registry["CC-D08"] == ("CC-D02", "CC-D03", "CC-D05")
    assert registry["CC-D17"] == ("CC-D05", "CC-D06")
    assert registry["CC-D18"] == ("CC-D10", "CC-D17")
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
        "CC-R10",
    )
    assert registry["CC-R10"] == ("CC-R07", "CC-D17")
    assert registry["CC-R09"] == (
        "CC-R08",
        "CC-D07",
        "CC-D10",
        "CC-D18",
        "CC-021",
        "CC-022",
    )
    assert "CC-D18" in registry["CC-R06"]
    assert registry["CC-P10"] == ("CC-P01", "CC-W02", "CC-R09")
    assert registry["CC-P21"] == ("CC-P12", "CC-P19", "CC-P20", "CC-R10")
    assert registry["CC-P52"] == ("CC-P45", "CC-P51", "CC-PUB01")


def test_research_runway_exposes_the_machine_and_realization_handoffs() -> None:
    program = PROGRAM.read_text(encoding="utf-8")
    normalized = " ".join(program.split())

    for required in (
        "strict protocol-machine program",
        "generic interpreter",
        "lean-review conformance",
        "no profile-specific event, record, or field name",
        "no arbitrary-code escape hatch",
        "frontend-neutral KnowledgeChangeSet",
        "PopulationPlan and operation-dependency plan remain derivation inputs",
        "canonical generic validation receipt",
        "no stable public API claim",
    ):
        assert required in normalized


def test_canonical_integration_manifest_is_valid() -> None:
    state = validate_integration(ROOT)
    x03 = state.cards["CC-X03"]
    ledger = load_overseer_ledger(CONTRACT / "overseer", repository=ROOT)
    workstream_states, _ = integration_module._workstream_states(ledger)

    assert len(state.workstreams) == 72
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
    assert state.cards["CC-R01"]["authorization"]["class"] == "FORMAL"
    assert workstream_states["CC-R01"] == "COMPLETE"

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
        "CC-D17": ("CC-D05", "CC-D06"),
        "CC-D18": ("CC-D10", "CC-D17"),
    }
    assert len(state.cards) == 34
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
    d17_responsibility = state.cards["CC-D17"]["responsibility"]
    for phrase in (
        "closed typed canonical ProtocolMachineProgram",
        "event vocabulary",
        "typed refusals",
        "projection programs separately identified",
        "machine semantic identity separate from executor identity",
        "arbitrary-code escape hatches",
        "same poststate and receipt or unchanged state and typed refusal",
        "Lean Review only as the first bounded future conformance slice",
        "selects no DSL",
        "no implementation",
    ):
        assert phrase in d17_responsibility
    d18_responsibility = state.cards["CC-D18"]["responsibility"]
    for phrase in (
        "KnowledgeChangeSet",
        "one authoritative ordered ledger",
        "replay-derived accepted temporal graph",
        "empty graph",
        "genesis change set",
        "same immutable change-set identity",
        "ordered primitive operations",
        "operation-local dependencies",
        "no direct accepted-state mutation",
        "persisted structural candidates remain non-governed and non-accepted",
        "cross-contract change",
        "zero-scope decision",
        "no runtime or ontology implementation",
    ):
        assert phrase in d18_responsibility


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
        "authorization_class",
        "workstream_state",
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
            "FORMAL",
            "COMPLETE",
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
            "FORMAL",
            "COMPLETE",
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
            "FORMAL",
            "COMPLETE",
        ),
    ),
)
def test_oracle_workstream_activation_boundaries_are_exact(
    workstream_id: str,
    assignment: dict[str, str],
    paired_input_id: str,
    scopes: list[dict[str, str]],
    required_phrases: tuple[str, ...],
    authorization_class: str,
    workstream_state: str,
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
    assert card["authorization"]["class"] == authorization_class
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert len(
        {current["assignment"]["owner_id"] for current in cards.values()}
    ) == len(cards)
    assert card["scopes"] == scopes
    expected_lifecycle = {
        "CC-012": ("COMPLETE", "ELIGIBLE", "RECORDED"),
        "CC-014": (workstream_state, "ELIGIBLE", "RECORDED"),
        "CC-016": (workstream_state, "ELIGIBLE", "RECORDED"),
    }[workstream_id]
    assert (
        workstream_states[workstream_id],
        card["candidate"]["state"],
        card["ledger"]["state"],
    ) == expected_lifecycle
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


def test_small_shop_input_completion_boundary_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-021")
    assert manifest["revision"] == 4
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
    report_path = ROOT / "conformance/contract_compiler/v0/evidence/CC-021.json"
    report = _read_json(report_path)
    report_source = report_path.read_bytes()
    assert card["candidate"] == {
        "artifacts": report["artifacts"],
        "base_commit": SMALL_SHOP_AUTHORITY_COMMIT,
        "evidence": [
            {
                "byte_length": len(report_source),
                "path": "conformance/contract_compiler/v0/evidence/CC-021.json",
                "result": "PASS",
                "sha256": _digest(report_source),
            }
        ],
        "head_commit": SMALL_SHOP_CANDIDATE_COMMIT,
        "head_tree": SMALL_SHOP_CANDIDATE_TREE,
        "state": "ELIGIBLE",
    }
    assert card["ledger"]["state"] == "RECORDED"
    assert card["ledger"]["entry_count"] == 7
    assert card["ledger"]["head_entry_id"] == "CC-021-WRK-000007"
    assert card["ledger"]["path"] == "workstreams/CC-021/ledger"
    assert states["CC-021"] == "COMPLETE"
    assert "CC-021" not in manifest["selections"]
    assert card["responsibility"] == SMALL_SHOP_RESPONSIBILITY

    touched = validate_candidate_history(
        ROOT,
        card["candidate"],
        allowed_scopes=card["scopes"],
        workstream_id="CC-021",
    )
    assert set(touched) == SMALL_SHOP_CANDIDATE_PATHS

    assert _registry_row(manifest, "CC-022")["card"]["state"] == "PRESENT"
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}


def test_small_shop_original_activation_remains_historically_exact() -> None:
    card_path = "design/contract_compiler/workstreams/CC-021/manifest.json"
    old_card = json.loads(
        _git(ROOT, "show", f"{SMALL_SHOP_ACTIVATION_COMMIT}:{card_path}")
    )
    activation = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ACTIVATION_COMMIT}:design/contract_compiler/overseer/"
            "entries/OVR-000214.json",
        )
    )

    assert old_card["responsibility"] == (
        "Author controlled Small Shop Fulfilment input bytes only under the exact "
        "research input prefix, with one canonical verification report and one fixed "
        "input validation test. Inputs may include ontology and domain source bytes, "
        "but no expected facts, mappings, transformations, identities, recipes, "
        "ProposedOperation values, candidates, evidence outcomes, compiler or runtime "
        "implementation, protocol or accepted knowledge-graph state, replay receipts, "
        "or research-journal findings. Create no CC-022 oracle or CC-R work, corpus or "
        "checksum publication, public API, package, Docker, or release change."
    )
    assert activation["data"]["previous_state"] == "PLANNED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is True
    assert (
        _git(
            ROOT,
            "ls-tree",
            "-r",
            "--name-only",
            SMALL_SHOP_ACTIVATION_COMMIT,
            "--",
            "research/ontology_driven_kg_realization/fixtures/"
            "small_shop_fulfilment/input",
            "conformance/contract_compiler/v0/evidence/CC-021.json",
            "tests/contract_compiler/test_small_shop_fixture_inputs.py",
        )
        == ""
    )


@pytest.mark.parametrize(
    ("workstream_id", "old_blocker"),
    (
        (
            "CC-014",
            "Content production waits for the operator to decide whether the CC-013 explicit-false boundary splits into separate positive and refusal cases and to approve minimal private refusal and relations JSON shapes.",
        ),
    ),
)
def test_feature_oracle_prior_pause_remains_historical(
    workstream_id: str,
    old_blocker: str,
) -> None:
    manifest = _read_json(INTEGRATION)
    card_path = CONTRACT / _registry_row(manifest, workstream_id)["card"]["path"]
    card = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ACTIVATION_COMMIT}:{card_path.relative_to(ROOT)}",
        )
    )
    prior = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_REANCHOR_BASE}:{card_path.relative_to(ROOT)}",
        )
    )
    states, _ = integration_module._workstream_states(_overseer_prefix(212))
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


def test_greenhouse_prior_pause_remains_historical() -> None:
    card_path = "design/contract_compiler/workstreams/CC-016/manifest.json"
    card = json.loads(_git(ROOT, "show", f"{GREENHOUSE_REACTIVATION_BASE}:{card_path}"))
    states, _ = integration_module._workstream_states(_overseer_prefix(260))

    assert card["authorization"] == {
        "authorized_by": {"id": "operator", "type": "OPERATOR"},
        "blockers": [
            "Content production waits for operator approval of minimal private refusal and relations JSON shapes.",
            "Resume only after CC-021 controlled Small Shop inputs and CC-022 independent Small Shop oracle are complete and fresh dependency bindings are issued.",
        ],
        "class": "BLOCKED",
    }
    assert card["candidate"] == {"state": "NONE"}
    assert card["ledger"] == {"state": "NOT_STARTED"}
    assert states["CC-016"] == "PAUSED"


def test_quiet_bell_prior_activation_and_pause_remain_historical() -> None:
    card_path = "design/contract_compiler/workstreams/CC-012/manifest.json"
    activation_card = json.loads(
        _git(ROOT, "show", f"{QUIET_BELL_ORACLE_ACTIVATION_COMMIT}:{card_path}")
    )
    paused_card = json.loads(
        _git(ROOT, "show", f"{QUIET_BELL_REACTIVATION_BASE}:{card_path}")
    )
    activation = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/"
            "overseer/entries/OVR-000205.json",
        )
    )
    pause = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_REACTIVATION_BASE}:design/contract_compiler/overseer/"
            "entries/OVR-000211.json",
        )
    )

    assert activation_card["authorization"]["class"] == "FORMAL"
    assert activation["data"] == {
        "blockers": [
            "Content production waits for operator approval of fixture-local private "
            "resolver, profile, configuration, media-type, and source-blob tokens; "
            "CC-R07 retains runtime artifact bytes and wire grammar."
        ],
        "bootstrap": True,
        "deliverables": [
            "Author only independently derived themed source descriptors, import graph, "
            "declarations, bindings, elaboration, facts, and logical artifact expectations "
            "under the exact CC-010 themed oracle prefix, with no runtime artifact bytes "
            "or wire grammar.",
            "Use accepted decisions and completed CC-011 sources, and write expected "
            "values by hand rather than exporting them from LinkML, OntologyRegistry, "
            "or the implementation under test.",
            "Keep source and trace inputs, compiler and runtime implementation, public "
            "API, package, Docker, release, corpus publication, selection, integration, "
            "and every CC-R stage outside CC-012.",
        ],
        "evidence_entry_ids": ["OVR-000203", "OVR-000204"],
        "new_state": "ACTIVE",
        "previous_state": "PLANNED",
        "workstream_id": "CC-012",
    }
    assert paused_card["authorization"]["class"] == "BLOCKED"
    assert pause["data"]["previous_state"] == "ACTIVE"
    assert pause["data"]["new_state"] == "PAUSED"
    assert pause["data"]["bootstrap"] is False
    assert (
        _git(
            ROOT,
            "ls-tree",
            "-r",
            "--name-only",
            QUIET_BELL_ORACLE_ACTIVATION_COMMIT,
            "--",
            "conformance/contract_kernel/v0/themed_fixture/oracle",
            "conformance/contract_compiler/v0/evidence/CC-012.json",
            "tests/contract_compiler/test_themed_compilation_oracles.py",
        )
        == ""
    )


def _assert_quiet_bell_private_boundary(responsibility: str) -> None:
    for token in QUIET_BELL_PRIVATE_TOKENS:
        assert token in responsibility
    assert "public format" not in responsibility
    assert "PUBLIC_MALLEUS_RESOLVER" not in responsibility, (
        "public-looking resolver material is forbidden"
    )
    assert "Small Shop domain values" in responsibility
    assert "use no Small Shop domain values" in responsibility


def test_quiet_bell_reactivation_boundary_is_exact() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CANDIDATE_BASE}:design/contract_compiler/integration.json",
        )
    )
    row = _registry_row(manifest, "CC-012")
    card_path = f"design/contract_compiler/{row['card']['path']}"
    card_source = subprocess.run(
        ["git", "show", f"{QUIET_BELL_CANDIDATE_BASE}:{card_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    card = json.loads(card_source)
    states, _ = integration_module._workstream_states(_overseer_prefix(254))

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-012/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert card["assignment"] == {
        "owner_id": "worker:cc012-themed-oracles",
        "state": "ASSIGNED",
        "task_id": "/root/cc012_themed_oracles",
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
        == QUIET_BELL_DEPENDENCIES
    )
    assert card["candidate"] == {"state": "NONE"}
    assert card["ledger"] == {"state": "NOT_STARTED"}
    assert card["responsibility"] == QUIET_BELL_ORACLE_RESPONSIBILITY
    _assert_quiet_bell_private_boundary(card["responsibility"])
    assert states["CC-012"] == "ACTIVE"
    assert states["CC-014"] == states["CC-016"] == "PAUSED"
    assert (
        sum(
            states[workstream_id] == "ACTIVE"
            for workstream_id in ("CC-012", "CC-014", "CC-016")
        )
        == 1
    )
    assert "CC-012" not in manifest["selections"]


def test_quiet_bell_reactivation_controls_hold_before_content() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CANDIDATE_BASE}:design/contract_compiler/integration.json",
        )
    )
    base_manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_REACTIVATION_BASE}:design/contract_compiler/integration.json",
        )
    )
    for workstream_id, expected_digest in (
        (
            "CC-014",
            "sha256:7fe06186f329ba16dfca09f02f8056f4b96c7f968af1c79262f1e7701fd31b3e",
        ),
        (
            "CC-016",
            "sha256:26123e398e10fe84a544f4fbd6c8526f018e80f0989fb3243a69fd7f3fa9930f",
        ),
    ):
        assert _registry_row(manifest, workstream_id) == _registry_row(
            base_manifest, workstream_id
        )
        assert (
            _registry_row(manifest, workstream_id)["card"]["sha256"] == expected_digest
        )
    assert _registry_row(manifest, "CC-012")["depends_on"] == list(
        QUIET_BELL_DEPENDENCIES
    )
    assert (
        _registry_row(manifest, "CC-014")["depends_on"]
        == _registry_row(base_manifest, "CC-014")["depends_on"]
    )
    assert (
        _registry_row(manifest, "CC-016")["depends_on"]
        == _registry_row(base_manifest, "CC-016")["depends_on"]
    )
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}
    assert manifest["revision"] == base_manifest["revision"] == 2
    assert manifest["selections"] == base_manifest["selections"]
    assert manifest["owner_separations"] == base_manifest["owner_separations"]
    assert (
        _git(
            ROOT,
            "ls-tree",
            "-r",
            "--name-only",
            QUIET_BELL_CANDIDATE_BASE,
            "--",
            *sorted(QUIET_BELL_CANDIDATE_PATHS),
        )
        == ""
    )


def test_quiet_bell_reactivation_report_is_exact() -> None:
    report_path = CONTRACT / "overseer/evidence/CC-012-reactivation.json"
    report = _read_json(report_path)

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_REACTIVATION_BASE
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-reactivation-red",
        "cc012-dependency-readiness",
        "cc012-private-token-boundary",
        "cc012-independent-authorship",
        "cc012-small-shop-separation",
        "cc012-adjacent-state",
        "cc012-kiss-reactivation",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert all(
        any(term in limitation for limitation in report["limitations"])
        for term in (
            "oracle content",
            "candidate",
            "compiler",
            "runtime artifact",
            "later suites",
        )
    )


def test_quiet_bell_reactivation_transaction_is_exact() -> None:
    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 229 <= entry["sequence"] <= 231
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000229",
        "OVR-000230",
        "OVR-000231",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "cc012-reactivation-boundary",
        "cc012-reactivation-verification",
        "CC-012",
    )
    revision, verification, activation = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {document["path"] for document in revision["data"]["documents"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-012-reactivation.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    assert verification["actor"] == {
        "id": "cc012-reactivation-verifier",
        "type": "MECHANICAL",
    }
    assert activation["data"]["workstream_id"] == "CC-012"
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000230",
    ]
    report_time = datetime.fromisoformat(
        _read_json(CONTRACT / "overseer/evidence/CC-012-reactivation.json")[
            "recorded_at"
        ].replace("Z", "+00:00")
    )
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_REACTIVATION_COMMIT}:design/contract_compiler/overseer/"
            "head.json",
        )
    )
    assert head["entry_count"] == 231
    assert head["head_entry_id"] == "OVR-000231"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_private_tokens_reject_public_lookalikes() -> None:
    responsibility = QUIET_BELL_ORACLE_RESPONSIBILITY + " PUBLIC_MALLEUS_RESOLVER_V0"
    assert all(token in responsibility for token in QUIET_BELL_PRIVATE_TOKENS)

    with pytest.raises(AssertionError, match="public-looking resolver"):
        _assert_quiet_bell_private_boundary(responsibility)


@pytest.mark.parametrize("mutation", ("missing", "stale"))
def test_quiet_bell_dependency_bindings_fail_closed(
    tmp_path: Path, mutation: str
) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)

    def mutate(card: dict[str, Any]) -> None:
        if mutation == "missing":
            card["authorization"]["dependency_bindings"].pop()
        else:
            card["authorization"]["dependency_bindings"][0]["card_sha256"] = (
                "sha256:" + "0" * 64
            )

    _rewrite_card(path, manifest, "CC-012", mutate)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_DEPENDENCY_BINDING")


def test_quiet_bell_reactivation_correction_report_is_exact() -> None:
    report_path = CONTRACT / "overseer/evidence/CC-012-reactivation-correction.json"
    report = _read_json(report_path)

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_REACTIVATION_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "design/contract_compiler/workstreams/CC-014/manifest.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_REACTIVATION_REPAIR_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-correction-red",
        "cc012-append-only-supersession",
        "cc012-process-readiness-truth",
        "cc012-execution-order",
        "cc012-public-token-guard",
        "cc012-frozen-boundaries",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    truth = next(
        check
        for check in report["checks"]
        if check["check_id"] == "cc012-process-readiness-truth"
    )["observed"]
    for exact in (
        "pre-existing formal process-readiness bindings",
        "no new DAG edge",
        "no Small Shop expected value, fact, identifier, derivation, shared helper, or interface",
    ):
        assert exact in truth


def test_quiet_bell_reactivation_correction_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 232 <= entry["sequence"] <= 236)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(232, 237)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "CORRECTION",
        "CORRECTION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "cc012-reactivation-verification",
        "CC-012",
        "cc012-reactivation-correction-boundary",
        "cc012-reactivation-verification",
        "CC-012",
    )
    verification_correction, state_correction, revision, verification, activation = (
        transaction
    )
    for correction, target in (
        (verification_correction, "OVR-000230"),
        (state_correction, "OVR-000231"),
    ):
        assert correction["data"]["replacement_required"] is True
        assert correction["data"]["supersedes_entry_id"] == target
        assert ("SUPERSEDES", "ENTRY", target) in {
            (reference["relation"], reference["type"], reference["target"])
            for reference in correction["references"]
        }
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/overseer/evidence/CC-012-reactivation-correction.json": "CREATED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    assert verification["actor"] == {
        "id": "cc012-reactivation-correction-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000234",
        "OVR-000235",
    ]
    assert activation["data"]["deliverables"][-1].endswith(
        "the first commit containing OVR-000236."
    )
    superseded = integration_module.superseded_entries(entries)
    assert {"OVR-000230", "OVR-000231"} <= superseded
    states, state_entries = integration_module._workstream_states(_overseer_prefix(236))
    assert states["CC-012"] == "ACTIVE"
    assert state_entries["CC-012"]["entry_id"] == "OVR-000236"

    report_time = datetime.fromisoformat(
        _read_json(CONTRACT / "overseer/evidence/CC-012-reactivation-correction.json")[
            "recorded_at"
        ].replace("Z", "+00:00")
    )
    times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert times[0] < times[1] < report_time < times[2] < times[3] < times[4]
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_REACTIVATION_REPAIR_COMMIT}:design/contract_compiler/"
            "overseer/head.json",
        )
    )
    assert head["entry_count"] == 236
    assert head["head_entry_id"] == "OVR-000236"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_candidate_authority_hardening_report_is_exact() -> None:
    report_path = (
        CONTRACT / "overseer/evidence/CC-012-candidate-authority-hardening.json"
    )
    report = _read_json(report_path)

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_REACTIVATION_REPAIR_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "scripts/contract_compiler_integration.py",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_AUTHORITY_HARDENING_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-authority-red",
        "cc012-trusted-history",
        "cc012-descendant-base",
        "cc012-all-candidate-admission",
        "cc012-bootstrap-compatibility",
        "cc012-frozen-content-boundary",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert all(
        any(term in limitation for limitation in report["limitations"])
        for term in (
            "oracle content",
            "candidate",
            "compiler semantics",
            "public contract",
        )
    )


def test_quiet_bell_candidate_authority_hardening_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 237 <= entry["sequence"] <= 240)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(237, 241)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "CORRECTION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    correction, revision, verification, activation = transaction
    assert correction["data"]["replacement_required"] is True
    assert correction["data"]["supersedes_entry_id"] == "OVR-000236"
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/overseer/evidence/CC-012-candidate-authority-hardening.json": "CREATED",
        "scripts/contract_compiler_integration.py": "MODIFIED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    assert verification["actor"] == {
        "id": "cc012-candidate-authority-verifier",
        "type": "MECHANICAL",
    }
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000234",
        "OVR-000235",
        "OVR-000238",
        "OVR-000239",
    ]
    assert activation["data"]["deliverables"][-1].endswith(
        "equal or descend from the first trusted commit containing OVR-000240."
    )
    superseded = integration_module.superseded_entries(entries)
    assert {"OVR-000230", "OVR-000231", "OVR-000236"} <= superseded
    states, state_entries = integration_module._workstream_states(_overseer_prefix(240))
    assert states["CC-012"] == "ACTIVE"
    assert state_entries["CC-012"]["entry_id"] == "OVR-000240"

    report_time = datetime.fromisoformat(
        _read_json(
            CONTRACT / "overseer/evidence/CC-012-candidate-authority-hardening.json"
        )["recorded_at"].replace("Z", "+00:00")
    )
    times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert times[0] < report_time < times[1] < times[2] < times[3]
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_AUTHORITY_HARDENING_COMMIT}:design/contract_compiler/"
            "overseer/head.json",
        )
    )
    assert head["entry_count"] == 240
    assert head["head_entry_id"] == "OVR-000240"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_candidate_clean_base_hardening_report_is_exact() -> None:
    report = _read_json(
        CONTRACT / "overseer/evidence/CC-012-candidate-clean-base-hardening.json"
    )

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_AUTHORITY_HARDENING_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "scripts/contract_compiler_integration.py",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_CLEAN_BASE_HARDENING_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-clean-base-red",
        "cc012-authority-scope-clean",
        "cc012-all-parent-prehistory",
        "cc012-exact-declared-delta",
        "cc012-frozen-legacy",
        "cc012-frozen-content-boundary",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("trusted repository HEAD" in item for item in report["limitations"])
    assert any("external attestation" in item for item in report["limitations"])
    assert any("information-flow proof" in item for item in report["limitations"])


def test_quiet_bell_candidate_clean_base_hardening_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 241 <= entry["sequence"] <= 244)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(241, 245)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "CORRECTION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    correction, revision, verification, activation = transaction
    assert correction["data"] == {
        "affected_subject_ids": ["CC-012"],
        "replacement_required": True,
        "supersedes_entry_id": "OVR-000240",
    }
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/overseer/evidence/CC-012-candidate-clean-base-hardening.json": "CREATED",
        "scripts/contract_compiler_integration.py": "MODIFIED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    assert verification["actor"] == {
        "id": "cc012-candidate-clean-base-verifier",
        "type": "MECHANICAL",
    }
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000234",
        "OVR-000235",
        "OVR-000242",
        "OVR-000243",
    ]
    assert "scope-untouched prehistory" in activation["data"]["deliverables"][-1]
    superseded = integration_module.superseded_entries(entries)
    assert "OVR-000240" in superseded
    states, state_entries = integration_module._workstream_states(_overseer_prefix(244))
    assert states["CC-012"] == "ACTIVE"
    assert state_entries["CC-012"]["entry_id"] == "OVR-000244"

    report_time = datetime.fromisoformat(
        _read_json(
            CONTRACT / "overseer/evidence/CC-012-candidate-clean-base-hardening.json"
        )["recorded_at"].replace("Z", "+00:00")
    )
    times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert times[0] < report_time < times[1] < times[2] < times[3]
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CLEAN_BASE_HARDENING_COMMIT}:design/contract_compiler/"
            "overseer/head.json",
        )
    )
    assert head["entry_count"] == 244
    assert head["head_entry_id"] == "OVR-000244"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_candidate_clean_base_closure_report_is_exact() -> None:
    report = _read_json(
        CONTRACT / "overseer/evidence/CC-012-candidate-clean-base-closure.json"
    )

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_CLEAN_BASE_HARDENING_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "scripts/contract_compiler_integration.py",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_CLEAN_BASE_CLOSURE_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-closure-red",
        "cc012-root-authority",
        "cc012-policy-path",
        "cc012-frozen-continuity",
        "cc012-reactivation-redo",
        "cc012-frozen-content-boundary",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("trusted repository HEAD" in item for item in report["limitations"])
    assert any("information-flow proof" in item for item in report["limitations"])


def test_quiet_bell_candidate_clean_base_closure_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 245 <= entry["sequence"] <= 249)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(245, 250)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "CORRECTION",
        "CORRECTION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    fact_correction, state_correction, revision, verification, activation = transaction
    assert fact_correction["data"]["supersedes_entry_id"] == "OVR-000243"
    assert state_correction["data"]["supersedes_entry_id"] == "OVR-000244"
    assert fact_correction["data"]["replacement_required"] is True
    assert state_correction["data"]["replacement_required"] is True
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/overseer/evidence/CC-012-candidate-clean-base-closure.json": "CREATED",
        "scripts/contract_compiler_integration.py": "MODIFIED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    assert verification["actor"] == {
        "id": "cc012-candidate-clean-base-closure-verifier",
        "type": "MECHANICAL",
    }
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000234",
        "OVR-000235",
        "OVR-000247",
        "OVR-000248",
    ]
    assert activation["data"]["deliverables"][-1].endswith(
        "first trusted commit containing OVR-000249."
    )
    superseded = integration_module.superseded_entries(entries)
    assert {"OVR-000243", "OVR-000244"} <= superseded
    states, state_entries = integration_module._workstream_states(_overseer_prefix(249))
    assert states["CC-012"] == "ACTIVE"
    assert state_entries["CC-012"]["entry_id"] == "OVR-000249"

    report_time = datetime.fromisoformat(
        _read_json(
            CONTRACT / "overseer/evidence/CC-012-candidate-clean-base-closure.json"
        )["recorded_at"].replace("Z", "+00:00")
    )
    times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert times[0] < times[1] < report_time < times[2] < times[3] < times[4]
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CLEAN_BASE_CLOSURE_COMMIT}:design/contract_compiler/"
            "overseer/head.json",
        )
    )
    assert head["entry_count"] == 249
    assert head["head_entry_id"] == "OVR-000249"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_git_object_identity_report_is_exact() -> None:
    report = _read_json(
        CONTRACT / "overseer/evidence/CC-012-git-object-identity-hardening.json"
    )

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_CLEAN_BASE_CLOSURE_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "scripts/contract_compiler_integration.py",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_CANDIDATE_BASE}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert {check["check_id"] for check in report["checks"]} == {
        "cc012-git-identity-red",
        "cc012-replacement-ref-refusal",
        "cc012-graft-overlay-refusal",
        "cc012-normal-history",
        "cc012-admission-controls",
        "cc012-content-boundary",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("trusted Git object store" in item for item in report["limitations"])
    assert any("external attestation" in item for item in report["limitations"])


def test_quiet_bell_git_object_identity_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 250 <= entry["sequence"] <= 254)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(250, 255)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "CORRECTION",
        "CORRECTION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    fact_correction, state_correction, revision, verification, activation = transaction
    assert fact_correction["data"]["supersedes_entry_id"] == "OVR-000248"
    assert state_correction["data"]["supersedes_entry_id"] == "OVR-000249"
    assert fact_correction["data"]["replacement_required"] is True
    assert state_correction["data"]["replacement_required"] is True
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert verification["actor"] == {
        "id": "cc012-git-object-identity-verifier",
        "type": "MECHANICAL",
    }
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000229",
        "OVR-000234",
        "OVR-000235",
        "OVR-000252",
        "OVR-000253",
    ]
    assert activation["data"]["deliverables"][-1].endswith(
        "first trusted commit containing OVR-000254."
    )
    superseded = integration_module.superseded_entries(entries)
    assert {"OVR-000248", "OVR-000249"} <= superseded
    states, state_entries = integration_module._workstream_states(_overseer_prefix(254))
    assert states["CC-012"] == "ACTIVE"
    assert state_entries["CC-012"]["entry_id"] == "OVR-000254"

    report_time = datetime.fromisoformat(
        _read_json(
            CONTRACT / "overseer/evidence/CC-012-git-object-identity-hardening.json"
        )["recorded_at"].replace("Z", "+00:00")
    )
    times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert times[0] < times[1] < report_time < times[2] < times[3] < times[4]
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CANDIDATE_BASE}:design/contract_compiler/overseer/head.json",
        )
    )
    assert head["entry_count"] == 254
    assert head["head_entry_id"] == "OVR-000254"
    assert head["head_hash"] == activation["entry_hash"]


def test_quiet_bell_greenhouse_edge_execution_order_has_no_control_bindings() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_CANDIDATE_BASE}:design/contract_compiler/integration.json",
        )
    )
    order = ("CC-012", "CC-016", "CC-014")
    control_ids = set(order)
    cards = {
        workstream_id: json.loads(
            _git(
                ROOT,
                "show",
                f"{QUIET_BELL_CANDIDATE_BASE}:design/contract_compiler/"
                f"{_registry_row(manifest, workstream_id)['card']['path']}",
            )
        )
        for workstream_id in order
    }
    for workstream_id, card in cards.items():
        assert control_ids.isdisjoint(
            _registry_row(manifest, workstream_id)["depends_on"]
        )
        assert control_ids.isdisjoint(
            binding["workstream_id"]
            for binding in card["authorization"].get("dependency_bindings", [])
        )

    frozen_paths = (
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-012-reactivation.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "design/contract_compiler/workstreams/CC-014/manifest.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
    )
    for path in frozen_paths:
        assert subprocess.run(
            ["git", "show", f"{QUIET_BELL_CANDIDATE_BASE}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout == subprocess.run(
            ["git", "show", f"{QUIET_BELL_REACTIVATION_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout

    entries = _overseer_prefix(254).entries
    superseded = integration_module.superseded_entries(entries)
    active_state_entries = tuple(
        entry
        for entry in entries
        if entry["entry_id"] not in superseded
        and entry["entry_type"] == "WORKSTREAM_STATE"
        and entry["sequence"] >= 232
        and entry["data"]["workstream_id"] in control_ids
    )
    assert [entry["data"]["workstream_id"] for entry in active_state_entries] == [
        "CC-012"
    ]
    for predecessor, successor in zip(order, order[1:]):
        successor_activations = [
            entry
            for entry in active_state_entries
            if entry["data"]["workstream_id"] == successor
            and entry["data"]["new_state"] == "ACTIVE"
        ]
        for successor_activation in successor_activations:
            assert any(
                entry["entry_id"] not in superseded
                and entry["entry_type"] == "WORKSTREAM_STATE"
                and entry["data"]["workstream_id"] == predecessor
                and entry["data"]["new_state"] == "COMPLETE"
                and entry["sequence"] < successor_activation["sequence"]
                for entry in entries
            )

    states, _ = integration_module._workstream_states(_overseer_prefix(254))
    assert tuple(states[workstream_id] for workstream_id in order) == (
        "ACTIVE",
        "PAUSED",
        "PAUSED",
    )
    assert tuple(
        cards[workstream_id]["candidate"]["state"] for workstream_id in order
    ) == (
        "NONE",
        "NONE",
        "NONE",
    )
    assert tuple(
        cards[workstream_id]["ledger"]["state"] for workstream_id in order
    ) == (
        "NOT_STARTED",
        "NOT_STARTED",
        "NOT_STARTED",
    )


def test_quiet_bell_completion_candidate_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-012")
    card_path = CONTRACT / row["card"]["path"]
    card_source = card_path.read_bytes()
    card = _read_json(card_path)
    report_path = ROOT / "conformance/contract_compiler/v0/evidence/CC-012.json"
    report_source = report_path.read_bytes()
    report = _read_json(report_path)
    expected_artifacts = [
        {
            "byte_length": 18567,
            "path": "conformance/contract_kernel/v0/themed_fixture/oracle/quiet_bell.json",
            "sha256": "sha256:cd7dbb8c4c8c81fb1d9d67e1423ba51e3bfa73b91d47a86f2381d1672f85e3e0",
        },
        {
            "byte_length": 26431,
            "path": "tests/contract_compiler/test_themed_compilation_oracles.py",
            "sha256": "sha256:d89242537da772c87f079bb393c11b75697897c554768917ef0700e6b9904e98",
        },
    ]

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-012/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert report["artifacts"] == expected_artifacts
    assert card["candidate"] == {
        "artifacts": expected_artifacts,
        "base_commit": QUIET_BELL_CANDIDATE_BASE,
        "evidence": [
            {
                "byte_length": 7871,
                "path": "conformance/contract_compiler/v0/evidence/CC-012.json",
                "result": "PASS",
                "sha256": "sha256:c200af169a1101540ef79fee313bec0f9bbf1ddf52bdd719f807d10392dba658",
            }
        ],
        "head_commit": QUIET_BELL_CANDIDATE_COMMIT,
        "head_tree": QUIET_BELL_CANDIDATE_TREE,
        "state": "ELIGIBLE",
    }
    assert len(report_source) == 7871
    assert _digest(report_source) == (
        "sha256:c200af169a1101540ef79fee313bec0f9bbf1ddf52bdd719f807d10392dba658"
    )
    assert card["responsibility"] == QUIET_BELL_ORACLE_RESPONSIBILITY
    assert len(card["authorization"]["dependency_bindings"]) == 9
    scopes, authority = _quiet_bell_candidate_authority()
    touched = validate_candidate_history(
        ROOT,
        card["candidate"],
        allowed_scopes=scopes,
        workstream_id="CC-012",
        authority_entry=authority,
        overseer_path="design/contract_compiler/overseer",
        enforce_clean_base=True,
    )
    assert touched == tuple(sorted(QUIET_BELL_CANDIDATE_PATHS))


def test_quiet_bell_completion_worker_chain_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    card = _read_json(CONTRACT / _registry_row(manifest, "CC-012")["card"]["path"])
    ledger_root = CONTRACT / "workstreams/CC-012/ledger"
    entries = [
        _read_json(path) for path in sorted((ledger_root / "entries").glob("*.json"))
    ]
    head = _read_json(ledger_root / "head.json")

    assert len(entries) == 7
    assert [entry["data"]["phase"] for entry in entries] == list(
        integration_module.TDD_PHASES
    )
    assert [entry["data"]["result"] for entry in entries] == [
        "EXPECTED_FAILURE",
        "PASS",
        "PASS",
        "PASS",
        "PASS",
        "NOT_APPLICABLE",
        "PASS",
    ]
    assert {entry["actor_id"] for entry in entries} == {
        "worker:cc012-themed-oracles"
    }
    candidate_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", QUIET_BELL_CANDIDATE_COMMIT)
    )
    entry_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in entries
    )
    assert entry_times[0] > candidate_time
    assert all(later > earlier for earlier, later in zip(entry_times, entry_times[1:]))
    assert "exactly 6 failures and 3 passes" in entries[0]["data"]["observed"]
    assert "All 15 fixed Quiet Bell oracle tests passed" in entries[1]["data"][
        "observed"
    ]
    assert "four-commit" in entries[2]["data"]["observed"]
    assert "three paths" in entries[2]["data"]["observed"]
    assert "9 passed and 6 deselected" in entries[3]["data"]["observed"]
    assert "refused-binding extra-member" in entries[3]["data"]["observed"]
    assert "101 contract-compiler" in entries[4]["data"]["observed"]
    assert "58 neighboring" in entries[4]["data"]["observed"]
    assert entries[5]["data"]["phase"] == "PACKAGE"
    assert "private repository-local test evidence" in entries[5]["data"]["observed"]
    assert QUIET_BELL_CANDIDATE_COMMIT in entries[6]["data"]["command"]
    assert "no P0-P3" in entries[6]["data"]["observed"]
    previous = "GENESIS"
    for entry in entries:
        assert entry["previous_entry_hash"] == previous
        assert entry["entry_hash"] == integration_module.worker_entry_hash(entry)
        previous = entry["entry_hash"]
    assert head == {
        "canonicalization": "malleus-canonical-json-v1",
        "entry_count": 7,
        "head_entry_id": "CC-012-WRK-000007",
        "head_hash": entries[-1]["entry_hash"],
        "schema": "malleus.contract-compiler.worker-ledger-head/v1",
        "workstream_id": "CC-012",
    }
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": "CC-012-WRK-000007",
        "head_hash": head["head_hash"],
        "path": "workstreams/CC-012/ledger",
        "state": "RECORDED",
    }


def test_quiet_bell_completion_semantics_are_exact() -> None:
    oracle = _read_json(
        ROOT / "conformance/contract_kernel/v0/themed_fixture/oracle/quiet_bell.json"
    )
    assert len(oracle["sources"]) == 6
    refused_imports = [
        edge for edge in oracle["import_edges"] if edge["resolution"] != "ACCEPT"
    ]
    assert refused_imports == [
        {
            "literal": "malleus",
            "ordinal": 1,
            "parent": "modules/foundation.yaml",
            "resolution": {"outcome": "REFUSE"},
        }
    ]
    assert sum(
        binding["target"] == {"outcome": "REFUSE"}
        for binding in oracle["qualified_bindings"]
    ) == 11
    assert [version["version"] for version in oracle["versions"]] == [
        "1.0.0",
        "1.0.1",
        "1.1.0",
    ]
    for version in oracle["versions"]:
        assert set(version["compiled"]) == {
            "compilation",
            "elaboration",
            "effective_contract",
            "fact_set",
            "facts",
            "logical_artifact",
            "qualified_bindings",
        }
        assert all(
            outcome == {"outcome": "REFUSE"}
            for outcome in version["compiled"].values()
        )
    assert [
        comparison["authored_local_semantic_projection"]
        for comparison in oracle["comparisons"]
    ] == ["SAME", "DIFFERENT", "DIFFERENT"]
    for comparison in oracle["comparisons"]:
        assert comparison["raw_source"] == "DIFFERENT"
        assert comparison["source_attestation"] == "DIFFERENT"
        assert {
            comparison["compiled_facts"],
            comparison["validated_fact_set"],
            comparison["effective_contract"],
            comparison["logical_artifact"],
        } == {"NOT_CLAIMED"}


def test_quiet_bell_completion_report_is_bounded() -> None:
    report = _read_json(CONTRACT / "overseer/evidence/CC-012-completion.json")
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-012"
    assert report["base_commit"] == QUIET_BELL_CANDIDATE_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_compiler/v0/evidence/CC-012.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-012/ledger/head.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_COMPLETION_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    checks = {check["check_id"]: check for check in report["checks"]}
    assert set(checks) == {
        "cc012-candidate-history",
        "cc012-card-report-equality",
        "cc012-semantic-boundary",
        "cc012-worker-tdd",
        "cc012-dependencies",
        "cc012-independent-audit",
        "cc012-regression",
        "cc012-unselected-completion",
        "cc012-process-lessons",
    }
    assert all(check["result"] == "PASS" for check in checks.values())
    assert "9 passed and 6 deselected" in checks["cc012-worker-tdd"]["observed"]
    assert "no P0-P3" in checks["cc012-independent-audit"]["observed"]
    assert "process technique only" in checks["cc012-process-lessons"]["observed"]
    assert any("private" in limitation for limitation in report["limitations"])
    assert any("bare malleus import" in limitation for limitation in report["limitations"])
    assert any("CC-R" in limitation for limitation in report["limitations"])


def test_quiet_bell_completion_transaction_is_exact() -> None:
    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 255 <= entry["sequence"] <= 257
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000255",
        "OVR-000256",
        "OVR-000257",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, completion = transaction
    expected_documents = {
        "conformance/contract_compiler/v0/evidence/CC-012.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-012-completion.json",
        "design/contract_compiler/workstreams/CC-012/ledger/head.json",
        "design/contract_compiler/workstreams/CC-012/manifest.json",
        "tests/test_contract_compiler_integration.py",
        *{
            "design/contract_compiler/workstreams/CC-012/ledger/entries/"
            f"CC-012-WRK-{sequence:06d}.json"
            for sequence in range(1, 8)
        },
    }
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-012"]
    assert {document["path"] for document in revision["data"]["documents"]} == (
        expected_documents
    )
    assert verification["actor"] == {
        "id": "cc012-completion-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert len(verification["data"]["claims"]) >= 8
    assert completion["data"]["previous_state"] == "ACTIVE"
    assert completion["data"]["new_state"] == "COMPLETE"
    assert completion["data"]["blockers"] == []
    assert completion["data"]["evidence_entry_ids"] == ["OVR-000256"]
    assert verification["previous_entry_hash"] == revision["entry_hash"]
    assert completion["previous_entry_hash"] == verification["entry_hash"]


def test_quiet_bell_completion_preserves_adjacent_authority() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_COMPLETION_COMMIT}:design/contract_compiler/integration.json",
        )
    )
    states, _ = integration_module._workstream_states(_overseer_prefix(257))
    cards = {
        workstream_id: json.loads(
            _git(
                ROOT,
                "show",
                f"{QUIET_BELL_COMPLETION_COMMIT}:design/contract_compiler/"
                f"{_registry_row(manifest, workstream_id)['card']['path']}",
            )
        )
        for workstream_id in ("CC-012", "CC-014", "CC-016")
    }

    assert manifest["revision"] == 2
    assert manifest["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    assert states["CC-012"] == "COMPLETE"
    assert states["CC-014"] == states["CC-016"] == "PAUSED"
    assert cards["CC-012"]["candidate"]["state"] == "ELIGIBLE"
    assert cards["CC-012"]["ledger"]["state"] == "RECORDED"
    for workstream_id in ("CC-014", "CC-016"):
        assert cards[workstream_id]["candidate"] == {"state": "NONE"}
        assert cards[workstream_id]["ledger"] == {"state": "NOT_STARTED"}
    assert "CC-012" not in manifest["selections"]
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}
    control_ids = {"CC-012", "CC-014", "CC-016"}
    for workstream_id, card in cards.items():
        assert control_ids.isdisjoint(
            _registry_row(manifest, workstream_id)["depends_on"]
        )
        assert control_ids.isdisjoint(
            binding["workstream_id"]
            for binding in card["authorization"].get("dependency_bindings", [])
        )
    later_activations = [
        entry
        for entry in _overseer_prefix(257).entries
        if entry["sequence"] > 254
        and entry["entry_type"] == "WORKSTREAM_STATE"
        and entry["data"]["workstream_id"] in {"CC-014", "CC-016"}
        and entry["data"]["new_state"] == "ACTIVE"
    ]
    assert later_activations == []


def test_quiet_bell_process_lessons_transfer_no_semantics() -> None:
    report = _read_json(CONTRACT / "overseer/evidence/CC-012-completion.json")
    lessons = next(
        check["observed"]
        for check in report["checks"]
        if check["check_id"] == "cc012-process-lessons"
    )
    for phrase in (
        "historical tests read historical Git",
        "accepted and refused shapes",
        "every semantic section and union arm",
        "authored-local from compiled",
        "missing exact import atomically refuses",
        "each identity layer separately",
        "own sources and accepted decisions",
        "process technique only",
    ):
        assert phrase in lessons
    for forbidden in (
        "expected values transfer",
        "facts transfer",
        "identifiers transfer",
        "derivations transfer",
        "helper transfer",
        "interface transfer",
        "DAG edge transfer",
    ):
        assert forbidden not in lessons


def _greenhouse_reactivation_commit() -> str:
    authority = next(
        entry
        for entry in _raw_overseer_state().entries
        if entry["entry_id"] == "OVR-000263"
    )
    return integration_module._authority_entry_commit(
        ROOT,
        authority,
        "design/contract_compiler/overseer",
    )


def test_greenhouse_reactivation_boundary_is_exact() -> None:
    activation_commit = _greenhouse_reactivation_commit()
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{activation_commit}:design/contract_compiler/integration.json",
        )
    )
    row = _registry_row(manifest, "CC-016")
    card_path = f"design/contract_compiler/{row['card']['path']}"
    card_source = subprocess.run(
        ["git", "show", f"{activation_commit}:{card_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    card = json.loads(card_source)
    states, _ = integration_module._workstream_states(_overseer_prefix(263))

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-016/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert card["assignment"] == {
        "owner_id": "worker:cc016-neutral-oracles",
        "state": "ASSIGNED",
        "task_id": "/root/cc016_neutral_oracles",
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
        == GREENHOUSE_DEPENDENCIES
    )
    assert card["candidate"] == {"state": "NONE"}
    assert card["ledger"] == {"state": "NOT_STARTED"}
    assert card["responsibility"] == GREENHOUSE_ORACLE_RESPONSIBILITY
    for token in GREENHOUSE_PRIVATE_TOKENS:
        assert token in card["responsibility"]
    for forbidden in ("public format", "Quiet Bell expected value transfer"):
        assert forbidden not in card["responsibility"]

    control_ids = {"CC-012", "CC-014", "CC-016"}
    assert control_ids.isdisjoint(row["depends_on"])
    assert control_ids.isdisjoint(
        binding["workstream_id"]
        for binding in card["authorization"]["dependency_bindings"]
    )
    assert states["CC-012"] == "COMPLETE"
    assert states["CC-016"] == "ACTIVE"
    assert states["CC-014"] == "PAUSED"
    assert "CC-016" not in manifest["selections"]
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}
    assert (
        _git(
            ROOT,
            "ls-tree",
            "-r",
            "--name-only",
            activation_commit,
            "--",
            "conformance/contract_kernel/v0/neutral_domain/oracle",
            "conformance/contract_kernel/v0/neutral_domain/traces/oracle",
            "conformance/contract_compiler/v0/evidence/CC-016.json",
            "tests/contract_compiler/test_neutral_domain_oracles.py",
        )
        == ""
    )


def test_greenhouse_reactivation_report_is_exact() -> None:
    activation_commit = _greenhouse_reactivation_commit()
    report = _read_json(CONTRACT / "overseer/evidence/CC-016-reactivation.json")

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-016"
    assert report["base_commit"] == GREENHOUSE_REACTIVATION_BASE
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            ["git", "show", f"{activation_commit}:{artifact['path']}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    checks = {check["check_id"]: check for check in report["checks"]}
    assert set(checks) == {
        "cc016-reactivation-red",
        "cc016-dependency-readiness",
        "cc016-private-representation",
        "cc016-independent-authorship",
        "cc016-quiet-bell-separation",
        "cc016-adjacent-state",
        "cc016-kiss-reactivation",
    }
    assert all(check["result"] == "PASS" for check in checks.values())
    assert all(
        any(term in limitation.lower() for limitation in report["limitations"])
        for term in ("answer-key", "public", "compiler", "corpus", "cc-r")
    )

    base_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", GREENHOUSE_REACTIVATION_BASE)
    )
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    assert report_time > base_time


def test_greenhouse_reactivation_transaction_is_exact() -> None:
    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 261 <= entry["sequence"] <= 263
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000261",
        "OVR-000262",
        "OVR-000263",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "cc016-reactivation-boundary",
        "cc016-reactivation-verification",
        "CC-016",
    )
    revision, verification, activation = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-016"]
    assert {document["path"] for document in revision["data"]["documents"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-016-reactivation.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    assert verification["actor"] == {
        "id": "cc016-reactivation-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert activation["data"]["workstream_id"] == "CC-016"
    assert activation["data"]["previous_state"] == "PAUSED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is False
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000261",
        "OVR-000262",
    ]
    assert verification["previous_entry_hash"] == revision["entry_hash"]
    assert activation["previous_entry_hash"] == verification["entry_hash"]

    report_time = datetime.fromisoformat(
        _read_json(CONTRACT / "overseer/evidence/CC-016-reactivation.json")[
            "recorded_at"
        ].replace("Z", "+00:00")
    )
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )


def test_greenhouse_completion_candidate_is_exact_and_private() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-016")
    card_path = CONTRACT / row["card"]["path"]
    card_source = card_path.read_bytes()
    card = _read_json(card_path)
    report_path = ROOT / "conformance/contract_compiler/v0/evidence/CC-016.json"
    report_source = report_path.read_bytes()
    report = _read_json(report_path)

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-016/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_kernel/v0/neutral_domain/oracle/greenhouse.json",
        "conformance/contract_kernel/v0/neutral_domain/traces/oracle/compile-source-outcomes.json",
        "tests/contract_compiler/test_neutral_domain_oracles.py",
    }
    assert card["candidate"] == {
        "artifacts": report["artifacts"],
        "base_commit": GREENHOUSE_CANDIDATE_BASE,
        "evidence": [
            {
                "byte_length": len(report_source),
                "path": "conformance/contract_compiler/v0/evidence/CC-016.json",
                "result": "PASS",
                "sha256": _digest(report_source),
            }
        ],
        "head_commit": GREENHOUSE_CANDIDATE_COMMIT,
        "head_tree": GREENHOUSE_CANDIDATE_TREE,
        "state": "ELIGIBLE",
    }
    assert card["responsibility"] == GREENHOUSE_ORACLE_RESPONSIBILITY
    assert "CC-016" not in manifest["selections"]
    scopes, authority = _greenhouse_candidate_authority()
    touched = validate_candidate_history(
        ROOT,
        card["candidate"],
        allowed_scopes=scopes,
        workstream_id="CC-016",
        authority_entry=authority,
        overseer_path="design/contract_compiler/overseer",
        enforce_clean_base=True,
    )
    assert touched == tuple(sorted(GREENHOUSE_CANDIDATE_PATHS))


def test_greenhouse_completion_worker_chain_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    card = _read_json(CONTRACT / _registry_row(manifest, "CC-016")["card"]["path"])
    ledger_root = CONTRACT / "workstreams/CC-016/ledger"
    entries = [
        _read_json(path) for path in sorted((ledger_root / "entries").glob("*.json"))
    ]
    head = _read_json(ledger_root / "head.json")

    assert len(entries) == 7
    assert [entry["data"]["phase"] for entry in entries] == list(
        integration_module.TDD_PHASES
    )
    assert [entry["data"]["result"] for entry in entries] == [
        "EXPECTED_FAILURE",
        "PASS",
        "PASS",
        "PASS",
        "PASS",
        "NOT_APPLICABLE",
        "PASS",
    ]
    assert {entry["actor_id"] for entry in entries} == {
        "worker:cc016-neutral-oracles"
    }
    candidate_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", GREENHOUSE_CANDIDATE_COMMIT)
    )
    entry_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in entries
    )
    assert entry_times[0] > candidate_time
    assert all(later > earlier for earlier, later in zip(entry_times, entry_times[1:]))
    assert "2 failures and 20 passes" in entries[0]["data"]["observed"]
    assert "All 28 fixed Greenhouse" in entries[1]["data"]["observed"]
    assert "seven-commit" in entries[2]["data"]["observed"]
    assert "14 mutation" in entries[3]["data"]["observed"]
    assert "129 contract-compiler" in entries[4]["data"]["observed"]
    assert "NOT_APPLICABLE" in entries[5]["data"]["observed"]
    assert GREENHOUSE_CANDIDATE_COMMIT in entries[6]["data"]["command"]
    assert "no P0-P3" in entries[6]["data"]["observed"]

    previous = "GENESIS"
    for entry in entries:
        assert entry["previous_entry_hash"] == previous
        assert entry["entry_hash"] == integration_module.worker_entry_hash(entry)
        previous = entry["entry_hash"]
    assert head == {
        "canonicalization": "malleus-canonical-json-v1",
        "entry_count": 7,
        "head_entry_id": "CC-016-WRK-000007",
        "head_hash": entries[-1]["entry_hash"],
        "schema": "malleus.contract-compiler.worker-ledger-head/v1",
        "workstream_id": "CC-016",
    }
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": "CC-016-WRK-000007",
        "head_hash": head["head_hash"],
        "path": "workstreams/CC-016/ledger",
        "state": "RECORDED",
    }


def test_greenhouse_completion_semantics_are_exact() -> None:
    oracle = _read_json(
        ROOT / "conformance/contract_kernel/v0/neutral_domain/oracle/greenhouse.json"
    )
    operations = _read_json(
        ROOT
        / "conformance/contract_kernel/v0/neutral_domain/traces/oracle/compile-source-outcomes.json"
    )["operations"]
    canonical_facts = json.dumps(
        oracle["baseline_facts"],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    assert len(oracle["baseline_facts"]) == 90
    assert len(canonical_facts) == 17906
    assert hashlib.sha256(canonical_facts).hexdigest() == (
        "4103a7cf5db383a1bf29f88bcf94e0057707ea94452f0a36a073b9bb95564db4"
    )
    assert len(oracle["semantic_change"]["removed_facts"]) == 2
    assert len(oracle["semantic_change"]["added_facts"]) == 2
    assert {source["outcome"] for source in oracle["sources"]} == {"ACCEPT"}
    assert len(operations) == 6
    assert {operation["outcome"] for operation in operations} == {"ACCEPT"}
    assert {len(operation["relations"]) for operation in operations} == {11}
    assert all(
        operation["relations"]["logical_artifact"] == "NOT_CLAIMED"
        for operation in operations
    )
    assert oracle["configuration"]["artifact_role"] == "CONFORMANCE_FIXTURE"
    assert oracle["configuration"]["public_contract"] is False


def test_greenhouse_completion_report_is_bounded() -> None:
    report = _read_json(CONTRACT / "overseer/evidence/CC-016-completion.json")
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-016"
    assert report["base_commit"] == GREENHOUSE_CANDIDATE_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_compiler/v0/evidence/CC-016.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-016/ledger/head.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
    }
    for artifact in report["artifacts"]:
        source = _git_bytes(
            ROOT,
            "show",
            f"{GREENHOUSE_COMPLETION_COMMIT}:{artifact['path']}",
        )
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    checks = {check["check_id"]: check for check in report["checks"]}
    assert set(checks) == {
        "cc016-candidate-history",
        "cc016-card-report-equality",
        "cc016-semantic-boundary",
        "cc016-worker-tdd",
        "cc016-dependencies",
        "cc016-independent-audit",
        "cc016-regression",
        "cc016-unselected-completion",
        "cc016-process-lessons",
    }
    assert all(check["result"] == "PASS" for check in checks.values())
    assert any("private" in limitation.lower() for limitation in report["limitations"])
    assert any("optional profile" in limitation.lower() for limitation in report["limitations"])
    assert any("CC-R" in limitation for limitation in report["limitations"])


def test_greenhouse_completion_transaction_and_adjacent_state_are_exact() -> None:
    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 265 <= entry["sequence"] <= 267
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000265",
        "OVR-000266",
        "OVR-000267",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, completion = transaction
    assert tuple(entry["subject"] for entry in transaction) == (
        {"id": "cc016-completion-boundary", "type": "DOCUMENT"},
        {"id": "cc016-completion-verification", "type": "EVIDENCE"},
        {"id": "CC-016", "type": "WORKSTREAM"},
    )
    expected_documents = {
        "conformance/contract_compiler/v0/evidence/CC-016.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-016-completion.json",
        "design/contract_compiler/workstreams/CC-016/ledger/head.json",
        "design/contract_compiler/workstreams/CC-016/manifest.json",
        "tests/test_contract_compiler_integration.py",
        *{
            "design/contract_compiler/workstreams/CC-016/ledger/entries/"
            f"CC-016-WRK-{sequence:06d}.json"
            for sequence in range(1, 8)
        },
    }
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-016"]
    assert {document["path"] for document in revision["data"]["documents"]} == (
        expected_documents
    )
    assert verification["actor"] == {
        "id": "cc016-completion-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert completion["data"]["previous_state"] == "ACTIVE"
    assert completion["data"]["new_state"] == "COMPLETE"
    assert completion["data"]["bootstrap"] is False
    assert completion["data"]["workstream_id"] == "CC-016"
    assert completion["data"]["blockers"] == []
    assert completion["data"]["evidence_entry_ids"] == ["OVR-000266"]
    assert verification["previous_entry_hash"] == revision["entry_hash"]
    assert completion["previous_entry_hash"] == verification["entry_hash"]

    report_time = datetime.fromisoformat(
        _read_json(CONTRACT / "overseer/evidence/CC-016-completion.json")[
            "recorded_at"
        ].replace("Z", "+00:00")
    )
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )

    states, _ = integration_module._workstream_states(_overseer_prefix(267))
    manifest = _read_json(INTEGRATION)
    card = _read_json(CONTRACT / _registry_row(manifest, "CC-016")["card"]["path"])
    assert states["CC-012"] == states["CC-016"] == "COMPLETE"
    assert states["CC-014"] == "PAUSED"
    assert card["candidate"]["state"] == "ELIGIBLE"
    assert card["ledger"]["state"] == "RECORDED"
    assert "CC-016" not in manifest["selections"]


def test_small_shop_program_boundary_is_exact() -> None:
    source = PROGRAM.read_text(encoding="utf-8")
    for exact in (
        "Ontology/domain sources plus raw `SCENARIO_SELECTION` and "
        "`SOURCE_TIME_CONTEXT` fixture parameters only; no normalized values, "
        "expected values, mappings, transformations, recipes, operations, outcomes, "
        "compiler, runtime, protocol, or accepted graph state",
        "CC-021 owns controlled ontology and domain source bytes plus raw "
        "`SCENARIO_SELECTION` and `SOURCE_TIME_CONTEXT` fixture parameters only.",
        "The parameter members may select the retained occurrence/entity tuple and "
        "declare fixture-local source format, calendar, synthetic year, and timezone.",
        "They contain no normalized values or outputs and implement no mapping or "
        "transformation.",
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


def test_cc021_provisional_commit_is_classified_without_candidate_authority() -> None:
    provisional_paths = {
        "conformance/contract_compiler/v0/evidence/CC-021.json",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/configuration/ret-010-selection.json",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/configuration/time-context.json",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/manifest.json",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/sources/inventory-units.csv",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/sources/warehouse.jsonl",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop-description-only.yaml",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop-root-instances.yaml",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop.yaml",
        "tests/contract_compiler/test_small_shop_fixture_inputs.py",
    }
    parameter_paths = {
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/configuration/ret-010-selection.json",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/configuration/time-context.json",
    }
    inherited_paths = {
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/sources/inventory-units.csv",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/sources/warehouse.jsonl",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop-description-only.yaml",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop-root-instances.yaml",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/tbox/small-shop.yaml",
    }
    required_reissue = provisional_paths - inherited_paths

    assert _git(ROOT, "rev-parse", f"{SMALL_SHOP_PROVISIONAL_COMMIT}^") == (
        SMALL_SHOP_OPERATOR_APPROVAL
    )
    assert _git(ROOT, "rev-parse", f"{SMALL_SHOP_PROVISIONAL_COMMIT}^{{tree}}") == (
        SMALL_SHOP_PROVISIONAL_TREE
    )
    assert (
        set(
            _git(
                ROOT,
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                SMALL_SHOP_PROVISIONAL_COMMIT,
            ).splitlines()
        )
        == provisional_paths
    )
    assert parameter_paths == {
        path for path in provisional_paths if "/configuration/" in path
    }
    assert len(parameter_paths) == 2
    assert len(inherited_paths) == 5
    assert required_reissue == {
        "conformance/contract_compiler/v0/evidence/CC-021.json",
        *parameter_paths,
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/"
        "input/manifest.json",
        "tests/contract_compiler/test_small_shop_fixture_inputs.py",
    }

    manifest = _read_json(INTEGRATION)
    assert "CC-021" not in manifest["selections"]
    assert manifest["authority"]["snapshot"]["result_commit"] != (
        SMALL_SHOP_PROVISIONAL_COMMIT
    )
    for row in manifest["workstreams"]:
        if row["card"]["state"] != "PRESENT":
            continue
        card = _read_json(CONTRACT / row["card"]["path"])
        candidate = card["candidate"]
        assert candidate.get("base_commit") != SMALL_SHOP_PROVISIONAL_COMMIT
        assert candidate.get("head_commit") != SMALL_SHOP_PROVISIONAL_COMMIT
        for binding in card["authorization"].get("dependency_bindings", []):
            assert binding["integrated_head"] != SMALL_SHOP_PROVISIONAL_COMMIT


def test_cc021_authorization_recovery_evidence_is_exact() -> None:
    report_path = (
        CONTRACT / "overseer" / "evidence" / "CC-021-authorization-recovery.json"
    )
    report = _read_json(report_path)
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-021"
    assert report["base_commit"] == SMALL_SHOP_PROVISIONAL_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/program.md",
        "design/contract_compiler/workstreams/CC-021/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{SMALL_SHOP_AUTHORITY_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    checks = {check["check_id"]: check for check in report["checks"]}
    assert set(checks) == {
        "cc021-operator-intent-precedes-provisional",
        "cc021-old-card-authority",
        "cc021-provisional-diff",
        "cc021-scope-classification",
        "cc021-provisional-nonauthority",
        "cc021-prospective-reauthorization",
        "cc021-unchanged-boundaries",
        "cc021-forbidden-side-effects",
    }
    assert all(check["result"] == "PASS" for check in checks.values())
    assert (
        SMALL_SHOP_OPERATOR_APPROVAL
        in checks["cc021-operator-intent-precedes-provisional"]["observed"]
    )
    assert SMALL_SHOP_PROVISIONAL_COMMIT in checks["cc021-provisional-diff"]["observed"]
    assert (
        "sha256:645787b641fce5e7da1314c80e27f5df3117fd8b332c73c3932030260968a7d1"
        in checks["cc021-old-card-authority"]["observed"]
    )
    assert "2960 bytes" in checks["cc021-old-card-authority"]["observed"]
    assert any("candidate" in limitation for limitation in report["limitations"])
    assert any("CC-R" in limitation for limitation in report["limitations"])


def test_cc021_authorization_recovery_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 216 <= entry["sequence"] <= 219)
    assert tuple(entry["entry_id"] for entry in transaction) == tuple(
        f"OVR-{sequence:06d}" for sequence in range(216, 220)
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "cc021-authorization-recovery",
        "cc021-authorization-recovery-verification",
        "CC-021",
        "CC-021",
    )
    revision, verification, paused, active = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-021"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/integration.json": "MODIFIED",
        "design/contract_compiler/overseer/evidence/"
        "CC-021-authorization-recovery.json": "CREATED",
        "design/contract_compiler/program.md": "MODIFIED",
        "design/contract_compiler/workstreams/CC-021/manifest.json": "MODIFIED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    report_path = (
        CONTRACT / "overseer" / "evidence" / "CC-021-authorization-recovery.json"
    )
    report_digest = _digest(report_path.read_bytes())
    revision_refs = {
        (reference["relation"], reference["type"], reference["target"])
        for reference in revision["references"]
    }
    assert (
        "EVIDENCES",
        "EVIDENCE",
        "design/contract_compiler/overseer/evidence/CC-021-authorization-recovery.json",
    ) in revision_refs
    assert (
        next(
            reference
            for reference in revision["references"]
            if reference["type"] == "EVIDENCE"
        )["digest"]
        == report_digest
    )
    assert {
        reference["target"]
        for reference in revision["references"]
        if reference["type"] == "COMMIT"
    } == {SMALL_SHOP_OPERATOR_APPROVAL, SMALL_SHOP_PROVISIONAL_COMMIT}
    assert {
        (reference["relation"], reference["type"], reference["target"])
        for reference in verification["references"]
    } >= {
        ("EVIDENCES", "ENTRY", "OVR-000216"),
        ("EVIDENCES", "COMMIT", SMALL_SHOP_OPERATOR_APPROVAL),
        ("EVIDENCES", "COMMIT", SMALL_SHOP_PROVISIONAL_COMMIT),
        ("AFFECTS", "WORKSTREAM", "CC-021"),
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert any(
        "provisional noncandidate" in claim.lower()
        for claim in verification["data"]["claims"]
    )
    assert any(
        "prospective" in claim.lower() for claim in verification["data"]["claims"]
    )

    assert paused["data"]["previous_state"] == "ACTIVE"
    assert paused["data"]["new_state"] == "PAUSED"
    assert paused["data"]["bootstrap"] is False
    assert paused["data"]["evidence_entry_ids"] == [
        "OVR-000216",
        "OVR-000217",
    ]
    assert len(paused["data"]["blockers"]) == 1
    assert "cannot gate candidacy" in paused["data"]["blockers"][0]

    assert active["data"]["previous_state"] == "PAUSED"
    assert active["data"]["new_state"] == "ACTIVE"
    assert active["data"]["bootstrap"] is False
    assert active["data"]["evidence_entry_ids"] == [
        "OVR-000216",
        "OVR-000217",
    ]
    assert active["data"]["blockers"] == []
    assert SMALL_SHOP_RESPONSIBILITY in " ".join(active["data"]["deliverables"])
    assert any(
        "first commit containing OVR-000219" in deliverable
        for deliverable in active["data"]["deliverables"]
    )

    report = _read_json(report_path)
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    provisional_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", SMALL_SHOP_PROVISIONAL_COMMIT)
    )
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert report_time > provisional_time
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )


def test_cc021_completion_evidence_and_worker_chain_are_exact() -> None:
    manifest = _read_json(INTEGRATION)
    card = _read_json(CONTRACT / _registry_row(manifest, "CC-021")["card"]["path"])
    ledger_root = CONTRACT / "workstreams" / "CC-021" / "ledger"
    entries = [
        _read_json(path) for path in sorted((ledger_root / "entries").glob("*.json"))
    ]
    head = _read_json(ledger_root / "head.json")
    assert len(entries) == 7
    assert [entry["data"]["phase"] for entry in entries] == list(
        integration_module.TDD_PHASES
    )
    assert entries[0]["data"]["result"] == "EXPECTED_FAILURE"
    assert entries[5]["data"]["result"] == "NOT_APPLICABLE"
    assert all(
        entry["data"]["result"] == "PASS" for entry in (*entries[1:5], entries[6])
    )
    assert {entry["actor_id"] for entry in entries} == {
        "worker:cc021-small-shop-inputs"
    }
    assert head == {
        "canonicalization": "malleus-canonical-json-v1",
        "entry_count": 7,
        "head_entry_id": "CC-021-WRK-000007",
        "head_hash": entries[-1]["entry_hash"],
        "schema": "malleus.contract-compiler.worker-ledger-head/v1",
        "workstream_id": "CC-021",
    }
    assert card["ledger"]["head_hash"] == head["head_hash"]

    report_path = CONTRACT / "overseer" / "evidence" / "CC-021-completion.json"
    report = _read_json(report_path)
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-021"
    assert report["base_commit"] == SMALL_SHOP_CANDIDATE_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_compiler/v0/evidence/CC-021.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-021/ledger/head.json",
        "design/contract_compiler/workstreams/CC-021/manifest.json",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{SMALL_SHOP_INPUT_COMPLETION_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("CC-022" in limitation for limitation in report["limitations"])
    assert any("package" in limitation.lower() for limitation in report["limitations"])


def test_cc021_candidate_reissue_and_inheritance_are_mechanical() -> None:
    ovr219_path = "design/contract_compiler/overseer/entries/OVR-000219.json"
    assert (
        _git(
            ROOT,
            "log",
            "--format=%H",
            "--diff-filter=A",
            "--",
            ovr219_path,
        )
        == SMALL_SHOP_AUTHORITY_COMMIT
    )
    assert (
        subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"{SMALL_SHOP_AUTHORITY_COMMIT}^:{ovr219_path}",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
        ).returncode
        != 0
    )
    assert (
        set(
            _git(
                ROOT,
                "diff",
                "--name-only",
                f"{SMALL_SHOP_AUTHORITY_COMMIT}..{SMALL_SHOP_CANDIDATE_COMMIT}",
            ).splitlines()
        )
        == SMALL_SHOP_CANDIDATE_PATHS
    )

    for path in SMALL_SHOP_INHERITED_PATHS:
        provisional = subprocess.run(
            ["git", "show", f"{SMALL_SHOP_PROVISIONAL_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        authority = subprocess.run(
            ["git", "show", f"{SMALL_SHOP_AUTHORITY_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        candidate = subprocess.run(
            ["git", "show", f"{SMALL_SHOP_CANDIDATE_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert provisional == authority == candidate

    for name in ("ret-010-selection.json", "time-context.json"):
        path = f"{SMALL_SHOP_INPUT_ROOT}/configuration/{name}"
        provisional = subprocess.run(
            ["git", "show", f"{SMALL_SHOP_PROVISIONAL_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        candidate = subprocess.run(
            ["git", "show", f"{SMALL_SHOP_CANDIDATE_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert provisional != candidate
        assert json.loads(provisional) == json.loads(candidate)


def test_cc021_completion_transaction_is_exact() -> None:
    entries = _raw_overseer_state().entries
    transaction = tuple(entry for entry in entries if 220 <= entry["sequence"] <= 222)
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000220",
        "OVR-000221",
        "OVR-000222",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, completion = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-021"]
    revision_paths = {item["path"] for item in revision["data"]["documents"]}
    assert revision_paths == {
        "conformance/contract_compiler/v0/evidence/CC-021.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-021-completion.json",
        "design/contract_compiler/workstreams/CC-021/ledger/head.json",
        "design/contract_compiler/workstreams/CC-021/manifest.json",
        "tests/test_contract_compiler_integration.py",
        *{
            "design/contract_compiler/workstreams/CC-021/ledger/entries/"
            f"CC-021-WRK-{sequence:06d}.json"
            for sequence in range(1, 8)
        },
    }
    assert verification["actor"] == {
        "id": "cc021-completion-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert completion["data"]["previous_state"] == "ACTIVE"
    assert completion["data"]["new_state"] == "COMPLETE"
    assert completion["data"]["blockers"] == []
    assert completion["data"]["evidence_entry_ids"] == ["OVR-000221"]
    assert ("SATISFIES", "WORKSTREAM", "CC-021") in {
        (reference["relation"], reference["type"], reference["target"])
        for reference in completion["references"]
    }


def test_cc021_completion_preserves_paused_controls_and_future_implementation() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_INPUT_COMPLETION_COMMIT}:design/contract_compiler/integration.json",
        )
    )
    states, _ = integration_module._workstream_states(_overseer_prefix(222))

    assert states["CC-021"] == "COMPLETE"
    assert states["CC-012"] == "PAUSED"
    assert states["CC-014"] == "PAUSED"
    assert states["CC-016"] == "PAUSED"
    oracle_row = _registry_row(manifest, "CC-022")
    assert oracle_row["card"] == {"state": "ABSENT"}
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}


def test_small_shop_oracle_activation_boundary_is_exact() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/integration.json",
        )
    )
    prior_manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ORACLE_DECISION_COMMIT}:design/contract_compiler/integration.json",
        )
    )
    oracle_paths = (
        SMALL_SHOP_ORACLE_ROOT,
        "conformance/contract_compiler/v0/evidence/CC-022.json",
        "tests/contract_compiler/test_small_shop_fixture_oracle.py",
    )

    assert len(manifest["workstreams"]) == 69
    assert manifest["revision"] == 2
    assert manifest["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}
    assert all(
        subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:{path}",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
        ).returncode
        != 0
        for path in oracle_paths
    )
    assert {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
        if row["workstream_id"] != "CC-022"
    } == {
        row["workstream_id"]: row
        for row in prior_manifest["workstreams"]
        if row["workstream_id"] != "CC-022"
    }
    for key in (
        "authority",
        "canonicalization",
        "owner_separations",
        "program_id",
        "reserved_scopes",
        "revision",
        "schema",
        "selections",
    ):
        assert manifest[key] == prior_manifest[key]

    row = _registry_row(manifest, "CC-022")
    assert row["card"]["state"] == "PRESENT"
    card_source = subprocess.run(
        [
            "git",
            "show",
            f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/"
            f"{row['card']['path']}",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-022/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    card = json.loads(card_source)
    assert card["assignment"] == {
        "owner_id": "worker:cc022-small-shop-oracle",
        "state": "ASSIGNED",
        "task_id": "/root/cc022_small_shop_oracle",
    }
    assert card["authorization"]["class"] == "FORMAL"
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert tuple(
        binding["workstream_id"]
        for binding in card["authorization"]["dependency_bindings"]
    ) == (
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
    assert card["scopes"] == [
        {"kind": "TREE", "path": SMALL_SHOP_ORACLE_ROOT},
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-022.json",
        },
        {
            "kind": "FILE",
            "path": "tests/contract_compiler/test_small_shop_fixture_oracle.py",
        },
    ]
    assert card["candidate"] == {"state": "NONE"}
    assert card["ledger"] == {"state": "NOT_STARTED"}
    assert card["responsibility"] == SMALL_SHOP_ORACLE_RESPONSIBILITY
    assert "CC-022" not in manifest["selections"]

    cards = {
        workstream_id: json.loads(
            _git(
                ROOT,
                "show",
                f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/"
                f"{_registry_row(manifest, workstream_id)['card']['path']}",
            )
        )
        for workstream_id in ("CC-021", "CC-022")
    }
    assert (
        cards["CC-021"]["assignment"]["owner_id"]
        != (cards["CC-022"]["assignment"]["owner_id"])
    )
    assert {tuple(edge.values()) for edge in manifest["owner_separations"]} >= {
        ("CC-021", "CC-022"),
        ("CC-022", "CC-R09"),
    }


def test_small_shop_oracle_completion_candidate_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-022")
    card_path = CONTRACT / row["card"]["path"]
    card_source = card_path.read_bytes()
    card = _read_json(card_path)
    canonical_report = ROOT / "conformance/contract_compiler/v0/evidence/CC-022.json"
    report = _read_json(canonical_report)

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-022/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert card["candidate"] == {
        "artifacts": report["artifacts"],
        "base_commit": SMALL_SHOP_ORACLE_ACTIVATION_COMMIT,
        "evidence": [
            {
                "byte_length": len(canonical_report.read_bytes()),
                "path": "conformance/contract_compiler/v0/evidence/CC-022.json",
                "result": "PASS",
                "sha256": _digest(canonical_report.read_bytes()),
            }
        ],
        "head_commit": SMALL_SHOP_ORACLE_CANDIDATE_COMMIT,
        "head_tree": SMALL_SHOP_ORACLE_CANDIDATE_TREE,
        "state": "ELIGIBLE",
    }
    assert card["candidate"]["artifacts"] == report["artifacts"]
    assert card["responsibility"] == SMALL_SHOP_ORACLE_RESPONSIBILITY
    assert len(card["authorization"]["dependency_bindings"]) == 9
    validate_candidate_history(ROOT, card["candidate"], allowed_scopes=card["scopes"])


def test_small_shop_oracle_completion_worker_chain_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    card = _read_json(CONTRACT / _registry_row(manifest, "CC-022")["card"]["path"])
    ledger_root = CONTRACT / "workstreams/CC-022/ledger"
    entries = [
        _read_json(path) for path in sorted((ledger_root / "entries").glob("*.json"))
    ]
    head = _read_json(ledger_root / "head.json")

    assert len(entries) == 7
    assert [entry["data"]["phase"] for entry in entries] == list(
        integration_module.TDD_PHASES
    )
    assert entries[0]["data"]["result"] == "EXPECTED_FAILURE"
    assert entries[5]["data"]["result"] == "NOT_APPLICABLE"
    assert all(
        entry["data"]["result"] == "PASS" for entry in (*entries[1:5], entries[6])
    )
    assert {entry["actor_id"] for entry in entries} == {
        "worker:cc022-small-shop-oracle"
    }
    assert head["entry_count"] == 7
    assert head["head_entry_id"] == "CC-022-WRK-000007"
    assert head["head_hash"] == entries[-1]["entry_hash"]
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": "CC-022-WRK-000007",
        "head_hash": head["head_hash"],
        "path": "workstreams/CC-022/ledger",
        "state": "RECORDED",
    }


def test_small_shop_oracle_completion_report_is_bounded() -> None:
    report = _read_json(CONTRACT / "overseer/evidence/CC-022-completion.json")
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-022"
    assert report["base_commit"] == SMALL_SHOP_ORACLE_CANDIDATE_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_compiler/v0/evidence/CC-022.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-022/ledger/head.json",
        "design/contract_compiler/workstreams/CC-022/manifest.json",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{QUIET_BELL_REACTIVATION_BASE}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any(
        "tripwire" in limitation and "information-flow proof" in limitation
        for limitation in report["limitations"]
    )
    assert all(
        any(term.lower() in limitation.lower() for limitation in report["limitations"])
        for term in ("public", "mapping", "compiler", "protocol", "package", "CC-R")
    )


def test_small_shop_oracle_completion_transaction_is_exact() -> None:
    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 226 <= entry["sequence"] <= 228
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000226",
        "OVR-000227",
        "OVR-000228",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, completion = transaction
    expected_documents = {
        "conformance/contract_compiler/v0/evidence/CC-022.json",
        "design/contract_compiler/integration.json",
        "design/contract_compiler/overseer/evidence/CC-022-completion.json",
        "design/contract_compiler/workstreams/CC-022/ledger/head.json",
        "design/contract_compiler/workstreams/CC-022/manifest.json",
        "tests/test_contract_compiler_integration.py",
        *{
            "design/contract_compiler/workstreams/CC-022/ledger/entries/"
            f"CC-022-WRK-{sequence:06d}.json"
            for sequence in range(1, 8)
        },
    }
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-022"]
    assert {document["path"] for document in revision["data"]["documents"]} == (
        expected_documents
    )
    assert verification["actor"] == {
        "id": "cc022-completion-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert completion["data"]["previous_state"] == "ACTIVE"
    assert completion["data"]["new_state"] == "COMPLETE"
    assert completion["data"]["blockers"] == []
    assert completion["data"]["evidence_entry_ids"] == ["OVR-000227"]


def test_small_shop_oracle_completion_preserves_adjacent_authority() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{QUIET_BELL_REACTIVATION_BASE}:design/contract_compiler/integration.json",
        )
    )
    states, _ = integration_module._workstream_states(_overseer_prefix(228))
    assert len(manifest["workstreams"]) == 69
    assert (
        len(
            _read_json(CONTRACT / "workstreams/CC-022/manifest.json")["authorization"][
                "dependency_bindings"
            ]
        )
        == 9
    )
    assert len(manifest["owner_separations"]) == 15
    assert manifest["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    assert states["CC-022"] == "COMPLETE"
    assert states["CC-012"] == states["CC-014"] == states["CC-016"] == "PAUSED"
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}
    assert "CC-022" not in manifest["selections"]


def test_small_shop_oracle_activation_report_binds_operator_decision() -> None:
    decision_paths = {
        "research/ontology_driven_kg_realization/experiments/small_shop/CHARTER.md",
        "research/ontology_driven_kg_realization/experiments/small_shop/journal.jsonl",
        "research/ontology_driven_kg_realization/experiments/small_shop/journal.py",
        "research/ontology_driven_kg_realization/experiments/small_shop/test_journal.py",
    }
    assert _git(ROOT, "rev-parse", f"{SMALL_SHOP_ORACLE_DECISION_COMMIT}^{{tree}}") == (
        SMALL_SHOP_ORACLE_DECISION_TREE
    )
    assert (
        set(
            _git(
                ROOT,
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                SMALL_SHOP_ORACLE_DECISION_COMMIT,
            ).splitlines()
        )
        == decision_paths
    )
    journal = [
        json.loads(line)
        for line in (
            ROOT
            / "research/ontology_driven_kg_realization/experiments/small_shop/journal.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(journal) == 5
    assert journal[-1]["sequence"] == 5
    assert journal[-1]["record_hash"] == SMALL_SHOP_ORACLE_DECISION_HASH
    assert journal[-1]["payload"]["decision_key"] == (
        "small_shop_oracle_representation"
    )

    report_path = CONTRACT / "overseer/evidence/CC-022-activation.json"
    report = _read_json(report_path)
    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-022"
    assert report["base_commit"] == SMALL_SHOP_ORACLE_DECISION_COMMIT
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "design/contract_compiler/integration.json",
        "design/contract_compiler/workstreams/CC-022/manifest.json",
        "tests/test_contract_compiler_integration.py",
    }
    for artifact in report["artifacts"]:
        source = subprocess.run(
            [
                "git",
                "show",
                f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:{artifact['path']}",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)
    checks = {check["check_id"]: check for check in report["checks"]}
    assert set(checks) == {
        "cc022-activation-red",
        "cc022-dependency-readiness",
        "cc022-journal-decision-binding",
        "cc022-oracle-boundary",
        "cc022-owner-separation",
        "cc022-kiss-activation",
        "cc022-adjacent-state",
    }
    assert all(check["result"] == "PASS" for check in checks.values())
    assert (
        SMALL_SHOP_ORACLE_DECISION_COMMIT
        in checks["cc022-journal-decision-binding"]["observed"]
    )
    assert (
        SMALL_SHOP_ORACLE_DECISION_TREE
        in checks["cc022-journal-decision-binding"]["observed"]
    )
    assert (
        SMALL_SHOP_ORACLE_DECISION_HASH
        in checks["cc022-journal-decision-binding"]["observed"]
    )
    assert all(
        any(term in limitation for limitation in report["limitations"])
        for term in ("oracle bytes", "public format", "compiler", "CC-R09", "corpus")
    )

    decision_time = datetime.fromisoformat(
        _git(ROOT, "show", "-s", "--format=%cI", SMALL_SHOP_ORACLE_DECISION_COMMIT)
    )
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    assert report_time > decision_time


def test_small_shop_oracle_activation_transaction_is_exact() -> None:
    manifest = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/"
            "integration.json",
        )
    )
    states, _ = integration_module._workstream_states(_overseer_prefix(225))
    assert states["CC-021"] == "COMPLETE"
    assert states["CC-012"] == states["CC-014"] == states["CC-016"] == "PAUSED"
    assert _registry_row(manifest, "CC-R09")["card"] == {"state": "ABSENT"}

    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 223 <= entry["sequence"] <= 225
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000223",
        "OVR-000224",
        "OVR-000225",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    assert tuple(entry["subject"]["id"] for entry in transaction) == (
        "cc022-activation-boundary",
        "cc022-activation-verification",
        "CC-022",
    )
    revision, verification, activation = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-022"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/integration.json": "MODIFIED",
        "design/contract_compiler/overseer/evidence/CC-022-activation.json": "CREATED",
        "design/contract_compiler/workstreams/CC-022/manifest.json": "CREATED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    report_path = CONTRACT / "overseer/evidence/CC-022-activation.json"
    report_digest = _digest(report_path.read_bytes())
    assert (
        next(
            reference
            for reference in revision["references"]
            if reference["type"] == "EVIDENCE"
        )["digest"]
        == report_digest
    )
    assert {
        (reference["relation"], reference["type"], reference["target"])
        for reference in revision["references"]
    } >= {
        ("EVIDENCES", "COMMIT", SMALL_SHOP_ORACLE_DECISION_COMMIT),
        ("IMPLEMENTS", "WORKSTREAM", "CC-022"),
    }
    assert verification["actor"] == {
        "id": "cc022-activation-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert {
        (reference["relation"], reference["type"], reference["target"])
        for reference in verification["references"]
    } >= {
        ("EVIDENCES", "ENTRY", "OVR-000223"),
        ("EVIDENCES", "COMMIT", SMALL_SHOP_ORACLE_DECISION_COMMIT),
        ("AFFECTS", "WORKSTREAM", "CC-022"),
    }
    assert activation["data"]["workstream_id"] == "CC-022"
    assert activation["data"]["previous_state"] == "PLANNED"
    assert activation["data"]["new_state"] == "ACTIVE"
    assert activation["data"]["bootstrap"] is True
    assert activation["data"]["blockers"] == []
    assert activation["data"]["evidence_entry_ids"] == [
        "OVR-000223",
        "OVR-000224",
    ]
    assert activation["data"]["deliverables"] == [
        "Hand-author exactly tbox-expectations.json and ret-000-ret-010.json as private fixture-local logical JSON answer-key evidence.",
        "Bind the approved operator decision, accepted ontology decisions, OKG-FX001, and completed controlled Small Shop inputs without consuming implementation output.",
        "Keep the oracle test-only and non-public; create no compiler input, mapping, recipe, operation, protocol, ledger, knowledge graph, replay, corpus, package, release, integration, or CC-R bytes.",
    ]

    report = _read_json(report_path)
    report_time = datetime.fromisoformat(report["recorded_at"].replace("Z", "+00:00"))
    transaction_times = tuple(
        datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00"))
        for entry in transaction
    )
    assert transaction_times[0] > report_time
    assert all(
        later > earlier
        for earlier, later in zip(transaction_times, transaction_times[1:])
    )
    head = json.loads(
        _git(
            ROOT,
            "show",
            f"{SMALL_SHOP_ORACLE_ACTIVATION_COMMIT}:design/contract_compiler/overseer/head.json",
        )
    )
    assert head["entry_count"] == 225
    assert head["head_entry_id"] == "OVR-000225"
    assert head["head_hash"] == activation["entry_hash"]


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
            SMALL_SHOP_ACTIVATION_COMMIT,
            "--",
            *unchanged,
        )
        == ""
    )
    canonical = _git(
        ROOT,
        "show",
        f"{SMALL_SHOP_ACTIVATION_COMMIT}:design/PROTOCOL_FOUNDATION_GRAPH.ttl",
    )
    assert "# Design graph revision: 21" in canonical
    assert "<https://malleus.dev/ontology-kg-realization/OKG-FX001>" in canonical


def test_formal_workstream_cannot_be_paused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = integration_module._workstream_states

    def pause_cc012(ledger_state):
        states, entries = original(ledger_state)
        states["CC-012"] = "PAUSED"
        return states, entries

    monkeypatch.setattr(integration_module, "_workstream_states", pause_cc012)
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
    assert f"validated 72 workstreams, {present_cards} cards," in result.stdout


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


def test_formal_activation_lists_incomplete_dependencies(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    original_states = integration_module._workstream_states

    def one_incomplete_dependency(ledger_state):
        states, entries = original_states(ledger_state)
        states["CC-014"] = "PAUSED"
        return states, entries

    monkeypatch.setattr(
        integration_module,
        "_workstream_states",
        one_incomplete_dependency,
    )
    _rewrite_card(
        path,
        manifest,
        "CC-014",
        lambda card: card.update(
            authorization={
                "class": "BLOCKED",
                "authorized_by": {"id": "operator", "type": "OPERATOR"},
                "blockers": ["Synthetic incomplete-dependency control."],
            }
        ),
    )

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
    assert "CC-016" not in str(error.value)
    assert "CC-014" in str(error.value)


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


@pytest.mark.parametrize(
    "copy_authority_entry",
    (False, True),
    ids=("missing-entry", "copied-entry"),
)
def test_stale_quiet_bell_branch_cannot_bypass_candidate_authority(
    tmp_path: Path,
    copy_authority_entry: bool,
) -> None:
    repository, candidate = _quiet_bell_history_candidate(
        tmp_path,
        base_commit=QUIET_BELL_REACTIVATION_COMMIT,
        copy_authority_entry=copy_authority_entry,
    )
    scopes, authority = _quiet_bell_candidate_authority()

    validate_candidate_history(
        repository,
        candidate,
        allowed_scopes=scopes,
        workstream_id="CC-012",
    )
    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=scopes,
            workstream_id="CC-012",
            authority_entry=authority,
            overseer_path="design/contract_compiler/overseer",
        )

    _assert_code(error, "CC000_CANDIDATE_AUTHORITY")


@pytest.mark.parametrize("descendant_base", (False, True))
def test_authority_floor_accepts_equal_or_descendant_candidate_base(
    tmp_path: Path,
    descendant_base: bool,
) -> None:
    repository, candidate = _quiet_bell_history_candidate(
        tmp_path,
        base_commit=QUIET_BELL_REACTIVATION_REPAIR_COMMIT,
        descendant_base=descendant_base,
    )
    scopes, authority = _quiet_bell_candidate_authority()

    touched = validate_candidate_history(
        repository,
        candidate,
        allowed_scopes=scopes,
        workstream_id="CC-012",
        authority_entry=authority,
        overseer_path="design/contract_compiler/overseer",
    )

    assert set(touched) == {
        "conformance/contract_compiler/v0/evidence/CC-012.json",
        "conformance/contract_kernel/v0/themed_fixture/oracle/candidate.json",
    }


def test_integration_admits_every_unselected_integrable_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    admitted: list[str] = []

    def record_candidate(*args, workstream_id=None, **kwargs):
        if workstream_id is not None:
            admitted.append(workstream_id)
        return ()

    monkeypatch.setattr(
        integration_module,
        "validate_candidate_history",
        record_candidate,
    )

    validate_integration(ROOT)

    assert "CC-X01" in admitted


def test_candidate_authority_uses_latest_active_not_complete_or_superseded() -> None:
    authorities = integration_module._latest_active_authority_entries(
        _raw_overseer_state()
    )

    assert authorities["CC-021"]["entry_id"] == "OVR-000219"
    assert authorities["CC-012"]["entry_id"] == "OVR-000254"
    assert authorities["CC-016"]["entry_id"] == "OVR-000263"
    assert {"OVR-000231", "OVR-000240"}.isdisjoint(
        entry["entry_id"] for entry in authorities.values()
    )


def test_existing_nonbootstrap_candidates_satisfy_generic_authority_floor() -> None:
    manifest = _read_json(INTEGRATION)
    schema = _read_json(CONTRACT / "integration.schema.json")
    authorities = integration_module._latest_active_authority_entries(
        _raw_overseer_state()
    )
    checked = []
    for row in manifest["workstreams"]:
        if row["card"]["state"] != "PRESENT":
            continue
        card = _read_json(CONTRACT / row["card"]["path"])
        if card["candidate"]["state"] not in {"ELIGIBLE", "INTEGRATED"}:
            continue
        if card["workstream_id"] == "CC-000":
            continue
        worker_ledger = integration_module._validate_worker_ledger(
            CONTRACT,
            card,
            schema,
            integration_module.PurePosixPath("design/contract_compiler"),
        )
        validate_candidate_history(
            ROOT,
            card["candidate"],
            allowed_scopes=card["scopes"],
            workstream_id=card["workstream_id"],
            authority_entry=authorities[card["workstream_id"]],
            overseer_path="design/contract_compiler/overseer",
            worker_ledger=worker_ledger,
        )
        checked.append(card["workstream_id"])

    assert len(checked) == 17
    assert "CC-000" not in checked
    assert "CC-014" in checked


@pytest.mark.parametrize(
    ("prebase_path", "merge_prebase", "delete_prebase"),
    (
        ("allowed/stale.json", True, False),
        ("allowed/helper.py", True, False),
        ("allowed/transient.json", False, True),
    ),
    ids=("merged-stale-artifact", "merged-hidden-helper", "add-delete"),
)
def test_clean_base_refuses_every_prebase_scope_change(
    tmp_path: Path,
    prebase_path: str,
    merge_prebase: bool,
    delete_prebase: bool,
) -> None:
    repository, candidate, authority = _clean_base_candidate(
        tmp_path,
        prebase_path=prebase_path,
        merge_prebase=merge_prebase,
        delete_prebase=delete_prebase,
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_CANDIDATE_CLEAN_BASE")


def test_clean_base_refuses_content_bundled_with_authority(tmp_path: Path) -> None:
    repository, candidate, authority = _clean_base_candidate(
        tmp_path,
        authority_path="allowed/bundled.json",
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_CANDIDATE_CLEAN_BASE")


def test_clean_base_refuses_root_authority_with_bundled_content(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(
        tmp_path,
        authority_path="allowed/root-helper.py",
        root_authority=True,
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_CANDIDATE_CLEAN_BASE")


def test_clean_base_refuses_declared_output_reverted_to_base(tmp_path: Path) -> None:
    repository, candidate, authority = _clean_base_candidate(
        tmp_path,
        revert_output=True,
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_CANDIDATE_UNCHANGED")


def test_clean_base_accepts_exact_declared_candidate_delta(tmp_path: Path) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)

    touched = validate_candidate_history(
        repository,
        candidate,
        allowed_scopes=ALLOWED_SCOPES,
        workstream_id="CC-TEST",
        authority_entry=authority,
        overseer_path="governance",
        enforce_clean_base=True,
    )

    assert touched == ("allowed/result.txt", "evidence/checks.json")


def test_clean_base_accepts_exact_own_worker_ledger_as_sideband(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-TEST",
    )

    touched = validate_candidate_history(
        repository,
        candidate,
        allowed_scopes=ALLOWED_SCOPES,
        workstream_id="CC-TEST",
        authority_entry=authority,
        overseer_path="governance",
        enforce_clean_base=True,
        worker_ledger=worker_ledger,
    )

    assert touched == (
        "allowed/result.txt",
        "design/contract_compiler/workstreams/CC-TEST/ledger/entries/"
        "CC-TEST-WRK-000001.json",
        "design/contract_compiler/workstreams/CC-TEST/ledger/head.json",
        "evidence/checks.json",
    )


def test_candidate_cannot_use_another_workstream_ledger_as_sideband(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-OTHER",
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
            worker_ledger=worker_ledger,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_requires_workstream_id(
    tmp_path: Path,
) -> None:
    repository, candidate, _ = _clean_base_candidate(tmp_path)
    candidate, _ = _add_candidate_worker_ledger(repository, candidate, "CC-TEST")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_requires_validated_ledger(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, _ = _add_candidate_worker_ledger(repository, candidate, "CC-TEST")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_refuses_unexpected_own_file(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-TEST",
    )
    unexpected = (
        repository
        / "design"
        / "contract_compiler"
        / "workstreams"
        / "CC-TEST"
        / "ledger"
        / "notes.json"
    )
    _write_json(unexpected, {"not": "a worker-ledger entry"})
    head = _commit(repository, "add undeclared worker-ledger file")
    candidate["head_commit"] = head
    candidate["head_tree"] = _git(repository, "rev-parse", f"{head}^{{tree}}")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
            worker_ledger=worker_ledger,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_refuses_added_then_deleted_entry(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-TEST",
    )
    removed = (
        repository
        / "design"
        / "contract_compiler"
        / "workstreams"
        / "CC-TEST"
        / "ledger"
        / "entries"
        / "CC-TEST-WRK-000002.json"
    )
    _write_json(removed, {"entry_id": "CC-TEST-WRK-000002"})
    _commit(repository, "add unvalidated worker-ledger entry")
    removed.unlink()
    head = _commit(repository, "delete unvalidated worker-ledger entry")
    candidate["head_commit"] = head
    candidate["head_tree"] = _git(repository, "rev-parse", f"{head}^{{tree}}")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
            worker_ledger=worker_ledger,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_refuses_changed_prefix_entry(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-TEST",
    )
    entry_path = (
        repository
        / "design"
        / "contract_compiler"
        / "workstreams"
        / "CC-TEST"
        / "ledger"
        / "entries"
        / "CC-TEST-WRK-000001.json"
    )
    entry = _read_json(entry_path)
    entry["summary"] = "Rewrite immutable RED."
    entry["entry_hash"] = integration_module.worker_entry_hash(entry)
    _write_json(entry_path, entry)
    head = _commit(repository, "rewrite candidate worker-ledger entry")
    candidate["head_commit"] = head
    candidate["head_tree"] = _git(repository, "rev-parse", f"{head}^{{tree}}")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
            worker_ledger=worker_ledger,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_candidate_worker_ledger_sideband_refuses_changed_then_restored_entry(
    tmp_path: Path,
) -> None:
    repository, candidate, authority = _clean_base_candidate(tmp_path)
    candidate, worker_ledger = _add_candidate_worker_ledger(
        repository,
        candidate,
        "CC-TEST",
    )
    relative = (
        "design/contract_compiler/workstreams/CC-TEST/ledger/entries/"
        "CC-TEST-WRK-000001.json"
    )
    entry_path = repository / relative
    entry = _read_json(entry_path)
    entry["summary"] = "Temporarily rewrite immutable RED."
    entry["entry_hash"] = integration_module.worker_entry_hash(entry)
    _write_json(entry_path, entry)
    _commit(repository, "rewrite candidate worker-ledger entry")
    _write_json(
        entry_path,
        json.loads(worker_ledger.entry_sources[relative].decode("utf-8")),
    )
    head = _commit(repository, "restore candidate worker-ledger entry")
    candidate["head_commit"] = head
    candidate["head_tree"] = _git(repository, "rev-parse", f"{head}^{{tree}}")

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
            worker_ledger=worker_ledger,
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")


def test_clean_base_refuses_undeclared_candidate_helper(tmp_path: Path) -> None:
    repository, candidate, authority = _clean_base_candidate(
        tmp_path,
        candidate_helper=True,
    )

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository,
            candidate,
            allowed_scopes=ALLOWED_SCOPES,
            workstream_id="CC-TEST",
            authority_entry=authority,
            overseer_path="governance",
            enforce_clean_base=True,
        )

    _assert_code(error, "CC000_CANDIDATE_DECLARATION")


def test_exact_prefix_240_candidates_are_the_only_legacy_set() -> None:
    cards, card_paths = _current_candidate_cards()

    legacy = integration_module._frozen_legacy_candidate_ids(
        ROOT,
        cards,
        card_paths,
        _raw_overseer_state(),
        "design/contract_compiler/overseer",
    )

    assert len(legacy) == 15
    assert legacy == {
        workstream_id
        for workstream_id, card in cards.items()
        if card["candidate"]["state"] in {"ELIGIBLE", "INTEGRATED"}
        and workstream_id not in {"CC-012", "CC-014", "CC-016"}
    }


@pytest.mark.parametrize(
    "state",
    ("NONE", "QUARANTINED", "ALTERNATE"),
)
def test_frozen_completed_candidate_continuity_refuses_replacement(
    state: str,
) -> None:
    cards, card_paths = _current_candidate_cards()
    candidate = copy.deepcopy(cards["CC-X03"]["candidate"])
    if state == "NONE":
        candidate = {"state": "NONE"}
    elif state == "QUARANTINED":
        candidate = {
            "base_commit": candidate["base_commit"],
            "head_commit": candidate["head_commit"],
            "limitations": ["Historical candidate was demoted."],
            "observed_touched_paths": [
                item["path"] for item in candidate["artifacts"] + candidate["evidence"]
            ],
            "reason": "Historical candidate was demoted.",
            "state": "QUARANTINED",
        }
    else:
        candidate["base_commit"] = _git(
            ROOT, "rev-parse", f"{candidate['base_commit']}^"
        )
    cards["CC-X03"]["candidate"] = candidate

    with pytest.raises(IntegrationValidationError) as error:
        integration_module._frozen_legacy_candidate_ids(
            ROOT,
            cards,
            card_paths,
            _raw_overseer_state(),
            "design/contract_compiler/overseer",
        )

    _assert_code(error, "CC000_CANDIDATE_LEGACY")


def test_frozen_completed_candidate_refuses_historical_card_relocation() -> None:
    cards, card_paths = _current_candidate_cards()
    card_paths["CC-X03"] = "workstreams/relocated-CC-X03.json"

    with pytest.raises(IntegrationValidationError) as error:
        integration_module._frozen_legacy_candidate_ids(
            ROOT,
            cards,
            card_paths,
            _raw_overseer_state(),
            "design/contract_compiler/overseer",
        )

    _assert_code(error, "CC000_CANDIDATE_LEGACY")


def test_frozen_candidate_ignores_git_replacement_path_relocation(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "replacement"
    subprocess.run(
        ["git", "clone", "--shared", str(ROOT), str(repository)],
        check=True,
        capture_output=True,
        text=True,
    )
    _git(repository, "checkout", QUIET_BELL_AUTHORITY_HARDENING_COMMIT)
    manifest_path = repository / "design/contract_compiler/integration.json"
    manifest = _read_json(manifest_path)
    row = _registry_row(manifest, "CC-X03")
    original = manifest_path.parent / row["card"]["path"]
    relocated = "workstreams/relocated-CC-X03/manifest.json"
    destination = manifest_path.parent / relocated
    destination.parent.mkdir(parents=True)
    shutil.copy2(original, destination)
    original.unlink()
    row["card"]["path"] = relocated
    _write_json(manifest_path, manifest)
    _git(repository, "add", "-A")
    replacement_tree = _git(repository, "write-tree")
    replacement_commit = _git(
        repository,
        "commit-tree",
        replacement_tree,
        "-p",
        f"{QUIET_BELL_AUTHORITY_HARDENING_COMMIT}^",
        "-m",
        "replacement overlay",
    )
    _git(
        repository,
        "replace",
        QUIET_BELL_AUTHORITY_HARDENING_COMMIT,
        replacement_commit,
    )
    cards, card_paths = _current_candidate_cards()
    card_paths["CC-X03"] = relocated

    with pytest.raises(IntegrationValidationError) as error:
        integration_module._frozen_legacy_candidate_ids(
            repository,
            cards,
            card_paths,
            _raw_overseer_state(),
            "design/contract_compiler/overseer",
        )

    _assert_code(error, "CC000_CANDIDATE_LEGACY")


def test_candidate_git_commands_ignore_legacy_grafts(tmp_path: Path) -> None:
    repository = tmp_path / "graft"
    subprocess.run(
        ["git", "clone", "--shared", str(ROOT), str(repository)],
        check=True,
        capture_output=True,
        text=True,
    )
    grafts = repository / ".git/info/grafts"
    grafts.write_text(QUIET_BELL_AUTHORITY_HARDENING_COMMIT + "\n", encoding="utf-8")

    result = integration_module._git(
        repository,
        "rev-list",
        "--parents",
        "-n",
        "1",
        QUIET_BELL_AUTHORITY_HARDENING_COMMIT,
    )

    assert result.returncode == 0
    assert len(result.stdout.split()) == 2


@pytest.mark.parametrize("integrated", (False, True), ids=("unchanged", "integrated"))
def test_frozen_completed_candidate_allows_only_state_progression(
    integrated: bool,
) -> None:
    cards, card_paths = _current_candidate_cards()
    if integrated:
        cards["CC-X03"]["candidate"]["state"] = "INTEGRATED"

    legacy = integration_module._frozen_legacy_candidate_ids(
        ROOT,
        cards,
        card_paths,
        _raw_overseer_state(),
        "design/contract_compiler/overseer",
    )

    assert "CC-X03" in legacy


def test_later_completion_coordinate_uses_strict_candidate_admission() -> None:
    cards, card_paths = _current_candidate_cards()
    cards["CC-X03"]["candidate"]["base_commit"] = _git(
        ROOT,
        "rev-parse",
        f"{cards['CC-X03']['candidate']['base_commit']}^",
    )
    ledger = _raw_overseer_state()
    later_entries = ledger.entries + (
        {
            "data": {
                "new_state": "ACTIVE",
                "workstream_id": "CC-X03",
            },
            "entry_hash": "sha256:" + "1" * 64,
            "entry_id": "OVR-TEST-X03-REACTIVE",
            "entry_type": "WORKSTREAM_STATE",
            "sequence": 1001,
        },
        {
            "data": {
                "new_state": "COMPLETE",
                "workstream_id": "CC-X03",
            },
            "entry_hash": "sha256:" + "2" * 64,
            "entry_id": "OVR-TEST-X03-RECOMPLETE",
            "entry_type": "WORKSTREAM_STATE",
            "sequence": 1002,
        },
    )

    legacy = integration_module._frozen_legacy_candidate_ids(
        ROOT,
        cards,
        card_paths,
        SimpleNamespace(entries=later_entries),
        "design/contract_compiler/overseer",
    )

    assert "CC-X03" not in legacy


@pytest.mark.parametrize(
    ("workstream_id", "base_commit"),
    (
        ("CC-000", "c410f11229e7c33a4fab9ebdfc9e2e109f18cbf7^"),
        ("CC-021", SMALL_SHOP_PROVISIONAL_COMMIT),
    ),
    ids=("broadened-bootstrap", "provisional-cc021"),
)
def test_legacy_candidate_identity_cannot_be_rebound(
    workstream_id: str,
    base_commit: str,
) -> None:
    cards, card_paths = _current_candidate_cards()
    rebound = copy.deepcopy(cards[workstream_id])
    rebound["candidate"]["base_commit"] = _git(ROOT, "rev-parse", base_commit)
    cards[workstream_id] = rebound
    ledger = _raw_overseer_state()

    with pytest.raises(IntegrationValidationError) as error:
        integration_module._frozen_legacy_candidate_ids(
            ROOT,
            cards,
            card_paths,
            ledger,
            "design/contract_compiler/overseer",
        )

    _assert_code(error, "CC000_CANDIDATE_LEGACY")


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
        lambda _bundle, card, _schema, _prefix: (
            integration_module.WorkerLedgerValidation(
                workstream_id=card["workstream_id"],
                phase_results=tuple(
                    {
                        "phase": phase,
                        "result": (
                            "EXPECTED_FAILURE" if phase == "RED" else "PASS"
                        ),
                    }
                    for phase in integration_module.TDD_PHASES
                ),
                head_path=None,
                head_static={},
                entry_sources={},
                entry_hashes=(),
            )
        ),
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
    cc021_digest = _registry_row(manifest, "CC-021")["card"]["sha256"]

    def rebind_small_shop_oracle(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-D11"]["card_sha256"] = d11_digest
        bindings["CC-021"]["card_sha256"] = cc021_digest

    _rewrite_card(manifest_path, manifest, "CC-022", rebind_small_shop_oracle)
    cc011_digest = _registry_row(manifest, "CC-011")["card"]["sha256"]
    cc015_digest = _registry_row(manifest, "CC-015")["card"]["sha256"]
    cc022_digest = _registry_row(manifest, "CC-022")["card"]["sha256"]

    def rebind_greenhouse_oracle(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-015"]["card_sha256"] = cc015_digest
        bindings["CC-021"]["card_sha256"] = cc021_digest
        bindings["CC-022"]["card_sha256"] = cc022_digest

    _rewrite_card(manifest_path, manifest, "CC-016", rebind_greenhouse_oracle)

    def rebind_quiet_bell_oracle(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-011"]["card_sha256"] = cc011_digest
        bindings["CC-021"]["card_sha256"] = cc021_digest
        bindings["CC-022"]["card_sha256"] = cc022_digest

    _rewrite_card(manifest_path, manifest, "CC-012", rebind_quiet_bell_oracle)

    cc013_digest = _registry_row(manifest, "CC-013")["card"]["sha256"]

    def rebind_feature_oracle(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        bindings["CC-010"]["card_sha256"] = cc010_digest
        bindings["CC-013"]["card_sha256"] = cc013_digest
        bindings["CC-021"]["card_sha256"] = cc021_digest
        bindings["CC-022"]["card_sha256"] = cc022_digest

    _rewrite_card(manifest_path, manifest, "CC-014", rebind_feature_oracle)
    changed_dependency_digests = {
        workstream_id: _registry_row(manifest, workstream_id)["card"]["sha256"]
        for workstream_id in (
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
    }

    def rebind_retained_source(card: dict[str, Any]) -> None:
        bindings = {
            binding["workstream_id"]: binding
            for binding in card["authorization"]["dependency_bindings"]
        }
        for workstream_id, digest in changed_dependency_digests.items():
            bindings[workstream_id]["card_sha256"] = digest
        bindings["CC-X03"]["integrated_head"] = result_commit

    _rewrite_card(manifest_path, manifest, "CC-R01", rebind_retained_source)
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


def test_feature_oracle_reactivation_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-014")
    card = _read_json(CONTRACT / row["card"]["path"])

    assert card["authorization"]["class"] == "FORMAL"
    assert [
        binding["workstream_id"]
        for binding in card["authorization"]["dependency_bindings"]
    ] == list(row["depends_on"])
    assert card["assignment"] == {
        "owner_id": "worker:cc014-feature-oracles",
        "state": "ASSIGNED",
        "task_id": "/root/cc014_feature_oracles",
    }

    responsibility = card["responsibility"]
    for exact in (
        "Split the mixed explicit-false boundary into separate accepted and refused results.",
        'minimal {"outcome":"REFUSE"}',
        "SAME, DIFFERENT, and NOT_CLAIMED",
        "explicitly experimental and fixture-local",
        "never compiler input",
    ):
        assert exact in responsibility

    transaction = tuple(
        entry
        for entry in _raw_overseer_state().entries
        if 280 <= entry["sequence"] <= 282
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000280",
        "OVR-000281",
        "OVR-000282",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, activated = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-014"]
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert activated["data"]["previous_state"] == "PAUSED"
    assert activated["data"]["new_state"] == "ACTIVE"
    assert activated["data"]["blockers"] == []
    assert activated["data"]["evidence_entry_ids"] == [
        "OVR-000280",
        "OVR-000281",
    ]
    assert activated["previous_entry_hash"] == verification["entry_hash"]

    report = _read_json(CONTRACT / "overseer/evidence/CC-014-reactivation.json")
    assert report["workstream_id"] == "CC-014"
    assert report["base_commit"] == "6bc61c7458469f9f70555d651c65d2736b723318"
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("test-only" in limitation for limitation in report["limitations"])


def test_feature_oracle_completion_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-014")
    card = _read_json(CONTRACT / row["card"]["path"])
    ledger_state = _raw_overseer_state()
    states, _ = integration_module._workstream_states(ledger_state)

    assert states["CC-012"] == states["CC-016"] == "COMPLETE"
    assert states["CC-014"] == "COMPLETE"
    assert card["candidate"] == {
        "artifacts": [
            {
                "byte_length": 18972,
                "path": (
                    "conformance/contract_kernel/v0/feature_cases/oracle/"
                    "feature_cases.json"
                ),
                "sha256": (
                    "sha256:83e48b5581acd9b23f42229c707a92f3a3bcb4f5f795ae147c2bbbd"
                    "428017068"
                ),
            },
            {
                "byte_length": 23720,
                "path": "tests/contract_compiler/test_feature_case_oracles.py",
                "sha256": (
                    "sha256:4f217511d88b43cb8d50edc344bda8a99e4567bafb28f7e02f4fa3"
                    "49ebc9313c"
                ),
            },
        ],
        "base_commit": "607706796bf157f10d2a911a57cff39a72876795",
        "evidence": [
            {
                "byte_length": 7861,
                "path": "conformance/contract_compiler/v0/evidence/CC-014.json",
                "result": "PASS",
                "sha256": (
                    "sha256:74fc1b37886770a8d34a541a3dc6f37e1e0d72710c1dd9bf6b5a3e"
                    "a3d6aeb7e9"
                ),
            }
        ],
        "head_commit": "81b987b071dcce38a0d09eaddff9b6bfbf6ca5eb",
        "head_tree": "af33fc96eba5924912c9c4c3c6e6a5be36a2066e",
        "state": "ELIGIBLE",
    }
    assert card["ledger"] == {
        "entry_count": 7,
        "head_entry_id": "CC-014-WRK-000007",
        "head_hash": (
            "sha256:ad67b5c4835874fc15f7523d040bcedf48e575e01b5f9f906499b72cf6302285"
        ),
        "path": "workstreams/CC-014/ledger",
        "state": "RECORDED",
    }
    authorities = integration_module._latest_active_authority_entries(ledger_state)
    worker_ledger = integration_module._validate_worker_ledger(
        CONTRACT,
        card,
        _read_json(CONTRACT / "integration.schema.json"),
        integration_module.PurePosixPath("design/contract_compiler"),
    )
    touched = validate_candidate_history(
        ROOT,
        card["candidate"],
        allowed_scopes=card["scopes"],
        workstream_id="CC-014",
        authority_entry=authorities["CC-014"],
        overseer_path="design/contract_compiler/overseer",
        enforce_clean_base=True,
        worker_ledger=worker_ledger,
    )
    assert touched == (
        "conformance/contract_compiler/v0/evidence/CC-014.json",
        "conformance/contract_kernel/v0/feature_cases/oracle/feature_cases.json",
        "design/contract_compiler/workstreams/CC-014/ledger/entries/"
        "CC-014-WRK-000001.json",
        "design/contract_compiler/workstreams/CC-014/ledger/entries/"
        "CC-014-WRK-000002.json",
        "design/contract_compiler/workstreams/CC-014/ledger/head.json",
        "tests/contract_compiler/test_feature_case_oracles.py",
    )

    oracle = _read_json(
        ROOT
        / "conformance/contract_kernel/v0/feature_cases/oracle/feature_cases.json"
    )
    assert len(oracle["groups"]) == 11
    assert len(oracle["outcomes"]) == 18
    assert sum(outcome == "ACCEPT" for outcome in oracle["outcomes"].values()) == 13
    assert sum(
        outcome == {"outcome": "REFUSE"}
        for outcome in oracle["outcomes"].values()
    ) == 5
    assert len(oracle["projections"]) == 13
    assert len(oracle["relations"]) == 4
    assert oracle["outcomes"]["positive/valid_explicit_false.json"] == "ACCEPT"
    assert oracle["outcomes"]["x01/explicit_false.json"] == {
        "outcome": "REFUSE"
    }

    completion = tuple(
        entry
        for entry in ledger_state.entries
        if 283 <= entry["sequence"] <= 285
    )
    assert tuple(entry["entry_id"] for entry in completion) == (
        "OVR-000283",
        "OVR-000284",
        "OVR-000285",
    )
    assert tuple(entry["entry_type"] for entry in completion) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, completed = completion
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-014"]
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert completed["data"]["previous_state"] == "ACTIVE"
    assert completed["data"]["new_state"] == "COMPLETE"
    assert completed["data"]["blockers"] == []
    assert completed["data"]["evidence_entry_ids"] == ["OVR-000284"]
    assert completed["data"]["deliverables"] == [
        (
            "Hand-author the private feature-case compilation and refusal answer "
            "key only from exact feature sources and accepted decisions."
        ),
        (
            "Bind the exact 6077067..81b987b eligible candidate, canonical report, "
            "seven worker TDD phases, and both clean final audits."
        ),
        (
            "Keep the candidate unselected and non-public and transfer only process "
            "technique into separately activated compiler implementation."
        ),
    ]
    assert completed["previous_entry_hash"] == verification["entry_hash"]

    report = _read_json(CONTRACT / "overseer/evidence/CC-014-completion.json")
    assert report["workstream_id"] == "CC-014"
    assert report["base_commit"] == "81b987b071dcce38a0d09eaddff9b6bfbf6ca5eb"
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert any("tripwire" in limitation for limitation in report["limitations"])
    chronology = [
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
        for value in (
            report["recorded_at"],
            revision["recorded_at"],
            verification["recorded_at"],
            completed["recorded_at"],
        )
    ]
    assert all(later > earlier for earlier, later in zip(chronology, chronology[1:]))
    assert "CC-014" not in manifest["selections"]
    completion_manifest = json.loads(
        _git(
            ROOT,
            "show",
            "3afca71f59c563eb559109ca4007a68e02fbf0ba:"
            "design/contract_compiler/integration.json",
        )
    )
    completion_r01 = json.loads(
        _git(
            ROOT,
            "show",
            "3afca71f59c563eb559109ca4007a68e02fbf0ba:"
            "design/contract_compiler/"
            f"{_registry_row(completion_manifest, 'CC-R01')['card']['path']}",
        )
    )
    assert completion_r01["authorization"]["class"] == "BLOCKED"


def test_retained_source_boundary_activation_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-R01")
    card_path = CONTRACT / row["card"]["path"]
    card_source = card_path.read_bytes()
    card = _read_json(card_path)
    ledger_state = _raw_overseer_state()
    states, _ = integration_module._workstream_states(ledger_state)

    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-R01/manifest.json",
        "sha256": _digest(card_source),
        "state": "PRESENT",
    }
    assert card["assignment"] == {
        "owner_id": "worker:ccr01-retained-source-boundary",
        "state": "ASSIGNED",
        "task_id": "/root/ccr01_retained_source_boundary",
    }
    assert card["authorization"]["authorized_by"] == {
        "id": "operator",
        "type": "OPERATOR",
    }
    assert card["authorization"]["class"] == "FORMAL"
    assert tuple(
        binding["workstream_id"]
        for binding in card["authorization"]["dependency_bindings"]
    ) == tuple(row["depends_on"])
    assert card["scopes"] == [
        {"kind": "FILE", "path": "src/malleus/_contract_source.py"},
        {
            "kind": "FILE",
            "path": "tests/contract_compiler/test_retained_source_boundary.py",
        },
        {
            "kind": "FILE",
            "path": "conformance/contract_compiler/v0/evidence/CC-R01.json",
        },
    ]
    assert "syntax-neutral" in card["responsibility"]
    assert "same resolver" in card["responsibility"]
    assert "complete immutable closure" in card["responsibility"]
    assert "without a partial result" in card["responsibility"]
    transaction = tuple(
        entry
        for entry in ledger_state.entries
        if 286 <= entry["sequence"] <= 288
    )
    assert tuple(entry["entry_id"] for entry in transaction) == (
        "OVR-000286",
        "OVR-000287",
        "OVR-000288",
    )
    assert tuple(entry["entry_type"] for entry in transaction) == (
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    revision, verification, activation = transaction
    assert revision["data"]["affected_ids"] == ["CC-000", "CC-R01"]
    assert {
        document["path"]: document["change"]
        for document in revision["data"]["documents"]
    } == {
        "design/contract_compiler/integration.json": "MODIFIED",
        "design/contract_compiler/overseer/evidence/CC-R01-activation.json": "CREATED",
        "design/contract_compiler/workstreams/CC-R01/manifest.json": "MODIFIED",
        "tests/test_contract_compiler_integration.py": "MODIFIED",
    }
    assert all(
        not document["path"].startswith("src/malleus/")
        and "test_retained_source_boundary.py" not in document["path"]
        and document["path"]
        != "conformance/contract_compiler/v0/evidence/CC-R01.json"
        for document in revision["data"]["documents"]
    )
    assert verification["actor"] == {
        "id": "ccr01-activation-verifier",
        "type": "MECHANICAL",
    }
    assert verification["data"]["as_of"] == verification["recorded_at"]
    assert activation["data"] == {
        "blockers": [],
        "bootstrap": True,
        "deliverables": [
            (
                "Write fixed tests before implementation for exact retention, "
                "recursive imports, diamonds, identity countercases, cycles, typed "
                "refusal, no fallback, and no hidden I/O."
            ),
            (
                "Implement one syntax-neutral closure executor driven only by one "
                "injected resolver and one injected ordered import reader."
            ),
            (
                "Return a complete immutable closure or refuse atomically; create no "
                "LinkML adapter, compiler facts, public API, package, selection, "
                "runtime protocol, ledger, graph, or fixture-specific policy."
            ),
        ],
        "evidence_entry_ids": ["OVR-000286", "OVR-000287"],
        "new_state": "ACTIVE",
        "previous_state": "PLANNED",
        "workstream_id": "CC-R01",
    }

    report = _read_json(CONTRACT / "overseer/evidence/CC-R01-activation.json")
    assert report["base_commit"] == "3afca71f59c563eb559109ca4007a68e02fbf0ba"
    assert report["workstream_id"] == "CC-R01"
    assert all(check["result"] == "PASS" for check in report["checks"])
    chronology = [
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
        for value in (
            report["recorded_at"],
            revision["recorded_at"],
            verification["recorded_at"],
            activation["recorded_at"],
        )
    ]
    assert all(later > earlier for earlier, later in zip(chronology, chronology[1:]))


def test_retained_source_boundary_completion_is_exact() -> None:
    manifest = _read_json(INTEGRATION)
    row = _registry_row(manifest, "CC-R01")
    card = _read_json(CONTRACT / row["card"]["path"])
    ledger_state = _raw_overseer_state()
    states, _ = integration_module._workstream_states(ledger_state)

    assert states["CC-R01"] == "COMPLETE"
    assert card["candidate"] == {
        "artifacts": [
            {
                "byte_length": 12588,
                "path": "src/malleus/_contract_source.py",
                "sha256": (
                    "sha256:dd8861dedbd26c2aa33600865683563fb732a6d3c749f2817905824"
                    "e0bc717d2"
                ),
            },
            {
                "byte_length": 33946,
                "path": "tests/contract_compiler/test_retained_source_boundary.py",
                "sha256": (
                    "sha256:9f69ae6b4f57823e92e924704534cdd0644078085a2cf2460acddc4"
                    "5a04ab8b8"
                ),
            },
        ],
        "base_commit": "dbc5eaee8493275b3d0c468b77f5567711507cd8",
        "evidence": [
            {
                "byte_length": 9474,
                "path": "conformance/contract_compiler/v0/evidence/CC-R01.json",
                "result": "PASS",
                "sha256": (
                    "sha256:67b39a464e8a73e98ab6b2929cc9ea230f9f5c9a149751eb1d6d9"
                    "bff48cb3b20"
                ),
            }
        ],
        "head_commit": "89645c1ca314fa58ba03e711cbbb29de94cfc007",
        "head_tree": "e5b198568fea8522e0a894458b4d98fb11b9f95e",
        "state": "ELIGIBLE",
    }
    assert card["ledger"] == {
        "entry_count": 20,
        "head_entry_id": "CC-R01-WRK-000020",
        "head_hash": (
            "sha256:5ee62ba931c7a03e1cb15f889fedc74ce8af899b60b28f1a25431a"
            "312bccb64e"
        ),
        "path": "workstreams/CC-R01/ledger",
        "state": "RECORDED",
    }
    worker_entries = [
        _read_json(path)
        for path in sorted((CONTRACT / "workstreams/CC-R01/ledger/entries").glob("*.json"))
    ]
    assert len(worker_entries) == 20
    assert any(
        entry["data"]["phase"] == "PACKAGE"
        and entry["data"]["result"] == "NOT_APPLICABLE"
        for entry in worker_entries
    )

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["tool"]["hatch"]["build"]["targets"]["wheel"]["exclude"] == [
        "/src/malleus/_contract_compiler.py",
        "/src/malleus/_contract_compiler_profile.json",
        "/src/malleus/_contract_source.py",
    ]
    assert "/src/malleus/_contract_source.py" in project["tool"]["hatch"]["build"][
        "include"
    ]

    corpus = _read_json(ROOT / "conformance/contract_kernel/v0/corpus.json")
    assert [corpus["cases"][0]["case_id"] for corpus in corpus["corpora"]] == [
        "quiet-bell-archive",
        "feature-isolation-suite",
        "neutral-greenhouse",
    ]
    checksums = _read_json(ROOT / "conformance/contract_kernel/v0/checksums.json")
    assert len(checksums["files"]) == 37

    completion = tuple(
        entry for entry in ledger_state.entries if 289 <= entry["sequence"] <= 292
    )
    assert tuple(entry["entry_id"] for entry in completion) == (
        "OVR-000289",
        "OVR-000290",
        "OVR-000291",
        "OVR-000292",
    )
    assert tuple(entry["entry_type"] for entry in completion) == (
        "DOCUMENT_REVISION",
        "DOCUMENT_REVISION",
        "VERIFIED_FACT",
        "WORKSTREAM_STATE",
    )
    candidate_revision, completion_revision, verification, completed = completion
    assert len(candidate_revision["data"]["documents"]) == 20
    assert len(completion_revision["data"]["documents"]) == 15
    assert completed["data"]["previous_state"] == "ACTIVE"
    assert completed["data"]["new_state"] == "COMPLETE"
    assert completed["data"]["blockers"] == []
    assert completed["data"]["evidence_entry_ids"] == ["OVR-000291"]

    report = _read_json(CONTRACT / "overseer/evidence/CC-R01-completion.json")
    assert report["workstream_id"] == "CC-R01"
    assert report["base_commit"] == "89645c1ca314fa58ba03e711cbbb29de94cfc007"
    assert all(check["result"] == "PASS" for check in report["checks"])
    chronology = [
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
        for value in (
            report["recorded_at"],
            candidate_revision["recorded_at"],
            completion_revision["recorded_at"],
            verification["recorded_at"],
            completed["recorded_at"],
        )
    ]
    assert all(later > earlier for earlier, later in zip(chronology, chronology[1:]))
    assert "CC-R01" not in manifest["selections"]

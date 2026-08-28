from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.contract_compiler_integration import (  # noqa: E402
    IntegrationValidationError,
    load_program_registry,
    validate_candidate_history,
    validate_integration,
)
from scripts.contract_compiler_ledger import load_ledger as load_overseer_ledger  # noqa: E402
import scripts.contract_compiler_integration as integration_module  # noqa: E402


CONTRACT = ROOT / "design" / "contract_compiler"
INTEGRATION = CONTRACT / "integration.json"
PROGRAM = CONTRACT / "program.md"


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ) + "\n"


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
        row
        for row in manifest["workstreams"]
        if row["workstream_id"] == workstream_id
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
    template = _read_json(
        _card_path(manifest_path, _registry_row(manifest, "CC-R01"))
    )
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
    path.parent.mkdir(parents=True)
    source = _canonical_json(template).encode("utf-8")
    path.write_bytes(source)
    _registry_row(manifest, workstream_id)["card"] = {
        "state": "PRESENT",
        "path": relative,
        "byte_length": len(source),
        "sha256": _digest(source),
    }
    _write_json(manifest_path, manifest)


def _assert_code(error: pytest.ExceptionInfo[IntegrationValidationError], code: str) -> None:
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


def test_program_registry_contains_the_exact_approved_66_workstreams() -> None:
    registry = load_program_registry(PROGRAM)

    assert len(registry) == 66
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
    )
    assert registry["CC-P52"] == ("CC-P45", "CC-P51", "CC-PUB01")


def test_canonical_integration_manifest_is_valid() -> None:
    state = validate_integration(ROOT)
    x03 = state.cards["CC-X03"]
    ledger = load_overseer_ledger(CONTRACT / "overseer", repository=ROOT)
    workstream_states, _ = integration_module._workstream_states(ledger)

    assert len(state.workstreams) == 66
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
        "CC-D08": ("CC-D02", "CC-D03", "CC-D05"),
        "CC-D11": ("CC-X03",),
        "CC-D13": ("CC-D01",),
        "CC-D14": (),
    }
    assert len(state.cards) == 20
    for workstream_id, dependencies in decisions.items():
        card = state.cards[workstream_id]
        assert card["assignment"] == {
            "owner_id": "overseer",
            "state": "ASSIGNED",
            "task_id": "/root",
        }
        assert card["authorization"]["class"] == "FORMAL"
        assert tuple(
            binding["workstream_id"]
            for binding in card["authorization"]["dependency_bindings"]
        ) == dependencies
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


def test_registry_card_pointer_must_match_its_workstream_row(tmp_path: Path) -> None:
    path, manifest = _copy_manifest_bundle(tmp_path)
    _registry_row(manifest, "CC-D07")["card"] = copy.deepcopy(
        _registry_row(manifest, "CC-D08")["card"]
    )
    _write_json(path, manifest)

    with pytest.raises(IntegrationValidationError) as error:
        validate_integration(ROOT, path)

    _assert_code(error, "CC000_CARD_ID")


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
    assert f"validated 66 workstreams, {present_cards} cards," in result.stdout


@pytest.mark.parametrize("workflow", ["tests.yml", "release.yml"])
def test_integration_ci_has_full_history_and_no_duplicate_yaml_keys(
    workflow: str,
) -> None:
    value = yaml.load(
        (ROOT / ".github" / "workflows" / workflow).read_text(encoding="utf-8"),
        Loader=_UniqueYamlLoader,
    )
    jobs = value["jobs"]
    guarded = [
        job
        for job in jobs.values()
        if any(
            step.get("name") == "Validate contract compiler integration gate"
            for step in job["steps"]
        )
    ]

    assert guarded
    for job in guarded:
        checkout = next(
            step for step in job["steps"] if step.get("uses") == "actions/checkout@v4"
        )
        assert checkout["with"]["fetch-depth"] == 0


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
    assert "CC-010" in str(error.value)
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
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_GIT_COMMIT_ID")


def test_candidate_commit_must_resolve(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["head_commit"] = "f" * 40

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_GIT_OBJECT_MISSING")


def test_candidate_head_must_descend_from_base(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    tree = _git(repository, "rev-parse", f"{head}^{{tree}}")
    orphan = _git(repository, "commit-tree", tree, "-m", "unrelated")
    candidate["head_commit"] = orphan
    candidate["head_tree"] = tree

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

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
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_SCOPE_VIOLATION")
    assert all(relative in str(error.value) for relative in themed)


def test_candidate_head_tree_is_bound_exactly(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["head_tree"] = base

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_CANDIDATE_TREE")


def test_candidate_artifact_digest_is_verified_at_head(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["artifacts"][0]["sha256"] = "sha256:" + "0" * 64

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_ARTIFACT_DIGEST")


def test_failed_evidence_cannot_gate_candidate(tmp_path: Path) -> None:
    repository, base, head = _candidate_repository(tmp_path)
    candidate = _candidate(repository, base, head)
    candidate["evidence"][0]["result"] = "FAIL"

    with pytest.raises(IntegrationValidationError) as error:
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

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
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_EVIDENCE_INVALID")


def test_selected_workstream_must_be_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _copy_manifest_bundle(tmp_path)
    for row in manifest["workstreams"]:
        if row["workstream_id"] != "CC-000":
            row["card"] = {"state": "ABSENT"}
    result_commit = "55d9da3b58d77d49bdcf449c376a26231d410824"
    result_report = _git(ROOT, "show", f"{result_commit}:design/contract_compiler/workstreams/CC-000/evidence/result.json")
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
    monkeypatch.setattr(integration_module, "load_ledger", lambda *args, **kwargs: active_prefix)
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
        validate_candidate_history(
            repository, candidate, allowed_scopes=ALLOWED_SCOPES
        )

    _assert_code(error, "CC000_CANDIDATE_STATE")

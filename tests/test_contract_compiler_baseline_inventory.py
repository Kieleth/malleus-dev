from __future__ import annotations

import copy
import http.client
import json
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "compiler_baseline_candidates.json"
)
EVIDENCE = (
    ROOT / "conformance" / "contract_compiler" / "v0" / "evidence" / "CC-X00.json"
)
SCRIPT = ROOT / "scripts" / "contract_compiler_baseline_inventory.py"
sys.path.insert(0, str(ROOT))

import scripts.contract_compiler_baseline_inventory as baseline_inventory  # noqa: E402
from scripts.contract_compiler_baseline_inventory import (  # noqa: E402
    InventoryError,
    inventory_identity,
    load_inventory,
    main,
    normalize_inventory,
    validate_inventory,
)
from scripts.contract_compiler_ledger import verify_evidence_snapshot  # noqa: E402


def _inventory() -> dict:
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def _candidate(data: dict, kind: str) -> dict:
    return next(
        candidate for candidate in data["candidates"] if candidate["kind"] == kind
    )


def _write(tmp_path: Path, value: dict) -> Path:
    path = tmp_path / "inventory.json"
    path.write_text(json.dumps(value, allow_nan=False), encoding="utf-8")
    return path


def _assert_invalid(value: dict, needle: str | None = None) -> None:
    with pytest.raises(InventoryError) as caught:
        validate_inventory(value)
    if needle is not None:
        assert needle in str(caught.value)


def _reseal_and_assert_invalid(
    monkeypatch: pytest.MonkeyPatch, value: dict, needle: str | None = None
) -> None:
    monkeypatch.setattr(
        baseline_inventory, "AUDITED_IDENTITY", baseline_inventory._identity(value)
    )
    _assert_invalid(value, needle)


def test_checked_inventory_is_valid_and_has_exactly_two_unordered_candidates() -> None:
    data = load_inventory(INVENTORY)

    assert data["schema"] == "malleus.contract-compiler.baseline-candidates/v1"
    assert data["decision_id"] == "OD-012"
    assert data["scope"] == "RESEARCH_INVENTORY"
    assert data["authority"] == {
        "decision_authority": "NONE",
        "production_artifact_authority": "NONE",
    }
    assert {candidate["kind"] for candidate in data["candidates"]} == {
        "RELEASE",
        "SOURCE_COMMIT",
    }
    assert len(data["candidates"]) == 2


def test_release_candidate_records_exact_release_and_published_artifacts() -> None:
    release = _candidate(_inventory(), "RELEASE")
    artifacts = {
        (distribution["name"], artifact["kind"]): artifact
        for distribution in release["distributions"]
        for artifact in distribution["artifacts"]
    }

    assert release["source"]["tag"] == "v1.11.1"
    assert release["source"]["commit"] == "a7ed3e4cbb19731f072d0d90b6d52f7d822569ee"
    assert {
        key: (artifact["filename"], artifact["sha256"], artifact["byte_length"])
        for key, artifact in artifacts.items()
    } == {
        ("linkml", "WHEEL"): (
            "linkml-1.11.1-py3-none-any.whl",
            "d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed",
            483751,
        ),
        ("linkml", "SDIST"): (
            "linkml-1.11.1.tar.gz",
            "2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524",
            374853,
        ),
        ("linkml-runtime", "WHEEL"): (
            "linkml_runtime-1.11.1-py3-none-any.whl",
            "b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da",
            654566,
        ),
        ("linkml-runtime", "SDIST"): (
            "linkml_runtime-1.11.1.tar.gz",
            "e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754",
            556549,
        ),
    }
    assert {artifact["provision"] for artifact in artifacts.values()} == {"PUBLISHED"}


def test_release_metadata_and_provenance_bind_both_distributions() -> None:
    release = _candidate(_inventory(), "RELEASE")

    assert {distribution["name"] for distribution in release["distributions"]} == {
        "linkml",
        "linkml-runtime",
    }
    for distribution in release["distributions"]:
        assert distribution["version"] == "1.11.1"
        assert distribution["requires_python"] == ">=3.10"
        assert distribution["advertised_python_minors"] == [
            "3.10",
            "3.11",
            "3.12",
            "3.13",
        ]
        assert distribution["provenance"]["state"] == "PYPI_ATTESTED"
        assert distribution["provenance"]["commit"] == release["source"]["commit"]
        assert distribution["provenance"]["tag"] == release["source"]["tag"]
    linkml = next(item for item in release["distributions"] if item["name"] == "linkml")
    assert linkml["dependency_constraints"] == [
        {"name": "linkml-runtime", "specifier": ">=1.10.0,<2.0.0"}
    ]


def test_source_candidate_records_exact_commit_and_two_build_targets() -> None:
    source = _candidate(_inventory(), "SOURCE_COMMIT")

    assert source["source"]["commit"] == "38737179acd92a7ee644357096583c77c01aed72"
    assert "tag" not in source["source"]
    assert source["source"]["coordinate_url"].endswith(source["source"]["commit"])
    assert {distribution["name"] for distribution in source["distributions"]} == {
        "linkml",
        "linkml-runtime",
    }
    for distribution in source["distributions"]:
        target = distribution["wheel_target"]
        assert target["provision"] == "SOURCE_BUILD_TARGET"
        assert target["identity_state"] == "REQUIRED_FROM_BUILD"
        assert set(target["required_identity_fields"]) == {
            "filename",
            "wheel_tags",
            "sha256",
            "byte_length",
        }
        assert "sha256" not in target


def test_repository_python_tuple_and_primary_sources_are_explicit() -> None:
    data = _inventory()
    python = data["python_candidates"][0]

    assert data["repository"] == {
        "distributions": [
            {"name": "linkml", "source_path": "packages/linkml"},
            {"name": "linkml-runtime", "source_path": "packages/linkml_runtime"},
        ],
        "layout": "MONOREPO",
        "url": "https://github.com/linkml/linkml",
    }
    assert python == {
        "abi": "cp312",
        "architecture": "x86_64",
        "artifact_target": "py3-none-any",
        "basis_source_id": "python-3.12.10-release",
        "candidate_id": "cpython-3.12.10-linux-x86_64-cp312",
        "implementation": "CPython",
        "limitation": "Research tuple only; OD-012 has not fixed a Python tuple.",
        "operating_system": "Linux",
        "version": "3.12.10",
    }
    assert len(data["python_candidates"]) >= 1
    assert all(source["url"].startswith("https://") for source in data["sources"])
    assert {source["publisher"] for source in data["sources"]} == {
        "GitHub",
        "PyPI",
        "Python Software Foundation",
    }


def test_all_unordered_collections_normalize_and_noncanonical_bytes_fail(
    tmp_path: Path,
) -> None:
    data = _inventory()
    permuted = copy.deepcopy(data)
    permuted["candidates"].reverse()
    permuted["python_candidates"].reverse()
    permuted["repository"]["distributions"].reverse()
    permuted["sources"].reverse()
    for candidate in permuted["candidates"]:
        candidate["distributions"].reverse()
        candidate["python_candidate_ids"].reverse()
        candidate["source"]["evidence_source_ids"].reverse()
        archive = candidate["source"]["archive"]
        if candidate["kind"] == "RELEASE":
            archive["artifact_ids"].reverse()
        else:
            archive["required_identity_fields"].reverse()
        candidate["lock_feasibility"]["present_inputs"].reverse()
        candidate["lock_feasibility"]["missing_inputs"].reverse()
        for distribution in candidate["distributions"]:
            if candidate["kind"] == "RELEASE":
                distribution["advertised_python_minors"].reverse()
                distribution["artifacts"].reverse()
                distribution["dependency_constraints"].reverse()
            else:
                distribution["wheel_target"]["required_identity_fields"].reverse()
                distribution["wheel_target"]["target_python_candidate_ids"].reverse()

    assert normalize_inventory(permuted) == normalize_inventory(data)
    assert inventory_identity(permuted) == inventory_identity(data)

    path = tmp_path / "noncanonical.json"
    path.write_text(
        json.dumps(permuted, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with pytest.raises(InventoryError) as caught:
        load_inventory(path)
    assert "canonical order" in str(caught.value)


def test_cli_default_check_succeeds_offline() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "check"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "candidates=2" in result.stdout
    assert "sha256:" in result.stdout


def test_cli_custom_path_fails_closed_without_traceback(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text('{"schema": NaN}', encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "check", str(path)],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 1
    assert "non-finite" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_check_does_not_modify_the_inventory() -> None:
    before = (INVENTORY.read_bytes(), INVENTORY.stat().st_mtime_ns)

    subprocess.run(
        [sys.executable, str(SCRIPT), "check", str(INVENTORY)],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )

    assert (INVENTORY.read_bytes(), INVENTORY.stat().st_mtime_ns) == before


def test_validator_and_cli_are_mechanically_denied_network(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def denied(*_args, **_kwargs):
        raise AssertionError("network attempted")

    monkeypatch.setattr(socket, "socket", denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(http.client.HTTPConnection, "connect", denied)
    monkeypatch.setattr(http.client.HTTPSConnection, "connect", denied)
    monkeypatch.setattr(urllib.request, "urlopen", denied)

    load_inventory(INVENTORY)
    assert main(["check", str(INVENTORY)]) == 0
    assert "candidates=2" in capsys.readouterr().out


def test_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    text = INVENTORY.read_text(encoding="utf-8")
    path = tmp_path / "duplicate.json"
    path.write_text(
        text.replace('"schema":', '"schema": "duplicate",\n  "schema":', 1),
        encoding="utf-8",
    )

    with pytest.raises(InventoryError) as caught:
        load_inventory(path)
    assert "duplicate JSON key" in str(caught.value)


def test_non_finite_json_numbers_are_rejected(tmp_path: Path) -> None:
    for token in ("NaN", "Infinity", "-Infinity"):
        path = tmp_path / f"{token.replace('-', 'negative-')}.json"
        path.write_text('{"value": ' + token + "}", encoding="utf-8")
        with pytest.raises(InventoryError) as caught:
            load_inventory(path)
        assert "non-finite" in str(caught.value)


def test_unknown_top_level_and_nested_fields_are_rejected() -> None:
    data = _inventory()
    data["notes"] = "escape hatch"
    _assert_invalid(data, "unknown field")
    data = _inventory()
    _candidate(data, "RELEASE")["source"]["notes"] = "escape hatch"
    _assert_invalid(data, "unknown field")


def test_mutable_source_references_are_rejected() -> None:
    mutations = []
    data = _inventory()
    _candidate(data, "SOURCE_COMMIT")["source"]["commit"] = "main"
    mutations.append(data)
    data = _inventory()
    _candidate(data, "RELEASE")["source"]["tag"] = "latest"
    mutations.append(data)
    data = _inventory()
    _candidate(data, "SOURCE_COMMIT")["source"]["coordinate_url"] = (
        "https://github.com/linkml/linkml/tree/main"
    )
    mutations.append(data)

    for mutation in mutations:
        _assert_invalid(mutation, "immutable")


def test_short_source_commit_is_rejected() -> None:
    data = _inventory()
    _candidate(data, "SOURCE_COMMIT")["source"]["commit"] = "38737179"

    _assert_invalid(data, "40 lowercase hexadecimal")


def test_non_exact_python_versions_are_rejected() -> None:
    for version in ("3.12", "3.12.x"):
        data = _inventory()
        data["python_candidates"][0]["version"] = version
        _assert_invalid(data, "exact three-part version")


def test_missing_or_duplicate_distribution_is_rejected() -> None:
    data = _inventory()
    _candidate(data, "RELEASE")["distributions"].pop()
    _assert_invalid(data, "exactly linkml and linkml-runtime")
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["distributions"][1] = copy.deepcopy(release["distributions"][0])
    _assert_invalid(data, "exactly linkml and linkml-runtime")


def test_absent_required_archive_identity_is_rejected() -> None:
    data = _inventory()
    del _candidate(data, "SOURCE_COMMIT")["source"]["archive"]

    _assert_invalid(data, "missing field")


def test_unsubstantiated_observed_archive_identity_is_rejected() -> None:
    data = _inventory()
    archive = _candidate(data, "SOURCE_COMMIT")["source"]["archive"]
    archive["identity_state"] = "OBSERVED"

    _assert_invalid(data, "observed archive")


def test_published_and_source_build_artifacts_cannot_be_conflated() -> None:
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["distributions"][0]["artifacts"][0]["provision"] = "SOURCE_BUILD_TARGET"

    _assert_invalid(data, "published artifact")
    data = _inventory()
    source = _candidate(data, "SOURCE_COMMIT")
    source["distributions"][0]["wheel_target"]["provision"] = "PUBLISHED"

    _assert_invalid(data, "source build target")


def test_unsupported_feasibility_state_is_rejected() -> None:
    data = _inventory()
    _candidate(data, "RELEASE")["lock_feasibility"]["state"] = "LIKELY"

    _assert_invalid(data, "lock feasibility state")


def test_probe_ready_requires_inputs_and_remaining_probe() -> None:
    data = _inventory()
    feasibility = _candidate(data, "RELEASE")["lock_feasibility"]
    feasibility["present_inputs"] = []
    feasibility["remaining_probe"] = ""

    _assert_invalid(data, "remaining_probe")


def test_probe_blocked_names_missing_immutable_inputs() -> None:
    data = _inventory()
    _candidate(data, "SOURCE_COMMIT")["lock_feasibility"]["missing_inputs"] = []

    _assert_invalid(data, "PROBE_BLOCKED")


def test_verified_feasibility_requires_complete_commands_and_results() -> None:
    for state in ("VERIFIED_FEASIBLE", "VERIFIED_INFEASIBLE"):
        data = _inventory()
        feasibility = _candidate(data, "RELEASE")["lock_feasibility"]
        feasibility["state"] = state
        _assert_invalid(data, "verified feasibility")


def test_official_source_and_provenance_refs_are_subject_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mutations = []
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["source"]["evidence_source_ids"][0] = "github-linkml-38737179-commit"
    mutations.append(data)
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["distributions"][0]["artifacts"][0]["evidence_source_id"] = (
        "pypi-linkml-runtime-1.11.1-metadata"
    )
    mutations.append(data)
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["distributions"][0]["provenance"]["evidence_source_id"] = (
        "pypi-linkml-runtime-1.11.1-provenance"
    )
    mutations.append(data)
    data = _inventory()
    record = next(
        source
        for source in data["sources"]
        if source["source_id"] == "github-linkml-38737179-commit"
    )
    record["url"] = (
        "https://github.com/linkml/linkml/commit/"
        "a7ed3e4cbb19731f072d0d90b6d52f7d822569ee"
    )
    mutations.append(data)
    data = _inventory()
    record = next(
        source
        for source in data["sources"]
        if source["source_id"] == "pypi-linkml-1.11.1-metadata"
    )
    record["project"] = "linkml-runtime"
    mutations.append(data)
    data = _inventory()
    data["sources"][0]["publisher"] = "PyPI"
    mutations.append(data)
    data = _inventory()
    data["python_candidates"][0]["basis_source_id"] = "unknown-python-release"
    mutations.append(data)
    data = _inventory()
    _candidate(data, "RELEASE")["python_candidate_ids"][0] = "unknown-python"
    mutations.append(data)

    for mutation in mutations:
        _reseal_and_assert_invalid(monkeypatch, mutation)


def test_source_archive_locator_evidence_and_feasibility_refs_are_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mutations = []
    data = _inventory()
    source = _candidate(data, "SOURCE_COMMIT")
    source["source"]["archive"]["locator"] = (
        "https://github.com/other/project/archive/"
        "38737179acd92a7ee644357096583c77c01aed72.tar.gz"
    )
    mutations.append((data, "mismatch"))
    data = _inventory()
    source = _candidate(data, "SOURCE_COMMIT")
    source["source"]["archive"]["evidence_source_id"] = "github-linkml-a7ed3e4c-commit"
    mutations.append((data, "mismatch"))
    data = _inventory()
    source = _candidate(data, "SOURCE_COMMIT")
    source["lock_feasibility"]["missing_inputs"][0]["id"] = "unknown"
    mutations.append((data, "PROBE_BLOCKED"))
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["lock_feasibility"]["present_inputs"][0]["id"] = "unknown"
    mutations.append((data, "PROBE_READY"))
    data = _inventory()
    source = _candidate(data, "SOURCE_COMMIT")
    source["distributions"][0]["wheel_target"]["artifact_id"] = "build:unknown"
    mutations.append((data, "source build"))

    for mutation, _needle in mutations:
        _reseal_and_assert_invalid(monkeypatch, mutation)


def test_malformed_nested_types_fail_cli_without_traceback(tmp_path: Path) -> None:
    mutations = []
    data = _inventory()
    release = _candidate(data, "RELEASE")
    release["distributions"][0]["artifacts"][0]["kind"] = {"not": "a string"}
    mutations.append(data)
    data = _inventory()
    data["sources"][0]["kind"] = {"not": "a string"}
    mutations.append(data)

    for index, mutation in enumerate(mutations):
        path = tmp_path / f"malformed-{index}.json"
        path.write_text(
            json.dumps(mutation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "check", str(path)],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        assert result.returncode == 1
        assert "Traceback" not in result.stderr


def test_governance_selection_and_ranking_fields_are_rejected() -> None:
    data = _inventory()
    data["selection"] = "release"

    _assert_invalid(data, "governance field")
    data = _inventory()
    _candidate(data, "RELEASE")["rank"] = 1

    _assert_invalid(data, "governance field")


def test_duplicate_candidate_kind_is_rejected() -> None:
    data = _inventory()
    data["candidates"][1] = copy.deepcopy(data["candidates"][0])

    _assert_invalid(data, "one RELEASE and one SOURCE_COMMIT")


def test_verification_report_has_exact_shape_artifacts_and_gate_set() -> None:
    report = verify_evidence_snapshot(EVIDENCE, ROOT)

    assert report["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert report["workstream_id"] == "CC-X00"
    assert report["base_commit"] == "8b3b65a01546407bff616fe06fd202399f849763"
    assert {artifact["path"] for artifact in report["artifacts"]} == {
        "conformance/contract_compiler/v0/compiler_baseline_candidates.json",
        "scripts/contract_compiler_baseline_inventory.py",
        "tests/test_contract_compiler_baseline_inventory.py",
    }
    assert str(EVIDENCE.relative_to(ROOT)) not in {
        artifact["path"] for artifact in report["artifacts"]
    }
    assert {check["check_id"] for check in report["checks"]} == {
        "ccx00-red",
        "ccx00-green",
        "ccx00-slice",
        "ccx00-disproof",
        "ccx00-regression",
        "ccx00-package",
        "ccx00-attest",
    }
    assert all(check["result"] == "PASS" for check in report["checks"])

"""Guards for the exact paper-v4 CPython 3.12 macOS dependency lock."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ENVIRONMENT = ROOT / "paper-v4/environment"
EXPECTED_DIGESTS = {
    "requirements.in": (
        "sha256:4c6eee755717731e217576cf5e901c181dab4c32fd849060ebe72ebf584e6d02"
    ),
    "retained-versions.txt": (
        "sha256:0aac78a7349c6662cb05736f325cb92adfda96a32c3ddd48a8e9f2787efdd1e9"
    ),
    "requirements-cp312-macos-arm64.lock": (
        "sha256:80161cf50e9748d8abd7bac6d0a8bc1c949957d8784a6e001da999f7e17451a0"
    ),
}
PACKAGE = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>\S+)")


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _packages(path: Path) -> dict[str, str]:
    return {
        match.group("name").lower().replace("_", "-").replace(".", "-"): match.group(
            "version"
        )
        for line in path.read_text().splitlines()
        if (match := PACKAGE.match(line)) is not None
    }


def test_lock_is_exact_hashed_and_free_of_machine_local_projects() -> None:
    for name, expected in EXPECTED_DIGESTS.items():
        assert _digest(ENVIRONMENT / name) == expected

    retained = _packages(ENVIRONMENT / "retained-versions.txt")
    lock_path = ENVIRONMENT / "requirements-cp312-macos-arm64.lock"
    lock = _packages(lock_path)
    lock_text = lock_path.read_text()

    assert len(lock) == 89
    assert lock == retained
    assert lock_text.count("--hash=sha256:") >= len(lock)
    for forbidden in (
        "/Users/",
        "git+ssh",
        "malleus-code-lab",
        "anthropic==",
        "openai==",
    ):
        assert forbidden not in lock_text

    package_starts = [
        match.start() for match in re.finditer(r"(?m)^[A-Za-z0-9_.-]+==", lock_text)
    ]
    package_starts.append(len(lock_text))
    assert all(
        "--hash=sha256:" in lock_text[start:end]
        for start, end in zip(package_starts[:-1], package_starts[1:], strict=True)
    )


def test_environment_manifest_and_clean_verification_are_bounded() -> None:
    manifest = json.loads((ENVIRONMENT / "environment.json").read_bytes())
    verification = json.loads((ENVIRONMENT / "verification.json").read_bytes())

    assert manifest["status"] == "FROZEN_AND_CLEAN_VERIFIED"
    assert manifest["target"] == {
        "python": "3.12.9",
        "python_build": "Anaconda, Inc.; Feb 6 2025; Clang 14.0.6",
        "implementation": "CPython",
        "cache_tag": "cpython-312",
        "operating_system": "macOS",
        "operating_system_version": "15.7.9",
        "darwin": "24.6.0",
        "machine": "arm64",
        "resolver": "uv 0.11.2",
        "installer": "pip 26.0.1",
    }
    assert manifest["resolution"]["package_count"] == 89
    assert manifest["resolution"]["lock_sha256"] == EXPECTED_DIGESTS[
        "requirements-cp312-macos-arm64.lock"
    ]
    assert verification["status"] == "PASS"
    assert verification["environment"]["hashed_install_succeeded"] is True
    assert verification["reproduction"]["public_results_byte_equal"] is True
    assert verification["reproduction"]["private_ledger_byte_equal"] is True
    assert verification["focused_gate"] == {
        "passed": 184,
        "failed": 0,
        "duration_seconds": 7.02,
    }


def test_private_research_seam_requires_the_declared_source_overlay() -> None:
    manifest = json.loads((ENVIRONMENT / "environment.json").read_bytes())
    project = (ROOT / "pyproject.toml").read_text()

    assert manifest["source_execution"]["source_path"] == "PYTHONPATH=.:src"
    assert '"/src/malleus/_contract_compiler.py"' in project
    assert (ROOT / "src/malleus/_contract_compiler.py").is_file()

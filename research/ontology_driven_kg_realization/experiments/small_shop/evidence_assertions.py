"""Test-only exact comparison against one identified Shop evidence generation.

No regeneration, producer selection, digest exclusions or runtime fallback.
"""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).parent
CURRENT = HERE / "evidence_2026_09_08"


def digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def assert_current_evidence(group, replay, outputs):
    binding = json.loads((CURRENT / "binding.json").read_bytes())
    scenario = binding["scenarios"][group]
    artifacts = {
        item.content
        for item in replay.retained_inputs
        if item.role == "VALIDATED_CONTRACT"
    }
    artifacts.update(
        revision.target_validated_contract_bytes
        for revision in replay.contract_revisions
    )
    actual = {
        digest(content): json.loads(content)["evidence"]["producer"]
        for content in artifacts
    }
    assert actual and actual == scenario["compiler_artifacts"], (
        "Compiler artifacts/producer differ from this evidence generation; "
        "inspect the change and record a successor, do not overwrite old evidence"
    )
    assert set(outputs) == set(scenario["outputs"]), "Output file set differs"
    for name, identity in binding["historical_outputs"].items():
        assert digest((HERE / name).read_bytes()) == identity, (
            f"Historical evidence changed: {name}"
        )
    for name, metadata in scenario["outputs"].items():
        expected = (CURRENT / group / name).read_bytes()
        assert digest(expected) == metadata["sha256"], f"Expected bytes changed: {name}"
        assert outputs[name] == expected, f"Output bytes differ: {group}/{name}"

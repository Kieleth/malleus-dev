"""Pin run-08 to one Core commit and write the manifest and the gate block.

Core changes on main while a cell is open, so a run's declared inputs are the
bytes its producer consumed at one commit and nothing else. This script reads
the seven tracked declared inputs with ``git show <commit>:<path>`` and the
selected reading from its private path, writes ``producer-input-manifest.json``,
and fills the parts of ``run-contract.json`` that are facts about that commit:
the execution baseline, the governance head as the ledger renders it, every
verified piece's digests, the pack versions, and the document adapter's refusal
reasons that are new since the v4.1 coordinate.

Nothing here is typed by hand. A pack version that has not moved, or a Core-12
reason that has not landed, is recorded as it stands and the change entry says
so; re-run the script after the Core work lands to re-pin.

    .venv/bin/python paper-v4/experiment-v4/run-08/pin.py --commit <sha>
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = HERE / "run-contract.json"
MANIFEST = HERE / "producer-input-manifest.json"

RUN_ID = "run-08"
PROTOCOL_VERSION = "v4.2"
INTERFACE_ORDINAL = "8"
PRODUCER_WORKSPACE = f"private/paper-v4-v4-{RUN_ID}/producer"

# The v4.1 coordinate every earlier cell of this iteration ran at. The Core-12
# reason names are whatever the document adapter's enum gained since it.
V4_1_BASELINE_COMMIT = "8b806f7411e11b84e1156cea84b4b641d701db19"

SKILL_PATH = ".claude/skills/malleus-acolyte/SKILL.md"
GOVERNANCE_STATUS = "design/contract_compiler/overseer/status.md"
DOCUMENT_ADAPTER = "src/malleus/_contract_pipeline/document.py"
PLAN_COMPILER = "src/malleus/_contract_pipeline/population.py"
RITE_MODULE = "src/malleus/inquisition/pack_grounding.py"
GROUNDING_RITE = "src/malleus/inquisition/pack-grounding.json"
PROFILE_PATH = "src/malleus/profiles/source-assertion.json"

# Name, tracked source path, workspace target. The eight are run-04's, in
# run-04's order, and the reading is the one input that is untracked.
DECLARED_INPUTS = (
    ("MALLEUS_NASCENT_PROJECT_SKILL", SKILL_PATH, SKILL_PATH),
    (
        "SELECTED_READING",
        "private/paper-v4-text-layer/selected-reading.json",
        "inputs/selected-reading.json",
    ),
    ("MALLEUS_ROOT", "ontology/malleus.yaml", "inputs/malleus.yaml"),
    (
        "LINKML_TYPES",
        "paper-v4/experiment-v2/run-inputs/linkml-types.yaml",
        "inputs/linkml-types.yaml",
    ),
    ("METROLOGY_PACK", "ontology/packs/metrology.yaml", "inputs/metrology.yaml"),
    ("CHRONOLOGY_PACK", "ontology/packs/chronology.yaml", "inputs/chronology.yaml"),
    ("RESEARCH_PACK", "ontology/packs/research.yaml", "inputs/research.yaml"),
    (
        "SOURCE_ASSERTION_PROFILE",
        PROFILE_PATH,
        "inputs/profile-source-assertion.json",
    ),
)
UNTRACKED_INPUTS = {"SELECTED_READING"}
PACKS = ("chronology", "metrology", "research")

HEAD_LINE = re.compile(
    r"^Ledger head: `(?P<entry>OVR-\d+)` / `(?P<hash>sha256:[0-9a-f]{64})`", re.M
)
VERSION_LINE = re.compile(r"^version: (?P<version>\S+)\s*$", re.M)
ENUM_MEMBER = re.compile(r"^    (?P<name>[A-Z][A-Z0-9_]*) = \"(?P=name)\"$", re.M)
ENUM_BLOCK = re.compile(
    r"class DocumentAssertionRefusalReason\(str, Enum\):\n(?P<body>(?:    .*\n|\n)*)"
)

LANDED = "LANDED"
PENDING = "PENDING_AT_PIN"


class PinRefusal(ValueError):
    """The commit does not carry something the pin must record."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _canonical_digest(data: bytes) -> str:
    """The identity Core gives a canonical JSON artifact, from its bytes."""
    return _digest(
        json.dumps(
            json.loads(data),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments], capture_output=True, cwd=ROOT, text=True
    )
    if completed.returncode != 0:
        raise PinRefusal(
            f"git {' '.join(arguments)} refused: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _git_show(commit: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"], capture_output=True, cwd=ROOT
    )
    if completed.returncode != 0:
        raise PinRefusal(
            f"declared input is not readable at {commit}: {path}"
            f" ({completed.stderr.decode(errors='replace').strip()})"
        )
    return completed.stdout


def _text(commit: str, path: str) -> str:
    return _git_show(commit, path).decode("utf-8")


def governance_head(commit: str) -> dict[str, str]:
    """The ledger head as the overseer status page renders it at ``commit``."""
    match = HEAD_LINE.search(_text(commit, GOVERNANCE_STATUS))
    if match is None:
        raise PinRefusal(f"{GOVERNANCE_STATUS} renders no ledger head at {commit}")
    return {"entry_id": match.group("entry"), "head_hash": match.group("hash")}


def pack_versions(commit: str) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in PACKS:
        match = VERSION_LINE.search(_text(commit, f"ontology/packs/{name}.yaml"))
        if match is None:
            raise PinRefusal(f"pack {name} declares no version at {commit}")
        versions[name] = match.group("version")
    return versions


def refusal_reasons(commit: str) -> list[str]:
    """Every member of the document adapter's refusal enum at ``commit``."""
    block = ENUM_BLOCK.search(_text(commit, DOCUMENT_ADAPTER))
    if block is None:
        raise PinRefusal(f"{DOCUMENT_ADAPTER} declares no refusal enum at {commit}")
    names = sorted(match.group("name") for match in ENUM_MEMBER.finditer(block.group("body")))
    if not names:
        raise PinRefusal(f"the refusal enum at {commit} is empty")
    return names


REFERENCE_RUN = "run-04"
REFERENCE_MANIFEST = f"paper-v4/experiment-v4/{REFERENCE_RUN}/producer-input-manifest.json"


def _moved_since_reference(declared: list[dict[str, str]]) -> dict[str, object]:
    """Which declared inputs carry other bytes than the v4.1 cell of record's.

    A cell states what its producer read, and a cell that shares an input list
    with an earlier one has to say which of those inputs actually moved. The
    packs move by design in v4.2; anything else that moved is a fact this run
    records rather than a change it claims.
    """
    reference = {
        item["name"]: item["sha256"]
        for item in json.loads((ROOT / REFERENCE_MANIFEST).read_bytes())[
            "declared_inputs"
        ]
    }
    observed = {item["name"]: item["sha256"] for item in declared}
    if set(observed) != set(reference):
        raise PinRefusal("the declared input set differs from the reference run's")
    return {
        "reference_run": REFERENCE_RUN,
        "reference_manifest": REFERENCE_MANIFEST,
        "moved": sorted(
            name for name in observed if observed[name] != reference[name]
        ),
        "unchanged": sorted(
            name for name in observed if observed[name] == reference[name]
        ),
    }


def build_manifest(commit: str, tree: str, reading: Path) -> dict[str, object]:
    contract = json.loads(CONTRACT.read_bytes())
    declared: list[dict[str, str]] = []
    for name, source, target in DECLARED_INPUTS:
        data = (
            reading.read_bytes()
            if name in UNTRACKED_INPUTS
            else _git_show(commit, source)
        )
        declared.append(
            {
                "name": name,
                "source": source,
                "target": target,
                "sha256": _digest(data),
            }
        )
    return {
        "schema": "malleus.paper-v4.producer-input-manifest/v1",
        "run_id": RUN_ID,
        "status": "FROZEN",
        "producer_workspace": PRODUCER_WORKSPACE,
        "core": {"commit": commit, "tree": tree},
        "interface_coordinates": {
            "capture_id": f"capture:paper-v4:yu-2025:v4:{INTERFACE_ORDINAL}",
            "plan_id": f"plan:paper-v4:yu-2025:v4:{INTERFACE_ORDINAL}",
            "source_id": contract["source"]["source_id"],
        },
        "history_profile": {
            "profile_id": "source-assertion",
            "profile_identity": _canonical_digest(_git_show(commit, PROFILE_PATH)),
            "semantic_unit": "COMPOSITION",
            "origin": "PARTIAL_IMPORT",
        },
        "producer": contract["producer"],
        "input_bytes": {
            "tracked": "GIT_SHOW_AT_CORE_COMMIT",
            "untracked": "PRIVATE_PATH",
            "untracked_inputs": sorted(UNTRACKED_INPUTS),
        },
        "interpreter_preflight": {
            "checked_by": "paper-v4/experiment-v4/run-08/prepare_producer.py",
            "lock": "paper-v4/environment/requirements-cp312-macos-arm64.lock",
            "packages": ["linkml", "linkml-runtime"],
            "recorded_in": "producer-input-receipt.json under interpreter",
        },
        "skill_installer": {
            "method": "WRITE_DECLARED_BYTES_AT_CORE_COMMIT",
            "reason": (
                "the live skill tree is expected to move; the run consumes the"
                " bytes recorded in this manifest"
            ),
            "installed_tree": ".claude/skills",
            "target": SKILL_PATH,
        },
        "declared_inputs": declared,
        "moved_since": _moved_since_reference(declared),
        "forbidden_inputs": contract["producer"]["forbidden_inputs"],
        "session": {
            "fresh": True,
            "single_session": True,
            "delegation": "FORBIDDEN",
            "max_compiler_diagnostic_returns": 2,
            "max_additive_revision_rounds": 2,
            "fallback": "FORBIDDEN",
        },
        "outputs": {
            "ontology_pattern": "work/ontology-attempt-NN.yaml",
            "population": "work/document-population.json",
            "session_log": "work/session-log.md",
            "status": "work/status.json",
        },
    }


def build_verified_pieces(commit: str, tree: str) -> dict[str, object]:
    profile_bytes = _git_show(commit, PROFILE_PATH)
    profile = json.loads(profile_bytes)
    event_role = list(profile["ontology_roles"]["event"])
    base = {"core_commit": commit, "core_tree": tree, "paper_audit": "DIGEST_PINNED"}
    plan_compiler_sha256 = _digest(_git_show(commit, PLAN_COMPILER))
    return {
        "AGGREGATE_REFUSAL_DIAGNOSTICS": {
            **base,
            "governance_entry": "OVR-000395",
            "shape": "ONE_SORTED_DEFECT_SET_PER_REFUSAL",
            "plan_compiler_sha256": plan_compiler_sha256,
            "rite_module_sha256": _digest(_git_show(commit, RITE_MODULE)),
        },
        "DERIVATION_CONTENT_CHECKS": {
            **base,
            "document_adapter_path": DOCUMENT_ADAPTER,
            "document_adapter_sha256": _digest(_git_show(commit, DOCUMENT_ADAPTER)),
            "refusal_reasons": refusal_reasons(commit),
        },
        "EVENT_FAMILY_ADMISSION": {
            **base,
            "profile_id": profile["profile_id"],
            "event_role": event_role,
            "admitted_families": (
                ["entities", "events", "relations"]
                if event_role
                else ["entities", "relations"]
            ),
            "event_participations": (
                "ONLY_WHEN_THE_COMPILED_CONTRACT_DECLARES_EventParticipation"
            ),
            "plan_compiler_sha256": plan_compiler_sha256,
        },
        "FULL_DOMAIN_HISTORY_PROFILE": {
            **base,
            "profile_id": profile["profile_id"],
            "profile_path": PROFILE_PATH,
            "profile_file_sha256": _digest(profile_bytes),
            "profile_sha256": _canonical_digest(profile_bytes),
        },
        "GROUNDED_PACKS_AND_PACK_GROUNDING": {
            **base,
            "grounding_rite_sha256": _digest(_git_show(commit, GROUNDING_RITE)),
            "pack_sha256": {
                name: _digest(_git_show(commit, f"ontology/packs/{name}.yaml"))
                for name in PACKS
            },
            "pack_version": pack_versions(commit),
        },
        "NASCENT_PROJECT_PLAYBOOK": {
            **base,
            "skill_path": SKILL_PATH,
            "skill_sha256": _digest(_git_show(commit, SKILL_PATH)),
        },
    }


def pin(commit_argument: str, reading: Path) -> dict[str, object]:
    commit = _git("rev-parse", f"{commit_argument}^{{commit}}")
    tree = _git("rev-parse", f"{commit}^{{tree}}")
    contract = json.loads(CONTRACT.read_bytes())

    contract["source"]["selected_reading_sha256"] = _digest(reading.read_bytes())
    profile_bytes = _git_show(commit, PROFILE_PATH)
    contract["history"]["profile_sha256"] = _canonical_digest(profile_bytes)

    gate = contract["core_gate"]
    gate["execution_baseline"] = {"core_commit": commit, "core_tree": tree}
    gate["governance_head"] = governance_head(commit)
    gate["verified_pieces"] = build_verified_pieces(commit, tree)
    absent = sorted(set(gate["required_pieces"]) - set(gate["verified_pieces"]))
    if absent:
        raise PinRefusal(f"required pieces are unverified: {', '.join(absent)}")

    changes = {item["id"]: item for item in contract["protocol"]["changes"]}

    packs = changes["PACKS_0_3_0"]
    observed = pack_versions(commit)
    packs["versions"] = {
        name: observed[name] for name in sorted(packs["expected_versions"])
    }
    packs["pin_status"] = (
        LANDED if packs["versions"] == packs["expected_versions"] else PENDING
    )

    derivation = changes["CORE_12_DERIVATION_CHECKS"]
    at_commit = set(refusal_reasons(commit))
    at_baseline = set(refusal_reasons(derivation["baseline_commit"]))
    derivation["reasons"] = sorted(at_commit - at_baseline)
    derivation["pin_status"] = (
        LANDED if set(derivation["expected_reasons"]) <= at_commit else PENDING
    )

    pending = [
        change["core_task"]
        for change in (packs, derivation)
        if change["pin_status"] != LANDED
    ]
    gate["status"] = (
        "PINNED_TO_THE_V4_2_CORE_COORDINATE"
        if not pending
        else "PROVISIONALLY_PINNED_PENDING_"
        + "_AND_".join(task.upper().replace("-", "_") for task in pending)
    )

    manifest = build_manifest(commit, tree, reading)
    MANIFEST.write_bytes(
        json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    CONTRACT.write_bytes(
        json.dumps(contract, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    return {
        "commit": commit,
        "tree": tree,
        "governance_head": gate["governance_head"],
        "pack_versions": packs["versions"],
        "core_12_reasons": derivation["reasons"],
        "core_gate_status": gate["status"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True, help="the Core commit to pin to")
    parser.add_argument(
        "--reading",
        type=Path,
        default=ROOT / "private/paper-v4-text-layer/selected-reading.json",
        help="the untracked selected reading",
    )
    arguments = parser.parse_args(argv)
    try:
        report = pin(arguments.commit, arguments.reading)
    except (OSError, TypeError, ValueError) as error:
        print(f"pin: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

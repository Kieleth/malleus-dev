"""Read-only blast radius of a persisted-format change for temporal correction.

Identities are read from Core objects, never typed. Each scenario recomputes the
affected identities in memory from Core's own shipped artifacts; the
recomputation is first checked to reproduce the shipped bundle identity
unchanged. File counts are ``git grep -l -F`` over the tree of BASE, so files
written by this gate are not counted.

    PYTHONPATH=src:. python design/temporal/g3/blast_radius.py
"""

from __future__ import annotations

import copy
from collections import Counter
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
import subprocess
import sys

import malleus.compiler as api

sys.path.insert(0, str(Path(__file__).resolve().parent))
from driver import build, compile_contract  # noqa: E402

BASE = "e7020879"
ROOT = Path(__file__).resolve().parents[3]


def canonical(value) -> bytes:
    return json.dumps(value, allow_nan=False, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()


def digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def profile_json(name: str) -> dict:
    return json.loads(files("malleus").joinpath("profiles", name).read_bytes())


def bundle_identity(check: dict, policy_bytes: bytes) -> dict:
    """The structural bundle's identity chain, composed the way compiler.py composes it."""
    bundle = api.STRUCTURAL_HISTORY_BUNDLE
    check_bytes = canonical(check)
    policy = api.PolicyProgram.from_bytes(policy_bytes)
    normative = api.compose_normative_profile(
        protocol_machine_program=bundle.protocol_machine_program,
        policy_programs={api.REQUIRED_CHECK_POLICY_REFERENCE: policy},
        capability_refs=(),
    )
    source = canonical(
        {
            "check_contract": check,
            "check_contract_identity": digest(check_bytes),
            "grammar": json.loads(bundle.canonical_bytes)["grammar"],
            "history_binding": json.loads(bundle.history_binding.canonical_bytes),
            "history_binding_identity": bundle.history_binding.identity,
            "normative_profile": json.loads(normative.canonical_bytes),
            "normative_profile_identity": normative.identity,
        }
    )
    return {
        "check contract": digest(check_bytes),
        "structural admission policy": policy.identity,
        "normative profile": normative.identity,
        "structural history bundle": digest(source),
        "_normative": normative,
    }


def shipped() -> dict:
    bundle = api.STRUCTURAL_HISTORY_BUNDLE
    return {
        "check contract": bundle.check_contract_identity,
        "structural admission policy": bundle.policy_program.identity,
        "normative profile": bundle.normative_profile.identity,
        "structural history bundle": bundle.identity,
        "protocol machine": bundle.protocol_machine_program.identity,
        "history binding": bundle.history_binding.identity,
        "state-version profile": api.STATE_VERSION_PROFILE.identity,
        "source-assertion profile": api.SOURCE_ASSERTION_PROFILE.identity,
        "object-event profile": api.OBJECT_EVENT_PROFILE.identity,
        "contract revision policy": api.CONTRACT_REVISION_POLICY.identity,
    }


def grep_files(text: str) -> list[str]:
    done = subprocess.run(
        ["git", "grep", "-l", "-F", text, BASE, "--"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if done.returncode not in (0, 1):
        raise RuntimeError(done.stderr)
    return sorted(line.split(":", 1)[1] for line in done.stdout.splitlines())


def count(text: str) -> dict:
    full = grep_files(text)
    short = grep_files(text[7:15]) if text.startswith("sha256:") else full
    return {
        "full": len(full),
        "prefix8": len(short),
        "by_area (union of both)": dict(Counter(path.split("/")[0] for path in sorted(set(full) | set(short)))),
    }


def scenarios(change_set) -> dict:
    """change_set: any composed KnowledgeChangeSet, to read its grammar string from."""
    ids = shipped()
    check = profile_json("structural-admission-check.json")
    policy = profile_json("structural-admission-policy.json")

    # Self-check: the in-memory composition reproduces the shipped chain.
    same = bundle_identity(check, canonical(policy))
    assert all(same[k] == ids[k] for k in ("check contract", "structural admission policy", "normative profile", "structural history bundle"))

    out = {}
    grammar = change_set.data["grammar"]

    # A. One optional operation field, same grammar string, same builtin version.
    bundle_bytes = api.STRUCTURAL_HISTORY_BUNDLE.canonical_bytes
    out["A"] = {
        "change": "an optional operation field (for example a declared correction link), emitted only when set; grammar string and builtin version unchanged",
        "moved": [],
        "evidence": {
            "bundle bytes name the change-set grammar": grammar.encode() in bundle_bytes,
            "bundle bytes name an operation kind or operation-only field": any(
                name.encode() in bundle_bytes
                for name in ("supersedes_record_id", "operation_type", "CREATE_ENTITY", "CREATE_RELATION", "valid_time")
            ),
            "existing change-set bytes unchanged": "yes, the field is absent from every existing operation",
        },
        "cost": "fail-closed readers: today's Core refuses an operation carrying an unknown field (MALFORMED_CHANGE_SET: operation fields are not closed), so bytes written with the field are unreadable by an older Core",
    }
    extended = json.loads(change_set.canonical_bytes)
    extended["operations"][0]["corrects_record_id"] = "r1"
    try:
        api.KnowledgeChangeSet.from_bytes(canonical(extended))
        out["A"]["today's reader on a change set with the field"] = "ACCEPTED"
    except api.KnowledgeChangeRefusal as refusal:
        out["A"]["today's reader on a change set with the field"] = f"{refusal.reason.name}: {refusal.detail}"

    # B. Bump the change-set grammar string.
    bumped = json.loads(change_set.canonical_bytes)
    bumped["grammar"] = grammar.replace("private-v0", "private-v1")
    try:
        api.KnowledgeChangeSet.from_bytes(canonical(bumped))
        reader = "ACCEPTED"
    except api.KnowledgeChangeRefusal as refusal:
        reader = f"{refusal.reason.name}: {refusal.detail}"
    out["B"] = {
        "change": f"bump the change-set grammar string {grammar}",
        "moved": ["every newly composed change-set identity, and so every ledger head re-derived from the same inputs"],
        "example": {"before": change_set.identity, "after": digest(canonical(bumped))},
        "today's reader on the bumped grammar": reader,
        "files naming the grammar string": count(grammar),
    }

    # C. Bump the CORE_BUILTIN version the structural check names.
    check_v2 = copy.deepcopy(check)
    check_v2["executor"]["builtin_version"] = str(int(check["executor"]["builtin_version"]) + 1)
    check_v2_identity = digest(canonical(check_v2))
    policy_v2 = copy.deepcopy(policy)
    for member in policy_v2["required_checks"]:
        if member["check_contract_id"] == check["check_contract_id"]:
            member["check_contract_identity"] = check_v2_identity
    moved = bundle_identity(check_v2, canonical(policy_v2))
    compilation = compile_contract("g1-01")
    partial_before = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    ).identity
    partial_after = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=moved["_normative"],
    ).identity
    try:
        api.resolve_core_builtin(check_v2["executor"]["builtin_id"], check_v2["executor"]["builtin_version"])
        registry = "HELD"
    except api.CheckContractError as error:
        registry = str(error)
    out["C"] = {
        "change": "the structural check's builtin applies a new operation kind or field, and its version is bumped",
        "moved": {
            name: {"before": ids[name], "after": moved[name], "files": count(ids[name])}
            for name in ("check contract", "structural admission policy", "normative profile", "structural history bundle")
        },
        "partial effective contract (g1-01 contract)": {"before": partial_before, "after": partial_after},
        "every structural history": "its bootstrap bytes, and so every ledger head and every recorded policy_identity in CHANGE_PROPOSED and CHECK_RECORDED",
        "today's builtin registry on the bumped version": registry,
    }

    # D. The state-version profile distinguishes correction from transition.
    profile = json.loads(api.STATE_VERSION_PROFILE.canonical_bytes)
    profile["change_semantics"]["correction"] = "CORRECT_STATE_VERSION"
    moved_profile = api.DomainHistoryProfile.from_data(profile).identity
    out["D"] = {
        "change": "state-version change_semantics.correction no longer equals transition",
        "moved": {"state-version profile": {"before": ids["state-version profile"], "after": moved_profile, "files": count(ids["state-version profile"])}},
        "unmoved": {name: count(ids[name]) for name in ("source-assertion profile", "object-event profile")},
    }
    out["unmoved in every scenario"] = {
        name: {"identity": ids[name], "files": count(ids[name])} for name in ("protocol machine", "history binding", "contract revision policy")
    }
    return out


if __name__ == "__main__":
    import tempfile

    run = build("g1-01", Path(tempfile.mkdtemp()))
    result = scenarios(run.history.replay().change_sets[0])
    print(json.dumps({k: v for k, v in result.items()}, indent=1, default=str))

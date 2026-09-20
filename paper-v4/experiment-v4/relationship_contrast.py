"""Reconstruct and stage a one-block input contrast. Does not launch models.

This is a paper experimental variant of historical guidance, not a Core skill
release. Runtime, source, packs, profile and every other skill paragraph stay
fixed. Actual launch attestation and evaluation binding are still needed.
"""

from hashlib import sha256
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
MANIFEST = Path(__file__).with_name("run-26") / "producer-input-manifest.json"
MANIFEST_SHA256 = "db7454fbaeb187442720b1a637b8147a8bd430dca1717ee862c7ffbcf25da5bc"
CORE = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
CORRECTION = "723a4f92c4a11d695547d21d3bc213ef80a6b503"
SKILL = ".claude/skills/malleus-acolyte/SKILL.md"
OLD_BLOCK = (
    b"   A relation's endpoints are formalized by an assertion whose statement names\n"
    b"   both of them; a relation the reading only implies is a `RELATION_ABSENT`\n"
    b"   gap, not a derivation from a neighbouring sentence.\n"
)
START = b"   Distinguish a proposition identity, an optional label, and its content.\n"
END = b"   Inspect the returned `canonical_census_bytes`; continue reviewing\n"


def digest(data):
    return "sha256:" + sha256(data).hexdigest()


def manifest():
    data = MANIFEST.read_bytes()
    if sha256(data).hexdigest() != MANIFEST_SHA256:
        raise ValueError("historical input manifest identity differs")
    value = json.loads(data)
    if value["core"]["commit"] != CORE:
        raise ValueError("historical Core coordinate differs")
    return value


def git_bytes(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def replace_guidance(old_skill):
    if old_skill.count(OLD_BLOCK) != 1:
        raise ValueError("old relationship block must occur exactly once")
    corrected = git_bytes(CORRECTION, SKILL)
    if corrected.count(START) != 1 or corrected.count(END) != 1:
        raise ValueError("corrected block boundaries must occur exactly once")
    start, end = corrected.index(START), corrected.index(END)
    if end <= start:
        raise ValueError("corrected block boundaries are reversed")
    return old_skill.replace(OLD_BLOCK, corrected[start:end], 1)


def check_pair(old, new):
    expected = {
        item["target"]: item["sha256"] for item in manifest()["declared_inputs"]
    }
    for arm in (old, new):
        if set(arm) != set(expected):
            raise ValueError("input closure differs from the eight declared inputs")
        if any(type(data) is not bytes or not data for data in arm.values()):
            raise ValueError("inputs must be nonempty bytes")
    for target, identity in expected.items():
        if digest(old[target]) != identity:
            raise ValueError(f"historical input identity differs: {target}")
        required = replace_guidance(old[target]) if target == SKILL else old[target]
        if new[target] != required:
            raise ValueError(
                f"change outside the selected relationship block: {target}"
            )


def build_pair():
    old = {}
    for item in manifest()["declared_inputs"]:
        data = (
            (ROOT / item["source"]).read_bytes()
            if item["name"] == "SELECTED_READING"
            else git_bytes(CORE, item["source"])
        )
        if digest(data) != item["source_sha256"]:
            raise ValueError(f"source identity differs: {item['name']}")
        if item["staged_as"] == "CANONICAL_JSON":
            data = json.dumps(
                json.loads(data),
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode()
        elif item["staged_as"] != "SOURCE_BYTES":
            raise ValueError(f"unknown input staging: {item['staged_as']}")
        old[item["target"]] = data
    new = {**old, SKILL: replace_guidance(old[SKILL])}
    check_pair(old, new)
    return old, new


def prepare_pair(root):
    """Stage the author-selected Sol pair once, without historical templates."""
    root = root.resolve()
    if root.exists():
        raise ValueError("comparison destination already exists")
    if PRIVATE.resolve() not in root.parents:
        raise ValueError("comparison must be below private/")
    pair = build_pair()
    reference = manifest()
    template = Path(__file__).with_name("relationship-producer-task.md").read_text()
    helper = (ROOT / "paper-v4/answer-demonstration/input_delivery.py").read_bytes()
    pending = {}
    for arm, inputs in zip(("a", "b"), pair, strict=True):
        run = root / arm
        task = (
            template.replace("<RUN>", str(run))
            .replace("<PYTHON>", str(ROOT / ".venv/bin/python"))
            .encode()
        )
        identity = f"sol-relationship-contrast-01-{arm}"
        packet = {
            "schema": "malleus.paper-v4.relationship-contrast-inputs/v1",
            "run_id": identity,
            "core": reference["core"],
            "producer": {
                "model_id": "gpt-5.6-sol",
                "reasoning_effort": "ultra",
                "harness": "collaboration.spawn_agent",
                "fork_turns": "none",
                "session": "FRESH_SINGLE_SESSION",
                "fallback": "FORBIDDEN",
                "max_compiler_diagnostic_returns": 2,
                "max_population_diagnostic_returns": 2,
                "max_additive_revision_rounds": 2,
            },
            "interface_coordinates": {
                "capture_id": f"capture:paper-v4:{identity}",
                "plan_id": f"plan:paper-v4:{identity}",
                "source_id": reference["interface_coordinates"]["source_id"],
            },
            "history_profile": reference["history_profile"],
            "declared_inputs": [
                {
                    "name": item["name"],
                    "target": item["target"],
                    "sha256": digest(inputs[item["target"]]),
                }
                for item in reference["declared_inputs"]
            ],
            "task_sha256": digest(task),
            "delivery_helper_sha256": digest(helper),
        }
        pending.update(
            {
                run / "task.md": task,
                run / "input_delivery.py": helper,
                run / "producer-input-manifest.json": (
                    json.dumps(packet, indent=2) + "\n"
                ).encode(),
                **{run / "producer" / target: data for target, data in inputs.items()},
            }
        )
    root.mkdir(parents=True, exist_ok=False)
    for path, data in pending.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for arm in ("a", "b"):
        (root / arm / "producer/work").mkdir()
    return root


if __name__ == "__main__":
    old, new = build_pair()
    print(
        json.dumps(
            {
                "status": "INPUT_CONTRAST_VERIFIED_NOT_LAUNCHED",
                "core": CORE,
                "correction_block_source": CORRECTION,
                "historical_manifest_sha256": "sha256:" + MANIFEST_SHA256,
                "inputs": {
                    key: {"old": digest(old[key]), "context": digest(new[key])}
                    for key in sorted(old)
                },
            },
            indent=2,
        )
    )

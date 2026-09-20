"""The new run uses copied, identified inputs, never the moving source tree."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "private/beam-weather-calibration-01"


def test_observed_launch_and_complete_model_visible_input_delivery():
    helper = RUN / "input_delivery.py"
    spec = importlib.util.spec_from_file_location("beam_delivery", helper)
    delivery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(delivery)
    launch = json.loads((RUN / "launch.json").read_bytes())
    assert launch["model"] == "gpt-5.6-sol"
    assert launch["reasoning_effort"] == "low"
    assert launch["reasoning_effort_request"] == "OMITTED"
    assert launch["deviation"]
    result = delivery.verify_delivery(RUN, "initial")
    assert result["reasoning_effort"] == "low"
    assert sum(result["frames_per_input"].values()) == 119


def test_producer_declared_inputs_are_exact_and_exclude_evaluation():
    manifest = json.loads((RUN / "producer-input-manifest.json").read_bytes())
    assert manifest["core"]["commit"] == "18015352e2eb5bffbb58125c95de40eba0f4c992"
    assert manifest["producer"]["model"] == "gpt-5.6-sol"
    assert manifest["producer"]["fork_turns"] == "none"
    assert manifest["history_profile_identity"] == (
        "sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5"
    )
    expected = {
        "TASK",
        "READING",
        "SOURCE_MAP",
        "ACOLYTE",
        "LINKML_TYPES",
        "MALLEUS_ROOT",
        "RESEARCH_PACK",
        "METROLOGY_PACK",
        "CHRONOLOGY_PACK",
        "OBJECT_EVENT",
        "HISTORY_PROFILE",
    }
    assert {item["name"] for item in manifest["declared_inputs"]} == expected
    for item in manifest["declared_inputs"]:
        path = RUN / "producer" / item["target"]
        assert path.resolve().is_relative_to(RUN)
        assert not path.resolve().is_relative_to(RUN / "evaluation")
        assert (
            "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        )


def test_copied_core_bytes_equal_exact_git_commit():
    manifest = json.loads((RUN / "runtime-manifest.json").read_bytes())
    commit = manifest["commit"]
    tracked = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", commit, *manifest["copied_roots"]], cwd=ROOT
    )
    expected = {
        row.split(b"\t", 1)[1].decode(): row.split()[2].decode()
        for row in tracked.split(b"\0")
        if row
    }
    actual = {
        p.relative_to(RUN / "runtime").as_posix(): p
        for p in (RUN / "runtime").rglob("*")
        if p.is_file()
    }
    assert actual.keys() == expected.keys()
    for name, path in actual.items():
        raw = path.read_bytes()
        assert (
            hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            == expected[name]
        )

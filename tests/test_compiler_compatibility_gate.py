"""The bounded two-producer gate cannot excuse behavioral failures."""

from copy import deepcopy
from importlib import import_module
from pathlib import Path

import pytest


def gate():
    return import_module("scripts.check_compiler_compatibility")


def result():
    return {
        "producer": "candidate",
        "collected": ["test_a", "test_b"],
        "exit_code": 1,
        "collection_errors": [],
        "tests": {
            "test_a": {"setup": "passed", "call": "passed", "teardown": "passed"},
            "test_b": {
                "setup": "passed",
                "call": "failed",
                "teardown": "passed",
                "failure": {
                    "type": "builtins.AssertionError",
                    "path": "test_b.py",
                    "line": 30,
                    "comparison": "exact-frozen-comparison",
                },
            },
        },
    }


def test_exact_observed_candidate_is_accepted_without_relabeling_raw_failure():
    api = gate()
    raw = result()
    before = deepcopy(raw)
    api.require_exact_run(raw, before)
    assert raw == before
    assert raw["exit_code"] == 1


@pytest.mark.parametrize(
    "mutation",
    [
        "producer",
        "same_node_earlier_failure",
        "same_location_different_values",
        "new_failure",
        "skip",
        "deselect",
        "collection_error",
        "teardown_error",
        "exit_code",
    ],
)
def test_candidate_failure_classification_is_not_a_node_allowlist(mutation):
    api = gate()
    expected = result()
    actual = deepcopy(expected)
    if mutation == "producer":
        actual["producer"] = "historical"
    elif mutation == "same_node_earlier_failure":
        actual["tests"]["test_b"]["failure"]["line"] = 12
    elif mutation == "same_location_different_values":
        actual["tests"]["test_b"]["failure"]["comparison"] = "changed-quantity"
    elif mutation == "new_failure":
        actual["tests"]["test_a"]["call"] = "failed"
    elif mutation == "skip":
        actual["tests"]["test_b"]["call"] = "skipped"
    elif mutation == "deselect":
        actual["collected"].remove("test_b")
    elif mutation == "collection_error":
        actual["collection_errors"].append("fixture unavailable")
    elif mutation == "teardown_error":
        actual["tests"]["test_b"]["teardown"] = "failed"
    else:
        actual["exit_code"] = 2
    with pytest.raises(api.GateRefusal):
        api.require_exact_run(actual, expected)


def test_semantic_parity_does_not_strip_arbitrary_hashes_or_fields():
    api = gate()
    old = {"producer": "old", "graph": {"quantity": 2}, "source": "old-source"}
    new = {**old, "producer": "new"}
    api.require_parity(old, new, ["/producer"])
    for key, value in (("graph", {"quantity": 3}), ("source", "other-source")):
        changed = {**new, key: value}
        with pytest.raises(api.GateRefusal):
            api.require_parity(old, changed, ["/producer"])
    with pytest.raises(api.GateRefusal):
        api.require_parity(old, old, ["/producer"])


def test_import_origin_must_belong_to_selected_archive(tmp_path):
    api = gate()
    selected = tmp_path / "selected"
    path = selected / "src/malleus/compiler.py"
    path.parent.mkdir(parents=True)
    path.touch()
    api.require_origin(path, selected)
    with pytest.raises(api.GateRefusal):
        api.require_origin(tmp_path / "other/src/malleus/compiler.py", selected)


def test_subprocess_environment_cannot_inherit_another_producer():
    api = gate()
    env = api.worker_environment(
        Path("/exact/archive"),
        {
            "PATH": "/bin",
            "PYTHONPATH": "/wrong",
            "PYTHONHOME": "/wrong",
            "PYTEST_ADDOPTS": "-k hide_failure",
            "PYTEST_PLUGINS": "bad_plugin",
        },
    )
    assert env["PYTHONPATH"] == "/exact/archive/src:/exact/archive"
    assert env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert "PYTEST_ADDOPTS" not in env and "PYTEST_PLUGINS" not in env
    assert "PYTHONHOME" not in env


def test_comparison_fingerprint_keeps_types_and_all_values():
    api = gate()
    fingerprint = api.comparison_identity
    assert fingerprint(b"2", "2") != fingerprint("2", "2")
    assert fingerprint({"q": 2}, {"q": 1}) != fingerprint({"q": 3}, {"q": 1})
    assert fingerprint({"a": 1, "b": 2}, {}) == fingerprint({"b": 2, "a": 1}, {})
    with pytest.raises(api.GateRefusal):
        fingerprint(object(), {})

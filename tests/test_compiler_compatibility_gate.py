"""The bounded two-producer gate cannot excuse behavioral failures."""

from copy import deepcopy
from importlib import import_module
import json
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


def test_real_pytest_failure_in_the_same_node_is_never_excused(tmp_path):
    api = gate()
    root = tmp_path / "archive"
    api.export(
        "1be958e88dce865c8e785638d1c15508c92bd1d2",
        "8334a558442eb64ec90973d6d0ab08eba3b85ce6",
        root,
    )
    test = root / "tests/test_gate_fault.py"
    test.write_text(
        "def test_receipt():\n    assert {'quantity': 2} == {'quantity': 1}\n"
    )
    baseline = api.run_worker(
        "pytest", root, tmp_path / "baseline.json", ["tests/test_gate_fault.py"]
    )
    assert baseline["exit_code"] == 1
    assert baseline["phases"]["call:failed"] == 1
    failure = next(iter(baseline["failures"].values()))
    assert failure["comparison"] == api.comparison_identity(
        {"quantity": 2}, {"quantity": 1}
    )
    for index, source in enumerate(
        (
            "def test_receipt():\n    assert {'quantity': 3} == {'quantity': 1}\n",
            "def test_receipt():\n    raise ValueError('new behavior failed')\n",
            "import pytest\ndef test_receipt():\n    pytest.skip('hide it')\n",
        )
    ):
        test.write_text(source)
        observed = api.run_worker(
            "pytest",
            root,
            tmp_path / f"mutation-{index}.json",
            ["tests/test_gate_fault.py"],
        )
        with pytest.raises(api.GateRefusal):
            api.require_exact_run(observed, baseline)
    test.write_text(
        "def test_receipt():\n    assert {'quantity': 2} == {'quantity': 1}\n"
    )
    producer = root / "src/malleus/_contract_pipeline/view.py"
    producer.write_bytes(
        producer.read_bytes() + b"\n# deliberately different producer\n"
    )
    wrong_producer = api.run_worker(
        "pytest", root, tmp_path / "producer.json", ["tests/test_gate_fault.py"]
    )
    assert wrong_producer["producer"] != baseline["producer"]
    assert wrong_producer["failures"] == baseline["failures"]
    with pytest.raises(api.GateRefusal):
        api.require_exact_run(wrong_producer, baseline)


def test_wrong_git_tree_refuses_before_export(tmp_path):
    api = gate()
    with pytest.raises(api.GateRefusal, match="Wrong tree"):
        api.export(
            "1be958e88dce865c8e785638d1c15508c92bd1d2",
            "wrong-tree",
            tmp_path / "archive",
        )
    assert not (tmp_path / "archive").exists()


def test_execution_identity_includes_the_independent_probe_code(tmp_path):
    api = gate()
    for name in api.GATE_CODE:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"original code")
    before = api.gate_code_identity(tmp_path)
    helper = tmp_path / "scripts/compiler_compatibility_probe.py"
    helper.write_bytes(b"changed probe")
    after = api.gate_code_identity(tmp_path)
    assert before["identity"] != after["identity"]
    assert (
        before["files"]["scripts/check_compiler_compatibility.py"]
        == after["files"]["scripts/check_compiler_compatibility.py"]
    )
    with pytest.raises(api.GateRefusal):
        api.require_exact_run(after, before)


def test_omitting_a_behavior_probe_or_its_trace_fails():
    api = gate()
    semantics = {
        name: {
            "graph": {"nodes": ["one"]},
            "record_links": {"one": []},
            "retained": {"source": "bytes"},
            "population_plan_traces": name not in {"showcase", "correction"},
            "traces": {"one": {}} if name not in {"showcase", "correction"} else {},
        }
        for name in (
            "fresh",
            "document",
            "object_event",
            "public_population",
            "showcase",
            "correction",
        )
    }
    probe = {"artifact": {}, "fresh_report": {}, "semantics": semantics}
    api.require_probe_coverage(probe)
    for name in semantics:
        missing = deepcopy(probe)
        del missing["semantics"][name]
        with pytest.raises(api.GateRefusal):
            api.require_probe_coverage(missing)
    probe["semantics"]["document"]["traces"] = {}
    with pytest.raises(api.GateRefusal):
        api.require_probe_coverage(probe)


def test_checked_in_binding_preserves_the_exact_nine_and_no_semantic_exemptions():
    api = gate()
    binding = json.loads(api.BINDING.read_bytes())
    api.require_binding(binding)
    altered = deepcopy(binding)
    altered["historical"]["expected_run"]["phases"]["call:passed"] = 8
    altered["historical"]["expected_run"]["phases"]["call:skipped"] = 1
    with pytest.raises(api.GateRefusal):
        api.require_binding(altered)
    for path in (
        "/semantics/fresh/graph",
        "/semantics/correction/check_receipts/2/value/change/operations/0/properties/ordered_quantity",
    ):
        altered = deepcopy(binding)
        altered["parity_differences"].append(path)
        with pytest.raises(api.GateRefusal):
            api.require_binding(altered)

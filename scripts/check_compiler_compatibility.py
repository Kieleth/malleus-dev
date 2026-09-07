"""Verify one frozen compiler repair against its exact historical producer.

Repository-local gate. A successful result does not turn the raw candidate
pytest invocation green. See research/action_history_contract_freeze/GATE.md.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from importlib import metadata
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "research/action_history_contract_freeze/gate.json"
GATE_CODE = (
    "scripts/check_compiler_compatibility.py",
    "scripts/compiler_compatibility_probe.py",
)


class GateRefusal(ValueError):
    """The exact bounded evidence contract was not satisfied."""


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def digest(value):
    return "sha256:" + sha256(value).hexdigest()


def gate_code_identity(root):
    closure = {name: digest((root / name).read_bytes()) for name in GATE_CODE}
    return {"files": closure, "identity": digest(canonical(closure))}


def require_probe_coverage(probe):
    scenarios = {
        "fresh",
        "document",
        "object_event",
        "public_population",
        "showcase",
        "correction",
    }
    if (
        set(probe) != {"artifact", "fresh_report", "semantics"}
        or set(probe["semantics"]) != scenarios
    ):
        raise GateRefusal("Missing or changed independent semantic proof scenario")
    for name, value in probe["semantics"].items():
        if not value["graph"] or not value["record_links"] or not value["retained"]:
            raise GateRefusal(f"Empty semantic proof: {name}")
        expected_trace = name not in {"showcase", "correction"}
        if (
            value["population_plan_traces"] is not expected_trace
            or bool(value["traces"]) is not expected_trace
        ):
            raise GateRefusal(f"Wrong population trace coverage: {name}")


def require_binding(binding):
    historical = binding["historical"]
    candidate = binding["candidate"]
    original = historical["expected_run"]
    current = candidate["expected_run"]
    selectors = historical["selectors"]
    if len(selectors) != 9 or len(set(selectors)) != 9:
        raise GateRefusal("Historical gate requires exactly nine distinct tests")
    if (
        original["phases"]
        != {"setup:passed": 9, "call:passed": 9, "teardown:passed": 9}
        or original["failures"]
        or original["xfails"]
        or original["exit_code"] != 0
    ):
        raise GateRefusal(
            "Historical reproduction must pass all nine, not skip or deselect"
        )
    if set(current["failures"]) != {f"{node}:call" for node in selectors}:
        raise GateRefusal(
            "Candidate failure bindings must name exactly the historical nine"
        )
    if any(
        value["type"] != "builtins.AssertionError" or not value["comparison"]
        for value in current["failures"].values()
    ):
        raise GateRefusal(
            "Each candidate mismatch needs an exact assertion and comparison"
        )
    if original["producer"] == current["producer"]:
        raise GateRefusal("Historical and repaired producers must be distinct")
    fixed = {
        "/artifact/evidence/producer/sha256",
        "/artifact/evidence_sha256",
        "/fresh_report/ledger_head",
        "/fresh_report/ledger_sha256",
        "/fresh_report/receipt_identity",
    }
    for path in binding["parity_differences"]:
        if path in fixed:
            continue
        parts = path.split("/")
        if (
            len(parts) < 6
            or parts[1] != "semantics"
            or parts[3] != "check_receipts"
            or not parts[4].isdecimal()
        ):
            raise GateRefusal(f"Unbounded parity exclusion: {path}")
        tail = parts[5:]
        allowed = (
            tail == ["record_id"]
            or (
                parts[2] == "correction"
                and tail
                in (
                    ["value", "base", "acceptance_head"],
                    ["value", "base", "materialization_head"],
                )
            )
            or (
                parts[2] == "showcase"
                and tail
                in (
                    ["value", "change_set_identity"],
                    ["value", "verification_identity"],
                )
            )
        )
        if parts[2] not in {"correction", "showcase"} or not allowed:
            raise GateRefusal(f"Domain/source/trace parity has no exclusion: {path}")


def comparison_identity(left, right):
    def typed(value):
        if type(value) is bytes:
            return ["bytes", value.hex()]
        if type(value) in (str, int, float, bool) or value is None:
            return [type(value).__name__, value]
        if type(value) in (list, tuple):
            return [type(value).__name__, [typed(item) for item in value]]
        if type(value) is dict and all(type(key) is str for key in value):
            return ["dict", {key: typed(item) for key, item in value.items()}]
        raise GateRefusal(f"Unsupported comparison value: {type(value).__name__}")

    return digest(canonical([typed(left), typed(right)]))


def changed_paths(left, right, path=""):
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict) and left.keys() == right.keys():
        return [
            p
            for key in sorted(left)
            for p in changed_paths(left[key], right[key], f"{path}/{key}")
        ]
    if isinstance(left, list) and len(left) == len(right):
        return [
            p
            for i, pair in enumerate(zip(left, right, strict=True))
            for p in changed_paths(*pair, f"{path}/{i}")
        ]
    return [] if left == right else [path]


def require_exact_run(actual, expected):
    differences = changed_paths(actual, expected)
    if differences:
        raise GateRefusal(f"Run differs from exact binding at {differences}")


def require_parity(old, new, allowed_paths):
    differences = changed_paths(old, new)
    if sorted(differences) != sorted(allowed_paths):
        raise GateRefusal(
            f"Semantic parity differs at {differences}; allowed {allowed_paths}"
        )


def require_origin(path, root):
    if not Path(path).resolve().is_relative_to(root.resolve()):
        raise GateRefusal(f"Producer mixing: {path} is outside {root}")


def worker_environment(root, inherited):
    env = {
        key: value
        for key, value in inherited.items()
        if not key.startswith(("PYTHON", "PYTEST"))
    }
    env.update(
        PYTHONPATH=f"{root}/src:{root}",
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONNOUSERSITE="1",
        PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
    )
    return env


def verify_loaded_origins(root):
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] in {"malleus", "tests", "research"}:
            path = getattr(module, "__file__", None)
            if path:
                require_origin(path, root)


def pytest_worker(selectors):
    import pytest
    from tests.contract_compiler.pareto.test_public_compiler import _compiled_shop
    import malleus.compiler as api

    producer = json.loads(_compiled_shop(api).artifact.artifact_bytes)["evidence"][
        "producer"
    ]["sha256"]

    class Reports:
        def __init__(self):
            self.collected = []
            self.errors = []
            self.phases = []
            self.failures = {}
            self.xfails = {}
            self.comparison = None

        def pytest_collection_finish(self, session):
            self.collected = sorted(item.nodeid for item in session.items)

        def pytest_collectreport(self, report):
            if report.failed:
                self.errors.append(report.nodeid)

        def pytest_runtest_setup(self, item):
            self.comparison = None

        def pytest_assertrepr_compare(self, config, op, left, right):
            self.comparison = None
            if op == "==":
                try:
                    self.comparison = comparison_identity(left, right)
                except GateRefusal:
                    pass  # An unsupported comparison cannot match a bound failure.

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(self, item, call):
            report = (yield).get_result()
            self.phases.append((report.when, report.outcome))
            if hasattr(report, "wasxfail"):
                self.xfails[item.nodeid] = report.wasxfail
            if report.failed:
                frame = call.excinfo.traceback[-1]
                self.failures[f"{item.nodeid}:{report.when}"] = {
                    "type": f"{call.excinfo.type.__module__}.{call.excinfo.type.__name__}",
                    "path": str(
                        Path(str(frame.path)).resolve().relative_to(Path.cwd())
                    ),
                    "line": frame.lineno + 1,
                    "comparison": self.comparison,
                }

    reports = Reports()
    code = pytest.main(
        ["-q", "-p", "no:cacheprovider", "--tb=short", *selectors], plugins=[reports]
    )
    verify_loaded_origins(Path.cwd())
    return {
        "producer": producer,
        "collected_sha256": digest(canonical(reports.collected)),
        "collected_count": len(reports.collected),
        "phases": {
            f"{phase}:{outcome}": count
            for (phase, outcome), count in sorted(Counter(reports.phases).items())
        },
        "failures": reports.failures,
        "xfails": reports.xfails,
        "collection_errors": reports.errors,
        "exit_code": int(code),
    }


def export(commit, tree, destination):
    actual = subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{tree}}"], cwd=ROOT, text=True
    ).strip()
    if actual != tree:
        raise GateRefusal(f"Wrong tree for {commit}: {actual}, expected {tree}")
    data = subprocess.check_output(["git", "archive", commit], cwd=ROOT)
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(destination, filter="data")


def run_worker(mode, root, result_path, selectors=()):
    with result_path.with_suffix(".log").open("wb") as log:
        process = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker",
                mode,
                "--result",
                str(result_path),
                *selectors,
            ],
            cwd=root,
            env=worker_environment(root, os.environ),
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    if process.returncode:
        raise GateRefusal(
            f"{mode} worker failed; inspect {result_path.with_suffix('.log')}"
        )
    return json.loads(result_path.read_bytes())


def run_gate(output):
    binding_bytes = BINDING.read_bytes()
    binding = json.loads(binding_bytes)
    require_binding(binding)
    code_identity = gate_code_identity(ROOT)
    output.mkdir(parents=True, exist_ok=False)
    results = {}
    with TemporaryDirectory(prefix="malleus-compiler-gate-") as temporary:
        for label in ("historical", "candidate"):
            selected = binding[label]
            archive = Path(temporary) / label
            export(selected["commit"], selected["tree"], archive)
            print(f"Running {label}: {selected['commit']}", flush=True)
            raw = run_worker(
                "pytest",
                archive,
                output / f"{label}-pytest.json",
                selected["selectors"],
            )
            # Retain the raw report and continue to independent behavior proof.
            results[label] = {
                "pytest": raw,
                "probe": run_worker("probe", archive, output / f"{label}-probe.json"),
            }
            print(f"{label} raw: {raw['phases']}", flush=True)
        for label in results:
            require_probe_coverage(results[label]["probe"])
            require_exact_run(results[label]["pytest"], binding[label]["expected_run"])
            if (
                results[label]["probe"]["artifact"]["evidence"]["producer"]["sha256"]
                != binding[label]["expected_run"]["producer"]
            ):
                raise GateRefusal(f"{label} probe uses the wrong producer")
        require_parity(
            results["historical"]["probe"],
            results["candidate"]["probe"],
            binding["parity_differences"],
        )
    require_exact_run(gate_code_identity(ROOT), code_identity)
    if BINDING.read_bytes() != binding_bytes:
        raise GateRefusal("Gate binding changed during execution")
    receipt = {
        "status": "BOUNDED_COMPATIBILITY_PASS",
        "raw_candidate_suite_is_green": False,
        "binding_sha256": digest(binding_bytes),
        "gate_code": code_identity,
        "python": sys.version,
        "executable": sys.executable,
        "dependencies": {
            name: metadata.version(name)
            for name in ("pytest", "linkml", "linkml-runtime", "PyYAML", "tzdata")
        },
        "results": {
            label: {
                "commit": binding[label]["commit"],
                "tree": binding[label]["tree"],
                "pytest_sha256": digest(canonical(value["pytest"])),
                "probe_sha256": digest(canonical(value["probe"])),
            }
            for label, value in results.items()
        },
        "non_claims": [
            "Not full-repository CI",
            "Not exact old receipts from a new producer",
            "No action runtime, merge, push or release",
        ],
    }
    (output / "result.json").write_bytes(canonical(receipt) + b"\n")
    print(json.dumps(receipt, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", choices=("pytest", "probe"), help=argparse.SUPPRESS)
    parser.add_argument("--result", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("selectors", nargs="*")
    args = parser.parse_args()
    try:
        if args.worker:
            if args.result is None:
                parser.error("internal worker requires --result")
            if args.worker == "pytest":
                result = pytest_worker(args.selectors)
            else:
                from compiler_compatibility_probe import probe

                result = probe()
                verify_loaded_origins(Path.cwd())
            args.result.write_bytes(canonical(result) + b"\n")
        else:
            if args.output is None or args.selectors or args.result:
                parser.error(
                    "provide only --output pointing to a new evidence directory"
                )
            run_gate(args.output.resolve())
    except (
        GateRefusal,
        OSError,
        subprocess.CalledProcessError,
        ValueError,
        KeyError,
    ) as error:
        parser.exit(1, f"COMPATIBILITY_REFUSED: {error}\n")


if __name__ == "__main__":
    main()

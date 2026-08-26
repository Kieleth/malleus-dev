"""CC-X02 raw bundled-declaration and duplicate measurements."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "contract_compiler_duplicate_scan.py"
PYPROJECT = ROOT / "pyproject.toml"
SCAN = (
    ROOT
    / "conformance"
    / "contract_compiler"
    / "v0"
    / "bundled_declaration_scan.json"
)
EVIDENCE = ROOT / "conformance" / "contract_compiler" / "v0" / "evidence" / "CC-X02.json"

MODULES = {
    "ontology/assent.yaml": {
        "id": "https://malleus.dev/schema/assent",
        "name": "malleus_assent",
        "version": "0.10.0",
        "imports": ["linkml:types", "malleus"],
        "declaration_counts": {"types": 0, "enums": 17, "slots": 232, "classes": 47},
    },
    "ontology/domains/attack.yaml": {
        "id": "https://malleus.dev/schema/attack",
        "name": "attack",
        "version": "0.1.0",
        "imports": ["linkml:types", "malleus"],
        "declaration_counts": {"types": 0, "enums": 5, "slots": 6, "classes": 14},
    },
    "ontology/domains/cyp450.yaml": {
        "id": "https://malleus.dev/schema/cyp450",
        "name": "cyp450",
        "version": "0.1.0",
        "imports": ["linkml:types", "malleus"],
        "declaration_counts": {"types": 0, "enums": 7, "slots": 5, "classes": 10},
    },
    "ontology/domains/ocr.yaml": {
        "id": "https://malleus.dev/schema/ocr",
        "name": "ocr",
        "version": "0.1.0",
        "imports": ["linkml:types", "malleus"],
        "declaration_counts": {"types": 0, "enums": 8, "slots": 42, "classes": 9},
    },
    "ontology/domains/recon.yaml": {
        "id": "https://malleus.dev/schema/recon",
        "name": "recon",
        "version": "0.1.0",
        "imports": ["linkml:types", "malleus"],
        "declaration_counts": {"types": 0, "enums": 9, "slots": 37, "classes": 38},
    },
    "ontology/malleus.yaml": {
        "id": "https://malleus.dev/schema",
        "name": "malleus",
        "version": "0.4.0",
        "imports": ["linkml:types"],
        "declaration_counts": {"types": 1, "enums": 1, "slots": 26, "classes": 9},
    },
}
KINDS = ("types", "enums", "slots", "classes")
EXPECTED_GROUPS = [
    {
        "kind": "slots",
        "symbol": "confidence",
        "occurrence_count": 2,
        "occurrences": [
            {"module_path": "ontology/domains/ocr.yaml", "adopts": {"state": "ABSENT"}},
            {"module_path": "ontology/domains/recon.yaml", "adopts": {"state": "ABSENT"}},
        ],
    },
    {
        "kind": "slots",
        "symbol": "evidence_ids",
        "occurrence_count": 2,
        "occurrences": [
            {"module_path": "ontology/assent.yaml", "adopts": {"state": "ABSENT"}},
            {"module_path": "ontology/domains/recon.yaml", "adopts": {"state": "ABSENT"}},
        ],
    },
    {
        "kind": "slots",
        "symbol": "locator",
        "occurrence_count": 2,
        "occurrences": [
            {"module_path": "ontology/domains/ocr.yaml", "adopts": {"state": "VALUE", "value": True}},
            {"module_path": "ontology/malleus.yaml", "adopts": {"state": "ABSENT"}},
        ],
    },
    {
        "kind": "slots",
        "symbol": "reviewer_id",
        "occurrence_count": 3,
        "occurrences": [
            {"module_path": "ontology/assent.yaml", "adopts": {"state": "VALUE", "value": True}},
            {"module_path": "ontology/domains/ocr.yaml", "adopts": {"state": "VALUE", "value": True}},
            {"module_path": "ontology/malleus.yaml", "adopts": {"state": "ABSENT"}},
        ],
    },
]
FORBIDDEN_POLICY_KEYS = {
    "authorization",
    "classification",
    "comparison",
    "decision",
    "equivalent",
    "policy",
    "preferred",
    "recommendation",
    "resolution",
    "selected",
    "verdict",
    "winner",
}


def _load_runner():
    spec = importlib.util.spec_from_file_location("contract_compiler_duplicate_scan", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot load CC-X02 scanner: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_runner()


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _digest(source: bytes) -> str:
    return "sha256:" + hashlib.sha256(source).hexdigest()


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _copy_inputs(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_bytes(PYPROJECT.read_bytes())
    for relative in MODULES:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return pyproject


def test_scan_has_exact_packaged_modules_and_source_identities():
    document = _read_json(SCAN)

    assert set(document) == {
        "schema",
        "workstream_id",
        "pyproject",
        "modules",
        "declarations",
        "duplicate_groups",
        "cross_kind_repeats",
        "summary",
    }
    assert document["schema"] == "malleus.contract-compiler.bundled-declaration-scan/v1"
    assert document["workstream_id"] == "CC-X02"
    assert document["pyproject"] == {
        "path": "pyproject.toml",
        "source_byte_length": len(PYPROJECT.read_bytes()),
        "source_sha256": _digest(PYPROJECT.read_bytes()),
    }
    assert [item["path"] for item in document["modules"]] == sorted(MODULES)

    for module in document["modules"]:
        expected = MODULES[module["path"]]
        source = (ROOT / module["path"]).read_bytes()
        assert module == {
            "path": module["path"],
            "id": expected["id"],
            "name": expected["name"],
            "version": expected["version"],
            "source_byte_length": len(source),
            "source_sha256": _digest(source),
            "imports": expected["imports"],
            "declaration_counts": expected["declaration_counts"],
            "declaration_count": sum(expected["declaration_counts"].values()),
        }


def test_all_523_declarations_are_raw_lossless_and_canonically_ordered():
    document = _read_json(SCAN)
    expected_raw = {}
    for relative in MODULES:
        loaded = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
        for kind in KINDS:
            for symbol, definition in (loaded.get(kind) or {}).items():
                expected_raw[(kind, symbol, relative)] = definition

    declarations = document["declarations"]
    assert len(declarations) == len(expected_raw) == 523
    assert [
        (KINDS.index(item["kind"]), item["symbol"], item["module"]["path"])
        for item in declarations
    ] == sorted(
        (KINDS.index(kind), symbol, relative)
        for kind, symbol, relative in expected_raw
    )

    seen = set()
    for item in declarations:
        assert set(item) == {"kind", "symbol", "module", "raw_definition", "adopts"}
        assert set(item["module"]) == {
            "path",
            "id",
            "name",
            "version",
            "source_byte_length",
            "source_sha256",
            "imports",
        }
        key = (item["kind"], item["symbol"], item["module"]["path"])
        assert key not in seen
        seen.add(key)
        assert item["raw_definition"] == expected_raw[key]
        json.dumps(item["raw_definition"], allow_nan=False)
        module = next(value for value in document["modules"] if value["path"] == key[2])
        assert item["module"] == {
            name: value for name, value in module.items() if not name.startswith("declaration")
        }
    assert seen == set(expected_raw)


def test_duplicate_groups_are_complete_same_kind_observations_only():
    document = _read_json(SCAN)

    assert document["duplicate_groups"] == EXPECTED_GROUPS
    assert document["cross_kind_repeats"] == []
    assert document["summary"] == {
        "module_count": 6,
        "declaration_count": 523,
        "duplicate_group_count": 4,
        "duplicate_occurrence_count": 9,
        "adopts_value_occurrence_count": 3,
        "cross_kind_repeat_count": 0,
    }

    grouped = {
        (group["kind"], group["symbol"]): {
            occurrence["module_path"] for occurrence in group["occurrences"]
        }
        for group in document["duplicate_groups"]
    }
    expected = {}
    for declaration in document["declarations"]:
        expected.setdefault((declaration["kind"], declaration["symbol"]), set()).add(
            declaration["module"]["path"]
        )
    assert grouped == {key: paths for key, paths in expected.items() if len(paths) > 1}


def test_adopts_retains_absent_null_false_and_true_without_coercion(tmp_path):
    source = tmp_path / "states.yaml"
    source.write_text(
        """\
id: https://example.test/states
name: states
version: 1.0.0
imports: [linkml:types]
types: {}
enums: {}
slots:
  absent: {}
  "null":
    annotations:
      adopts:
  "false":
    annotations:
      adopts: false
  "true":
    annotations:
      adopts: true
classes: {}
""",
        encoding="utf-8",
    )

    _, declarations = runner.scan_module(source, tmp_path)
    assert {item["symbol"]: item["adopts"] for item in declarations} == {
        "absent": {"state": "ABSENT"},
        "null": {"state": "NULL"},
        "false": {"state": "VALUE", "value": False},
        "true": {"state": "VALUE", "value": True},
    }
    assert {item["symbol"]: item["raw_definition"] for item in declarations} == {
        "absent": {},
        "null": {"annotations": {"adopts": None}},
        "false": {"annotations": {"adopts": False}},
        "true": {"annotations": {"adopts": True}},
    }


def test_duplicate_yaml_keys_fail_loudly(tmp_path):
    source = tmp_path / "duplicate.yaml"
    source.write_text(
        """\
id: https://example.test/duplicate
name: duplicate
version: 1.0.0
imports: []
slots:
  value: {}
  value:
    required: true
""",
        encoding="utf-8",
    )

    with pytest.raises(runner.DuplicateScanError, match="Duplicate YAML key 'value'"):
        runner.load_yaml_module(source)


def test_render_is_deterministic_and_matches_retained_bytes():
    first = runner.render_scan(PYPROJECT)
    second = runner.render_scan(PYPROJECT)

    assert first == second == SCAN.read_bytes()
    assert json.loads(first) == _read_json(SCAN)


def test_check_rejects_mutated_output_and_mutated_source(tmp_path):
    changed = deepcopy(_read_json(SCAN))
    changed["declarations"][0]["raw_definition"]["mutated"] = True
    changed_output = tmp_path / "changed.json"
    changed_output.write_bytes(runner.canonical_json(changed))
    with pytest.raises(runner.DuplicateScanError, match="do not match"):
        runner.check_scan(PYPROJECT, changed_output)

    copied_pyproject = _copy_inputs(tmp_path / "source-change")
    copied_output = tmp_path / "copied.json"
    copied_output.write_bytes(runner.render_scan(copied_pyproject))
    changed_source = copied_pyproject.parent / "ontology" / "malleus.yaml"
    changed_source.write_text(
        changed_source.read_text(encoding="utf-8") + "\n# changed bytes\n",
        encoding="utf-8",
    )
    with pytest.raises(runner.DuplicateScanError, match="do not match"):
        runner.check_scan(copied_pyproject, copied_output)


def test_cli_checks_without_rewriting_retained_bytes():
    before = SCAN.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "CC-X02 bundled declaration scan matches retained bytes\n"
    assert SCAN.read_bytes() == before


def test_scanner_has_no_semantic_engine_or_regex_import_path():
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    imported_roots = set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Name):
            names.add(node.id)

    assert imported_roots.isdisjoint({"linkml", "linkml_runtime", "malleus", "re"})
    assert names.isdisjoint({"OntologyRegistry", "SchemaView"})


def test_scan_contains_no_policy_or_classification_fields():
    document = _read_json(SCAN)
    for mapping in _walk(document):
        assert FORBIDDEN_POLICY_KEYS.isdisjoint(mapping)


def test_evidence_binds_only_the_measurement_and_implementation_bytes():
    evidence = _read_json(EVIDENCE)
    assert set(evidence) == {
        "schema",
        "workstream_id",
        "recorded_at",
        "base_commit",
        "artifacts",
        "checks",
        "limitations",
    }
    assert evidence["schema"] == "malleus.contract-compiler.verification-report/v1"
    assert evidence["workstream_id"] == "CC-X02"
    assert evidence["base_commit"] == "61f488ded1870fbfbf2fbdecc901baf9c1c503dd"
    assert [item["path"] for item in evidence["artifacts"]] == [
        "conformance/contract_compiler/v0/bundled_declaration_scan.json",
        "scripts/contract_compiler_duplicate_scan.py",
        "tests/test_contract_compiler_duplicate_scan.py",
    ]
    assert evidence["checks"]
    assert all(item["result"] == "PASS" for item in evidence["checks"])
    assert evidence["limitations"]
    for artifact in evidence["artifacts"]:
        source = (ROOT / artifact["path"]).read_bytes()
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == _digest(source)

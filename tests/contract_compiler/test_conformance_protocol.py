"""Fixed validation for the CC-010 three-corpus protocol."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


REPOSITORY = Path(__file__).resolve().parents[2]
PROTOCOL_ROOT = REPOSITORY / "conformance" / "contract_kernel" / "v0"
SCHEMA_PATH = PROTOCOL_ROOT / "corpus.schema.json"
CORPUS_PATH = PROTOCOL_ROOT / "corpus.json"
MATRIX_PATH = PROTOCOL_ROOT / "stage-matrix.json"
CHECKSUMS_PATH = PROTOCOL_ROOT / "checksums.json"
GUIDE_PATH = REPOSITORY / "docs" / "contract_compiler" / "conformance_protocol.md"
INTEGRATION_PATH = REPOSITORY / "design" / "contract_compiler" / "integration.json"

CORPUS_IDS = ("themed_vertical", "feature_isolation", "neutral_domain")
CORPUS_ROOTS = ("themed_fixture", "feature_cases", "neutral_domain")
STAGES = tuple(f"CC-R{index:02d}" for index in range(1, 9))
PROTOCOL_FILES = (
    "conformance/contract_kernel/v0/corpus.json",
    "conformance/contract_kernel/v0/corpus.schema.json",
    "conformance/contract_kernel/v0/stage-matrix.json",
)
REQUIREMENTS_PATH = (
    "conformance/contract_kernel/v0/requirements/scenarios.json"
)
LAYOUT = {
    "themed_vertical": {
        "root": "themed_fixture",
        "input_prefixes": [
            "conformance/contract_kernel/v0/themed_fixture/direct-input",
            "conformance/contract_kernel/v0/themed_fixture/sources",
            "conformance/contract_kernel/v0/themed_fixture/traces/input",
        ],
        "oracle_prefixes": [
            "conformance/contract_kernel/v0/themed_fixture/oracle",
            "conformance/contract_kernel/v0/themed_fixture/traces/oracle",
        ],
    },
    "feature_isolation": {
        "root": "feature_cases",
        "input_prefixes": [
            "conformance/contract_kernel/v0/feature_cases/inputs"
        ],
        "oracle_prefixes": [
            "conformance/contract_kernel/v0/feature_cases/oracle"
        ],
    },
    "neutral_domain": {
        "root": "neutral_domain",
        "input_prefixes": [
            "conformance/contract_kernel/v0/neutral_domain/sources",
            "conformance/contract_kernel/v0/neutral_domain/traces/input",
        ],
        "oracle_prefixes": [
            "conformance/contract_kernel/v0/neutral_domain/oracle",
            "conformance/contract_kernel/v0/neutral_domain/traces/oracle",
        ],
    },
}
STAGE_TESTS = {
    "CC-R01": ["AT-001"],
    "CC-R02": ["AT-002"],
    "CC-R03": ["AT-003"],
    "CC-R04": ["AT-004", "AT-005", "AT-006"],
    "CC-R05": ["AT-007"],
    "CC-R06": ["AT-008", "AT-008a", "AT-010", "AT-011", "AT-012"],
    "CC-R07": ["AT-009"],
    "CC-R08": [
        "AT-001",
        "AT-002",
        "AT-003",
        "AT-004",
        "AT-005",
        "AT-006",
        "AT-007",
        "AT-008",
        "AT-008a",
        "AT-009",
        "AT-010",
        "AT-011",
        "AT-012",
    ],
}
OWNER_PAIRS = {
    frozenset(("CC-011", "CC-012")),
    frozenset(("CC-013", "CC-014")),
    frozenset(("CC-015", "CC-016")),
    frozenset(("CC-019", "CC-020")),
}
HEX = frozenset("0123456789abcdef")
IDENTIFIER_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
)


class ProtocolError(ValueError):
    """The corpus protocol or its raw stored members is invalid."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ProtocolError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ProtocolError(f"nonfinite JSON number: {value}")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise ProtocolError(f"{path}: root must be an object")
    return value


def _validate_schema(document: dict[str, Any], schema: dict[str, Any]) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        raise errors[0]


def _identifier(value: str, context: str) -> None:
    if not value or not value.isascii() or any(
        character not in IDENTIFIER_CHARACTERS for character in value
    ):
        raise ProtocolError(f"{context}: invalid identifier {value!r}")


def _path(value: str, context: str) -> PurePosixPath:
    parsed = PurePosixPath(value)
    if (
        not value
        or parsed.is_absolute()
        or parsed.as_posix() != value
        or "." in parsed.parts
        or ".." in parsed.parts
        or "\\" in value
    ):
        raise ProtocolError(f"{context}: unsafe repository-relative POSIX path")
    return parsed


def _under_any(value: str, roots: list[str], context: str) -> None:
    path = _path(value, context)
    bases = [_path(root, f"{context} root") for root in roots]
    if not any(path != base and path.is_relative_to(base) for base in bases):
        raise ProtocolError(f"{context}: path is outside its allowed prefixes")


def _digest(value: str, context: str) -> None:
    prefix = "sha256:"
    body = value.removeprefix(prefix)
    if not value.startswith(prefix) or len(body) != 64 or any(
        character not in HEX for character in body
    ):
        raise ProtocolError(f"{context}: invalid SHA-256 digest")


def _members(corpus: dict[str, Any]) -> set[str]:
    paths: list[str] = list(corpus["protocol_files"])
    for path in paths:
        _path(path, "protocol control")
    requirements = corpus["shared_requirements"]
    _path(requirements["path"], "shared requirements")
    if requirements["state"] == "LISTED":
        paths.append(requirements["path"])
    any_cases = any(item["cases"] for item in corpus["corpora"])
    if any_cases and requirements["state"] != "LISTED":
        raise ProtocolError("cases require listed shared requirements")
    for item in corpus["corpora"]:
        for prefix in (*item["input_prefixes"], *item["oracle_prefixes"]):
            _path(prefix, f"{item['corpus_id']} prefix")
        case_ids = [case["case_id"] for case in item["cases"]]
        if case_ids != sorted(case_ids) or len(case_ids) != len(set(case_ids)):
            raise ProtocolError(
                f"{item['corpus_id']}: case IDs must be unique and sorted"
            )
        for case in item["cases"]:
            _identifier(case["case_id"], f"{item['corpus_id']} case_id")
            for field in ("scenario_ids", "input_files", "oracle_files"):
                if case[field] != sorted(case[field]) or len(case[field]) != len(
                    set(case[field])
                ):
                    raise ProtocolError(
                        f"{case['case_id']}: {field} must be unique and sorted"
                    )
            for scenario_id in case["scenario_ids"]:
                _identifier(scenario_id, f"{case['case_id']} scenario_id")
            for path in case["input_files"]:
                _under_any(
                    path, item["input_prefixes"], f"{case['case_id']} input"
                )
                paths.append(path)
            for path in case["oracle_files"]:
                _under_any(
                    path, item["oracle_prefixes"], f"{case['case_id']} oracle"
                )
                paths.append(path)
    if len(paths) != len(set(paths)):
        raise ProtocolError("normative membership contains a duplicate path")
    return set(paths)


def _validate_checksums(
    repository: Path,
    corpus: dict[str, Any],
    checksums: dict[str, Any],
) -> None:
    members = _members(corpus)
    records = {item["path"]: item for item in checksums["files"]}
    if len(records) != len(checksums["files"]):
        raise ProtocolError("checksum manifest contains a duplicate path")
    if set(records) != members:
        raise ProtocolError("membership and checksum path sets differ")
    if [item["path"] for item in checksums["files"]] != sorted(records):
        raise ProtocolError("checksum records are not sorted")
    for path, record in records.items():
        _path(path, "checksum path")
        _digest(record["sha256"], path)
        candidate = repository / path
        try:
            resolved = candidate.resolve(strict=True)
        except OSError as error:
            raise ProtocolError(f"{path}: normative member is unreadable") from error
        if (
            candidate.is_symlink()
            or not candidate.is_file()
            or not resolved.is_relative_to(repository.resolve())
        ):
            raise ProtocolError(f"{path}: normative member is not a regular in-repo file")
        source = candidate.read_bytes()
        if record["byte_length"] != len(source):
            raise ProtocolError(f"{path}: byte length mismatch")
        actual = "sha256:" + hashlib.sha256(source).hexdigest()
        if record["sha256"] != actual:
            raise ProtocolError(f"{path}: SHA-256 mismatch")


def _documents() -> tuple[dict[str, Any], ...]:
    schema = _load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    corpus = _load_json(CORPUS_PATH)
    matrix = _load_json(MATRIX_PATH)
    checksums = _load_json(CHECKSUMS_PATH)
    for document in (corpus, matrix, checksums):
        _validate_schema(document, schema)
    return schema, corpus, matrix, checksums


def _validate_requirements(document: dict[str, Any]) -> set[str]:
    scenario_ids = [item["scenario_id"] for item in document["scenarios"]]
    if scenario_ids != sorted(scenario_ids) or len(scenario_ids) != len(
        set(scenario_ids)
    ):
        raise ProtocolError("scenario IDs must be unique and sorted")
    requirement_ids: list[str] = []
    for scenario in document["scenarios"]:
        _identifier(scenario["scenario_id"], "scenario_id")
        ids = [item["requirement_id"] for item in scenario["requirements"]]
        if ids != sorted(ids):
            raise ProtocolError(
                f"{scenario['scenario_id']}: requirement IDs are not sorted"
            )
        for requirement in scenario["requirements"]:
            _identifier(requirement["requirement_id"], "requirement_id")
            if requirement["decision_anchors"] != sorted(
                requirement["decision_anchors"]
            ) or len(requirement["decision_anchors"]) != len(
                set(requirement["decision_anchors"])
            ):
                raise ProtocolError(
                    f"{requirement['requirement_id']}: decision anchors must be unique and sorted"
                )
            for anchor in requirement["decision_anchors"]:
                _identifier(anchor, "decision anchor")
        requirement_ids.extend(ids)
    if len(requirement_ids) != len(set(requirement_ids)):
        raise ProtocolError("requirement IDs must be globally unique")
    return set(scenario_ids)


def _validate_requirements_member(
    repository: Path,
    schema: dict[str, Any],
    corpus: dict[str, Any],
) -> None:
    requirements = corpus["shared_requirements"]
    if requirements["state"] == "OPTIONAL_UNTIL_LISTED":
        return
    document = _load_json(repository / requirements["path"])
    _validate_schema(document, schema)
    scenario_ids = _validate_requirements(document)
    referenced = {
        scenario_id
        for item in corpus["corpora"]
        for case in item["cases"]
        for scenario_id in case["scenario_ids"]
    }
    if not referenced <= scenario_ids:
        raise ProtocolError("case membership references an unknown scenario")


def test_protocol_bootstrap_is_closed_empty_and_valid() -> None:
    schema, corpus, matrix, checksums = _documents()

    assert [item["corpus_id"] for item in corpus["corpora"]] == list(CORPUS_IDS)
    assert [item["root"] for item in corpus["corpora"]] == list(CORPUS_ROOTS)
    assert corpus["protocol_files"] == list(PROTOCOL_FILES)
    assert corpus["shared_requirements"]["path"] == REQUIREMENTS_PATH
    assert corpus["shared_requirements"]["schema"] == (
        "malleus.contract-kernel.scenarios/v0"
    )
    if corpus["shared_requirements"]["state"] == "OPTIONAL_UNTIL_LISTED":
        assert all(item["cases"] == [] for item in corpus["corpora"])
    assert [item["stage"] for item in matrix["stages"]] == list(STAGES)
    assert all(item["corpora"] == list(CORPUS_IDS) for item in matrix["stages"])
    assert {
        item["stage"]: item["assigned_acceptance_tests"]
        for item in matrix["stages"]
    } == STAGE_TESTS
    assert matrix["cumulative_rule"] == "EACH_STAGE_RERUNS_PRIOR_SLICES"
    assert matrix["whole_pipeline_obligations"] == [
        "CURRENT_BUNDLED_ONTOLOGIES",
        "MUTATION_ADEQUACY",
    ]
    assert not any(key == "default" for key in _all_keys(schema))
    _validate_requirements_member(REPOSITORY, schema, corpus)
    _validate_checksums(REPOSITORY, corpus, checksums)


def _all_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [
            key
            for name, item in value.items()
            for key in (name, *_all_keys(item))
        ]
    if isinstance(value, list):
        return [key for item in value for key in _all_keys(item)]
    return []


def test_source_and_oracle_ownership_comes_from_integration() -> None:
    integration = _load_json(INTEGRATION_PATH)
    pairs = {
        frozenset((item["left"], item["right"]))
        for item in integration["owner_separations"]
    }
    assert OWNER_PAIRS <= pairs

    _, corpus, _, _ = _documents()
    forbidden_authority_fields = {
        "owner",
        "owner_id",
        "source_owner",
        "input_owner",
        "oracle_owner",
        "workstream",
        "workstream_id",
    }
    assert forbidden_authority_fields.isdisjoint(_all_keys(corpus))


def test_exact_layout_is_disjoint_and_below_contract_kernel_v0() -> None:
    _, corpus, _, _ = _documents()
    observed = {
        item["corpus_id"]: {
            "root": item["root"],
            "input_prefixes": item["input_prefixes"],
            "oracle_prefixes": item["oracle_prefixes"],
        }
        for item in corpus["corpora"]
    }
    assert observed == LAYOUT
    prefixes = [
        prefix
        for item in observed.values()
        for prefix in (*item["input_prefixes"], *item["oracle_prefixes"])
    ]
    assert len(prefixes) == len(set(prefixes))
    protocol_root = PurePosixPath("conformance/contract_kernel/v0")
    assert all(
        _path(prefix, "layout prefix").is_relative_to(protocol_root)
        for prefix in prefixes
    )


def test_internal_guide_keeps_the_kiss_expansion_contract() -> None:
    guide = GUIDE_PATH.read_text(encoding="utf-8")
    required = (
        "Why exactly three corpora",
        "themed_vertical",
        "feature_isolation",
        "neutral_domain",
        "written by hand",
        "integration owner alone",
        "Expanding a corpus",
        "checksums.json` excludes itself",
        "expected-delta manifest",
        "Sphinx wiring is deferred",
    )
    assert all(text in guide for text in required)


def test_schema_refuses_missing_unknown_identity_order_and_addition_drift() -> None:
    schema, corpus, matrix, checksums = _documents()

    mutations: list[dict[str, Any]] = []
    missing = copy.deepcopy(corpus)
    del missing["protocol"]
    mutations.append(missing)
    unknown = copy.deepcopy(corpus)
    unknown["implicit_default"] = True
    mutations.append(unknown)
    identity = copy.deepcopy(corpus)
    identity["corpora"][0]["corpus_id"] = "other"
    mutations.append(identity)
    order = copy.deepcopy(corpus)
    order["corpora"][0], order["corpora"][1] = (
        order["corpora"][1],
        order["corpora"][0],
    )
    mutations.append(order)
    addition = copy.deepcopy(corpus)
    addition["corpora"].append(copy.deepcopy(addition["corpora"][0]))
    mutations.append(addition)
    matrix_order = copy.deepcopy(matrix)
    matrix_order["stages"][0], matrix_order["stages"][1] = (
        matrix_order["stages"][1],
        matrix_order["stages"][0],
    )
    mutations.append(matrix_order)
    checksum_unknown = copy.deepcopy(checksums)
    checksum_unknown["files_perhaps"] = []
    mutations.append(checksum_unknown)

    for mutation in mutations:
        with pytest.raises(ValidationError):
            _validate_schema(mutation, schema)


def test_schema_discriminates_exactly_four_document_kinds() -> None:
    schema, corpus, matrix, checksums = _documents()
    assert schema["oneOf"] == [
        {"$ref": "#/$defs/corpusManifest"},
        {"$ref": "#/$defs/stageMatrix"},
        {"$ref": "#/$defs/checksumManifest"},
        {"$ref": "#/$defs/scenarioRequirements"},
    ]
    requirements = {
        "schema": "malleus.contract-kernel.scenarios/v0",
        "scenarios": [
            {
                "requirements": [
                    {
                        "decision_anchors": ["OD-005"],
                        "kind": "POSITIVE",
                        "requirement_id": "example-positive",
                        "statement": "Exact obligation.",
                    }
                ],
                "scenario_id": "example",
            }
        ],
    }
    definitions = (
        "corpusManifest",
        "stageMatrix",
        "checksumManifest",
        "scenarioRequirements",
    )

    def branch_count(document: dict[str, Any]) -> int:
        return sum(
            not tuple(
                Draft202012Validator(
                    {"$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]}
                ).iter_errors(document)
            )
            for definition in definitions
        )

    for document in (corpus, matrix, checksums, requirements):
        assert branch_count(document) == 1
        wrong = copy.deepcopy(document)
        wrong["schema"] = "malleus.contract-kernel.unknown/v0"
        assert branch_count(wrong) == 0

    hybrid = copy.deepcopy(corpus)
    hybrid.update({"algorithm": "sha256", "files": []})
    assert branch_count(hybrid) == 0


def test_membership_refuses_nondeterministic_list_order() -> None:
    _, corpus, _, _ = _documents()
    cases = [
        {
            "case_id": "case-a",
            "input_files": [
                "conformance/contract_kernel/v0/feature_cases/inputs/a.json",
                "conformance/contract_kernel/v0/feature_cases/inputs/b.json",
            ],
            "oracle_files": [
                "conformance/contract_kernel/v0/feature_cases/oracle/a.json",
                "conformance/contract_kernel/v0/feature_cases/oracle/b.json",
            ],
            "scenario_ids": ["scenario-a", "scenario-b"],
        },
        {
            "case_id": "case-b",
            "input_files": [
                "conformance/contract_kernel/v0/feature_cases/inputs/c.json"
            ],
            "oracle_files": [
                "conformance/contract_kernel/v0/feature_cases/oracle/c.json"
            ],
            "scenario_ids": ["scenario-c"],
        },
    ]
    mutations: list[list[dict[str, Any]]] = []
    for field in ("scenario_ids", "input_files", "oracle_files"):
        mutation = copy.deepcopy(cases)
        mutation[0][field].sort(reverse=True)
        mutations.append(mutation)
    mutations.append(list(reversed(copy.deepcopy(cases))))
    duplicate_id = copy.deepcopy(cases)
    duplicate_id[1]["case_id"] = "case-a"
    mutations.append(duplicate_id)

    for mutation in mutations:
        populated = copy.deepcopy(corpus)
        populated["shared_requirements"]["state"] = "LISTED"
        populated["corpora"][1]["cases"] = mutation
        with pytest.raises(ProtocolError, match="sorted"):
            _members(populated)


@pytest.mark.parametrize(
    "raw",
    (
        "{",
        '{"schema":"x","schema":"y"}',
        '{"value":NaN}',
        '{"value":Infinity}',
    ),
)
def test_json_loading_refuses_malformed_duplicate_and_nonfinite(
    tmp_path: Path, raw: str
) -> None:
    path = tmp_path / "document.json"
    path.write_text(raw, encoding="utf-8")
    with pytest.raises(ProtocolError):
        _load_json(path)


@pytest.mark.parametrize(
    "path",
    (
        "/absolute.json",
        "../escape.json",
        "feature_cases/inputs/../oracle/value.json",
        "feature_cases//inputs/value.json",
        "feature_cases\\inputs\\value.json",
        "conformance/contract_kernel/v0/neutral_domain/sources/cross.json",
    ),
)
def test_membership_refuses_bad_or_cross_root_paths(path: str) -> None:
    schema, corpus, _, _ = _documents()
    populated = copy.deepcopy(corpus)
    populated["shared_requirements"]["state"] = "LISTED"
    populated["corpora"][1]["cases"] = [
        {
            "case_id": "case-1",
            "input_files": [
                "conformance/contract_kernel/v0/feature_cases/inputs/case-1.json"
            ],
            "oracle_files": [
                "conformance/contract_kernel/v0/feature_cases/oracle/case-1.json"
            ],
            "scenario_ids": ["scenario-1"],
        }
    ]
    _validate_schema(populated, schema)
    _members(populated)
    populated["corpora"][1]["cases"][0]["input_files"] = [path]
    with pytest.raises(ProtocolError):
        _members(populated)


def test_declared_direct_and_trace_inputs_are_valid_but_cross_role_refuses() -> None:
    schema, corpus, _, _ = _documents()
    populated = copy.deepcopy(corpus)
    populated["shared_requirements"]["state"] = "LISTED"
    case = {
        "case_id": "planned-paths",
        "input_files": [
            "conformance/contract_kernel/v0/themed_fixture/direct-input/facts.json",
            "conformance/contract_kernel/v0/themed_fixture/traces/input/trace.json",
        ],
        "oracle_files": [
            "conformance/contract_kernel/v0/themed_fixture/traces/oracle/trace.json"
        ],
        "scenario_ids": ["planned-paths"],
    }
    populated["corpora"][0]["cases"] = [case]
    _validate_schema(populated, schema)
    _members(populated)

    crossed = copy.deepcopy(populated)
    crossed["corpora"][0]["cases"][0]["input_files"] = [
        "conformance/contract_kernel/v0/themed_fixture/oracle/wrong-role.json"
    ]
    with pytest.raises(ProtocolError, match="allowed prefixes"):
        _members(crossed)


def test_requirements_grammar_is_frozen_without_creating_content() -> None:
    schema, _, _, _ = _documents()
    valid = {
        "schema": "malleus.contract-kernel.scenarios/v0",
        "scenarios": [
            {
                "scenario_id": "example",
                "requirements": [
                    {
                        "decision_anchors": ["OD-005"],
                        "kind": "POSITIVE",
                        "requirement_id": "example-positive",
                        "statement": "One exact semantic obligation.",
                    }
                ],
            }
        ],
    }
    _validate_schema(valid, schema)
    assert _validate_requirements(valid) == {"example"}

    unknown = copy.deepcopy(valid)
    unknown["scenarios"][0]["expected"] = "not owned here"
    with pytest.raises(ValidationError):
        _validate_schema(unknown, schema)

    second = copy.deepcopy(valid["scenarios"][0])
    second["scenario_id"] = "another"
    second["requirements"][0]["requirement_id"] = "another-positive"
    reordered_scenarios = copy.deepcopy(valid)
    reordered_scenarios["scenarios"] = [valid["scenarios"][0], second]
    with pytest.raises(ProtocolError, match="scenario IDs"):
        _validate_requirements(reordered_scenarios)

    bad_requirement_order = copy.deepcopy(valid)
    later = copy.deepcopy(bad_requirement_order["scenarios"][0]["requirements"][0])
    later["requirement_id"] = "a-first"
    bad_requirement_order["scenarios"][0]["requirements"].append(later)
    with pytest.raises(ProtocolError, match="requirement IDs"):
        _validate_requirements(bad_requirement_order)

    bad_anchor_order = copy.deepcopy(valid)
    bad_anchor_order["scenarios"][0]["requirements"][0]["decision_anchors"] = [
        "OD-006",
        "OD-005",
    ]
    with pytest.raises(ProtocolError, match="decision anchors"):
        _validate_requirements(bad_anchor_order)

    duplicate_requirement = copy.deepcopy(valid)
    second_scenario = copy.deepcopy(duplicate_requirement["scenarios"][0])
    second_scenario["scenario_id"] = "second"
    duplicate_requirement["scenarios"].append(second_scenario)
    with pytest.raises(ProtocolError, match="globally unique"):
        _validate_requirements(duplicate_requirement)


def test_membership_checksum_bijection_and_raw_byte_integrity(tmp_path: Path) -> None:
    schema, corpus, _, checksums = _documents()
    controls: list[Path] = []
    for path in PROTOCOL_FILES:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPOSITORY / path).read_bytes())
        controls.append(target)
    path = "conformance/contract_kernel/v0/feature_cases/inputs/case-1.json"
    oracle_path = (
        "conformance/contract_kernel/v0/feature_cases/oracle/case-1.json"
    )
    requirements_path = tmp_path / REQUIREMENTS_PATH
    requirements_path.parent.mkdir(parents=True)
    requirements_path.write_bytes(
        b'{"schema":"malleus.contract-kernel.scenarios/v0","scenarios":['
        b'{"requirements":[{"decision_anchors":["OD-005"],'
        b'"kind":"POSITIVE","requirement_id":"scenario-1-positive",'
        b'"statement":"Exact obligation."}],"scenario_id":"scenario-1"}]}'
    )
    stored = tmp_path / path
    stored.parent.mkdir(parents=True)
    stored.write_bytes(b'{"value":"exact raw bytes"}\n')
    oracle = tmp_path / oracle_path
    oracle.parent.mkdir(parents=True)
    oracle.write_bytes(b'{"expected":"hand authored"}\n')

    populated = copy.deepcopy(corpus)
    populated["shared_requirements"]["state"] = "LISTED"
    populated["corpora"][1]["cases"] = [
        {
            "case_id": "case-1",
            "input_files": [path],
            "oracle_files": [oracle_path],
            "scenario_ids": ["scenario-1"],
        }
    ]
    populated_checksums = copy.deepcopy(checksums)
    populated_checksums["files"] = [
        {
            "byte_length": len(member.read_bytes()),
            "path": member.relative_to(tmp_path).as_posix(),
            "sha256": "sha256:" + hashlib.sha256(member.read_bytes()).hexdigest(),
        }
        for member in sorted((*controls, requirements_path, stored, oracle))
    ]
    _validate_schema(populated, schema)
    _validate_schema(populated_checksums, schema)
    _validate_requirements_member(tmp_path, schema, populated)
    _validate_checksums(tmp_path, populated, populated_checksums)

    reordered = copy.deepcopy(populated_checksums)
    reordered["files"].reverse()
    with pytest.raises(ProtocolError, match="not sorted"):
        _validate_checksums(tmp_path, populated, reordered)

    missing = copy.deepcopy(populated_checksums)
    missing["files"] = []
    with pytest.raises(ProtocolError, match="path sets differ"):
        _validate_checksums(tmp_path, populated, missing)

    duplicate = copy.deepcopy(populated_checksums)
    duplicate["files"].append(copy.deepcopy(duplicate["files"][0]))
    with pytest.raises(ProtocolError, match="duplicate path"):
        _validate_checksums(tmp_path, populated, duplicate)

    bad_size = copy.deepcopy(populated_checksums)
    stored_record = next(item for item in bad_size["files"] if item["path"] == path)
    stored_record["byte_length"] += 1
    with pytest.raises(ProtocolError, match="byte length mismatch"):
        _validate_checksums(tmp_path, populated, bad_size)

    bad_digest = copy.deepcopy(populated_checksums)
    stored_record = next(item for item in bad_digest["files"] if item["path"] == path)
    stored_record["sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ProtocolError, match="SHA-256 mismatch"):
        _validate_checksums(tmp_path, populated, bad_digest)

    stored.write_bytes(b'{"value":"Exact raw bytes"}\n')
    with pytest.raises(ProtocolError, match="SHA-256 mismatch"):
        _validate_checksums(tmp_path, populated, populated_checksums)

    stored.write_bytes(b'{"value":"exact raw bytes"}\n')
    stored.write_bytes(stored.read_bytes() + b"mutation")
    with pytest.raises(ProtocolError, match="byte length mismatch"):
        _validate_checksums(tmp_path, populated, populated_checksums)

    original = next(
        item for item in populated_checksums["files"] if item["path"] == path
    )
    stored.write_bytes(b'{"value":"exact raw bytes"}\n')
    assert len(stored.read_bytes()) == original["byte_length"]
    stored.unlink()
    stored.symlink_to(oracle)
    with pytest.raises(ProtocolError, match="not a regular in-repo file"):
        _validate_checksums(tmp_path, populated, populated_checksums)


def test_checksum_manifest_excludes_itself() -> None:
    _, corpus, _, checksums = _documents()
    assert CHECKSUMS_PATH.relative_to(REPOSITORY).as_posix() not in _members(corpus)
    checksum_path = CHECKSUMS_PATH.relative_to(REPOSITORY).as_posix()
    assert all(item["path"] != checksum_path for item in checksums["files"])

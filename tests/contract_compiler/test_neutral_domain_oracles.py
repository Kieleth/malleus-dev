"""Fixed private answer-key checks for the Neutral Greenhouse fixture."""

from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import pytest


REPOSITORY = Path(__file__).resolve().parents[2]
KERNEL = REPOSITORY / "conformance" / "contract_kernel" / "v0"
SOURCE_ROOT = KERNEL / "neutral_domain" / "sources" / "greenhouse"
OPERATION_ROOT = KERNEL / "neutral_domain" / "traces" / "input"
ORACLE_ROOT = KERNEL / "neutral_domain" / "oracle"
TRACE_ORACLE_ROOT = KERNEL / "neutral_domain" / "traces" / "oracle"
ORACLE_PATH = ORACLE_ROOT / "greenhouse.json"
TRACE_ORACLE_PATH = TRACE_ORACLE_ROOT / "compile-source-outcomes.json"

GREENHOUSE = "https://example.malleus.dev/greenhouse"
CONTRACT_FACTS = "https://malleus.dev/contract-facts/"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
RDFS_SUBCLASS = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
LOWERCASE_HEX = frozenset("0123456789abcdef")
REFUSE = {"outcome": "REFUSE"}

CONFIGURATION = {
    "artifact_media_type": "TEST_ONLY_PRIVATE_JSON",
    "artifact_role": "CONFORMANCE_FIXTURE",
    "capabilities": "TEST_ONLY_REPOSITORY_FILE_NETWORK_DENIED_V0",
    "profile": "TEST_ONLY_LINKML_V0_PROFILE",
    "public_contract": False,
    "resolver": "TEST_ONLY_STRICT_MALLEUS_RESOLVER_V0",
    "source_media_type": "TEST_ONLY_JSON_SHAPED_YAML",
}

SOURCE_DESCRIPTORS = (
    (
        "baseline.yaml",
        1456,
        "3bb5b580021b2f5ca6c0113a3ef63d047ce2dcf63e846ffc6fa4fe03b87fee98",
    ),
    (
        "explicit-defaults.yaml",
        1900,
        "f842338536f01b581618cf51eeca03668bcb8ff7861b36f872870889158201b5",
    ),
    (
        "numeric-equivalent.yaml",
        1459,
        "80145c298d708d955cb3ee521bf7953feed287d1b97aab28b348ad63cd8b3d3e",
    ),
    (
        "presentation-only.yaml",
        1477,
        "c389a0add25ca17516663abf92d4370e0b29efe14b522250b2056bc221c45c65",
    ),
    (
        "reordered.yaml",
        1456,
        "b909bee4789dce0c0b25e0987cfc0f0fe67569138e482f25a3cb804e1ce8b877",
    ),
    (
        "semantic-change.yaml",
        1456,
        "86d7ab9958d2bc0781a39807c428c837d18ef6c35b31470c0370d6d28359d404",
    ),
)

BASELINE_SOURCE = (
    "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/baseline.yaml"
)
SOURCE_PATHS = {
    name.removesuffix(".yaml"): (
        "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse/" + name
    )
    for name, _, _ in SOURCE_DESCRIPTORS
}

SAMPLE = f"{GREENHOUSE}/Sample"
TRACEABLE = f"{GREENHOUSE}/Traceable"
OBSERVATION = f"{GREENHOUSE}/Observation"
CELSIUS = f"{GREENHOUSE}/Celsius"
PLANT_STATE = f"{GREENHOUSE}/PlantState"
SPECIMEN_ID = f"{GREENHOUSE}/specimen_id"
TEMPERATURE = f"{GREENHOUSE}/temperature"
STATE = f"{GREENHOUSE}/state"
NOTE = f"{GREENHOUSE}/Observation/note"

SPECIMEN_USE = (
    "urn:malleus:contract-structure:slot-use:v0:sha256:"
    "61e084e16ea3ef4e89d061a8a95f843962b6dd02e9a7871718da2f89d5d90591"
)
TEMPERATURE_USE = (
    "urn:malleus:contract-structure:slot-use:v0:sha256:"
    "cc51d84fdfbb1f9f6bba0c2fe30b13b98fd3001d38589f83506d2f238c94675d"
)
STATE_USE = (
    "urn:malleus:contract-structure:slot-use:v0:sha256:"
    "e33dfa2fb125a065137ac3d88b49c5742b0a29ed69e5def656b467f4e0768dd0"
)
NOTE_USE = (
    "urn:malleus:contract-structure:slot-use:v0:sha256:"
    "1bfb1cf705602cde0a82f40465a418febaab02d24fa9d666ed833940fead2c0a"
)
EXACTLY_ONE_GROUP = (
    "urn:malleus:contract-structure:exactly-one-group:v0:sha256:"
    "9879af547ef8a1370a50d60d075dae1b68a63cf8a378c62b9118fa3f9d6aa574"
)
STATE_ALTERNATIVE_DIGEST = (
    "sha256:b9ccca7b66e4c08161b8423e743621725a5e64afc87c0b1bab0f7a6f826e46a5"
)
TEMPERATURE_ALTERNATIVE_DIGEST = (
    "sha256:93bc8e0247f7b6d8eb95123cdafb121839fecf7109f915bc1144eb9cf82f9cc9"
)
STATE_ALTERNATIVE = (
    "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"
    "e8ef1131caeb64f7c51af755bd69aee594b139383f1a8288d4e9364fe8c48c73"
)
TEMPERATURE_ALTERNATIVE = (
    "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"
    "847fa3c090e228a792bb79d696bb82ea37e2edebe727d2c1581ce8bbf0a82dad"
)
STATE_CONDITION = (
    "urn:malleus:contract-structure:slot-condition:v0:sha256:"
    "ff6e3ab82671dbb26b59ef72b7e7aba75b635c60e65927290232ff15bf10e5cf"
)
TEMPERATURE_CONDITION = (
    "urn:malleus:contract-structure:slot-condition:v0:sha256:"
    "8e6a37dee67ef89a97d413791d1c227bbf843d3676def59fb5c9af966437587f"
)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


FactObject = str | bool
FactTriple = tuple[str, str, FactObject]

# This is the independent answer key. Every one of the 90 facts is written here;
# no source loader, LinkML object, registry, compiler, or runtime produces it.
BASELINE_FACT_TRIPLES: tuple[FactTriple, ...] = (
    (SAMPLE, RDF_TYPE, f"{CONTRACT_FACTS}Class"),
    (SAMPLE, f"{CONTRACT_FACTS}isMixin", False),
    (SAMPLE, f"{CONTRACT_FACTS}abstract", False),
    (TRACEABLE, RDF_TYPE, f"{CONTRACT_FACTS}Class"),
    (TRACEABLE, f"{CONTRACT_FACTS}isMixin", True),
    (TRACEABLE, f"{CONTRACT_FACTS}abstract", False),
    (OBSERVATION, RDF_TYPE, f"{CONTRACT_FACTS}Class"),
    (OBSERVATION, RDFS_SUBCLASS, SAMPLE),
    (OBSERVATION, f"{CONTRACT_FACTS}usesMixin", TRACEABLE),
    (OBSERVATION, f"{CONTRACT_FACTS}isMixin", False),
    (OBSERVATION, f"{CONTRACT_FACTS}abstract", False),
    (CELSIUS, RDF_TYPE, f"{CONTRACT_FACTS}Scalar"),
    (CELSIUS, f"{CONTRACT_FACTS}typeof", f"{CONTRACT_FACTS}Float"),
    (PLANT_STATE, RDF_TYPE, f"{CONTRACT_FACTS}Enum"),
    (PLANT_STATE, f"{CONTRACT_FACTS}enumValue", "HEALTHY"),
    (PLANT_STATE, f"{CONTRACT_FACTS}enumValue", "STRESSED"),
    (SPECIMEN_ID, RDF_TYPE, f"{CONTRACT_FACTS}Slot"),
    (SPECIMEN_ID, f"{CONTRACT_FACTS}valueRange", f"{CONTRACT_FACTS}String"),
    (SPECIMEN_ID, f"{CONTRACT_FACTS}required", False),
    (SPECIMEN_ID, f"{CONTRACT_FACTS}multivalued", False),
    (SPECIMEN_ID, f"{CONTRACT_FACTS}identifier", True),
    (SPECIMEN_ID, f"{CONTRACT_FACTS}inlined", False),
    (TEMPERATURE, RDF_TYPE, f"{CONTRACT_FACTS}Slot"),
    (TEMPERATURE, f"{CONTRACT_FACTS}valueRange", CELSIUS),
    (TEMPERATURE, f"{CONTRACT_FACTS}required", False),
    (TEMPERATURE, f"{CONTRACT_FACTS}multivalued", False),
    (TEMPERATURE, f"{CONTRACT_FACTS}identifier", False),
    (TEMPERATURE, f"{CONTRACT_FACTS}inlined", False),
    (TEMPERATURE, f"{CONTRACT_FACTS}minimum", "-20"),
    (TEMPERATURE, f"{CONTRACT_FACTS}maximum", "60"),
    (STATE, RDF_TYPE, f"{CONTRACT_FACTS}Slot"),
    (STATE, f"{CONTRACT_FACTS}valueRange", PLANT_STATE),
    (STATE, f"{CONTRACT_FACTS}required", False),
    (STATE, f"{CONTRACT_FACTS}multivalued", False),
    (STATE, f"{CONTRACT_FACTS}identifier", False),
    (STATE, f"{CONTRACT_FACTS}inlined", False),
    (NOTE, RDF_TYPE, f"{CONTRACT_FACTS}Slot"),
    (NOTE, f"{CONTRACT_FACTS}valueRange", f"{CONTRACT_FACTS}String"),
    (NOTE, f"{CONTRACT_FACTS}required", False),
    (NOTE, f"{CONTRACT_FACTS}multivalued", False),
    (NOTE, f"{CONTRACT_FACTS}identifier", False),
    (NOTE, f"{CONTRACT_FACTS}inlined", False),
    (SPECIMEN_USE, RDF_TYPE, f"{CONTRACT_FACTS}SlotUse"),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}onClass", OBSERVATION),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}usesSlot", SPECIMEN_ID),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}valueRange", f"{CONTRACT_FACTS}String"),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}required", True),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}multivalued", False),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}identifier", True),
    (SPECIMEN_USE, f"{CONTRACT_FACTS}inlined", False),
    (TEMPERATURE_USE, RDF_TYPE, f"{CONTRACT_FACTS}SlotUse"),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}onClass", OBSERVATION),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}usesSlot", TEMPERATURE),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}valueRange", CELSIUS),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}required", False),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}multivalued", False),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}identifier", False),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}inlined", False),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}minimum", "-20"),
    (TEMPERATURE_USE, f"{CONTRACT_FACTS}maximum", "60"),
    (STATE_USE, RDF_TYPE, f"{CONTRACT_FACTS}SlotUse"),
    (STATE_USE, f"{CONTRACT_FACTS}onClass", OBSERVATION),
    (STATE_USE, f"{CONTRACT_FACTS}usesSlot", STATE),
    (STATE_USE, f"{CONTRACT_FACTS}valueRange", PLANT_STATE),
    (STATE_USE, f"{CONTRACT_FACTS}required", False),
    (STATE_USE, f"{CONTRACT_FACTS}multivalued", False),
    (STATE_USE, f"{CONTRACT_FACTS}identifier", False),
    (STATE_USE, f"{CONTRACT_FACTS}inlined", False),
    (NOTE_USE, RDF_TYPE, f"{CONTRACT_FACTS}SlotUse"),
    (NOTE_USE, f"{CONTRACT_FACTS}onClass", OBSERVATION),
    (NOTE_USE, f"{CONTRACT_FACTS}usesSlot", NOTE),
    (NOTE_USE, f"{CONTRACT_FACTS}valueRange", f"{CONTRACT_FACTS}String"),
    (NOTE_USE, f"{CONTRACT_FACTS}required", False),
    (NOTE_USE, f"{CONTRACT_FACTS}multivalued", False),
    (NOTE_USE, f"{CONTRACT_FACTS}identifier", False),
    (NOTE_USE, f"{CONTRACT_FACTS}inlined", False),
    (EXACTLY_ONE_GROUP, RDF_TYPE, f"{CONTRACT_FACTS}ExactlyOneGroup"),
    (EXACTLY_ONE_GROUP, f"{CONTRACT_FACTS}onClass", OBSERVATION),
    (
        STATE_ALTERNATIVE,
        RDF_TYPE,
        f"{CONTRACT_FACTS}ExactlyOneAlternative",
    ),
    (STATE_ALTERNATIVE, f"{CONTRACT_FACTS}inGroup", EXACTLY_ONE_GROUP),
    (
        TEMPERATURE_ALTERNATIVE,
        RDF_TYPE,
        f"{CONTRACT_FACTS}ExactlyOneAlternative",
    ),
    (TEMPERATURE_ALTERNATIVE, f"{CONTRACT_FACTS}inGroup", EXACTLY_ONE_GROUP),
    (STATE_CONDITION, RDF_TYPE, f"{CONTRACT_FACTS}SlotCondition"),
    (STATE_CONDITION, f"{CONTRACT_FACTS}inAlternative", STATE_ALTERNATIVE),
    (STATE_CONDITION, f"{CONTRACT_FACTS}usesSlot", STATE),
    (STATE_CONDITION, f"{CONTRACT_FACTS}equalsString", "HEALTHY"),
    (TEMPERATURE_CONDITION, RDF_TYPE, f"{CONTRACT_FACTS}SlotCondition"),
    (
        TEMPERATURE_CONDITION,
        f"{CONTRACT_FACTS}inAlternative",
        TEMPERATURE_ALTERNATIVE,
    ),
    (TEMPERATURE_CONDITION, f"{CONTRACT_FACTS}usesSlot", TEMPERATURE),
    (TEMPERATURE_CONDITION, f"{CONTRACT_FACTS}valuePresence", "PRESENT"),
)


def _facts(triples: tuple[FactTriple, ...]) -> list[dict[str, FactObject]]:
    return sorted(
        (
            {"object": object_, "predicate": predicate, "subject": subject}
            for subject, predicate, object_ in triples
        ),
        key=_canonical_json_bytes,
    )


BASELINE_FACTS = _facts(BASELINE_FACT_TRIPLES)
BASELINE_FACT_BYTES = 17906
BASELINE_FACT_SHA256 = (
    "4103a7cf5db383a1bf29f88bcf94e0057707ea94452f0a36a073b9bb95564db4"
)
SEMANTIC_FACT_BYTES = 17906
SEMANTIC_FACT_SHA256 = (
    "20de741716c686ea5beb48951c0b9ecab05f63348745a6bd424c834748d32664"
)

REMOVED_FACTS = _facts(
    (
        (TEMPERATURE, f"{CONTRACT_FACTS}maximum", "60"),
        (TEMPERATURE_USE, f"{CONTRACT_FACTS}maximum", "60"),
    )
)
ADDED_FACTS = _facts(
    (
        (TEMPERATURE, f"{CONTRACT_FACTS}maximum", "55"),
        (TEMPERATURE_USE, f"{CONTRACT_FACTS}maximum", "55"),
    )
)

EXPECTED_SOURCES = [
    {
        "byte_length": byte_length,
        "outcome": "ACCEPT",
        "path": SOURCE_PATHS[name.removesuffix(".yaml")],
        "source_blob": f"TEST_ONLY_SOURCE_BLOB_SHA256_{digest}",
    }
    for name, byte_length, digest in SOURCE_DESCRIPTORS
]

EXPECTED_COMPILATIONS = [
    {
        "canonical_fact_byte_length": BASELINE_FACT_BYTES,
        "canonical_facts_sha256": (
            f"TEST_ONLY_CANONICAL_FACTS_SHA256_{BASELINE_FACT_SHA256}"
        ),
        "fact_count": 90,
        "outcome": "ACCEPT",
        "source_path": SOURCE_PATHS[source],
    }
    for source in (
        "baseline",
        "explicit-defaults",
        "numeric-equivalent",
        "presentation-only",
        "reordered",
    )
] + [
    {
        "canonical_fact_byte_length": SEMANTIC_FACT_BYTES,
        "canonical_facts_sha256": (
            f"TEST_ONLY_CANONICAL_FACTS_SHA256_{SEMANTIC_FACT_SHA256}"
        ),
        "fact_count": 90,
        "outcome": "ACCEPT",
        "source_path": SOURCE_PATHS["semantic-change"],
    }
]

EXPECTED_COMPILATION_ORACLE = {
    "baseline_facts": BASELINE_FACTS,
    "compilations": EXPECTED_COMPILATIONS,
    "configuration": CONFIGURATION,
    "semantic_change": {
        "added_facts": ADDED_FACTS,
        "reference_source_path": BASELINE_SOURCE,
        "removed_facts": REMOVED_FACTS,
        "source_path": SOURCE_PATHS["semantic-change"],
    },
    "sources": EXPECTED_SOURCES,
}

OPERATION_INPUTS = {
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "closed-composition-semantic-change/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "closed-composition-delta",
        "scenario_id": "closed-contract-composition",
        "source_path": SOURCE_PATHS["semantic-change"],
    },
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "linkml-profile-baseline/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-positive",
        "scenario_id": "linkml-support-profile",
        "source_path": SOURCE_PATHS["baseline"],
    },
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "linkml-profile-explicit-defaults/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": SOURCE_PATHS["explicit-defaults"],
    },
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "linkml-profile-numeric-equivalent/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": SOURCE_PATHS["numeric-equivalent"],
    },
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "linkml-profile-presentation-only/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": SOURCE_PATHS["presentation-only"],
    },
    (
        "conformance/contract_kernel/v0/neutral_domain/traces/input/"
        "linkml-profile-reordered/operation.json"
    ): {
        "operation": "COMPILE_SOURCE",
        "requirement_id": "linkml-profile-metamorphic",
        "scenario_id": "linkml-support-profile",
        "source_path": SOURCE_PATHS["reordered"],
    },
}

RELATION_AXES = frozenset(
    {
        "accepted_temporal_epoch",
        "compiled_facts",
        "contract_composition",
        "effective_contract",
        "governance_contract",
        "governed_graph_contract",
        "logical_artifact",
        "protocol_record_contract",
        "raw_source",
        "source_attestation",
        "validated_fact_set",
    }
)

BASELINE_RELATIONS = {
    "accepted_temporal_epoch": "SAME",
    "compiled_facts": "SAME",
    "contract_composition": "SAME",
    "effective_contract": "SAME",
    "governance_contract": "SAME",
    "governed_graph_contract": "SAME",
    "logical_artifact": "NOT_CLAIMED",
    "protocol_record_contract": "SAME",
    "raw_source": "SAME",
    "source_attestation": "SAME",
    "validated_fact_set": "SAME",
}
EQUIVALENT_RELATIONS = {
    **BASELINE_RELATIONS,
    "raw_source": "DIFFERENT",
    "source_attestation": "DIFFERENT",
}
SEMANTIC_CHANGE_RELATIONS = {
    **EQUIVALENT_RELATIONS,
    "accepted_temporal_epoch": "DIFFERENT",
    "compiled_facts": "DIFFERENT",
    "contract_composition": "DIFFERENT",
    "effective_contract": "DIFFERENT",
    "governed_graph_contract": "DIFFERENT",
    "validated_fact_set": "DIFFERENT",
}


def _operation_outcome(
    input_path: str,
    source_path: str,
    relations: dict[str, str],
) -> dict[str, Any]:
    return {
        "input_path": input_path,
        "outcome": "ACCEPT",
        "reference_source_path": BASELINE_SOURCE,
        "relations": relations,
        "source_path": source_path,
    }


EXPECTED_OPERATION_OUTCOMES = [
    _operation_outcome(
        input_path,
        operation["source_path"],
        (
            SEMANTIC_CHANGE_RELATIONS
            if operation["source_path"] == SOURCE_PATHS["semantic-change"]
            else BASELINE_RELATIONS
            if operation["source_path"] == BASELINE_SOURCE
            else EQUIVALENT_RELATIONS
        ),
    )
    for input_path, operation in OPERATION_INPUTS.items()
]

EXPECTED_OPERATION_ORACLE = {
    "configuration": CONFIGURATION,
    "operations": EXPECTED_OPERATION_OUTCOMES,
}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON number: {value}")


def _decode_json(raw: str) -> Any:
    return json.loads(
        raw,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
    )


def _load_json(path: Path) -> dict[str, Any]:
    value = _decode_json(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _strings(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [
            string
            for key, item in value.items()
            for member in (key, item)
            for string in _strings(member)
        ]
    if isinstance(value, list):
        return [string for item in value for string in _strings(item)]
    return [value] if isinstance(value, str) else []


def _assert_json_types_match(value: Any, expected: Any) -> None:
    assert type(value) is type(expected)
    if isinstance(expected, dict):
        assert set(value) == set(expected)
        for key, item in expected.items():
            _assert_json_types_match(value[key], item)
    elif isinstance(expected, list):
        assert len(value) == len(expected)
        for item, expected_item in zip(value, expected):
            _assert_json_types_match(item, expected_item)


def _assert_no_producer_dependency(source: str) -> None:
    tree = ast.parse(source)
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(
                alias.name.split(".", maxsplit=1)[0] for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            assert node.module is not None
            imported_roots.add(node.module.split(".", maxsplit=1)[0])
    assert imported_roots == {
        "__future__",
        "ast",
        "copy",
        "hashlib",
        "json",
        "pathlib",
        "pytest",
        "typing",
    }
    forbidden_calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"__import__", "compile", "eval", "exec"}
    }
    forbidden_calls.update(
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"import_module", "run_module", "run_path"}
    )
    assert not forbidden_calls


def _assert_digest_token(value: str, prefix: str) -> None:
    assert value.startswith(prefix)
    digest = value.removeprefix(prefix)
    assert len(digest) == 64
    assert set(digest) <= LOWERCASE_HEX


def _assert_outcome(value: Any) -> None:
    assert value == "ACCEPT" or value == REFUSE


def _assert_compilation_oracle(value: dict[str, Any]) -> None:
    _assert_json_types_match(value, EXPECTED_COMPILATION_ORACLE)
    assert set(value) == {
        "baseline_facts",
        "compilations",
        "configuration",
        "semantic_change",
        "sources",
    }
    assert value["configuration"] == CONFIGURATION
    assert value["sources"] == EXPECTED_SOURCES
    assert value["compilations"] == EXPECTED_COMPILATIONS
    assert value["baseline_facts"] == BASELINE_FACTS
    assert value["semantic_change"] == EXPECTED_COMPILATION_ORACLE["semantic_change"]

    for source in value["sources"]:
        assert set(source) == {"byte_length", "outcome", "path", "source_blob"}
        _assert_outcome(source["outcome"])
        _assert_digest_token(source["source_blob"], "TEST_ONLY_SOURCE_BLOB_SHA256_")
    for compilation in value["compilations"]:
        assert set(compilation) == {
            "canonical_fact_byte_length",
            "canonical_facts_sha256",
            "fact_count",
            "outcome",
            "source_path",
        }
        _assert_outcome(compilation["outcome"])
        _assert_digest_token(
            compilation["canonical_facts_sha256"],
            "TEST_ONLY_CANONICAL_FACTS_SHA256_",
        )
    for fact in value["baseline_facts"]:
        assert set(fact) == {"object", "predicate", "subject"}
    assert set(value["semantic_change"]) == {
        "added_facts",
        "reference_source_path",
        "removed_facts",
        "source_path",
    }
    assert value == EXPECTED_COMPILATION_ORACLE


def _assert_operation_oracle(value: dict[str, Any]) -> None:
    _assert_json_types_match(value, EXPECTED_OPERATION_ORACLE)
    assert set(value) == {"configuration", "operations"}
    assert value["configuration"] == CONFIGURATION
    assert value["operations"] == EXPECTED_OPERATION_OUTCOMES
    for operation in value["operations"]:
        assert set(operation) == {
            "input_path",
            "outcome",
            "reference_source_path",
            "relations",
            "source_path",
        }
        _assert_outcome(operation["outcome"])
        assert set(operation["relations"]) == RELATION_AXES
        assert set(operation["relations"].values()) <= {
            "DIFFERENT",
            "NOT_CLAIMED",
            "SAME",
        }
        assert operation["relations"]["logical_artifact"] == "NOT_CLAIMED"
    assert value == EXPECTED_OPERATION_ORACLE


def _inventory(root: Path) -> tuple[str, ...]:
    return tuple(
        sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        )
    )


def test_compilation_oracle_matches_the_independent_literal_answer_key() -> None:
    assert _inventory(ORACLE_ROOT) == ("greenhouse.json",)
    assert not any(path.is_symlink() for path in ORACLE_ROOT.rglob("*"))
    _assert_compilation_oracle(_load_json(ORACLE_PATH))


def test_operation_oracle_matches_the_independent_literal_answer_key() -> None:
    assert _inventory(TRACE_ORACLE_ROOT) == ("compile-source-outcomes.json",)
    assert not any(path.is_symlink() for path in TRACE_ORACLE_ROOT.rglob("*"))
    _assert_operation_oracle(_load_json(TRACE_ORACLE_PATH))


def test_source_descriptors_are_exact_and_every_source_is_accepted() -> None:
    assert len(EXPECTED_SOURCES) == 6
    assert {source["outcome"] for source in EXPECTED_SOURCES} == {"ACCEPT"}
    for relative, byte_length, digest in SOURCE_DESCRIPTORS:
        raw = (SOURCE_ROOT / relative).read_bytes()
        assert len(raw) == byte_length
        assert sha256(raw).hexdigest() == digest


def test_operation_inputs_are_exact_bounded_stimuli() -> None:
    assert len(OPERATION_INPUTS) == 6
    for relative, expected in OPERATION_INPUTS.items():
        path = REPOSITORY / relative
        assert _load_json(path) == expected


def test_baseline_is_the_exact_90_fact_canonical_array() -> None:
    assert len(BASELINE_FACT_TRIPLES) == 90
    assert len(set(BASELINE_FACT_TRIPLES)) == 90
    assert len(BASELINE_FACTS) == 90
    assert BASELINE_FACTS == sorted(BASELINE_FACTS, key=_canonical_json_bytes)

    canonical = _canonical_json_bytes(BASELINE_FACTS)
    assert len(canonical) == BASELINE_FACT_BYTES
    assert sha256(canonical).hexdigest() == BASELINE_FACT_SHA256

    assert {
        "object": False,
        "predicate": f"{CONTRACT_FACTS}required",
        "subject": SPECIMEN_ID,
    } in BASELINE_FACTS
    assert {
        "object": True,
        "predicate": f"{CONTRACT_FACTS}required",
        "subject": SPECIMEN_USE,
    } in BASELINE_FACTS


def test_structural_subjects_follow_the_literal_od005_od008_envelopes() -> None:
    slot_use_inputs = {
        SPECIMEN_USE: SPECIMEN_ID,
        TEMPERATURE_USE: TEMPERATURE,
        STATE_USE: STATE,
        NOTE_USE: NOTE,
    }
    for subject, slot in slot_use_inputs.items():
        envelope = {
            "class": OBSERVATION,
            "domain": "malleus.contract-structure.slot-use/v0",
            "slot": slot,
        }
        assert subject.endswith(sha256(_canonical_json_bytes(envelope)).hexdigest())

    alternative_semantics = {
        STATE_ALTERNATIVE_DIGEST: {
            "conditions": [{"equalsString": "HEALTHY", "slot": STATE}],
            "domain": "malleus.exactly-one-alternative-semantics/v0",
        },
        TEMPERATURE_ALTERNATIVE_DIGEST: {
            "conditions": [{"slot": TEMPERATURE, "valuePresence": "PRESENT"}],
            "domain": "malleus.exactly-one-alternative-semantics/v0",
        },
    }
    for digest, envelope in alternative_semantics.items():
        assert digest == f"sha256:{sha256(_canonical_json_bytes(envelope)).hexdigest()}"

    group_envelope = {
        "alternative_semantic_digests": sorted(alternative_semantics),
        "class": OBSERVATION,
        "domain": "malleus.contract-structure.exactly-one-group/v0",
    }
    assert EXACTLY_ONE_GROUP.endswith(
        sha256(_canonical_json_bytes(group_envelope)).hexdigest()
    )

    alternatives = {
        STATE_ALTERNATIVE: STATE_ALTERNATIVE_DIGEST,
        TEMPERATURE_ALTERNATIVE: TEMPERATURE_ALTERNATIVE_DIGEST,
    }
    for subject, semantic_digest in alternatives.items():
        envelope = {
            "alternative_semantic_digest": semantic_digest,
            "domain": "malleus.contract-structure.exactly-one-alternative/v0",
            "group": EXACTLY_ONE_GROUP,
        }
        assert subject.endswith(sha256(_canonical_json_bytes(envelope)).hexdigest())

    conditions = {
        STATE_CONDITION: (STATE_ALTERNATIVE, STATE),
        TEMPERATURE_CONDITION: (TEMPERATURE_ALTERNATIVE, TEMPERATURE),
    }
    for subject, (alternative, slot) in conditions.items():
        envelope = {
            "alternative": alternative,
            "domain": "malleus.contract-structure.slot-condition/v0",
            "slot": slot,
        }
        assert subject.endswith(sha256(_canonical_json_bytes(envelope)).hexdigest())


def test_semantic_change_is_exactly_two_removals_and_two_additions() -> None:
    assert len(REMOVED_FACTS) == len(ADDED_FACTS) == 2
    assert {fact["subject"] for fact in REMOVED_FACTS} == {
        TEMPERATURE,
        TEMPERATURE_USE,
    }
    assert {fact["subject"] for fact in ADDED_FACTS} == {
        TEMPERATURE,
        TEMPERATURE_USE,
    }
    assert {fact["predicate"] for fact in REMOVED_FACTS + ADDED_FACTS} == {
        f"{CONTRACT_FACTS}maximum"
    }
    assert {fact["object"] for fact in REMOVED_FACTS} == {"60"}
    assert {fact["object"] for fact in ADDED_FACTS} == {"55"}

    semantic_facts = [
        fact for fact in BASELINE_FACTS if fact not in REMOVED_FACTS
    ] + ADDED_FACTS
    semantic_facts.sort(key=_canonical_json_bytes)
    assert len(semantic_facts) == 90
    assert {fact["subject"] for fact in semantic_facts} == {
        fact["subject"] for fact in BASELINE_FACTS
    }
    canonical = _canonical_json_bytes(semantic_facts)
    assert len(canonical) == SEMANTIC_FACT_BYTES
    assert sha256(canonical).hexdigest() == SEMANTIC_FACT_SHA256


def test_relation_axes_preserve_two_roles_and_change_only_domain_dependents() -> None:
    assert set(BASELINE_RELATIONS) == RELATION_AXES
    assert set(EQUIVALENT_RELATIONS) == RELATION_AXES
    assert set(SEMANTIC_CHANGE_RELATIONS) == RELATION_AXES
    assert len(EXPECTED_OPERATION_OUTCOMES) == 6
    assert {item["outcome"] for item in EXPECTED_OPERATION_OUTCOMES} == {"ACCEPT"}

    semantic = next(
        item
        for item in EXPECTED_OPERATION_OUTCOMES
        if item["source_path"] == SOURCE_PATHS["semantic-change"]
    )["relations"]
    assert {axis for axis, relation in semantic.items() if relation == "DIFFERENT"} == {
        "accepted_temporal_epoch",
        "compiled_facts",
        "contract_composition",
        "effective_contract",
        "governed_graph_contract",
        "raw_source",
        "source_attestation",
        "validated_fact_set",
    }
    assert semantic["protocol_record_contract"] == "SAME"
    assert semantic["governance_contract"] == "SAME"
    assert all(
        item["relations"]["logical_artifact"] == "NOT_CLAIMED"
        for item in EXPECTED_OPERATION_OUTCOMES
    )

    for item in EXPECTED_OPERATION_OUTCOMES:
        if item["source_path"] in {
            SOURCE_PATHS["explicit-defaults"],
            SOURCE_PATHS["numeric-equivalent"],
            SOURCE_PATHS["presentation-only"],
            SOURCE_PATHS["reordered"],
        }:
            assert item["relations"] == EQUIVALENT_RELATIONS


@pytest.mark.parametrize(
    ("target", "mutation"),
    (
        ("compilation", "fact-object"),
        ("compilation", "fact-boolean-type"),
        ("compilation", "source-outcome"),
        ("compilation", "delta-member"),
        ("compilation", "top-level-member"),
        ("operation", "relation"),
        ("operation", "outcome"),
        ("operation", "relations-member"),
        ("operation", "configuration-boolean-type"),
        ("operation", "top-level-member"),
    ),
)
def test_exact_guards_detect_private_oracle_mutations(
    target: str,
    mutation: str,
) -> None:
    if target == "compilation":
        value = deepcopy(EXPECTED_COMPILATION_ORACLE)
        if mutation == "fact-object":
            value["baseline_facts"][0]["object"] = "CORRUPT"
        elif mutation == "fact-boolean-type":
            boolean_fact = next(
                fact for fact in value["baseline_facts"] if fact["object"] is False
            )
            boolean_fact["object"] = 0
        elif mutation == "source-outcome":
            value["sources"][0]["outcome"] = "ERROR"
        elif mutation == "delta-member":
            value["semantic_change"]["unexpected"] = True
        else:
            value["unexpected"] = True
        guard = _assert_compilation_oracle
    else:
        value = deepcopy(EXPECTED_OPERATION_ORACLE)
        if mutation == "relation":
            value["operations"][0]["relations"]["compiled_facts"] = "SAME"
        elif mutation == "outcome":
            value["operations"][0]["outcome"] = "ERROR"
        elif mutation == "relations-member":
            value["operations"][0]["relations"]["unexpected"] = "SAME"
        elif mutation == "configuration-boolean-type":
            value["configuration"]["public_contract"] = 0
        else:
            value["unexpected"] = True
        guard = _assert_operation_oracle

    with pytest.raises(AssertionError):
        guard(value)


@pytest.mark.parametrize(
    "raw",
    (
        '{"value":1,"value":2}',
        '{"value":NaN}',
        '{"value":Infinity}',
        '{"value":-Infinity}',
    ),
)
def test_private_json_loader_refuses_duplicate_keys_and_nonfinite_numbers(
    raw: str,
) -> None:
    with pytest.raises(ValueError):
        _decode_json(raw)


def test_private_metadata_and_result_unions_create_no_public_contract() -> None:
    for oracle in (EXPECTED_COMPILATION_ORACLE, EXPECTED_OPERATION_ORACLE):
        assert oracle["configuration"] == CONFIGURATION
        assert oracle["configuration"]["artifact_role"] == "CONFORMANCE_FIXTURE"
        assert oracle["configuration"]["public_contract"] is False
        for value in _strings(oracle):
            if value.startswith("TEST_ONLY_SOURCE_BLOB_SHA256_"):
                _assert_digest_token(value, "TEST_ONLY_SOURCE_BLOB_SHA256_")
            elif value.startswith("TEST_ONLY_CANONICAL_FACTS_SHA256_"):
                _assert_digest_token(value, "TEST_ONLY_CANONICAL_FACTS_SHA256_")
            elif value.startswith("TEST_ONLY_"):
                assert value in set(CONFIGURATION.values())

        serialized = json.dumps(oracle, sort_keys=True)
        for forbidden in (
            "PUBLIC_",
            "artifact_bytes",
            "compatibility_contract",
            "runtime_wire",
            "wire_format",
        ):
            assert forbidden not in serialized


def test_oracles_are_absent_from_inputs_and_the_test_imports_no_producer() -> None:
    forbidden_input_tokens = (
        "TEST_ONLY_",
        "NOT_CLAIMED",
        BASELINE_FACT_SHA256,
        SEMANTIC_FACT_SHA256,
        ORACLE_PATH.name,
        TRACE_ORACLE_PATH.name,
    )
    input_paths = [
        *(SOURCE_ROOT / relative for relative, _, _ in SOURCE_DESCRIPTORS),
        *(REPOSITORY / relative for relative in OPERATION_INPUTS),
    ]
    for path in input_paths:
        raw = path.read_text(encoding="utf-8")
        for token in forbidden_input_tokens:
            assert token not in raw

    _assert_no_producer_dependency(Path(__file__).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "snippet",
    (
        '__import__("linkml_runtime")',
        'exec("import linkml_runtime")',
        "from linkml_runtime import Any",
    ),
)
def test_no_producer_guard_rejects_hidden_producer_imports(snippet: str) -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    with pytest.raises(AssertionError):
        _assert_no_producer_dependency(f"{source}\n{snippet}\n")

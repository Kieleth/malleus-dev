"""Fixed private answer-key checks for the Quiet Bell compilation fixture."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import pytest


REPOSITORY = Path(__file__).resolve().parents[2]
KERNEL = REPOSITORY / "conformance" / "contract_kernel" / "v0"
SOURCE_ROOT = KERNEL / "themed_fixture" / "sources"
ORACLE_ROOT = KERNEL / "themed_fixture" / "oracle"
ORACLE_PATH = ORACLE_ROOT / "quiet_bell.json"

CONFIGURATION = {
    "capabilities": "TEST_ONLY_REPOSITORY_FILE_NETWORK_DENIED_V0",
    "media_type": "TEST_ONLY_JSON_SHAPED_YAML",
    "profile": "TEST_ONLY_LINKML_V0_PROFILE",
    "resolver": "TEST_ONLY_STRICT_MALLEUS_RESOLVER_V0",
}
SOURCE_DESCRIPTORS = (
    (
        "modules/activity.yaml",
        1821,
        "66814b70e6756f8038afc9aa7b4344f07be509a08b952473cb410b1c59df9f54",
    ),
    (
        "modules/entities.yaml",
        1378,
        "b9076cf744f59a1aefc5e2e5d347cb5e5f14481df5ba1e177ea19315a26c529f",
    ),
    (
        "modules/foundation.yaml",
        1166,
        "2fe7824e048e474fb33be09239cd249b9303d307327d9e5ce2d9eca8cc535948",
    ),
    (
        "v1.0.0/quiet_bell.yaml",
        845,
        "2b93cf1a25439d3d7dcc67556429d72e9783373b7283794a10f99137ed6c5a7a",
    ),
    (
        "v1.0.1/quiet_bell.yaml",
        880,
        "5a7b56c07301426c21d4dc68356549450ac0a0f2fd40c92cb9cf6033aa469f80",
    ),
    (
        "v1.1.0/quiet_bell.yaml",
        1081,
        "faeeb2e7013400a5930793f42058464e727715aa7658f35a6340b791e059c698",
    ),
)
REFUSE = {"outcome": "REFUSE"}
EXPECTED_IMPORT_EDGES = [
    {
        "child": "modules/foundation.yaml",
        "literal": "foundation",
        "ordinal": 0,
        "parent": "modules/activity.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/entities.yaml",
        "literal": "entities",
        "ordinal": 1,
        "parent": "modules/activity.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/foundation.yaml",
        "literal": "foundation",
        "ordinal": 0,
        "parent": "modules/entities.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "linkml:types",
        "literal": "linkml:types",
        "ordinal": 0,
        "parent": "modules/foundation.yaml",
        "resolution": "ACCEPT",
    },
    {
        "literal": "malleus",
        "ordinal": 1,
        "parent": "modules/foundation.yaml",
        "resolution": REFUSE,
    },
    {
        "child": "modules/entities.yaml",
        "literal": "../modules/entities",
        "ordinal": 0,
        "parent": "v1.0.0/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/activity.yaml",
        "literal": "../modules/activity",
        "ordinal": 1,
        "parent": "v1.0.0/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/activity.yaml",
        "literal": "../modules/activity",
        "ordinal": 0,
        "parent": "v1.0.1/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/entities.yaml",
        "literal": "../modules/entities",
        "ordinal": 1,
        "parent": "v1.0.1/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/entities.yaml",
        "literal": "../modules/entities",
        "ordinal": 0,
        "parent": "v1.1.0/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
    {
        "child": "modules/activity.yaml",
        "literal": "../modules/activity",
        "ordinal": 1,
        "parent": "v1.1.0/quiet_bell.yaml",
        "resolution": "ACCEPT",
    },
]
EXPECTED_DECLARATIONS = {
    "modules/activity.yaml": {
        "Class": [
            "https://malleus.dev/conformance/quiet-bell/activity/CitesFolioRelation",
            "https://malleus.dev/conformance/quiet-bell/activity/SealDiscrepancySignal",
            "https://malleus.dev/conformance/quiet-bell/activity/SealReviewEvent",
        ],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/activity/reviewed_by",
            "https://malleus.dev/conformance/quiet-bell/activity/reviewed_relation",
        ],
    },
    "modules/entities.yaml": {
        "Class": [
            "https://malleus.dev/conformance/quiet-bell/entities/ArchiveExaminer",
            "https://malleus.dev/conformance/quiet-bell/entities/EvidenceFolio",
            "https://malleus.dev/conformance/quiet-bell/entities/EvidenceLocator",
        ],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/entities/EvidenceFolio/locator"
        ],
    },
    "modules/foundation.yaml": {
        "Enum": [
            "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveEventKind",
            "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveRelationKind",
            "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveSignalKind",
        ],
        "Scalar": [
            "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveShelfmark"
        ],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/foundation/certainty",
            "https://malleus.dev/conformance/quiet-bell/foundation/content_digest",
            "https://malleus.dev/conformance/quiet-bell/foundation/shelfmark",
        ],
    },
    "v1.0.0/quiet_bell.yaml": {
        "Class": ["https://malleus.dev/conformance/quiet-bell/InquiryDossier"],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
            "https://malleus.dev/conformance/quiet-bell/dossier_code",
        ],
    },
    "v1.0.1/quiet_bell.yaml": {
        "Class": ["https://malleus.dev/conformance/quiet-bell/InquiryDossier"],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
            "https://malleus.dev/conformance/quiet-bell/dossier_code",
        ],
    },
    "v1.1.0/quiet_bell.yaml": {
        "Class": ["https://malleus.dev/conformance/quiet-bell/InquiryDossier"],
        "Slot": [
            "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
            "https://malleus.dev/conformance/quiet-bell/dossier_code",
            "https://malleus.dev/conformance/quiet-bell/marginal_note",
        ],
    },
}
UNRESOLVED_BINDINGS = {
    "Agent",
    "Entity",
    "Event",
    "Relation",
    "Signal",
    "agent_type",
    "event_type",
    "relation_type",
    "signal_type",
    "source_id",
    "target_id",
}
EXPECTED_ACCEPTED_BINDINGS = {
    "ArchiveEventKind": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveEventKind",
    "ArchiveExaminer": "https://malleus.dev/conformance/quiet-bell/entities/ArchiveExaminer",
    "ArchiveRelationKind": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveRelationKind",
    "ArchiveShelfmark": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveShelfmark",
    "ArchiveSignalKind": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveSignalKind",
    "CitesFolioRelation": "https://malleus.dev/conformance/quiet-bell/activity/CitesFolioRelation",
    "EvidenceFolio": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceFolio",
    "EvidenceLocator": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceLocator",
    "InquiryDossier": "https://malleus.dev/conformance/quiet-bell/InquiryDossier",
    "assigned_examiner": "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
    "certainty": "https://malleus.dev/conformance/quiet-bell/foundation/certainty",
    "content_digest": "https://malleus.dev/conformance/quiet-bell/foundation/content_digest",
    "dossier_code": "https://malleus.dev/conformance/quiet-bell/dossier_code",
    "float": "https://malleus.dev/contract-facts/Float",
    "marginal_note": "https://malleus.dev/conformance/quiet-bell/marginal_note",
    "reviewed_by": "https://malleus.dev/conformance/quiet-bell/activity/reviewed_by",
    "reviewed_relation": "https://malleus.dev/conformance/quiet-bell/activity/reviewed_relation",
    "shelfmark": "https://malleus.dev/conformance/quiet-bell/foundation/shelfmark",
    "string": "https://malleus.dev/contract-facts/String",
}
EXPECTED_CLASS_DEFAULTS = [
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/InquiryDossier",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/activity/CitesFolioRelation",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/activity/SealDiscrepancySignal",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/activity/SealReviewEvent",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/entities/ArchiveExaminer",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceFolio",
    },
    {
        "abstract": False,
        "isMixin": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceLocator",
    },
]
EXPECTED_COMPLETE_SLOTS = [
    {
        "identifier": False,
        "inlined": False,
        "maximum": "1",
        "minimum": "0",
        "multivalued": False,
        "required": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/certainty",
        "valueRange": "https://malleus.dev/contract-facts/Float",
    },
    {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/content_digest",
        "valueRange": "https://malleus.dev/contract-facts/String",
    },
    {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/shelfmark",
        "valueRange": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveShelfmark",
    },
    {
        "identifier": False,
        "inlined": True,
        "multivalued": False,
        "required": True,
        "symbol": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceFolio/locator",
        "valueRange": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceLocator",
    },
    {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/marginal_note",
        "valueRange": "https://malleus.dev/contract-facts/String",
    },
    {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": True,
        "symbol": "https://malleus.dev/conformance/quiet-bell/dossier_code",
        "valueRange": "https://malleus.dev/contract-facts/String",
    },
]
EXPECTED_ENUM_VALUES = [
    {
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveEventKind",
        "value": "SEAL_REVIEW",
    },
    {
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveRelationKind",
        "value": "CITES_FOLIO",
    },
    {
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveSignalKind",
        "value": "SEAL_DISCREPANCY",
    },
]
EXPECTED_SCALARS = [
    {
        "symbol": "https://malleus.dev/conformance/quiet-bell/foundation/ArchiveShelfmark",
        "typeof": "https://malleus.dev/contract-facts/String",
    }
]
EXPECTED_COMPARISONS = [
    {
        "authored_local_semantic_projection": "SAME",
        "compiled_facts": "NOT_CLAIMED",
        "effective_contract": "NOT_CLAIMED",
        "left": "1.0.0",
        "logical_artifact": "NOT_CLAIMED",
        "raw_source": "DIFFERENT",
        "right": "1.0.1",
        "source_attestation": "DIFFERENT",
        "validated_fact_set": "NOT_CLAIMED",
    },
    {
        "authored_local_semantic_projection": "DIFFERENT",
        "compiled_facts": "NOT_CLAIMED",
        "effective_contract": "NOT_CLAIMED",
        "left": "1.0.0",
        "logical_artifact": "NOT_CLAIMED",
        "raw_source": "DIFFERENT",
        "right": "1.1.0",
        "source_attestation": "DIFFERENT",
        "validated_fact_set": "NOT_CLAIMED",
    },
    {
        "authored_local_semantic_projection": "DIFFERENT",
        "compiled_facts": "NOT_CLAIMED",
        "effective_contract": "NOT_CLAIMED",
        "left": "1.0.1",
        "logical_artifact": "NOT_CLAIMED",
        "raw_source": "DIFFERENT",
        "right": "1.1.0",
        "source_attestation": "DIFFERENT",
        "validated_fact_set": "NOT_CLAIMED",
    },
]
EXPECTED_AUTHORED_LOCAL_RESULTS = {
    "declarations": "ACCEPT",
    "import_graph": "ACCEPT",
    "source_descriptors": "ACCEPT",
}
EXPECTED_COMPILED_RESULTS = {
    "compilation": REFUSE,
    "elaboration": REFUSE,
    "effective_contract": REFUSE,
    "fact_set": REFUSE,
    "facts": REFUSE,
    "logical_artifact": REFUSE,
    "qualified_bindings": REFUSE,
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


def _load_oracle() -> dict[str, Any]:
    value = json.loads(
        ORACLE_PATH.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
    )
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
        return [item for member in value for item in _strings(member)]
    return [value] if isinstance(value, str) else []


def _objects(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value, *(item for member in value.values() for item in _objects(member))]
    if isinstance(value, list):
        return [item for member in value for item in _objects(member)]
    return []


def _assert_exact_accepted_bindings(oracle: dict[str, Any]) -> None:
    bindings = oracle["qualified_bindings"]
    references = [binding["reference"] for binding in bindings]
    assert len(references) == len(set(references))
    assert set(references) == set(EXPECTED_ACCEPTED_BINDINGS) | UNRESOLVED_BINDINGS
    assert {
        binding["reference"]: binding["target"]
        for binding in bindings
        if isinstance(binding["target"], str)
    } == EXPECTED_ACCEPTED_BINDINGS


def _assert_exact_class_defaults(oracle: dict[str, Any]) -> None:
    assert oracle["local_elaboration"]["class_defaults"] == EXPECTED_CLASS_DEFAULTS


def _assert_exact_complete_slots(oracle: dict[str, Any]) -> None:
    assert oracle["local_elaboration"]["complete_slots"] == EXPECTED_COMPLETE_SLOTS


def _assert_exact_enum_values(oracle: dict[str, Any]) -> None:
    assert oracle["local_elaboration"]["enum_values"] == EXPECTED_ENUM_VALUES


def _assert_exact_scalars(oracle: dict[str, Any]) -> None:
    assert oracle["local_elaboration"]["scalars"] == EXPECTED_SCALARS


def test_private_oracle_membership_configuration_and_source_descriptors() -> None:
    members = tuple(
        sorted(
            path.relative_to(ORACLE_ROOT).as_posix()
            for path in ORACLE_ROOT.rglob("*")
            if path.is_file()
        )
    )
    assert members == ("quiet_bell.json",)
    assert not any(path.is_symlink() for path in ORACLE_ROOT.rglob("*"))

    oracle = _load_oracle()
    assert oracle["configuration"] == CONFIGURATION
    assert oracle["sources"] == [
        {
            "byte_length": length,
            "outcome": "ACCEPT",
            "path": path,
            "source_blob": f"TEST_ONLY_SOURCE_BLOB_SHA256_{digest}",
        }
        for path, length, digest in SOURCE_DESCRIPTORS
    ]
    for relative, length, digest in SOURCE_DESCRIPTORS:
        path = SOURCE_ROOT / relative
        raw = path.read_bytes()
        assert len(raw) == length
        assert sha256(raw).hexdigest() == digest


def test_import_graph_retains_authored_edges_and_refuses_unknown_malleus_source() -> None:
    oracle = _load_oracle()
    assert oracle["import_edges"] == EXPECTED_IMPORT_EDGES
    refused = [
        edge
        for edge in oracle["import_edges"]
        if edge["resolution"] == REFUSE
    ]
    assert refused == [
        {
            "literal": "malleus",
            "ordinal": 1,
            "parent": "modules/foundation.yaml",
            "resolution": REFUSE,
        }
    ]


def test_declarations_bind_only_symbols_derived_from_controlled_sources() -> None:
    oracle = _load_oracle()
    assert oracle["declarations"] == EXPECTED_DECLARATIONS
    bindings = oracle["qualified_bindings"]
    assert [binding["reference"] for binding in bindings] == sorted(
        binding["reference"] for binding in bindings
    )
    assert {
        binding["reference"]
        for binding in bindings
        if binding["target"] == REFUSE
    } == UNRESOLVED_BINDINGS
    local_targets = {
        symbol
        for declarations in EXPECTED_DECLARATIONS.values()
        for symbols in declarations.values()
        for symbol in symbols
    }
    asserted_targets = {
        binding["target"]
        for binding in bindings
        if isinstance(binding["target"], str)
    }
    seed_targets = {
        "https://malleus.dev/contract-facts/Float",
        "https://malleus.dev/contract-facts/String",
    }
    assert asserted_targets <= local_targets | seed_targets
    _assert_exact_accepted_bindings(oracle)


def test_local_defaults_are_explicit_and_downstream_stages_refuse_atomically() -> None:
    oracle = _load_oracle()
    _assert_exact_class_defaults(oracle)
    _assert_exact_complete_slots(oracle)
    _assert_exact_enum_values(oracle)
    _assert_exact_scalars(oracle)
    elaboration = oracle["local_elaboration"]
    complete = {item["symbol"]: item for item in elaboration["complete_slots"]}

    marginal_note = complete["https://malleus.dev/conformance/quiet-bell/marginal_note"]
    assert marginal_note == {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
        "symbol": "https://malleus.dev/conformance/quiet-bell/marginal_note",
        "valueRange": "https://malleus.dev/contract-facts/String",
    }
    assert elaboration["incomplete_slots"] == [
        {
            "effective_value": REFUSE,
            "symbol": "https://malleus.dev/conformance/quiet-bell/activity/reviewed_by",
        },
        {
            "effective_value": REFUSE,
            "symbol": "https://malleus.dev/conformance/quiet-bell/activity/reviewed_relation",
        },
        {
            "effective_value": REFUSE,
            "symbol": "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
        },
    ]
    assert elaboration["exactly_one"] == {
        "alternatives": [
            [
                {
                    "slot": "https://malleus.dev/conformance/quiet-bell/foundation/content_digest",
                    "valuePresence": "ABSENT",
                },
                {
                    "required": True,
                    "slot": "https://malleus.dev/conformance/quiet-bell/foundation/shelfmark",
                },
            ],
            [
                {
                    "required": True,
                    "slot": "https://malleus.dev/conformance/quiet-bell/foundation/content_digest",
                },
                {
                    "slot": "https://malleus.dev/conformance/quiet-bell/foundation/shelfmark",
                    "valuePresence": "ABSENT",
                },
            ],
        ],
        "class": "https://malleus.dev/conformance/quiet-bell/entities/EvidenceLocator",
        "outcome": "ACCEPT",
    }
    for version in oracle["versions"]:
        assert version["authored_local"] == EXPECTED_AUTHORED_LOCAL_RESULTS
        assert version["compiled"] == EXPECTED_COMPILED_RESULTS


@pytest.mark.parametrize(
    "mutation",
    (
        "resolved-target-swapped",
        "accepted-binding-removed",
        "class-default-flipped",
        "complete-slot-maximum-changed",
        "enum-value-changed",
        "scalar-target-changed",
    ),
)
def test_exact_semantic_guards_reject_corruptions(mutation: str) -> None:
    oracle = deepcopy(_load_oracle())

    if mutation == "resolved-target-swapped":
        binding = next(
            item
            for item in oracle["qualified_bindings"]
            if item["reference"] == "ArchiveExaminer"
        )
        binding["target"] = EXPECTED_ACCEPTED_BINDINGS["EvidenceFolio"]
        guard = _assert_exact_accepted_bindings
    elif mutation == "accepted-binding-removed":
        oracle["qualified_bindings"] = [
            item
            for item in oracle["qualified_bindings"]
            if item["reference"] != "ArchiveExaminer"
        ]
        guard = _assert_exact_accepted_bindings
    elif mutation == "class-default-flipped":
        oracle["local_elaboration"]["class_defaults"][0]["abstract"] = True
        guard = _assert_exact_class_defaults
    elif mutation == "complete-slot-maximum-changed":
        oracle["local_elaboration"]["complete_slots"][0]["maximum"] = "999"
        guard = _assert_exact_complete_slots
    elif mutation == "enum-value-changed":
        oracle["local_elaboration"]["enum_values"][0]["value"] = "OTHER"
        guard = _assert_exact_enum_values
    else:
        oracle["local_elaboration"]["scalars"][0]["typeof"] = (
            "https://malleus.dev/contract-facts/Float"
        )
        guard = _assert_exact_scalars

    with pytest.raises(AssertionError):
        guard(oracle)


def test_version_meanings_and_nonclaims_are_exact() -> None:
    oracle = _load_oracle()
    assert oracle["comparisons"] == EXPECTED_COMPARISONS
    assert oracle["versions"] == [
        {
            "authored_local": EXPECTED_AUTHORED_LOCAL_RESULTS,
            "compiled": EXPECTED_COMPILED_RESULTS,
            "root": "v1.0.0/quiet_bell.yaml",
            "semantic_members": [
                "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
                "https://malleus.dev/conformance/quiet-bell/dossier_code",
            ],
            "version": "1.0.0",
        },
        {
            "authored_local": EXPECTED_AUTHORED_LOCAL_RESULTS,
            "compiled": EXPECTED_COMPILED_RESULTS,
            "root": "v1.0.1/quiet_bell.yaml",
            "semantic_members": [
                "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
                "https://malleus.dev/conformance/quiet-bell/dossier_code",
            ],
            "version": "1.0.1",
        },
        {
            "authored_local": EXPECTED_AUTHORED_LOCAL_RESULTS,
            "compiled": EXPECTED_COMPILED_RESULTS,
            "root": "v1.1.0/quiet_bell.yaml",
            "semantic_members": [
                "https://malleus.dev/conformance/quiet-bell/assigned_examiner",
                "https://malleus.dev/conformance/quiet-bell/dossier_code",
                "https://malleus.dev/conformance/quiet-bell/marginal_note",
            ],
            "version": "1.1.0",
        },
    ]


def test_private_vocabulary_and_nonpublic_boundary_are_closed() -> None:
    oracle = _load_oracle()
    assert set(oracle) == {
        "comparisons",
        "configuration",
        "declarations",
        "import_edges",
        "local_elaboration",
        "qualified_bindings",
        "sources",
        "versions",
    }
    for value in _objects(oracle):
        if value.get("outcome") == "REFUSE":
            assert value == REFUSE

    allowed_test_tokens = set(CONFIGURATION.values())
    allowed_comparisons = {"DIFFERENT", "NOT_CLAIMED", "SAME"}
    lowercase_hex = frozenset("0123456789abcdef")

    for value in _strings(oracle):
        if value.startswith("TEST_ONLY_SOURCE_BLOB_SHA256_"):
            digest = value.removeprefix("TEST_ONLY_SOURCE_BLOB_SHA256_")
            assert len(digest) == 64
            assert set(digest) <= lowercase_hex
        elif value.startswith("TEST_ONLY_"):
            assert value in allowed_test_tokens
        if value in allowed_comparisons:
            assert value in allowed_comparisons

    serialized = json.dumps(oracle, sort_keys=True)
    for forbidden in (
        "PUBLIC_",
        "artifact_bytes",
        "canonical_artifact",
        "compatibility",
        "runtime_wire",
        "wire_bytes",
    ):
        assert forbidden not in serialized

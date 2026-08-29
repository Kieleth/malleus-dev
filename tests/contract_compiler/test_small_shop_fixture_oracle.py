import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment"
)
INPUT_ROOT = FIXTURE_ROOT / "input"
ORACLE_ROOT = FIXTURE_ROOT / "oracle"
TBOX_ORACLE = ORACLE_ROOT / "tbox-expectations.json"
RET_ORACLE = ORACLE_ROOT / "ret-000-ret-010.json"
PRODUCTION_SOURCE_ROOT = ROOT / "src" / "malleus"

INPUT_MANIFEST_BYTE_LENGTH = 2481
INPUT_MANIFEST_SHA256 = (
    "sha256:7583bfbc6f9aff6382727a7befa333c82b73bed221d8958d6bb7e1a55d0549e8"
)
INPUT_CANDIDATE = {
    "commit": "39f41544ff47c60663d1eed7b4ec8959165f37e4",
    "parent": "f6b2bf96ae04351ec7ce29c080e57b58a8b7cea6",
    "tree": "4d50c14af6dd0f4c84dbd89c6407b02711d3bb35",
}
INPUT_COMPLETION = {
    "commit": "e5535033d8f1886271d827ddeed4662196410cdf",
    "completion_entry_hash": (
        "sha256:2d7e2f6500baaae317043be97e1850d5b0ba11efa60044fbd9c13db70514abe2"
    ),
    "completion_entry_id": "OVR-000222",
    "parent": "39f41544ff47c60663d1eed7b4ec8959165f37e4",
    "tree": "06ddc6bf9282481082ed6750a651e386020783b9",
}

PRIVATE_METADATA = {
    "artifact_class": "PRIVATE_FIXTURE_LOCAL_TEST_EVIDENCE",
    "authorship": "INDEPENDENTLY_HAND_AUTHORED",
    "compiler_input": False,
    "future_semantic_edits": (
        "INDEPENDENTLY_REVIEWED_EXPECTED_DELTA_EVIDENCE_REQUIRED"
    ),
    "publication_contract": "NON_PUBLIC_NO_COMPATIBILITY_CONTRACT",
    "wire_format": "PRIVATE_UNSTABLE_NO_PUBLIC_SCHEMA",
}

EXPECTED_TBOX_ORACLE = {
    "fixture_id": "OKG-FX001",
    "metadata": PRIVATE_METADATA,
    "tbox_expectations": {
        "controlled_baseline": {
            "disposition": "ACCEPT",
            "source_member": "tbox/small-shop.yaml",
        },
        "description_only": {
            "disposition": "ACCEPT",
            "exact_source_attestation": "DIFFERENT",
            "semantic_contract": "SAME",
            "source_member": "tbox/small-shop-description-only.yaml",
        },
        "root_instances": {
            "atomic": True,
            "disposition": "REFUSE",
            "refusal_basis": (
                "instances is not a listed schema-root field under accepted OD-008."
            ),
            "refused_root_field": "instances",
            "source_member": "tbox/small-shop-root-instances.yaml",
        },
    },
}

EXPECTED_RET_ORACLE = {
    "cases": {
        "RET-000": {
            "abox_logical_object_count": 0,
            "case_scope": "ONTOLOGY_ONLY",
            "disposition": "ACCEPT",
            "proposed_operation_value_count": 0,
        },
        "RET-010": {
            "derivation": {
                "evidence_sufficiency": "CLOSED_DERIVATION_PACKAGE",
                "review": {
                    "acceptance_authority": False,
                    "semantics": "PASSIVE_EXACT_REVIEW_NOT_ACCEPT_AUTHORITY",
                },
            },
            "expected_outputs": {
                "logical_entities": [
                    {
                        "attributes": {"order_number": "O1"},
                        "class": "SalesOrder",
                        "fixture_key": "O1",
                    },
                    {
                        "attributes": {"product_code": "X"},
                        "class": "InventoryUnit",
                        "fixture_key": "X1",
                    },
                ],
                "logical_relation": {
                    "class": "OrderContainsUnit",
                    "relation_type": "ORDER_CONTAINS_UNIT",
                    "source_fixture_key": "O1",
                    "target_fixture_key": "X1",
                },
                "temporal_provenance": ("FIXTURE_DERIVED_SYNTHETIC_YEAR_AND_UTC"),
                "valid_time": "2000-05-07T17:00:00Z",
            },
            "frozen_input_bindings": {
                "inventory_lookup": {
                    "inventory_unit_id": "X1",
                    "product_code": "X",
                },
                "selected_source": {
                    "event_id": "e27",
                    "inventory_unit_id": "X1",
                    "order_id": "O1",
                },
                "source_time": {
                    "grammar": "%d-%m %H:%M",
                    "synthetic_year": 2000,
                    "timezone": "UTC",
                    "value": "07-05 17:00",
                },
            },
            "retained_typed_red": {
                "event_object_expected": False,
                "event_to_entity_correlation_output_expected": False,
                "named_gap": "EVENT_ENTITY_CORRELATION_REPRESENTATION_UNSELECTED",
                "status": "TYPED_RED",
            },
        },
    },
    "fixture_id": "OKG-FX001",
    "metadata": PRIVATE_METADATA,
    "representation_boundaries": {
        "excluded_representations": [
            "MAPPINGS",
            "TRANSFORMATION_CODE",
            "IDENTITY_RULES",
            "RECIPES",
            "PROPOSED_OPERATION_BYTES_OR_ORDER",
            "CANDIDATES",
            "EVIDENCE_OUTCOMES",
            "PROTOCOL_EVENTS",
            "LEDGER_KG_REPLAY_OUTPUT",
        ],
        "fixture_key_semantics": "SOURCE_FIXTURE_KEYS_NOT_FINAL_OR_PUBLIC_IDS",
        "logical_relation_semantics": (
            "PRIVATE_LOGICAL_EXPECTATION_NOT_PUBLIC_ABOX_ENCODING"
        ),
    },
}

EXPECTED_INPUT_MANIFEST = {
    "fixture_id": "OKG-FX001",
    "input_set_id": "small-shop-ret-000-ret-010-v1",
    "limitations": [
        "Only the one retained e27 source row and one X1 reference row are in scope.",
        (
            "The source time omits year and timezone; separate fixture context records "
            "both assumptions."
        ),
        "These members contain inputs only and make no compiler or runtime result claim.",
    ],
    "members": [
        {
            "byte_length": 239,
            "media_type": "application/json",
            "path": "configuration/ret-010-selection.json",
            "role": "SCENARIO_SELECTION",
            "sha256": (
                "sha256:11000db0f0262137a7c0075987c7d7202452ab32232f8e94fa8821f80b8a1af7"
            ),
        },
        {
            "byte_length": 479,
            "media_type": "application/json",
            "path": "configuration/time-context.json",
            "role": "SOURCE_TIME_CONTEXT",
            "sha256": (
                "sha256:799cae6f980615a087e3d97bdc824ceda4410be2c93d92723829cd96c9a00561"
            ),
        },
        {
            "byte_length": 36,
            "media_type": "text/csv",
            "path": "sources/inventory-units.csv",
            "role": "DOMAIN_REFERENCE_DATA",
            "sha256": (
                "sha256:2e18a2a88c5964b80036799fe9f044d91e4dc790789b701df5f50a86c24a59ec"
            ),
        },
        {
            "byte_length": 118,
            "media_type": "application/x-ndjson",
            "path": "sources/warehouse.jsonl",
            "role": "SOURCE_OCCURRENCE_TRANSCRIPTION",
            "sha256": (
                "sha256:6ff31debb3603892de9d015f4e412da9f40a4add384f3f939b506ab7066e640e"
            ),
        },
        {
            "byte_length": 1137,
            "media_type": "application/yaml",
            "path": "tbox/small-shop-description-only.yaml",
            "role": "LINKML_DESCRIPTION_VARIANT",
            "sha256": (
                "sha256:e4a5898ccf85493c7a866c3891055ffe4ecb776361dfc1306b538627c7b6c74f"
            ),
        },
        {
            "byte_length": 1143,
            "media_type": "application/yaml",
            "path": "tbox/small-shop-root-instances.yaml",
            "role": "LINKML_ROOT_INSTANCES_VECTOR",
            "sha256": (
                "sha256:fbb37113a0546a0e1dced65579e830fbdc4087c918b4d98a534852a574eb961b"
            ),
        },
        {
            "byte_length": 1129,
            "media_type": "application/yaml",
            "path": "tbox/small-shop.yaml",
            "role": "LINKML_TBOX",
            "sha256": (
                "sha256:f374c7f1c1cba4ecbf747ca9471511307ea5cca1051540d5bf533a17360ca528"
            ),
        },
    ],
    "schema": "malleus.small-shop.input-set/v1",
    "source_attribution": {
        "doi": "10.1007/978-3-031-08848-3_9",
        "event_id": "e27",
        "source_locator": "Table 1",
        "transcription_classification": "CONTROLLED_FIXTURE_TRANSCRIPTION",
        "work_title": "Event Knowledge Graphs",
    },
}

ACCEPTED_DECISIONS = {
    "OD-002": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D02.json",
        "evidence_sha256": (
            "sha256:f6701459231240104809bbf7de8bc5a3d9440ccbbc9fcfca76e2f6dc1d92a044"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D02/manifest.json",
        "manifest_sha256": (
            "sha256:c649d411edd45a82a4d7559b5efc69ba8fade92327c998a685f4e57d7415ebb7"
        ),
        "workstream_id": "CC-D02",
    },
    "OD-003": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D03.json",
        "evidence_sha256": (
            "sha256:801c312367d8c95e01e0b423e25889a4a9e82963918b298fafc8c0905c70b20c"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D03/manifest.json",
        "manifest_sha256": (
            "sha256:e10dacbcdc6343d5360a47179bc9762732a30f0b05b91d70282eac776ac72146"
        ),
        "workstream_id": "CC-D03",
    },
    "OD-005": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D05.json",
        "evidence_sha256": (
            "sha256:30aabf6b43de8b0e371eb9a9ce5fa6ac09102d2b0c7136cfe2fd7171284fa7c1"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D05/manifest.json",
        "manifest_sha256": (
            "sha256:7daccbd334fb5486c75be38104116ebac14768a5cd10b51e6ea0ea3ad0d8f356"
        ),
        "workstream_id": "CC-D05",
    },
    "OD-006": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D06.json",
        "evidence_sha256": (
            "sha256:3cc09c2cdc0a5e4039f3870cf46b931e996c88e6db77e2db72d07d65c8b9d6cf"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D06/manifest.json",
        "manifest_sha256": (
            "sha256:0bd4ab014e972ea8b79a9d7ebe399af0a0c7a3652ecdbdb905ca00679f464adb"
        ),
        "workstream_id": "CC-D06",
    },
    "OD-008": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D08.json",
        "evidence_sha256": (
            "sha256:cd95e75149317baeb8b061db4169e0ba2070fc82201025a59926f274f527b2d2"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D08/manifest.json",
        "manifest_sha256": (
            "sha256:b771de9568edc9557ba14271a40780aaa3181b1a5a94d6cb446f5ed4b7f1b2e7"
        ),
        "workstream_id": "CC-D08",
    },
    "OD-010": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D10.json",
        "evidence_sha256": (
            "sha256:3ccb6f468936efac93f6eb4da6f1732aea9e56f05fa0c43437331c4c1905cab0"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D10/manifest.json",
        "manifest_sha256": (
            "sha256:75f3533acf2412b4e5770f3718587fde668591ccded77a56d60f30b0a2ee5bd9"
        ),
        "workstream_id": "CC-D10",
    },
    "OD-011": {
        "evidence_path": "design/contract_compiler/overseer/evidence/CC-D11.json",
        "evidence_sha256": (
            "sha256:cb13e6bd165ec348f448d5318ff2685329d7e9d3878e7cd87177eb20a4ee07f5"
        ),
        "manifest_path": "design/contract_compiler/workstreams/CC-D11/manifest.json",
        "manifest_sha256": (
            "sha256:cc86c841ff11cb5b19d37278ee7555aa3ed486b784e24e0095fce4e801438561"
        ),
        "workstream_id": "CC-D11",
    },
}


def _sha256(raw):
    return f"sha256:{hashlib.sha256(raw).hexdigest()}"


def _object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json_bytes(raw):
    assert not raw.startswith(b"\xef\xbb\xbf")
    return json.loads(
        raw.decode("utf-8"), object_pairs_hook=_object_without_duplicate_keys
    )


def _load_json(path):
    return _strict_json_bytes(path.read_bytes())


def _load_private_json(path):
    raw = path.read_bytes()
    assert raw.endswith(b"\n")
    assert b"\r" not in raw
    value = _strict_json_bytes(raw)
    canonical = (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    assert raw == canonical
    return value


def _git_bytes(*arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def _commit_coordinates(commit):
    lines = (
        _git_bytes("show", "-s", "--format=%H%n%T%n%P", commit)
        .decode("ascii")
        .splitlines()
    )
    assert len(lines) == 3
    return {"commit": lines[0], "tree": lines[1], "parent": lines[2]}


def _all_keys(value):
    if isinstance(value, dict):
        keys = set(value)
        for child in value.values():
            keys.update(_all_keys(child))
        return keys
    if isinstance(value, list):
        keys = set()
        for child in value:
            keys.update(_all_keys(child))
        return keys
    return set()


def _accepted_decision_evidence():
    evidence_by_decision = {}
    for decision_id, binding in ACCEPTED_DECISIONS.items():
        manifest_path = ROOT / binding["manifest_path"]
        evidence_path = ROOT / binding["evidence_path"]
        manifest_raw = manifest_path.read_bytes()
        evidence_raw = evidence_path.read_bytes()
        assert _sha256(manifest_raw) == binding["manifest_sha256"]
        assert _sha256(evidence_raw) == binding["evidence_sha256"]

        manifest = _strict_json_bytes(manifest_raw)
        evidence = _strict_json_bytes(evidence_raw)
        assert manifest["schema"] == "malleus.contract-compiler.workstream-card/v1"
        assert manifest["workstream_id"] == binding["workstream_id"]
        assert decision_id in manifest["responsibility"]
        assert manifest["authorization"]["class"] == "FORMAL"
        assert manifest["candidate"] == {"state": "NONE"}
        assert manifest["ledger"] == {"state": "NOT_STARTED"}
        assert manifest["scopes"] == []
        assert evidence["schema"] == "malleus.contract-compiler.verification-report/v1"
        assert evidence["workstream_id"] == binding["workstream_id"]
        assert evidence["checks"]
        assert all(check["result"] == "PASS" for check in evidence["checks"])
        evidence_by_decision[decision_id] = evidence
    return evidence_by_decision


def test_accepted_decision_bindings_are_exact():
    evidence = _accepted_decision_evidence()
    od008_checks = {check["check_id"]: check for check in evidence["OD-008"]["checks"]}
    assert (
        "unlisted fields and annotations refuse"
        in od008_checks["ccd08-closed-source-profile"]["observed"]
    )
    assert "descriptions" in od008_checks["ccd08-source-identity"]["observed"]
    assert (
        "do not enter semantic facts or candidate identity"
        in od008_checks["ccd08-source-identity"]["observed"]
    )

    od010_checks = {check["check_id"]: check for check in evidence["OD-010"]["checks"]}
    endpoint_observation = od010_checks["ccd10-endpoint-bearer-identity"]["observed"]
    assert "Event, Signal, Relation" in endpoint_observation
    assert "endpoints refuse" in endpoint_observation


def test_frozen_input_manifest_and_completed_coordinates_are_exact():
    manifest_path = INPUT_ROOT / "manifest.json"
    manifest_raw = manifest_path.read_bytes()
    assert len(manifest_raw) == INPUT_MANIFEST_BYTE_LENGTH
    assert _sha256(manifest_raw) == INPUT_MANIFEST_SHA256
    assert _strict_json_bytes(manifest_raw) == EXPECTED_INPUT_MANIFEST

    assert _commit_coordinates(INPUT_CANDIDATE["commit"]) == INPUT_CANDIDATE
    expected_completion_commit = {
        key: INPUT_COMPLETION[key] for key in ("commit", "tree", "parent")
    }
    assert _commit_coordinates(INPUT_COMPLETION["commit"]) == expected_completion_commit
    manifest_relative = manifest_path.relative_to(ROOT).as_posix()
    assert (
        _git_bytes("show", f"{INPUT_CANDIDATE['commit']}:{manifest_relative}")
        == manifest_raw
    )
    assert (
        _git_bytes("show", f"{INPUT_COMPLETION['commit']}:{manifest_relative}")
        == manifest_raw
    )
    input_relative = INPUT_ROOT.relative_to(ROOT).as_posix()
    unchanged = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            INPUT_CANDIDATE["commit"],
            "HEAD",
            "--",
            input_relative,
        ],
        cwd=ROOT,
        check=False,
    )
    assert unchanged.returncode == 0
    assert INPUT_COMPLETION["completion_entry_id"] == "OVR-000222"
    assert INPUT_COMPLETION["completion_entry_hash"] == (
        "sha256:2d7e2f6500baaae317043be97e1850d5b0ba11efa60044fbd9c13db70514abe2"
    )

    for member in EXPECTED_INPUT_MANIFEST["members"]:
        member_raw = (INPUT_ROOT / member["path"]).read_bytes()
        assert len(member_raw) == member["byte_length"]
        assert _sha256(member_raw) == member["sha256"]


def test_tbox_controls_are_closed_and_follow_accepted_od008():
    oracle = _load_private_json(TBOX_ORACLE)
    assert sorted(path.name for path in ORACLE_ROOT.iterdir()) == [
        RET_ORACLE.name,
        TBOX_ORACLE.name,
    ]
    assert oracle == EXPECTED_TBOX_ORACLE
    assert oracle["metadata"] == PRIVATE_METADATA

    baseline = (INPUT_ROOT / "tbox/small-shop.yaml").read_text(encoding="utf-8")
    description_only = (INPUT_ROOT / "tbox/small-shop-description-only.yaml").read_text(
        encoding="utf-8"
    )
    root_instances = (INPUT_ROOT / "tbox/small-shop-root-instances.yaml").read_text(
        encoding="utf-8"
    )
    baseline_description = (
        "description: Controlled TBox for the OKG-FX001 Small Shop Fulfilment fixture."
    )
    variant_description = (
        "description: Presentation-only description variant for the OKG-FX001 "
        "controlled TBox."
    )
    assert baseline.count(baseline_description) == 1
    assert description_only == baseline.replace(
        baseline_description, variant_description, 1
    )
    assert root_instances == baseline + "instances: {}\n"

    controls = oracle["tbox_expectations"]
    assert controls["controlled_baseline"]["disposition"] == "ACCEPT"
    assert controls["description_only"]["disposition"] == "ACCEPT"
    assert controls["description_only"]["exact_source_attestation"] == "DIFFERENT"
    assert controls["description_only"]["semantic_contract"] == "SAME"
    assert controls["root_instances"]["disposition"] == "REFUSE"
    assert controls["root_instances"]["atomic"] is True
    assert controls["root_instances"]["refused_root_field"] == "instances"
    assert (
        "not a listed schema-root field" in controls["root_instances"]["refusal_basis"]
    )
    assert {
        "diagnostic_code",
        "effective_contract_digest",
        "fact_array",
        "facts",
    }.isdisjoint(_all_keys(oracle))


def test_ret_000_ret_010_closed_hand_derivation_is_exact():
    oracle = _load_private_json(RET_ORACLE)
    assert oracle == EXPECTED_RET_ORACLE
    assert oracle["metadata"] == PRIVATE_METADATA

    selection = _load_json(INPUT_ROOT / "configuration/ret-010-selection.json")
    time_context = _load_json(INPUT_ROOT / "configuration/time-context.json")
    warehouse_lines = (INPUT_ROOT / "sources/warehouse.jsonl").read_bytes().splitlines()
    assert len(warehouse_lines) == 1
    warehouse = _strict_json_bytes(warehouse_lines[0])
    inventory_rows = list(
        csv.DictReader(
            (INPUT_ROOT / "sources/inventory-units.csv")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    )
    assert inventory_rows == [{"inventory_unit_id": "X1", "product_code": "X"}]
    inventory_lookup = inventory_rows[0]

    ret000 = oracle["cases"]["RET-000"]
    assert ret000["case_scope"] == "ONTOLOGY_ONLY"
    assert ret000["abox_logical_object_count"] == 0
    assert ret000["proposed_operation_value_count"] == 0

    ret010 = oracle["cases"]["RET-010"]
    frozen = ret010["frozen_input_bindings"]
    outputs = ret010["expected_outputs"]
    assert frozen["selected_source"] == {
        "event_id": selection["event_id"],
        "inventory_unit_id": selection["inventory_unit_id"],
        "order_id": selection["order_id"],
    }
    assert selection["source_member"] == "sources/warehouse.jsonl"
    assert selection["source_record_ordinal"] == 1
    assert selection["event_id"] == warehouse["event_id"]
    assert selection["order_id"] == warehouse["order"]
    assert selection["inventory_unit_id"] in warehouse["items"]
    assert frozen["inventory_lookup"] == inventory_lookup
    assert frozen["source_time"] == {
        "grammar": time_context["source_format"],
        "synthetic_year": time_context["fixture_year"],
        "timezone": time_context["timezone"],
        "value": warehouse["time"],
    }
    assert time_context["calendar"] == "PROLEPTIC_GREGORIAN"
    assert time_context["derived_value_classification"] == "FIXTURE_DERIVED"
    assert time_context["timezone_semantics"] == "FIXED_UTC_NO_DST"
    assert time_context["ambiguous_local_time"] == "REFUSE"
    assert time_context["nonexistent_local_time"] == "REFUSE"

    parsed_source_time = datetime.strptime(
        frozen["source_time"]["value"], frozen["source_time"]["grammar"]
    ).replace(year=frozen["source_time"]["synthetic_year"], tzinfo=timezone.utc)
    assert parsed_source_time.strftime("%Y-%m-%dT%H:%M:%SZ") == outputs["valid_time"]
    assert "valid_time" in outputs
    assert "valid_time" not in frozen
    assert "logical_relation" in outputs
    assert "logical_relation" not in frozen

    entities = outputs["logical_entities"]
    assert entities == [
        {
            "attributes": {"order_number": "O1"},
            "class": "SalesOrder",
            "fixture_key": selection["order_id"],
        },
        {
            "attributes": {"product_code": inventory_lookup["product_code"]},
            "class": "InventoryUnit",
            "fixture_key": selection["inventory_unit_id"],
        },
    ]
    relation = outputs["logical_relation"]
    assert relation == {
        "class": "OrderContainsUnit",
        "relation_type": "ORDER_CONTAINS_UNIT",
        "source_fixture_key": selection["order_id"],
        "target_fixture_key": selection["inventory_unit_id"],
    }
    assert outputs["temporal_provenance"] == ("FIXTURE_DERIVED_SYNTHETIC_YEAR_AND_UTC")
    assert ret010["derivation"] == {
        "evidence_sufficiency": "CLOSED_DERIVATION_PACKAGE",
        "review": {
            "acceptance_authority": False,
            "semantics": "PASSIVE_EXACT_REVIEW_NOT_ACCEPT_AUTHORITY",
        },
    }
    assert ret010["retained_typed_red"] == {
        "event_object_expected": False,
        "event_to_entity_correlation_output_expected": False,
        "named_gap": "EVENT_ENTITY_CORRELATION_REPRESENTATION_UNSELECTED",
        "status": "TYPED_RED",
    }

    boundaries = oracle["representation_boundaries"]
    assert boundaries["fixture_key_semantics"] == (
        "SOURCE_FIXTURE_KEYS_NOT_FINAL_OR_PUBLIC_IDS"
    )
    assert boundaries["logical_relation_semantics"] == (
        "PRIVATE_LOGICAL_EXPECTATION_NOT_PUBLIC_ABOX_ENCODING"
    )
    assert boundaries["excluded_representations"] == [
        "MAPPINGS",
        "TRANSFORMATION_CODE",
        "IDENTITY_RULES",
        "RECIPES",
        "PROPOSED_OPERATION_BYTES_OR_ORDER",
        "CANDIDATES",
        "EVIDENCE_OUTCOMES",
        "PROTOCOL_EVENTS",
        "LEDGER_KG_REPLAY_OUTPUT",
    ]
    assert {
        "candidates",
        "diagnostic_code",
        "effective_contract_digest",
        "evidence_outcomes",
        "final_id",
        "knowledge_graph",
        "mappings",
        "operation_bytes",
        "operation_order",
        "protocol_events",
        "public_abox",
        "public_schema",
        "recipes",
        "replay_output",
        "transformation_code",
    }.isdisjoint(_all_keys(oracle))


def test_oracles_are_not_inputs_or_production_read_targets():
    manifest = _load_json(INPUT_ROOT / "manifest.json")
    compiler_inputs = {member["path"] for member in manifest["members"]}
    assert compiler_inputs == {
        member["path"] for member in EXPECTED_INPUT_MANIFEST["members"]
    }
    assert all("oracle" not in member for member in compiler_inputs)
    assert TBOX_ORACLE.name not in compiler_inputs
    assert RET_ORACLE.name not in compiler_inputs

    oracle_relative_root = ORACLE_ROOT.relative_to(ROOT).as_posix()
    forbidden_references = (
        oracle_relative_root.encode("utf-8"),
        TBOX_ORACLE.name.encode("utf-8"),
        RET_ORACLE.name.encode("utf-8"),
    )
    scanned_sources = []
    for source_path in sorted(PRODUCTION_SOURCE_ROOT.rglob("*")):
        if not source_path.is_file() or "__pycache__" in source_path.parts:
            continue
        if source_path.suffix in {".pyc", ".pyo"}:
            continue
        scanned_sources.append(source_path)
        source_bytes = source_path.read_bytes()
        for forbidden_reference in forbidden_references:
            assert forbidden_reference not in source_bytes, source_path
    assert scanned_sources


def test_oracle_test_has_only_compiler_independent_imports():
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module is not None
            imported_roots.add(node.module.split(".", 1)[0])
    assert imported_roots == {
        "ast",
        "csv",
        "datetime",
        "hashlib",
        "json",
        "pathlib",
        "subprocess",
    }
    assert "re" not in imported_roots

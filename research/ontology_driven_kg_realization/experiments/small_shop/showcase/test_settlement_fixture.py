"""Integrity contract for the immutable Small Shop payment-settlement fixture."""

from __future__ import annotations

import csv
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from malleus._contract_binder import bind_contract
from malleus._contract_linkml_adapter import LinkMLImportReader, adapt_linkml_closure
from malleus._contract_pipeline import compile_binding
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    ResolvedSource,
    ResolverSelection,
    RootRequest,
    build_source_closure,
)


ROOT = Path(__file__).resolve().parents[5]
FIXTURE = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment_settlement_v1"
)
INPUT = FIXTURE / "input"
ORACLE = FIXTURE / "oracle/shop-payment-settlement.json"
CORRECTION_FIXTURE = FIXTURE.with_name("small_shop_fulfilment_correction_v1")
CORRECTION_TBOX = CORRECTION_FIXTURE / "input/tbox/small-shop-correction.yaml"

CORRECTION_TBOX_SHA256 = (
    "54e4e170d704056008296c91d1398b024d3a3c3897aba2640599375bf6f42b62"
)
SETTLEMENT_SHA256 = {
    "input/attribution.json": (
        "d8560cdc50b7d49c3164c47778564da4f08a81cc1a6ede9dfc4442f5edbd3cbe"
    ),
    "input/configuration/shop-payment-settlement-selection.json": (
        "173795759f135d09c35b42c6d222fafde26660ae82b2915cab67d5c3ff5421bc"
    ),
    "input/manifest.json": (
        "d823ee893d78908f78078052f480f0b3a7c63a752a157164dae0bc7905d61274"
    ),
    "input/sources/invoices.csv": (
        "048b6c70b94cddc026c656f51746794f5dfc1a70ce2372c5fed341b02973f175"
    ),
    "input/sources/payments.jsonl": (
        "3ad1935a2912eb698c14977ff9e42b3e49020912de0dad6f37ad10b4e27a060d"
    ),
    "input/tbox/small-shop-settlement.yaml": (
        "98dd530aa249763be24ff16a0ff4848c0821dc0150bf09ef2ee5a3f19e66b956"
    ),
    "oracle/shop-payment-settlement.json": (
        "d74b3a2c201bf083069383fe31797f8d848050279d5877bbf864ae316dfc16e6"
    ),
}
INPUT_MEMBERS = {
    "attribution.json": ("SOURCE_ATTRIBUTION", "application/json"),
    "configuration/shop-payment-settlement-selection.json": (
        "SCENARIO_SELECTION",
        "application/json",
    ),
    "sources/invoices.csv": ("DOMAIN_REFERENCE_DATA", "text/csv"),
    "sources/payments.jsonl": (
        "SOURCE_OCCURRENCE_TRANSCRIPTION",
        "application/x-ndjson",
    ),
    "tbox/small-shop-settlement.yaml": (
        "LINKML_TBOX_EXTENSION",
        "application/yaml",
    ),
}


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes(), object_pairs_hook=_unique_object)
    assert isinstance(value, dict)
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    values = [
        json.loads(line, object_pairs_hook=_unique_object)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    assert all(isinstance(value, dict) for value in values)
    return values


def test_fixture_bytes_are_exactly_frozen() -> None:
    assert {
        relative: _digest(FIXTURE / relative) for relative in SETTLEMENT_SHA256
    } == SETTLEMENT_SHA256


def test_manifest_is_a_closed_digest_bound_input_set() -> None:
    manifest = _load_json(INPUT / "manifest.json")
    assert set(manifest) == {
        "fixture_id",
        "input_set_id",
        "limitations",
        "members",
        "schema",
        "source_attribution",
        "tbox_import",
    }
    assert manifest["schema"] == "malleus.small-shop.input-set/v1"
    assert manifest["fixture_id"] == "OKG-FX001"
    assert manifest["input_set_id"] == "shop-payment-settlement-v1"
    assert manifest["limitations"] == [
        (
            "Only invoice identities I1 and I2 and the e30 co-occurrence of P1, "
            "I1, and I2 are source claims in scope."
        ),
        (
            "The directed PAYMENT_SETTLES_INVOICE predicate is fixture-defined "
            "semantics, not a source-native Event Knowledge Graph edge."
        ),
        (
            "The selected case has exactly two invoices and claims no generic "
            "collection expansion, fan-out, or cardinality rule."
        ),
        (
            "The publication establishes event order but no accepted timestamp, "
            "invoice value, or payment value, so temporal semantics are ORDER_ONLY."
        ),
        (
            "These members contain inputs only and make no compiler, protocol, "
            "ledger, runtime, or accepted-graph result claim."
        ),
    ]
    assert manifest["source_attribution"] == {
        "attribution_member": "attribution.json",
        "doi": "10.1007/978-3-031-08848-3_9",
        "source_locator": "Table 1",
        "transcription_classification": "CONTROLLED_FIXTURE_TRANSCRIPTION",
        "work_title": (
            "Process Mining over Multiple Behavioral Dimensions with Event "
            "Knowledge Graphs"
        ),
    }
    assert manifest["tbox_import"] == {
        "byte_length": 1009,
        "import_literal": "small-shop-correction",
        "input_set_id": "shop-supplier-order-correction-v1",
        "path": (
            "research/ontology_driven_kg_realization/fixtures/"
            "small_shop_fulfilment_correction_v1/input/tbox/"
            "small-shop-correction.yaml"
        ),
        "sha256": f"sha256:{CORRECTION_TBOX_SHA256}",
    }

    members = manifest["members"]
    assert isinstance(members, list)
    assert [member["path"] for member in members] == sorted(INPUT_MEMBERS)
    assert len({member["path"] for member in members}) == len(INPUT_MEMBERS)
    for member in members:
        assert set(member) == {
            "byte_length",
            "media_type",
            "path",
            "role",
            "sha256",
        }
        relative = member["path"]
        assert isinstance(relative, str)
        path = PurePosixPath(relative)
        assert not path.is_absolute() and ".." not in path.parts
        assert INPUT_MEMBERS[relative] == (member["role"], member["media_type"])
        target = INPUT / relative
        assert target.is_file() and not target.is_symlink()
        assert member["byte_length"] == len(target.read_bytes())
        assert member["sha256"] == f"sha256:{_digest(target)}"

    actual_inputs = {
        path.relative_to(INPUT).as_posix()
        for path in INPUT.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    assert actual_inputs == set(INPUT_MEMBERS)
    assert _digest(CORRECTION_TBOX) == CORRECTION_TBOX_SHA256


def test_source_rows_are_strict_and_assert_only_cooccurrence() -> None:
    with (INPUT / "sources/invoices.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["invoice_id"]
        assert list(reader) == [{"invoice_id": "I1"}, {"invoice_id": "I2"}]

    payments = _load_jsonl(INPUT / "sources/payments.jsonl")
    assert payments == [
        {
            "event_id": "e30",
            "invoice_ids": ["I1", "I2"],
            "payment_id": "P1",
        }
    ]
    assert set(payments[0]) == {"event_id", "invoice_ids", "payment_id"}
    assert "settle" not in (INPUT / "sources/payments.jsonl").read_text().lower()


def test_selection_is_closed_zero_based_source_order() -> None:
    selection = _load_json(
        INPUT / "configuration/shop-payment-settlement-selection.json"
    )
    assert selection == {
        "event_id": "e30",
        "invoice_ids": ["I1", "I2"],
        "invoice_record_ordinals": [0, 1],
        "invoice_source_member": "sources/invoices.csv",
        "ordinal_base": 0,
        "payment_id": "P1",
        "payment_record_ordinal": 0,
        "payment_source_member": "sources/payments.jsonl",
        "record_order": "SOURCE_ORDER",
        "schema": "malleus.small-shop.settlement-selection/v1",
        "selection_id": "SHOP-PAYMENT-SETTLEMENT",
        "settlement_semantics": "FIXTURE_DEFINED_DIRECTED_PAYMENT_TO_INVOICE",
        "temporal_semantics": "ORDER_ONLY",
    }

    with (INPUT / selection["invoice_source_member"]).open(
        encoding="utf-8", newline=""
    ) as stream:
        invoices = list(csv.DictReader(stream))
    payments = _load_jsonl(INPUT / selection["payment_source_member"])
    selected_invoices = [
        invoices[ordinal]["invoice_id"]
        for ordinal in selection["invoice_record_ordinals"]
    ]
    assert selected_invoices == selection["invoice_ids"]
    payment = payments[selection["payment_record_ordinal"]]
    assert payment == {
        "event_id": selection["event_id"],
        "invoice_ids": selection["invoice_ids"],
        "payment_id": selection["payment_id"],
    }


def test_attribution_separates_source_claims_from_fixture_semantics() -> None:
    attribution = _load_json(INPUT / "attribution.json")
    assert attribution["published_source_claims"] == [
        {"invoice_id": "I1"},
        {"invoice_id": "I2"},
        {
            "cooccurring_entity_ids": ["P1", "I1", "I2"],
            "event_id": "e30",
        },
    ]
    assert attribution["fixture_defined_semantics"] == [
        {
            "relation_type": "PAYMENT_SETTLES_INVOICE",
            "source_id": "P1",
            "target_id": "I1",
        },
        {
            "relation_type": "PAYMENT_SETTLES_INVOICE",
            "source_id": "P1",
            "target_id": "I2",
        },
    ]
    assert attribution["interpretation_authority"] == (
        "FIXTURE_DECLARATION_NOT_SOURCE_NATIVE_RELATION"
    )
    assert attribution["source_locator"] == "Table 1"
    assert attribution["doi"] == "10.1007/978-3-031-08848-3_9"
    assert attribution["excluded_claims"] == [
        "ABSOLUTE_OR_CALENDAR_TIME",
        "ACCEPTED_KNOWLEDGE_OR_PROTOCOL_OUTCOME",
        "EVENT_GRAPH_NODE",
        "GENERIC_FAN_OUT_OR_CARDINALITY",
        "INVOICE_VALUE",
        "NATIVE_SETTLEMENT_EDGE",
        "PAYMENT_VALUE",
    ]


class _ExactResolver:
    def __init__(self, sources: dict[str, bytes]) -> None:
        self._sources = sources

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        locator = (
            request.requested_locator
            if isinstance(request, RootRequest)
            else request.literal_import
        )
        try:
            source = self._sources[locator]
        except KeyError as error:
            raise CollaboratorRefusal(locator) from error
        return ResolvedSource(locator, source, "application/yaml")


def test_tbox_adds_only_the_three_settlement_classes_and_exact_relation() -> None:
    settlement = INPUT / "tbox/small-shop-settlement.yaml"
    base = FIXTURE.with_name("small_shop_fulfilment") / "input/tbox/small-shop.yaml"
    authored = yaml.safe_load(settlement.read_bytes())
    assert set(authored["classes"]) == {
        "Invoice",
        "Payment",
        "PaymentSettlesInvoiceRelation",
    }
    assert authored["slots"] == {
        "invoice_number": {"range": "string"},
        "payment_number": {"range": "string"},
    }
    assert "enums" not in authored
    assert authored["imports"] == ["small-shop-correction"]
    assert authored["classes"]["Invoice"] == {
        "is_a": "Entity",
        "slots": ["invoice_number"],
        "slot_usage": {"invoice_number": {"required": True}},
    }
    assert authored["classes"]["Payment"] == {
        "is_a": "Entity",
        "slots": ["payment_number"],
        "slot_usage": {"payment_number": {"required": True}},
    }

    trusted_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    closure = build_source_closure(
        requested_locator="small-shop-settlement",
        selection=ResolverSelection(
            resolver_id="SHOP_PAYMENT_SETTLEMENT_EXACT_RESOLVER",
            profile_version="PRIVATE_V0",
            configuration_id="SHOP_PAYMENT_SETTLEMENT_NO_AMBIENT_IO",
        ),
        resolver=_ExactResolver(
            {
                "small-shop-settlement": settlement.read_bytes(),
                "small-shop-correction": CORRECTION_TBOX.read_bytes(),
                "small-shop": base.read_bytes(),
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": trusted_types,
            }
        ),
        import_reader=LinkMLImportReader(),
    )
    result = compile_binding(bind_contract(adapt_linkml_closure(closure)))
    namespace = "https://malleus.dev/schema/small-shop-fulfilment-settlement"
    foundation = "https://malleus.dev/schema"
    payment = f"{namespace}/Payment"
    invoice = f"{namespace}/Invoice"
    relation = f"{namespace}/PaymentSettlesInvoiceRelation"

    assert result.view.is_subtype_of(payment, f"{foundation}/Entity")
    assert result.view.is_subtype_of(invoice, f"{foundation}/Entity")
    assert result.view.is_subtype_of(relation, f"{foundation}/Relation")
    assert result.view.get_slot_constraint(
        invoice, f"{namespace}/invoice_number"
    ).required
    assert result.view.get_slot_constraint(
        payment, f"{namespace}/payment_number"
    ).required
    relation_type = result.view.get_slot_constraint(
        relation, f"{foundation}/relation_type"
    )
    source = result.view.get_slot_constraint(relation, f"{foundation}/source_id")
    target = result.view.get_slot_constraint(relation, f"{foundation}/target_id")
    assert relation_type.required
    assert relation_type.equals_string == "PAYMENT_SETTLES_INVOICE"
    assert source.required and source.range_id == payment
    assert target.required and target.range_id == invoice


def test_independent_expectation_is_not_an_input_and_states_nonclaims() -> None:
    oracle = _load_json(ORACLE)
    assert oracle["fixture_id"] == "OKG-FX001"
    assert oracle["case_id"] == "SHOP-PAYMENT-SETTLEMENT"
    assert oracle["metadata"] == {
        "artifact_class": "PRIVATE_FIXTURE_LOCAL_TEST_EVIDENCE",
        "authorship": "INDEPENDENTLY_HAND_AUTHORED",
        "compiler_input": False,
        "publication_contract": "NON_PUBLIC_NO_COMPATIBILITY_CONTRACT",
        "wire_format": "PRIVATE_UNSTABLE_NO_PUBLIC_SCHEMA",
    }
    assert oracle["expected_existing_base"] == {
        "logical_entities": [
            {
                "attributes": {"invoice_number": "I1"},
                "class": "Invoice",
                "fixture_key": "I1",
            },
            {
                "attributes": {"invoice_number": "I2"},
                "class": "Invoice",
                "fixture_key": "I2",
            },
        ]
    }
    assert oracle["expected_outputs"] == {
        "logical_entities": [
            {
                "attributes": {"payment_number": "P1"},
                "class": "Payment",
                "fixture_key": "P1",
            }
        ],
        "logical_relations": [
            {
                "class": "PaymentSettlesInvoiceRelation",
                "fixture_key": "P1:I1",
                "relation_type": "PAYMENT_SETTLES_INVOICE",
                "source_fixture_key": "P1",
                "target_fixture_key": "I1",
            },
            {
                "class": "PaymentSettlesInvoiceRelation",
                "fixture_key": "P1:I2",
                "relation_type": "PAYMENT_SETTLES_INVOICE",
                "source_fixture_key": "P1",
                "target_fixture_key": "I2",
            },
        ],
    }
    assert oracle["semantic_basis"] == (
        "FIXTURE_DEFINED_DIRECTION_FROM_SOURCE_COOCCURRENCE"
    )
    assert oracle["excluded_claims"] == [
        "ACCEPTED_KNOWLEDGE_OR_PROTOCOL_OUTCOME",
        "GENERIC_COLLECTION_EXPANSION",
        "GENERIC_SETTLEMENT_CARDINALITY",
        "NATIVE_EVENT_KNOWLEDGE_GRAPH_SETTLEMENT_EDGE",
        "PROPOSED_OPERATION_BYTES_OR_ORDER",
        "SOURCE_ASSERTED_RELATION_DIRECTION",
    ]

    manifest = _load_json(INPUT / "manifest.json")
    member_paths = {member["path"] for member in manifest["members"]}
    assert all(not path.startswith("oracle/") for path in member_paths)
    assert ORACLE.is_file() and INPUT not in ORACLE.parents
    oracle_digest = _digest(ORACLE)
    assert all(
        oracle_digest not in path.read_text(encoding="utf-8")
        for path in INPUT.rglob("*")
        if path.is_file()
    )


def test_fixture_contains_no_undeclared_files_or_symlinks() -> None:
    expected = {
        "input/attribution.json",
        "input/configuration/shop-payment-settlement-selection.json",
        "input/manifest.json",
        "input/sources/invoices.csv",
        "input/sources/payments.jsonl",
        "input/tbox/small-shop-settlement.yaml",
        "oracle/shop-payment-settlement.json",
    }
    actual = {
        path.relative_to(FIXTURE).as_posix()
        for path in FIXTURE.rglob("*")
        if path.is_file()
    }
    assert actual == expected
    assert all(not path.is_symlink() for path in FIXTURE.rglob("*"))

"""Integrity contract for the additive Small Shop supplier-order correction fixture."""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path, PurePosixPath

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
BASE_FIXTURE = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment"
)
FIXTURE = BASE_FIXTURE.with_name("small_shop_fulfilment_correction_v1")
INPUT = FIXTURE / "input"
ORACLE = FIXTURE / "oracle/shop-supplier-order-correction.json"
MAPPING = Path(__file__).with_name("mapping.json")

BASELINE_SHA256 = {
    "input/configuration/ret-010-selection.json": (
        "11000db0f0262137a7c0075987c7d7202452ab32232f8e94fa8821f80b8a1af7"
    ),
    "input/configuration/time-context.json": (
        "799cae6f980615a087e3d97bdc824ceda4410be2c93d92723829cd96c9a00561"
    ),
    "input/manifest.json": (
        "7583bfbc6f9aff6382727a7befa333c82b73bed221d8958d6bb7e1a55d0549e8"
    ),
    "input/sources/inventory-units.csv": (
        "2e18a2a88c5964b80036799fe9f044d91e4dc790789b701df5f50a86c24a59ec"
    ),
    "input/sources/warehouse.jsonl": (
        "6ff31debb3603892de9d015f4e412da9f40a4add384f3f939b506ab7066e640e"
    ),
    "input/tbox/small-shop-description-only.yaml": (
        "e4a5898ccf85493c7a866c3891055ffe4ecb776361dfc1306b538627c7b6c74f"
    ),
    "input/tbox/small-shop-root-instances.yaml": (
        "fbb37113a0546a0e1dced65579e830fbdc4087c918b4d98a534852a574eb961b"
    ),
    "input/tbox/small-shop.yaml": (
        "f374c7f1c1cba4ecbf747ca9471511307ea5cca1051540d5bf533a17360ca528"
    ),
    "oracle/ret-000-ret-010.json": (
        "4565c5f2dd84670c762c0a53e5a0868fe8cab6f1781a9757ecb41581e7f32fcc"
    ),
    "oracle/tbox-expectations.json": (
        "0a8d3fdae6f16117643d898eb7576022e61700d3f83d286ff164fb66f6ae0f31"
    ),
}

CORRECTION_SHA256 = {
    "input/attribution.json": (
        "5c0bec7e8c3783903db211128b810c3b6dea262a95d7b7cd9cd4cf571775b942"
    ),
    "input/configuration/shop-supplier-order-correction-selection.json": (
        "7f99da452836bac16fccbebca0cb43b995cdfc192d5364203a1ff319832987a2"
    ),
    "input/manifest.json": (
        "3ae5281e505882ba14fab159ff85e7f433ba79a6936c1113a5f0e54a1cc8ad13"
    ),
    "input/sources/supplier-order-history.jsonl": (
        "a441c49f325670e09d9fc09fd8e6510669258bed1d5532cfb2b1104c4eceb081"
    ),
    "input/tbox/small-shop-correction.yaml": (
        "54e4e170d704056008296c91d1398b024d3a3c3897aba2640599375bf6f42b62"
    ),
    "oracle/shop-supplier-order-correction.json": (
        "b08b4b02a82d7b64c8f49481bdd3ceffb4b255e085378544808a5c4958843518"
    ),
}
MAPPING_SHA256 = "77bcc53ef39b301a940ee051c1afd6d3e08e90ba6e8bd344a7ba14ff6f101795"

INPUT_MEMBERS = {
    "attribution.json": ("SOURCE_ATTRIBUTION", "application/json"),
    "configuration/shop-supplier-order-correction-selection.json": (
        "SCENARIO_SELECTION",
        "application/json",
    ),
    "sources/supplier-order-history.jsonl": (
        "SOURCE_OCCURRENCE_TRANSCRIPTION",
        "application/x-ndjson",
    ),
    "tbox/small-shop-correction.yaml": (
        "LINKML_TBOX_EXTENSION",
        "application/yaml",
    ),
}


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _load_jsonl(path: Path) -> list[dict[str, object]]:
    values = [json.loads(line) for line in path.read_text().splitlines()]
    assert all(isinstance(value, dict) for value in values)
    return values


def test_existing_ret010_bundle_remains_byte_identical() -> None:
    assert {
        relative: _digest(BASE_FIXTURE / relative)
        for relative in BASELINE_SHA256
    } == BASELINE_SHA256


def test_correction_fixture_and_mapping_have_exact_frozen_bytes() -> None:
    assert {
        relative: _digest(FIXTURE / relative)
        for relative in CORRECTION_SHA256
    } == CORRECTION_SHA256
    assert _digest(MAPPING) == MAPPING_SHA256


def test_bounded_supplier_order_case_does_not_claim_the_broader_ret030_stage() -> (
    None
):
    artifacts = [
        *(path for path in FIXTURE.rglob("*") if path.is_file()),
        MAPPING,
    ]
    for artifact in artifacts:
        text = artifact.read_text(encoding="utf-8")
        assert "RET-030" not in text
        assert "ret-030" not in text


def test_manifest_binds_the_complete_additive_input_set() -> None:
    manifest = _load_json(INPUT / "manifest.json")
    assert set(manifest) == {
        "fixture_id",
        "input_set_id",
        "limitations",
        "members",
        "schema",
        "source_attribution",
    }
    assert manifest["schema"] == "malleus.small-shop.input-set/v1"
    assert manifest["fixture_id"] == "OKG-FX001"
    assert manifest["input_set_id"] == (
        "shop-supplier-order-correction-v1"
    )
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
        assert not path.is_absolute() and "." not in path.parts
        assert INPUT_MEMBERS[relative] == (member["role"], member["media_type"])
        target = INPUT / relative
        assert target.is_file() and not target.is_symlink()
        assert member["byte_length"] == len(target.read_bytes())
        assert member["sha256"] == f"sha256:{_digest(target)}"


def test_source_and_attribution_contain_only_the_accepted_published_story() -> None:
    source = _load_jsonl(INPUT / "sources/supplier-order-history.jsonl")
    assert source == [
        {
            "event_id": "e4",
            "product_code": "Y",
            "quantity": 1,
            "supplier_order_id": "B",
        },
        {
            "event_id": "e7",
            "product_code": "Y",
            "quantity": 2,
            "supplier_order_id": "B",
        },
    ]
    assert all(
        set(record) == {
            "event_id",
            "product_code",
            "quantity",
            "supplier_order_id",
        }
        for record in source
    )

    attribution = _load_json(INPUT / "attribution.json")
    assert attribution["accepted_claims"] == [
        {
            "event_id": "e4",
            "product_code": "Y",
            "quantity": 1,
            "supplier_order_id": "B",
        },
        {
            "event_id": "e7",
            "product_code": "Y",
            "quantity": 2,
            "supplier_order_id": "B",
        },
        {
            "earlier_event_id": "e4",
            "later_event_id": "e7",
            "relation": "SUPERSEDES",
        },
    ]
    assert attribution["excluded_claims"] == [
        "ABSOLUTE_OR_CALENDAR_TIME",
        "ACTOR_IDENTITY",
        "DEMAND_OR_SUPPLY_GAP",
        "ACTION_OR_EFFECT",
        "INVOICE_VALUE",
        "EVENT_GRAPH_NODE",
    ]


def test_selection_is_zero_based_source_order_with_order_only_time() -> None:
    selection = _load_json(
        INPUT / "configuration/shop-supplier-order-correction-selection.json"
    )
    source = _load_jsonl(INPUT / selection["source_member"])

    assert selection == {
        "correction": {
            "event_id": "e7",
            "source_record_ordinal": 1,
            "supersedes_event_id": "e4",
        },
        "initial": {"event_id": "e4", "source_record_ordinal": 0},
        "ordinal_base": 0,
        "record_order": "SOURCE_ORDER",
        "schema": "malleus.small-shop.correction-selection/v1",
        "selection_id": "SHOP-SUPPLIER-ORDER-CORRECTION",
        "source_member": "sources/supplier-order-history.jsonl",
        "temporal_semantics": "ORDER_ONLY",
    }
    assert source[selection["initial"]["source_record_ordinal"]]["event_id"] == "e4"
    assert source[selection["correction"]["source_record_ordinal"]]["event_id"] == (
        "e7"
    )


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


def test_linkml_extension_compiles_as_a_real_domain_contract() -> None:
    correction = INPUT / "tbox/small-shop-correction.yaml"
    base = BASE_FIXTURE / "input/tbox/small-shop.yaml"
    trusted_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    sources = {
        "small-shop-correction": correction.read_bytes(),
        "small-shop": base.read_bytes(),
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": trusted_types,
    }
    closure = build_source_closure(
        requested_locator="small-shop-correction",
        selection=ResolverSelection(
            resolver_id="SHOP_SUPPLIER_ORDER_CORRECTION_EXACT_RESOLVER",
            profile_version="PRIVATE_V0",
            configuration_id="SHOP_SUPPLIER_ORDER_CORRECTION_NO_AMBIENT_IO",
        ),
        resolver=_ExactResolver(sources),
        import_reader=LinkMLImportReader(),
    )
    result = compile_binding(bind_contract(adapt_linkml_closure(closure)))
    namespace = "https://malleus.dev/schema/small-shop-fulfilment-correction"
    foundation = "https://malleus.dev/schema"
    subject = f"{namespace}/SupplierOrderState"

    assert result.view.is_subtype_of(subject, f"{foundation}/Entity")
    for slot in ("supplier_order_id", "ordered_quantity", "source_occurrence_id"):
        assert result.view.get_slot_constraint(subject, f"{namespace}/{slot}").required
    assert result.view.get_slot_constraint(
        subject,
        "https://malleus.dev/schema/small-shop-fulfilment/product_code",
    ).required


def test_mapping_is_declarative_private_and_oracle_independent() -> None:
    mapping = _load_json(MAPPING)
    manifest_identity = f"sha256:{_digest(INPUT / 'manifest.json')}"

    assert set(mapping) == {
        "changes",
        "compiler",
        "fixture_id",
        "grammar",
        "history_base",
        "input_manifest_sha256",
        "input_set_id",
        "publication_contract",
        "selection_member",
        "source",
        "state_bindings",
    }
    assert mapping["grammar"] == (
        "malleus.small-shop.supplier-order-correction-mapping/private-v0"
    )
    assert mapping["fixture_id"] == "OKG-FX001"
    assert mapping["input_manifest_sha256"] == manifest_identity
    assert mapping["publication_contract"] == (
        "PRIVATE_FIXTURE_LOCAL_NO_PUBLIC_ABOX_FORMAT"
    )
    assert mapping["source"] == {
        "member": "sources/supplier-order-history.jsonl",
        "ordinal_base": 0,
        "record_order": "SOURCE_ORDER",
    }
    assert [change["valid_time"] for change in mapping["changes"]] == [
        {"kind": "ORDER_ONLY", "value": "e4"},
        {"kind": "ORDER_ONLY", "value": "e7"},
    ]
    assert set(mapping["changes"][0]) == {
        "change_set_id",
        "kind",
        "operations",
        "source_record_ordinal",
        "supersedes",
        "valid_time",
    }
    assert set(mapping["changes"][1]) == set(mapping["changes"][0])
    assert set(mapping["changes"][0]["operations"][0]) == {
        "depends_on",
        "operation_id",
        "operation_type",
        "ordinal",
        "properties",
        "record_id",
        "record_type",
    }
    assert set(mapping["changes"][1]["operations"][0]) == {
        *set(mapping["changes"][0]["operations"][0]),
        "supersedes_record_id",
    }
    assert mapping["changes"][0]["supersedes"] == []
    assert mapping["changes"][1]["supersedes"] == [
        "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4"
    ]
    assert mapping["changes"][1]["operations"][0]["supersedes_record_id"] == (
        "supplier-order-state:B:e4"
    )
    assert "oracle" not in MAPPING.read_text().lower()
    assert _digest(ORACLE) not in MAPPING.read_text()


def test_hand_authored_oracle_states_history_current_state_and_limits() -> None:
    oracle = _load_json(ORACLE)
    assert oracle["fixture_id"] == "OKG-FX001"
    assert oracle["case_id"] == "SHOP-SUPPLIER-ORDER-CORRECTION"
    assert oracle["metadata"] == {
        "artifact_class": "PRIVATE_FIXTURE_LOCAL_TEST_EVIDENCE",
        "authorship": "INDEPENDENTLY_HAND_AUTHORED",
        "compiler_input": False,
        "publication_contract": "NON_PUBLIC_NO_COMPATIBILITY_CONTRACT",
        "wire_format": "PRIVATE_UNSTABLE_NO_PUBLIC_SCHEMA",
    }
    assert oracle["expected_states"] == [
        {
            "attributes": {
                "ordered_quantity": 1,
                "product_code": "Y",
                "source_occurrence_id": "e4",
                "supplier_order_id": "B",
            },
            "class": "SupplierOrderState",
            "fixture_state_key": "B@e4",
            "valid_time": {"kind": "ORDER_ONLY", "value": "e4"},
        },
        {
            "attributes": {
                "ordered_quantity": 2,
                "product_code": "Y",
                "source_occurrence_id": "e7",
                "supplier_order_id": "B",
            },
            "class": "SupplierOrderState",
            "fixture_state_key": "B@e7",
            "valid_time": {"kind": "ORDER_ONLY", "value": "e7"},
        },
    ]
    assert oracle["expected_supersession"] == {
        "earlier_fixture_state_key": "B@e4",
        "later_fixture_state_key": "B@e7",
    }
    assert oracle["expected_current_fixture_state_key"] == "B@e7"
    assert oracle["preservation"] == {
        "baseline_ret010_record_ids": ["O1", "X1", "contains:O1:X1"],
        "expected_effect": "UNCHANGED",
    }
    assert set(oracle["excluded_claims"]) == {
        "ACTIONS_OR_EXTERNAL_EFFECTS",
        "DEMAND_OR_SUPPLY_GAP",
        "EVENT_NODE_REPRESENTATION",
        "INVOICE_OR_PAYMENT_CORRECTION",
        "SEMANTIC_REENTRY",
    }


def test_oracle_is_not_an_input_or_mapping_dependency() -> None:
    manifest = _load_json(INPUT / "manifest.json")
    member_paths = {member["path"] for member in manifest["members"]}
    assert all(not path.startswith("oracle/") for path in member_paths)
    assert ORACLE.is_file()
    assert INPUT not in ORACLE.parents


def test_fixture_contains_no_undeclared_files_or_symlinks() -> None:
    expected = {
        "input/attribution.json",
        "input/configuration/shop-supplier-order-correction-selection.json",
        "input/manifest.json",
        "input/sources/supplier-order-history.jsonl",
        "input/tbox/small-shop-correction.yaml",
        "oracle/shop-supplier-order-correction.json",
    }
    actual = {
        path.relative_to(FIXTURE).as_posix()
        for path in FIXTURE.rglob("*")
        if path.is_file()
    }
    assert actual == expected
    assert all(not path.is_symlink() for path in FIXTURE.rglob("*"))

"""Actual compilation of the local action subtype, not action authorization."""

from copy import deepcopy
from importlib.resources import files
from pathlib import Path

import pytest

import malleus.compiler as api
from malleus.assent import make_record
from malleus.ledger import content_digest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIELDS = {
    "logical_source_id": "S0",
    "supplier_order_id": "B",
    "product_code": "Y",
    "expected_quantity": 1,
    "requested_quantity": 2,
    "expected_source_digest": (
        "sha256:edc05a0c3b95e04a54cd83fb5075ec91795680497c925e04635562b35d057e85"
    ),
    "new_source_occurrence_id": "reentry-amendment-1",
}


@pytest.fixture(scope="module")
def action_compilation():
    return api.compile_linkml_contract(
        root_locator="supplier-amendment",
        sources={
            "supplier-amendment": (HERE / "supplier-action.yaml").read_bytes(),
            "assent": (ROOT / "ontology/assent.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


def action_record():
    # Explicit shape specimen. Its policy digest is not an applied authority.
    return make_record(
        "SupplierOrderAmendment",
        id="action:supplier-schema-specimen",
        event_id="event:supplier-schema-specimen",
        generated_at="2026-09-08T00:00:00Z",
        actor_id="actor:supplier-schema-specimen",
        role="proposer",
        source_record_ids=[],
        action_type="AMEND_SUPPLIER_ORDER",
        action_payload_hash=content_digest(FIELDS),
        action_key="episode:supplier-schema-specimen",
        revision=1,
        authorization_policy_id="policy:supplier-schema-specimen",
        authorization_policy_hash=content_digest({"purpose": "shape specimen only"}),
        **FIELDS,
    )


def test_real_contract_preserves_the_existing_action_identity(action_compilation):
    view = action_compilation.view
    assert view.is_subtype_of("SupplierOrderAmendment", "ActionProposal")
    assert not view.get_type("SupplierOrderAmendment").abstract
    assert view.get_type("ActionProposal").abstract
    assert not view.has_type("LocalAction")
    record = action_record()
    before = deepcopy(record)
    assert view.validate_instance("SupplierOrderAmendment", record) == []
    loaded = api.load_validated_contract_artifact(
        action_compilation.artifact.artifact_bytes
    )
    assert loaded.validate_instance("SupplierOrderAmendment", record) == []
    assert record == before


@pytest.mark.parametrize("field", list(FIELDS))
def test_every_amendment_field_is_required(action_compilation, field):
    record = action_record()
    del record[field]
    assert action_compilation.view.validate_instance("SupplierOrderAmendment", record)


@pytest.mark.parametrize(
    "field,value",
    [
        ("expected_quantity", True),
        ("requested_quantity", False),
        ("expected_quantity", "1"),
        ("requested_quantity", 2.5),
        ("logical_source_id", 7),
        ("supplier_order_id", False),
        ("product_code", []),
        ("expected_source_digest", None),
        ("new_source_occurrence_id", {}),
        ("action_type", "LOCAL_ACTION"),
        ("action_type", "DIRECT_KG_WRITE"),
        ("revision", True),
    ],
)
def test_action_contract_refuses_wrong_types_and_operators(
    action_compilation, field, value
):
    record = action_record()
    record[field] = value
    assert action_compilation.view.validate_instance("SupplierOrderAmendment", record)


def test_action_cannot_smuggle_graph_operations(action_compilation):
    record = action_record()
    record["graph_operations"] = [{"record_id": "B", "quantity": 2}]
    assert action_compilation.view.validate_instance("SupplierOrderAmendment", record)


def test_schema_does_not_promote_fixture_quantities_into_ontology(action_compilation):
    record = action_record()
    record.update(
        supplier_order_id="another-order",
        product_code="another-product",
        expected_quantity=2,
        requested_quantity=3,
    )
    # Structural validity is not applicability under the selected 1-to-2 model.
    assert (
        action_compilation.view.validate_instance("SupplierOrderAmendment", record)
        == []
    )


def test_exact_assent_date_semantics_survive_the_subtype(action_compilation):
    assert action_compilation.view.get_slot_constraint(
        "ValidTime", "calendar_date"
    ).range_id == ("https://w3id.org/linkml/types/date")
    assert action_compilation.view.get_enum_values("AuthorizationVerdict") == {
        "AUTHORIZE",
        "BLOCK",
        "CLARIFY",
    }

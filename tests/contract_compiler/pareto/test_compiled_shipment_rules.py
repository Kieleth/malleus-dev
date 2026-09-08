"""The existing rule checker must consume the compiled Shop contract directly."""

from dataclasses import replace
from hashlib import sha256
from importlib.resources import files
from pathlib import Path

import pytest

from malleus import KnowledgeGraph
import malleus.compiler as api
from malleus.logic import LogicContract, LogicError, logic_contract_digest
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph


ROOT = Path(__file__).resolve().parents[3]
SHOP = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/small_shop/partial_shipments"
)
RULE = """malleus_rule('ONE_SHIPMENT_PER_UNIT').
malleus_violation('ONE_SHIPMENT_PER_UNIT', 'UNIT_ASSIGNED_TWICE', [A, B, Unit]) :-
    m_relation(A, 'ShipmentContainsUnit', First, Unit),
    m_relation(B, 'ShipmentContainsUnit', Second, Unit),
    First @< Second.
"""


@pytest.fixture(scope="module")
def view():
    return api.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": (SHOP / "small-shop-with-shipments.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    ).view


def contract(view):
    fields = {
        "schema_version": "1",
        "contract_id": "shop-one-shipment-per-unit",
        "contract_version": "1",
        "ontology_hash": "sha256:" + view.content_hash(),
        "fact_contract_version": "2",
        "ruleset_id": "shop-shipment-rules",
        "ruleset_version": "1",
        "rule_ids": ("ONE_SHIPMENT_PER_UNIT",),
        "timeout_seconds": 5,
        "ruleset_hash": "sha256:" + sha256(RULE.encode()).hexdigest(),
    }
    return LogicContract(
        **fields,
        rules_path=Path(__file__),
        rules_source=RULE,
        contract_hash=logic_contract_digest(**fields),
    )


def candidate(view, second_unit):
    graph = KnowledgeGraph(view)
    writes = [
        ProposedOperation.entity("InventoryUnit", unit, {"product_code": "X"})
        for unit in ("unit:1", "unit:2")
    ]
    for shipment, unit in (("shipment:1", "unit:1"), ("shipment:2", second_unit)):
        writes.extend(
            (
                ProposedOperation.entity(
                    "Shipment", shipment, {"tracking_id": shipment}
                ),
                ProposedOperation.relation(
                    "ShipmentContainsUnit",
                    "contains:" + shipment,
                    shipment,
                    unit,
                    {"relation_type": "SHIPMENT_CONTAINS_UNIT"},
                ),
            )
        )
    return graph, stage_subgraph(graph, writes)


@pytest.mark.parametrize("second_unit", ["unit:1", "unit:2"])
def test_compiled_shop_runs_real_rule_without_reparsing(view, second_unit):
    graph, staged = candidate(view, second_unit)
    before = graph.export_records()
    assert staged.valid
    result = PrologVerifier(contract(view)).verify_candidate_subgraph(staged)
    assert graph.export_records() == before
    assert result.outcome == ("VIOLATED" if second_unit == "unit:1" else "SATISFIED")
    assert result.checked_rule_ids == ("ONE_SHIPMENT_PER_UNIT",)
    if second_unit == "unit:1":
        assert len(result.violations) == 1
        assert result.violations[0].violation_code == "UNIT_ASSIGNED_TWICE"
        assert result.violations[0].witness_record_ids == (
            "contains:shipment:1",
            "contains:shipment:2",
            "unit:1",
        )
    else:
        assert not result.violations


def test_different_compiled_identity_is_a_typed_logic_refusal(view):
    selected = contract(view)
    digest_fields = {
        name: getattr(selected, name)
        for name in (
            "schema_version",
            "contract_id",
            "contract_version",
            "ontology_hash",
            "fact_contract_version",
            "ruleset_id",
            "ruleset_version",
            "rule_ids",
            "timeout_seconds",
            "ruleset_hash",
        )
    }
    digest_fields["ontology_hash"] = "sha256:" + "0" * 64
    wrong = replace(
        selected,
        ontology_hash=digest_fields["ontology_hash"],
        contract_hash=logic_contract_digest(**digest_fields),
    )
    graph, staged = candidate(view, "unit:2")
    before = graph.export_records()
    with pytest.raises(LogicError, match="different ontologies"):
        PrologVerifier(wrong).verify_candidate_subgraph(staged)
    assert graph.export_records() == before

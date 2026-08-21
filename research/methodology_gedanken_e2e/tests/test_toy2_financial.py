"""Toy 2 verdicts, executed, including the self-report trap.

The trap test is the load-bearing one for D0. It shows a graph whose records,
types and edges are byte-for-byte the same passing or failing depending on one
string the writer chose.
"""

from __future__ import annotations

from drivers.common import check, codes, contract_for, findings, registry_for
from drivers.financial import (
    TOY,
    graph_a_writes,
    graph_b1_writes,
    graph_b2_writes,
    self_report_trap,
)


def test_contract_pins_the_ontology_actually_loaded():
    contract = contract_for(TOY)
    assert contract.ontology_hash == f"sha256:{registry_for(TOY).content_hash()}"
    assert contract.rule_ids == ("PROVENANCE_PATTERN",)


def test_graph_a_is_silent():
    result = check(TOY, graph_a_writes())
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


def test_graph_b1_fires_missing_risk_stage():
    result = check(TOY, graph_b1_writes())
    assert ("PROVENANCE_PATTERN", "MISSING_RISK_STAGE", ("rec2",)) in findings(result)


def test_graph_b1_also_fires_on_its_own_dates():
    """Not in the sketch's prose, and it follows from the sketch's own numbers.

    GEDANKEN.md:177 gives rec2 `asserted_at` 2026-02-09 and derives it from o1,
    asserted 2026-02-10. The evidence postdates the conclusion it supports, so
    B1 is a double violation, not the single shape failure the prose describes.
    """
    result = check(TOY, graph_b1_writes())
    assert ("PROVENANCE_PATTERN", "SUPPORT_POSTDATES_CONCLUSION", ("o1", "rec2")) in findings(
        result
    )
    assert codes(result) == ("MISSING_RISK_STAGE", "SUPPORT_POSTDATES_CONCLUSION")


def test_graph_b2_has_the_right_shape_and_the_wrong_order():
    result = check(TOY, graph_b2_writes())
    assert codes(result) == ("SUPPORT_POSTDATES_CONCLUSION",)
    assert ("PROVENANCE_PATTERN", "SUPPORT_POSTDATES_CONCLUSION", ("k3", "rec3")) in findings(
        result
    )


def test_the_self_report_trap():
    """One edited string turns VIOLATED into SATISFIED on an unchanged graph.

    `asserted_at` is a domain slot the writer supplies. The rule that catches
    the post-hoc rationalization reads it, and B2 is precisely the case where
    the writer has an incentive to set it to something else.
    """
    honest, lying, same_shape = self_report_trap()
    assert same_shape
    assert honest == (("PROVENANCE_PATTERN", "SUPPORT_POSTDATES_CONCLUSION", ("k3", "rec3")),)
    assert lying == ()


def test_the_lie_changes_one_fact_and_nothing_structural():
    """The two graphs differ in exactly one compiled fact, and it is the string."""
    from drivers.common import facts, materialize

    honest = facts(TOY, materialize(TOY, graph_b2_writes("2026-02-14")))
    lying = facts(TOY, materialize(TOY, graph_b2_writes("2026-02-12")))
    assert honest.record_ids == lying.record_ids
    only_honest = set(honest.facts) - set(lying.facts)
    only_lying = set(lying.facts) - set(honest.facts)
    assert only_honest == {"m_property('k3', 'asserted_at', 'string', '2026-02-14')"}
    assert only_lying == {"m_property('k3', 'asserted_at', 'string', '2026-02-12')"}
    structural = {fact for fact in honest.facts if fact.startswith(("m_record(", "m_relation("))}
    assert structural == {
        fact for fact in lying.facts if fact.startswith(("m_record(", "m_relation("))
    }


def test_signals_became_entities():
    """The forced repair. Comparison and RiskAssessment are Signals in the sketch.

    Both are DerivedFrom endpoints, and a concrete relation's endpoint ranges
    must be Entity subtypes, so neither can be a Signal. No fact in this toy
    carries the `signal` kind.
    """
    from drivers.common import facts, materialize

    compiled = facts(TOY, materialize(TOY, graph_a_writes()))
    assert "m_record('k1', 'RiskAssessment', 'entity')" in compiled.facts
    kinds = {fact.rsplit(", ", 1)[1] for fact in compiled.facts if fact.startswith("m_record(")}
    assert kinds == {"'entity')", "'relation')"}

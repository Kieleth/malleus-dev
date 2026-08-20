"""Toy 3 verdicts, executed.

Two of these contradict the expectation the toy was written with: graph C fires
one violation code, not two, and the sketch's rules never read the ordinal they
made required.
"""

from __future__ import annotations

from drivers.common import check, codes, contract_for, findings, registry_for
from drivers.diagnosis import (
    TOY,
    batch_writes,
    graph_c2_writes,
    graph_c_writes,
    graph_d_writes,
)


def test_contract_pins_the_ontology_actually_loaded():
    contract = contract_for(TOY)
    assert contract.ontology_hash == f"sha256:{registry_for(TOY).content_hash()}"
    assert contract.rule_ids == ("DIFFERENTIAL_REQUIRED",)


def test_graph_c_fires_single_hypothesis():
    result = check(TOY, graph_c_writes())
    assert result.outcome == "VIOLATED"
    assert findings(result) == (("DIFFERENTIAL_REQUIRED", "SINGLE_HYPOTHESIS", ("dx1",)),)


def test_graph_c_cannot_fire_competitor_not_refuted():
    """Only one code fires on C, and the second one structurally cannot.

    COMPETITOR_NOT_REFUTED existentially requires a rival hypothesis. Graph C
    has none, so the rule body has no solution and the code is silent. The two
    codes are complementary, not cumulative: no single graph fires both.
    """
    assert codes(check(TOY, graph_c_writes())) == ("SINGLE_HYPOTHESIS",)


def test_graph_c2_fires_competitor_not_refuted():
    """Graph C2 is not in the sketch and without it this code is never exercised."""
    result = check(TOY, graph_c2_writes())
    assert codes(result) == ("COMPETITOR_NOT_REFUTED",)
    assert findings(result) == (
        ("DIFFERENTIAL_REQUIRED", "COMPETITOR_NOT_REFUTED", ("dx1", "h2")),
        ("DIFFERENTIAL_REQUIRED", "COMPETITOR_NOT_REFUTED", ("dx1", "h3")),
    )


def test_graph_d_is_silent():
    result = check(TOY, graph_d_writes())
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


def test_the_reverse_engineered_differential_passes_identically():
    """Graph D and the same records claimed at one turn return the same verdict.

    Every `entered_at` in `batch_writes` reads 6, the turn of the conclusion:
    the clinician decided, then assembled the differential. The rules do not
    read the slot, so the two graphs are indistinguishable to them.
    """
    sound = check(TOY, graph_d_writes())
    batch = check(TOY, batch_writes())
    assert findings(sound) == findings(batch) == ()
    assert sound.translated_record_ids == batch.translated_record_ids
    assert sound.fact_count == batch.fact_count


def test_entered_at_is_compiled_but_unread():
    """The ordinal reaches the facts. No rule in the pinned contract mentions it."""
    from drivers.common import contract_for as load, facts, materialize

    compiled = facts(TOY, materialize(TOY, graph_d_writes()))
    assert "m_property('dx1', 'entered_at', 'integer', 6)" in compiled.facts
    clauses = "\n".join(
        line for line in load(TOY).rules_source.splitlines() if not line.startswith("%%")
    )
    assert "entered_at" not in clauses


def test_events_became_entities():
    """TestOrder and TestResult are Events in the sketch and cannot be here."""
    from drivers.common import facts, materialize

    compiled = facts(TOY, materialize(TOY, graph_d_writes()))
    assert "m_record('r2', 'TestResult', 'entity')" in compiled.facts
    kinds = {fact.rsplit(", ", 1)[1] for fact in compiled.facts if fact.startswith("m_record(")}
    assert kinds == {"'entity')", "'relation')"}

"""Toy 1 verdicts, executed. Every assertion is a verdict this run produced.

Where an assertion contradicts GEDANKEN.md's prose it says so, because the
prose was never executed and this is what executing it returned.
"""

from __future__ import annotations

from drivers.common import check, contract_for, findings, registry_for
from drivers.kitchen import TOY, sketch_writes, sound_writes


def test_contract_pins_the_ontology_actually_loaded():
    """The pinned hash is recomputed here, so a schema edit fails loudly."""
    contract = contract_for(TOY)
    assert contract.ontology_hash == f"sha256:{registry_for(TOY).content_hash()}"
    assert contract.rule_ids == ("MISE_EN_PLACE",)


def test_sketch_graph_fires_on_the_tomato():
    result = check(TOY, sketch_writes())
    assert result.outcome == "VIOLATED"
    assert ("MISE_EN_PLACE", "UNPREPARED_INGREDIENT", ("s6", "tomato")) in findings(result)


def test_sketch_graph_also_fires_on_the_oil():
    """Not in the sketch's prose, and the rule the sketch wrote catches it.

    GEDANKEN.md:84 names the tomato as the single L3 failure. Step s3 combines
    `oil` at index 3 and no PrepStep anywhere touches the oil, so the rule as
    written binds twice. The prose read the graph less carefully than the rule
    does.
    """
    result = check(TOY, sketch_writes())
    assert ("MISE_EN_PLACE", "UNPREPARED_INGREDIENT", ("oil", "s3")) in findings(result)
    assert len(result.violations) == 2


def test_sound_graph_is_silent():
    """Without this the rule is only ever seen firing, which proves nothing."""
    result = check(TOY, sound_writes())
    assert result.outcome == "SATISFIED"
    assert result.violations == ()


def test_l1_and_l2_pass_on_the_failing_graph():
    """The point of the toy: the bad graph is a legal, staged, consistent graph.

    Every write passes registry validation, so the candidate is valid and
    materializes. Only the methodology rule objects.
    """
    from malleus.kg import KnowledgeGraph
    from malleus.staging import stage_subgraph

    graph = KnowledgeGraph(registry_for(TOY))
    candidate = stage_subgraph(graph, sketch_writes())
    assert candidate.valid
    assert candidate.rejection_reason is None
    candidate.materialize_into(graph)
    assert graph.node_count == 13
    assert graph.edge_count == 12


def test_sketch_node_and_edge_counts_disagree_with_the_prose():
    """GEDANKEN.md:57 says 14 nodes and 11 edges; its own table says 13 and 12.

    Recorded rather than corrected: the table is the operative spec and the
    graph above is built from the table, row for row.
    """
    from malleus.kg import KnowledgeGraph
    from malleus.staging import stage_subgraph

    graph = KnowledgeGraph(registry_for(TOY))
    stage_subgraph(graph, sketch_writes()).materialize_into(graph)
    uses = len(graph.query_relations(relation_type="UsesRelation"))
    into = len(graph.query_relations(relation_type="IntoRelation"))
    yields = len(graph.query_relations(relation_type="YieldsRelation"))
    assert (uses, into, yields) == (6, 5, 1)
    assert (uses, into, yields) != (7, 3, 1)


def test_every_step_compiles_as_entity_kind():
    """The forced repair, made visible in the facts the rules actually see.

    GEDANKEN types the steps as Events. The ontology refuses that, so the
    `m_record/3` kind argument reads `entity` for every node in the toy and the
    entity/event/signal discriminator carries no information here.
    """
    from drivers.common import facts, materialize

    compiled = facts(TOY, materialize(TOY, sketch_writes()))
    assert "m_record('s6', 'CombineStep', 'entity')" in compiled.facts
    kinds = {fact.rsplit(", ", 1)[1] for fact in compiled.facts if fact.startswith("m_record(")}
    assert kinds == {"'entity')", "'relation')"}

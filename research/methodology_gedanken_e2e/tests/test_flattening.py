"""The flattening limitation, measured rather than argued.

GEDANKEN.md:117-121 claims a rule cannot tell whether a record is the write
being proposed now or one accepted last week, because
`verify_candidate_subgraph` calls `compile(*context, overlay)`. These tests
compile the same records under different context/candidate splits and compare
the fact sets byte for byte.
"""

from __future__ import annotations

from malleus.kg import KnowledgeGraph
from malleus.staging import stage_subgraph

from drivers.common import check, contract_for, facts, registry_for
from drivers.kitchen import TOY, sketch_writes

from malleus.prolog_verifier import PrologVerifier


def _materialized(writes):
    graph = KnowledgeGraph(registry_for(TOY))
    stage_subgraph(graph, writes).materialize_into(graph)
    return graph


def test_the_same_records_compile_identically_as_context_and_as_candidate():
    """One record set, two roles, one fact set.

    Left: the records sit in a materialized graph passed as context. Right: the
    identical records sit in a staged candidate that has never been accepted.
    The compiler flattens both into the same facts and the same hash.
    """
    writes = sketch_writes()
    as_context = facts(TOY, _materialized(writes))
    as_candidate = facts(TOY, stage_subgraph(KnowledgeGraph(registry_for(TOY)), writes).overlay())
    assert as_context.facts == as_candidate.facts
    assert as_context.facts_hash == as_candidate.facts_hash
    assert as_context.record_ids == as_candidate.record_ids


def test_moving_the_accepted_boundary_changes_no_fact():
    """The split between already-written and being-proposed can sit anywhere.

    Three placements of the same 25 records: all proposed, entities accepted
    and edges proposed, everything but the last edge accepted. The fact sets
    are equal, so no rule can discriminate them.
    """
    writes = sketch_writes()
    splits = (0, 13, len(writes) - 1)
    hashes = set()
    for split in splits:
        base = KnowledgeGraph(registry_for(TOY))
        if split:
            stage_subgraph(base, writes[:split]).materialize_into(base)
        candidate = stage_subgraph(base, writes[split:])
        assert candidate.valid, candidate.rejection_reason
        hashes.add(facts(TOY, candidate.overlay()).facts_hash)
    assert len(hashes) == 1


def test_the_check_record_keeps_the_boundary_the_facts_lost():
    """The protocol does record which write was proposed. The rules never see it.

    Two runs over the same final graph with different splits return different
    `candidate_digest` and `base_state_digest` values on the LogicCheckResult,
    an identical `facts_hash`, and identical violations. The distinction exists
    one layer above the fact vocabulary and stops there.
    """
    writes = sketch_writes()
    verifier = PrologVerifier(contract_for(TOY))

    whole = KnowledgeGraph(registry_for(TOY))
    first = verifier.verify_candidate_subgraph(stage_subgraph(whole, writes))

    partial = KnowledgeGraph(registry_for(TOY))
    stage_subgraph(partial, writes[:13]).materialize_into(partial)
    second = verifier.verify_candidate_subgraph(stage_subgraph(partial, writes[13:]))

    assert first.candidate_digest != second.candidate_digest
    assert first.base_state_digest != second.base_state_digest
    assert first.facts_hash == second.facts_hash
    assert first.violations == second.violations


def test_a_candidate_cannot_reference_a_context_graph():
    """The `*context` parameter carries disjoint graphs, not a prior state.

    Staging revalidates every endpoint against the candidate's own base, so a
    relation whose target lives in a context graph is refused before any rule
    runs. Splitting a graph across context and candidate is therefore only
    possible where no edge crosses the split.
    """
    writes = sketch_writes()
    pantry = _materialized(writes[:6])
    orphan = stage_subgraph(KnowledgeGraph(registry_for(TOY)), writes[6:])
    assert not orphan.valid
    assert "Target entity 'onion' does not exist" in orphan.rejection_reason
    assert pantry.node_count == 6


def test_a_disjoint_split_across_context_and_candidate_also_flattens():
    """Where a split is legal, the compiler still erases it.

    Six unrelated entities: three in a context graph, three in a candidate.
    Compiled together they equal the same six compiled as one graph.
    """
    pantry = sketch_writes()[:6]
    context = _materialized(pantry[:3])
    candidate = stage_subgraph(KnowledgeGraph(registry_for(TOY)), pantry[3:])
    assert candidate.valid, candidate.rejection_reason
    split = facts(TOY, context, candidate.overlay())
    whole = facts(TOY, _materialized(pantry))
    assert split.facts == whole.facts
    assert split.facts_hash == whole.facts_hash


def test_the_verdict_is_unchanged_by_where_the_records_were_written():
    """The end-to-end statement, at the level a caller acts on."""
    proposed = check(TOY, sketch_writes())
    writes = sketch_writes()
    accepted = KnowledgeGraph(registry_for(TOY))
    stage_subgraph(accepted, writes[:13]).materialize_into(accepted)
    partial = PrologVerifier(contract_for(TOY)).verify_candidate_subgraph(
        stage_subgraph(accepted, writes[13:])
    )
    assert proposed.outcome == partial.outcome == "VIOLATED"
    assert proposed.violations == partial.violations

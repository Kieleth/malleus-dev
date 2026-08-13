"""Guardrails for isolated, atomic proposed-subgraph staging."""

from pathlib import Path

import pytest

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry
from malleus.staging import (
    ProposedOperation,
    StagingError,
    StaleCandidateError,
    stage_subgraph,
)


ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"
CYP450_SCHEMA = ONTOLOGY_DIR / "domains" / "cyp450.yaml"
ATTACK_SCHEMA = ONTOLOGY_DIR / "domains" / "attack.yaml"


@pytest.fixture
def graph():
    return KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))


def simple_subgraph():
    return [
        ProposedOperation.entity("Drug", "drug-1", {"name": "Drug One"}),
        ProposedOperation.entity(
            "Enzyme",
            "enzyme-1",
            {"name": "CYP3A4", "cyp_isoform": "CYP3A4"},
        ),
        ProposedOperation.relation(
            "SubstrateOfRelation",
            "relation-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        ),
    ]


class TestIsolatedStaging:
    def test_stages_complete_subgraph_without_base_mutation(self, graph):
        before = graph.snapshot()
        candidate = stage_subgraph(graph, simple_subgraph(), turn=4)

        assert candidate.valid
        assert graph.snapshot() == before
        assert graph.operations == []
        assert [operation.op_status for operation in candidate.operations] == [
            OpStatus.STAGED,
            OpStatus.STAGED,
            OpStatus.STAGED,
        ]
        overlay = candidate.overlay()
        assert overlay.node_count == 2
        assert overlay.edge_count == 1
        assert overlay.query_relations()[0]["key"] == "relation-1"

    def test_relation_can_depend_on_entities_in_same_candidate(self, graph):
        candidate = stage_subgraph(graph, simple_subgraph())
        assert candidate.valid
        assert candidate.overlay().query_relations(source_id="drug-1")

    def test_invalid_member_rejects_whole_candidate(self, graph):
        before = graph.snapshot()
        writes = [
            ProposedOperation.entity("Drug", "drug-1", {"name": "Drug One"}),
            ProposedOperation.entity("UnknownType", "unknown-1"),
        ]
        candidate = stage_subgraph(graph, writes)

        assert not candidate.valid
        assert candidate.candidate_state_digest is None
        assert "Unknown entity type" in candidate.rejection_reason
        assert graph.snapshot() == before
        assert graph.operations == []
        with pytest.raises(StagingError, match="no usable overlay"):
            candidate.overlay()
        with pytest.raises(StagingError, match="cannot be materialized"):
            candidate.materialize_into(graph)

    def test_overlay_reads_are_defensive(self, graph):
        candidate = stage_subgraph(graph, simple_subgraph())
        first = candidate.overlay()
        first.create_entity("Drug", "injected", {"name": "Injected"})

        assert not candidate.overlay().has_node("injected")
        assert not graph.has_node("injected")

    def test_proposed_properties_do_not_alias_input_or_reads(self):
        properties = {"name": "Drug One", "tags": ["original"]}
        write = ProposedOperation.entity("Drug", "drug-1", properties)
        properties["tags"].append("input mutation")
        read = write.properties
        read["tags"].append("read mutation")

        assert write.properties == {"name": "Drug One", "tags": ["original"]}

    def test_empty_and_untyped_candidates_fail_loudly(self, graph):
        with pytest.raises(StagingError, match="at least one"):
            stage_subgraph(graph, [])
        with pytest.raises(TypeError, match=r"writes\[0\]"):
            stage_subgraph(graph, [{}])

    def test_missing_identifiers_and_invalid_turn_fail_loudly(self, graph):
        with pytest.raises(StagingError, match="record_id"):
            ProposedOperation.entity("Drug", "")
        with pytest.raises(StagingError, match="source_id"):
            ProposedOperation.relation(
                "SubstrateOfRelation",
                "relation-1",
                "",
                "enzyme-1",
                {"relation_type": "SUBSTRATE_OF"},
            )
        with pytest.raises(TypeError, match="nonnegative integer"):
            stage_subgraph(
                graph,
                [ProposedOperation.entity("Drug", "drug-1")],
                turn=True,
            )

    def test_noncanonical_properties_fail_loudly(self):
        with pytest.raises(StagingError, match="properties are invalid"):
            ProposedOperation.entity("Drug", "drug-1", {"bad": float("nan")})

    def test_nested_nonstring_property_keys_fail_loudly(self):
        with pytest.raises(StagingError, match="object keys must be strings"):
            ProposedOperation.entity("Drug", "drug-1", {"nested": {1: "bad"}})

    def test_candidate_digest_binds_ordered_writes_and_base(self, graph):
        writes = [
            ProposedOperation.entity("Drug", "drug-a", {"name": "A"}),
            ProposedOperation.entity("Drug", "drug-b", {"name": "B"}),
        ]
        first = stage_subgraph(graph, writes)
        repeated = stage_subgraph(graph, writes)
        reversed_candidate = stage_subgraph(graph, list(reversed(writes)))

        assert first.candidate_digest == repeated.candidate_digest
        assert first.candidate_digest != reversed_candidate.candidate_digest

        graph.create_entity("Drug", "base-drug", {"name": "Base"})
        new_base = stage_subgraph(graph, writes)
        assert first.candidate_digest != new_base.candidate_digest


class TestAtomicMaterialization:
    def test_materializes_entire_candidate(self, graph):
        candidate = stage_subgraph(graph, simple_subgraph(), turn=7)
        committed = candidate.materialize_into(graph)

        assert graph.node_count == 2
        assert graph.edge_count == 1
        assert graph.state_digest() == candidate.candidate_state_digest
        assert len(committed) == 3
        assert all(operation.op_status == OpStatus.COMMITTED for operation in committed)
        assert all(operation.turn == 7 for operation in committed)

    def test_stale_candidate_cannot_overwrite_new_state(self, graph):
        candidate = stage_subgraph(
            graph,
            [ProposedOperation.entity("Drug", "candidate-drug", {"name": "Candidate"})],
        )
        graph.create_entity("Drug", "concurrent-drug", {"name": "Concurrent"})
        before = graph.snapshot()

        with pytest.raises(StaleCandidateError, match="changed"):
            candidate.materialize_into(graph)

        assert graph.snapshot() == before
        assert graph.has_node("concurrent-drug")
        assert not graph.has_node("candidate-drug")

    def test_different_ontology_cannot_receive_candidate(self, graph):
        candidate = stage_subgraph(
            graph,
            [ProposedOperation.entity("Drug", "drug-1", {"name": "Drug One"})],
        )
        target = KnowledgeGraph(OntologyRegistry(ATTACK_SCHEMA))

        with pytest.raises(StagingError, match="different ontologies"):
            candidate.materialize_into(target)
        assert target.node_count == 0

    def test_revalidation_exception_leaves_base_untouched(self, graph, monkeypatch):
        candidate = stage_subgraph(
            graph,
            [ProposedOperation.entity("Drug", "drug-1", {"name": "Drug One"})],
        )
        before = graph.snapshot()

        def fail_before_materialization(*args, **kwargs):
            raise RuntimeError("injected materialization failure")

        monkeypatch.setattr(KnowledgeGraph, "create_entity", fail_before_materialization)
        with pytest.raises(RuntimeError, match="injected"):
            candidate.materialize_into(graph)
        assert graph.snapshot() == before
        assert graph.operations == []

    def test_state_digest_excludes_rejected_audit_entries(self, graph):
        before = graph.state_digest()
        graph.create_entity("UnknownType", "bad-1")
        assert graph.state_digest() == before
        assert len(graph.rejected_operations()) == 1

    def test_state_digest_is_independent_of_insertion_order(self):
        registry = OntologyRegistry(CYP450_SCHEMA)
        first = KnowledgeGraph(registry)
        second = KnowledgeGraph(registry)
        first.create_entity("Drug", "drug-a", {"name": "A"})
        first.create_entity("Drug", "drug-b", {"name": "B"})
        second.create_entity("Drug", "drug-b", {"name": "B"})
        second.create_entity("Drug", "drug-a", {"name": "A"})
        assert first.state_digest() == second.state_digest()

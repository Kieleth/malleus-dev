"""Tests for the Knowledge Graph: write-time validation, operation logging, queries.

These tests verify the core architectural property: the ontology is the
constructor parameter, and invalid writes are rejected at write time.
"""

from pathlib import Path

import pytest

from malleus.ontology import OntologyRegistry
from malleus.kg import KnowledgeGraph, OpStatus, OpType

ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"
CYP450_SCHEMA = ONTOLOGY_DIR / "domains" / "cyp450.yaml"
ATTACK_SCHEMA = ONTOLOGY_DIR / "domains" / "attack.yaml"


@pytest.fixture
def cyp450_registry():
    return OntologyRegistry(CYP450_SCHEMA)


@pytest.fixture
def attack_registry():
    return OntologyRegistry(ATTACK_SCHEMA)


@pytest.fixture
def cyp450_kg(cyp450_registry):
    return KnowledgeGraph(cyp450_registry)


@pytest.fixture
def attack_kg(attack_registry):
    return KnowledgeGraph(attack_registry)


# --- Constructor parameter property ---


class TestOntologyAsConstructor:
    def test_kg_requires_registry(self):
        """KG cannot be instantiated without an ontology registry."""
        with pytest.raises(TypeError):
            KnowledgeGraph()

    def test_kg_has_registry(self, cyp450_kg):
        """KG exposes its registry."""
        assert cyp450_kg.registry is not None
        assert cyp450_kg.registry.has_type("Drug")

    def test_empty_kg(self, cyp450_kg):
        """Fresh KG has no nodes or edges."""
        assert cyp450_kg.node_count == 0
        assert cyp450_kg.edge_count == 0


# --- Entity write-time validation ---


class TestEntityValidation:
    def test_valid_entity_committed(self, cyp450_kg):
        """Valid typed entity is committed to the graph."""
        op = cyp450_kg.create_entity("Drug", "drug-simvastatin", {"name": "Simvastatin"})
        assert op.op_status == OpStatus.COMMITTED
        assert cyp450_kg.node_count == 1
        assert cyp450_kg.has_node("drug-simvastatin")

    def test_unknown_type_rejected(self, cyp450_kg):
        """Entity with unknown type is rejected."""
        op = cyp450_kg.create_entity("Spaceship", "ship-1")
        assert op.op_status == OpStatus.REJECTED
        assert "Unknown entity type" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    def test_non_entity_type_rejected(self, cyp450_kg):
        """Using a Relation type for an entity is rejected."""
        op = cyp450_kg.create_entity("DrugRelation", "rel-1")
        assert op.op_status == OpStatus.REJECTED
        assert "not an Entity subtype" in op.rejection_reason

    def test_duplicate_id_rejected(self, cyp450_kg):
        """Duplicate entity ID is rejected."""
        cyp450_kg.create_entity("Drug", "drug-1")
        op = cyp450_kg.create_entity("Drug", "drug-1")
        assert op.op_status == OpStatus.REJECTED
        assert "already exists" in op.rejection_reason

    def test_enzyme_requires_isoform(self, cyp450_kg):
        """Enzyme requires cyp_isoform slot."""
        op = cyp450_kg.create_entity("Enzyme", "enz-1")
        assert op.op_status == OpStatus.REJECTED
        assert "cyp_isoform" in op.rejection_reason

    def test_enzyme_valid_isoform(self, cyp450_kg):
        """Enzyme with valid CYP isoform is committed."""
        op = cyp450_kg.create_entity("Enzyme", "enz-cyp3a4", {"cyp_isoform": "CYP3A4"})
        assert op.op_status == OpStatus.COMMITTED

    def test_enzyme_invalid_isoform_rejected(self, cyp450_kg):
        """Enzyme with invalid CYP isoform is rejected."""
        op = cyp450_kg.create_entity("Enzyme", "enz-bad", {"cyp_isoform": "CYP99Z9"})
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason


# --- Relation write-time validation ---


class TestRelationValidation:
    @pytest.fixture(autouse=True)
    def setup_entities(self, cyp450_kg):
        """Create base entities for relation tests."""
        cyp450_kg.create_entity("Drug", "drug-simvastatin", {"name": "Simvastatin"})
        cyp450_kg.create_entity("Enzyme", "enz-cyp3a4", {"cyp_isoform": "CYP3A4", "name": "CYP3A4"})
        cyp450_kg.create_entity("Drug", "drug-clarithromycin", {"name": "Clarithromycin"})

    def test_valid_relation_committed(self, cyp450_kg):
        """Valid typed relation is committed."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.COMMITTED
        assert cyp450_kg.edge_count == 1

    def test_invalid_relation_type_rejected(self, cyp450_kg):
        """Relation with invalid relation_type enum value is rejected."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "DESTROYS"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason

    def test_missing_source_rejected(self, cyp450_kg):
        """Relation with nonexistent source is rejected."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-nonexistent", "enz-cyp3a4",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "does not exist" in op.rejection_reason

    def test_missing_target_rejected(self, cyp450_kg):
        """Relation with nonexistent target is rejected."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-simvastatin", "enz-nonexistent",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "does not exist" in op.rejection_reason

    def test_strength_out_of_range_rejected(self, cyp450_kg):
        """Relation with strength outside 0.0-1.0 is rejected."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "INHIBITS", "strength": 5.0},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Strength" in op.rejection_reason

    def test_inhibition_strength_validated(self, cyp450_kg):
        """InhibitionStrength enum is validated on DrugRelation."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-clarithromycin", "enz-cyp3a4",
            {"relation_type": "INHIBITS", "inhibition_strength": "MEGA_STRONG"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason

    def test_valid_inhibition_strength(self, cyp450_kg):
        """Valid InhibitionStrength passes."""
        op = cyp450_kg.create_relation(
            "DrugRelation", "rel-1",
            "drug-clarithromycin", "enz-cyp3a4",
            {"relation_type": "INHIBITS", "inhibition_strength": "STRONG", "strength": 0.9},
        )
        assert op.op_status == OpStatus.COMMITTED


# --- Signal validation ---


class TestSignalValidation:
    @pytest.fixture(autouse=True)
    def setup_entities(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1", {"name": "Drug A"})

    def test_signal_requires_bearer(self, cyp450_kg):
        """Signal without bearer_id is rejected (dependent continuant)."""
        op = cyp450_kg.create_signal("DrugSignal", "sig-1", {"signal_type": "INTERACTION_RISK"})
        assert op.op_status == OpStatus.REJECTED
        assert "bearer_id" in op.rejection_reason

    def test_signal_invalid_bearer_rejected(self, cyp450_kg):
        """Signal with nonexistent bearer is rejected."""
        op = cyp450_kg.create_signal("DrugSignal", "sig-1", {
            "signal_type": "INTERACTION_RISK",
            "bearer_id": "nonexistent",
        })
        assert op.op_status == OpStatus.REJECTED
        assert "does not exist" in op.rejection_reason

    def test_valid_signal_committed(self, cyp450_kg):
        """Valid signal with existing bearer is committed."""
        op = cyp450_kg.create_signal("DrugSignal", "sig-1", {
            "signal_type": "INTERACTION_RISK",
            "bearer_id": "drug-1",
            "value": 0.85,
        })
        assert op.op_status == OpStatus.COMMITTED

    def test_invalid_signal_type_rejected(self, cyp450_kg):
        """Signal with invalid signal_type enum value is rejected."""
        op = cyp450_kg.create_signal("DrugSignal", "sig-1", {
            "signal_type": "MAGIC_SCORE",
            "bearer_id": "drug-1",
        })
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason


# --- Event validation ---


class TestEventValidation:
    def test_valid_event_committed(self, cyp450_kg):
        """Valid typed event is committed."""
        op = cyp450_kg.create_event("DrugEvent", "evt-1", {"event_type": "INTERACTION_DETECTED"})
        assert op.op_status == OpStatus.COMMITTED

    def test_invalid_event_type_rejected(self, cyp450_kg):
        """Event with invalid event_type is rejected."""
        op = cyp450_kg.create_event("DrugEvent", "evt-1", {"event_type": "EXPLOSION"})
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason


# --- Operation log ---


class TestOperationLog:
    def test_operations_recorded(self, cyp450_kg):
        """All operations (committed and rejected) are logged."""
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Spaceship", "ship-1")
        assert len(cyp450_kg.operations) == 2

    def test_committed_operations_filtered(self, cyp450_kg):
        """Can filter to committed operations only."""
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Spaceship", "ship-1")
        assert len(cyp450_kg.committed_operations()) == 1

    def test_rejected_operations_filtered(self, cyp450_kg):
        """Can filter to rejected operations only."""
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Spaceship", "ship-1")
        assert len(cyp450_kg.rejected_operations()) == 1

    def test_operations_by_turn(self, cyp450_kg):
        """Operations are tagged with turn number."""
        cyp450_kg.set_turn(1)
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.set_turn(2)
        cyp450_kg.create_entity("Drug", "drug-2")
        assert len(cyp450_kg.committed_operations(turn=1)) == 1
        assert len(cyp450_kg.committed_operations(turn=2)) == 1

    def test_rejection_rate(self, cyp450_kg):
        """Rejection rate computed correctly."""
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Spaceship", "ship-1")
        assert cyp450_kg.rejection_rate() == 0.5

    def test_operation_contains_data(self, cyp450_kg):
        """Operation records the full data for audit trail."""
        op = cyp450_kg.create_entity("Drug", "drug-1", {"name": "Aspirin"})
        assert op.data["id"] == "drug-1"
        assert op.data["name"] == "Aspirin"
        assert op.entity_type == "Drug"
        assert op.op_type == OpType.CREATE_ENTITY


# --- Query operations ---


class TestQueries:
    @pytest.fixture(autouse=True)
    def setup_graph(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-sim", {"name": "Simvastatin"})
        cyp450_kg.create_entity("Drug", "drug-cla", {"name": "Clarithromycin"})
        cyp450_kg.create_entity("Enzyme", "enz-3a4", {"cyp_isoform": "CYP3A4", "name": "CYP3A4"})
        cyp450_kg.create_relation("DrugRelation", "rel-1", "drug-sim", "enz-3a4", {"relation_type": "SUBSTRATE_OF"})
        cyp450_kg.create_relation("DrugRelation", "rel-2", "drug-cla", "enz-3a4", {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"})

    def test_query_by_type(self, cyp450_kg):
        """Query entities by type."""
        drugs = cyp450_kg.query("Drug")
        assert len(drugs) == 2

    def test_query_by_name(self, cyp450_kg):
        """Query entities by property."""
        results = cyp450_kg.query(name="Simvastatin")
        assert len(results) == 1
        assert results[0]["id"] == "drug-sim"

    def test_query_relations(self, cyp450_kg):
        """Query relations by type."""
        rels = cyp450_kg.query_relations(source_id="drug-sim")
        assert len(rels) == 1
        assert rels[0]["type"] == "DrugRelation"

    def test_get_node(self, cyp450_kg):
        """Get a specific node by ID."""
        node = cyp450_kg.get_node("drug-sim")
        assert node is not None
        assert node["name"] == "Simvastatin"

    def test_get_missing_node(self, cyp450_kg):
        """Get returns None for missing node."""
        assert cyp450_kg.get_node("nonexistent") is None


# --- ATT&CK domain cross-check ---


class TestAttackDomain:
    def test_technique_committed(self, attack_kg):
        """ATT&CK Technique entity validates against attack ontology."""
        op = attack_kg.create_entity("Technique", "t1566", {
            "name": "Phishing",
            "attack_id": "T1566",
            "tactic": "INITIAL_ACCESS",
        })
        assert op.op_status == OpStatus.COMMITTED

    def test_invalid_tactic_rejected(self, attack_kg):
        """Invalid tactic enum value is rejected."""
        op = attack_kg.create_entity("Technique", "t1566", {
            "name": "Phishing",
            "tactic": "MAGIC_PHASE",
        })
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason

    def test_attack_chain_link(self, attack_kg):
        """CHAIN_LINK relation validates between techniques."""
        attack_kg.create_entity("Technique", "t1566", {"name": "Phishing", "tactic": "INITIAL_ACCESS"})
        attack_kg.create_entity("Technique", "t1059", {"name": "Command Scripting", "tactic": "EXECUTION"})
        op = attack_kg.create_relation(
            "AttackRelation", "chain-1",
            "t1566", "t1059",
            {"relation_type": "CHAIN_LINK", "capability": "user-code-execution"},
        )
        assert op.op_status == OpStatus.COMMITTED

    def test_drug_type_rejected_in_attack_kg(self, attack_kg):
        """Drug type from CYP450 domain is NOT valid in ATT&CK KG."""
        # Drug is registered (because attack.yaml imports malleus which has Entity,
        # but Drug is only in cyp450.yaml). This tests domain isolation.
        op = attack_kg.create_entity("Drug", "drug-1")
        assert op.op_status == OpStatus.REJECTED

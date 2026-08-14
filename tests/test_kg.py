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
        op = cyp450_kg.create_entity("InhibitsRelation", "rel-1")
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
            "SubstrateOfRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.COMMITTED
        assert cyp450_kg.edge_count == 1

    def test_invalid_relation_type_rejected(self, cyp450_kg):
        """Relation with invalid relation_type enum value is rejected."""
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "DESTROYS"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason

    def test_missing_source_rejected(self, cyp450_kg):
        """Relation with nonexistent source is rejected."""
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation", "rel-1",
            "drug-nonexistent", "enz-cyp3a4",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "does not exist" in op.rejection_reason

    def test_missing_target_rejected(self, cyp450_kg):
        """Relation with nonexistent target is rejected."""
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation", "rel-1",
            "drug-simvastatin", "enz-nonexistent",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "does not exist" in op.rejection_reason

    def test_strength_out_of_range_rejected(self, cyp450_kg):
        """Relation with strength outside 0.0-1.0 is rejected."""
        op = cyp450_kg.create_relation(
            "InhibitsRelation", "rel-1",
            "drug-simvastatin", "enz-cyp3a4",
            {"relation_type": "INHIBITS", "strength": 5.0},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "at most 1.0" in op.rejection_reason

    def test_inhibition_strength_validated(self, cyp450_kg):
        """InhibitionStrength enum is validated on InhibitsRelation."""
        op = cyp450_kg.create_relation(
            "InhibitsRelation", "rel-1",
            "drug-clarithromycin", "enz-cyp3a4",
            {"relation_type": "INHIBITS", "inhibition_strength": "MEGA_STRONG"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value" in op.rejection_reason

    def test_valid_inhibition_strength(self, cyp450_kg):
        """Valid InhibitionStrength passes."""
        op = cyp450_kg.create_relation(
            "InhibitsRelation", "rel-1",
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


# --- Strict closed-world validation ---


class TestStrictStructuralValidation:
    @pytest.mark.parametrize(
        "method, arguments",
        [
            ("create_entity", ([], "entity-1")),
            ("create_relation", ([], "rel-1", "source", "target")),
            ("create_signal", ([], "signal-1")),
            ("create_event", ([], "event-1")),
        ],
    )
    def test_nonstring_type_class_is_audited_rejection(
        self,
        cyp450_kg,
        method,
        arguments,
    ):
        op = getattr(cyp450_kg, method)(*arguments)
        assert op.op_status == OpStatus.REJECTED
        assert "must be a nonblank string" in op.rejection_reason
        assert cyp450_kg.node_count == 0
        assert cyp450_kg.edge_count == 0
        assert cyp450_kg.rejected_operations() == [op]

    def test_abstract_root_relation_cannot_bypass_signatures(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Drug", "drug-2")
        op = cyp450_kg.create_relation(
            "Relation",
            "rel-1",
            "drug-1",
            "drug-2",
            {"relation_type": "UNCONSTRAINED"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "abstract and cannot be instantiated" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_unknown_property_rejected_without_mutation(self, cyp450_kg):
        before = (cyp450_kg.node_count, cyp450_kg.edge_count)
        op = cyp450_kg.create_entity("Drug", "drug-1", {"invented": True})
        assert op.op_status == OpStatus.REJECTED
        assert "Unknown property 'invented'" in op.rejection_reason
        assert (cyp450_kg.node_count, cyp450_kg.edge_count) == before
        assert cyp450_kg.rejected_operations() == [op]

    @pytest.mark.parametrize(
        "entity_type, properties, message",
        [
            ("TacticEntity", {"tactic_order": "first"}, "must be an integer"),
            ("Technique", {"is_subtechnique": "false"}, "must be a boolean"),
            ("Technique", {"platform": "Linux"}, "must be a list"),
            ("Technique", {"created_at": "yesterday"}, "ISO 8601 datetime"),
        ],
    )
    def test_primitive_datetime_and_collection_ranges_rejected(
        self,
        attack_kg,
        entity_type,
        properties,
        message,
    ):
        op = attack_kg.create_entity(entity_type, "t-1", properties)
        assert op.op_status == OpStatus.REJECTED
        assert message in op.rejection_reason
        assert attack_kg.node_count == 0

    def test_missing_relation_discriminator_rejected(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation", "rel-1", "drug-1", "enzyme-1"
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Required slot 'relation_type'" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_missing_signal_discriminator_rejected(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        op = cyp450_kg.create_signal("DrugSignal", "signal-1", {"bearer_id": "drug-1"})
        assert op.op_status == OpStatus.REJECTED
        assert "Required slot 'signal_type'" in op.rejection_reason
        assert not cyp450_kg.has_node("signal-1")

    def test_missing_event_discriminator_rejected(self, cyp450_kg):
        op = cyp450_kg.create_event("DrugEvent", "event-1")
        assert op.op_status == OpStatus.REJECTED
        assert "Required slot 'event_type'" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    @pytest.mark.parametrize("identifier", ["", "   ", 7])
    def test_invalid_identifier_rejected(self, cyp450_kg, identifier):
        op = cyp450_kg.create_entity("Drug", identifier)
        assert op.op_status == OpStatus.REJECTED
        assert "nonblank string" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    def test_identifier_is_unique_across_record_kinds(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "shared-id")
        op = cyp450_kg.create_event(
            "DrugEvent",
            "shared-id",
            {"event_type": "INTERACTION_DETECTED"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "already exists as ENTITY" in op.rejection_reason
        assert cyp450_kg.node_count == 1

    def test_relation_identifier_is_unique_across_endpoints(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Drug", "drug-2")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        cyp450_kg.create_relation(
            "SubstrateOfRelation",
            "rel-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        )
        op = cyp450_kg.create_relation(
            "InhibitsRelation",
            "rel-1",
            "drug-2",
            "enzyme-1",
            {"relation_type": "INHIBITS"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "already exists as RELATION" in op.rejection_reason
        assert cyp450_kg.edge_count == 1

    def test_relation_predicate_must_match_concrete_class(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "InhibitsRelation",
            "rel-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "must equal 'INHIBITS'" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_relation_endpoint_ranges_enforced(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Drug", "drug-2")
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation",
            "rel-1",
            "drug-1",
            "drug-2",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "expected 'Enzyme'" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_event_cannot_be_relation_endpoint(self, cyp450_kg):
        cyp450_kg.create_event(
            "DrugEvent",
            "event-1",
            {"event_type": "INTERACTION_DETECTED"},
        )
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation",
            "rel-1",
            "event-1",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Source 'event-1' is not an Entity" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_signal_can_use_relation_as_bearer(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        cyp450_kg.create_relation(
            "SubstrateOfRelation",
            "rel-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        )
        op = cyp450_kg.create_signal(
            "DrugSignal",
            "signal-1",
            {"signal_type": "INTERACTION_RISK", "bearer_id": "rel-1"},
        )
        assert op.op_status == OpStatus.COMMITTED

    def test_event_cannot_be_signal_bearer(self, cyp450_kg):
        cyp450_kg.create_event(
            "DrugEvent",
            "event-1",
            {"event_type": "INTERACTION_DETECTED"},
        )
        op = cyp450_kg.create_signal(
            "DrugSignal",
            "signal-1",
            {"signal_type": "INTERACTION_RISK", "bearer_id": "event-1"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "must be an Entity or Relation" in op.rejection_reason

    def test_reserved_positional_property_rejected(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"id": "other"})
        assert op.op_status == OpStatus.REJECTED
        assert "Reserved positional properties" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    def test_nonmapping_properties_rejected(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", ["not", "a", "mapping"])
        assert op.op_status == OpStatus.REJECTED
        assert op.rejection_reason == "Properties must be a mapping"
        assert cyp450_kg.node_count == 0

    def test_nonstring_property_key_is_audited_rejection(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"name": "A", 2: "bad"})
        assert op.op_status == OpStatus.REJECTED
        assert "Property names must be UTF-8 encodable strings" in op.rejection_reason
        assert cyp450_kg.node_count == 0
        assert cyp450_kg.rejected_operations() == [op]

    def test_empty_optional_enum_is_validated(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "InhibitsRelation",
            "rel-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "INHIBITS", "inhibition_strength": ""},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Invalid value '' for inhibition_strength" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_empty_optional_datetime_is_validated(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"created_at": ""})
        assert op.op_status == OpStatus.REJECTED
        assert "ISO 8601 datetime" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    def test_empty_endpoint_reference_is_validated(self, cyp450_kg):
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "SubstrateOfRelation",
            "rel-1",
            "",
            "enzyme-1",
            {"relation_type": "SUBSTRATE_OF"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "Reference 'source_id' must be a nonblank identifier" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_empty_list_on_singular_slot_is_validated(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"name": []})
        assert op.op_status == OpStatus.REJECTED
        assert "Property 'name' must be singular" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    def test_empty_string_on_multivalued_slot_is_validated(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"tags": ""})
        assert op.op_status == OpStatus.REJECTED
        assert "Property 'tags' must be a list" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    @pytest.mark.parametrize("strength", [float("nan"), float("inf"), float("-inf")])
    def test_nonfinite_number_cannot_bypass_bounds(self, cyp450_kg, strength):
        cyp450_kg.create_entity("Drug", "drug-1")
        cyp450_kg.create_entity("Enzyme", "enzyme-1", {"cyp_isoform": "CYP3A4"})
        op = cyp450_kg.create_relation(
            "InhibitsRelation",
            "rel-1",
            "drug-1",
            "enzyme-1",
            {"relation_type": "INHIBITS", "strength": strength},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "finite number" in op.rejection_reason
        assert cyp450_kg.edge_count == 0

    def test_date_without_time_is_not_a_datetime(self, cyp450_kg):
        op = cyp450_kg.create_event(
            "DrugEvent",
            "event-1",
            {"event_type": "INTERACTION_DETECTED", "occurred_at": "2024-01-01"},
        )
        assert op.op_status == OpStatus.REJECTED
        assert "ISO 8601 datetime" in op.rejection_reason
        assert cyp450_kg.node_count == 0

    @pytest.mark.parametrize(
        "timestamp",
        ["2024-01-01T12:30:00Z", "2024-01-01T12:30:00+01:00"],
    )
    def test_datetime_with_time_and_zone_is_valid(self, cyp450_kg, timestamp):
        op = cyp450_kg.create_event(
            "DrugEvent",
            f"event-{timestamp[-1]}",
            {"event_type": "INTERACTION_DETECTED", "occurred_at": timestamp},
        )
        assert op.op_status == OpStatus.COMMITTED

    def test_original_collection_cannot_mutate_validated_graph(self, cyp450_kg):
        tags = ["safe"]
        cyp450_kg.create_entity("Drug", "drug-1", {"tags": tags})
        tags.append(7)
        assert cyp450_kg.get_node("drug-1")["tags"] == ["safe"]

    def test_read_collection_cannot_mutate_validated_graph(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1", {"tags": ["safe"]})
        read = cyp450_kg.get_node("drug-1")
        read["tags"].append(False)
        assert cyp450_kg.get_node("drug-1")["tags"] == ["safe"]

    def test_returned_operation_cannot_mutate_graph_or_audit(self, cyp450_kg):
        op = cyp450_kg.create_entity("Drug", "drug-1", {"tags": ["safe"]})
        op.data["tags"].append(None)
        assert cyp450_kg.get_node("drug-1")["tags"] == ["safe"]
        assert cyp450_kg.operations[0].data["tags"] == ["safe"]

    def test_operations_property_is_defensive_copy(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-1", {"tags": ["safe"]})
        operations = cyp450_kg.operations
        operations[0].data["tags"].append(1)
        assert cyp450_kg.operations[0].data["tags"] == ["safe"]


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
        cyp450_kg.create_relation("SubstrateOfRelation", "rel-1", "drug-sim", "enz-3a4", {"relation_type": "SUBSTRATE_OF"})
        cyp450_kg.create_relation("InhibitsRelation", "rel-2", "drug-cla", "enz-3a4", {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"})

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
        assert rels[0]["type"] == "SubstrateOfRelation"

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
            "ChainLinkRelation", "chain-1",
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


# --- Mixin filtering in queries ---


class TestMixinQuery:
    def test_query_by_mixin(self, tmp_path):
        """kg.query(mixin=...) returns every node whose type carries the mixin."""
        import textwrap, shutil
        schema = tmp_path / "agent_domain.yaml"
        schema.write_text(textwrap.dedent("""
            id: https://example.org/schema/agent_test
            name: agent_test
            imports: [malleus, linkml:types]
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Person:
                is_a: Entity
                mixins: [Agent]
              Service:
                is_a: Entity
                mixins: [Agent]
              Drug:
                is_a: Entity
        """).strip())
        shutil.copy(ONTOLOGY_DIR / "malleus.yaml", tmp_path / "malleus.yaml")

        reg = OntologyRegistry(schema)
        kg = KnowledgeGraph(reg)

        kg.create_entity("Person", "alice", {"name": "Alice"})
        kg.create_entity("Service", "svc-1", {"name": "web-api"})
        kg.create_entity("Drug", "drug-x", {"name": "Aspirin"})

        agents = kg.query(mixin="Agent")
        agent_ids = {a["id"] for a in agents}
        assert agent_ids == {"alice", "svc-1"}
        assert "drug-x" not in agent_ids

    def test_query_mixin_and_type_combine(self, tmp_path):
        """mixin and entity_type filters both apply (AND)."""
        import textwrap, shutil
        schema = tmp_path / "agent_domain.yaml"
        schema.write_text(textwrap.dedent("""
            id: https://example.org/schema/agent_test
            name: agent_test
            imports: [malleus, linkml:types]
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Person:
                is_a: Entity
                mixins: [Agent]
              Service:
                is_a: Entity
                mixins: [Agent]
        """).strip())
        shutil.copy(ONTOLOGY_DIR / "malleus.yaml", tmp_path / "malleus.yaml")

        reg = OntologyRegistry(schema)
        kg = KnowledgeGraph(reg)
        kg.create_entity("Person", "alice", {"name": "Alice"})
        kg.create_entity("Service", "svc-1", {"name": "web-api"})

        persons_that_are_agents = kg.query(entity_type="Person", mixin="Agent")
        assert {p["id"] for p in persons_that_are_agents} == {"alice"}


class TestRelaxedBearerIsRejectedNotRaised:
    """A domain schema may relax bearer_id; the runtime must refuse with a
    reason, never a KeyError (self-inquisition S1)."""

    def test_signal_without_bearer_is_rejected_as_data(self, tmp_path):
        schema = tmp_path / "loose.yaml"
        schema.write_text(
            "id: https://example.org/schema/loose\n"
            "name: loose\n"
            "imports:\n"
            "  - malleus\n"
            "  - linkml:types\n"
            "classes:\n"
            "  LooseSignal:\n"
            "    is_a: Signal\n"
            "    slot_usage:\n"
            "      signal_type:\n"
            "        range: LooseSignalType\n"
            "      bearer_id:\n"
            "        required: false\n"
            "enums:\n"
            "  LooseSignalType:\n"
            "    permissible_values:\n"
            "      LOOSE:\n"
        )
        from malleus.ontology import bundled_ontology_path

        registry = OntologyRegistry(
            schema, import_map={"malleus": str(bundled_ontology_path("malleus.yaml"))}
        )
        kg = KnowledgeGraph(registry)
        op = kg.create_signal("LooseSignal", "s1", {"signal_type": "LOOSE"})
        assert op.op_status == OpStatus.REJECTED
        assert "bearer_id" in op.rejection_reason


class TestSurrogatesAreRefusedAtTheGate:
    """A value the validator accepts must survive the serialization the
    identity layer performs (second self-inquisition H2)."""

    @pytest.mark.parametrize("value", ["\ud800", "\udc00", "\ud800" "\udc00"])
    def test_surrogate_value_is_rejected_with_reason(self, cyp450_kg, value):
        op = cyp450_kg.create_entity("Drug", "drug-surrogate", {"name": value})
        assert op.op_status == OpStatus.REJECTED
        assert "UTF-8" in op.rejection_reason


# --- Relation lookup by id ---


class TestRelationLookup:
    @pytest.fixture(autouse=True)
    def setup_graph(self, cyp450_kg):
        cyp450_kg.create_entity("Drug", "drug-cla", {"name": "Clarithromycin"})
        cyp450_kg.create_entity("Enzyme", "enz-3a4", {"cyp_isoform": "CYP3A4"})
        cyp450_kg.create_relation("InhibitsRelation", "rel-inh", "drug-cla", "enz-3a4", {
            "relation_type": "INHIBITS",
            "inhibition_strength": "STRONG",
        })

    def test_get_relation_returns_committed_record(self, cyp450_kg):
        """Get a specific relation by ID, endpoints and properties included."""
        assert cyp450_kg.get_relation("rel-inh") == {
            "id": "rel-inh",
            "source_id": "drug-cla",
            "target_id": "enz-3a4",
            "type": "InhibitsRelation",
            "relation_type": "INHIBITS",
            "inhibition_strength": "STRONG",
        }

    def test_get_missing_relation(self, cyp450_kg):
        """Get returns None for missing relation."""
        assert cyp450_kg.get_relation("rel-nonexistent") is None

    def test_get_relation_ignores_node_ids(self, cyp450_kg):
        """An entity ID is not a relation ID."""
        assert cyp450_kg.get_relation("drug-cla") is None

    def test_rejected_relation_is_not_retrievable(self, cyp450_kg):
        """A refused write leaves nothing to retrieve."""
        op = cyp450_kg.create_relation("InhibitsRelation", "rel-bad", "drug-cla", "enz-3a4", {
            "relation_type": "SUBSTRATE_OF",
        })
        assert op.op_status == OpStatus.REJECTED
        assert cyp450_kg.get_relation("rel-bad") is None

    def test_returned_relation_cannot_mutate_graph(self, cyp450_kg):
        """get_relation hands back a defensive copy."""
        relation = cyp450_kg.get_relation("rel-inh")
        relation["inhibition_strength"] = "WEAK"
        assert cyp450_kg.get_relation("rel-inh")["inhibition_strength"] == "STRONG"

    def test_idempotency_needs_no_rejection_string_match(self, cyp450_kg):
        """Idempotent writes read the graph instead of parsing a refusal reason."""
        def ensure_relation(relation_id):
            existing = cyp450_kg.get_relation(relation_id)
            if existing is not None:
                return existing
            op = cyp450_kg.create_relation("SubstrateOfRelation", relation_id, "drug-cla", "enz-3a4", {
                "relation_type": "SUBSTRATE_OF",
            })
            assert op.op_status == OpStatus.COMMITTED
            return cyp450_kg.get_relation(relation_id)

        first = ensure_relation("rel-sub")
        second = ensure_relation("rel-sub")
        assert first == second
        assert cyp450_kg.edge_count == 2
        assert cyp450_kg.rejected_operations() == []


# --- Structural export and rehydration ---


@pytest.fixture
def populated_kg(cyp450_kg):
    cyp450_kg.create_entity("Drug", "drug-sim", {"name": "Simvastatin", "drug_class": "statin"})
    cyp450_kg.create_entity("Drug", "drug-cla", {"name": "Clarithromycin"})
    cyp450_kg.create_entity("Enzyme", "enz-3a4", {"cyp_isoform": "CYP3A4", "name": "CYP3A4"})
    cyp450_kg.create_relation("SubstrateOfRelation", "rel-sub", "drug-sim", "enz-3a4", {
        "relation_type": "SUBSTRATE_OF",
    })
    cyp450_kg.create_relation("InhibitsRelation", "rel-inh", "drug-cla", "enz-3a4", {
        "relation_type": "INHIBITS",
        "inhibition_strength": "STRONG",
    })
    cyp450_kg.create_signal("DrugSignal", "sig-risk", {
        "signal_type": "INTERACTION_RISK",
        "bearer_id": "rel-inh",
        "value": 0.85,
    })
    cyp450_kg.create_event("DrugEvent", "evt-detected", {"event_type": "INTERACTION_DETECTED"})
    return cyp450_kg


class TestExportRecords:
    def test_export_has_the_four_create_families(self, populated_kg):
        """Export buckets match the four create_* families."""
        export = populated_kg.export_records()
        assert set(export) == {"entities", "relations", "signals", "events"}
        assert [len(export[family]) for family in ("entities", "relations", "signals", "events")] == [3, 2, 1, 1]

    def test_records_carry_create_arguments(self, populated_kg):
        """Each record is exactly the argument set of its create_* call."""
        export = populated_kg.export_records()
        entities = {record["id"]: record for record in export["entities"]}
        assert entities["drug-sim"] == {
            "type": "Drug",
            "id": "drug-sim",
            "properties": {"name": "Simvastatin", "drug_class": "statin"},
        }
        assert export["relations"][0] == {
            "type": "InhibitsRelation",
            "id": "rel-inh",
            "source_id": "drug-cla",
            "target_id": "enz-3a4",
            "properties": {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"},
        }
        assert export["signals"][0] == {
            "type": "DrugSignal",
            "id": "sig-risk",
            "properties": {
                "signal_type": "INTERACTION_RISK",
                "bearer_id": "rel-inh",
                "value": 0.85,
            },
        }
        assert export["events"][0] == {
            "type": "DrugEvent",
            "id": "evt-detected",
            "properties": {"event_type": "INTERACTION_DETECTED"},
        }

    def test_export_is_json_serializable(self, populated_kg):
        """The export survives a JSON round trip unchanged."""
        import json
        export = populated_kg.export_records()
        assert json.loads(json.dumps(export)) == export

    def test_export_cannot_mutate_graph(self, populated_kg):
        """Mutating the export does not touch materialized state."""
        digest = populated_kg.state_digest()
        export = populated_kg.export_records()
        export["entities"][0]["properties"]["name"] = "Tampered"
        export["entities"].append({"type": "Drug", "id": "drug-ghost", "properties": {}})
        export["relations"].clear()
        assert populated_kg.state_digest() == digest
        assert populated_kg.node_count == 5
        assert populated_kg.edge_count == 2
        assert populated_kg.export_records()["entities"][0]["properties"]["name"] != "Tampered"

    def test_export_excludes_the_operation_audit_log(self, populated_kg):
        """Refusals are execution-local: they leave no trace in the export."""
        before = populated_kg.export_records()
        op = populated_kg.create_entity("Enzyme", "enz-bad", {"cyp_isoform": "CYP99Z9"})
        assert op.op_status == OpStatus.REJECTED
        assert populated_kg.rejected_operations()
        assert populated_kg.export_records() == before
        assert "operations" not in before


class TestFromRecords:
    def test_round_trip_preserves_state(self, populated_kg, cyp450_registry):
        """Export then rehydrate reproduces counts and state digest."""
        rehydrated = KnowledgeGraph.from_records(cyp450_registry, populated_kg.export_records())
        assert rehydrated.node_count == populated_kg.node_count
        assert rehydrated.edge_count == populated_kg.edge_count
        assert rehydrated.state_digest() == populated_kg.state_digest()
        assert rehydrated.export_records() == populated_kg.export_records()

    def test_round_trip_preserves_record_kinds(self, populated_kg, cyp450_registry):
        """Signals and events come back as signals and events, not plain nodes."""
        rehydrated = KnowledgeGraph.from_records(cyp450_registry, populated_kg.export_records())
        assert rehydrated.get_node("sig-risk")["is_signal"] is True
        assert rehydrated.get_node("evt-detected")["is_event"] is True
        assert rehydrated.get_relation("rel-inh") == populated_kg.get_relation("rel-inh")

    def test_rehydration_replays_through_the_validated_gate(self, populated_kg, cyp450_registry):
        """Every rehydrated record is a committed operation in the new local audit."""
        rehydrated = KnowledgeGraph.from_records(cyp450_registry, populated_kg.export_records())
        assert len(rehydrated.operations) == 7
        assert rehydrated.rejection_rate() == 0.0

    def test_empty_records_build_an_empty_graph(self, cyp450_registry):
        """An absent family means no records of that kind."""
        graph = KnowledgeGraph.from_records(cyp450_registry, {})
        assert graph.node_count == 0
        assert graph.edge_count == 0

    def test_invalid_record_aggregates_every_reason(self, cyp450_registry):
        """One bad record fails the whole rehydration, with all reasons as data."""
        records = {
            "entities": [
                {"type": "Drug", "id": "drug-ok", "properties": {"name": "Simvastatin"}},
                {"type": "Enzyme", "id": "enz-bad", "properties": {"cyp_isoform": "CYP99Z9"}},
            ],
            "relations": [
                {
                    "type": "SubstrateOfRelation",
                    "id": "rel-1",
                    "source_id": "drug-ok",
                    "target_id": "enz-bad",
                    "properties": {"relation_type": "SUBSTRATE_OF"},
                },
            ],
        }
        with pytest.raises(ValueError) as excinfo:
            KnowledgeGraph.from_records(cyp450_registry, records)
        message = str(excinfo.value)
        assert "entities[1] 'enz-bad'" in message
        assert "Invalid value" in message
        assert "relations[0] 'rel-1'" in message
        assert "Target entity 'enz-bad' does not exist" in message

    def test_failed_rehydration_leaves_the_source_untouched(self, populated_kg, cyp450_registry):
        """Rehydration builds in isolation, so a failure cannot half-write anything."""
        digest = populated_kg.state_digest()
        records = populated_kg.export_records()
        records["entities"].append({"type": "Drug", "id": "drug-sim", "properties": {}})
        with pytest.raises(ValueError, match="already exists"):
            KnowledgeGraph.from_records(cyp450_registry, records)
        assert populated_kg.state_digest() == digest
        assert populated_kg.node_count == 5

    def test_unknown_type_is_rejected_despite_plausible_shape(self, cyp450_registry):
        """A well-shaped record with a type the registry does not know is refused."""
        records = {"entities": [{"type": "Spaceship", "id": "ship-1", "properties": {"name": "Rocinante"}}]}
        with pytest.raises(ValueError, match="Unknown entity type"):
            KnowledgeGraph.from_records(cyp450_registry, records)

    def test_records_are_validated_against_the_target_registry(self, populated_kg, attack_registry):
        """A CYP450 export does not rehydrate into an ATT&CK registry."""
        with pytest.raises(ValueError, match="Unknown entity type"):
            KnowledgeGraph.from_records(attack_registry, populated_kg.export_records())

    def test_unknown_record_family_is_rejected(self, populated_kg, cyp450_registry):
        """A snapshot dict is not a record export, and is refused as such."""
        with pytest.raises(ValueError, match="Unknown record family: 'nodes'"):
            KnowledgeGraph.from_records(cyp450_registry, populated_kg.snapshot())

    def test_malformed_records_are_rejected_with_reasons(self, cyp450_registry):
        """Missing, extra and non-mapping records each name what is wrong."""
        records = {
            "entities": [
                {"type": "Drug", "id": "drug-1"},
                {"type": "Drug", "id": "drug-2", "properties": {}, "bearer_id": "drug-1"},
                "drug-3",
            ],
        }
        with pytest.raises(ValueError) as excinfo:
            KnowledgeGraph.from_records(cyp450_registry, records)
        message = str(excinfo.value)
        assert "entities[0] is missing required keys: ['properties']" in message
        assert "entities[1] carries unexpected keys: ['bearer_id']" in message
        assert "entities[2] is not a mapping" in message

    def test_nonmapping_records_raise_type_error(self, cyp450_registry):
        """The records container itself must be a mapping."""
        with pytest.raises(TypeError, match="Records must be a mapping"):
            KnowledgeGraph.from_records(cyp450_registry, [])

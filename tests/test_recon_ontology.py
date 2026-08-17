from pathlib import Path

from malleus.ontology import OntologyRegistry, bundled_ontology_path


ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "ontology" / "domains" / "recon.yaml"


def test_recon_ontology_is_shipped_and_constructs():
    assert bundled_ontology_path("domains", "recon.yaml").resolve() == SCHEMA.resolve()
    registry = OntologyRegistry(SCHEMA)
    assert registry.schema_version == "0.1.0"
    assert registry.is_subtype_of("Work", "ReviewSubject")
    assert registry.is_subtype_of("ReviewSubject", "Entity")


def test_recon_ontology_has_the_review_primitives():
    registry = OntologyRegistry(SCHEMA)
    expected = {
        "ReviewTarget",
        "Work",
        "Claim",
        "Result",
        "ComparisonAxis",
        "EvidenceAttachment",
        "SearchEvent",
        "ReviewBoundary",
        "CoversAxisRelation",
    }
    assert expected <= set(registry.type_names())


def test_coverage_relation_is_typed_and_evidence_bearing():
    registry = OntologyRegistry(SCHEMA)
    slots = registry.effective_slots("CoversAxisRelation")
    assert slots["source_id"].range == "ReviewSubject"
    assert slots["target_id"].range == "ComparisonAxis"
    assert slots["relation_type"].equals_string == "COVERS_AXIS"
    for required in (
        "review_state",
        "assertion_status",
        "confidence",
        "basis",
        "evidence_ids",
        "coverage_level",
    ):
        assert slots[required].required is True


def test_recon_coverage_language_preserves_unresolved_state():
    registry = OntologyRegistry(SCHEMA)
    assert registry.get_enum_values("CoverageLevel") == {
        "CENTRAL",
        "MATERIAL",
        "PARTIAL",
        "ADJACENT",
        "NOT_ESTABLISHED",
        "CONTRADICTED",
        "NOT_APPLICABLE",
    }


def test_reviewed_work_requires_priority_basis_and_evidence_slot_is_typed():
    registry = OntologyRegistry(SCHEMA)
    errors = registry.validate_instance(
        "Work",
        {
            "id": "work:one",
            "label": "One",
            "title": "One paper",
            "priority_date": "2026-08-16",
            "publication_status": "PREPRINT",
            "review_state": "REVIEWED",
        },
    )
    assert "Required slot 'priority_date_basis' missing for Work" in errors
    assert registry.effective_slots("Work")["evidence_ids"].range == "EvidenceAttachment"

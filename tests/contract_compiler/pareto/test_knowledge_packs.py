"""Public contract for optional grounded knowledge packs."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from importlib.resources import files
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from malleus.ontology import bundled_ontology_path


ROOT = Path(__file__).resolve().parents[3]
PACK_NAMES = ("metrology", "chronology", "research")
ASSERTION_MODALITIES = {
    "STATED",
    "MEASURED",
    "CALCULATED",
    "HYPOTHESISED",
    "CONTESTED",
    "NEGATED",
}
QUDT_QUANTITY_KIND_NAMESPACE = "http://qudt.org/vocab/quantitykind/"
QUDT_QUANTITY_KINDS = (
    "Length",
    "Time",
    "Temperature",
    "Pressure",
    "Mass",
    "Volume",
    "Area",
    "Velocity",
    "Density",
    "Frequency",
    "Energy",
    "Force",
    "MassFraction",
    "Count",
    "Angle",
)
VALUE_QUALIFICATIONS = (
    "EXACT",
    "APPROXIMATE",
    "OPEN_LOWER_BOUND",
    "OPEN_UPPER_BOUND",
    "ORDER_OF_MAGNITUDE",
)
HYPOTHESIS_DISPOSITIONS = ("PREFERRED", "NOT_SUPPORTED", "UNDECIDED")
CREDIT_TAXONOMY_URL = "https://credit.niso.org/"
CREDIT_VOCABULARY = "ANSI/NISO Z39.104-2022, CRediT, Contributor Roles Taxonomy"
CREDIT_ROLE_NAMES = (
    "Conceptualization",
    "Data curation",
    "Formal analysis",
    "Funding acquisition",
    "Investigation",
    "Methodology",
    "Project administration",
    "Resources",
    "Software",
    "Supervision",
    "Validation",
    "Visualization",
    "Writing – original draft",
    "Writing – review & editing",
)
CREDIT_ROLES = {
    "CONCEPTUALIZATION": (
        "Ideas; formulation or evolution of overarching research goals and aims."
    ),
    "DATA_CURATION": (
        "Management activities to annotate (produce metadata), scrub data and "
        "maintain research data (including software code, where it is necessary "
        "for interpreting the data itself) for initial use and later re-use."
    ),
    "FORMAL_ANALYSIS": (
        "Application of statistical, mathematical, computational, or other "
        "formal techniques to analyze or synthesize study data."
    ),
    "FUNDING_ACQUISITION": (
        "Acquisition of the financial support for the project leading to this "
        "publication."
    ),
    "INVESTIGATION": (
        "Conducting a research and investigation process, specifically "
        "performing the experiments, or data/evidence collection."
    ),
    "METHODOLOGY": "Development or design of methodology; creation of models.",
    "PROJECT_ADMINISTRATION": (
        "Management and coordination responsibility for the research activity "
        "planning and execution."
    ),
    "RESOURCES": (
        "Provision of study materials, reagents, materials, patients, "
        "laboratory samples, animals, instrumentation, computing resources, or "
        "other analysis tools."
    ),
    "SOFTWARE": (
        "Programming, software development; designing computer programs; "
        "implementation of the computer code and supporting algorithms; testing "
        "of existing code components."
    ),
    "SUPERVISION": (
        "Oversight and leadership responsibility for the research activity "
        "planning and execution, including mentorship external to the core team."
    ),
    "VALIDATION": (
        "Verification, whether as a part of the activity or separate, of the "
        "overall replication/reproducibility of results/experiments and other "
        "research outputs."
    ),
    "VISUALIZATION": (
        "Preparation, creation and/or presentation of the published work, "
        "specifically visualization/data presentation."
    ),
    "WRITING_ORIGINAL_DRAFT": (
        "Preparation, creation and/or presentation of the published work, "
        "specifically writing the initial draft (including substantive "
        "translation)."
    ),
    "WRITING_REVIEW_AND_EDITING": (
        "Preparation, creation and/or presentation of the published work by "
        "those from the original research group, specifically critical review, "
        "commentary or revision – including pre- or post-publication stages."
    ),
}
GROUNDING_EXAMPLE_MARKER = (
    "carries a `grounding` block:\n\n"
    "```yaml\n"
)


def _compiler():
    return import_module("malleus.compiler")


def _inquisition():
    return import_module("malleus.inquisition")


def _linkml_types() -> bytes:
    return (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )


def _pack_sources() -> dict[str, bytes]:
    return {
        "linkml:types": _linkml_types(),
        "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
        **{
            name: bundled_ontology_path("packs", f"{name}.yaml").read_bytes()
            for name in PACK_NAMES
        },
    }


def _annotation(value: dict[str, object]) -> dict[str, object]:
    return {"grounding": {"tag": "grounding", "value": value}}


def _cited_grounding() -> dict[str, object]:
    return {
        "area": "Physical measurement",
        "taxonomy": "DDC 530.8",
        "vocabularies": [
            {
                "vocabulary": "JCGM 200:2012 (VIM), 3rd edition",
                "vocabulary_url": "https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf",
                "borrowed_terms": ["quantity value"],
            }
        ],
        "invented_terms": [],
    }


def _source(
    *,
    annotations: dict[str, object] | None = None,
    class_annotations: dict[str, object] | None = None,
    parent: str = "Entity",
    prefixes: dict[str, str] | None = None,
) -> bytes:
    value: dict[str, object] = {
        "id": "https://example.org/project",
        "name": "project",
        "imports": ["linkml:types", "malleus"],
        "classes": {"ProjectThing": {"is_a": parent}},
    }
    if annotations is not None:
        value["annotations"] = annotations
    if class_annotations is not None:
        value["classes"]["ProjectThing"]["annotations"] = class_annotations
    if prefixes is not None:
        value["prefixes"] = prefixes
    return yaml.safe_dump(value, sort_keys=False).encode()


def test_public_grounding_rite_surface_is_explicit() -> None:
    api = _inquisition()
    assert {
        "PackConformanceReceipt",
        "PackGroundingReceipt",
        "PackGroundingRefusal",
        "PackGroundingRefusalReason",
        "validate_pack_conformance",
        "validate_pack_grounding",
    } <= set(api.__all__)


@pytest.mark.parametrize("name", PACK_NAMES)
def test_shipped_pack_is_resolvable_grounded_and_compilable(name: str) -> None:
    compiler = _compiler()
    rite = _inquisition()
    path = bundled_ontology_path("packs", f"{name}.yaml")
    source = path.read_bytes()

    receipt = rite.validate_pack_grounding(source, role="PACK")
    compiled = compiler.compile_linkml_contract(
        root_locator=name,
        sources=_pack_sources(),
    )

    assert receipt.role == "PACK"
    assert receipt.source_sha256 == "sha256:" + sha256(source).hexdigest()
    assert receipt.grounded_subjects == ("https://malleus.dev/schema/packs/" + name,)
    assert compiled.artifact.validated_fact_set_sha256.startswith("sha256:")


def test_research_pack_carries_the_shared_assertion_modality() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    values = source["enums"]["AssertionModality"]["permissible_values"]
    assert set(values) == ASSERTION_MODALITIES


def test_metrology_uses_the_exact_vim_term_for_quantity_kind() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    )
    vocabularies = source["annotations"]["grounding"]["value"]["vocabularies"]
    vim_terms = next(
        item["borrowed_terms"]
        for item in vocabularies
        if item["vocabulary"].startswith("JCGM 200:2012")
    )

    assert "kind of quantity" in vim_terms
    assert "quantity kind" not in vim_terms
    assert "quantity_kind" in source["slots"]


def test_metrology_classifies_quantity_kinds_against_the_qudt_vocabulary() -> None:
    """A free-text kind alone is readable and not comparable.

    One producer wrote 137 distinct strings into ``quantity_kind`` for 137
    observations, so a type-only query binding could not sharpen. The pack
    carries a controlled classification whose values are QUDT quantity-kind
    names, plus one local escape, and the borrowed names are cited.
    """
    source = yaml.safe_load(
        bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    )
    values = source["enums"]["QuantityKindClass"]["permissible_values"]
    qudt = next(
        item
        for item in source["annotations"]["grounding"]["value"]["vocabularies"]
        if item["vocabulary"] == "QUDT Quantity Kinds"
    )

    assert tuple(values) == QUDT_QUANTITY_KINDS + ("OTHER",)
    assert qudt["vocabulary_url"] == QUDT_QUANTITY_KIND_NAMESPACE
    assert tuple(qudt["borrowed_terms"]) == QUDT_QUANTITY_KINDS
    assert source["version"] == "0.3.0"


def test_metrology_keeps_the_source_wording_beside_the_classification() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    )
    carried = source["classes"]["Quantified"]["slots"]

    assert carried.index("quantity_kind") + 1 == carried.index("quantity_kind_class")
    assert source["slots"]["quantity_kind"]["range"] == "string"
    assert source["slots"]["quantity_kind_class"]["range"] == "QuantityKindClass"


def test_compiled_quantity_kind_class_is_optional_and_carries_the_qudt_names() -> None:
    view = _compiler().compile_linkml_contract(
        root_locator="research",
        sources=_pack_sources(),
    ).view

    assert view.get_enum_values("QuantityKindClass") == frozenset(
        QUDT_QUANTITY_KINDS + ("OTHER",)
    )
    assert view.get_slot_constraint("Observation", "quantity_kind_class").required is (
        False
    )
    assert view.get_slot_constraint("Observation", "quantity_kind").required is False


def test_metrology_records_how_the_source_states_the_number() -> None:
    """A bound pair alone cannot carry a hedge or an open end.

    Twenty-five of run-04's sixty-one typed gaps are
    INTERVAL_NOT_EXPRESSIBLE reading "the source marks this value as
    approximate; the records carry the stated number as an exact bound pair and
    cannot carry the approximation", and run-05 declared a gap for a
    temperature the source states only as above a threshold. The pack carries
    an optional qualification of how the source states the number; the number
    and its unit are untouched.
    """
    source = yaml.safe_load(
        bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    )
    carried = source["classes"]["Quantified"]["slots"]
    grounding = source["annotations"]["grounding"]["value"]

    assert tuple(source["enums"]["ValueQualification"]["permissible_values"]) == (
        VALUE_QUALIFICATIONS
    )
    assert carried.index("value_upper") + 1 == carried.index("value_qualification")
    assert source["slots"]["value_qualification"]["range"] == "ValueQualification"
    assert grounding["invented_terms"] == ["ValueQualification"]
    assert "QUDT" in grounding["invention_search"]
    assert "UCUM" in grounding["invention_search"]
    assert "ISO 80000" in grounding["invention_search"]
    assert source["version"] == "0.3.0"


def test_compiled_value_qualification_admits_an_open_bound_and_a_hedge() -> None:
    """Run-05's open lower bound and run-04's approximations, as records."""
    view = _compiler().compile_linkml_contract(
        root_locator="research",
        sources=_pack_sources(),
    ).view

    assert view.get_enum_values("ValueQualification") == frozenset(
        VALUE_QUALIFICATIONS
    )
    for name in ("value_qualification", "value_lower", "value_upper"):
        assert view.get_slot_constraint("Observation", name).required is False
    assert view.validate_instance(
        "Observation",
        {
            "id": "observation:mantle-temperature-rc2",
            "quantity_kind": "mantle temperature",
            "value_lower": 1100.0,
            "unit": "Cel",
            "value_qualification": "OPEN_LOWER_BOUND",
        },
    ) == []
    assert view.validate_instance(
        "Observation",
        {
            "id": "observation:full-spreading-rate",
            "quantity_kind": "full spreading rate",
            "value_lower": 24.0,
            "value_upper": 24.0,
            "unit": "mm/a",
            "value_qualification": "APPROXIMATE",
        },
    ) == []


def test_shipped_pack_revision_is_its_own_conformance_baseline() -> None:
    """The rite's baseline is the exact reference bytes its caller supplies.

    ``validate_pack_conformance`` knows nothing of version history, so a
    shipped revision checked against the bytes it ships as is never refused
    for the declarations that revision added.
    """
    api = _inquisition()
    for name in PACK_NAMES:
        reference = bundled_ontology_path("packs", f"{name}.yaml").read_bytes()

        receipt = api.validate_pack_conformance(reference, reference=reference)

        assert receipt.source_sha256 == receipt.reference_sha256


def test_research_observation_is_explicitly_grounded_in_sosa_ssn() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    vocabularies = source["annotations"]["grounding"]["value"]["vocabularies"]
    sosa = next(item for item in vocabularies if item["vocabulary"] == "W3C SOSA/SSN")
    assert sosa["vocabulary_url"] == "https://www.w3.org/TR/vocab-ssn/"
    assert "Observation" in sosa["borrowed_terms"]


def test_research_grounding_assigns_only_supported_term_groups() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    grounding = source["annotations"]["grounding"]["value"]
    vocabularies = {
        item["vocabulary"]: item["borrowed_terms"] for item in grounding["vocabularies"]
    }

    assert vocabularies["W3C SOSA/SSN"] == ["Observation", "Sample"]
    assert vocabularies["JCGM 200:2012 (VIM), 3rd edition"] == ["measuring instrument"]
    assert vocabularies["OECD Frascati Manual 2015"] == [
        "research and experimental development",
        "investigation",
        "method",
    ]
    assert vocabularies["SEPIO"] == [
        "assertion",
        "Data Item",
        "Evidence Line",
        "support",
        "refute",
    ]
    assert {"Agent", "Campaign", "Instrument"}.isdisjoint(
        term for terms in vocabularies.values() for term in terms
    )
    assert grounding["invented_terms"] == [
        "Campaign",
        "Contribution",
        "ContributionRelation",
        "Evaluative",
        "HypothesisDisposition",
        "Instrument",
    ]
    assert grounding["invention_search"]


def test_research_carries_a_locator_and_a_digest_rather_than_source_text() -> None:
    """Verbatim source sentences in Claim.statement put copyrighted prose into
    graph state and forced one run's query rows out of the public repository.

    The graph carries a route back to the retained assertion and the digest of
    the exact text. Both sit on the SourceAsserted mixin, which reaches every
    claim-bearing record, and Source declares the licence that decides whether
    the sentence itself may be reproduced.
    """
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    asserted = source["classes"]["SourceAsserted"]["slots"]
    dcmi = next(
        item
        for item in source["annotations"]["grounding"]["value"]["vocabularies"]
        if item["vocabulary"] == "DCMI Metadata Terms"
    )

    assert asserted[-2:] == ["assertion_locator", "statement_sha256"]
    assert source["slots"]["assertion_locator"]["range"] == "string"
    assert source["slots"]["statement_sha256"]["range"] == "string"
    assert source["classes"]["Source"]["slots"] == ["licence"]
    assert source["slots"]["licence"]["range"] == "string"
    assert dcmi["borrowed_terms"] == ["license"]
    assert dcmi["vocabulary_url"] == (
        "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/"
    )
    assert source["version"] == "0.4.0"


def test_compiled_claim_keeps_statement_optional_beside_locator_and_digest() -> None:
    view = _compiler().compile_linkml_contract(
        root_locator="research",
        sources=_pack_sources(),
    ).view

    for holder in ("Claim", "Observation"):
        carried = view.effective_slots(holder)
        assert {"assertion_locator", "statement_sha256"} <= set(carried)
    for name in ("statement", "assertion_locator", "statement_sha256"):
        assert view.get_slot_constraint("Claim", name).required is False
    assert view.get_slot_constraint("Source", "licence").required is False


def test_project_claim_subclass_reaches_the_locator_and_digest() -> None:
    """Run-02's MechanismHypothesis is ``is_a: Claim``, so a project declaring
    nothing new must still reach both slots."""
    sources = _pack_sources()
    sources["project"] = b"""\
id: https://example.org/claim-bearing-project
name: claim_bearing_project
imports:
  - linkml:types
  - malleus
  - research
classes:
  MechanismHypothesis:
    is_a: Claim
"""

    compiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )

    assert {"assertion_locator", "statement_sha256"} <= set(
        compiled.view.effective_slots("MechanismHypothesis")
    )


def test_research_carries_the_credit_contributor_roles() -> None:
    """Run-04 declared two TYPE_ABSENT gaps for the roles its source states.

    The source names a specific contribution for each author and the accepted
    ontology carried no contribution-role vocabulary. CRediT is the published
    NISO standard for exactly that, so the pack ships its fourteen roles under
    their own definitions rather than coining a list.
    """
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    values = source["enums"]["ContributorRole"]["permissible_values"]
    credit = next(
        item
        for item in source["annotations"]["grounding"]["value"]["vocabularies"]
        if item["vocabulary"] == CREDIT_VOCABULARY
    )

    assert tuple(values) == tuple(CREDIT_ROLES) + ("OTHER",)
    assert tuple(credit["borrowed_terms"]) == CREDIT_ROLE_NAMES
    assert credit["vocabulary_url"] == CREDIT_TAXONOMY_URL
    for name, definition in CREDIT_ROLES.items():
        assert " ".join(values[name]["description"].split()) == definition
    assert source["version"] == "0.4.0"


def test_research_carries_the_contribution_relation_that_holds_the_role() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    grounding = source["annotations"]["grounding"]["value"]

    assert source["classes"]["Contribution"]["slots"] == ["contribution_role"]
    assert source["classes"]["Contribution"]["mixin"] is True
    assert source["classes"]["ContributionRelation"]["is_a"] == "ResearchRelation"
    assert source["classes"]["ContributionRelation"]["mixins"] == ["Contribution"]
    assert source["slots"]["contribution_role"]["range"] == "ContributorRole"
    assert (
        "CONTRIBUTED_TO" in source["enums"]["ResearchRelationType"]["permissible_values"]
    )
    assert grounding["invented_terms"] == [
        "Campaign",
        "Contribution",
        "ContributionRelation",
        "Evaluative",
        "HypothesisDisposition",
        "Instrument",
    ]


def test_compiled_contribution_role_is_optional_on_the_relation() -> None:
    view = _compiler().compile_linkml_contract(
        root_locator="research",
        sources=_pack_sources(),
    ).view
    credited = {
        "id": "contribution:yu-zhiteng-writing-original-draft",
        "relation_type": "CONTRIBUTED_TO",
        "source_id": "person:yu-zhiteng",
        "target_id": "source:yu-2025-mid-atlantic-ridge",
        "contribution_role": "WRITING_ORIGINAL_DRAFT",
    }

    assert view.get_enum_values("ContributorRole") == frozenset(
        tuple(CREDIT_ROLES) + ("OTHER",)
    )
    assert view.get_slot_constraint(
        "ContributionRelation", "contribution_role"
    ).required is False
    assert view.is_subtype_of("ContributionRelation", "Relation")
    assert view.validate_instance("ContributionRelation", credited) == []
    assert view.validate_instance(
        "ContributionRelation",
        {key: value for key, value in credited.items() if key != "contribution_role"},
    ) == []


def test_research_pack_matches_the_accepted_campaign_surface() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    classes = source["classes"]
    relations = source["enums"]["ResearchRelationType"]["permissible_values"]

    assert source["imports"] == ["linkml:types", "malleus", "metrology", "chronology"]
    assert classes["Campaign"]["is_a"] == "Entity"
    assert classes["Campaign"]["mixins"] == ["TemporalExtent", "Counted"]
    assert "Investigation" not in classes
    assert "PART_OF_CAMPAIGN" in relations
    assert "PART_OF_INVESTIGATION" not in relations


def test_governing_design_uses_the_executable_grounding_shape() -> None:
    design = (ROOT / "design" / "KNOWLEDGE_PACKS.md").read_text(encoding="utf-8")
    example = yaml.safe_load(
        design.split(GROUNDING_EXAMPLE_MARKER, 1)[1].split("\n```", 1)[0]
    )
    grounding = example["annotations"]["grounding"]

    assert set(grounding) == {"tag", "value"}
    assert grounding["tag"] == "grounding"
    assert set(grounding["value"]) == {
        "area",
        "taxonomy",
        "vocabularies",
        "invented_terms",
    }
    assert grounding["value"]["vocabularies"] == [
        {
            "vocabulary": "JCGM 200:2012 (VIM), 3rd edition",
            "vocabulary_url": (
                "https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf"
            ),
            "borrowed_terms": [
                "quantity value",
                "measurement unit",
                "measurement uncertainty",
                "kind of quantity",
            ],
        }
    ]
    assert "measured versus derived value" not in design
    assert "quantity kind" not in design
    assert _inquisition().validate_pack_grounding(
        _source(annotations=example["annotations"]),
        role="PACK",
    )


def test_governing_design_records_the_pack_revision_decisions() -> None:
    """The design record is where the reason survives the change.

    Decision 13 says why free text alone failed and why the list is QUDT's
    rather than a coined one. Decision 14 says why the graph carries a route
    and a digest instead of the sentence.
    """
    design = (ROOT / "design" / "KNOWLEDGE_PACKS.md").read_text(encoding="utf-8")
    normalized = " ".join(design.split())

    for phrase in (
        "13. A controlled quantity-kind classification in `metrology`",
        "137 distinct strings",
        "reuse before invent",
        "`QuantityKindClass`",
        "http://qudt.org/vocab/quantitykind/",
        "keeps the source's own wording",
        "additive",
        "14. Claim text policy",
        "`assertion_locator`",
        "`statement_sha256`",
        "`SourceAsserted` mixin",
        "declares a licence that permits reproduction",
        "a PDF text layer, a malleus-ocr bundle, a recon record, or a time "
        "span in a wav file",
    ):
        assert phrase in normalized
    assert normalized.index("13. A controlled quantity-kind classification") < (
        normalized.index("14. Claim text policy")
    )


def test_research_declares_which_slots_are_evaluative() -> None:
    """Decision 17. All five of run-04's hypothesis dispositions derive from
    HYPOTHESISED assertions: the sentence that raises each hypothesis, never
    the sentence that disposes of it. The pack now carries the disposition and
    names it evaluative, and the mixin's slot list is the declaration the
    document adapter reads through the compiled contract."""

    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )

    assert source["classes"]["Evaluative"]["mixin"] is True
    assert source["classes"]["Evaluative"]["slots"] == ["hypothesis_disposition"]
    assert "Evaluative" in source["classes"]["Claim"]["mixins"]
    assert source["slots"]["hypothesis_disposition"]["range"] == (
        "HypothesisDisposition"
    )
    assert tuple(source["enums"]["HypothesisDisposition"]["permissible_values"]) == (
        HYPOTHESIS_DISPOSITIONS
    )
    assert source["version"] == "0.4.0"


def test_compiled_evaluative_mixin_names_the_slots_the_adapter_reads() -> None:
    view = _compiler().compile_linkml_contract(
        root_locator="research",
        sources=_pack_sources(),
    ).view

    assert set(view.effective_slots("Evaluative")) == {"hypothesis_disposition"}
    assert view.get_slot_constraint("Claim", "hypothesis_disposition").required is (
        False
    )
    assert view.get_enum_values("HypothesisDisposition") == frozenset(
        HYPOTHESIS_DISPOSITIONS
    )


def test_governing_design_records_the_evaluative_slot_decision() -> None:
    """Decision 17 says which slots are evaluative and how a reader finds out."""

    design = (ROOT / "design" / "KNOWLEDGE_PACKS.md").read_text(encoding="utf-8")
    normalized = " ".join(design.split())

    for phrase in (
        "17. Evaluative slots in `research`",
        "`hypothesis_disposition`",
        "`Evaluative`",
        "`HypothesisDisposition`",
        "all five of run-04's dispositions derive from HYPOTHESISED assertions",
        "the mixin's slot list is the declaration",
        "0.4.0",
    ):
        assert phrase in normalized
    assert normalized.index("16. Contribution roles in `research`") < (
        normalized.index("17. Evaluative slots in `research`")
    )


def test_governing_design_records_the_second_pack_revision_decisions() -> None:
    """Decision 15 says why a bound pair could not carry a hedge or an open
    end, and that the vocabulary search found nothing to borrow. Decision 16
    says why the roles are CRediT's fourteen and not a coined list."""
    design = (ROOT / "design" / "KNOWLEDGE_PACKS.md").read_text(encoding="utf-8")
    normalized = " ".join(design.split())

    for phrase in (
        "15. How the source states its number, in `metrology`",
        "25 of run-04's 61 typed gaps",
        "`ValueQualification`",
        "`value_qualification`",
        "OPEN_LOWER_BOUND",
        "never changes the number",
        "no term for how a source qualifies a stated number",
        "16. Contribution roles in `research`",
        "ANSI/NISO Z39.104-2022",
        "`ContributorRole`",
        "fourteen roles",
        "https://credit.niso.org/",
        "0.3.0",
    ):
        assert phrase in normalized
    assert normalized.index("15. How the source states its number") < (
        normalized.index("16. Contribution roles in `research`")
    )


def test_governing_design_sketches_match_the_shipped_pack_revisions() -> None:
    design = (ROOT / "design" / "KNOWLEDGE_PACKS.md").read_text(encoding="utf-8")
    normalized = " ".join(design.split())
    metrology = normalized.split("### metrology", 1)[1].split("### chronology", 1)[0]
    research = normalized.split("### research", 1)[1].split("## Grounding", 1)[0]
    status = normalized.split("Status:", 1)[1].split("## Why", 1)[0]

    assert "`quantity_kind_class`" in metrology
    assert "`value_qualification`" in metrology
    assert "`assertion_locator`" in research
    assert "`statement_sha256`" in research
    assert "`licence`" in research
    assert "`contribution_role`" in research
    assert "0.2.0" in status
    assert "0.3.0" in status


def test_public_milestone_names_the_live_frozen_receipt_guard() -> None:
    index = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    current = (
        "test_vertical.py::"
        "test_recorded_research_receipt_stays_frozen_while_current_history_runs"
    )

    assert current in index
    assert "test_recorded_research_receipt_regenerates_from_the_exact_history" not in index


def test_project_importing_research_and_metrology_compiles_through_public_api() -> None:
    sources = _pack_sources()
    sources["project"] = b"""\
id: https://example.org/grounded-project
name: grounded_project
imports:
  - linkml:types
  - malleus
  - research
  - metrology
classes:
  StudyObservation:
    is_a: Observation
"""

    compiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )

    assert compiled.view.is_subtype_of("StudyObservation", "Entity")
    assert compiled.view.has_enum("AssertionModality")


def test_edited_pack_conformance_refuses_a_deleted_reference_surface() -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    del edited["classes"]
    del edited["slots"]
    del edited["enums"]
    candidate = yaml.safe_dump(edited, sort_keys=False).encode()

    assert api.validate_pack_grounding(candidate, role="PACK")
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(candidate, reference=reference)

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert "classes.Counted" in caught.value.detail
    assert "enums.Determination" in caught.value.detail
    assert "slots.quantity_kind" in caught.value.detail


def test_edited_pack_conformance_allows_documentation_and_additive_changes() -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    edited["description"] = "A locally documented compatible copy."
    edited["classes"]["LocalReading"] = {"is_a": "QuantityValue"}
    edited["enums"]["Determination"]["permissible_values"]["CALIBRATED"] = None
    candidate = yaml.safe_dump(edited, sort_keys=False).encode()

    receipt = api.validate_pack_conformance(candidate, reference=reference)

    assert receipt.source_id == "https://example.org/packs/local-metrology"
    assert receipt.reference_id == "https://malleus.dev/schema/packs/metrology"
    assert receipt.source_sha256 == "sha256:" + sha256(candidate).hexdigest()
    assert receipt.reference_sha256 == "sha256:" + sha256(reference).hexdigest()


@pytest.mark.parametrize(
    "mutate,expected_path",
    [
        (
            lambda source: source["classes"]["QuantityValue"].update(
                {"abstract": True}
            ),
            "classes.QuantityValue.abstract",
        ),
        (
            lambda source: source["slots"]["quantity_kind"].update({"required": True}),
            "slots.quantity_kind.required",
        ),
    ],
)
def test_edited_pack_conformance_refuses_stronger_existing_declarations(
    mutate,
    expected_path: str,
) -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    mutate(edited)

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(
            yaml.safe_dump(edited, sort_keys=False).encode(),
            reference=reference,
        )

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert expected_path in caught.value.detail


def test_edited_pack_conformance_refuses_a_new_mixin_on_an_existing_class() -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    edited["slots"]["local_tag"] = {"range": "string"}
    edited["classes"]["RequiredTag"] = {
        "mixin": True,
        "slots": ["local_tag"],
        "slot_usage": {"local_tag": {"required": True}},
    }
    edited["classes"]["QuantityValue"]["mixins"].append("RequiredTag")

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(
            yaml.safe_dump(edited, sort_keys=False).encode(),
            reference=reference,
        )

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert "classes.QuantityValue.mixins['RequiredTag']" in caught.value.detail


@pytest.mark.parametrize(
    "mutate,expected_path",
    [
        (
            lambda source: source["classes"]["QuantityValue"]["mixins"].append(
                "Quantified"
            ),
            "classes.QuantityValue.mixins['Quantified']",
        ),
        (
            lambda source: source["classes"]["Quantified"]["slots"].append(
                "quantity_kind"
            ),
            "classes.Quantified.slots['quantity_kind']",
        ),
    ],
)
def test_edited_pack_conformance_refuses_duplicate_existing_list_member(
    mutate,
    expected_path: str,
) -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    mutate(edited)

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(
            yaml.safe_dump(edited, sort_keys=False).encode(),
            reference=reference,
        )

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert expected_path in caught.value.detail


@pytest.mark.parametrize(
    "mutate",
    [
        lambda source: source["imports"].remove("malleus"),
        lambda source: source["imports"].append("malleus"),
    ],
)
def test_edited_pack_conformance_preserves_unique_reference_imports(mutate) -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    mutate(edited)

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(
            yaml.safe_dump(edited, sort_keys=False).encode(),
            reference=reference,
        )

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert "imports['malleus']" in caught.value.detail


def test_pack_without_grounding_refuses_with_typed_reason() -> None:
    api = _inquisition()
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(_source(), role="PACK")
    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_REQUIRED


def test_duplicate_yaml_key_refuses_as_malformed_source() -> None:
    api = _inquisition()

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            b"id: https://example.org/one\nid: https://example.org/two\n",
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.MALFORMED_SOURCE
    assert "Duplicate YAML key 'id'" in caught.value.detail


@pytest.mark.parametrize(
    "mutation,reason",
    [
        (
            lambda value: value.update({"surprise": "not declared"}),
            "GROUNDING_NOT_CLOSED",
        ),
        (
            lambda value: value["vocabularies"][0].update({"vocabulary_url": ""}),
            "GROUNDING_INCOMPLETE",
        ),
        (
            lambda value: value["vocabularies"][0].update({"borrowed_terms": []}),
            "GROUNDING_INCOMPLETE",
        ),
    ],
)
def test_grounding_shape_refuses_unknown_or_missing_meaning(
    mutation, reason: str
) -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    mutation(grounding)
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )
    assert caught.value.reason.name == reason


ROOT_FORMS = (
    "closed forms: area+taxonomy+vocabularies+invented_terms "
    "| area+taxonomy+vocabularies+invented_terms+invention_search "
    "| area+taxonomy+none_found+search+invented_terms"
)
ENTRY_FORM = "closed form: vocabulary+vocabulary_url+borrowed_terms"


def _classes(**bodies: dict[str, object]) -> bytes:
    value = yaml.safe_load(_source())
    value["classes"] = dict(bodies)
    return yaml.safe_dump(value, sort_keys=False).encode()


def _grounded_class(grounding: dict[str, object]) -> dict[str, object]:
    return {"is_a": "Entity", "annotations": _annotation(grounding)}


def _unclosed_entry() -> dict[str, object]:
    grounding = _cited_grounding()
    grounding["vocabularies"][0]["surprise"] = "not declared"
    return grounding


def test_project_grounding_reports_every_unclosed_entry_at_once() -> None:
    api = _inquisition()
    source = _classes(
        BetaThing=_grounded_class(_unclosed_entry()),
        AlphaThing=_grounded_class(_unclosed_entry()),
    )

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(source, role="PROJECT")

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_NOT_CLOSED
    assert caught.value.detail == (
        "grounding blocks are not accepted: "
        f"AlphaThing.grounding.vocabularies[0] fields are not closed "
        f"[GROUNDING_NOT_CLOSED] {ENTRY_FORM}; "
        f"BetaThing.grounding.vocabularies[0] fields are not closed "
        f"[GROUNDING_NOT_CLOSED] {ENTRY_FORM}"
    )


def test_project_grounding_reports_defects_of_different_reasons_together() -> None:
    api = _inquisition()
    unpaired = _cited_grounding()
    unpaired["invented_terms"] = ["LocalRidge"]
    source = _classes(
        AlphaThing=_grounded_class(_unclosed_entry()),
        BetaThing=_grounded_class(unpaired),
    )

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(source, role="PROJECT")

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_NOT_CLOSED
    assert caught.value.detail == (
        "grounding blocks are not accepted: "
        f"AlphaThing.grounding.vocabularies[0] fields are not closed "
        f"[GROUNDING_NOT_CLOSED] {ENTRY_FORM}; "
        f"BetaThing must pair invented terms with invention_search "
        f"[GROUNDING_INCOMPLETE] {ROOT_FORMS}"
    )


def test_pack_grounding_reports_every_entry_defect_in_one_block() -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    grounding["vocabularies"][0]["vocabulary_url"] = "not-absolute"
    grounding["vocabularies"].append(
        {
            "vocabulary": "ISO 8601",
            "vocabulary_url": "https://www.iso.org/iso-8601-date-and-time-format.html",
            "borrowed_terms": [],
        }
    )

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_INCOMPLETE
    assert caught.value.detail == (
        "grounding blocks are not accepted: "
        "https://example.org/project.grounding.vocabularies[0].vocabulary_url "
        f"must be an absolute locator [GROUNDING_INCOMPLETE] {ENTRY_FORM}; "
        "https://example.org/project.grounding.vocabularies[1].borrowed_terms "
        f"must be a nonempty unique string list [GROUNDING_INCOMPLETE] {ENTRY_FORM}"
    )


def test_unsupported_grounding_form_states_all_three_closed_forms() -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    grounding.pop("invented_terms")

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_NOT_CLOSED
    assert caught.value.detail == (
        "grounding blocks are not accepted: "
        "https://example.org/project grounding fields are not one supported "
        f"closed form [GROUNDING_NOT_CLOSED] {ROOT_FORMS}"
    )


def test_shape_defect_keeps_precedence_over_the_missing_root_report() -> None:
    api = _inquisition()
    source = _classes(
        AlphaThing={"is_a": "Entity"},
        BetaThing=_grounded_class(_unclosed_entry()),
    )

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(source, role="PROJECT")

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_NOT_CLOSED
    assert "AlphaThing" not in caught.value.detail


def test_project_direct_root_extension_requires_its_own_grounding() -> None:
    api = _inquisition()
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(_source(), role="PROJECT")
    assert (
        caught.value.reason
        is api.PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED
    )


def test_project_grounding_reports_every_ungrounded_direct_root_at_once() -> None:
    api = _inquisition()
    source = yaml.safe_load(_source())
    source["classes"] = {
        "GeologicFeature": {"is_a": "Entity"},
        "EarthMaterial": {"is_a": "Entity"},
        "GeologicOccurrence": {"is_a": "Event"},
    }

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            yaml.safe_dump(source, sort_keys=False).encode(),
            role="PROJECT",
        )

    assert (
        caught.value.reason
        is api.PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED
    )
    assert caught.value.detail == (
        "project classes extend Malleus roots without grounding: "
        "EarthMaterial extends Entity; GeologicFeature extends Entity; "
        "GeologicOccurrence extends Event"
    )


@pytest.mark.parametrize("prefix", ["malleus", "root"])
def test_project_malleus_curie_root_extension_requires_its_own_grounding(
    prefix: str,
) -> None:
    api = _inquisition()
    source = _source(
        parent=f"{prefix}:Entity",
        prefixes={prefix: "https://malleus.dev/schema/"},
    )
    sources = _pack_sources()
    sources["project"] = source

    compiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )
    assert compiled.view.is_subtype_of("ProjectThing", "Entity")

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(source, role="PROJECT")

    assert (
        caught.value.reason
        is api.PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED
    )


@pytest.mark.parametrize(
    "parent,prefixes",
    [
        ("foreign:Entity", {"foreign": "https://example.org/foreign/"}),
        ("https://malleus.dev/schema/Entity", None),
    ],
)
def test_project_grounding_ignores_noncompiler_root_spellings(
    parent: str,
    prefixes: dict[str, str] | None,
) -> None:
    receipt = _inquisition().validate_pack_grounding(
        _source(parent=parent, prefixes=prefixes),
        role="PROJECT",
    )

    assert receipt.grounded_subjects == ()


def test_project_may_record_a_bounded_none_found_search() -> None:
    api = _inquisition()
    none_found = {
        "area": "Retail operations",
        "taxonomy": "DDC 658.8",
        "none_found": True,
        "search": "No shared vocabulary found for the local shelf marker.",
        "invented_terms": ["LocalShelfMarker"],
    }
    source = _source(class_annotations=_annotation(none_found))
    receipt = api.validate_pack_grounding(source, role="PROJECT")
    sources = _pack_sources()
    sources["project"] = source
    compiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )

    assert receipt.grounded_subjects == ("ProjectThing",)
    assert compiled.view.is_subtype_of("ProjectThing", "Entity")

    revised = yaml.safe_load(source)
    revised["classes"]["ProjectThing"]["annotations"]["grounding"]["value"][
        "search"
    ] = "A second bounded vocabulary search found no shared shelf marker."
    sources["project"] = yaml.safe_dump(revised, sort_keys=False).encode()
    recompiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )

    assert compiled.artifact.validated_fact_set_sha256 == (
        recompiled.artifact.validated_fact_set_sha256
    )
    assert compiled.artifact.evidence != recompiled.artifact.evidence
    assert compiled.artifact.artifact_bytes != recompiled.artifact.artifact_bytes


def test_cited_grounding_requires_a_search_when_it_invents_terms() -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    grounding["invented_terms"] = ["LocalInstrument"]

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_INCOMPLETE


def test_project_class_extending_a_pack_class_needs_no_duplicate_grounding() -> None:
    receipt = _inquisition().validate_pack_grounding(
        _source(parent="Observation"),
        role="PROJECT",
    )
    assert receipt.grounded_subjects == ()


def test_grounding_changes_source_attestation_not_contract_fact_identity() -> None:
    sources = _pack_sources()
    baseline = _compiler().compile_linkml_contract(
        root_locator="metrology",
        sources=sources,
    )
    changed = yaml.safe_load(sources["metrology"])
    changed["annotations"]["grounding"]["value"]["area"] = (
        "Physical measurement and metrology"
    )
    sources["metrology"] = yaml.safe_dump(changed, sort_keys=False).encode()
    described = _compiler().compile_linkml_contract(
        root_locator="metrology",
        sources=sources,
    )

    assert baseline.artifact.validated_fact_set_sha256 == (
        described.artifact.validated_fact_set_sha256
    )
    assert baseline.artifact.evidence != described.artifact.evidence
    assert baseline.artifact.artifact_bytes != described.artifact.artifact_bytes


def test_pack_grounding_cli_reports_the_exact_receipt() -> None:
    path = bundled_ontology_path("packs", "metrology.yaml")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-grounding",
            str(path),
            "--role",
            "PACK",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["role"] == "PACK"
    assert payload["source_sha256"] == "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_pack_grounding_cli_reports_duplicate_key_as_typed_refusal(
    tmp_path: Path,
) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_bytes(b"id: https://example.org/one\nid: https://example.org/two\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-grounding",
            str(path),
            "--role",
            "PACK",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "MALFORMED_SOURCE" in result.stderr
    assert "Duplicate YAML key 'id'" in result.stderr
    assert "Traceback" not in result.stderr


def test_pack_conformance_cli_refuses_a_deleted_reference_surface(
    tmp_path: Path,
) -> None:
    reference = bundled_ontology_path("packs", "metrology.yaml")
    edited = yaml.safe_load(reference.read_bytes())
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    del edited["classes"]
    del edited["slots"]
    del edited["enums"]
    candidate = tmp_path / "local-metrology.yaml"
    candidate.write_text(yaml.safe_dump(edited, sort_keys=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-conformance",
            str(candidate),
            "--against",
            str(reference),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "PACK_SURFACE_NOT_PRESERVED" in result.stderr
    assert "Traceback" not in result.stderr

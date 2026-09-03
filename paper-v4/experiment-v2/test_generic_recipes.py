"""Guards for the value-generic paper-v4 v2 construction recipes."""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
from pathlib import Path

from malleus.kg import KnowledgeGraph
from malleus.ontology import OntologyRegistry

from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (
    derive_compiled_logical_contract,
    require_plan_contract_alignment,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (
    ExactSource,
    compile_exact_ontology,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.assembly import (
    assemble_plan,
    stage_and_materialize,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.stottr import (
    MGRP,
    RecipeTerm,
    compile_graph_recipe,
    expand_invocation,
    parse_stottr,
)


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "paper-v4/experiment-v2/ontology-run"
LIBRARY = ROOT / "paper-v4/experiment-v2/generic-recipes.stottr"
DOMAIN = "https://malleus.dev/domains/mid-ocean-ridge-geodynamics/"
RECIPE = "https://malleus.dev/paper-v4/experiment-v2/recipe/"
PROFILE = "https://malleus.dev/graph-recipe/profile/v0"

ENTITY_TYPES = (
    "ObservationMethod",
    "Instrument",
    "GeologicFeature",
    "SeismicPhenomenon",
    "QuantitativeObservation",
    "GeologicMaterial",
    "ChemicalConstituent",
    "GeologicProcess",
    "CategoricalObservation",
)
RELATION_TYPES = (
    "MethodUsesInstrumentRelation",
    "FeaturePartOfRelation",
    "SeismicPhenomenonOccursAtRelation",
    "ObservationCharacterizesRelation",
    "ObservationConcernsConstituentRelation",
    "MaterialOccursAtRelation",
    "ProcessActsOnMaterialRelation",
    "ProcessReleasesConstituentRelation",
    "ProcessCausesProcessRelation",
    "ProcessTriggersSeismicPhenomenonRelation",
)
ABSTRACT_TYPES = ("GeoscienceObject", "DomainObservation")
CONCRETE_TYPES = (*ENTITY_TYPES, *RELATION_TYPES)
RECORD_TYPE_IRIS = tuple(DOMAIN + name for name in (*CONCRETE_TYPES, *ABSTRACT_TYPES))
TEMPLATES = tuple(name + "-1.0.0" for name in CONCRETE_TYPES)
FIXED_RELATION_VALUES = {
    "METHOD_USES_INSTRUMENT",
    "FEATURE_PART_OF",
    "SEISMIC_PHENOMENON_OCCURS_AT",
    "OBSERVATION_CHARACTERIZES",
    "OBSERVATION_CONCERNS_CONSTITUENT",
    "MATERIAL_OCCURS_AT",
    "PROCESS_ACTS_ON_MATERIAL",
    "PROCESS_RELEASES_CONSTITUENT",
    "PROCESS_CAUSES_PROCESS",
    "PROCESS_TRIGGERS_SEISMIC_PHENOMENON",
}


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _source(locator: str, source: bytes) -> ExactSource:
    return ExactSource(locator, source, _digest(source))


def _compilation():
    ontology = (RUN / "ontology-02.yaml").read_bytes()
    malleus = (RUN / "inputs/malleus.yaml").read_bytes()
    linkml_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    return compile_exact_ontology(
        root=_source("paper-v4:v2-marine-ontology", ontology),
        malleus=_source("malleus", malleus),
        linkml_types=_source("linkml:types", linkml_types),
    ).compilation


def _registry() -> OntologyRegistry:
    return OntologyRegistry(
        RUN / "ontology-02.yaml",
        import_map={"malleus": str((RUN / "inputs/malleus.yaml").resolve())},
    )


def _iri(value: str) -> RecipeTerm:
    return RecipeTerm.iri(value)


def _string(value: str) -> RecipeTerm:
    return RecipeTerm.literal(value)


def _float(value: str) -> RecipeTerm:
    return RecipeTerm.literal(value, "http://www.w3.org/2001/XMLSchema#float")


def _member(name: str) -> RecipeTerm:
    return _iri(f"urn:malleus:paper-v4:v2-test-member:{name}")


def _entity_invocations() -> list[tuple[str, str, dict[str, RecipeTerm]]]:
    return [
        (
            "ObservationMethod-1.0.0",
            "method",
            {
                "member": _member("method"),
                "recordId": _string("sentinel:method"),
                "name": _string("fictional thermal survey"),
                "observationMethodKind": _string("THERMAL_MODELING"),
            },
        ),
        (
            "Instrument-1.0.0",
            "instrument",
            {
                "member": _member("instrument"),
                "recordId": _string("sentinel:instrument"),
                "name": _string("fictional field sensor"),
                "instrumentKind": _string("SEISMOMETER"),
            },
        ),
        *(
            (
                "GeologicFeature-1.0.0",
                slug,
                {
                    "member": _member(slug),
                    "recordId": _string(f"sentinel:{slug}"),
                    "name": _string(label),
                    "geologicFeatureKind": _string(kind),
                },
            )
            for slug, label, kind in (
                ("feature-small", "fictional small cone", "VOLCANIC_CONE"),
                ("feature-large", "fictional large mound", "HYDROTHERMAL_MOUND"),
            )
        ),
        (
            "SeismicPhenomenon-1.0.0",
            "seismic",
            {
                "member": _member("seismic"),
                "recordId": _string("sentinel:seismic"),
                "name": _string("fictional seismic swarm"),
                "seismicPhenomenonKind": _string("EARTHQUAKE_SWARM"),
            },
        ),
        (
            "QuantitativeObservation-1.0.0",
            "quantity",
            {
                "member": _member("quantity"),
                "recordId": _string("sentinel:quantity"),
                "name": _string("fictional temperature interval"),
                "quantityKind": _string("TEMPERATURE"),
                "lowerNumericValue": _float("111.25"),
                "upperNumericValue": _float("222.75"),
                "measurementUnit": _string("DEGREE_CELSIUS"),
                "observationBasis": _string("MEASURED"),
            },
        ),
        (
            "GeologicMaterial-1.0.0",
            "material",
            {
                "member": _member("material"),
                "recordId": _string("sentinel:material"),
                "name": _string("fictional sediment"),
                "geologicMaterialKind": _string("SEDIMENT"),
            },
        ),
        (
            "ChemicalConstituent-1.0.0",
            "constituent",
            {
                "member": _member("constituent"),
                "recordId": _string("sentinel:constituent"),
                "name": _string("fictional constituent"),
                "chemicalFormula": _string("Xy9"),
            },
        ),
        *(
            (
                "GeologicProcess-1.0.0",
                slug,
                {
                    "member": _member(slug),
                    "recordId": _string(f"sentinel:{slug}"),
                    "name": _string(label),
                    "geologicProcessKind": _string(kind),
                },
            )
            for slug, label, kind in (
                (
                    "process-first",
                    "fictional fluid circulation",
                    "HYDROTHERMAL_CIRCULATION",
                ),
                (
                    "process-second",
                    "fictional cooling process",
                    "LITHOSPHERE_COOLING",
                ),
            )
        ),
        (
            "CategoricalObservation-1.0.0",
            "category",
            {
                "member": _member("category"),
                "recordId": _string("sentinel:category"),
                "name": _string("fictional morphology observation"),
                "categoricalObservationKind": _string("MORPHOLOGY"),
                "categoricalObservationValue": _string("SMOOTH"),
                "observationBasis": _string("OBSERVED"),
            },
        ),
    ]


def _relation(
    template: str,
    slug: str,
    source: str,
    target: str,
) -> tuple[str, str, dict[str, RecipeTerm]]:
    return (
        template,
        slug,
        {
            "member": _member(slug),
            "recordId": _string(f"sentinel:{slug}"),
            "sourceMember": _member(source),
            "sourceId": _string(f"sentinel:{source}"),
            "targetMember": _member(target),
            "targetId": _string(f"sentinel:{target}"),
        },
    )


def _relation_invocations() -> list[tuple[str, str, dict[str, RecipeTerm]]]:
    return [
        _relation(
            "MethodUsesInstrumentRelation-1.0.0",
            "relation-method-instrument",
            "method",
            "instrument",
        ),
        _relation(
            "FeaturePartOfRelation-1.0.0",
            "relation-feature-part",
            "feature-small",
            "feature-large",
        ),
        _relation(
            "SeismicPhenomenonOccursAtRelation-1.0.0",
            "relation-seismic-feature",
            "seismic",
            "feature-small",
        ),
        _relation(
            "ObservationCharacterizesRelation-1.0.0",
            "relation-observation-seismic",
            "quantity",
            "seismic",
        ),
        _relation(
            "ObservationConcernsConstituentRelation-1.0.0",
            "relation-observation-constituent",
            "quantity",
            "constituent",
        ),
        _relation(
            "MaterialOccursAtRelation-1.0.0",
            "relation-material-feature",
            "material",
            "feature-small",
        ),
        _relation(
            "ProcessActsOnMaterialRelation-1.0.0",
            "relation-process-material",
            "process-first",
            "material",
        ),
        _relation(
            "ProcessReleasesConstituentRelation-1.0.0",
            "relation-process-constituent",
            "process-first",
            "constituent",
        ),
        _relation(
            "ProcessCausesProcessRelation-1.0.0",
            "relation-process-process",
            "process-first",
            "process-second",
        ),
        _relation(
            "ProcessTriggersSeismicPhenomenonRelation-1.0.0",
            "relation-process-seismic",
            "process-second",
            "seismic",
        ),
    ]


def test_each_concrete_record_has_one_value_generic_wrapper() -> None:
    document = parse_stottr(LIBRARY.read_bytes(), LIBRARY.name)
    templates = {template.template_iri: template for template in document.templates}
    assert set(templates) == {
        *(MGRP + name for name in (
            "Record",
            "Property",
            "RelationSource",
            "RelationTarget",
            "DependsOn",
        )),
        *(RECIPE + name for name in TEMPLATES),
    }

    wrapped_types = []
    observed_literals = set()
    for template_name in TEMPLATES:
        template = templates[RECIPE + template_name]
        records = [
            call for call in template.patterns if call.template_iri == MGRP + "Record"
        ]
        assert len(records) == 1
        record = records[0]
        assert record.arguments[2].kind == "iri"
        wrapped_types.append(record.arguments[2].value)
        assert record.arguments[3].kind == "variable"

        for call in template.patterns:
            if call.template_iri == MGRP + "Property":
                assert call.arguments[1].kind == "iri"
                if call.arguments[1].value != "https://malleus.dev/schema/relation_type":
                    assert call.arguments[2].kind == "variable"
            if call.template_iri in {
                MGRP + "RelationSource",
                MGRP + "RelationTarget",
            }:
                assert call.arguments[1].kind == "variable"
            for argument in call.arguments:
                if argument.kind == "literal":
                    observed_literals.add(argument.value)

    assert set(wrapped_types) == {DOMAIN + name for name in CONCRETE_TYPES}
    assert len(wrapped_types) == len(set(wrapped_types))
    assert observed_literals == FIXED_RELATION_VALUES


def test_library_contains_no_document_answers_or_population_identity() -> None:
    lowered = LIBRARY.read_text().lower()
    for forbidden in (
        "smarties",
        "rc2",
        "2019",
        "co2",
        "wt%",
        "beneath",
        "ascending melt",
        "deep mantle earthquakes",
        "block_id",
        "locator",
        "record-id:",
    ):
        assert forbidden not in lowered


def test_all_recipes_compile_and_form_one_valid_fictional_plan() -> None:
    compilation = _compilation()
    contract = derive_compiled_logical_contract(
        compilation,
        record_type_iris=RECORD_TYPE_IRIS,
        contract_id="https://malleus.dev/contracts/paper-v4/experiment-v2",
    )
    for abstract_name in ABSTRACT_TYPES:
        abstract_iri = DOMAIN + abstract_name
        record = contract.record_for_iri(abstract_iri)
        assert record.abstract is True
        assert record.legal_operation_kind is None
        assert abstract_iri not in contract.constructible_record_types
    assert set(contract.constructible_record_types) == {
        DOMAIN + name for name in CONCRETE_TYPES
    }

    document = parse_stottr(LIBRARY.read_bytes(), LIBRARY.name)
    emissions = []
    invocation_digests = []
    invocations = [*_entity_invocations(), *_relation_invocations()]
    assert {template for template, _, _ in invocations} == set(TEMPLATES)
    for template_name, slug, arguments in invocations:
        compiled = compile_graph_recipe(
            (document,),
            root_template=RECIPE + template_name,
            contract_digest=contract.contract_digest,
            profile_id=PROFILE,
            expansion_profile_id=PROFILE,
        )
        expansion = expand_invocation(
            compiled,
            invocation_id=f"https://malleus.dev/paper-v4/experiment-v2/test/{slug}",
            arguments=arguments,
        )
        emissions.extend(expansion.emissions)
        invocation_digests.append(expansion.invocation_digest)

    plan = assemble_plan(
        contract,
        emissions,
        invocation_digests=invocation_digests,
    )
    assert require_plan_contract_alignment(plan, contract, compilation) is plan
    assert len(plan.operations) == 21
    result = stage_and_materialize(KnowledgeGraph(_registry()), plan)
    assert result.materialization == "committed-atomically"
    assert len(result.snapshot["nodes"]) == 11
    assert len(result.snapshot["relations"]) == 10

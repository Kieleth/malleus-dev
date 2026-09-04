"""Guards for the answer-free paper-v4 construction recipes."""

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
RUN = ROOT / "paper-v4/experiment/ontology-run"
LIBRARY = ROOT / "paper-v4/experiment/generic-recipes.stottr"
DOMAIN = "https://malleus.dev/schema/paper-four-domain/"
RECIPE = "https://malleus.dev/paper-v4/recipe/"
PROFILE = "https://malleus.dev/graph-recipe/profile/v0"
RECORD_TYPES = tuple(
    DOMAIN + name
    for name in (
        "ObservingSystem",
        "Campaign",
        "Region",
        "EarthquakePopulation",
        "PrimaryMeltPopulation",
        "BoundedQuantity",
        "MechanismHypothesis",
        "DataAcquisitionRelation",
        "SpatialAssociationRelation",
        "QuantityCharacterizationRelation",
        "HypothesisExplainsRelation",
    )
)
TEMPLATES = (
    "NamedEntity-1.0.0",
    "ObservingSystem-1.0.0",
    "BoundedQuantity-1.0.0",
    "MechanismHypothesis-1.0.0",
    "DataAcquisitionRelation-1.0.0",
    "SpatialAssociationRelation-1.0.0",
    "QuantityCharacterizationRelation-1.0.0",
    "HypothesisExplainsRelation-1.0.0",
)
FIXED_ONTOLOGY_VALUES = {
    "PREFERRED",
    "DATA_ACQUISITION",
    "SPATIAL_ASSOCIATION",
    "QUANTITY_CHARACTERIZATION",
    "EXPLAINS",
}


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _source(locator: str, source: bytes) -> ExactSource:
    return ExactSource(locator, source, _digest(source))


def _compilation():
    ontology = (RUN / "ontology.yaml").read_bytes()
    malleus = (RUN / "inputs/malleus.yaml").read_bytes()
    linkml_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    return compile_exact_ontology(
        root=_source("paper-v4:marine-ontology", ontology),
        malleus=_source("malleus", malleus),
        linkml_types=_source("linkml:types", linkml_types),
    ).compilation


def _registry() -> OntologyRegistry:
    return OntologyRegistry(
        RUN / "ontology.yaml",
        import_map={"malleus": str((RUN / "inputs/malleus.yaml").resolve())},
    )


def _iri(value: str) -> RecipeTerm:
    return RecipeTerm.iri(value)


def _string(value: str) -> RecipeTerm:
    return RecipeTerm.literal(value)


def _float(value: str) -> RecipeTerm:
    return RecipeTerm.literal(value, "http://www.w3.org/2001/XMLSchema#float")


def _member(name: str) -> RecipeTerm:
    return _iri(f"urn:malleus:paper-v4:test-member:{name}")


def _invocations() -> tuple[tuple[str, str, dict[str, RecipeTerm]], ...]:
    named = (
        ("campaign", "Campaign", "fictional campaign"),
        ("region", "Region", "fictional region"),
        ("earthquakes", "EarthquakePopulation", "fictional event cohort"),
        ("melt", "PrimaryMeltPopulation", "fictional melt cohort"),
    )
    values: list[tuple[str, str, dict[str, RecipeTerm]]] = [
        (
            "NamedEntity-1.0.0",
            name,
            {
                "member": _member(name),
                "recordType": _iri(DOMAIN + record_type),
                "recordId": _string(f"sentinel:{name}"),
                "name": _string(label),
            },
        )
        for name, record_type, label in named
    ]
    values.extend(
        (
            (
                "ObservingSystem-1.0.0",
                "system",
                {
                    "member": _member("system"),
                    "recordId": _string("sentinel:system"),
                    "name": _string("fictional observing system"),
                    "instrumentKind": _string("fictional gauge"),
                },
            ),
            (
                "BoundedQuantity-1.0.0",
                "quantity-a",
                {
                    "member": _member("quantity-a"),
                    "recordId": _string("sentinel:quantity:a"),
                    "quantityKind": _string("fictional depth"),
                    "lowerValue": _float("1.25"),
                    "upperValue": _float("2.75"),
                    "unit": _string("fictional unit a"),
                    "quantityStatus": _string("REPORTED_OBSERVATION"),
                },
            ),
            (
                "BoundedQuantity-1.0.0",
                "quantity-b",
                {
                    "member": _member("quantity-b"),
                    "recordId": _string("sentinel:quantity:b"),
                    "quantityKind": _string("fictional composition"),
                    "lowerValue": _float("0.5"),
                    "upperValue": _float("3.0"),
                    "unit": _string("fictional unit b"),
                    "quantityStatus": _string("CALCULATED_ESTIMATE"),
                },
            ),
            (
                "MechanismHypothesis-1.0.0",
                "hypothesis",
                {
                    "member": _member("hypothesis"),
                    "recordId": _string("sentinel:hypothesis"),
                    "initiatingCondition": _string("fictional initial state"),
                    "transformation": _string("fictional transformation"),
                    "physicalEffect": _string("fictional physical effect"),
                    "stressContext": _string("fictional stress context"),
                    "outcome": _string("fictional outcome"),
                },
            ),
            (
                "DataAcquisitionRelation-1.0.0",
                "acquisition",
                {
                    "member": _member("acquisition"),
                    "recordId": _string("sentinel:relation:acquisition"),
                    "sourceMember": _member("campaign"),
                    "sourceId": _string("sentinel:campaign"),
                    "targetMember": _member("system"),
                    "targetId": _string("sentinel:system"),
                    "instrumentCount": RecipeTerm.integer(7),
                    "dataKind": _string("fictional data"),
                },
            ),
            (
                "SpatialAssociationRelation-1.0.0",
                "spatial",
                {
                    "member": _member("spatial"),
                    "recordId": _string("sentinel:relation:spatial"),
                    "sourceMember": _member("earthquakes"),
                    "sourceId": _string("sentinel:earthquakes"),
                    "targetMember": _member("region"),
                    "targetId": _string("sentinel:region"),
                    "relativePosition": _string("fictional relative position"),
                },
            ),
            (
                "QuantityCharacterizationRelation-1.0.0",
                "quantity-link-a",
                {
                    "member": _member("quantity-link-a"),
                    "recordId": _string("sentinel:relation:quantity:a"),
                    "sourceMember": _member("quantity-a"),
                    "sourceId": _string("sentinel:quantity:a"),
                    "targetMember": _member("earthquakes"),
                    "targetId": _string("sentinel:earthquakes"),
                },
            ),
            (
                "QuantityCharacterizationRelation-1.0.0",
                "quantity-link-b",
                {
                    "member": _member("quantity-link-b"),
                    "recordId": _string("sentinel:relation:quantity:b"),
                    "sourceMember": _member("quantity-b"),
                    "sourceId": _string("sentinel:quantity:b"),
                    "targetMember": _member("melt"),
                    "targetId": _string("sentinel:melt"),
                },
            ),
            (
                "HypothesisExplainsRelation-1.0.0",
                "explanation",
                {
                    "member": _member("explanation"),
                    "recordId": _string("sentinel:relation:explanation"),
                    "sourceMember": _member("hypothesis"),
                    "sourceId": _string("sentinel:hypothesis"),
                    "targetMember": _member("earthquakes"),
                    "targetId": _string("sentinel:earthquakes"),
                },
            ),
        )
    )
    return tuple(values)


def test_recipe_constants_are_only_ontology_fixed_values() -> None:
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

    observed_values = set()
    for template_name in TEMPLATES:
        template = templates[RECIPE + template_name]
        for call in template.patterns:
            if call.template_iri == MGRP + "Record":
                assert call.arguments[3].kind == "variable"
            if call.template_iri in {MGRP + "RelationSource", MGRP + "RelationTarget"}:
                assert call.arguments[1].kind == "variable"
            for argument in call.arguments:
                if argument.kind == "literal":
                    observed_values.add(argument.value)
    assert observed_values == FIXED_ONTOLOGY_VALUES


def test_all_generic_recipes_form_one_valid_arbitrary_plan() -> None:
    compilation = _compilation()
    contract = derive_compiled_logical_contract(
        compilation,
        record_type_iris=RECORD_TYPES,
        contract_id="https://malleus.dev/contracts/paper-four-domain",
    )
    document = parse_stottr(LIBRARY.read_bytes(), LIBRARY.name)
    emissions = []
    invocation_digests = []
    for template_name, slug, arguments in _invocations():
        compiled = compile_graph_recipe(
            (document,),
            root_template=RECIPE + template_name,
            contract_digest=contract.contract_digest,
            profile_id=PROFILE,
            expansion_profile_id=PROFILE,
        )
        expansion = expand_invocation(
            compiled,
            invocation_id=f"https://malleus.dev/paper-v4/test-invocation/{slug}",
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
    assert len(plan.operations) == 13
    result = stage_and_materialize(KnowledgeGraph(_registry()), plan)
    assert result.materialization == "committed-atomically"

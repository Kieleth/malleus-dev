"""Fiction-only checks for the paper-local D3 population compiler."""

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (
    derive_compiled_logical_contract,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (
    ExactSource,
    compile_exact_ontology,
)
from research.ontology_driven_kg_realization.experiments.document_paper.population_compile import (
    PopulationCompileRefusal,
    PopulationRecipeProfile,
    compile_population,
)
from tests.contract_compiler.pareto.test_validated_contract import _trusted_types


ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / "paper-v4/experiment"
ONTOLOGY = (RUN / "population-run/inputs/ontology.yaml").read_bytes()
RECIPES = (RUN / "population-run/inputs/generic-recipes.stottr").read_bytes()
DOMAIN = "https://malleus.dev/schema/paper-four-domain/"
BLOCKS = frozenset({"fiction:block:1", "fiction:block:2"})
READING = json.dumps(
    {
        "block_count": 2,
        "extractor": {},
        "page_count": 1,
        "pages": [
            {
                "blocks": [
                    {
                        "id": block,
                        "ordinal": index,
                        "sha256": "sha256:" + "0" * 64,
                        "text": "fiction\n",
                    }
                    for index, block in enumerate(sorted(BLOCKS), start=1)
                ],
                "page": 1,
            }
        ],
        "projection": {},
        "schema": "malleus.paper-v4.text-layer-reading/v1",
        "source_sha256": "sha256:" + "1" * 64,
    },
    allow_nan=False,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
).encode("utf-8")
ONTOLOGY_DIGEST = "sha256:" + sha256(ONTOLOGY).hexdigest()
READING_DIGEST = "sha256:" + sha256(READING).hexdigest()
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
V1_PROFILE_FIELDS = {
    "population_schema": "malleus.paper-v4.population/v1",
    "selected_reading_schema": "malleus.paper-v4.text-layer-reading/v1",
    "provenance_schema": "malleus.paper-v4.population-provenance/v1",
    "graph_recipe_profile_iri": "https://malleus.dev/graph-recipe/profile/v0",
    "recipe_namespace": "https://malleus.dev/paper-v4/recipe/",
    "member_namespace": "https://malleus.dev/paper-v4/population/member/",
    "record_type_templates": (
        ("Campaign", "NamedEntity-1.0.0"),
        ("Region", "NamedEntity-1.0.0"),
        ("EarthquakePopulation", "NamedEntity-1.0.0"),
        ("PrimaryMeltPopulation", "NamedEntity-1.0.0"),
        ("ObservingSystem", "ObservingSystem-1.0.0"),
        ("BoundedQuantity", "BoundedQuantity-1.0.0"),
        ("MechanismHypothesis", "MechanismHypothesis-1.0.0"),
        ("DataAcquisitionRelation", "DataAcquisitionRelation-1.0.0"),
        ("SpatialAssociationRelation", "SpatialAssociationRelation-1.0.0"),
        (
            "QuantityCharacterizationRelation",
            "QuantityCharacterizationRelation-1.0.0",
        ),
        ("HypothesisExplainsRelation", "HypothesisExplainsRelation-1.0.0"),
    ),
}
V1_PROFILE = PopulationRecipeProfile(**V1_PROFILE_FIELDS)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _source(locator: str, source: bytes) -> ExactSource:
    return ExactSource(locator, source, _digest(source))


@pytest.fixture(scope="module")
def compiler_inputs():
    malleus = (RUN / "ontology-run/inputs/malleus.yaml").read_bytes()
    linkml_types = _trusted_types()
    compilation = compile_exact_ontology(
        root=_source("paper-v4:fiction-ontology", ONTOLOGY),
        malleus=_source("malleus", malleus),
        linkml_types=_source("linkml:types", linkml_types),
    ).compilation
    contract = derive_compiled_logical_contract(
        compilation,
        record_type_iris=RECORD_TYPES,
        contract_id="https://malleus.dev/contracts/paper-four-fiction",
    )
    return compilation, contract


def _located(value, block_id: str = "fiction:block:1") -> dict[str, object]:
    return {"value": value, "block_id": block_id}


def _population() -> dict[str, object]:
    return {
        "schema": "malleus.paper-v4.population/v1",
        "ontology_sha256": ONTOLOGY_DIGEST,
        "reading_sha256": READING_DIGEST,
        "records": [
            {
                "record_id": "fiction:campaign",
                "record_type": "Campaign",
                "record_block_id": "fiction:block:1",
                "properties": {"name": _located("Fictional campaign")},
            },
            {
                "record_id": "fiction:system",
                "record_type": "ObservingSystem",
                "record_block_id": "fiction:block:1",
                "properties": {
                    "name": _located("Fictional array"),
                    "instrument_kind": _located("fictional gauge"),
                },
            },
            {
                "record_id": "fiction:acquisition",
                "record_type": "DataAcquisitionRelation",
                "record_block_id": "fiction:block:2",
                "properties": {
                    "instrument_count": _located(3, "fiction:block:2"),
                    "data_kind": _located("fictional samples", "fiction:block:2"),
                },
                "source": {
                    "record_id": "fiction:campaign",
                    "block_id": "fiction:block:2",
                },
                "target": {
                    "record_id": "fiction:system",
                    "block_id": "fiction:block:2",
                },
            },
        ],
    }


def _bytes(population: dict[str, object]) -> bytes:
    return json.dumps(
        population,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _compile(
    compiler_inputs,
    population=None,
    *,
    recipes=RECIPES,
    reading=READING,
    recipe_profile=V1_PROFILE,
):
    compilation, contract = compiler_inputs
    return compile_population(
        _bytes(_population() if population is None else population),
        compiled_ontology=compilation,
        logical_contract=contract,
        generic_recipe_bytes=recipes,
        selected_reading_bytes=reading,
        recipe_profile=recipe_profile,
    )


def _codes(error: PopulationCompileRefusal) -> set[str]:
    return {item.code for item in error.diagnostics}


@pytest.mark.parametrize("field", tuple(V1_PROFILE_FIELDS))
def test_population_recipe_profile_has_no_implicit_field(field: str) -> None:
    fields = dict(V1_PROFILE_FIELDS)
    del fields[field]

    with pytest.raises(TypeError, match=field):
        PopulationRecipeProfile(**fields)


def test_population_recipe_profile_rejects_duplicate_record_type_mapping() -> None:
    fields = dict(V1_PROFILE_FIELDS)
    fields["record_type_templates"] = V1_PROFILE.record_type_templates + (
        ("Campaign", "OtherTemplate-1.0.0"),
    )

    with pytest.raises(ValueError, match="duplicate record types: Campaign"):
        PopulationRecipeProfile(**fields)


def test_population_recipe_profile_rejects_unmapped_population_type(
    compiler_inputs,
) -> None:
    fields = dict(V1_PROFILE_FIELDS)
    fields["record_type_templates"] = tuple(
        mapping
        for mapping in V1_PROFILE.record_type_templates
        if mapping[0] != "Campaign"
    )

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(
            compiler_inputs,
            recipe_profile=PopulationRecipeProfile(**fields),
        )
    assert _codes(refusal.value) == {"POPULATION_RECORD_TYPE_UNMAPPED"}


def test_population_recipe_profile_rejects_unknown_contract_mapping(
    compiler_inputs,
) -> None:
    fields = dict(V1_PROFILE_FIELDS)
    fields["record_type_templates"] = V1_PROFILE.record_type_templates + (
        ("ImaginedType", "ImaginedType-1.0.0"),
    )

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(
            compiler_inputs,
            recipe_profile=PopulationRecipeProfile(**fields),
        )
    assert _codes(refusal.value) == {"POPULATION_PROFILE_RECORD_TYPE_UNKNOWN"}


def test_population_recipe_profile_rejects_abstract_contract_mapping(
    compiler_inputs,
) -> None:
    compilation, contract = compiler_inputs
    campaign = contract.record_for_symbol("Campaign")
    abstract_campaign = replace(campaign, abstract=True, legal_operation_kind=None)
    record_types = tuple(
        abstract_campaign if record == campaign else record
        for record in contract.record_types
    )
    abstract_contract = replace(
        contract,
        record_types=record_types,
        constructible_record_types=tuple(
            record.type_iri for record in record_types if not record.abstract
        ),
    )

    with pytest.raises(PopulationCompileRefusal) as refusal:
        compile_population(
            _bytes(_population()),
            compiled_ontology=compilation,
            logical_contract=abstract_contract,
            generic_recipe_bytes=RECIPES,
            selected_reading_bytes=READING,
            recipe_profile=V1_PROFILE,
        )
    assert _codes(refusal.value) == {
        "POPULATION_PROFILE_RECORD_TYPE_NONCONSTRUCTIBLE"
    }


def test_population_recipe_profile_rejects_unknown_template_mapping(
    compiler_inputs,
) -> None:
    fields = dict(V1_PROFILE_FIELDS)
    fields["record_type_templates"] = tuple(
        (record_type, "MissingTemplate-1.0.0")
        if record_type == "Campaign"
        else (record_type, template)
        for record_type, template in V1_PROFILE.record_type_templates
    )

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(
            compiler_inputs,
            recipe_profile=PopulationRecipeProfile(**fields),
        )
    assert _codes(refusal.value) == {"POPULATION_PROFILE_TEMPLATE_UNKNOWN"}


def test_population_schema_profile_field_is_enforced(compiler_inputs) -> None:
    schema = "example.population/v2"
    profile = replace(V1_PROFILE, population_schema=schema)
    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(compiler_inputs, recipe_profile=profile)
    assert _codes(refusal.value) == {"POPULATION_SCHEMA_INVALID"}

    population = _population()
    population["schema"] = schema
    assert _compile(compiler_inputs, population, recipe_profile=profile).plan.operations


def test_selected_reading_schema_profile_field_is_enforced(
    compiler_inputs,
) -> None:
    schema = "example.reading/v2"
    profile = replace(V1_PROFILE, selected_reading_schema=schema)
    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(compiler_inputs, recipe_profile=profile)
    assert _codes(refusal.value) == {"POPULATION_READING_INVALID"}

    reading = json.loads(READING)
    reading["schema"] = schema
    reading_bytes = _bytes(reading) + b"\n"
    population = _population()
    population["reading_sha256"] = _digest(reading_bytes)
    assert _compile(
        compiler_inputs,
        population,
        reading=reading_bytes,
        recipe_profile=profile,
    ).plan.operations


def test_provenance_schema_profile_field_controls_output(compiler_inputs) -> None:
    schema = "example.provenance/v2"
    result = _compile(
        compiler_inputs,
        recipe_profile=replace(V1_PROFILE, provenance_schema=schema),
    )
    assert json.loads(result.provenance_map_bytes)["schema"] == schema


def test_graph_recipe_profile_field_controls_plan_identity(compiler_inputs) -> None:
    baseline = _compile(compiler_inputs)
    changed = _compile(
        compiler_inputs,
        recipe_profile=replace(
            V1_PROFILE,
            graph_recipe_profile_iri="https://example.test/profile/v2",
        ),
    )
    assert changed.plan.plan_digest != baseline.plan.plan_digest


def test_recipe_namespace_profile_field_selects_template_roots(
    compiler_inputs,
) -> None:
    namespace = "https://example.test/recipe/"
    recipes = RECIPES.replace(
        b"https://malleus.dev/paper-v4/recipe/",
        namespace.encode("utf-8"),
    )
    result = _compile(
        compiler_inputs,
        recipes=recipes,
        recipe_profile=replace(V1_PROFILE, recipe_namespace=namespace),
    )
    assert result.plan.operations


def test_member_namespace_profile_field_controls_member_identity(
    compiler_inputs,
) -> None:
    namespace = "https://example.test/member/"
    result = _compile(
        compiler_inputs,
        recipe_profile=replace(V1_PROFILE, member_namespace=namespace),
    )
    assert all(
        member.member.startswith(namespace)
        for member in result.plan.members
    )


def test_valid_multi_record_population_compiles_deterministically(
    compiler_inputs,
) -> None:
    first = _compile(compiler_inputs)
    second = _compile(compiler_inputs)

    assert first.plan == second.plan
    assert first.provenance_map_bytes == second.provenance_map_bytes
    assert len(first.plan.operations) == 3
    assert {item.record_id for item in first.plan.operations} == {
        "fiction:campaign",
        "fiction:system",
        "fiction:acquisition",
    }
    provenance = json.loads(first.provenance_map_bytes)
    assert provenance["schema"] == "malleus.paper-v4.population-provenance/v1"
    assert provenance["ontology_sha256"] == ONTOLOGY_DIGEST
    assert provenance["reading_sha256"] == READING_DIGEST
    assert provenance["plan_sha256"] == first.plan.plan_digest
    assert len(provenance["assertions"]) == 10
    compilation, contract = compiler_inputs
    del compilation
    members = {member.record_id: member.member for member in first.plan.members}
    operations = {operation.record_id: operation for operation in first.plan.operations}
    emission_ids = {
        emission_id
        for _, emissions in first.plan.member_emissions
        for emission_id, _ in emissions
    }
    observed = set()
    for assertion in provenance["assertions"]:
        record_id = assertion["record_id"]
        fact = assertion["emitted_fact"]
        assert assertion["emission_id"] in emission_ids
        assert assertion["block_id"] in BLOCKS
        assert fact["member"] == members[record_id]
        kind = assertion["assertion_kind"]
        if kind == "RECORD":
            assert fact["kind"] == "Record"
            assert fact["record_id"] == record_id
            key = (record_id, kind, None)
        elif kind == "PROPERTY":
            name = assertion["property"]
            assert fact["kind"] == "Property"
            assert fact["property"] == contract.symbol_bindings.property_iri(name)
            assert name in operations[record_id].properties
            key = (record_id, kind, name)
        else:
            role = kind.lower()
            assert fact["kind"] == "Relation" + role.title()
            assert fact["record_id"] == getattr(operations[record_id], role + "_id")
            assert fact["record_id"] == assertion["endpoint_record_id"]
            key = (record_id, kind, None)
        observed.add(key)
    expected = {
        (record["record_id"], "RECORD", None) for record in _population()["records"]
    }
    for record in _population()["records"]:
        expected.update(
            (record["record_id"], "PROPERTY", name) for name in record["properties"]
        )
        if "source" in record:
            expected.update(
                {
                    (record["record_id"], "SOURCE", None),
                    (record["record_id"], "TARGET", None),
                }
            )
    assert observed == expected
    assert _bytes(provenance) == first.provenance_map_bytes


def test_population_digests_bind_compiled_ontology_and_exact_reading(
    compiler_inputs,
) -> None:
    compilation, contract = compiler_inputs
    ontology_drift = _population()
    ontology_drift["ontology_sha256"] = "sha256:" + "c" * 64
    with pytest.raises(PopulationCompileRefusal) as ontology_mismatch:
        compile_population(
            _bytes(ontology_drift),
            compiled_ontology=compilation,
            logical_contract=contract,
            generic_recipe_bytes=RECIPES,
            selected_reading_bytes=READING,
            recipe_profile=V1_PROFILE,
        )
    assert _codes(ontology_mismatch.value) == {"POPULATION_DIGEST_MISMATCH"}

    reading_drift = _population()
    reading_drift["reading_sha256"] = "sha256:" + "d" * 64
    with pytest.raises(PopulationCompileRefusal) as reading_mismatch:
        _compile(compiler_inputs, reading_drift)
    assert _codes(reading_mismatch.value) == {"POPULATION_DIGEST_MISMATCH"}

    malformed_reading = (
        b'{"schema":"malleus.paper-v4.text-layer-reading/v1","blocks":[]}'
    )
    with pytest.raises(PopulationCompileRefusal) as malformed:
        _compile(compiler_inputs, reading=malformed_reading)
    assert _codes(malformed.value) == {"POPULATION_FIELDS_INVALID"}


@pytest.mark.parametrize(
    "location",
    ("record", "property", "endpoint"),
)
def test_every_population_locator_must_resolve(compiler_inputs, location) -> None:
    population = _population()
    records = population["records"]
    if location == "record":
        records[0]["record_block_id"] = "fiction:block:missing"
    elif location == "property":
        records[0]["properties"]["name"]["block_id"] = "fiction:block:missing"
    else:
        records[2]["source"]["block_id"] = "fiction:block:missing"

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(compiler_inputs, population)
    assert _codes(refusal.value) == {"POPULATION_LOCATOR_UNKNOWN"}


@pytest.mark.parametrize(
    ("mutation", "code"),
    (
        ("type", "POPULATION_RECORD_TYPE_UNMAPPED"),
        ("missing-property", "POPULATION_FIELDS_INVALID"),
        ("extra-property", "POPULATION_FIELDS_INVALID"),
    ),
)
def test_record_types_and_property_sets_are_closed(
    compiler_inputs, mutation, code
) -> None:
    population = _population()
    record = population["records"][0]
    if mutation == "type":
        record["record_type"] = "ImaginedType"
    elif mutation == "missing-property":
        del record["properties"]["name"]
    else:
        record["properties"]["invented"] = _located("not admitted")

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(compiler_inputs, population)
    assert code in _codes(refusal.value)


@pytest.mark.parametrize(
    ("mutation", "code"),
    (
        ("duplicate", "POPULATION_RECORD_ID_DUPLICATE"),
        ("dangling", "POPULATION_ENDPOINT_DANGLING"),
        ("wrong-direction", "POPULATION_ENDPOINT_TYPE_MISMATCH"),
        ("relation-endpoint", "POPULATION_ENDPOINT_NOT_ENTITY"),
    ),
)
def test_record_identity_and_relation_endpoints_are_closed(
    compiler_inputs,
    mutation,
    code,
) -> None:
    population = _population()
    records = population["records"]
    relation = records[2]
    if mutation == "duplicate":
        records[1]["record_id"] = records[0]["record_id"]
    elif mutation == "dangling":
        relation["target"]["record_id"] = "fiction:missing"
    elif mutation == "wrong-direction":
        relation["source"]["record_id"] = "fiction:system"
        relation["target"]["record_id"] = "fiction:campaign"
    else:
        relation["source"]["record_id"] = "fiction:acquisition"

    with pytest.raises(PopulationCompileRefusal) as refusal:
        _compile(compiler_inputs, population)
    assert code in _codes(refusal.value)


def _quantity() -> dict[str, object]:
    population = _population()
    population["records"] = [
        {
            "record_id": "fiction:quantity",
            "record_type": "BoundedQuantity",
            "record_block_id": "fiction:block:1",
            "properties": {
                "quantity_kind": _located("fictional measure"),
                "lower_value": _located(1.25),
                "upper_value": _located(2.75),
                "unit": _located("fictional unit"),
                "quantity_status": _located("REPORTED_OBSERVATION"),
            },
        }
    ]
    return population


def test_enum_scalar_finiteness_and_numeric_bounds_refuse(compiler_inputs) -> None:
    bad_enum = _quantity()
    bad_enum["records"][0]["properties"]["quantity_status"]["value"] = "IMAGINED"
    with pytest.raises(PopulationCompileRefusal) as enum_refusal:
        _compile(compiler_inputs, bad_enum)
    assert _codes(enum_refusal.value) == {"POPULATION_RECORD_INVALID"}

    bad_scalar = _quantity()
    bad_scalar["records"][0]["properties"]["lower_value"]["value"] = 10**1000
    with pytest.raises(PopulationCompileRefusal) as scalar_refusal:
        _compile(compiler_inputs, bad_scalar)
    assert _codes(scalar_refusal.value) == {"POPULATION_RECORD_INVALID"}

    below_minimum = _population()
    below_minimum["records"][2]["properties"]["instrument_count"]["value"] = -1
    with pytest.raises(PopulationCompileRefusal) as bound_refusal:
        _compile(compiler_inputs, below_minimum)
    assert _codes(bound_refusal.value) == {"POPULATION_RECORD_INVALID"}


def test_strict_json_and_recipe_or_assembly_failures_remain_typed(
    compiler_inputs,
) -> None:
    duplicate_key = _bytes(_population()).replace(
        b'"schema":"malleus.paper-v4.population/v1"',
        b'"schema":"malleus.paper-v4.population/v1","schema":"duplicate"',
    )
    compilation, contract = compiler_inputs
    with pytest.raises(PopulationCompileRefusal) as json_refusal:
        compile_population(
            duplicate_key,
            compiled_ontology=compilation,
            logical_contract=contract,
            generic_recipe_bytes=RECIPES,
            selected_reading_bytes=READING,
            recipe_profile=V1_PROFILE,
        )
    assert _codes(json_refusal.value) == {"POPULATION_JSON_INVALID"}

    with pytest.raises(PopulationCompileRefusal) as recipe_refusal:
        _compile(compiler_inputs, recipes=b"not stOTTR")
    assert "STOTTR_SYNTAX_ERROR" in _codes(recipe_refusal.value)

    broken = RECIPES.replace(
        b'  mgrp:Property(?member, malleus:relation_type, "DATA_ACQUISITION"),\n',
        b"",
        1,
    )
    assert broken != RECIPES
    with pytest.raises(PopulationCompileRefusal) as assembly_refusal:
        _compile(compiler_inputs, recipes=broken)
    assert "MEMBER_REQUIRED_PROPERTY_MISSING" in _codes(assembly_refusal.value)

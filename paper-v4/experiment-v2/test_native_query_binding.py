"""Guards for the type-only paper-v4 v2 native query binding."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import pytest

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry
from research.ontology_driven_kg_realization.experiments.document_paper.native_query import (
    NativeQueryRefusal,
    load_query_binding,
    run_frozen_queries,
    validate_query_binding,
    validate_query_binding_against_ontology,
)


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "paper-v4/experiment-v2/ontology-run"
BINDING = ROOT / "paper-v4/experiment-v2/native-query-binding.json"


def _registry() -> OntologyRegistry:
    return OntologyRegistry(
        RUN / "ontology-02.yaml",
        import_map={"malleus": str((RUN / "inputs/malleus.yaml").resolve())},
    )


def _binding() -> dict[str, Any]:
    return load_query_binding(BINDING.read_bytes())


def _commit(operation: Any) -> None:
    assert operation.op_status is OpStatus.COMMITTED, operation.rejection_reason


def _entity(
    graph: KnowledgeGraph,
    record_type: str,
    record_id: str,
    **properties: Any,
) -> None:
    _commit(graph.create_entity(record_type, record_id, properties))


def _relation(
    graph: KnowledgeGraph,
    record_type: str,
    record_id: str,
    source_id: str,
    target_id: str,
    relation_type: str,
) -> None:
    _commit(
        graph.create_relation(
            record_type,
            record_id,
            source_id,
            target_id,
            {"relation_type": relation_type},
        )
    )


def _fictional_graph() -> KnowledgeGraph:
    graph = KnowledgeGraph(_registry())

    _entity(
        graph,
        "ObservationMethod",
        "sentinel:method:a",
        name="fictional monitoring method alpha",
        observation_method_kind="PASSIVE_SEISMIC_MONITORING",
    )
    _entity(
        graph,
        "ObservationMethod",
        "sentinel:method:b",
        name="fictional calculation method beta",
        observation_method_kind="TRAVEL_TIME_CALCULATION",
    )
    _entity(
        graph,
        "Instrument",
        "sentinel:instrument:a",
        name="fictional sensor alpha",
        instrument_kind="SEISMOMETER",
    )
    _entity(
        graph,
        "Instrument",
        "sentinel:instrument:b",
        name="fictional sensor beta",
        instrument_kind="OCEAN_BOTTOM_SEISMOMETER",
    )
    _entity(
        graph,
        "GeologicFeature",
        "sentinel:feature:a",
        name="fictional cone alpha",
        geologic_feature_kind="VOLCANIC_CONE",
    )
    _entity(
        graph,
        "GeologicFeature",
        "sentinel:feature:b",
        name="fictional mound beta",
        geologic_feature_kind="HYDROTHERMAL_MOUND",
    )
    _entity(
        graph,
        "SeismicPhenomenon",
        "sentinel:seismic:a",
        name="fictional swarm alpha",
        seismic_phenomenon_kind="EARTHQUAKE_SWARM",
    )
    _entity(
        graph,
        "SeismicPhenomenon",
        "sentinel:seismic:b",
        name="fictional seismicity beta",
        seismic_phenomenon_kind="MICROSEISMICITY",
    )
    _entity(
        graph,
        "QuantitativeObservation",
        "sentinel:quantity:a",
        name="fictional temperature interval",
        quantity_kind="TEMPERATURE",
        lower_numeric_value=111.25,
        upper_numeric_value=222.75,
        measurement_unit="DEGREE_CELSIUS",
        observation_basis="MEASURED",
    )
    _entity(
        graph,
        "QuantitativeObservation",
        "sentinel:quantity:b",
        name="fictional thickness interval",
        quantity_kind="THICKNESS",
        lower_numeric_value=31.5,
        upper_numeric_value=47.75,
        measurement_unit="METER",
        observation_basis="MODELED",
    )
    _entity(
        graph,
        "GeologicMaterial",
        "sentinel:material",
        name="fictional sediment",
        geologic_material_kind="SEDIMENT",
    )
    _entity(
        graph,
        "ChemicalConstituent",
        "sentinel:constituent",
        name="fictional constituent",
        chemical_formula="Xy9",
    )
    for suffix, name, kind in (
        ("a", "fictional circulation", "HYDROTHERMAL_CIRCULATION"),
        ("b", "fictional cooling", "LITHOSPHERE_COOLING"),
        ("c", "fictional localization", "STRAIN_LOCALIZATION"),
    ):
        _entity(
            graph,
            "GeologicProcess",
            f"sentinel:process:{suffix}",
            name=name,
            geologic_process_kind=kind,
        )
    _entity(
        graph,
        "CategoricalObservation",
        "sentinel:category:a",
        name="fictional morphology state",
        categorical_observation_kind="MORPHOLOGY",
        categorical_observation_value="SMOOTH",
        observation_basis="OBSERVED",
    )
    _entity(
        graph,
        "CategoricalObservation",
        "sentinel:category:b",
        name="fictional thermal state",
        categorical_observation_kind="THERMAL_REGIME",
        categorical_observation_value="COLD",
        observation_basis="ESTIMATED",
    )

    _relation(
        graph,
        "MethodUsesInstrumentRelation",
        "sentinel:relation:method-instrument:a",
        "sentinel:method:a",
        "sentinel:instrument:a",
        "METHOD_USES_INSTRUMENT",
    )
    _relation(
        graph,
        "MethodUsesInstrumentRelation",
        "sentinel:relation:method-instrument:b",
        "sentinel:method:b",
        "sentinel:instrument:b",
        "METHOD_USES_INSTRUMENT",
    )
    _relation(
        graph,
        "SeismicPhenomenonOccursAtRelation",
        "sentinel:relation:seismic-feature:a",
        "sentinel:seismic:a",
        "sentinel:feature:a",
        "SEISMIC_PHENOMENON_OCCURS_AT",
    )
    _relation(
        graph,
        "SeismicPhenomenonOccursAtRelation",
        "sentinel:relation:seismic-feature:b",
        "sentinel:seismic:b",
        "sentinel:feature:b",
        "SEISMIC_PHENOMENON_OCCURS_AT",
    )
    _relation(
        graph,
        "FeaturePartOfRelation",
        "sentinel:relation:feature-part",
        "sentinel:feature:a",
        "sentinel:feature:b",
        "FEATURE_PART_OF",
    )
    _relation(
        graph,
        "ObservationCharacterizesRelation",
        "sentinel:relation:quantity-seismic",
        "sentinel:quantity:a",
        "sentinel:seismic:a",
        "OBSERVATION_CHARACTERIZES",
    )
    _relation(
        graph,
        "ObservationCharacterizesRelation",
        "sentinel:relation:quantity-material",
        "sentinel:quantity:b",
        "sentinel:material",
        "OBSERVATION_CHARACTERIZES",
    )
    _relation(
        graph,
        "ObservationConcernsConstituentRelation",
        "sentinel:relation:quantity-constituent",
        "sentinel:quantity:b",
        "sentinel:constituent",
        "OBSERVATION_CONCERNS_CONSTITUENT",
    )
    _relation(
        graph,
        "MaterialOccursAtRelation",
        "sentinel:relation:material-feature",
        "sentinel:material",
        "sentinel:feature:a",
        "MATERIAL_OCCURS_AT",
    )
    _relation(
        graph,
        "ProcessActsOnMaterialRelation",
        "sentinel:relation:process-material",
        "sentinel:process:a",
        "sentinel:material",
        "PROCESS_ACTS_ON_MATERIAL",
    )
    _relation(
        graph,
        "ProcessReleasesConstituentRelation",
        "sentinel:relation:process-constituent",
        "sentinel:process:a",
        "sentinel:constituent",
        "PROCESS_RELEASES_CONSTITUENT",
    )
    _relation(
        graph,
        "ProcessCausesProcessRelation",
        "sentinel:relation:process-process:a",
        "sentinel:process:a",
        "sentinel:process:b",
        "PROCESS_CAUSES_PROCESS",
    )
    _relation(
        graph,
        "ProcessCausesProcessRelation",
        "sentinel:relation:process-process:b",
        "sentinel:process:b",
        "sentinel:process:c",
        "PROCESS_CAUSES_PROCESS",
    )
    _relation(
        graph,
        "ProcessTriggersSeismicPhenomenonRelation",
        "sentinel:relation:process-seismic",
        "sentinel:process:c",
        "sentinel:seismic:a",
        "PROCESS_TRIGGERS_SEISMIC_PHENOMENON",
    )
    _relation(
        graph,
        "ObservationCharacterizesRelation",
        "sentinel:relation:category-process",
        "sentinel:category:a",
        "sentinel:process:a",
        "OBSERVATION_CHARACTERIZES",
    )
    _relation(
        graph,
        "ObservationCharacterizesRelation",
        "sentinel:relation:category-feature",
        "sentinel:category:b",
        "sentinel:feature:b",
        "OBSERVATION_CHARACTERIZES",
    )
    return graph


def _walk(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)
    else:
        yield value


def test_binding_is_frozen_to_types_and_conforms_to_v2_ontology() -> None:
    binding = _binding()
    assert validate_query_binding_against_ontology(binding, _registry()) is binding
    assert [len(query["cases"]) for query in binding["queries"]] == [1, 2, 4, 6]

    extra_join = deepcopy(binding)
    extra_join["queries"][1]["cases"][0]["join"] = {
        "to_case": 2,
        "on": "target_id",
    }
    with pytest.raises(NativeQueryRefusal, match="extra=.*join"):
        validate_query_binding(extra_join)

    reversed_endpoints = deepcopy(binding)
    first = reversed_endpoints["queries"][0]["cases"][0]
    first["source_record_type"], first["target_record_type"] = (
        first["target_record_type"],
        first["source_record_type"],
    )
    with pytest.raises(NativeQueryRefusal, match="outside source_id range"):
        validate_query_binding_against_ontology(reversed_endpoints, _registry())


def test_binding_contains_no_population_values_or_closure_assumptions() -> None:
    binding = json.loads(BINDING.read_bytes())
    forbidden_keys = {
        "allowed_record_ids",
        "answer",
        "block_id",
        "cardinality",
        "closure",
        "entity_count",
        "expected_row_count",
        "locator",
        "maximum_rows",
        "minimum_rows",
        "record_id",
        "relation_count",
        "source_phrase",
    }
    values = list(_walk(binding))
    assert forbidden_keys.isdisjoint(item for item in values if isinstance(item, str))

    forbidden_values = {
        "smarties",
        "rc2",
        "2019",
        "19",
        "17",
        "10",
        "20",
        "0.4",
        "3.0",
        "co2",
        "km",
        "wt%",
        "beneath the ridge axis",
        "ascending melt",
    }
    assert forbidden_values.isdisjoint(
        item.lower() for item in values if isinstance(item, str)
    )
    numbers = [item for item in values if type(item) in {int, float}]
    assert numbers == [1, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6]

    for query in binding["queries"]:
        for case in query["cases"]:
            for fields in case["output_fields"].values():
                assert {"id", "key", "source_id", "target_id"}.isdisjoint(fields)


def test_direct_cases_return_all_matching_fictional_rows_without_joins() -> None:
    results = run_frozen_queries(_fictional_graph(), _binding())
    by_id = {result["query_id"]: result for result in results}

    assert [row["case_ordinal"] for row in by_id["NQ-CQ-01"]["rows"]] == [1, 1]
    assert {
        row["target"]["name"] for row in by_id["NQ-CQ-01"]["rows"]
    } == {"fictional sensor alpha", "fictional sensor beta"}

    assert [row["case_ordinal"] for row in by_id["NQ-CQ-02"]["rows"]] == [1, 1, 2]
    assert [row["case_ordinal"] for row in by_id["NQ-CQ-03"]["rows"]] == [
        1,
        2,
        3,
        4,
    ]
    assert [row["case_ordinal"] for row in by_id["NQ-CQ-04"]["rows"]] == [
        1,
        2,
        3,
        3,
        4,
        5,
        6,
    ]
    causes = [
        row
        for row in by_id["NQ-CQ-04"]["rows"]
        if row["case_ordinal"] == 3
    ]
    assert [(row["source"]["name"], row["target"]["name"]) for row in causes] == [
        ("fictional circulation", "fictional cooling"),
        ("fictional cooling", "fictional localization"),
    ]

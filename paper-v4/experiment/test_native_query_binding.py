"""Hard guards for the type-only paper-v4 query binding."""

from __future__ import annotations

import builtins
from copy import deepcopy
from pathlib import Path
import socket
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
RUN = ROOT / "paper-v4/experiment/ontology-run"
BINDING = ROOT / "paper-v4/experiment/native-query-binding.json"


def _registry() -> OntologyRegistry:
    return OntologyRegistry(
        RUN / "ontology.yaml",
        import_map={"malleus": str((RUN / "inputs/malleus.yaml").resolve())},
    )


def _binding() -> dict[str, Any]:
    return load_query_binding(BINDING.read_bytes())


def _commit(operation: Any) -> None:
    assert operation.op_status is OpStatus.COMMITTED, operation.rejection_reason


class _ObservedGraph(KnowledgeGraph):
    def __init__(self, registry: OntologyRegistry) -> None:
        super().__init__(registry)
        self.query_reads: list[str] = []

    def query(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        raise AssertionError("type-bound queries must not scan graph nodes")

    def query_relations(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        self.query_reads.append("query_relations")
        return super().query_relations(*args, **kwargs)

    def get_node(self, *args: Any, **kwargs: Any) -> dict[str, Any] | None:
        self.query_reads.append("get_node")
        return super().get_node(*args, **kwargs)


def _graph(*, observed: bool = False, first_count: int = 17) -> KnowledgeGraph:
    graph_type = _ObservedGraph if observed else KnowledgeGraph
    graph = graph_type(_registry())

    for suffix, campaign, system, count in (
        ("a", "Fictional Voyage Alpha", "Fictional Array Alpha", first_count),
        ("b", "Fictional Voyage Beta", "Fictional Array Beta", 23),
    ):
        _commit(
            graph.create_entity(
                "Campaign", f"sentinel:campaign:{suffix}", {"name": campaign}
            )
        )
        _commit(
            graph.create_entity(
                "ObservingSystem",
                f"sentinel:system:{suffix}",
                {"instrument_kind": "fictional gauge", "name": system},
            )
        )
        _commit(
            graph.create_relation(
                "DataAcquisitionRelation",
                f"sentinel:acquisition:{suffix}",
                f"sentinel:campaign:{suffix}",
                f"sentinel:system:{suffix}",
                {
                    "data_kind": "fictional waveform",
                    "instrument_count": count,
                    "relation_type": "DATA_ACQUISITION",
                },
            )
        )

    _commit(graph.create_entity("Region", "sentinel:region", {"name": "Zone Q"}))
    _commit(
        graph.create_entity(
            "EarthquakePopulation",
            "sentinel:earthquakes",
            {"name": "fictional tremor cohort"},
        )
    )
    _commit(
        graph.create_entity(
            "PrimaryMeltPopulation",
            "sentinel:melt",
            {"name": "fictional melt cohort"},
        )
    )
    _commit(
        graph.create_relation(
            "SpatialAssociationRelation",
            "sentinel:spatial:earthquakes",
            "sentinel:earthquakes",
            "sentinel:region",
            {
                "relation_type": "SPATIAL_ASSOCIATION",
                "relative_position": "below a fictional line",
            },
        )
    )
    _commit(
        graph.create_relation(
            "SpatialAssociationRelation",
            "sentinel:spatial:system",
            "sentinel:system:a",
            "sentinel:region",
            {
                "relation_type": "SPATIAL_ASSOCIATION",
                "relative_position": "outside the question pattern",
            },
        )
    )

    for suffix, lower, upper, status, target in (
        ("depth", 11.5, 19.25, "REPORTED_OBSERVATION", "sentinel:earthquakes"),
        ("composition", 0.4, 2.6, "CALCULATED_ESTIMATE", "sentinel:melt"),
    ):
        quantity_id = f"sentinel:quantity:{suffix}"
        _commit(
            graph.create_entity(
                "BoundedQuantity",
                quantity_id,
                {
                    "lower_value": lower,
                    "quantity_kind": f"fictional {suffix}",
                    "quantity_status": status,
                    "unit": f"fictional-unit-{suffix}",
                    "upper_value": upper,
                },
            )
        )
        _commit(
            graph.create_relation(
                "QuantityCharacterizationRelation",
                f"sentinel:characterization:{suffix}",
                quantity_id,
                target,
                {"relation_type": "QUANTITY_CHARACTERIZATION"},
            )
        )

    _commit(
        graph.create_entity(
            "MechanismHypothesis",
            "sentinel:hypothesis",
            {
                "hypothesis_status": "PREFERRED",
                "initiating_condition": "fictional initial state",
                "outcome": "fictional outcome",
                "physical_effect": "fictional physical effect",
                "stress_context": "fictional stress context",
                "transformation": "fictional transformation",
            },
        )
    )
    _commit(
        graph.create_relation(
            "HypothesisExplainsRelation",
            "sentinel:explanation",
            "sentinel:hypothesis",
            "sentinel:earthquakes",
            {"relation_type": "EXPLAINS"},
        )
    )
    return graph


def test_binding_is_closed_and_conforms_to_the_selected_ontology() -> None:
    binding = _binding()
    assert validate_query_binding_against_ontology(binding, _registry()) is binding

    extra_filter = deepcopy(binding)
    extra_filter["queries"][0]["cases"][0]["cardinality"] = 1
    with pytest.raises(NativeQueryRefusal, match="extra=.*cardinality"):
        validate_query_binding(extra_filter)

    unknown_type = deepcopy(binding)
    unknown_type["queries"][0]["cases"][0]["source_record_type"] = "Unknown"
    with pytest.raises(NativeQueryRefusal, match="unknown record type"):
        validate_query_binding_against_ontology(unknown_type, _registry())

    reversed_endpoints = deepcopy(binding)
    first = reversed_endpoints["queries"][0]["cases"][0]
    first["source_record_type"], first["target_record_type"] = (
        first["target_record_type"],
        first["source_record_type"],
    )
    with pytest.raises(NativeQueryRefusal, match="outside source_id range"):
        validate_query_binding_against_ontology(reversed_endpoints, _registry())

    wrong_enum = deepcopy(binding)
    wrong_enum["queries"][0]["cases"][0]["relation_type"]["enum"] = (
        "QuantityStatus"
    )
    with pytest.raises(NativeQueryRefusal, match="enum does not match"):
        validate_query_binding_against_ontology(wrong_enum, _registry())

    wrong_value = deepcopy(binding)
    wrong_value["queries"][0]["cases"][0]["relation_type"]["value"] = "EXPLAINS"
    with pytest.raises(NativeQueryRefusal, match="value does not match"):
        validate_query_binding_against_ontology(wrong_value, _registry())

    unknown_output = deepcopy(binding)
    unknown_output["queries"][0]["cases"][0]["output_fields"]["source"] = [
        "answer"
    ]
    with pytest.raises(NativeQueryRefusal, match="unknown source output"):
        validate_query_binding_against_ontology(unknown_output, _registry())


def test_queries_return_every_matching_row_and_only_graph_values() -> None:
    results = run_frozen_queries(_graph(first_count=41), _binding())
    by_id = {result["query_id"]: result for result in results}

    acquisitions = by_id["NQ-CQ-01"]["rows"]
    assert len(acquisitions) == 2
    assert [row["relation"]["instrument_count"] for row in acquisitions] == [41, 23]
    assert [row["source"]["name"] for row in acquisitions] == [
        "Fictional Voyage Alpha",
        "Fictional Voyage Beta",
    ]

    spatial = by_id["NQ-CQ-02"]["rows"]
    assert len(spatial) == 1
    assert spatial[0]["relation"]["relative_position"] == "below a fictional line"

    quantities = by_id["NQ-CQ-03"]["rows"]
    assert [row["case_ordinal"] for row in quantities] == [1, 2]
    assert [row["source"]["lower_value"] for row in quantities] == [11.5, 0.4]

    hypotheses = by_id["NQ-CQ-04"]["rows"]
    assert len(hypotheses) == 1
    assert hypotheses[0]["source"]["outcome"] == "fictional outcome"


def test_query_execution_isolated_to_graph_and_loaded_binding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    graph = _graph(observed=True)
    binding = _binding()

    def blocked(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("query execution attempted forbidden external access")

    monkeypatch.setattr(builtins, "open", blocked)
    monkeypatch.setattr(Path, "open", blocked)
    monkeypatch.setattr(socket, "socket", blocked)

    results = run_frozen_queries(graph, binding)
    assert [result["query_id"] for result in results] == [
        "NQ-CQ-01",
        "NQ-CQ-02",
        "NQ-CQ-03",
        "NQ-CQ-04",
    ]
    assert set(graph.query_reads) == {"query_relations", "get_node"}

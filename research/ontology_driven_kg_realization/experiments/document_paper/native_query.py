"""Frozen native queries for the paper-v4 recovery control.

The executor reads one already materialized ``KnowledgeGraph`` through its
public query surface. It performs no file, network, source-text, oracle, or
embedding access.
"""

from __future__ import annotations

from collections import Counter
import math
from typing import Any, Callable, Mapping

from malleus.kg import KnowledgeGraph


QUERY_IDS = ("NQ-CQ-01", "NQ-CQ-02", "NQ-CQ-03", "NQ-CQ-04")
QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")

NODE_CARDINALITIES = (
    ("ObservationNetwork", 1),
    ("Campaign", 1),
    ("RidgeSection", 1),
    ("EarthquakePopulation", 1),
    ("MeltPopulation", 1),
    ("QuantitativeRange", 2),
    ("CausalHypothesis", 1),
    ("MechanismElement", 7),
)
RELATION_CARDINALITIES = (
    ("DataAcquisitionRelation", 1),
    ("SpatialAssociationRelation", 2),
    ("QuantitySubjectRelation", 2),
    ("HypothesisComponentRelation", 7),
    ("CausalLinkRelation", 7),
    ("HypothesisTargetRelation", 1),
)

CAUSAL_KIND_EDGES = frozenset(
    {
        ("ASCENDING_MELT", "CARBON_DIOXIDE_DEGASSING"),
        ("CARBON_DIOXIDE_DEGASSING", "VOLUME_CHANGE"),
        ("CARBON_DIOXIDE_DEGASSING", "PRESSURE_INCREASE"),
        ("VOLUME_CHANGE", "LOCAL_HIGH_STRAIN_RATE"),
        ("EXTENSIONAL_STRESS", "LOCAL_HIGH_STRAIN_RATE"),
        ("PRESSURE_INCREASE", "EARTHQUAKE_TRIGGERING"),
        ("LOCAL_HIGH_STRAIN_RATE", "EARTHQUAKE_TRIGGERING"),
    }
)

_MECHANISM_LABELS = {
    "ASCENDING_MELT": "ascending melt",
    "CARBON_DIOXIDE_DEGASSING": "CO2 degassing",
    "VOLUME_CHANGE": "volume change",
    "PRESSURE_INCREASE": "pressure increase",
    "EXTENSIONAL_STRESS": "extensional stress",
    "LOCAL_HIGH_STRAIN_RATE": "locally high strain rates",
    "EARTHQUAKE_TRIGGERING": "earthquake triggering",
}
_STATUS_LABELS = {
    "REPORTED_OBSERVATION": "reported observation",
    "CALCULATED_ESTIMATE": "calculated estimate",
    "PREFERRED_HYPOTHESIS": "authors' preferred hypothesis",
}
_UNIT_LABELS = {
    "KILOMETER": "km",
    "WEIGHT_PERCENT": "wt%",
}
_POSITION_LABELS = {
    "BENEATH_RIDGE_AXIS": "beneath the ridge axis",
    "ALONG_RIDGE_SECTION": "along the ridge section",
}


class NativeQueryRefusal(ValueError):
    """A frozen query could not produce one unambiguous result."""

    def __init__(self, query_id: str, detail: str) -> None:
        self.query_id = query_id
        self.detail = detail
        super().__init__(f"{query_id}: {detail}")


def _refuse(query_id: str, detail: str) -> None:
    raise NativeQueryRefusal(query_id, detail)


def _required(record: Mapping[str, Any], field: str, query_id: str) -> Any:
    if field not in record:
        _refuse(query_id, f"required field {field!r} is absent")
    return record[field]


def _text(record: Mapping[str, Any], field: str, query_id: str) -> str:
    value = _required(record, field, query_id)
    if not isinstance(value, str) or not value.strip():
        _refuse(query_id, f"required field {field!r} must be a nonblank string")
    return value


def _integer(record: Mapping[str, Any], field: str, query_id: str) -> int:
    value = _required(record, field, query_id)
    if type(value) is not int:
        _refuse(query_id, f"required field {field!r} must be an integer")
    return value


def _number(record: Mapping[str, Any], field: str, query_id: str) -> float:
    value = _required(record, field, query_id)
    if type(value) not in {int, float} or not math.isfinite(value):
        _refuse(query_id, f"required field {field!r} must be a finite number")
    return float(value)


def _equals(
    record: Mapping[str, Any],
    field: str,
    expected: str,
    query_id: str,
) -> None:
    observed = _text(record, field, query_id)
    if observed != expected:
        _refuse(
            query_id,
            f"field {field!r} must equal {expected!r}, observed {observed!r}",
        )


def _label(labels: Mapping[str, str], value: Any, field: str, query_id: str) -> str:
    if not isinstance(value, str):
        _refuse(query_id, f"required field {field!r} must be a string")
    if value not in labels:
        _refuse(query_id, f"field {field!r} has no frozen lexical form: {value!r}")
    return labels[value]


def _only(records: list[dict[str, Any]], subject: str, query_id: str) -> dict[str, Any]:
    if len(records) != 1:
        _refuse(query_id, f"{subject} cardinality must be 1, observed {len(records)}")
    return records[0]


def _entities(
    graph: KnowledgeGraph,
    record_type: str,
    query_id: str,
) -> list[dict[str, Any]]:
    records = graph.query(entity_type=record_type)
    exact = [
        record for record in records if _text(record, "type", query_id) == record_type
    ]
    return sorted(exact, key=lambda record: _text(record, "id", query_id))


def _relations(
    graph: KnowledgeGraph,
    record_type: str,
    query_id: str,
) -> list[dict[str, Any]]:
    records = graph.query_relations(relation_type=record_type)
    return sorted(records, key=lambda record: _text(record, "key", query_id))


def _node(
    graph: KnowledgeGraph,
    record_id: str,
    record_type: str,
    query_id: str,
) -> dict[str, Any]:
    record = graph.get_node(record_id)
    if record is None:
        _refuse(query_id, f"endpoint {record_id!r} does not resolve to a node")
    observed = _text(record, "type", query_id)
    if observed != record_type:
        _refuse(
            query_id,
            f"endpoint {record_id!r} must be {record_type}, observed {observed}",
        )
    return record


def _witness(
    entities: list[Mapping[str, Any]],
    relations: list[Mapping[str, Any]],
    query_id: str,
) -> dict[str, list[str]]:
    return {
        "entity_ids": sorted(_text(item, "id", query_id) for item in entities),
        "relation_ids": sorted(_text(item, "key", query_id) for item in relations),
    }


def _result(
    query_id: str,
    answer: dict[str, Any],
    semantics: dict[str, Any],
    entities: list[Mapping[str, Any]],
    relations: list[Mapping[str, Any]],
) -> dict[str, Any]:
    position = QUERY_IDS.index(query_id)
    return {
        "answer": answer,
        "query_id": query_id,
        "question_id": QUESTION_IDS[position],
        "raw_semantics": semantics,
        "witness": _witness(entities, relations, query_id),
    }


def _require_graph_closure(graph: KnowledgeGraph) -> None:
    query_id = "NQ-GRAPH-CLOSURE"
    nodes = graph.query()
    relations = graph.query_relations()
    node_counts = Counter(_text(item, "type", query_id) for item in nodes)
    relation_counts = Counter(_text(item, "type", query_id) for item in relations)
    expected_nodes = Counter(dict(NODE_CARDINALITIES))
    expected_relations = Counter(dict(RELATION_CARDINALITIES))
    if node_counts != expected_nodes:
        _refuse(
            query_id,
            f"node type cardinalities differ: expected={dict(expected_nodes)}, "
            f"observed={dict(node_counts)}",
        )
    if relation_counts != expected_relations:
        _refuse(
            query_id,
            f"relation type cardinalities differ: expected={dict(expected_relations)}, "
            f"observed={dict(relation_counts)}",
        )
    for record in nodes:
        _text(record, "id", query_id)
    for record in relations:
        _text(record, "key", query_id)


def _query_cq_01(graph: KnowledgeGraph) -> dict[str, Any]:
    query_id = "NQ-CQ-01"
    relation = _only(
        _relations(graph, "DataAcquisitionRelation", query_id),
        "data-acquisition relation",
        query_id,
    )
    _equals(relation, "relation_type", "ACQUIRED_DURING", query_id)
    _equals(relation, "data_kind", "MICROSEISMICITY", query_id)
    _equals(relation, "epistemic_status", "REPORTED_OBSERVATION", query_id)
    network = _node(
        graph,
        _text(relation, "source_id", query_id),
        "ObservationNetwork",
        query_id,
    )
    campaign = _node(
        graph,
        _text(relation, "target_id", query_id),
        "Campaign",
        query_id,
    )
    answer = {
        "observing_system": _text(network, "name", query_id),
        "campaign": _text(campaign, "name", query_id),
        "campaign_year": _integer(campaign, "campaign_year", query_id),
        "deployed_instrument_count": _integer(
            network, "deployed_instrument_count", query_id
        ),
        "usable_instrument_count": _integer(
            network, "usable_instrument_count", query_id
        ),
    }
    semantics = {
        **answer,
        "data_acquisition": {
            "data_kind": _text(relation, "data_kind", query_id),
            "epistemic_status": _text(relation, "epistemic_status", query_id),
            "relation_type": _text(relation, "relation_type", query_id),
        },
    }
    return _result(query_id, answer, semantics, [network, campaign], [relation])


def _spatial_relation_for(
    graph: KnowledgeGraph,
    source_id: str,
    query_id: str,
) -> dict[str, Any]:
    relations = [
        relation
        for relation in _relations(graph, "SpatialAssociationRelation", query_id)
        if _text(relation, "source_id", query_id) == source_id
    ]
    relation = _only(relations, f"spatial relation from {source_id!r}", query_id)
    _equals(relation, "relation_type", "SPATIALLY_ASSOCIATED_WITH", query_id)
    _equals(relation, "epistemic_status", "REPORTED_OBSERVATION", query_id)
    return relation


def _query_cq_02(graph: KnowledgeGraph) -> dict[str, Any]:
    query_id = "NQ-CQ-02"
    population = _only(
        _entities(graph, "EarthquakePopulation", query_id),
        "earthquake population",
        query_id,
    )
    relation = _spatial_relation_for(graph, _text(population, "id", query_id), query_id)
    ridge = _node(
        graph,
        _text(relation, "target_id", query_id),
        "RidgeSection",
        query_id,
    )
    answer = {
        "ridge_subsection": _text(ridge, "name", query_id),
        "event_population": _text(population, "name", query_id),
        "spatial_relation": _label(
            _POSITION_LABELS,
            _required(relation, "relative_position", query_id),
            "relative_position",
            query_id,
        ),
    }
    semantics = {
        "epistemic_status": _text(relation, "epistemic_status", query_id),
        "event_population": _text(population, "name", query_id),
        "relative_position": _text(relation, "relative_position", query_id),
        "ridge_subsection": _text(ridge, "name", query_id),
    }
    return _result(
        query_id,
        answer,
        semantics,
        [population, ridge],
        [relation],
    )


def _ranges_by_kind(
    graph: KnowledgeGraph,
    query_id: str,
) -> dict[str, dict[str, Any]]:
    ranges = _entities(graph, "QuantitativeRange", query_id)
    by_kind: dict[str, dict[str, Any]] = {}
    for record in ranges:
        kind = _text(record, "quantity_kind", query_id)
        if kind in by_kind:
            _refuse(query_id, f"quantity kind {kind!r} is duplicated")
        by_kind[kind] = record
    expected = {"EARTHQUAKE_DEPTH", "PRIMARY_MELT_CO2_CONCENTRATION"}
    if set(by_kind) != expected:
        _refuse(
            query_id,
            f"quantity kinds differ: expected={sorted(expected)}, "
            f"observed={sorted(by_kind)}",
        )
    return by_kind


def _quantity_relation_for(
    graph: KnowledgeGraph,
    target_id: str,
    query_id: str,
) -> dict[str, Any]:
    relations = [
        relation
        for relation in _relations(graph, "QuantitySubjectRelation", query_id)
        if _text(relation, "target_id", query_id) == target_id
    ]
    relation = _only(relations, f"quantity relation to {target_id!r}", query_id)
    _equals(relation, "relation_type", "HAS_QUANTITY", query_id)
    return relation


def _range_answer(record: Mapping[str, Any], query_id: str) -> dict[str, Any]:
    return {
        "lower": _number(record, "lower_bound", query_id),
        "upper": _number(record, "upper_bound", query_id),
        "unit": _label(
            _UNIT_LABELS,
            _required(record, "unit", query_id),
            "unit",
            query_id,
        ),
        "status": _label(
            _STATUS_LABELS,
            _required(record, "epistemic_status", query_id),
            "epistemic_status",
            query_id,
        ),
    }


def _query_cq_03(graph: KnowledgeGraph) -> dict[str, Any]:
    query_id = "NQ-CQ-03"
    ranges = _ranges_by_kind(graph, query_id)
    depth = ranges["EARTHQUAKE_DEPTH"]
    co2 = ranges["PRIMARY_MELT_CO2_CONCENTRATION"]
    depth_relation = _quantity_relation_for(
        graph, _text(depth, "id", query_id), query_id
    )
    co2_relation = _quantity_relation_for(graph, _text(co2, "id", query_id), query_id)
    earthquake = _node(
        graph,
        _text(depth_relation, "source_id", query_id),
        "EarthquakePopulation",
        query_id,
    )
    melt = _node(
        graph,
        _text(co2_relation, "source_id", query_id),
        "MeltPopulation",
        query_id,
    )
    earthquake_spatial = _spatial_relation_for(
        graph, _text(earthquake, "id", query_id), query_id
    )
    melt_spatial = _spatial_relation_for(graph, _text(melt, "id", query_id), query_id)
    _equals(
        earthquake_spatial,
        "relative_position",
        "BENEATH_RIDGE_AXIS",
        query_id,
    )
    _equals(
        melt_spatial,
        "relative_position",
        "ALONG_RIDGE_SECTION",
        query_id,
    )
    earthquake_ridge = _text(earthquake_spatial, "target_id", query_id)
    melt_ridge = _text(melt_spatial, "target_id", query_id)
    if earthquake_ridge != melt_ridge:
        _refuse(query_id, "quantity subjects do not share one ridge section")
    ridge = _node(graph, earthquake_ridge, "RidgeSection", query_id)
    answer = {
        "earthquake_depth": _range_answer(depth, query_id),
        "primary_melt_co2": _range_answer(co2, query_id),
    }
    semantics = {
        "earthquake_depth": {
            "epistemic_status": _text(depth, "epistemic_status", query_id),
            "lower": _number(depth, "lower_bound", query_id),
            "quantity_kind": _text(depth, "quantity_kind", query_id),
            "subject_id": _text(earthquake, "id", query_id),
            "unit": _text(depth, "unit", query_id),
            "upper": _number(depth, "upper_bound", query_id),
        },
        "primary_melt_co2": {
            "epistemic_status": _text(co2, "epistemic_status", query_id),
            "lower": _number(co2, "lower_bound", query_id),
            "quantity_kind": _text(co2, "quantity_kind", query_id),
            "subject_id": _text(melt, "id", query_id),
            "unit": _text(co2, "unit", query_id),
            "upper": _number(co2, "upper_bound", query_id),
        },
        "shared_ridge_id": _text(ridge, "id", query_id),
    }
    return _result(
        query_id,
        answer,
        semantics,
        [earthquake, melt, ridge, depth, co2],
        [depth_relation, co2_relation, earthquake_spatial, melt_spatial],
    )


def _mechanisms_by_kind(
    graph: KnowledgeGraph,
    hypothesis: Mapping[str, Any],
    query_id: str,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    hypothesis_id = _text(hypothesis, "id", query_id)
    components = _relations(graph, "HypothesisComponentRelation", query_id)
    mechanisms = _entities(graph, "MechanismElement", query_id)
    for relation in components:
        _equals(relation, "relation_type", "HAS_COMPONENT", query_id)
        _equals(relation, "source_id", hypothesis_id, query_id)
    component_targets = {
        _text(relation, "target_id", query_id) for relation in components
    }
    mechanism_ids = {_text(item, "id", query_id) for item in mechanisms}
    if len(component_targets) != 7 or component_targets != mechanism_ids:
        _refuse(query_id, "hypothesis components do not equal seven mechanisms")
    by_kind: dict[str, dict[str, Any]] = {}
    for mechanism in mechanisms:
        kind = _text(mechanism, "mechanism_kind", query_id)
        if kind in by_kind:
            _refuse(query_id, f"mechanism kind {kind!r} is duplicated")
        by_kind[kind] = mechanism
    if set(by_kind) != set(_MECHANISM_LABELS):
        _refuse(
            query_id,
            f"mechanism kinds differ: expected={sorted(_MECHANISM_LABELS)}, "
            f"observed={sorted(by_kind)}",
        )
    return by_kind, components


def _causal_relations(
    graph: KnowledgeGraph,
    mechanisms: Mapping[str, Mapping[str, Any]],
    query_id: str,
) -> tuple[list[dict[str, Any]], tuple[tuple[str, str], ...]]:
    by_id = {_text(record, "id", query_id): kind for kind, record in mechanisms.items()}
    relations = _relations(graph, "CausalLinkRelation", query_id)
    observed_edges: list[tuple[str, str]] = []
    for relation in relations:
        _equals(relation, "relation_type", "CAUSES", query_id)
        _equals(relation, "epistemic_status", "PREFERRED_HYPOTHESIS", query_id)
        source_id = _text(relation, "source_id", query_id)
        target_id = _text(relation, "target_id", query_id)
        if source_id not in by_id or target_id not in by_id:
            _refuse(query_id, "causal link endpoint is outside hypothesis components")
        observed_edges.append((by_id[source_id], by_id[target_id]))
    if len(set(observed_edges)) != len(observed_edges):
        _refuse(query_id, "causal kind edge is duplicated")
    if set(observed_edges) != CAUSAL_KIND_EDGES:
        _refuse(
            query_id,
            f"causal topology differs: expected={sorted(CAUSAL_KIND_EDGES)}, "
            f"observed={sorted(observed_edges)}",
        )
    return relations, tuple(sorted(observed_edges))


def _query_cq_04(graph: KnowledgeGraph) -> dict[str, Any]:
    query_id = "NQ-CQ-04"
    hypothesis = _only(
        _entities(graph, "CausalHypothesis", query_id),
        "causal hypothesis",
        query_id,
    )
    _equals(hypothesis, "epistemic_status", "PREFERRED_HYPOTHESIS", query_id)
    mechanisms, components = _mechanisms_by_kind(graph, hypothesis, query_id)
    causal, causal_edges = _causal_relations(graph, mechanisms, query_id)

    target = _only(
        _relations(graph, "HypothesisTargetRelation", query_id),
        "hypothesis target relation",
        query_id,
    )
    _equals(target, "relation_type", "EXPLAINS", query_id)
    _equals(target, "source_id", _text(hypothesis, "id", query_id), query_id)
    earthquake = _node(
        graph,
        _text(target, "target_id", query_id),
        "EarthquakePopulation",
        query_id,
    )
    spatial = _spatial_relation_for(graph, _text(earthquake, "id", query_id), query_id)
    _equals(spatial, "relative_position", "BENEATH_RIDGE_AXIS", query_id)
    ridge = _node(
        graph,
        _text(spatial, "target_id", query_id),
        "RidgeSection",
        query_id,
    )

    labels = {
        kind: _label(_MECHANISM_LABELS, kind, "mechanism_kind", query_id)
        for kind in mechanisms
    }
    answer = {
        "epistemic_status": _label(
            _STATUS_LABELS,
            _required(hypothesis, "epistemic_status", query_id),
            "epistemic_status",
            query_id,
        ),
        "source_process": (
            f"{labels['CARBON_DIOXIDE_DEGASSING']} from {labels['ASCENDING_MELT']}"
        ),
        "intermediate_processes": [
            labels["VOLUME_CHANGE"],
            f"{labels['PRESSURE_INCREASE']} under {labels['EXTENSIONAL_STRESS']}",
            labels["LOCAL_HIGH_STRAIN_RATE"],
        ],
        "outcome": (
            "triggered deep mantle earthquakes beneath the "
            f"{_text(ridge, 'name', query_id)} ridge axis"
        ),
    }
    semantics = {
        "causal_edges": [list(edge) for edge in causal_edges],
        "epistemic_status": _text(hypothesis, "epistemic_status", query_id),
        "mechanism_kinds": sorted(mechanisms),
        "target": {
            "population_name": _text(earthquake, "name", query_id),
            "population_type": _text(earthquake, "type", query_id),
            "relative_position": _text(spatial, "relative_position", query_id),
            "ridge_name": _text(ridge, "name", query_id),
        },
    }
    entities = [hypothesis, earthquake, ridge, *mechanisms.values()]
    relations = [*components, *causal, target, spatial]
    return _result(query_id, answer, semantics, entities, relations)


_QUERY_RUNNERS: Mapping[str, Callable[[KnowledgeGraph], dict[str, Any]]] = {
    "NQ-CQ-01": _query_cq_01,
    "NQ-CQ-02": _query_cq_02,
    "NQ-CQ-03": _query_cq_03,
    "NQ-CQ-04": _query_cq_04,
}


def run_native_query(graph: KnowledgeGraph, query_id: str) -> dict[str, Any]:
    """Run one frozen query after checking the complete graph closure."""

    if type(graph) is not KnowledgeGraph:
        raise TypeError("graph must be one exact KnowledgeGraph")
    if query_id not in _QUERY_RUNNERS:
        _refuse("NQ-DISPATCH", f"unknown query id {query_id!r}")
    _require_graph_closure(graph)
    return _QUERY_RUNNERS[query_id](graph)


def run_frozen_queries(graph: KnowledgeGraph) -> tuple[dict[str, Any], ...]:
    """Run the four frozen queries in competency-question order."""

    if type(graph) is not KnowledgeGraph:
        raise TypeError("graph must be one exact KnowledgeGraph")
    _require_graph_closure(graph)
    return tuple(_QUERY_RUNNERS[query_id](graph) for query_id in QUERY_IDS)

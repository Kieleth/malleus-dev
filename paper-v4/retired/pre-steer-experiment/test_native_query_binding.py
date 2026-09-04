"""Hard guards for the prepopulation native-query freeze."""

from __future__ import annotations

import ast
import builtins
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import pytest

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ontology import OntologyRegistry
from research.ontology_driven_kg_realization.experiments.document_paper import (
    native_query,
)
from research.ontology_driven_kg_realization.experiments.document_paper.native_query import (
    NativeQueryRefusal,
    run_frozen_queries,
    run_native_query,
)


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4/experiment"
PRIVATE = ROOT / "private/paper-v4-evaluation"
BINDING = EXPERIMENT / "native-query-binding.json"
EXECUTOR = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/document_paper/native_query.py"
)

SYNTHETIC_CAUSAL_EDGES = (
    ("ASCENDING_MELT", "CARBON_DIOXIDE_DEGASSING"),
    ("CARBON_DIOXIDE_DEGASSING", "PRESSURE_INCREASE"),
    ("CARBON_DIOXIDE_DEGASSING", "VOLUME_CHANGE"),
    ("EXTENSIONAL_STRESS", "LOCAL_HIGH_STRAIN_RATE"),
    ("LOCAL_HIGH_STRAIN_RATE", "EARTHQUAKE_TRIGGERING"),
    ("PRESSURE_INCREASE", "EARTHQUAKE_TRIGGERING"),
    ("VOLUME_CHANGE", "LOCAL_HIGH_STRAIN_RATE"),
)


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_bytes())
    assert type(loaded) is dict
    return loaded


def _commit(operation: Any) -> None:
    assert operation.op_status is OpStatus.COMMITTED, operation.rejection_reason


def _synthetic_graph(
    *,
    network_name: str = "FICTIONAL SENTINEL OBS ARRAY",
    campaign_name: str = "FICTIONAL SENTINEL VOYAGE",
    campaign_year: int = 2042,
    deployed_count: int = 31,
    usable_count: int = 29,
    ridge_name: str = "ZX-9",
    event_name: str = "fictional abyssal tremor cohort",
    depth_bounds: tuple[float, float] = (12.5, 18.75),
    co2_bounds: tuple[float, float] = (0.6, 2.4),
    depth_unit: str = "KILOMETER",
    depth_status: str = "REPORTED_OBSERVATION",
    co2_unit: str = "WEIGHT_PERCENT",
    co2_status: str = "CALCULATED_ESTIMATE",
    event_position: str = "BENEATH_RIDGE_AXIS",
    melt_position: str = "ALONG_RIDGE_SECTION",
    causal_edges: tuple[tuple[str, str], ...] = SYNTHETIC_CAUSAL_EDGES,
    extra_network: bool = False,
    omit_acquisition: bool = False,
) -> KnowledgeGraph:
    registry = OntologyRegistry(
        EXPERIMENT / "controlled-ontology-recovery.yaml",
        import_map={"malleus": str(ROOT / "ontology/malleus.yaml")},
    )
    graph = KnowledgeGraph(registry)
    _commit(
        graph.create_entity(
            "ObservationNetwork",
            "sentinel:network",
            {
                "name": network_name,
                "deployed_instrument_count": deployed_count,
                "usable_instrument_count": usable_count,
            },
        )
    )
    if extra_network:
        _commit(
            graph.create_entity(
                "ObservationNetwork",
                "sentinel:network:extra",
                {
                    "name": "FICTIONAL EXTRA ARRAY",
                    "deployed_instrument_count": 7,
                    "usable_instrument_count": 5,
                },
            )
        )
    _commit(
        graph.create_entity(
            "Campaign",
            "sentinel:campaign",
            {"name": campaign_name, "campaign_year": campaign_year},
        )
    )
    _commit(
        graph.create_entity(
            "RidgeSection",
            "sentinel:ridge",
            {"name": ridge_name},
        )
    )
    _commit(
        graph.create_entity(
            "EarthquakePopulation",
            "sentinel:events",
            {"name": event_name},
        )
    )
    _commit(
        graph.create_entity(
            "MeltPopulation",
            "sentinel:melt",
            {"name": "fictional primary melt cohort"},
        )
    )
    _commit(
        graph.create_entity(
            "QuantitativeRange",
            "sentinel:range:depth",
            {
                "quantity_kind": "EARTHQUAKE_DEPTH",
                "lower_bound": depth_bounds[0],
                "upper_bound": depth_bounds[1],
                "unit": depth_unit,
                "epistemic_status": depth_status,
            },
        )
    )
    _commit(
        graph.create_entity(
            "QuantitativeRange",
            "sentinel:range:co2",
            {
                "quantity_kind": "PRIMARY_MELT_CO2_CONCENTRATION",
                "lower_bound": co2_bounds[0],
                "upper_bound": co2_bounds[1],
                "unit": co2_unit,
                "epistemic_status": co2_status,
            },
        )
    )
    _commit(
        graph.create_entity(
            "CausalHypothesis",
            "sentinel:hypothesis",
            {
                "name": "fictional preferred causal account",
                "epistemic_status": "PREFERRED_HYPOTHESIS",
            },
        )
    )

    mechanism_ids = {}
    for kind in sorted(
        {
            "ASCENDING_MELT",
            "CARBON_DIOXIDE_DEGASSING",
            "VOLUME_CHANGE",
            "PRESSURE_INCREASE",
            "EXTENSIONAL_STRESS",
            "LOCAL_HIGH_STRAIN_RATE",
            "EARTHQUAKE_TRIGGERING",
        }
    ):
        record_id = "sentinel:mechanism:" + kind.lower()
        mechanism_ids[kind] = record_id
        _commit(
            graph.create_entity(
                "MechanismElement",
                record_id,
                {"mechanism_kind": kind},
            )
        )

    if not omit_acquisition:
        _commit(
            graph.create_relation(
                "DataAcquisitionRelation",
                "sentinel:relation:acquisition",
                "sentinel:network",
                "sentinel:campaign",
                {
                    "relation_type": "ACQUIRED_DURING",
                    "data_kind": "MICROSEISMICITY",
                    "epistemic_status": "REPORTED_OBSERVATION",
                },
            )
        )
    for suffix, source_id, position in (
        ("events", "sentinel:events", event_position),
        ("melt", "sentinel:melt", melt_position),
    ):
        _commit(
            graph.create_relation(
                "SpatialAssociationRelation",
                f"sentinel:relation:spatial:{suffix}",
                source_id,
                "sentinel:ridge",
                {
                    "relation_type": "SPATIALLY_ASSOCIATED_WITH",
                    "relative_position": position,
                    "epistemic_status": "REPORTED_OBSERVATION",
                },
            )
        )
    for suffix, source_id, target_id in (
        ("depth", "sentinel:events", "sentinel:range:depth"),
        ("co2", "sentinel:melt", "sentinel:range:co2"),
    ):
        _commit(
            graph.create_relation(
                "QuantitySubjectRelation",
                f"sentinel:relation:quantity:{suffix}",
                source_id,
                target_id,
                {"relation_type": "HAS_QUANTITY"},
            )
        )
    for kind, target_id in sorted(mechanism_ids.items()):
        _commit(
            graph.create_relation(
                "HypothesisComponentRelation",
                "sentinel:relation:component:" + kind.lower(),
                "sentinel:hypothesis",
                target_id,
                {"relation_type": "HAS_COMPONENT"},
            )
        )
    for position, (source_kind, target_kind) in enumerate(causal_edges, 1):
        _commit(
            graph.create_relation(
                "CausalLinkRelation",
                f"sentinel:relation:causal:{position:02d}",
                mechanism_ids[source_kind],
                mechanism_ids[target_kind],
                {
                    "relation_type": "CAUSES",
                    "epistemic_status": "PREFERRED_HYPOTHESIS",
                },
            )
        )
    _commit(
        graph.create_relation(
            "HypothesisTargetRelation",
            "sentinel:relation:target",
            "sentinel:hypothesis",
            "sentinel:events",
            {"relation_type": "EXPLAINS"},
        )
    )
    return graph


def test_binding_binds_exact_selected_control_and_executor() -> None:
    binding = _load(BINDING)
    identities = binding["identities"]
    expected_files = {
        "question_set": EXPERIMENT / "competency-questions.json",
        "sealed_oracle": PRIVATE / "answer-oracle.json",
        "recovery_precommit": EXPERIMENT / "ontology-recovery-precommit.json",
        "recovery_ontology": EXPERIMENT / "controlled-ontology-recovery.yaml",
        "validated_contract": (
            EXPERIMENT / "ontology-recovery-compilation/validated-contract.json"
        ),
        "compiler_receipt": (
            EXPERIMENT / "ontology-recovery-compilation/compile-receipt.json"
        ),
        "recovery_review_result": (PRIVATE / "ontology-recovery-adequacy-result.json"),
        "recovery_review_receipt": (
            EXPERIMENT / "ontology-recovery-adequacy-receipt.json"
        ),
        "knowledge_graph_runtime": ROOT / "src/malleus/kg.py",
        "query_executor": EXECUTOR,
    }

    assert binding["schema"] == "malleus.paper-v4.native-query-binding/v1"
    assert binding["status"] == "FROZEN_AFTER_SELECTED_CONTROL_BEFORE_POPULATION"
    assert binding["classification"] == "POST_PRIMARY_CONTROL"
    assert set(identities) == set(expected_files)
    for role, path in expected_files.items():
        assert identities[role] == {
            "path": str(path.relative_to(ROOT)),
            "sha256": _digest(path),
        }
    assert identities["recovery_review_result"]["sha256"] == (
        "sha256:fbd6b609a854619b3931933932f39687f4e9fe2861076cfc1941c9631a92ce4c"
    )
    assert identities["recovery_review_receipt"]["sha256"] == (
        "sha256:c61ca58167a2655b4d6b4a160559e158db32a5a2872f280d56b9e4c5e41d4841"
    )
    assert binding["compiled_contract"] == {
        "contract_id": "https://malleus.dev/contracts/paper-v4-domain-proposal",
        "logical_contract_digest": (
            "sha256:38dd043bd5b4b596b23da9e5634fa414233c3a6a589d71ae662ccd82b42c0abb"
        ),
        "registry_hash": (
            "sha256:c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332"
        ),
        "symbol_binding_id": (
            "urn:malleus:compiled-graph-recipe-bindings:"
            "14af66f206b0ddeaa870be391a03ab6f0679e57fa224a2686fdd1b93d5726b9f"
        ),
    }
    assert binding["core"] == {
        "commit": "1611944eb8856dbd4f25c2ea8bddbecdb970a3a3",
        "tree": "657ba6ce1be83064d104803ad5dad644d65b4352",
    }
    registry = OntologyRegistry(
        EXPERIMENT / "controlled-ontology-recovery.yaml",
        import_map={"malleus": str(ROOT / "ontology/malleus.yaml")},
    )
    assert "sha256:" + registry.content_hash() == binding["rehydration_registry_hash"]

def test_binding_freezes_exact_closure_questions_and_query_contracts() -> None:
    binding = _load(BINDING)

    assert binding["graph_closure"] == {
        "entities": dict(native_query.NODE_CARDINALITIES),
        "relations": dict(native_query.RELATION_CARDINALITIES),
        "total_entities": 15,
        "total_relations": 20,
    }
    assert [item["id"] for item in binding["queries"]] == list(native_query.QUERY_IDS)
    assert [item["question_id"] for item in binding["queries"]] == list(
        native_query.QUESTION_IDS
    )
    by_id = {item["id"]: item for item in binding["queries"]}
    assert by_id["NQ-CQ-01"]["allowed_record_types"] == [
        "ObservationNetwork",
        "Campaign",
        "DataAcquisitionRelation",
    ]
    assert by_id["NQ-CQ-02"]["allowed_record_types"] == [
        "EarthquakePopulation",
        "RidgeSection",
        "SpatialAssociationRelation",
    ]
    assert by_id["NQ-CQ-03"]["cardinalities"] == {
        "depth_ranges": 1,
        "melt_co2_ranges": 1,
        "quantity_relations": 2,
        "shared_ridge_sections": 1,
        "spatial_relations": 2,
    }
    assert by_id["NQ-CQ-04"]["cardinalities"] == {
        "causal_hypotheses": 1,
        "causal_links": 7,
        "hypothesis_components": 7,
        "hypothesis_targets": 1,
        "mechanism_elements": 7,
        "outcome_spatial_relations": 1,
    }
    assert {
        tuple(edge) for edge in by_id["NQ-CQ-04"]["causal_kind_edges"]
    } == native_query.CAUSAL_KIND_EDGES
    assert binding["execution_boundary"] == {
        "allowed_graph_methods": ["query", "query_relations", "get_node"],
        "runtime_inputs": ["SOURCE_FREE_GRAPH_PROJECTION", "QUERY_BINDING"],
        "forbidden_runtime_inputs": [
            "PDF",
            "OCR_TEXT",
            "SOURCE_LEDGER",
            "LOCATOR_MAP",
            "MODEL_TRANSCRIPT",
            "ANSWER_ORACLE",
            "EMBEDDING_MODEL",
            "VECTOR_INDEX",
            "NETWORK",
        ],
        "oracle_comparison": "SEPARATE_EVALUATOR_PROCESS",
    }


def test_binding_contains_no_pdf_specific_values_or_source_locators() -> None:
    binding = BINDING.read_text(encoding="utf-8")
    forbidden = (
        "SMARTIES",
        "ocean-bottom",
        "RC2",
        "deep microseismicity",
        "Mid-Atlantic",
        "page:",
        "selected-reading",
        "yu-2025",
    )
    assert not [value for value in forbidden if value in binding]


def test_executor_uses_only_the_frozen_public_graph_query_surface() -> None:
    tree = ast.parse(EXECUTOR.read_text(encoding="utf-8"))
    graph_calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "graph"
    }
    imports = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert graph_calls == {"get_node", "query", "query_relations"}
    assert not {"_graph", "snapshot", "export_records"} & {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert not {"pathlib", "os", "socket", "requests", "urllib"} & imports
    assert "open" not in called_names


def test_queries_return_fictional_graph_values_and_raw_semantics_in_order() -> None:
    results = run_frozen_queries(_synthetic_graph())

    assert [item["query_id"] for item in results] == list(native_query.QUERY_IDS)
    assert [item["question_id"] for item in results] == list(native_query.QUESTION_IDS)
    assert results[0]["answer"] == {
        "observing_system": "FICTIONAL SENTINEL OBS ARRAY",
        "campaign": "FICTIONAL SENTINEL VOYAGE",
        "campaign_year": 2042,
        "deployed_instrument_count": 31,
        "usable_instrument_count": 29,
    }
    assert results[1]["answer"] == {
        "ridge_subsection": "ZX-9",
        "event_population": "fictional abyssal tremor cohort",
        "spatial_relation": "beneath the ridge axis",
    }
    assert results[2]["answer"] == {
        "earthquake_depth": {
            "lower": 12.5,
            "upper": 18.75,
            "unit": "km",
            "status": "reported observation",
        },
        "primary_melt_co2": {
            "lower": 0.6,
            "upper": 2.4,
            "unit": "wt%",
            "status": "calculated estimate",
        },
    }
    assert results[3]["answer"] == {
        "epistemic_status": "authors' preferred hypothesis",
        "source_process": "CO2 degassing from ascending melt",
        "intermediate_processes": [
            "volume change",
            "pressure increase under extensional stress",
            "locally high strain rates",
        ],
        "outcome": "triggered deep mantle earthquakes beneath the ZX-9 ridge axis",
    }
    assert results[1]["raw_semantics"]["relative_position"] == ("BENEATH_RIDGE_AXIS")
    assert results[2]["raw_semantics"]["earthquake_depth"]["unit"] == ("KILOMETER")
    assert results[3]["raw_semantics"]["causal_edges"] == [
        list(edge) for edge in sorted(SYNTHETIC_CAUSAL_EDGES)
    ]
    for result in results:
        assert result["witness"]["entity_ids"] == sorted(
            result["witness"]["entity_ids"]
        )
        assert result["witness"]["relation_ids"] == sorted(
            result["witness"]["relation_ids"]
        )


def test_scalar_and_enum_mutations_flow_from_graph_to_rendered_answers() -> None:
    graph = _synthetic_graph(
        network_name="FICTIONAL MUTATED ARRAY",
        campaign_name="FICTIONAL MUTATED VOYAGE",
        campaign_year=2057,
        deployed_count=43,
        usable_count=37,
        ridge_name="QY-4",
        event_name="fictional mutated event cohort",
        depth_bounds=(7.25, 9.75),
        co2_bounds=(1.1, 1.9),
        depth_unit="WEIGHT_PERCENT",
        depth_status="CALCULATED_ESTIMATE",
        co2_unit="KILOMETER",
        co2_status="REPORTED_OBSERVATION",
    )

    cq1 = run_native_query(graph, "NQ-CQ-01")["answer"]
    cq2 = run_native_query(graph, "NQ-CQ-02")["answer"]
    cq3 = run_native_query(graph, "NQ-CQ-03")["answer"]
    cq4 = run_native_query(graph, "NQ-CQ-04")["answer"]
    assert cq1 == {
        "observing_system": "FICTIONAL MUTATED ARRAY",
        "campaign": "FICTIONAL MUTATED VOYAGE",
        "campaign_year": 2057,
        "deployed_instrument_count": 43,
        "usable_instrument_count": 37,
    }
    assert cq2 == {
        "ridge_subsection": "QY-4",
        "event_population": "fictional mutated event cohort",
        "spatial_relation": "beneath the ridge axis",
    }
    assert cq3["earthquake_depth"] == {
        "lower": 7.25,
        "upper": 9.75,
        "unit": "wt%",
        "status": "calculated estimate",
    }
    assert cq3["primary_melt_co2"] == {
        "lower": 1.1,
        "upper": 1.9,
        "unit": "km",
        "status": "reported observation",
    }
    assert cq4["outcome"].endswith("beneath the QY-4 ridge axis")

    position_answer = run_native_query(
        _synthetic_graph(event_position="ALONG_RIDGE_SECTION"),
        "NQ-CQ-02",
    )["answer"]
    assert position_answer["spatial_relation"] == "along the ridge section"


@pytest.mark.parametrize(
    ("graph", "query_id", "match"),
    [
        (
            lambda: _synthetic_graph(extra_network=True),
            "NQ-CQ-01",
            "node type cardinalities differ",
        ),
        (
            lambda: _synthetic_graph(omit_acquisition=True),
            "NQ-CQ-01",
            "relation type cardinalities differ",
        ),
        (
            lambda: _synthetic_graph(melt_position="BENEATH_RIDGE_AXIS"),
            "NQ-CQ-03",
            "must equal 'ALONG_RIDGE_SECTION'",
        ),
        (
            lambda: _synthetic_graph(
                causal_edges=(
                    *SYNTHETIC_CAUSAL_EDGES[:-1],
                    ("ASCENDING_MELT", "EARTHQUAKE_TRIGGERING"),
                )
            ),
            "NQ-CQ-04",
            "causal topology differs",
        ),
    ],
)
def test_cardinality_context_and_topology_mutations_refuse_atomically(
    graph: Any,
    query_id: str,
    match: str,
) -> None:
    with pytest.raises(NativeQueryRefusal, match=match):
        run_native_query(graph(), query_id)


def test_query_execution_performs_no_file_or_network_access(monkeypatch: Any) -> None:
    graph = _synthetic_graph()

    def forbidden_open(*args: Any, **kwargs: Any) -> None:
        raise AssertionError(f"query attempted file access: {args!r} {kwargs!r}")

    monkeypatch.setattr(builtins, "open", forbidden_open)
    assert len(run_frozen_queries(graph)) == 4


def test_unknown_query_and_non_graph_inputs_fail_loudly() -> None:
    graph = _synthetic_graph()
    with pytest.raises(NativeQueryRefusal, match="unknown query id"):
        run_native_query(graph, "NQ-CQ-99")
    with pytest.raises(TypeError, match="exact KnowledgeGraph"):
        run_native_query(object(), "NQ-CQ-01")

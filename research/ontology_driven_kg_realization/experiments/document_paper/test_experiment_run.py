"""Fiction-only checks for the private paper-v4 experiment orchestrator."""

from __future__ import annotations

import ast
from dataclasses import MISSING, fields, replace
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory
from malleus.ledger import canonical_json
from malleus.staging import ProposedOperation

from research.ontology_driven_kg_realization.experiments.document_paper import (
    experiment_run as experiment_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.experiment_run import (
    ExperimentRunError,
    PaperExperimentConfiguration,
    run_paper_experiment,
)
from research.ontology_driven_kg_realization.experiments.document_paper.population_compile import (
    PopulationCompilation,
)
from research.ontology_driven_kg_realization.experiments.document_paper.query_replay import (
    run_query_replay,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.assembly import (
    AssemblyPlan,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.model import (
    GraphRecipeFailure,
)
from research.ontology_driven_kg_realization.experiments.document_paper.test_population_compile import (
    ONTOLOGY,
    ONTOLOGY_DIGEST,
    READING,
    RECORD_TYPES,
    RECIPES,
    V1_PROFILE,
    _bytes,
    _located,
    _population,
    _source,
)
from tests.contract_compiler.pareto.test_validated_contract import _trusted_types


ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / "paper-v4" / "experiment"
MALLEUS = (RUN / "ontology-run" / "inputs" / "malleus.yaml").read_bytes()
QUERIES = (RUN / "native-query-binding.json").read_bytes()
MACHINE = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/small_shop/pareto/machine.json"
).read_bytes()
SOURCE_DIGEST = (
    "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
)


def _reading(source_digest: str = SOURCE_DIGEST) -> bytes:
    reading = json.loads(READING)
    reading["source_sha256"] = source_digest
    return canonical_json(reading).encode("utf-8") + b"\n"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _redigest_plan(plan: AssemblyPlan) -> AssemblyPlan:
    draft = replace(plan, plan_digest="sha256:" + "0" * 64)
    plan_bytes = canonical_json(
        {
            "schema_version": "graph-recipe-plan-v0",
            "contract_digest": draft.contract_digest,
            "invocation_digests": list(draft.invocation_digests),
            "member_graph": draft.member_graph_artifact(),
            "proposed_operations": draft.proposed_operations_artifact(),
        }
    ).encode("utf-8")
    return replace(draft, plan_digest=_digest(plan_bytes))


def _acceptance(ontology_digest: str = ONTOLOGY_DIGEST) -> bytes:
    return (
        canonical_json(
            {
                "actor_id": "actor:paper-v4-evaluator",
                "decision": "ACCEPT_FOR_POPULATION",
                "event_type": "ONTOLOGY_DECISION",
                "ontology_sha256": ontology_digest,
                "ordinal": 1,
                "schema": "malleus.paper-v4.ontology-decision/v1",
            }
        ).encode("utf-8")
        + b"\n"
    )


def _configuration(
    *,
    ontology: bytes = ONTOLOGY,
    reading: bytes | None = None,
    population: bytes | None = None,
    recipes: bytes = RECIPES,
    acceptance: bytes | None = None,
    machine: bytes = MACHINE,
) -> PaperExperimentConfiguration:
    reading_bytes = _reading() if reading is None else reading
    population_bytes = _bytes(_full_population()) if population is None else population
    acceptance_bytes = (
        _acceptance(_digest(ontology)) if acceptance is None else acceptance
    )
    return PaperExperimentConfiguration(
        result_schema="malleus.paper-v4.knowledge-build-result/v2",
        source_sha256=SOURCE_DIGEST,
        ontology_sha256=_digest(ontology),
        reading_sha256=_digest(reading_bytes),
        malleus_import_sha256=_digest(MALLEUS),
        linkml_types_sha256=_digest(_trusted_types()),
        population_sha256=_digest(population_bytes),
        generic_recipe_sha256=_digest(recipes),
        ontology_acceptance_sha256=_digest(acceptance_bytes),
        protocol_machine_sha256=_digest(machine),
        population_recipe_profile=V1_PROFILE,
        record_type_iris=RECORD_TYPES,
        contract_id="https://malleus.dev/contracts/paper-four-fiction",
        transaction_time="2026-09-02T00:00:00Z",
        ontology_locator="paper-v4:fiction-ontology",
        malleus_import_locator="malleus",
        linkml_types_locator="linkml:types",
    )


def _full_population() -> dict[str, object]:
    population = _population()
    population["reading_sha256"] = _digest(_reading())
    population["records"] = [
        *population["records"][:2],
        {
            "record_id": "fiction:region",
            "record_type": "Region",
            "record_block_id": "fiction:block:1",
            "properties": {"name": _located("Fictional region")},
        },
        {
            "record_id": "fiction:earthquakes",
            "record_type": "EarthquakePopulation",
            "record_block_id": "fiction:block:1",
            "properties": {"name": _located("Fictional earthquake cohort")},
        },
        {
            "record_id": "fiction:melts",
            "record_type": "PrimaryMeltPopulation",
            "record_block_id": "fiction:block:2",
            "properties": {
                "name": _located("Fictional melt cohort", "fiction:block:2")
            },
        },
        {
            "record_id": "fiction:depth",
            "record_type": "BoundedQuantity",
            "record_block_id": "fiction:block:1",
            "properties": {
                "quantity_kind": _located("fictional depth"),
                "lower_value": _located(1.25),
                "upper_value": _located(2.75),
                "unit": _located("fictional depth unit"),
                "quantity_status": _located("REPORTED_OBSERVATION"),
            },
        },
        {
            "record_id": "fiction:composition",
            "record_type": "BoundedQuantity",
            "record_block_id": "fiction:block:2",
            "properties": {
                "quantity_kind": _located("fictional composition", "fiction:block:2"),
                "lower_value": _located(0.5, "fiction:block:2"),
                "upper_value": _located(1.5, "fiction:block:2"),
                "unit": _located("fictional composition unit", "fiction:block:2"),
                "quantity_status": _located("CALCULATED_ESTIMATE", "fiction:block:2"),
            },
        },
        {
            "record_id": "fiction:hypothesis",
            "record_type": "MechanismHypothesis",
            "record_block_id": "fiction:block:2",
            "properties": {
                "initiating_condition": _located("fictional start", "fiction:block:2"),
                "transformation": _located("fictional process", "fiction:block:2"),
                "physical_effect": _located("fictional effect", "fiction:block:2"),
                "stress_context": _located("fictional stress", "fiction:block:2"),
                "outcome": _located("fictional outcome", "fiction:block:2"),
            },
        },
        population["records"][2],
        {
            "record_id": "fiction:spatial-earthquakes",
            "record_type": "SpatialAssociationRelation",
            "record_block_id": "fiction:block:1",
            "properties": {"relative_position": _located("fictionally below")},
            "source": {
                "record_id": "fiction:earthquakes",
                "block_id": "fiction:block:1",
            },
            "target": {"record_id": "fiction:region", "block_id": "fiction:block:1"},
        },
        {
            "record_id": "fiction:spatial-melts",
            "record_type": "SpatialAssociationRelation",
            "record_block_id": "fiction:block:2",
            "properties": {
                "relative_position": _located("fictionally beside", "fiction:block:2")
            },
            "source": {"record_id": "fiction:melts", "block_id": "fiction:block:2"},
            "target": {"record_id": "fiction:region", "block_id": "fiction:block:2"},
        },
        {
            "record_id": "fiction:depth-characterization",
            "record_type": "QuantityCharacterizationRelation",
            "record_block_id": "fiction:block:1",
            "properties": {},
            "source": {"record_id": "fiction:depth", "block_id": "fiction:block:1"},
            "target": {
                "record_id": "fiction:earthquakes",
                "block_id": "fiction:block:1",
            },
        },
        {
            "record_id": "fiction:composition-characterization",
            "record_type": "QuantityCharacterizationRelation",
            "record_block_id": "fiction:block:2",
            "properties": {},
            "source": {
                "record_id": "fiction:composition",
                "block_id": "fiction:block:2",
            },
            "target": {"record_id": "fiction:melts", "block_id": "fiction:block:2"},
        },
        {
            "record_id": "fiction:explanation",
            "record_type": "HypothesisExplainsRelation",
            "record_block_id": "fiction:block:2",
            "properties": {},
            "source": {
                "record_id": "fiction:hypothesis",
                "block_id": "fiction:block:2",
            },
            "target": {
                "record_id": "fiction:earthquakes",
                "block_id": "fiction:block:2",
            },
        },
    ]
    return population


def _run(
    path: Path,
    *,
    ontology: bytes = ONTOLOGY,
    population: bytes | None = None,
    reading: bytes | None = None,
    acceptance: bytes | None = None,
    machine: bytes = MACHINE,
    configuration: PaperExperimentConfiguration | None = None,
):
    reading_bytes = _reading() if reading is None else reading
    population_bytes = _bytes(_full_population()) if population is None else population
    acceptance_bytes = (
        _acceptance(_digest(ontology)) if acceptance is None else acceptance
    )
    configured = configuration or _configuration(
        ontology=ontology,
        reading=reading_bytes,
        population=population_bytes,
        acceptance=acceptance_bytes,
        machine=machine,
    )
    return run_paper_experiment(
        path,
        configuration=configured,
        selected_ontology=_source(configured.ontology_locator, ontology),
        malleus_import=_source(configured.malleus_import_locator, MALLEUS),
        linkml_types=_source(configured.linkml_types_locator, _trusted_types()),
        selected_reading_bytes=reading_bytes,
        population_bytes=population_bytes,
        generic_recipe_bytes=RECIPES,
        ontology_acceptance_bytes=acceptance_bytes,
        protocol_machine_bytes=machine,
    )


def test_run_is_deterministic_and_reopens_from_ledger_only(tmp_path: Path) -> None:
    first_path = tmp_path / "first" / "semantic.jsonl"
    second_path = tmp_path / "second" / "semantic.jsonl"
    first = _run(first_path)
    second = _run(second_path)

    assert first == second
    assert first_path.read_bytes() == second_path.read_bytes()
    assert canonical_json(json.loads(first.canonical_plan_bytes)).encode() == (
        first.canonical_plan_bytes
    )
    assert canonical_json(json.loads(first.provenance_bytes)).encode() == (
        first.provenance_bytes
    )
    result = json.loads(first.result_bytes)
    assert result == {
        "decision": "ACCEPT",
        "entity_count": 8,
        "ledger_head": KnowledgeChangeHistory.reopen(first_path).replay().ledger_head,
        "ontology_sha256": ONTOLOGY_DIGEST,
        "reading_sha256": _digest(_reading()),
        "relation_count": 6,
        "replay_receipt_sha256": _digest(first.replay_receipt_bytes),
        "schema": "malleus.paper-v4.knowledge-build-result/v2",
        "source_sha256": SOURCE_DIGEST,
    }
    replay = KnowledgeChangeHistory.reopen(first_path).replay()
    assert replay.receipt.canonical_bytes == first.replay_receipt_bytes
    assert replay.graph.node_count == 8
    assert replay.graph.edge_count == 6
    assert (
        replay.machine_state.get_record(
            "DecisionRecord", "decision:paper-v4:population"
        )["verdict"]
        == "ACCEPT"
    )


def test_check_events_are_derived_from_retained_receipts(tmp_path: Path) -> None:
    ledger = tmp_path / "semantic.jsonl"
    run = _run(ledger)
    replay = KnowledgeChangeHistory.reopen(ledger).replay()
    closure = dict((*replay.change_sets[0].sources, *replay.change_sets[0].evidence))
    assert replay.retained_bytes("evidence:paper-v4:population") == _bytes(
        _full_population()
    )
    assert replay.retained_bytes("evidence:paper-v4:ontology-acceptance") == (
        _acceptance()
    )
    assert replay.retained_bytes("evidence:paper-v4:generic-recipes") == RECIPES
    with pytest.raises(KeyError, match="unknown retained record"):
        replay.retained_bytes("evidence:paper-v4:query-binding")
    assert replay.retained_bytes("evidence:paper-v4:assembly-plan") == (
        run.canonical_plan_bytes
    )
    assert replay.retained_bytes("evidence:paper-v4:population-provenance") == (
        run.provenance_bytes
    )

    for check_id in ("source-locator-integrity", "structural-conformance"):
        contract_id = f"evidence:paper-v4:check-contract:{check_id}"
        result_id = f"evidence:paper-v4:check-result:{check_id}"
        contract_bytes = replay.retained_bytes(contract_id)
        receipt_bytes = replay.retained_bytes(result_id)
        receipt = json.loads(receipt_bytes)
        assert closure[contract_id] == _digest(contract_bytes)
        assert closure[result_id] == _digest(receipt_bytes)
        assert receipt["check_contract_id"] == check_id
        assert receipt["check_contract_identity"] == _digest(contract_bytes)
        assert receipt["outcome"] == "SATISFIED"
        assert "verdict" not in receipt
        if check_id == "source-locator-integrity":
            assert {item["record_id"] for item in receipt["inputs"]} == {
                "source:paper-v4:selected-reading",
                "evidence:paper-v4:population",
                "evidence:paper-v4:assembly-plan",
                "evidence:paper-v4:population-provenance",
            }
        for item in receipt["inputs"]:
            assert closure[item["record_id"]] == item["sha256"]
        record = replay.machine_state.get_record("CheckRecord", receipt["receipt_id"])
        assert record is not None
        for field in (
            "check_contract_id",
            "check_contract_identity",
            "outcome",
            "receipt_id",
        ):
            assert record[field] == receipt[field]

    verdict_events = [
        json.loads(line)
        for line in ledger.read_bytes().splitlines()
        if json.loads(line)["event_type"] == "VERDICT_RECORDED"
    ]
    assert len(verdict_events) == 1
    assert verdict_events[0]["payload"] == {
        "decision_id": "decision:paper-v4:population",
        "proposal_id": "proposal:paper-v4:population",
    }
    assert "verdict" not in verdict_events[0]["payload"]


def test_satisfied_receipt_requires_a_verifier_result() -> None:
    with pytest.raises(ExperimentRunError, match="completed verification"):
        experiment_module._make_check(object())


def test_configuration_has_no_defaulted_coordinates() -> None:
    assert all(
        field.default is MISSING and field.default_factory is MISSING
        for field in fields(PaperExperimentConfiguration)
    )
    assert set(_configuration().input_identities()) == {
        "acceptance",
        "linkml",
        "malleus",
        "machine",
        "ontology",
        "population",
        "reading",
        "recipes",
    }
    with pytest.raises(TypeError, match="population_recipe_profile"):
        replace(_configuration(), population_recipe_profile=object())
    with pytest.raises(ExperimentRunError, match="transaction_time is invalid"):
        replace(_configuration(), transaction_time="not-a-time")


def test_configured_transaction_time_controls_the_complete_history(
    tmp_path: Path,
) -> None:
    transaction_time = "2026-09-03T09:00:00Z"
    ledger = tmp_path / "semantic.jsonl"

    _run(
        ledger,
        configuration=replace(
            _configuration(),
            transaction_time=transaction_time,
        ),
    )

    assert {
        json.loads(line)["transaction_time"] for line in ledger.read_bytes().splitlines()
    } == {transaction_time}


def test_full_run_honors_non_v1_provenance_schema(tmp_path: Path) -> None:
    profile = replace(V1_PROFILE, provenance_schema="fiction.provenance/v2")
    configuration = replace(
        _configuration(),
        population_recipe_profile=profile,
    )

    run = _run(tmp_path / "semantic.jsonl", configuration=configuration)

    assert json.loads(run.provenance_bytes)["schema"] == "fiction.provenance/v2"


def test_every_knowledge_build_coordinate_is_required() -> None:
    configuration = _configuration()
    inputs = {
        "acceptance": _acceptance(),
        "linkml": _trusted_types(),
        "malleus": MALLEUS,
        "machine": MACHINE,
        "ontology": ONTOLOGY,
        "population": _bytes(_full_population()),
        "reading": _reading(),
        "recipes": RECIPES,
    }
    for role in inputs:
        missing = dict(inputs)
        del missing[role]
        with pytest.raises(ExperimentRunError, match=role):
            experiment_module._require_build_inputs(configuration, missing)

        drifted = dict(inputs)
        drifted[role] += b"\n"
        with pytest.raises(ExperimentRunError, match=role):
            experiment_module._require_build_inputs(configuration, drifted)


def test_query_surface_has_no_live_admission_path() -> None:
    signature = inspect.signature(run_paper_experiment)
    assert "query_binding_bytes" not in signature.parameters
    tree = ast.parse(inspect.getsource(experiment_module))
    referenced_names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    assert "load_query_binding" not in referenced_names
    assert "query_binding_bytes" not in referenced_names
    assert "_D4_INPUTS" not in referenced_names


def test_admitted_evidence_closure_is_exactly_query_neutral(tmp_path: Path) -> None:
    ledger = tmp_path / "semantic.jsonl"
    _run(ledger)
    change = KnowledgeChangeHistory.reopen(ledger).replay().change_sets[0]

    assert {record_id for record_id, _ in change.evidence} == {
        "evidence:paper-v4:assembly-plan",
        "evidence:paper-v4:check-contract:source-locator-integrity",
        "evidence:paper-v4:check-contract:structural-conformance",
        "evidence:paper-v4:check-result:source-locator-integrity",
        "evidence:paper-v4:check-result:structural-conformance",
        "evidence:paper-v4:generic-recipes",
        "evidence:paper-v4:linkml-types",
        "evidence:paper-v4:malleus-import",
        "evidence:paper-v4:ontology-source",
        "evidence:paper-v4:ontology-acceptance",
        "evidence:paper-v4:ontology-compilation-receipt",
        "evidence:paper-v4:population",
        "evidence:paper-v4:population-provenance",
    }


def test_replacement_query_binding_cannot_change_admitted_history(
    tmp_path: Path,
) -> None:
    ledger = tmp_path / "semantic.jsonl"
    run = _run(ledger)
    admitted_bytes = ledger.read_bytes()
    admitted_change = KnowledgeChangeHistory.reopen(ledger).replay().change_sets[0]

    replacement = json.loads(QUERIES)
    replacement["queries"][3]["cases"][0]["output_fields"]["source"].reverse()
    replacement_bytes = canonical_json(replacement).encode("utf-8")
    assert _digest(replacement_bytes) != _digest(QUERIES)

    query_inputs = {
        "receipt_source": run.replay_receipt_bytes,
        "ontology_path": RUN / "population-run/inputs/ontology.yaml",
        "ontology_source": ONTOLOGY,
        "malleus_path": RUN / "ontology-run/inputs/malleus.yaml",
        "malleus_source": MALLEUS,
    }
    first_result = json.loads(run_query_replay(binding_source=QUERIES, **query_inputs))
    second_result = json.loads(
        run_query_replay(binding_source=replacement_bytes, **query_inputs)
    )

    assert first_result["inputs"]["query_binding_sha256"] == _digest(QUERIES)
    assert second_result["inputs"]["query_binding_sha256"] == _digest(replacement_bytes)
    assert ledger.read_bytes() == admitted_bytes
    reopened = KnowledgeChangeHistory.reopen(ledger).replay()
    assert reopened.change_sets[0].identity == admitted_change.identity
    assert all("query" not in record_id for record_id, _ in admitted_change.evidence)


def test_exact_knowledge_build_input_mutations_refuse_before_compile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configured = _configuration()
    ontology = ONTOLOGY + b"\n# companion-consistent ontology drift\n"
    ontology_population = _full_population()
    ontology_population["ontology_sha256"] = _digest(ontology)

    reading_data = json.loads(_reading())
    reading_data["pages"][0]["blocks"][0]["text"] = "companion-consistent drift\n"
    reading_data["pages"][0]["blocks"][0]["sha256"] = _digest(
        b"companion-consistent drift\n"
    )
    reading = canonical_json(reading_data).encode("utf-8") + b"\n"
    reading_population = _full_population()
    reading_population["reading_sha256"] = _digest(reading)
    population = _bytes({**_full_population(), "schema": "drift"})

    cases = (
        ("ontology", {"ontology": ontology, "population": _bytes(ontology_population)}),
        ("reading", {"reading": reading, "population": _bytes(reading_population)}),
        ("population", {"population": population}),
        ("acceptance", {"acceptance": _acceptance() + b"\n"}),
        ("machine", {"machine": MACHINE + b"\n"}),
    )
    monkeypatch.setattr(
        experiment_module,
        "compile_exact_ontology",
        lambda **_: pytest.fail("compiler reached after D4 input drift"),
    )
    for name, arguments in cases:
        ledger = tmp_path / f"{name}.jsonl"
        with pytest.raises(ExperimentRunError, match="knowledge-build input drift"):
            _run(ledger, configuration=configured, **arguments)
        assert not ledger.exists()


@pytest.mark.parametrize(
    ("replacement", "message"),
    (
        ("fiction:block:2", "locator claims differ"),
        ("fiction:block:missing", "unknown reading block"),
    ),
)
def test_provenance_locator_mutation_cannot_create_check_or_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement: str,
    message: str,
) -> None:
    compile_population = experiment_module.compile_population
    make_check = experiment_module._make_check
    checks = []

    def mutate(*args, **kwargs) -> PopulationCompilation:
        result = compile_population(*args, **kwargs)
        provenance = json.loads(result.provenance_map_bytes)
        assertion = next(
            item for item in provenance["assertions"] if item["block_id"] != replacement
        )
        assertion["block_id"] = replacement
        return replace(
            result,
            provenance_map_bytes=canonical_json(provenance).encode("utf-8"),
        )

    monkeypatch.setattr(experiment_module, "compile_population", mutate)
    monkeypatch.setattr(
        experiment_module,
        "_make_check",
        lambda verification: checks.append(verification.check_id)
        or make_check(verification),
    )
    ledger = tmp_path / "provenance-drift.jsonl"
    with pytest.raises(ExperimentRunError, match=message):
        _run(ledger)
    assert not ledger.exists()
    assert checks == []


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("fact-member", "semantic claims differ"),
        ("fact-value", "semantic claims differ"),
        ("emission-lineage", "emission lineage differs"),
    ),
)
def test_provenance_semantic_or_lineage_mutation_refuses_before_check(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
    message: str,
) -> None:
    compile_population = experiment_module.compile_population
    make_check = experiment_module._make_check
    checks = []

    def mutate(*args, **kwargs) -> PopulationCompilation:
        result = compile_population(*args, **kwargs)
        provenance = json.loads(result.provenance_map_bytes)
        properties = [
            item
            for item in provenance["assertions"]
            if item["assertion_kind"] == "PROPERTY"
        ]
        assertion = properties[0]
        if mutation == "fact-member":
            assertion["emitted_fact"]["member"] += ":drift"
        elif mutation == "fact-value":
            assertion["emitted_fact"]["value"]["lexical_form"] += " drift"
        else:
            assertion, companion = next(
                (left, right)
                for index, left in enumerate(properties)
                for right in properties[index + 1 :]
                if right["record_id"] == left["record_id"]
            )
            for field in ("emission_id", "expansion_path_id"):
                assertion[field], companion[field] = companion[field], assertion[field]
        return replace(
            result,
            provenance_map_bytes=canonical_json(provenance).encode("utf-8"),
        )

    monkeypatch.setattr(experiment_module, "compile_population", mutate)
    monkeypatch.setattr(
        experiment_module,
        "_make_check",
        lambda verification: checks.append(verification.check_id)
        or make_check(verification),
    )
    ledger = tmp_path / f"{mutation}.jsonl"
    with pytest.raises(ExperimentRunError, match=message):
        _run(ledger)
    assert not ledger.exists()
    assert checks == []


def test_provenance_plan_digest_drift_cannot_create_check_or_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    compile_population = experiment_module.compile_population
    checks = []

    def mutate(*args, **kwargs) -> PopulationCompilation:
        result = compile_population(*args, **kwargs)
        provenance = json.loads(result.provenance_map_bytes)
        provenance["plan_sha256"] = "sha256:" + "f" * 64
        return replace(
            result,
            provenance_map_bytes=canonical_json(provenance).encode("utf-8"),
        )

    monkeypatch.setattr(experiment_module, "compile_population", mutate)
    monkeypatch.setattr(
        experiment_module,
        "_make_check",
        lambda verification: checks.append(verification.check_id),
    )
    ledger = tmp_path / "provenance-plan-drift.jsonl"
    with pytest.raises(ExperimentRunError, match="does not bind its inputs"):
        _run(ledger)
    assert not ledger.exists()
    assert checks == []


@pytest.mark.parametrize(
    ("population_value", "plan_value"),
    ((3, 3.0), (1, True)),
    ids=("int-float", "int-bool"),
)
def test_plan_property_python_equal_type_mutation_refuses_before_check(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    population_value: int,
    plan_value: float | bool,
) -> None:
    assert population_value == plan_value
    assert type(population_value) is not type(plan_value)
    source = _full_population()
    acquisition = next(
        record
        for record in source["records"]
        if record["record_id"] == "fiction:acquisition"
    )
    acquisition["properties"]["instrument_count"]["value"] = population_value
    compile_population = experiment_module.compile_population
    checks = []

    def mutate(*args, **kwargs) -> PopulationCompilation:
        result = compile_population(*args, **kwargs)
        operations = list(result.plan.operations)
        index = next(
            index
            for index, operation in enumerate(operations)
            if operation.record_id == "fiction:acquisition"
        )
        operation = operations[index]
        properties = operation.properties
        properties["instrument_count"] = plan_value
        operations[index] = ProposedOperation(
            operation.op_type,
            operation.record_type,
            operation.record_id,
            properties,
            operation.source_id,
            operation.target_id,
        )
        plan = _redigest_plan(replace(result.plan, operations=tuple(operations)))
        provenance = json.loads(result.provenance_map_bytes)
        provenance["plan_sha256"] = plan.plan_digest
        return replace(
            result,
            plan=plan,
            provenance_map_bytes=canonical_json(provenance).encode("utf-8"),
        )

    monkeypatch.setattr(experiment_module, "compile_population", mutate)
    monkeypatch.setattr(
        experiment_module,
        "_make_check",
        lambda verification: checks.append(verification.check_id),
    )
    ledger = tmp_path / f"property-type-{type(plan_value).__name__}.jsonl"
    with pytest.raises(ExperimentRunError, match="plan operation differ"):
        _run(ledger, population=_bytes(source))
    assert not ledger.exists()
    assert checks == []


def test_plan_alignment_mutation_cannot_create_check_or_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    compile_population = experiment_module.compile_population
    make_check = experiment_module._make_check
    checks = []

    def mutate(*args, **kwargs) -> PopulationCompilation:
        result = compile_population(*args, **kwargs)
        draft = replace(
            result.plan,
            contract_digest="sha256:" + "f" * 64,
            plan_digest="sha256:" + "0" * 64,
        )
        plan_bytes = canonical_json(
            {
                "schema_version": "graph-recipe-plan-v0",
                "contract_digest": draft.contract_digest,
                "invocation_digests": list(draft.invocation_digests),
                "member_graph": draft.member_graph_artifact(),
                "proposed_operations": draft.proposed_operations_artifact(),
            }
        ).encode("utf-8")
        plan = replace(draft, plan_digest=_digest(plan_bytes))
        provenance = json.loads(result.provenance_map_bytes)
        provenance["plan_sha256"] = plan.plan_digest
        return replace(
            result,
            plan=plan,
            provenance_map_bytes=canonical_json(provenance).encode("utf-8"),
        )

    monkeypatch.setattr(experiment_module, "compile_population", mutate)
    monkeypatch.setattr(
        experiment_module,
        "_make_check",
        lambda verification: checks.append(verification.check_id)
        or make_check(verification),
    )
    ledger = tmp_path / "plan-drift.jsonl"
    with pytest.raises(GraphRecipeFailure, match="AssemblyPlan contract digest"):
        _run(ledger)
    assert not ledger.exists()
    assert checks == ["source-locator-integrity"]


def test_selected_reading_source_digest_drift_refuses_before_ledger(
    tmp_path: Path,
) -> None:
    ledger = tmp_path / "source-drift.jsonl"
    reading = _reading("sha256:" + "f" * 64)
    with pytest.raises(ExperimentRunError, match="configured source identity"):
        _run(ledger, reading=reading)
    assert not ledger.exists()

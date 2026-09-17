"""Domain-neutral graph compiler, contract, and logic-check record tests."""

from pathlib import Path
from dataclasses import replace

import pytest

from malleus.kg import KnowledgeGraph
from malleus.logic import (
    GraphFactCompiler,
    GraphProvenance,
    LogicCheckResult,
    LogicContract,
    LogicError,
    LogicExecutionError,
    RecordDerivation,
    RetainedSourceText,
    Violation,
    FACT_CONTRACT_VERSION,
    FACT_PREDICATES,
    FACT_PREDICATES_BY_VERSION,
    SUPPORTED_FACT_CONTRACT_VERSIONS,
    fact_declarations,
    logic_monitor_failure_records,
)
from malleus.ontology import OntologyRegistry
from malleus.protocol import content_digest
from malleus.staging import ProposedOperation, stage_subgraph


ROOT = Path(__file__).parent.parent
CYP450_SCHEMA = ROOT / "ontology" / "domains" / "cyp450.yaml"
CYP450_CONTRACT = ROOT / "prolog" / "cyp450_logic.yaml"


def test_contract_hashes_rules_and_declared_metadata(tmp_path):
    rules = tmp_path / "rules.pl"
    rules.write_text("malleus_rule('R').\nmalleus_violation(_, _, _) :- fail.\n", encoding="utf-8")
    ontology_hash = f"sha256:{OntologyRegistry(CYP450_SCHEMA).content_hash()}"
    contract_path = tmp_path / "logic.yaml"
    contract_path.write_text(
        f'''schema_version: "1"
contract_id: contract
contract_version: "1"
ontology_hash: {ontology_hash}
fact_contract_version: "2"
ruleset_id: rules
ruleset_version: "1"
rules_file: rules.pl
rule_ids:
  - R
timeout_seconds: 5
''',
        encoding="utf-8",
    )
    first = LogicContract.load(contract_path)
    rules.write_text(rules.read_text(encoding="utf-8") + "% changed\n", encoding="utf-8")
    second = LogicContract.load(contract_path)
    assert first.ruleset_hash != second.ruleset_hash
    assert first.contract_hash != second.contract_hash


def test_ruleset_hash_commits_to_exact_line_ending_bytes(tmp_path):
    rules = tmp_path / "rules.pl"
    ontology_hash = f"sha256:{OntologyRegistry(CYP450_SCHEMA).content_hash()}"
    contract_path = tmp_path / "logic.yaml"
    contract_path.write_text(
        f'''schema_version: "1"
contract_id: contract
contract_version: "1"
ontology_hash: {ontology_hash}
fact_contract_version: "2"
ruleset_id: rules
ruleset_version: "1"
rules_file: rules.pl
rule_ids:
  - R
timeout_seconds: 5
''',
        encoding="utf-8",
    )
    rules.write_bytes(b"malleus_rule('R').\nmalleus_violation(_, _, _) :- fail.\n")
    lf = LogicContract.load(contract_path)
    rules.write_bytes(b"malleus_rule('R').\r\nmalleus_violation(_, _, _) :- fail.\r\n")
    crlf = LogicContract.load(contract_path)
    assert lf.ruleset_hash != crlf.ruleset_hash
    assert lf.contract_hash != crlf.contract_hash


def test_rule_manifest_order_has_set_semantics(tmp_path):
    rules = tmp_path / "rules.pl"
    rules.write_text(
        "malleus_rule('A').\nmalleus_rule('B').\nmalleus_violation(_, _, _) :- fail.\n",
        encoding="utf-8",
    )
    ontology_hash = f"sha256:{OntologyRegistry(CYP450_SCHEMA).content_hash()}"
    paths = []
    for name, rule_ids in (("first", ["A", "B"]), ("second", ["B", "A"])):
        path = tmp_path / f"{name}.yaml"
        path.write_text(
            f'''schema_version: "1"
contract_id: contract
contract_version: "1"
ontology_hash: {ontology_hash}
fact_contract_version: "2"
ruleset_id: rules
ruleset_version: "1"
rules_file: rules.pl
rule_ids:
  - {rule_ids[0]}
  - {rule_ids[1]}
timeout_seconds: 5
''',
            encoding="utf-8",
        )
        paths.append(path)
    first, second = map(LogicContract.load, paths)
    assert first.rule_ids == second.rule_ids == ("A", "B")
    assert first.contract_hash == second.contract_hash


def test_logic_contract_builds_replay_visible_semantic_artifact():
    contract = LogicContract.load(CYP450_CONTRACT)
    ruleset_record_hash = "sha256:" + "1" * 64
    artifact = contract.to_protocol_artifact(
        event_id="event:contract",
        generated_at="2026-08-12T18:00:00Z",
        actor_id="actor:registrar",
        role="registrar",
        ruleset_record_hash=ruleset_record_hash,
    )
    assert artifact["artifact_hash"] == contract.contract_hash
    assert artifact["ruleset_record_hash"] == ruleset_record_hash
    assert artifact["ruleset_artifact_hash"] == contract.ruleset_hash
    assert artifact["rule_ids"] == sorted(contract.rule_ids)


@pytest.mark.parametrize(
    "field,value,message",
    [
        ("rules_source", "malleus_rule('OTHER').\n", "rules_source"),
        ("rule_ids", ("OTHER",), "contract_hash"),
        ("timeout_seconds", 99, "contract_hash"),
        ("ontology_hash", "sha256:" + "0" * 64, "contract_hash"),
    ],
)
def test_mutated_in_memory_contract_cannot_execute_or_serialize(field, value, message):
    contract = replace(LogicContract.load(CYP450_CONTRACT), **{field: value})
    with pytest.raises(LogicError, match=message):
        contract.validate_integrity()
    with pytest.raises(LogicError, match=message):
        contract.to_protocol_artifact(
            event_id="event:contract",
            generated_at="2026-08-12T18:00:00Z",
            actor_id="actor:registrar",
            role="registrar",
            ruleset_record_hash="sha256:" + "1" * 64,
        )


@pytest.mark.parametrize(
    "replacement, message",
    [
        ("schema_version: \"2\"", "Unsupported"),
        ("rule_ids:\n  - R\n  - R", "must be unique"),
        ("rule_ids: []", "nonempty"),
    ],
)
def test_invalid_contracts_fail_loudly(tmp_path, replacement, message):
    base = (ROOT / "prolog" / "cyp450_logic.yaml").read_text(encoding="utf-8")
    if replacement.startswith("schema"):
        base = base.replace('schema_version: "1"', replacement)
    else:
        start = base.index("rule_ids:")
        end = base.index("timeout_seconds:", start)
        base = base[:start] + replacement + "\n" + base[end:]
    (tmp_path / "cyp450_rules.pl").write_text("rule.\n", encoding="utf-8")
    path = tmp_path / "logic.yaml"
    path.write_text(base, encoding="utf-8")
    with pytest.raises(LogicError, match=message):
        LogicContract.load(path)


def test_duplicate_contract_keys_fail_loudly(tmp_path):
    path = tmp_path / "logic.yaml"
    path.write_text("schema_version: '1'\nschema_version: '1'\n", encoding="utf-8")
    with pytest.raises(LogicError, match="Duplicate YAML key"):
        LogicContract.load(path)


def test_unknown_fact_contract_version_fails_loudly(tmp_path):
    base = CYP450_CONTRACT.read_text(encoding="utf-8").replace(
        'fact_contract_version: "2"',
        'fact_contract_version: "99"',
    )
    (tmp_path / "cyp450_rules.pl").write_text("rule.\n", encoding="utf-8")
    path = tmp_path / "logic.yaml"
    path.write_text(base, encoding="utf-8")
    with pytest.raises(LogicError, match="fact_contract_version"):
        LogicContract.load(path)


def test_every_fixed_fact_predicate_is_declared_even_when_empty():
    declarations = set(fact_declarations().splitlines())
    assert declarations == {
        f":- dynamic {predicate}/{arity}."
        for predicate, arity in FACT_PREDICATES.items()
    }


def test_compiler_is_insertion_order_deterministic():
    registry = OntologyRegistry(CYP450_SCHEMA)
    first = KnowledgeGraph(registry)
    second = KnowledgeGraph(registry)
    for graph, identifiers in ((first, ("a", "b")), (second, ("b", "a"))):
        for identifier in identifiers:
            graph.create_entity("Drug", identifier, {"name": identifier.upper()})
    left = GraphFactCompiler().compile(first)
    right = GraphFactCompiler().compile(second)
    assert left.facts == right.facts
    assert left.facts_hash == right.facts_hash


def test_compiler_binds_digest_to_the_snapshot_that_produced_facts():
    class MutatingAfterSnapshot(KnowledgeGraph):
        def snapshot(self):
            captured = super().snapshot()
            if "later" not in self._identifiers:
                self.create_entity("Drug", "later", {"name": "Later"})
            return captured

    graph = MutatingAfterSnapshot(OntologyRegistry(CYP450_SCHEMA))
    graph.create_entity("Drug", "first", {"name": "First"})
    compiled = GraphFactCompiler().compile(graph)

    assert compiled.state_digests == (content_digest({
        "ontology_hash": f"sha256:{graph.registry.content_hash()}",
        "nodes": [{"id": "first", "type": "Drug", "name": "First"}],
        "relations": [],
    }),)
    assert "later" not in compiled.record_ids
    assert graph.state_digest() != compiled.state_digests[0]


def test_compiler_rejects_mixed_ontologies():
    cyp = KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))
    attack = KnowledgeGraph(OntologyRegistry(ROOT / "ontology" / "domains" / "attack.yaml"))
    with pytest.raises(LogicError, match="different ontologies"):
        GraphFactCompiler().compile(cyp, attack)


def test_compiler_rejects_duplicate_context_record_ids():
    registry = OntologyRegistry(CYP450_SCHEMA)
    first = KnowledgeGraph(registry)
    second = KnowledgeGraph(registry)
    first.create_entity("Drug", "duplicate", {"name": "A"})
    second.create_entity("Drug", "duplicate", {"name": "A"})
    with pytest.raises(LogicError, match="Duplicate graph record"):
        GraphFactCompiler().compile(first, second)


def test_unrelated_ontology_uses_same_generic_vocabulary(tmp_path):
    root_schema = ROOT / "ontology" / "malleus.yaml"
    schema = tmp_path / "toy.yaml"
    schema.write_text(
        """id: https://example.org/toy
name: toy
version: 1.0.0
imports:
  - malleus
classes:
  Planet:
    is_a: Entity
    slots:
      - mass
slots:
  mass:
    range: float
    required: true
""",
        encoding="utf-8",
    )
    registry = OntologyRegistry(schema, import_map={"malleus": root_schema})
    graph = KnowledgeGraph(registry)
    graph.create_entity("Planet", "planet-1", {"mass": 4.2})
    compiled = GraphFactCompiler().compile(graph)
    assert any("'Planet'" in fact for fact in compiled.facts)
    assert not any("Drug" in fact or "CYP" in fact for fact in compiled.facts)


def test_agent_mixin_is_preserved_as_ontology_structure(tmp_path):
    root_schema = ROOT / "ontology" / "malleus.yaml"
    schema = tmp_path / "agents.yaml"
    schema.write_text(
        """id: https://example.org/agents
name: agents
version: 1.0.0
imports:
  - malleus
classes:
  Researcher:
    is_a: Entity
    mixins:
      - Agent
  SeniorResearcher:
    is_a: Researcher
""",
        encoding="utf-8",
    )
    registry = OntologyRegistry(schema, import_map={"malleus": root_schema})
    graph = KnowledgeGraph(registry)
    graph.create_entity("Researcher", "researcher-1", {"name": "R", "agent_type": "human"})
    facts = GraphFactCompiler().compile(graph).facts
    assert "m_mixin('Agent')" in facts
    assert "m_has_mixin('Researcher', 'Agent')" in facts
    assert "m_has_mixin('SeniorResearcher', 'Agent')" in facts
    assert "m_has_mixin('Researcher', 'Identifiable')" in facts


def test_architecture_documents_exact_fact_vocabulary():
    text = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    block = text.split("```prolog", 1)[1].split("```", 1)[0]
    documented = {
        line.split("(", 1)[0]
        for line in block.splitlines()
        if line.startswith("m_")
    }
    assert documented == set(FACT_PREDICATES)


def test_compiler_covers_every_structurally_accepted_scalar_and_optional_null(tmp_path):
    root_schema = ROOT / "ontology" / "malleus.yaml"
    schema = tmp_path / "scalars.yaml"
    schema.write_text(
        """id: https://example.org/scalars
name: scalars
version: 1.0.0
imports:
  - malleus
classes:
  ScalarRecord:
    is_a: Entity
    slots:
      - integer_value
      - float_value
      - boolean_value
      - nullable_value
      - list_value
slots:
  integer_value:
    range: integer
  float_value:
    range: float
  boolean_value:
    range: boolean
  nullable_value:
    range: string
  list_value:
    range: string
    multivalued: true
""",
        encoding="utf-8",
    )
    graph = KnowledgeGraph(OntologyRegistry(schema, import_map={"malleus": root_schema}))
    operation = graph.create_entity(
        "ScalarRecord",
        "scalar-1",
        {
            "name": "Text",
            "integer_value": 3,
            "float_value": 4.5,
            "boolean_value": True,
            "nullable_value": None,
            "list_value": ["a", "b"],
        },
    )
    assert operation.op_status.value == "COMMITTED"
    facts = GraphFactCompiler().compile(graph).facts
    assert "m_property('scalar-1', 'integer_value', 'integer', 3)" in facts
    assert "m_property('scalar-1', 'float_value', 'float', 4.5)" in facts
    assert "m_property('scalar-1', 'boolean_value', 'boolean', true)" in facts
    assert "m_property('scalar-1', 'nullable_value', 'null', null)" in facts
    assert "m_list('scalar-1', 'list_value', 2)" in facts


def test_logic_check_records_are_content_addressed_and_not_named_proofs():
    result = LogicCheckResult(
        candidate_digest="sha256:" + "1" * 64,
        base_state_digest="sha256:" + "2" * 64,
        candidate_state_digest="sha256:" + "3" * 64,
        context_state_digests=("sha256:" + "4" * 64,),
        ontology_hash="sha256:" + "5" * 64,
        fact_contract_version="2",
        contract_id="contract",
        contract_version="1",
        contract_hash="sha256:" + "6" * 64,
        ruleset_id="rules",
        ruleset_version="1",
        ruleset_hash="sha256:" + "7" * 64,
        engine_name="SWI-Prolog",
        engine_version="90004",
        timeout_seconds=5,
        facts_hash="sha256:" + "8" * 64,
        fact_count=10,
        translated_record_ids=("record-1", "record-2"),
        checked_rule_ids=("R",),
        violations=(Violation("R", "BAD", ("record-1",)),),
    )
    check, witnesses = result.to_protocol_records(
        check_id="logic-check:1",
        event_id="event:logic-check:1",
        generated_at="2026-08-12T18:00:00Z",
        actor_id="actor:monitor",
        role="logic-monitor",
        proposal_id="proposal:1",
        proposal_content_hash="sha256:" + "9" * 64,
        base_acceptance_head="sha256:" + "a" * 64,
        monitor_id="monitor:logic",
        monitor_version="1",
        monitor_hash="sha256:" + "b" * 64,
        logic_contract_record_hash="sha256:" + "c" * 64,
        ruleset_record_hash="sha256:" + "d" * 64,
    )
    assert check["content_hash"].startswith("sha256:")
    assert check["check_outcome"] == "VIOLATED"
    assert check["violation_witness_ids"] == [witnesses[0]["id"]]
    assert witnesses[0]["witness_binding_hash"].startswith("sha256:")
    assert "proof" not in str(check).lower()


def test_execution_failure_builds_unknown_assessment_without_completed_check():
    failure, assessment = logic_monitor_failure_records(
        error=LogicExecutionError("engine timed out"),
        failure_id="failure:1",
        assessment_id="assessment:1",
        event_id="event:1",
        generated_at="2026-08-12T18:00:00Z",
        actor_id="actor:monitor",
        role="logic-monitor",
        proposal_id="proposal:1",
        proposal_content_hash="sha256:" + "1" * 64,
        base_acceptance_head="sha256:" + "2" * 64,
        monitor_id="monitor:1",
        monitor_version="1",
        monitor_hash="sha256:" + "3" * 64,
        logic_contract_id="logic-contract:1",
        logic_contract_record_hash="sha256:" + "5" * 64,
        ruleset_id="rules:1",
        ruleset_record_hash="sha256:" + "4" * 64,
        failure_category="TIMEOUT",
        error_code="ENGINE_TIMEOUT",
    )
    assert failure["failed_assessment_kind"] == "LOGICAL"
    assert assessment["assessment_outcome"] == "UNKNOWN"
    assert "checked_rule_ids" not in assessment
    assert "violated_rule_ids" not in assessment
    assert "logic_check_record_ids" not in assessment
    assert assessment["monitor_failure_id"] == failure["id"]
    assert failure["logic_contract_id"] == "logic-contract:1"
    assert assessment["logic_contract_record_hash"] == "sha256:" + "5" * 64


_VERSION_TWO_PREDICATES = {
    "m_ontology_hash": 1,
    "m_type": 1,
    "m_mixin": 1,
    "m_subtype": 2,
    "m_has_mixin": 2,
    "m_record": 3,
    "m_relation": 4,
    "m_property": 4,
    "m_list": 3,
    "m_list_item": 5,
}


def _drug_graph():
    graph = KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))
    graph.create_entity("Drug", "drug-1", {"name": "Fluconazole"})
    return graph


def _drug_provenance():
    return GraphProvenance(
        derivations=(
            RecordDerivation(
                record_id="drug-1",
                path=("properties", "name"),
                source_id="source:list",
                locator="row:0:name",
            ),
        ),
        source_texts=(
            RetainedSourceText(
                source_id="source:list",
                locator="row:0:name",
                text="Fluconazole 150 mg",
            ),
        ),
    )


def test_fact_contract_version_three_adds_provenance_and_keeps_version_two():
    assert FACT_CONTRACT_VERSION == "3"
    assert SUPPORTED_FACT_CONTRACT_VERSIONS == ("2", "3")
    assert set(FACT_PREDICATES_BY_VERSION) == {"2", "3"}
    assert FACT_PREDICATES_BY_VERSION["2"] == _VERSION_TWO_PREDICATES
    assert FACT_PREDICATES_BY_VERSION["3"] == {
        **_VERSION_TWO_PREDICATES,
        "m_derivation": 4,
        "m_source_text": 3,
    }
    assert FACT_PREDICATES == FACT_PREDICATES_BY_VERSION["3"]


def test_fact_declarations_follow_the_declared_contract_version():
    version_two = set(fact_declarations("2").splitlines())
    version_three = set(fact_declarations("3").splitlines())

    assert ":- dynamic m_derivation/4." not in version_two
    assert ":- dynamic m_source_text/3." not in version_two
    assert version_two < version_three
    assert version_three - version_two == {
        ":- dynamic m_derivation/4.",
        ":- dynamic m_source_text/3.",
    }
    with pytest.raises(LogicError, match="fact_contract_version"):
        fact_declarations("99")


def test_compiler_emits_a_records_derivation_and_the_text_its_locator_resolves_to():
    compiled = GraphFactCompiler(fact_contract_version="3").compile(
        _drug_graph(), provenance=_drug_provenance()
    )

    assert compiled.fact_contract_version == "3"
    assert (
        "m_derivation('drug-1', 'properties/name', 'source:list', 'row:0:name')"
        in compiled.facts
    )
    assert (
        "m_source_text('source:list', 'row:0:name', 'Fluconazole 150 mg')"
        in compiled.facts
    )


def test_compiler_at_version_three_without_provenance_emits_no_provenance_fact():
    compiled = GraphFactCompiler(fact_contract_version="3").compile(_drug_graph())

    assert compiled.fact_contract_version == "3"
    assert not [fact for fact in compiled.facts if fact.startswith("m_derivation")]
    assert not [fact for fact in compiled.facts if fact.startswith("m_source_text")]


def test_compiler_at_version_two_compiles_exactly_the_earlier_vocabulary():
    """The migration answer for a contract already pinned at version 2."""

    compiled = GraphFactCompiler(fact_contract_version="2").compile(_drug_graph())

    assert compiled.fact_contract_version == "2"
    assert {fact.split("(", 1)[0] for fact in compiled.facts} <= set(
        _VERSION_TWO_PREDICATES
    )


def test_compiler_refuses_provenance_under_the_earlier_fact_contract():
    """A version-2 rule cannot read these facts, so dropping them would lie."""

    with pytest.raises(LogicError, match="fact contract version 2"):
        GraphFactCompiler(fact_contract_version="2").compile(
            _drug_graph(), provenance=_drug_provenance()
        )


def test_compiler_refuses_an_unsupported_fact_contract_version():
    with pytest.raises(LogicError, match="fact_contract_version"):
        GraphFactCompiler(fact_contract_version="99")


def test_compiler_refuses_a_derivation_for_a_record_the_graph_does_not_carry():
    provenance = GraphProvenance(
        derivations=(
            RecordDerivation(
                record_id="drug-absent",
                path=("properties", "name"),
                source_id="source:list",
                locator="row:0:name",
            ),
        ),
        source_texts=(),
    )
    with pytest.raises(LogicError, match="unknown graph record"):
        GraphFactCompiler(fact_contract_version="3").compile(
            _drug_graph(), provenance=provenance
        )


def test_compiler_refuses_a_path_step_that_would_hide_the_join_separator():
    with pytest.raises(LogicError, match="path step"):
        RecordDerivation(
            record_id="drug-1",
            path=("properties", "name/extra"),
            source_id="source:list",
            locator="row:0:name",
        )


def test_compiler_refuses_two_texts_for_one_retained_locator():
    provenance = GraphProvenance(
        derivations=(),
        source_texts=(
            RetainedSourceText("source:list", "row:0:name", "Fluconazole"),
            RetainedSourceText("source:list", "row:0:name", "Ketoconazole"),
        ),
    )
    with pytest.raises(LogicError, match="two texts"):
        GraphFactCompiler(fact_contract_version="3").compile(
            _drug_graph(), provenance=provenance
        )

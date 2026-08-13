"""Execution guardrails for the optional SWI-Prolog logic monitor."""

import shutil
from pathlib import Path
from dataclasses import replace

import pytest

pytestmark = pytest.mark.skipif(
    shutil.which("swipl") is None,
    reason="SWI-Prolog executable is not available",
)

from malleus.kg import KnowledgeGraph
from malleus.logic import LogicContract, LogicError, LogicExecutionError, Violation
from malleus.ontology import OntologyRegistry
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, StagingError, stage_subgraph


ROOT = Path(__file__).parent.parent
CYP450_SCHEMA = ROOT / "ontology" / "domains" / "cyp450.yaml"
CYP450_CONTRACT = ROOT / "prolog" / "cyp450_logic.yaml"


@pytest.fixture
def graph():
    registry = OntologyRegistry(CYP450_SCHEMA)
    result = KnowledgeGraph(registry)
    result.create_entity("Enzyme", "enzyme-1", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
    result.create_entity("Drug", "drug-1", {"name": "Drug One"})
    result.create_relation(
        "InhibitsRelation",
        "inhibits-1",
        "drug-1",
        "enzyme-1",
        {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"},
    )
    return result


@pytest.fixture
def verifier():
    return PrologVerifier(LogicContract.load(CYP450_CONTRACT))


def candidate(graph, *, relation_id="induces-1", relation_type="SUBSTRATE_OF"):
    record_type = {
        "SUBSTRATE_OF": "SubstrateOfRelation",
        "INDUCES": "InducesRelation",
    }[relation_type]
    properties = {"relation_type": relation_type}
    if relation_type == "INDUCES":
        properties["inhibition_strength"] = "STRONG"
    return stage_subgraph(graph, [ProposedOperation.relation(
        record_type,
        relation_id,
        "drug-1",
        "enzyme-1",
        properties,
    )])


def write_contract(tmp_path, rules: str, *, rule_ids=None, timeout_seconds=5) -> Path:
    rules_path = tmp_path / "rules.pl"
    rules_path.write_text(rules, encoding="utf-8")
    ontology_hash = f"sha256:{OntologyRegistry(CYP450_SCHEMA).content_hash()}"
    contract = tmp_path / "logic.yaml"
    ids = rule_ids or ["RULE_ONE"]
    rendered_ids = "\n".join(f"  - {rule_id}" for rule_id in ids)
    contract.write_text(
        f'''schema_version: "1"
contract_id: test-contract
contract_version: "1"
ontology_hash: {ontology_hash}
fact_contract_version: "2"
ruleset_id: test-rules
ruleset_version: "1"
rules_file: rules.pl
rule_ids:
{rendered_ids}
timeout_seconds: {timeout_seconds}
''',
        encoding="utf-8",
    )
    return contract


class TestCandidateVerification:
    def test_absent_relation_and_list_predicates_are_empty_not_undefined(self, verifier):
        graph = KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))
        staged = stage_subgraph(graph, [
            ProposedOperation.entity("Drug", "drug-only", {"name": "Drug Only"})
        ])
        result = verifier.verify_candidate_subgraph(staged)
        assert result.outcome == "SATISFIED"

    def test_clean_candidate_is_satisfied(self, graph, verifier):
        staged = candidate(graph)
        before = graph.snapshot()
        result = verifier.verify_candidate_subgraph(staged)

        assert result.valid
        assert result.outcome == "SATISFIED"
        assert result.checked_rule_ids == ("CYP450_INHIBITOR_INDUCER_CONFLICT",)
        assert result.violations == ()
        assert graph.snapshot() == before

    def test_all_violations_are_canonicalized(self, graph, verifier):
        staged = candidate(graph, relation_type="INDUCES")
        result = verifier.verify_candidate_subgraph(staged)

        assert not result.valid
        assert result.outcome == "VIOLATED"
        assert result.violated_rule_ids == ("CYP450_INHIBITOR_INDUCER_CONFLICT",)
        assert len(result.violations) == 1
        violation = result.violations[0]
        assert violation.violation_code == "INHIBITOR_AND_INDUCER"
        assert violation.witness_record_ids == ("induces-1", "inhibits-1")

    def test_rejected_candidate_has_no_logic_input(self, graph, verifier):
        rejected = stage_subgraph(graph, [ProposedOperation.entity("UnknownType", "bad-1")])
        with pytest.raises(StagingError, match="no usable overlay"):
            verifier.verify_candidate_subgraph(rejected)

    def test_contract_ontology_must_match_candidate(self, graph, tmp_path):
        contract_path = write_contract(
            tmp_path,
            "malleus_rule('RULE_ONE').\nmalleus_violation(_, _, _) :- fail.\n",
        )
        text = contract_path.read_text(encoding="utf-8").replace(
            f"sha256:{graph.registry.content_hash()}",
            "sha256:" + "0" * 64,
        )
        contract_path.write_text(text, encoding="utf-8")
        verifier = PrologVerifier(LogicContract.load(contract_path))
        with pytest.raises(LogicError, match="different ontologies"):
            verifier.verify_candidate_subgraph(candidate(graph))

    def test_old_domain_query_and_tentative_apis_are_deleted(self, verifier):
        assert not hasattr(verifier, "verify_proposed_relation")
        assert not hasattr(verifier, "query_interactions")
        assert not hasattr(verifier, "sync_from_kg")


class TestExecutionFailures:
    def test_mutated_in_memory_contract_cannot_run(self, graph):
        contract = replace(
            LogicContract.load(CYP450_CONTRACT),
            rules_source="malleus_rule('CYP450_INHIBITOR_INDUCER_CONFLICT').\n"
            "malleus_violation(_, _, _) :- fail.\n",
        )
        with pytest.raises(LogicError, match="rules_source"):
            PrologVerifier(contract).verify_candidate_subgraph(candidate(graph))

    def test_missing_swipl_fails_not_satisfied(self, graph, verifier, monkeypatch):
        monkeypatch.setattr("malleus.prolog_verifier.shutil.which", lambda _name: None)
        with pytest.raises(LogicExecutionError, match="not available"):
            verifier.verify_candidate_subgraph(candidate(graph))

    def test_invalid_rules_file_fails_not_satisfied(self, graph, tmp_path):
        contract = write_contract(tmp_path, "this is not valid prolog.\n")
        with pytest.raises(LogicExecutionError, match="exited|JSON result"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_missing_entrypoint_fails_not_satisfied(self, graph, tmp_path):
        contract = write_contract(tmp_path, "malleus_rule('RULE_ONE').\n")
        with pytest.raises(LogicExecutionError, match="JSON result|malleus_violation"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_timeout_fails_not_satisfied(self, graph, tmp_path):
        contract = write_contract(
            tmp_path,
            "malleus_rule('RULE_ONE').\nmalleus_violation(_, _, _) :- sleep(2), fail.\n",
            timeout_seconds=1,
        )
        with pytest.raises(LogicExecutionError, match="exceeded 1 seconds"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_rule_manifest_mismatch_fails(self, graph, tmp_path):
        contract = write_contract(
            tmp_path,
            "malleus_rule('OTHER').\nmalleus_violation(_, _, _) :- fail.\n",
        )
        with pytest.raises(LogicExecutionError, match="differs"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_undeclared_violation_rule_fails(self, graph, tmp_path):
        contract = write_contract(
            tmp_path,
            """malleus_rule('RULE_ONE').
malleus_violation('OTHER', 'BAD', ['drug-1']).
""",
        )
        with pytest.raises(LogicExecutionError, match="undeclared"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    @pytest.mark.parametrize("term", ["1", "1.5", "true", "_"])
    def test_nonstring_rule_identifiers_fail(self, graph, tmp_path, term):
        contract = write_contract(
            tmp_path,
            f"malleus_rule({term}).\nmalleus_violation(_, _, _) :- fail.\n",
            rule_ids=["RULE_ONE"],
        )
        with pytest.raises(LogicExecutionError, match="ground string|invalid JSON"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    @pytest.mark.parametrize("term", ["2", "2.5", "true", "_"])
    def test_nonstring_violation_codes_fail(self, graph, tmp_path, term):
        contract = write_contract(
            tmp_path,
            f"malleus_rule('RULE_ONE').\nmalleus_violation('RULE_ONE', {term}, ['drug-1']).\n",
        )
        with pytest.raises(LogicExecutionError, match="ground string|invalid JSON"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    @pytest.mark.parametrize("term", ["3", "3.5", "true", "_"])
    def test_nonstring_witness_identifiers_fail(self, graph, tmp_path, term):
        contract = write_contract(
            tmp_path,
            f"malleus_rule('RULE_ONE').\nmalleus_violation('RULE_ONE', 'BAD', [{term}]).\n",
        )
        with pytest.raises(LogicExecutionError, match="ground string|invalid JSON"):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_underscore_prefixed_ground_strings_remain_valid(self, tmp_path):
        graph = KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))
        staged = stage_subgraph(graph, [
            ProposedOperation.entity("Drug", "_d", {"name": "D"})
        ])
        contract = write_contract(
            tmp_path,
            "malleus_rule('_RULE').\nmalleus_violation('_RULE', '_CODE', ['_d']).\n",
            rule_ids=["_RULE"],
        )
        result = PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(staged)
        assert result.violations == (Violation("_RULE", "_CODE", ("_d",)),)

    @pytest.mark.parametrize(
        "witness, message",
        [
            ("[]", "nonempty proper list"),
            ("['missing']", "unknown witness"),
            ("['drug-1', 'drug-1']", "must be unique"),
        ],
    )
    def test_malformed_witnesses_fail(self, graph, tmp_path, witness, message):
        contract = write_contract(
            tmp_path,
            f"""malleus_rule('RULE_ONE').
malleus_violation('RULE_ONE', 'BAD', {witness}).
""",
        )
        with pytest.raises(LogicExecutionError, match=message):
            PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))

    def test_duplicate_derivations_have_set_semantics(self, graph, tmp_path):
        contract = write_contract(
            tmp_path,
            """malleus_rule('RULE_ONE').
malleus_violation('RULE_ONE', 'BAD', ['drug-1']).
malleus_violation('RULE_ONE', 'BAD', ['drug-1']).
""",
        )
        result = PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))
        assert len(result.violations) == 1

    def test_all_distinct_violations_are_retained_in_canonical_order(self, graph, tmp_path):
        contract = write_contract(
            tmp_path,
            """malleus_rule('RULE_TWO').
malleus_rule('RULE_ONE').
malleus_violation('RULE_TWO', 'SECOND', ['drug-1']).
malleus_violation('RULE_ONE', 'FIRST', ['enzyme-1', 'drug-1']).
""",
            rule_ids=["RULE_TWO", "RULE_ONE"],
        )
        result = PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(candidate(graph))
        assert result.checked_rule_ids == ("RULE_ONE", "RULE_TWO")
        assert [item.rule_id for item in result.violations] == ["RULE_ONE", "RULE_TWO"]
        assert result.violations[0].witness_record_ids == ("drug-1", "enzyme-1")

    def test_fresh_engine_prevents_cross_run_fact_leakage(self, graph, verifier):
        first = verifier.verify_candidate_subgraph(candidate(graph, relation_type="INDUCES"))
        clean_graph = KnowledgeGraph(graph.registry)
        clean_graph.create_entity("Enzyme", "enzyme-1", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
        clean_graph.create_entity("Drug", "drug-1", {"name": "Drug One"})
        second = verifier.verify_candidate_subgraph(candidate(clean_graph))
        assert not first.valid
        assert second.valid

    def test_quoted_identifier_is_data_not_prolog_code(self, graph, verifier):
        staged = stage_subgraph(graph, [ProposedOperation.entity(
            "Drug",
            "drug-quote') :- throw(injected). %",
            {"name": "quoted\nvalue'). malleus_rule('INJECTED"},
        )])
        result = verifier.verify_candidate_subgraph(staged)
        assert result.valid

    @pytest.mark.parametrize(
        "identifier",
        ["drug\u0085separator", "drug\u2028separator", "drug\u2029separator", "drug\x00nul", "drug-😀"],
    )
    def test_all_control_and_unicode_data_round_trip_in_witnesses(self, tmp_path, identifier):
        graph = KnowledgeGraph(OntologyRegistry(CYP450_SCHEMA))
        staged = stage_subgraph(graph, [
            ProposedOperation.entity("Drug", identifier, {"name": identifier})
        ])
        contract = write_contract(
            tmp_path,
            """malleus_rule('RULE_ONE').
malleus_violation('RULE_ONE', 'UNICODE', [RecordId]) :-
    m_record(RecordId, 'Drug', 'entity').
""",
        )
        result = PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(staged)
        assert result.violations[0].witness_record_ids == (identifier,)

    def test_rule_parser_directive_cannot_turn_graph_data_into_code(self, graph, tmp_path):
        staged = stage_subgraph(graph, [
            ProposedOperation.entity("Drug", "d", {"name": "D"}),
            ProposedOperation.entity(
                "Drug",
                "x').\u2028malleus_violation('RULE_ONE','INJECTED',['d']).\u2028%",
                {"name": "Untrusted graph data"},
            ),
        ])
        contract = write_contract(
            tmp_path,
            """:- set_prolog_flag(character_escapes, false).
malleus_rule('RULE_ONE').
malleus_violation(_, _, _) :- fail.
""",
        )
        result = PrologVerifier.from_contract(str(contract)).verify_candidate_subgraph(staged)
        assert result.outcome == "SATISFIED"

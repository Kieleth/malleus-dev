"""Tests for the optional Prolog verification layer.

Generic tests that don't depend on any specific domain. Uses a minimal
in-memory rules file and a hand-built KG.

Requires: pyswip and SWI-Prolog installed (pip install malleus-dev[prolog]).
"""

import textwrap
from pathlib import Path

import pytest

pytest.importorskip("pyswip")

from malleus.kg import KnowledgeGraph
from malleus.ontology import OntologyRegistry
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, StagingError, stage_subgraph

ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"
CYP450_SCHEMA = ONTOLOGY_DIR / "domains" / "cyp450.yaml"


MINIMAL_RULES = textwrap.dedent("""\
    %% Minimal test rules: drug-enzyme interactions and contradictions.

    %% Interaction: inhibitor + substrate on the same enzyme -> increased exposure.
    interaction(Inhibitor, Substrate, increased_exposure, Enzyme, Strength) :-
        inhibits(Inhibitor, Enzyme, Strength),
        substrate_of(Substrate, Enzyme),
        Inhibitor \\= Substrate.

    %% Interaction: inducer + substrate on the same enzyme -> decreased exposure.
    interaction(Inducer, Substrate, decreased_exposure, Enzyme, Strength) :-
        induces(Inducer, Enzyme, Strength),
        substrate_of(Substrate, Enzyme),
        Inducer \\= Substrate.

    %% Contradiction: same drug cannot be strong inhibitor AND strong inducer
    %% of the same enzyme.
    contradiction(Drug, Enzyme, inhibitor_and_inducer) :-
        inhibits(Drug, Enzyme, strong),
        induces(Drug, Enzyme, strong).
""")


@pytest.fixture
def rules_file(tmp_path):
    """Write the minimal rules to a tempfile and return its path."""
    p = tmp_path / "rules.pl"
    p.write_text(MINIMAL_RULES)
    return p


@pytest.fixture
def populated_kg():
    """A small CYP450 KG: 2 enzymes, 3 drugs, 4 relations."""
    reg = OntologyRegistry(CYP450_SCHEMA)
    kg = KnowledgeGraph(reg)

    kg.create_entity("Enzyme", "enz-1", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
    kg.create_entity("Enzyme", "enz-2", {"name": "CYP2D6", "cyp_isoform": "CYP2D6"})
    kg.create_entity("Drug", "drug-sub", {"name": "Substrate", "drug_class": "x"})
    kg.create_entity("Drug", "drug-inh", {"name": "Inhibitor", "drug_class": "y"})
    kg.create_entity("Drug", "drug-ind", {"name": "Inducer", "drug_class": "z"})

    kg.create_relation("SubstrateOfRelation", "r1", "drug-sub", "enz-1",
                       {"relation_type": "SUBSTRATE_OF"})
    kg.create_relation("InhibitsRelation", "r2", "drug-inh", "enz-1",
                       {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"})
    kg.create_relation("InducesRelation", "r3", "drug-ind", "enz-1",
                       {"relation_type": "INDUCES", "inhibition_strength": "STRONG"})
    return kg


class TestPrologSync:
    def test_sync_loads_facts(self, rules_file, populated_kg):
        """After sync, the fact base is non-empty."""
        v = PrologVerifier(rules_file)
        v.sync_from_kg(populated_kg)
        results = v.query_all_interactions()
        assert len(results) > 0

    def test_sync_multiple_kgs(self, rules_file, populated_kg):
        """Verifier syncs from both static and dynamic KGs."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        dynamic = KnowledgeGraph(reg)
        dynamic.create_entity("Drug", "drug-new", {"name": "New", "drug_class": "z"})
        dynamic.create_relation("InhibitsRelation", "rN", "drug-new", "enz-1",
                                {"relation_type": "SUBSTRATE_OF"})
        # Wait — drug-new depends on enz-1 which is only in populated_kg.
        # The relation above should be rejected because enz-1 isn't in dynamic.
        # That's fine; we're testing that sync can combine both KGs.

        # Rebuild dynamic with its own enzyme copy:
        dynamic = KnowledgeGraph(reg)
        dynamic.create_entity("Enzyme", "enz-1", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
        dynamic.create_entity("Drug", "drug-new", {"name": "New", "drug_class": "z"})
        dynamic.create_relation("InhibitsRelation", "rN", "drug-new", "enz-1",
                                {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"})

        v = PrologVerifier(rules_file)
        v.sync_from_kg(populated_kg, dynamic)
        results = v.query_all_interactions()
        # Both static (drug-inh) and dynamic (drug-new) interactions should appear.
        perpetrators = {r["perpetrator"] for r in results}
        assert "drug-inh" in perpetrators
        assert "drug-new" in perpetrators


class TestInteractionDetection:
    def test_inhibition_interaction_detected(self, rules_file, populated_kg):
        """Inhibitor + substrate on same enzyme = increased_exposure."""
        v = PrologVerifier(rules_file)
        v.sync_from_kg(populated_kg)
        results = v.query_interactions("drug-inh")
        sub = [r for r in results if r["substrate"] == "drug-sub"]
        assert len(sub) == 1
        assert sub[0]["effect"] == "increased_exposure"
        assert sub[0]["enzyme"] == "enz-1"

    def test_induction_interaction_detected(self, rules_file, populated_kg):
        """Inducer + substrate on same enzyme = decreased_exposure."""
        v = PrologVerifier(rules_file)
        v.sync_from_kg(populated_kg)
        results = v.query_interactions("drug-ind")
        sub = [r for r in results if r["substrate"] == "drug-sub"]
        assert len(sub) == 1
        assert sub[0]["effect"] == "decreased_exposure"


class TestVerifyCandidateSubgraph:
    def test_valid_candidate_passes(self, rules_file, populated_kg):
        """A non-contradictory candidate overlay passes verification."""
        v = PrologVerifier(rules_file)
        candidate = stage_subgraph(populated_kg, [ProposedOperation.relation(
            "SubstrateOfRelation",
            "candidate-r1",
            "drug-sub",
            "enz-2",
            {"relation_type": "SUBSTRATE_OF"},
        )])
        result = v.verify_candidate_subgraph(
            candidate,
        )
        assert result.valid

    def test_contradiction_caught(self, rules_file, populated_kg):
        """A drug that's a strong inhibitor added as strong inducer of the same enzyme
        should be flagged as a contradiction."""
        v = PrologVerifier(rules_file)
        candidate = stage_subgraph(populated_kg, [ProposedOperation.relation(
            "InducesRelation",
            "candidate-r2",
            "drug-inh",
            "enz-1",
            {"relation_type": "INDUCES", "inhibition_strength": "STRONG"},
        )])
        result = v.verify_candidate_subgraph(candidate)
        assert not result.valid
        assert result.rule_violated == "contradiction"

    def test_verification_is_read_only(self, rules_file, populated_kg):
        """Verification does not mutate the KG."""
        v = PrologVerifier(rules_file)
        candidate = stage_subgraph(populated_kg, [ProposedOperation.relation(
            "SubstrateOfRelation",
            "candidate-r3",
            "drug-sub",
            "enz-2",
            {"relation_type": "SUBSTRATE_OF"},
        )])
        before = populated_kg.snapshot()
        v.verify_candidate_subgraph(candidate)
        assert populated_kg.snapshot() == before

    def test_rejected_candidate_cannot_be_verified(self, rules_file, populated_kg):
        v = PrologVerifier(rules_file)
        candidate = stage_subgraph(
            populated_kg,
            [ProposedOperation.entity("UnknownType", "bad-1")],
        )
        with pytest.raises(StagingError, match="no usable overlay"):
            v.verify_candidate_subgraph(candidate)

    def test_tentative_relation_api_is_deleted(self, rules_file):
        assert not hasattr(PrologVerifier(rules_file), "verify_proposed_relation")


class TestNoContradictions:
    def test_clean_facts_verify(self, rules_file, populated_kg):
        """Seed facts with no contradictions verify as valid."""
        v = PrologVerifier(rules_file)
        v.sync_from_kg(populated_kg)
        result = v.verify_no_contradictions()
        assert result.valid

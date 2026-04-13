"""Prolog verification layer: translates KG state to Prolog facts and verifies.

Bridges the KG (NetworkX) to SWI-Prolog (via pyswip). Each KG entity
and relation becomes a Prolog fact. Domain rules are loaded from .pl files.
Verification checks proposed operations against rules + accumulated state.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pyswip import Prolog

from malleus.kg import KnowledgeGraph, Operation, OpType


def _escape(s: str) -> str:
    """Escape a string for safe use as a Prolog atom.

    Wraps in single quotes and escapes internal single quotes
    to prevent injection (bug fix #7).
    """
    if not isinstance(s, str):
        s = str(s)
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


@dataclass
class VerificationResult:
    """Result of Prolog verification of a proposed KG operation."""
    valid: bool
    rule_violated: str | None = None
    proof_trace: list[str] | None = None


class PrologVerifier:
    """Verifies KG operations against Prolog domain rules.

    Translates KG state to Prolog facts, loads domain rules,
    and checks proposed operations for consistency.
    """

    def __init__(self, rules_path: str | Path):
        self._rules_path = Path(rules_path)
        self._prolog = Prolog()
        self._prolog.consult(str(self._rules_path))
        self._asserted_facts: list[str] = []

    def sync_from_kg(self, *kgs: KnowledgeGraph):
        """Sync KG state into Prolog as facts.

        Accepts one or more KGs (typically static + dynamic).
        Retracts all previous dynamic facts and reasserts from
        all provided KGs. Called before verification.
        """
        self._retract_all()

        for kg in kgs:
            self._sync_single_kg(kg)

    def _sync_single_kg(self, kg: KnowledgeGraph):
        """Sync a single KG's nodes and edges into Prolog facts."""
        for node_id, data in kg._graph.nodes(data=True):
            node_type = data.get("type", "")

            if data.get("cyp_isoform"):
                self._assert_fact(
                    f"enzyme({_escape(node_id)}, {_escape(data.get('name', ''))}, {_escape(data.get('cyp_isoform', ''))})"
                )
            elif not data.get("is_signal") and not data.get("is_event"):
                if node_type == "Drug" or (kg.registry.has_type(node_type) and kg.registry.is_subtype_of(node_type, "Entity")):
                    self._assert_fact(
                        f"drug({_escape(node_id)}, {_escape(data.get('name', ''))}, {_escape(data.get('drug_class', ''))})"
                    )

        for u, v, key, data in kg._graph.edges(data=True, keys=True):
            rel_type = data.get("relation_type", "")
            strength = data.get("inhibition_strength", "").lower() if data.get("inhibition_strength") else "unknown"

            if rel_type == "SUBSTRATE_OF":
                self._assert_fact(f"substrate_of({_escape(u)}, {_escape(v)})")
            elif rel_type == "INHIBITS":
                self._assert_fact(f"inhibits({_escape(u)}, {_escape(v)}, {strength})")
            elif rel_type == "INDUCES":
                self._assert_fact(f"induces({_escape(u)}, {_escape(v)}, {strength})")

    def _assert_fact(self, fact: str):
        """Assert a fact into the Prolog knowledge base."""
        self._prolog.assertz(fact)
        self._asserted_facts.append(fact)

    def _retract_all(self):
        """Retract all dynamically asserted facts."""
        for pred in ["substrate_of", "inhibits", "induces", "drug", "enzyme"]:
            try:
                list(self._prolog.query(f"retractall({pred}(_, _))"))
            except Exception:
                pass
            try:
                list(self._prolog.query(f"retractall({pred}(_, _, _))"))
            except Exception:
                pass
        self._asserted_facts.clear()

    def verify_no_contradictions(self) -> VerificationResult:
        """Check if the current fact base has any contradictions."""
        results = list(self._prolog.query("contradiction(Drug, Enzyme, Type)"))
        if results:
            r = results[0]
            return VerificationResult(
                valid=False,
                rule_violated="contradiction",
                proof_trace=[
                    f"Drug '{r['Drug']}' is both a strong inhibitor and strong inducer of enzyme '{r['Enzyme']}'"
                ],
            )
        return VerificationResult(valid=True)

    def query_interactions(self, drug_id: str) -> list[dict[str, Any]]:
        """Query all interactions where drug_id is the perpetrator."""
        results = list(self._prolog.query(
            f"interaction('{drug_id}', Substrate, Effect, Enzyme, Strength)"
        ))
        return [
            {
                "perpetrator": drug_id,
                "substrate": str(r["Substrate"]),
                "effect": str(r["Effect"]),
                "enzyme": str(r["Enzyme"]),
                "strength": str(r["Strength"]),
            }
            for r in results
        ]

    def query_all_interactions(self) -> list[dict[str, Any]]:
        """Query all interactions in the current fact base."""
        results = list(self._prolog.query(
            "interaction(Perpetrator, Substrate, Effect, Enzyme, Strength)"
        ))
        return [
            {
                "perpetrator": str(r["Perpetrator"]),
                "substrate": str(r["Substrate"]),
                "effect": str(r["Effect"]),
                "enzyme": str(r["Enzyme"]),
                "strength": str(r["Strength"]),
            }
            for r in results
        ]

    def query_polypharmacy_risk(self, substrate_id: str) -> list[dict]:
        """Check if a substrate is affected by multiple perpetrators."""
        results = list(self._prolog.query(
            f"polypharmacy_risk('{substrate_id}', Perpetrators)"
        ))
        if results:
            return [{"substrate": substrate_id, "perpetrators": str(results[0]["Perpetrators"])}]
        return []

    def query_combined_inhibition(self) -> list[dict]:
        """Find cases where two drugs inhibit the same enzyme affecting a substrate."""
        results = list(self._prolog.query(
            "combined_inhibition(Drug1, Drug2, Substrate, Enzyme)"
        ))
        return [
            {
                "drug1": str(r["Drug1"]),
                "drug2": str(r["Drug2"]),
                "substrate": str(r["Substrate"]),
                "enzyme": str(r["Enzyme"]),
            }
            for r in results
        ]

    def verify_proposed_relation(self, *kgs: KnowledgeGraph, source_id: str, target_id: str, relation_type: str, properties: dict) -> VerificationResult:
        """Verify a proposed relation against domain rules.

        Syncs current KG state (static + dynamic), tentatively adds
        the proposed fact, checks for contradictions, then retracts.
        """
        self.sync_from_kg(*kgs)

        strength = properties.get("inhibition_strength", "unknown").lower()
        tentative_fact = None

        if relation_type == "SUBSTRATE_OF":
            tentative_fact = f"substrate_of('{source_id}', '{target_id}')"
        elif relation_type == "INHIBITS":
            tentative_fact = f"inhibits('{source_id}', '{target_id}', {strength})"
        elif relation_type == "INDUCES":
            tentative_fact = f"induces('{source_id}', '{target_id}', {strength})"

        if tentative_fact:
            self._prolog.assertz(tentative_fact)

        result = self.verify_no_contradictions()

        if tentative_fact:
            try:
                self._prolog.retract(tentative_fact)
            except Exception:
                pass

        return result

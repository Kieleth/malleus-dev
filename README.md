# Malleus

[![PyPI](https://img.shields.io/pypi/v/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![Python](https://img.shields.io/pypi/pyversions/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

A root ontology in LinkML, and the opinion that words have power.

## Why this exists

I believe words have power. The closer we work with them, the more carefully we pin down what they mean and how they relate, the closer we get to something a machine can use without guessing. An ontology is that pinning-down, made explicit and machine-readable. Borges and Le Guin understood this long before software did: to name something precisely is to begin controlling it.

The practical bet: if you define your domain once, in an ontology, you can propagate that definition through every layer of a system. LinkML already compiles a schema down to JSON Schema, Pydantic, SQL DDL, OWL, SHACL, TypeScript, whatever you need. So the same five concepts, with the same constraints, can shape the frontend form, the backend validator, the ML training contract, the LLM tool schema, the knowledge graph's node types, and the Prolog rules that reason over them. One source. All layers speaking the same vocabulary.

When that actually happens across a codebase, something unexpectedly useful shows up. Components stop drifting apart. The frontend and backend stop disagreeing about what a "Drug" is. A new contributor learns one vocabulary instead of five. Whole classes of bugs (the ones caused by definitions sliding between modules) just stop existing. Adding a new concept becomes one change in one file, flowing outward through whatever code generators you've wired up.

That's malleus: a small, stable root vocabulary, plus the mechanics to keep everything built on top of it honest.

## The core primitives

Everything in malleus is one of five things:

- **Entity**: something that persists through time. A drug, a server, a person, a concept.
- **Event**: something that happens. A click, a deployment, an interaction detected.
- **Signal**: a derived quality computed from patterns. A risk score, a health status, a trend.
- **Agent**: a mixin capturing the capability to act or decide. Not a class, a trait.
- **Relation**: a typed, directed, reified edge between entities.

Plus four cross-cutting mixins so every typed thing can carry basics without reinventing them: `Identifiable` (id, name), `Temporal` (created_at, updated_at), `Describable` (description, tags), `Statusable` (ACTIVE, INACTIVE, DESTROYED).

Domains extend this root. CYP450 drug interactions, MITRE ATT&CK threat models, both come with examples in this repo. Writing your own is a YAML file.

## Install

```bash
pip install malleus-dev

# Optional SWI-Prolog verification layer:
pip install malleus-dev[prolog]
```

## Quick start

```python
from malleus import OntologyRegistry, KnowledgeGraph

reg = OntologyRegistry("ontology/domains/cyp450.yaml")
kg = KnowledgeGraph(reg)

kg.create_entity("Enzyme", "enz-cyp3a4", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
kg.create_entity("Drug", "drug-sim", {"name": "Simvastatin"})
kg.create_relation("DrugRelation", "rel-001", "drug-sim", "enz-cyp3a4",
                   {"relation_type": "SUBSTRATE_OF"})

# Write-time validation. Nothing wrong reaches the graph.
op = kg.create_entity("NotAType", "x", {})
assert op.op_status.value == "REJECTED"
print(op.rejection_reason)   # "Unknown entity type: 'NotAType'"
```

The `OntologyRegistry` is the constructor parameter for the `KnowledgeGraph`. No registry, no KG. That's the rule, and it's the whole point: the graph can only ever hold things the ontology says exist.

## Distributed convergence

Every `OntologyRegistry` has a deterministic content hash and a fingerprint of atomic facts. Two peers running the same schema produce the same hash, no coordination needed. Two peers running different versions can verify compatibility without exchanging full schemas.

```python
reg = OntologyRegistry("ontology/domains/cyp450.yaml")
print(reg.content_hash())        # 64-char SHA-256, deterministic
print(len(reg.fingerprint()))    # frozenset of atomic facts

result = reg.check_compatibility(foreign_hash, foreign_fingerprint)
# "identical" | "superset" | "subset" | "divergent"
```

Under additive-only evolution (add types, enum values, or slots; relax required to optional), a newer ontology's fingerprint is always a strict superset of an older one's. Peers can tag every write with the hash they used, and receivers can decide: accept (we're compatible), quarantine (we'll understand this after we upgrade), or reject (we've forked, this is a bug).

This matters in fleets running rolling updates. Without it, CRDT sync during the upgrade window can silently drop properties the older node doesn't recognize. With it, the older node says "I can't validate this yet, hold it" and nothing is lost.

## Domain extensions

Two examples ship with the library. Write your own the same way:

```yaml
# your_domain.yaml
id: https://example.org/schema/your_domain
name: your_domain
imports:
  - malleus
  - linkml:types

classes:
  YourEntity:
    is_a: Entity
    slot_usage:
      your_slot:
        required: true
        range: YourEnum

enums:
  YourEnum:
    permissible_values:
      VALUE_A: {}
      VALUE_B: {}
```

## Optional Prolog verification

For domains where logical consistency matters (pharmacology, security, regulatory rules, anything where "can this combination of facts coexist?" is a real question), the `PrologVerifier` syncs the KG into SWI-Prolog and checks proposed writes against a rule file you supply.

```python
from malleus import PrologVerifier

verifier = PrologVerifier("your_rules.pl")
result = verifier.verify_proposed_relation(
    kg,
    source_id="drug-a",
    target_id="enz-x",
    relation_type="INHIBITS",
    properties={"strength": "strong"},
)
if not result.valid:
    print(f"Rule violation: {result.rule_violated}")
    print(result.proof_trace)
```

Verification is read-only. Rejected writes are rolled back from the tentative assertion, never committed. The rule file is yours; the library doesn't ship domain rules.

## Architecture

For the layer-by-layer walkthrough (vocabulary, typed graph, ground truth loading, logic engine, distributed convergence), see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Adoption guides:
- [docs/ONTOLOGY_PROTOCOL.md](docs/ONTOLOGY_PROTOCOL.md): how to add malleus to an existing project
- [docs/KNOWLEDGE_GRAPH_PROTOCOL.md](docs/KNOWLEDGE_GRAPH_PROTOCOL.md): how the ontology shapes the KG

## Tests

```bash
pip install -e .[prolog,dev]
pytest tests/ -v
# 89 tests, ~2 seconds
```

## License

Apache-2.0. See [LICENSE](LICENSE).

## A note on the name

Malleus is the Latin for "hammer". The tool that shapes. Use it to shape your own domains.

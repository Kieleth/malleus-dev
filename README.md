# Malleus

A root ontology in LinkML plus a reference implementation of ontology-typed knowledge graphs with write-time validation and content-addressable hashing for distributed convergence.

## What it is

Five universal primitives (Entity, Event, Signal, Agent, Relation) plus four cross-cutting mixins (Identifiable, Temporal, Describable, Statusable). Domain extensions add typed classes and enums that build on the root. The `OntologyRegistry` is the constructor parameter for the knowledge graph: no registry, no KG. Every write is validated at the boundary.

## Install

```bash
pip install malleus-dev

# Optional Prolog verification layer (requires SWI-Prolog on the system)
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

# Write-time validation: invalid types and enum values are rejected with feedback.
op = kg.create_entity("NotAType", "x", {})
assert op.op_status.value == "REJECTED"
print(op.rejection_reason)   # "Unknown entity type: 'NotAType'"
```

## Ontology hashing and distributed convergence

Every registry has a deterministic content hash and a fingerprint of atomic facts. Two instances can verify compatibility without exchanging full schemas.

```python
reg = OntologyRegistry("ontology/domains/cyp450.yaml")

print(reg.content_hash())        # 64-char SHA-256 hex, deterministic
print(len(reg.fingerprint()))    # frozenset of atomic facts (types, enums, slots, inheritance)

# Check compatibility against another peer's ontology:
result = reg.check_compatibility(foreign_hash, foreign_fingerprint)
# -> "identical" | "superset" | "subset" | "divergent"
```

Under additive-only evolution (adding types, enum values, or slots; relaxing required constraints), a newer ontology's fingerprint is always a strict superset of an older one's. This lets peers in a distributed KG safely exchange operations tagged with their ontology hash: receivers accept what they understand and quarantine what they don't until they upgrade.

## Domain extensions

Two example domain extensions ship with the library. Write your own the same way.

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

## Optional: Prolog verification

For domains where logical consistency matters (pharmacology, security threat modeling, regulatory rules), the `PrologVerifier` syncs the KG into SWI-Prolog and checks proposed writes against a rule file you supply.

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

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a layer-by-layer walkthrough: vocabulary, typed graph, ground truth loading, logic engine, distributed convergence.

Protocols:
- [`docs/ONTOLOGY_PROTOCOL.md`](docs/ONTOLOGY_PROTOCOL.md) — how to adopt malleus in a new project
- [`docs/KNOWLEDGE_GRAPH_PROTOCOL.md`](docs/KNOWLEDGE_GRAPH_PROTOCOL.md) — how the ontology shapes the KG

## Tests

```bash
pip install -e .[prolog,dev]
pytest tests/ -v
# 95 tests pass in ~3 seconds
```

## License

Apache-2.0. See [`LICENSE`](LICENSE).

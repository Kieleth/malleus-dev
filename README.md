# Malleus

[![PyPI](https://img.shields.io/pypi/v/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![Python](https://img.shields.io/pypi/pyversions/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

A root ontology in LinkML, and the opinion that words have power.

## Why this exists

I believe words have power. The closer we work with them, the more carefully we pin down what they mean and how they relate, the closer we get to something a machine can use without guessing. An ontology is that pinning-down, made explicit and machine-readable. Borges and Le Guin understood this long before software did: to name something precisely is to begin controlling it.

The practical bet: if you define your domain once, in an ontology, you can propagate that definition through every layer of a system. LinkML already compiles a schema down to JSON Schema, Pydantic, SQL DDL, OWL, SHACL, TypeScript, whatever you need. So the same five concepts, with the same constraints, can shape the frontend form, the backend validator, the ML training contract, Shelob's tool schema, the knowledge graph's node types, and the Prolog rules that reason over them. One source. All layers speaking the same vocabulary.

When that actually happens across a codebase, something unexpectedly useful shows up. Components stop drifting apart. The frontend and backend stop disagreeing about what a "Drug" is. A new contributor learns one vocabulary instead of five. Whole classes of bugs (the ones caused by definitions sliding between modules) just stop existing. Adding a new concept becomes one change in one file, flowing outward through whatever code generators you've wired up.

That's malleus: a small, stable root vocabulary, plus the mechanics to keep everything built on top of it honest.

Current package boundary: `0.2.0`, `stage-4-structural-staging`. See
[docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md) for implemented
and explicitly pending capabilities. Code can inspect the same boundary through
`malleus.IMPLEMENTATION_STATUS`.

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
```

The Python package contains the logic compiler and verifier. Executing logic checks also requires a `swipl` executable on `PATH`; absence fails explicitly at check time.

## Quick start

```python
from malleus import KnowledgeGraph, OntologyRegistry, ProposedOperation, stage_subgraph

reg = OntologyRegistry("ontology/domains/cyp450.yaml")
kg = KnowledgeGraph(reg)

kg.create_entity("Enzyme", "enz-cyp3a4", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
kg.create_entity("Drug", "drug-sim", {"name": "Simvastatin"})

candidate = stage_subgraph(kg, [
    ProposedOperation.relation(
        "SubstrateOfRelation", "rel-001", "drug-sim", "enz-cyp3a4",
        {"relation_type": "SUBSTRATE_OF"},
    )
])
assert candidate.valid
assert kg.edge_count == 0             # staging never mutates the base graph
print(candidate.candidate_digest)     # binds ontology, base state, and ordered writes
candidate.materialize_into(kg)        # explicit structural materialization

# Write-time validation. No structurally invalid write materializes.
op = kg.create_entity("NotAType", "x", {})
assert op.op_status.value == "REJECTED"
print(op.rejection_reason)   # "Unknown entity type: 'NotAType'"
```

The `OntologyRegistry` is the constructor parameter for the `KnowledgeGraph`. No registry, no KG. That's the rule, and it's the whole point: the graph can only ever hold things the ontology says exist.

`STAGED` means an operation passed validation inside an isolated candidate. `COMMITTED` means it was structurally materialized. Neither means the record is true, epistemically accepted, or authorized for action.

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

One caveat, worth saying plainly. Relaxing a slot from required to optional is additive on the producer side (you're loosening a guarantee) but subtractive on the consumer side (code that hardcoded the field's presence will crash when a new producer omits it). The default `check_compatibility()` answers the producer question: can data flow safely between us? For the consumer question, use `strict_fingerprint()` and `check_compatibility_strict()`, which include required-constraint facts. A relaxation shows up there as divergence, surfacing the risk that would otherwise stay hidden.

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

  YourRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: YourRelationType
        required: true
        equals_string: CONNECTS
      source_id:
        range: YourEntity
      target_id:
        range: YourEntity

enums:
  YourEnum:
    permissible_values:
      VALUE_A: {}
      VALUE_B: {}

  YourRelationType:
    permissible_values:
      CONNECTS: {}

slots:
  your_slot:
    range: YourEnum
```

Relations use concrete classes with explicit source and target ranges. Malleus rejects unknown properties, missing required fields, malformed values, duplicate identifiers, mismatched predicates, and invalid endpoint types before graph mutation.

## Pinned Prolog verification

`GraphFactCompiler` converts any Malleus graph into a fixed typed fact vocabulary. A `LogicContract` pins the ontology hash, exact trusted rule bytes, declared rule IDs, versions, and subprocess wall-clock timeout. `PrologVerifier` evaluates caller-supplied context plus an isolated candidate in a fresh SWI-Prolog process. Stage 5 does not claim that the context is protocol-accepted state.

```python
from malleus import LogicContract, PrologVerifier, ProposedOperation, stage_subgraph

contract = LogicContract.load("your_logic_contract.yaml")
verifier = PrologVerifier(contract)
candidate = stage_subgraph(kg, [
    ProposedOperation.relation(
        "InhibitsRelation", "rel-002", "drug-sim", "enz-cyp3a4",
        {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"},
    )
])
result = verifier.verify_candidate_subgraph(candidate)
if not result.valid:
    for violation in result.violations:
        print(violation.rule_id, violation.violation_code, violation.witness_record_ids)
else:
    # Structural materialization only. This is not epistemic acceptance.
    candidate.materialize_into(kg)
```

The rule program exposes only two required predicates:

```prolog
malleus_rule(RuleId).
malleus_violation(RuleId, ViolationCode, WitnessRecordIds).
```

The verifier enumerates every violation, rejects malformed or unknown witnesses, and never mutates the base graph. Consult errors, timeouts, manifest mismatches, and malformed results raise `LogicExecutionError`; they never become `SATISFIED`. `logic_monitor_failure_records()` converts such a failure into a `MonitorFailure` and a logical `UNKNOWN` assessment. Completed checks can be serialized as content-addressed `LogicCheckRecord` and `ViolationWitness` records.

The package ships the CYP450 contract and rules as an example. Stage 5 accepts only trusted, pinned local rule programs. The timeout bounds the Prolog subprocess wall clock, not graph compilation, output size, memory, or CPU. It does not sandbox untrusted Prolog or issue formal proof certificates.

## Architecture

For the layer-by-layer walkthrough (vocabulary, typed graph, ground truth loading, logic engine, distributed convergence), see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Adoption guides:
- [docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md): the current machine-checked capability boundary
- [docs/ONTOLOGY_PROTOCOL.md](docs/ONTOLOGY_PROTOCOL.md): how to add malleus to an existing project
- [docs/KNOWLEDGE_GRAPH_PROTOCOL.md](docs/KNOWLEDGE_GRAPH_PROTOCOL.md): how the ontology shapes the KG
- [docs/ASSENT_PROTOCOL.md](docs/ASSENT_PROTOCOL.md): how proposals, assessments, decisions, authorization, and replay remain separate

## Tests

```bash
pip install -e .[dev]
pytest tests/ -v
```

## License

Apache-2.0. See [LICENSE](LICENSE).

## A note on the name

Malleus is the Latin for "hammer". The tool that shapes. Use it to shape your own domains.

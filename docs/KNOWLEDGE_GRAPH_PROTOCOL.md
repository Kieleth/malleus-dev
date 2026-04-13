# Knowledge Graph Protocol

How to build a Knowledge Graph that is defined by an ontology, not validated against one.

---

## Core principle: the ontology is the KG's DNA

The ontology does not validate the Knowledge Graph. The ontology **defines** what the Knowledge Graph can be. The KG is an instantiation of the ontology. Without the ontology, the KG cannot exist.

This is the TBox/ABox split from Description Logic:
- **TBox** (terminological box): the schema. Defines concepts, relationships, and constraints. Stable, versioned, changes rarely.
- **ABox** (assertional box): the instances. Contains the actual data. Dynamic, changes constantly.

The TBox is not checked at query time. The ABox can only be written using the vocabulary the TBox defines. An assertion that references a concept not in the TBox cannot even be formulated.

## Two architectures (pick A, never B)

**Architecture A: Ontology defines KG (constitutive)**
```
Ontology (YAML) --generates--> KG type system
                                    |
                                    v
                          KG constructed FROM type system
                          (constructor parameter)
                                    |
                                    v
                          Every write checked as PRECONDITION
                          Invalid writes rejected at point of call
```

The ontology is a constructor parameter. The KG is born with its type system. Invalid data cannot enter. The type system is constitutive: it defines what CAN exist, and nothing else CAN.

**Architecture B: KG validates against ontology (descriptive)**
```
KG exists (freeform) <-- writes data freely
         |
         v (periodic or on-query)
Ontology consulted as external reference
         |
         v
Validation report (after the fact)
```

The KG is independent. The ontology is an external document. Invalid data can temporarily exist. The type system is descriptive: it describes what SHOULD exist, but other things MAY.

**Architecture A is correct. Architecture B is a trap.** It creates a window where invalid data exists, forces post-hoc cleanup, and makes "does the KG conform to the ontology?" a question that should never need asking.

## Principles

### 1. The KG cannot be constructed without an ontology

The ontology is not optional configuration. It is a required constructor parameter. No ontology, no KG. This is not a runtime check that warns; it is a structural impossibility.

```
// Right: ontology is required
KG kg(ontology);

// Wrong: ontology is loaded later
KG kg;
kg.loadOntology(ontology);
```

### 2. Every write is validated as a precondition, not a post-hoc check

When you create an entity, the type must exist in the ontology. When you create a relation, the relation type must exist, and the source/target entity types must match the domain/range constraints. When you set a property, the property must be declared for that entity type.

This happens at the point of the call. Invalid writes are rejected immediately. No invalid data ever materializes in the graph.

### 3. The ontology is immutable after construction

Once the KG is born with its ontology, the ontology cannot be changed in ways that invalidate existing data. It can only grow monotonically:
- Add new entity types (including new subtypes of existing types)
- Add new relation types
- Add new optional properties to existing types
- Add new enum values

It cannot:
- Remove types, relations, or properties that may have instances
- Make optional properties required (existing data may lack them)
- Narrow a range (existing values may not conform)

This is the same constraint Silk enforces via `ExtendOntology` (additive only).

### 4. The ontology generates the KG's type system, not just type definitions

The generation pipeline produces two outputs:

**Output 1: Type definitions** (for compile-time safety)
- C++ structs, enums, to_string/from_string
- Used by application code for type-safe construction

**Output 2: Runtime ontology registry** (for KG construction)
- A data structure containing: all valid type names, inheritance chains, relation types with domain/range, property schemas per type
- Passed to the KG constructor
- Used for write-time validation of string-based operations

Both outputs come from the same YAML source of truth. They are two views of the same ontology: one for the compiler, one for the runtime.

### 5. String API and typed API coexist, both validated

The KG accepts both:
- **Typed API**: `kg.createEntity(EntityType::HUMANOID)` — compile-time safe, impossible to pass an invalid type
- **String API**: `kg.createEntity("Humanoid")` — for dynamic/data-driven use (file loading, LLM commands, scripting), validated against the registry at runtime

Both paths produce the same result. The string API exists for flexibility; the typed API exists for safety. Neither can create invalid data.

### 6. The registry is the single source of truth at runtime

Application code should never hardcode type names, relation types, or property names as string literals. Instead:
- Use generated enums for compile-time references
- Use the registry for runtime introspection ("what types exist?", "what relations can a Humanoid have?", "what properties does a Tree have?")

The registry is queryable: you can enumerate types, check inheritance, discover valid relations for a given type pair. This enables tooling, editors, and AI systems to discover the ontology at runtime without parsing YAML.

## Implementation pattern

### Step 1: Define ontology (YAML)

Per ONTOLOGY_PROTOCOL.md. Your schema imports malleus and defines domain types.

### Step 2: Generate type definitions + runtime registry

The generation script produces:
- Type definition header (structs, enums) — already covered by gen-cpp-header / gen-pydantic
- Runtime registry source file — a data structure encoding the full ontology for KG construction

For C++, the registry is a generated .h/.cpp pair containing:
```cpp
namespace your_project::ontology {

struct OntologyRegistry {
    // All valid entity type names, with parent chain
    // All valid relation types, with source/target type constraints
    // All valid property names per entity type, with value type and constraints
};

// Generated function returning the registry singleton
const OntologyRegistry& registry();

}
```

For Python, the registry is a generated dict or Pydantic model (similar to Shelob's ONTOLOGY dict passed to Silk).

### Step 3: Construct KG with registry

The KG takes the registry as a constructor parameter:
```cpp
auto& reg = your_project::ontology::registry();
KnowledgeGraph kg(reg);
```

Or in Python:
```python
store = GraphStore(instance_id, ontology_json())
```

### Step 4: All writes go through the registry

The KG's write methods check every operation against the registry before materializing:
- `createEntity(type)` — type must exist (or be a subtype of a declared type)
- `createRelation(source, type, target)` — relation type must exist, source/target entity types must match domain/range
- `setProperty(entity, key, value)` — property must be declared for this entity type, value must match range

### Step 5: Extensions are additive only

If a game extends the base ontology (Eden extends Logosphere), it produces its own registry that is merged into the base:
```cpp
auto& base = logosphere::ontology::registry();
auto& ext = eden::ontology::registry();
KnowledgeGraph kg(base, ext);  // merged, extension adds to base
```

The extension can add types, relations, properties. It cannot remove or contradict the base.

## Reference implementations

- **Silk** (Rust): `GraphStore(instance_id, ontology_json())` — ontology as constructor param, write-time validation, quarantine for invalid ops in CRDT sync
- **TypeDB**: `define` block creates the schema, `insert` block creates instances — schema-first, insert fails if type undefined
- **Shelob**: `ONTOLOGY` dict in `store.py` → passed to Silk → all node/edge creation validated against it

## What this is NOT

- It is not OWL reasoning. OWL's Open World Assumption infers rather than rejects. We use Closed World.
- It is not SHACL post-hoc validation. SHACL validates existing data. We prevent invalid data from existing.
- It is not a runtime query the KG makes to an external ontology service. The ontology is inside the KG, not beside it.

---

*See also: ONTOLOGY_PROTOCOL.md for how to define the ontology. This document covers how to use it to construct a Knowledge Graph.*

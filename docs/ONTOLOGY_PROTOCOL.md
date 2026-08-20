# Ontology Protocol

How to adopt the Malleus root ontology in any project.

---

## What Malleus provides

A minimal shared identity and metadata layer. Five core concepts:

| Concept | What it is | BFO/PROV alignment |
|---------|-----------|---------------------|
| **Entity** | Any identifiable thing with a name, timestamps, and description | BFO:Independent Continuant |
| **Event** | Something that happens, with cause chain | BFO:Process Boundary / PROV:Activity |
| **Signal** | A derived quality that emerges from patterns of Events between Entities | BFO:Specifically Dependent Continuant (Quality) / SSN/SOSA:Observation |
| **Agent** | An entity that can act or bear responsibility | PROV:Agent |
| **Relation** | A typed directed edge between entities, reified for metadata | N-ary relation pattern |

Four mixins for cross-cutting traits:

| Mixin | Slots |
|-------|-------|
| **Identifiable** | id, name |
| **Temporal** | created_at, updated_at |
| **Describable** | description, tags |
| **Statusable** | status (ACTIVE / INACTIVE / DESTROYED) |

## How to use it

### Step 1: Create your project schema

```
your-project/
  schema/
    your_project.yaml
```

Your schema imports malleus:

```yaml
id: https://your-project.dev/schema
name: your_project
imports:
  - malleus
  - linkml:types
```

Malleus must be resolvable. Options:
- Place or symlink `malleus.yaml` into the schema directory or one of its parents.
- Pass an explicit local map for an alias, CURIE, or URI import:

```python
registry = OntologyRegistry(
    "schema/your_project.yaml",
    import_map={"malleus:root": "vendor/malleus-0.4.0.yaml"},
)
```

Unresolved imports fail registry construction. Malleus never ignores them.

### Step 2: Extend, don't redefine

Your domain entities extend `Entity`:

```yaml
classes:
  MyDomainThing:
    is_a: Entity
    description: A thing specific to my domain.
    slots:
      - my_custom_property
```

Your domain events extend `Event`:

```yaml
classes:
  DeploymentEvent:
    is_a: Event
    slot_usage:
      event_type:
        range: DeploymentEventType  # constrain to your enum
```

Your agents apply the `Agent` mixin:

```yaml
classes:
  Bot:
    is_a: Entity
    mixins:
      - Agent
    slot_usage:
      agent_type:
        range: BotType
```

Your domain signals extend `Signal`:

```yaml
classes:
  TrustSignal:
    is_a: Signal
    slot_usage:
      signal_type:
        range: TrustSignalType
      algorithm:
        range: TrustAlgorithm
      perspective:
        required: true  # trust is always subjective
    slots:
      - trustor
      - trustee

  HealthSignal:
    is_a: Signal
    slot_usage:
      signal_type:
        range: HealthSignalType
      perspective:
        required: false  # health can be global
```

Signals are dependent continuants — they must reference a bearer via `bearer_id`. They are computed, not asserted: the `algorithm` slot names the computation, and `computed_at` records when the value was last derived. The value is ephemeral — recomputable from the underlying Events at any time.

Your domain relations use one concrete class per predicate. The class fixes the predicate and narrows both endpoint ranges:

```yaml
enums:
  MyRelationType:
    permissible_values:
      DEPENDS_ON: {}

classes:
  DependsOnRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: MyRelationType
        required: true
        equals_string: DEPENDS_ON
      source_id:
        range: MyDomainThing
      target_id:
        range: MyDomainThing
```

Do not multiplex predicates with different endpoint signatures through one generic relation class. Concrete classes make the source and target contract inspectable and enforceable.

### Step 3: Constrain loose slots

Malleus intentionally leaves `event_type`, `agent_type`, `relation_type`, and `signal_type` as strings. Your project MUST constrain these to project-specific enums:

```yaml
enums:
  MyEventType:
    permissible_values:
      CREATED:
      UPDATED:
      DELETED:

classes:
  MyEvent:
    is_a: Event
    slot_usage:
      event_type:
        range: MyEventType
```

This is the three-layer pattern in action:
- Layer 1 (Malleus): vocabulary with string ranges
- Layer 2 (your project): semantic constraints via enums and domain/range
- Layer 3 (Malleus runtime): required fields, closed properties, value shape, identifiers, and endpoint ranges
- Layer 4 (your application): domain rules, evidence policy, acceptance, and authorization

### Step 4: Generate code

For C++ projects:
```bash
gen-cpp-header schema/your_project.yaml --namespace your_project::ontology
```

For Python projects:
```bash
gen-pydantic schema/your_project.yaml
```

For TypeScript:
```bash
gen-typescript schema/your_project.yaml
```

### Step 5: Validate

```bash
linkml-validate -s schema/your_project.yaml your_data.yaml
gen-shacl schema/your_project.yaml  # generate SHACL shapes
```

## Rules

1. **Never redefine Malleus types.** Extend them. If Entity doesn't have what you need, add slots via `slot_usage` or create a subclass.

2. **Never add domain-specific concepts to Malleus.** If it's not universal across all projects, it belongs in your project schema. Push things UP only when two or more projects independently need the same concept.

3. **Constrain string slots.** Malleus uses `range: string` for extensibility. Your project MUST narrow these to enums or specific types.

4. **Mixins for cross-cutting concerns.** Don't force traits into the class hierarchy. If something applies across unrelated classes (like "has a position" or "has health"), make it a mixin in your project schema.

5. **Keep it shallow.** The research says: a class with a single subclass is suspicious. Don't create depth for the sake of depth.

6. **Treat `COMMITTED` narrowly.** It means a write passed structural validation and materialized. It does not establish truth, epistemic acceptance, or permission to act.

## Current adopters

| Project | Schema | Extends |
|---------|--------|---------|
| Logosphere | `schema/logosphere.yaml` | Entity, Event, Agent, Relation |
| Shelob | `src/shelob/schema/shelob.yaml` | Entity, Event, Agent, Relation, Signal (health) |
| Mycelia | `docs/infrastructure/trust.md` | Entity, Event, Agent, Signal (trust) |

## File structure

```
malleus/
  schema/
    malleus.yaml          # root ontology (source of truth)
  ONTOLOGY_PROTOCOL.md    # this file
  research_ontology_best_practices_March2026.md
```

## Adoption: a duplicate that is not an error

Rule 2 asks you to push a concept up once two projects need it independently.
Until 0.13.4 that request was an outage: the loader treated every duplicate
name as a collision, so the moment the root adopted a concept a domain had
already named, the domain stopped loading. Not degraded, stopped.

A duplicate is still a collision by default. It is an adoption when the
downstream definition says so and already agrees with the upstream one:

```yaml
slots:
  locator:
    range: string
    annotations: {adopts: true}
```

Both halves are load-bearing. The declaration is a human saying these are the
same concept, which no machine can check: `recon` and `ocr` both declare
`confidence` as a float and mean opposite things, a reviewer's judgment against
a provider's uncalibrated number. The structural check is the machine refusing
a declaration that is wrong about the parts it can see, naming the field that
disagrees.

Adoption keeps the upstream definition. Description and annotations are
excluded from the comparison, because a machine cannot judge prose. Slots only:
a class or enum that exists upstream is reused by importing it.

The declaration is not part of the content hash. Adopting a name changes no
structural fact, and if it did, declaring an adoption would re-anchor every
ledger, which is absurd for a statement that two definitions already agree.

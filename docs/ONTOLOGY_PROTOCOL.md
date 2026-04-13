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
- Symlink `malleus.yaml` into your schema directory
- Add malleus to your LinkML import path
- Use a local imports map

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
- Layer 3 (your application): cardinality, required fields, closed shapes

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

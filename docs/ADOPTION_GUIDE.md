# Malleus Adoption Guide

How to bring malleus into a project and keep it alive while the project grows.

Written for two readers at once: a human building a project, and the coding
assistant working with them. If you are the assistant, this file is your
operating manual. Read it fully, then follow the contract at the end.

---

## The idea in three sentences

Define every domain concept once, in one YAML file, with its fields, allowed
values, and relationships. Generate or construct everything else from that
file: validators, typed classes, form schemas, tool definitions, the knowledge
graph's type system. The graph can only ever hold what the schema allows, so
modules cannot drift apart, because there is nothing to drift from except one
shared definition.

That is the whole trick. The rest of this guide is how to do it and how to
keep doing it after week one, which is where most projects fail.

## Pick your level

Malleus is a ladder. Climb only as high as your project needs. Most projects
stop at level 2 or 3.

| Level | What you get | What you use | Use it when |
|-------|-------------|--------------|-------------|
| 1 | Shared vocabulary | Your YAML schema + LinkML code generators. No malleus runtime. | You want one source of truth for types across frontend, backend, and data. |
| 2 | Typed knowledge graph | `OntologyRegistry` + `KnowledgeGraph`. Every write checked before it lands. | You keep domain state in a graph and want invalid data to be impossible, not cleaned up later. |
| 3 | Atomic batches | `stage_subgraph()` + candidates | A claim needs several records at once and half-written state is unacceptable. |
| 4 | Domain rules | `LogicContract` + `PrologVerifier` | Your domain has invariants worth machine-checking ("a drug cannot strongly inhibit and strongly induce the same enzyme"). |
| 5 | Decision records | Assent protocol, accepted-graph replay | You must prove later who accepted which change, under which policy, and what the graph said at any past moment. |

The internal names for these levels live in `docs/IMPLEMENTATION_STATUS.md`
(levels 2 through 5 are stages 2, 4, 5, and 6/7 there). You do not need the
internal names to use the ladder.

One warning before you pick: level 5 is heavy machinery for audit-grade
decisions. If you are building a game, a tool, or an app, you almost certainly
want levels 1 to 3. Do not let the top of the ladder scare you off the bottom.

## Day one

### 1. Get the root schema

Two options. Installing the package gives you the schema plus the runtime:

```bash
pip install malleus-dev
```

```python
from malleus import bundled_ontology_path
root = bundled_ontology_path("malleus.yaml")   # works from source tree or installed wheel
```

Or vendor it: copy `ontology/malleus.yaml` into your repo (Logosphere does
this, at `schema/malleus.yaml`). Vendoring works for non-Python projects.
Record which malleus version you copied.

While you are here: `malleus-inquisitor install-skills --project .` gives
your coding assistant the `malleus-acolyte` skill, which carries this
guide's playbook as standing orders and can self-check your adoption at any
point. Everything below still applies; the skill just keeps it at hand.

### 2. Create your project schema

```
your-project/
  schema/
    your_project.yaml
```

```yaml
id: https://your-project.dev/schema
name: your_project
imports:
  - linkml:types
  - malleus
```

When you want a template, copy `ontology/domains/cyp450.yaml` from the
malleus repo: it is the fully worked example (loader, seed data, executable
rules). `attack.yaml` is a declaration-only shape example and says so in
its description.

The import must resolve. Either the malleus file sits next to yours, or you
pass an explicit map:

```python
from malleus import OntologyRegistry, bundled_ontology_path

registry = OntologyRegistry(
    "schema/your_project.yaml",
    import_map={"malleus": str(bundled_ontology_path("malleus.yaml"))},
)
```

### 3. Extend, never redefine

Everything in malleus is one of five things. Your concepts subclass them:

- **Entity**: a thing that persists. A drug, a server, a character, an invoice.
- **Event**: a thing that happens. A deployment, an attack, a payment.
- **Signal**: a quality computed from events. A risk score, a health status.
- **Agent**: a trait (mixin) for anything that can act or decide.
- **Relation**: a typed, directed edge between entities, itself a record with an id.

```yaml
classes:
  Creature:
    is_a: Entity
    slots:
      - species

  TamesRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: YourRelationType
        required: true
        equals_string: TAMES
      source_id:
        range: Character
      target_id:
        range: Creature
```

One concrete class per relation predicate. The class pins the predicate name
and narrows what can sit at each end. Do not funnel five different predicates
through one generic relation class; you lose the endpoint contract.

### 4. Constrain the loose strings

Malleus leaves `event_type`, `agent_type`, `relation_type`, and `signal_type`
as plain strings on purpose. Your schema must narrow every one you use to an
enum. An unconstrained string slot is a hole in the fence.

### 5. Wire it in

Level 1, generate code and stop:

```bash
gen-pydantic schema/your_project.yaml     # Python classes
gen-typescript schema/your_project.yaml   # TypeScript types
gen-json-schema schema/your_project.yaml  # form/API validation
```

Level 2, construct the graph from the registry:

```python
from malleus import KnowledgeGraph

kg = KnowledgeGraph(registry)   # no registry, no graph. That is the rule.
op = kg.create_entity("Creature", "cr-001", {"name": "Direwolf", "species": "wolf"})
assert op.op_status.value == "COMMITTED"
```

A rejected write comes back with the reason (`op.rejection_reason`). That
reason is feedback, not an obstacle. Fix the data, or extend the schema if the
data was right and the schema was behind.

## A real layered example

Logosphere shows the chain working across four layers, each importing the one
below and only adding:

```
malleus.yaml          five primitives, four mixins. Never edited by games.
  logosphere.yaml     game-engine vocabulary: materials, physics, lights
    earth.yaml        a setting pack: trees, grass, rock, small fauna
      eden.yaml       one game: narrative entities, mythological relations
```

Eden's import block says exactly what it borrows and why:

```yaml
imports:
  - linkml:types
  - logosphere
  # Earth-like vocabulary is a SETTING PACK, not core.
  # This game grows things, so it asks.
  - earth
```

A concept moves down a layer only when a second consumer needs it. That is the
promotion rule, and it works in both directions of the stack.

## The playbook: keeping it alive

Adoption is not the hard part. The hard part is month two, when code moves
fast and the schema quietly stops being true. These are the situations that
come up and what to do in each. Assistant: these are standing orders.

**The human names a new domain concept in conversation or code.**
Check the schema first. If it is there, use the existing name, even if the
human used a synonym; surface the schema name. If it is missing, propose the
schema addition before writing the code that needs it. The YAML change comes
first, the code second. Never invent a type name in code only.

**A new field appears on an existing concept.**
If it describes the domain (a creature's diet, a drug's half-life), it goes in
the schema. If it is plumbing (a cache key, a render handle), it stays in
code. When unsure, ask one question: would a second module ever care? Domain
data in code-only fields is how drift starts.

**Two modules disagree about what a term means.**
The schema is the tiebreaker. Fix the definition there, regenerate, and let
the compiler or validator surface every place that was relying on the old
meaning. Do not negotiate the meaning locally in one module.

**Someone wants to rename or delete a type.**
Schema evolution is add-only: new types, new optional fields, new enum values.
You cannot remove or narrow what may already have instances. To retire a
concept, add its replacement, migrate writers, and mark the old one
deprecated in its description. Deleting definitions breaks every graph and
peer that was built on them.

**A write gets rejected.**
Read the reason. It names the exact violated constraint. Two valid responses:
the data was wrong, fix the data; or the data was right and the schema is
behind, extend the schema. There is no third option. Bypassing the registry,
even once, even in a test, ends the guarantee the whole system rests on.

**The same concept shows up in a second project.**
That is the signal to push it down a layer (project schema to shared pack, or
pack to root). One consumer is project-specific. Two independent consumers is
shared vocabulary. Do not push down speculatively before the second consumer
exists.

**An LLM is writing to the graph.**
Let it reason freely, then make it commit conclusions only through typed
operations. Feed rejections back to it verbatim; models correct course well
when told exactly which constraint they violated. If it keeps producing valid
insights the schema cannot express, that is not noise. Log those, review them
weekly, and grow the schema where they cluster.

**Nothing has changed in a while.**
Run the drift check: list the domain nouns in recent code and commits, and
check each exists in the schema. Nouns in code but not schema are unmanaged
concepts. Either promote them or consciously rule them out as plumbing. This
takes minutes and catches the silent divergence everything else here exists
to prevent.

## Rules that do not bend

1. Never redefine a malleus root type. Extend it.
2. Never put project-specific concepts in the root. Push down only on the second consumer.
3. Every string type-slot you use gets an enum.
4. One concrete relation class per predicate.
5. All writes go through the registry-backed graph. No side doors.
6. Schema changes are add-only once instances exist.
7. Keep the hierarchy shallow. A class with one subclass is a smell.
8. `COMMITTED` means the record's shape was valid, nothing more. Whether it is
   true, trusted, or safe to act on is a separate question, answered at level
   4 or 5, or by your application. Do not let "it is in the graph" mean "it is
   true" anywhere in your code or prose.

## Contract for the assistant

When a project points you at malleus, this is your job, stated once:

Before writing code that touches a domain concept, read the project schema.
When the human introduces a concept, propose schema first, code second. When
validation rejects, repair data or propose a schema extension, never a bypass.
When you see domain data living only in code, say so. When a concept earns a
second consumer, propose promotion. Keep the human honest about rule 8. And
when the schema and the code disagree, the schema wins until the human
changes the schema.

You are not the ontology police. You are the gardener. The goal is that six
months in, the schema still describes the project and everything still
compiles from it.

## Going deeper

- `docs/ONTOLOGY_PROTOCOL.md`: the full schema-authoring reference.
- `docs/KNOWLEDGE_GRAPH_PROTOCOL.md`: why the ontology constructs the graph instead of validating it.
- `docs/ARCHITECTURE.md`: the layer-by-layer walkthrough.
- `docs/ASSENT_PROTOCOL.md` and `docs/IMPLEMENTATION_STATUS.md`: levels 4 and 5, when you need them.
- `README.md`: runnable quickstart for levels 2 and 3.

# Fresh-session v2 population task

You are the sole population producer for one frozen experiment. Read only these five files:

1. `task.md`
2. `inputs/ontology.yaml`
3. `inputs/generic-recipes.stottr`
4. `inputs/competency-questions.json`
5. `/Users/luis/Projects/malleus-dev/.claude/worktrees/paper-v4-multimodel/private/paper-v4-text-layer/selected-reading.json`

Do not inspect any other file, directory, conversation, tool output, network resource, query binding, answer key, earlier ontology or population, manuscript, plan, ledger, test, source code, or model transcript. Do not delegate. Write only `population.json` in this directory. Use the Write tool to create it. Do not modify an input.

## Goal

Propose the smallest ontology-conforming population that the selected reading directly supports and that is useful for the four competency questions. The questions guide selection only. Their `required_semantics` entries do not authorize a type, property, or distinction absent from the ontology.

Use only prose blocks in the selected reading. Figures and tables are excluded. Do not modify the ontology or recipes. Do not invent a required value, entity, count, distinction, relation, or epistemic status. Missing ontology semantics must remain missing.

In particular:

- Do not represent a campaign as an observation method or a network as one physical instrument.
- Do not expand an aggregate instrument count into invented individual instruments.
- Do not encode a count, location, direction, relationship, causal clause, epistemic qualifier, or several facts inside `name`.
- Do not turn a proposed or preferred mechanism into an unqualified causal relation when the ontology cannot preserve that epistemic status.
- Use `name` only as a short noun phrase that denotes the record. It must not carry a fact that lacks a corresponding typed property or relation.
- Use opaque sequential ids such as `urn:malleus:paper-v4:v2:record:001`. An id must not disclose an answer value or source phrase.

An incomplete population is a valid proposal if it is the smallest faithful result under the ontology. If no nonempty valid population can be produced without invention, use the refusal form below.

## Success object

Write one strict UTF-8 JSON object with exactly these top-level fields:

- `schema`: exactly `malleus.paper-v4.population/v2`
- `ontology_sha256`: exactly `sha256:7fad8b9e9480781dd2207725d9c8d9906742c61988f1acbfa7883c2a55a16015`
- `reading_sha256`: exactly `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`
- `records`: a nonempty array of record objects

Every `record_id` must be unique and match `urn:malleus:paper-v4:v2:record:` followed by a three-digit ordinal. In array order, ids must start at `001` and increase without gaps. Every `block_id` must exactly equal a block id in the selected reading.

An entity record has exactly:

- `record_id`
- `record_type`
- `record_block_id`, supporting the record's existence and classification
- `properties`, an object containing exactly the fields required below, each wrapped in an object with exactly `value` and `block_id`

A relation record has those fields plus:

- `source`, with exactly `record_id` and `block_id`
- `target`, with exactly `record_id` and `block_id`

Each endpoint id must name an entity in this population. Its locator must support that relation and direction. Do not emit `relation_type`; its recipe fixes that ontology enum. Use JSON numbers for numeric properties and JSON strings for all other properties. No value may be null, blank, an array, a Boolean, or an object other than the declared wrappers.

## Constructible entity types

- `SeismicInstrument`: `status`
- `SeismicEvent`: `hypocenter_depth`, `location_quality`
- `RidgeSegment`: `segment_class`, `spreading_rate`
- `RockSample`: `lithology`, `volatile_concentration`
- `GeologicalProcess`: `process_kind`
- `status` is the imported Malleus root slot; its permissible values are `ACTIVE`, `INACTIVE`, `DESTROYED`.

Every enum-valued property must use one exact permissible value declared for that property in `inputs/ontology.yaml`. For an exact numeric observation, use the same finite JSON number for both bounds. Do not convert or normalize a source unit.

## Constructible relation types

- `InstrumentDetectedEventRelation`: source `SeismicInstrument`, target `SeismicEvent`
- `EventLocatedBeneathSegmentRelation`: source `SeismicEvent`, target `RidgeSegment`
- `SampleCollectedFromSegmentRelation`: source `RockSample`, target `RidgeSegment`
- `ProcessCausesEventRelation`: source `GeologicalProcess`, target `SeismicEvent`

Every relation has an empty `properties` object because its `relation_type` is fixed by the recipe. Do not emit an extra property, an abstract type, a type outside these lists, a dangling endpoint, or a reversed endpoint.

## Refusal object

If no nonempty success object can be produced without invention, write one strict JSON object with exactly:

- `schema`: exactly `malleus.paper-v4.population-refusal/v2`
- `reason`: one nonblank string

Write no prose or code fence outside the JSON file.

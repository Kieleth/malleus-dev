# Fresh-session document population task

You are the sole population producer for one frozen experiment. Work only from these four inputs:

1. `inputs/ontology.yaml`
2. `inputs/generic-recipes.stottr`
3. `inputs/competency-questions.json`
4. `/Users/luis/Projects/malleus-dev/.claude/worktrees/paper-v4-lean/private/paper-v4-text-layer/selected-reading.json`

Do not inspect any other file, directory, conversation, tool output, network resource, query binding, manuscript, plan, ledger, old experiment, model transcript, or answer key. Do not delegate. Do not write files. Return only the delimited JSON requested below.

## Goal

Propose the smallest ontology-conforming population that captures the selected reading well enough for the four competency questions. You choose every record, identity, value, and relation from the allowed ontology. The recipes define construction shapes only. They do not prescribe how many records to create.

Use only prose blocks from the selected reading. Figures and tables are out of scope. Do not modify the ontology or recipes. Do not invent a required value. If the reading does not support the required population, return the refusal form.

## Output object

Return one JSON object with exactly these top-level fields:

- `schema`: exactly `malleus.paper-v4.population/v1`
- `ontology_sha256`: exactly `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`
- `reading_sha256`: exactly `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`
- `records`: a nonempty array of record objects

Every `record_id` must be a unique nonblank string chosen by you. It is graph identity, not a quotation, so it needs no locator. Every `block_id` must exactly equal a block id present in the selected reading.

An entity record has exactly:

- `record_id`
- `record_type`
- `record_block_id`, supporting the record's existence and classification
- `properties`, an object whose values each have exactly `value` and `block_id`

A relation record has the same fields plus:

- `source`, with exactly `record_id` and `block_id`
- `target`, with exactly `record_id` and `block_id`

Each relation endpoint `record_id` must name an entity in the same population. Its `block_id` must support the asserted relation. Do not emit `relation_type`; the relation recipe fixes it from the ontology.

Use JSON numbers for numeric properties and JSON strings for other properties. No value may be null, blank, an array, or an object other than its `value` and `block_id` wrapper.

## Allowed record types and exact property sets

- `Campaign`: `name`
- `Region`: `name`
- `EarthquakePopulation`: `name`
- `PrimaryMeltPopulation`: `name`
- `ObservingSystem`: `name`, `instrument_kind`
- `BoundedQuantity`: `quantity_kind`, `lower_value`, `upper_value`, `unit`, `quantity_status`
- `MechanismHypothesis`: `initiating_condition`, `transformation`, `physical_effect`, `stress_context`, `outcome`
- `DataAcquisitionRelation`: `instrument_count`, `data_kind`, plus source `Campaign` and target `ObservingSystem`
- `SpatialAssociationRelation`: `relative_position`, plus source any allowed entity and target `Region`
- `QuantityCharacterizationRelation`: no variable properties, plus source `BoundedQuantity` and target any allowed entity
- `HypothesisExplainsRelation`: no variable properties, plus source `MechanismHypothesis` and target `EarthquakePopulation`

`quantity_status` must be `REPORTED_OBSERVATION` or `CALCULATED_ESTIMATE`. The ontology and recipe fix a `MechanismHypothesis` as `PREFERRED`; do not repeat that property in the population.

Do not emit an extra property, a type outside this list, a dangling endpoint, or a relation whose endpoint direction differs from the list. Do not collapse two source claims into one value merely to reduce record count.

## Response

On success, return exactly:

`BEGIN_POPULATION_JSON`

the JSON object

`END_POPULATION_JSON`

If you cannot produce the object without inventing required data, return exactly:

`BEGIN_POPULATION_REFUSAL`

one JSON object with exactly `schema` equal to `malleus.paper-v4.population-refusal/v1` and a nonblank `reason`

`END_POPULATION_REFUSAL`

No prose or code fence may appear outside the delimiters.

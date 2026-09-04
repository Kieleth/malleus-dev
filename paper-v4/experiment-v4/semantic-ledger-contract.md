# Semantic-ledger contract for the v4 run

Status: paper-owned design note for the next experiment. This is not an
experiment result, a Core contract, or a change to the selected v2 evidence.

## The missing distinction

An ontology defines the legal domain language. It does not define what one
accepted change means. Ledger mechanics define retention, admission, and
replay. They do not choose whether a change represents a source assertion, a
version of world state, an event, or an economic commitment.

The `DomainHistoryProfile` makes that choice explicit. The population plan then
states the records proposed under that choice, with field-level source
derivations and typed gaps. The ledger records the accepted change. Replay
projects current graph state according to the selected profile.

```text
packs + project ontology       legal vocabulary
DomainHistoryProfile           meaning of one change
capture + PopulationPlan       source-grounded proposal
policy + KnowledgeChangeSet    commitment decision
ledger + replay                accepted history and current projection
```

These are separate contracts. Passing compilation and replay proves that the
contracts executed consistently. It does not prove that the ontology was
adequate, the capture was exhaustive, or the source was true.

## The two current consumers

| Question | Paper document | Small Shop |
| --- | --- | --- |
| Selected profile | `source-assertion` | `state-version` |
| Semantic unit | One atomic composition of assertions captured from an identified source | One version of a domain state record |
| Vocabulary | Optional research, metrology, and chronology packs plus project terms | Small Shop project ontology |
| Source evidence | Exact reading, captured verbatim assertion, block locator, modality, attribution | Exact source rows and mapping evidence |
| Domain time | Optional lexical evidence on each assertion for an event, observation, or sample | Source occurrence order such as `e4`, then `e7` |
| Assertion time | Optional lexical evidence on each retained assertion | Not the semantic unit |
| Change valid time | `ORDER_ONLY` with the capture id, meaning capture/import order | Domain valid time, such as `e4`, then `e7` |
| Transaction time | When Malleus admits the proposal | When Malleus admits each state version |
| Correction | A later assertion and any formalized record explicitly supersede their predecessors | A later state record explicitly supersedes the earlier version |
| Retraction | Not admitted by the shipped profile | Outside the frozen correction example |
| Current graph | Accepted formalized records selected by the source-assertion projection rule | Latest non-superseded state records |
| Retained history | Earlier assertions, evidence, records, and supersession links remain inspectable | Both `B/Y/1@e4` and `B/Y/2@e7` remain; only `e7` is current |

The selected document profile fixes origin as `PARTIAL_IMPORT`, genesis as one
retained partial import, and completeness as the declared capture only. It does
not claim that the graph or capture is a complete account of the wider domain.
The capture census reports which reading blocks were reviewed and how many
captured assertions were fully, partly, or not formalized.

## No epistemic flattening

The source-assertion profile creates one additional obligation. Suppose the
captured clause says that the authors hypothesize that process X causes event
Y. The capture can retain `HYPOTHESISED` while the population creates an
ordinary `CAUSES_EVENT` relation. If replay exposes only that unqualified edge,
the graph has flattened a claim about a hypothesis into an apparent domain
fact.

The design space contained three queryable representations:

1. Every projected record licensed by a source assertion carries its modality
   and attribution.
2. Replay projects a reified Claim with modality and an explicit link to the
   domain statement.
3. Modality remains in retained evidence, and the public read boundary exposes
   a typed graph-to-assertion provenance join.

An optional ontology mixin is not an enforcement rule. P6 selects the third
representation. The capture retains modality, and
`trace_population_record` joins an accepted replayed record to the exact
assertion that licensed it. A paper query that reports epistemic status must
include that trace. A bare domain edge is not enough.

## What the three prior producers established

The retained v3 comparison changes only the proposal producer. Its artifact
summary reports:

| Producer | Ontology entity/relation classes | Population records | Query rows, CQ1 to CQ4 |
| --- | ---: | ---: | --- |
| gpt-5.6-sol | 15 / 33 | 13 | 0, 2, 4, 0 |
| Claude Opus 5 | 20 / 18 | 6 | 0, 0, 0, 1 |
| Claude Sonnet 5 | 8 / 8 | 2 | 0, 0, 0, 0 |

Every run admitted and replayed a 23-event history, and every guarded query
reported zero forbidden access attempts. The graph differences therefore do
not diagnose ledger failure. They show that the vocabulary and the meaning of
population were under-specified before admission. Packs address repeated
vocabulary. The history profile addresses what a change means. Neither removes
the need for source-grounded inspection.

The retained population-session reports name the concrete failure. Sonnet and
Opus both refused to invent point values where the source reports ranges. They
also omitted the preferred causal mechanism because their ontologies could not
carry its hypothesis status. Sonnet additionally refused to turn an aggregate
instrument count into invented instruments. In the old runs those choices
appeared only as missing records plus a later self-report. In v4 they must become
typed `INTERVAL_NOT_EXPRESSIBLE`, `MODALITY_NOT_EXPRESSIBLE`, or
`AGGREGATE_ONLY` gaps tied to source locators. A gap makes the loss inspectable;
it does not repair the ontology or authorize a guessed fact.

## Execution gate

Core's full public `DomainHistoryProfile`, population, ontology-revision,
replay, graph-read, and provenance-trace path is verified through commit
`573c45b82725d6f444b70e5ff193302dac883e7b`, tree
`6704031dea824572b4d7163ba477c33175397fe7`. The selected profile is
`source-assertion` at
`sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5`.
The public
`trace_population_record` read follows a replayed record through its accepted
change, population plan, history profile, field derivations, and retained
source and evidence bytes. This realizes the third no-flattening option above:
the paper can join a graph row to its source assertion and modality without
adding assertion metadata to every domain record. It does not make the graph
edge self-qualifying, so paper queries that report epistemic status must execute
and display that verified join.

The v4 document run still waits for the remaining Core pieces that implement
the approved experiment rather than another paper-local brief:

- the grounded metrology, chronology, and research packs;
- the nascent-project skill playbook.

Until those pieces are frozen, paper work may refine the run manifest,
isolation checks, and manuscript explanation. It must not create v4 population
facts, rebind the selected v2 result, or claim that the new profile executed.

## Accepted KISS cut

The lean candidate is one document, one default single-session v4 loop, and no
more than the revision rounds produced naturally by typed gaps. The existing
three-producer comparison remains diagnostic background and does not need to be
rerun under v4 for the first paper. The staged-session variant and a new
multi-producer matrix can move to follow-on work.

The author accepted this cut in E-0100. It is the active v4 execution boundary.

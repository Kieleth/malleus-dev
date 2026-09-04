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
| Semantic unit | One dated, attributed assertion from an identified source | One version of a domain state record |
| Vocabulary | Optional research, metrology, and chronology packs plus project terms | Small Shop project ontology |
| Source evidence | Exact reading, captured verbatim assertion, block locator, modality, attribution | Exact source rows and mapping evidence |
| Domain time | Time stated by the document for an event, observation, or sample | Source occurrence order such as `e4`, then `e7` |
| Assertion time | The date attached to the source assertion | Not the semantic unit |
| Transaction time | When Malleus admits the proposal | When Malleus admits each state version |
| Correction | A later assertion and any formalized record explicitly supersede their predecessors | A later state record explicitly supersedes the earlier version |
| Retraction | A superseding assertion with modality `NEGATED`; no destructive erase | Outside the frozen correction example |
| Current graph | Accepted formalized records selected by the source-assertion projection rule | Latest non-superseded state records |
| Retained history | Earlier assertions, evidence, records, and supersession links remain inspectable | Both `B/Y/1@e4` and `B/Y/2@e7` remain; only `e7` is current |

The paper still needs an explicit origin choice for the selected document run.
`SNAPSHOT` may overstate capture completeness. `PARTIAL_IMPORT` is safer unless
the implemented profile defines snapshot scope as the identified reading and
the census makes its limited coverage explicit. The run must record the chosen
value before ontology construction.

## No epistemic flattening

The source-assertion profile creates one additional obligation. Suppose the
captured clause says that the authors hypothesize that process X causes event
Y. The capture can retain `HYPOTHESISED` while the population creates an
ordinary `CAUSES_EVENT` relation. If replay exposes only that unqualified edge,
the graph has flattened a claim about a hypothesis into an apparent domain
fact.

The full profile must select and enforce one queryable representation:

1. Every projected record licensed by a source assertion carries its modality
   and attribution.
2. Replay projects a reified Claim with modality and an explicit link to the
   domain statement.
3. Modality remains in retained evidence, and the public read boundary exposes
   a typed graph-to-assertion provenance join.

An optional ontology mixin is not an enforcement rule. The selected contract
must either preserve the qualification or refuse the proposal before
admission. The minimum test begins with one `HYPOTHESISED` capture and proves a
qualified replay query or the typed refusal.

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

## Execution gate

Core P3 is verified at final tip
`add4535f757551b6ed30b449e19c31fc97769e1e`, tree
`df2c0b7acafc44ff2d45ed9195d13b73577b0979`. It exposes contract compilation,
neutral population compilation, governed admission, reopen, replay, and graph
query through `malleus.compiler`.

The v4 document run still waits for the later Core pieces that implement the
approved experiment rather than another paper-local brief:

- the document-assertion adapter;
- replay across an ontology supersession and typed revision policy;
- the full `DomainHistoryProfile` contract;
- the grounded metrology, chronology, and research packs;
- the nascent-project skill playbook.

Until those pieces are frozen, paper work may refine the run manifest,
isolation checks, and manuscript explanation. It must not create v4 population
facts, rebind the selected v2 result, or claim that the new profile executed.

## KISS cut for author review

The lean candidate is one document, one default single-session v4 loop, and no
more than the revision rounds produced naturally by typed gaps. The existing
three-producer comparison remains diagnostic background and does not need to be
rerun under v4 for the first paper. The staged-session variant and a new
multi-producer matrix can move to follow-on work.

This is a provisional scope recommendation. It does not change the master plan
until the author accepts it.

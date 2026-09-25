# Temporal representation: what each option provides

2026-09-24. Research and recommendation, awaiting author decision.
Implementation remains paused. No database, schema, API or policy is selected.

Forward note: the author requested worked cross-flow experiments before deciding.
GEDANKENEXPERIMENTS-01.md and STORAGE-FLOWS-01.md now challenge this recommendation.
It is not an approved implementation direction.

## Correction to the previous choice

The A/B question in NEXT-STAGE.md was under-specified. It mixed three decisions:

1. **Meaning and identity:** what assertion does a value belong to, and how can
   a calculation name the exact assertion it used?
2. **Temporal semantics:** how do accepted changes determine applicability and
   historical answers? Who enforces that interpretation?
3. **Representation and storage:** ordinary graph records, temporal properties,
   indices, or a different physical backend?

An identified version need not be a node. A native temporal property can expose
an exact version handle. Conversely, adding version nodes and four timestamps
does not give an ordinary graph correct bitemporal queries automatically.

The research supports combining qualified assertions with Core-owned temporal
queries. It does not establish that Malleus needs a new storage engine now.
That is a proposed design conclusion, not an implemented result.

## One example, the same obligation for both

Use the already authored price control, not a new experiment:

- K1: accept r1, reporting 750 cents from 1 May, with no stated end.
- K2: accept r2, reporting a real transition to 800 cents from 12 May.
- K3: accept r3, correcting the earlier 1 May to 12 May price to 775 cents.

These are successive accepted knowledge positions, not measurement dates. The
known-open period is part of the authored account, not proof about the future.

| Question | Required answer |
|---|---|
| What applied on 5 May, according to K1? | 750, referring to r1 |
| What applied on 5 May, according to K3? | 775, referring to the correction |
| What applied on 15 May, according to K3? | 800, unchanged by the correction |
| What did the old calculation use? | Its original exact 750 premise, not a redirected reference |

All assertions remain queryable at K3. A selected answer does not discard the
other versions. Closure metadata must also respect the selected knowledge
position: K1 cannot disclose the ending learned at K2 or the correction at K3.
The four applicability cells in NEXT-STAGE.md are derived accounts of three
source assertions. They do not require four source statements, four LLM outputs
or four copies of every product property.

## A: explicit qualified assertion/version records

An illustrative graph has a stable product linked to identified price
assertions. Each assertion carries its value and unit and references its source,
account and applicability. A correction points to what it corrects. A calculation
points to its exact premise and selection context. These are design roles, not
a newly specified Malleus ontology.

This makes the object of explanation explicit: "this source asserted this
price in this context", rather than merely "this product has three prices".
Whole entity snapshots are optional. A price assertion need not copy the
product's name, address or unrelated properties.

**Provides:** normal graph traversal of evidence, corrections and calculations;
natural grouping of qualifications; ordinary graph export of the full account.

**Does not provide by itself:** interval closure, historical reconstruction,
same-time joins, selection of one account, or temporal rule evaluation. Leaving
each adopter to write date filters would leave the central requirement unmet.

**Cost:** additional graph structure and traversal. Core must define which
records belong to its optional temporal profile, how they are validated, and
how ordinary domain queries avoid treating the history as simultaneous facts.
Core must not silently add arbitrary domain classes or wrap every literal.

## B: temporal properties and edges built into the graph interface

The stable product has a price property with multiple qualified versions. The
graph interface understands history and selection at a knowledge position and
domain time. An exact version handle can identify the premise of a calculation;
whether that handle is exported as a node is a separate choice.

**Provides:** a uniform place for temporal operations, compact selected-value
queries, and independently changing properties without whole entity copies.
Temporal matching can express simultaneous or sequential relationships rather
than reconstructing the intended time semantics separately in every query.

**Does not provide by itself:** evidence qualifications, source authority,
distinguishing a hypothesis from a report, uncertainty interpretation, or an
immutable premise-reference contract. Those remain explicit model obligations.
For example, versioning a numeric value and its unit independently must not
permit combining a new value with an incompatible old unit.

**Cost:** a temporal value model and corresponding query, export, validation and
rule-input contracts. This is a larger change if introduced inside today's
ordinary KnowledgeGraph, but it need not replace the ledger or require a new
database. A temporal query layer over derived assertion records is also possible.

## What the inspected sources establish

These are different kinds of evidence, not competing products in a benchmark.
No external system was installed or timed. Documentation was inspected on
24 September 2026; the graph paper describes a research model/prototype.

| Source | Established by the inspected text | Transfer to Malleus and limit |
|---|---|---|
| [W3C n-ary relation note](https://www.w3.org/TR/swbp-n-aryRelations/), Pattern 1 | A relation instance can be an identified object with several participants and qualifications. | Useful for one coherent qualified assertion; not a temporal engine or an endorsement of one ontology. |
| [Wikibase conceptual model](https://www.mediawiki.org/wiki/Wikibase/DataModel), statements and scope | Statements have values, qualifiers and references; the conceptual model is distinct from physical implementation. | Keep meaning separate from storage. This does not establish immutable Malleus version identities. |
| [Wikibase RDF format](https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format), statement types and representation | Full statements are nodes with qualifiers/references; simplified direct values also exist, but their selection ignores qualifiers. | Full and compact views can coexist. Malleus must not copy the qualifier-blind shortcut for temporal use. |
| [Rost et al., TPGM+](https://dbs.uni-leipzig.de/files/research/publications/2021-11/pdf/Rost_2021_Bitemporal%20Property%20Graphs%20to%20Organize.pdf), sections 3, 4.2 and 6 | Bitemporal property versions, history and temporal predicates; avoids whole-element copies for property changes; prototype uses relational storage. | Time-aware graph semantics do not dictate physical storage. Exact premise identity and epistemic context need separate Malleus contracts. |
| [XTDB resolution design](https://xtdb.com/blog/building-a-bitemp-index-2-resolution), append-only log and resolution sections | The log retains updates and valid periods; system-end boundaries are derived during resolution rather than supplied in each input. | Do not make producers maintain all historical cells. This is database implementation evidence, not a graph model or authority-resolution policy. |
| [XTDB time documentation](https://docs.xtdb.com/about/time-in-xtdb.html), system and valid time | Separates system history from domain applicability, including retrospective and future-effective changes. | Useful operational distinction. Malleus still needs explicit unknowns, account selection and exact ledger checkpoints. |

Do not infer that an unspecified date applies forever. Do not infer source
truth from database membership. Do not use latest arrival to adjudicate
independent sources. The sources do not settle those Malleus requirements.

## Comparison against our use cases

The table is design analysis based on the sources and inspected local code,
not a claim that either complete option already exists in Malleus.

| Requirement | Explicit records alone | Native temporal interface | What Malleus must own regardless |
|---|---|---|---|
| Keep all versions | Straightforward identified records | Versioned values/edges and history access | Replay closure and stable references |
| Inspect evidence for one premise | Ordinary graph links | Version handle plus evidence representation | Exact assertion, evidence and interpretation binding |
| Ask both time questions | Needs a selector | First-class responsibility | Defined applicability and knowledge coordinates |
| Keep queries simple | Extra hops unless a view is supplied | Selected properties can look ordinary | Qualified view, never an unlabelled historical union |
| Join two values for one calculation | Easy to combine incompatible records accidentally | Temporal operators help, but query scope still matters | Same account/context and relevant time compatibility |
| Correct past knowledge | Additional records are representable; selection is not automatic | Correction semantics can be built in | Distinguish correction from world transition |
| Preserve unknown time and competing accounts | Flexible modelling space | Must be represented beyond ordinary interval defaults | No invented dates or silent authority choice |
| Avoid copying unchanged data | Fine-grained records/shared payloads possible | Per-property versions possible | Coherent assertion boundaries and atomic changes |
| Efficient repeated queries | Indexable | Indexable, with time-aware execution opportunities | Measure representative workloads before choosing a backend |

A temporal edge also needs a declared meaning. A relationship describing two
coexisting domain objects differs from a correction or provenance link between
accounts. Imposing temporal overlap on every edge would break legitimate
historical explanations. Conversely, allowing arbitrary cross-time joins would
break same-time calculations. Node-versus-property choice does not resolve this.

## Fit to the inspected Malleus checkout

Isolated branch `codex/core-temporal`, base
`ebff70f72dc4cd67b2f910b88575e558a2824728`, with prior local T2 changes.
The following are source observations, not results from a new runtime test:

- [PRINCIPLES.md](../../docs/PRINCIPLES.md) already states a ledger-derived
  temporal history and a separately resolved valid-time view.
- [knowledge.py](../../src/malleus/_contract_pipeline/knowledge.py),
  KnowledgeRecordHistory and `_apply_change`, retains old operations separately
  but removes superseded records from the ordinary graph. Its replacement rule
  requires a later INSTANT and cannot express our correction of the ended
  earlier period. Neither representation is obtained by only relaxing that rule.
- [kg.py](../../src/malleus/kg.py), `query`, `get_node` and `get_relation`,
  exposes ordinary record properties, not independently time-selected versions.
- [logic.py](../../src/malleus/logic.py), GraphFactCompiler.compile, compiles
  graph snapshots into facts by record identity. Feeding the full historical
  union into current-state rules would change their meaning. Required temporal
  check scopes must be specified under either representation.
- T2's local `replay_at` is an exact prefix read, not a domain-time selector.
  Separate Assent temporal facilities already exist, including
  [valid_time.py](../../src/malleus/valid_time.py). Reuse requires semantic
  compatibility; this memo does not claim temporal support is absent everywhere.

Inference from these observations: explicit qualified records with a Core
selector offer the narrower first implementation boundary. Native properties
inside the existing graph would affect more ordinary consumers. This is a
change-surface assessment, not an effort estimate or performance measurement.

## Recommendation for approval

**Specify identified assertions and native temporal selection semantics first.
Implement the first projection using ordinary graph records, with one ledger
authority and no second accepted-state writer.**

Here "native" means Malleus owns and enforces the temporal operation. It does
not mean a new database or a temporal list hidden inside every existing property.
The proposed optional profile would provide:

1. A full, graph-queryable qualified history, including old exact assertions.
2. A Core-selected view at an explicit knowledge position, domain time and
   account/context, with traceable source assertions and unresolved cases.
3. Exact premise references for calculations and checks. A simpler selected
   value must remain connected to its qualified account.
4. Closure derived from admitted changes. Producers declare supported temporal
   meaning, not hand-maintained transaction end times or generated history cells.

This combines A's explicit explanation structure with B's ownership of temporal
queries. It is one interpretation with two views, not two independently writable
graphs, a compatibility fallback or two competing selection algorithms.

Adopting a specific generic assertion shape still needs the P1 contract and
author review. Value, unit, uncertainty, evidence and application must stay
coherent where their meaning depends on each other; a node per scalar is not
required. Domain ontology changes must be declared, never injected silently.

## Evidence still needed before implementation or broader adoption

The next deliverable is P1, not a runtime patch: exact representation, accepted
operation meanings, selector results/refusals, premise identities and actual
check-input scope for the three existing controls. Do not silently extend this
approval into general interval splitting or multi-authority arbitration.

Then RED tests must fail on old-premise redirection, future metadata leakage,
incorrect past correction, incompatible temporal joins and fabricated unknown
dates. A separate positive case must retain a legitimate cross-time evidence
link. GREEN must pass the independently authored answer key and the required
real checks, not merely compare two implementations with each other.

Only after semantic correctness should a differently shaped temporal backend
be assessed against the same observations and measured workload. No backend
performance or replaceability result exists yet. Neither ordinary nodes nor
native temporal properties, on their own, prove source faithfulness.

## Research retention and scope

The source comparison is retained through the public Recon API in ignored
`private/temporal-bitemporal-recon/`, extending the earlier research pass without
changing its records. New source, axis and boundary records distinguish
documentation claims from Malleus requirements. Structural validation of that
research ledger is not validation of this architectural recommendation.

Skill influence: the maintainer skill keeps the proposal OPTIONAL_PROFILE,
Python a REFERENCE_IMPLEMENTATION, controls CONFORMANCE_FIXTURE candidates and
domain authority ADOPTER_CHOICE. Recon keeps source evidence, inferred transfer
and unestablished capabilities separate. Nothing is promoted automatically.

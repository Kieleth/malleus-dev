# Delimitations

What malleus reuses, what it rejects, what it must be measured against, and what
it can honestly claim. This is the guard rail against reinventing the wheel,
for this repo and for every project building on it. It is also the evidence
base for the paper's related-formalisms section.

Research verified against primary sources in August 2026. Unverified items are
listed at the end, not silently mixed in.

---

## The comparison axis

Passive description and post-hoc validation are common, but they are not
universal. TypeDB, Stardog guard mode, RDF4J ShaclSail, TerminusDB, Fluree, and
Blue Brain Nexus all gate some writes. Malleus cannot distinguish itself by
saying that other systems only validate later.

The narrower comparison is the complete lifecycle: ontology-bound
construction, isolated content-addressed candidates, checks under pinned
contracts, a protocol state between structural validity and epistemic
acceptance, bitemporal application, and replay from one ledger authority.
Independent work establishes each ingredient and corroborates the direction.
The candidate contribution is their protocolized composition, the explicit
boundaries between them, and the behavior measured when the whole protocol
runs.

## Five foundations to inherit explicitly

Independent groups reached each ingredient before or alongside Malleus. That
is useful confirmation and a source of tested techniques. The paper should
inherit all five explicitly, cite them, and state what Malleus learned from
each:

1. **Write gating exists.** TypeDB fails non-conforming inserts and terminates
   the transaction. Stardog's ICV guard mode fails any transaction that would
   violate constraints. GraphDB and RDF4J's ShaclSail validate on commit and
   roll back on violation. TerminusDB schema-checks every commit. Fluree
   enforces SHACL at transaction time. Rejecting writes nonconforming to a
   configured structural contract is established engineering, not a Malleus
   invention.
2. **The bitemporal semantics are SQL:2011's, adopted deliberately.**
   Application time (valid time) vs system time (transaction time), half-open
   intervals, retroactive changes visible only in later transaction views.
   Canonical citation: Kulkarni and Michels, SIGMOD Record 41(3), 2012. XTDB
   v2 (GA 2025) implements full automatic bitemporality on the same model.
3. **Ledger as authority with a rebuilt projection is established.**
   Database recovery and state-machine replication predate Malleus. Fowler
   documented the Event Sourcing pattern; Kreps unified logs for replication
   and integration; Kleppmann made log-derived materialized views explicit.
   The JSONL ledger and NetworkX projection reuse that architecture.
4. **Semantic streams and event-sourced KGs exist.** Linked Data Event Streams
   publishes append-only immutable RDF members. Blue Brain Nexus persists KG
   changes through an event log and rebuilds graph and search projections.
   Event Knowledge Graphs and ActiveGraph also derive graph structure from
   event histories.
5. **Content-addressed RDF subgraphs exist.** Kuhn and Dumontier (ESWC 2014)
   defined hash-embedded identifiers at the RDF-graph level. A nanopublication
   assigned a trusty URI can be content-addressed, but trusty URIs are
   recommended rather than mandatory in the nanopublication model. Fluree
   content-addresses commits; TerminusDB commits are immutable delta layers;
   git and IPLD are generic ancestors.

## Protocol and empirical contribution hypotheses

With those foundations explicit, the survey sharpens five composition
hypotheses and the empirical results needed to support them:

- **The composition.** The reviewed systems cover substantial subsets. Blue
  Brain Nexus independently demonstrates a strong pre-2026 log-to-KG
  architecture. LDES confirms semantic append-only publication. ActiveGraph
  confirms deterministic agent log-to-graph replay and, through its later
  *Regimes* preprint, proposal, evaluation, gating, and promotion loops. These
  systems support the direction and offer mechanisms and tests to acquire. No
  exact match has been found in the current set for Malleus's combination of
  portable contracts, isolated candidates, ontology-bound evidence, requested
  review under an independence policy, epistemic acceptance, bitemporal
  application, evolution, and ledger replay. This is a bounded finding, not
  proof of absence.
- **Ontology as a portable artifact, injected at construction.** Several
  validating stores reviewed here keep schema as database-resident state
  managed through their own DDL, including TypeDB definitions, Stardog
  constraint sets, and TerminusDB schema documents. Current Malleus loads an
  external LinkML-shaped YAML file into an `OntologyRegistry`, which is the
  constructor parameter. Accepted future design makes pinned LinkML 1.11.1 the
  replaceable first-party frontend and compiles to a frontend-neutral effective
  contract. No current registry, no current graph.
- **Content-addressing applied to pre-commit candidates.** Nanopubs bind
  content to identity at publication; Fluree and TerminusDB address committed
  history. No exact match found in the current comparison set stages a
  not-yet-committed candidate subgraph whose digest binds ontology hash, base
  state, and ordered writes through an acceptance workflow.
- **Hash-pinned rule contracts.** The rules lineage, including SWRL, SPIN,
  SHACL-AF, and SPARQL 1.2 RL, treats rules as inference producers or
  constraint bodies.
  No exact match found in the current comparison set gives a rule set a pinned
  identity, binds that identity into the check record, and evaluates it against
  isolated candidates.
- **The structural/epistemic split as first-class protocol state.** The
  current comparison set has not yielded an exact database or KG match for a
  state machine between "structurally valid and recorded" and "accepted
  knowledge" (PROPOSED, ACCEPT, REJECT, DEFER, CONTEST). Palantir's Action
  approvals and git staging and review are workflow analogs. TMS and ATMS are
  conceptual predecessors for assumptions, justifications, dependencies,
  contradiction, and belief revision, not direct analogs of this review state
  machine. Nanopublication assertion and provenance provide another partial
  structural analog. Their authority and semantic boundaries differ, so this
  remains a candidate composition claim, not unoccupied ground.

## Formalism by formalism

Verdict vocabulary: **Reuse** (Malleus consumes it directly), **Reject**
(deliberate design refusal, with grounds), **Inherit** (independent convergence
or an established mechanism that grounds Malleus and needs an explicit paper
paragraph), **Note** (one line suffices).

Words such as "closest" and "strongest" below are rankings only within the
current comparison set. They identify the most useful systems to learn from.

### Semantic web standards

| Formalism | Status (Aug 2026) | Verdict |
|---|---|---|
| OWL 2 | Rec since 2012; DL reasoning niche in industry | **Reject.** Open world plus no unique-name assumption: a missing required property is "unknown," not a violation. Fifteen years of integrity-constraint literature (Tao and Sirin, AAAI 2010) documents that OWL natively cannot do closed-world checking. LinkML's gen-owl gives interop for free. |
| SHACL Core | Rec 2017; SHACL 1.2 Core still Working Draft (Aug 2026) | **Inherit.** SHACL defines validation over an RDF data graph and a validation report. The data graph may be an in-memory candidate; the Recommendation does not prescribe persistence timing or an admission lifecycle. Malleus binds candidate identity, validation, review, and assent into one protocol. |
| SPARQL 1.2 RL | W3C Working Draft, 26 Aug 2026 | **Inherit + watch.** Specifies Datalog-style RDF inference with stratified negation-as-failure. It does not assert global closed-world semantics, define an admission gate, content-address a rule set, or record firing provenance. Moving target: recheck at submission. |
| ShEx | CG report 2019, never Rec-track | **Note.** Defines shape conformance, not an admission lifecycle. It can also be applied before persistence. LinkML has gen-shex. |
| SWRL, SPIN | Legacy; SPIN formally superseded by SHACL | **Note.** Lineage material only. |
| N3 + EYE reasoner | CG report 2023; EYE very active | **Note.** Rules-as-data in a live non-Rec ecosystem; open-world defaults. |
| RDF 1.2 (RDF-star) | Concepts and Semantics at Candidate Rec, April 2026 | **Inherit** for future claims work. `rdf:reifies` standardizes referring to a proposition without asserting it. Malleus claim design must answer "why not RDF 1.2 reifiers": packaging of multi-record units, typing, and the write gate. |
| Named graphs + PROV-O | RDF 1.1 datasets; PROV-O Rec 2013, stable | **Reuse (map onto).** Staged candidates are named-graph-shaped; acceptance events are PROV activities. PROV is passive vocabulary; malleus makes the structure a condition of materialization. |
| LinkML | Active, 1.11.1 (May 2026) | **Reuse, foundational future frontend.** Current core directly interprets LinkML-shaped YAML through `OntologyRegistry`; it does not execute official LinkML semantics. Accepted design pins 1.11.1 as the replaceable first-party frontend and compiler baseline, with a LinkML-free effective contract boundary. LinkML itself supplies no Malleus admission lifecycle. |

### Validating and versioned stores

| System | Mechanism | Verdict |
|---|---|---|
| TypeDB 3.x | Hard write gating against rich types; rule inference removed in 3.x in favor of explicit functions | **Inherit.** Strongest established gating mechanism in this comparison set. No temporal model, no portable schema artifact, no staging, no acceptance layer, no replayable ledger. |
| Stardog ICV guard mode | Opt-in per-database; violating transactions fail | **Inherit.** Real commit-time gating since the 2010s. Constraints are DB-resident; no staging, no digests, no protocol. |
| GraphDB / RDF4J ShaclSail | SHACL validation on commit, exception on violation | **Inherit.** Same family; SHACL subset limits; opt-in bolt-on. |
| TerminusDB | Closed-world git-like graph DB: every commit atomic and schema-checked, immutable layers, branch/diff/merge, time travel. Stewardship to DFRNT 2025, v12 current | **Inherit, closest composite system.** Individual paragraph required in the paper. Lacks valid-time bitemporality (version time-travel only), acceptance distinct from commit, portable schema artifact, pinned rule contracts. |
| Fluree | Signed transactions on immutable ledger, content-addressed commits, SHACL at transaction time | **Inherit, second-closest composite.** Same gaps: no valid time, no acceptance state, no pre-commit candidate addressing. |
| Neo4j / GQL / SQL-PGQ | ISO GQL published 2024; Neo4j whole-graph GRAPH TYPE is a 2026.02 preview, not production | **Note.** The mainstream property-graph world is only now standardizing schema. |
| Datomic | Log of immutable facts, derived indexes, transaction time only | **Note.** No valid time, attribute-level schema only. |
| XTDB v2 | Full automatic bitemporality on SQL:2011 lines, log-centric, schema-free | **Inherit.** Established temporal semantics for Stage 7b to reuse deliberately. Schema-free and gate-free: any write materializes; one commit event where Malleus has two. |
| Wikidata / Wikibase | Statement model with qualifiers, references, ranks; constraints advisory, never blocking | **Inherit** for claims work. Operating proof that claims-with-context scale, and the established answer (ranks, deprecation, supersession) that a Malleus claim design must match or map to. The constraint-violation backlog is the documented cost of soft constraints. |

### Semantic logs, event graphs, and extraction systems

| System | Mechanism | Verdict |
|---|---|---|
| RDF Stream Processing, including C-SPARQL, CQELS, and RSP-QL | Time-annotated RDF streams, continuous queries, windows, reporting policies, and formal result semantics | **Inherit.** Confirms the semantic-stream direction and contributes an explicit evaluation-policy boundary for future streaming projections. It does not provide a durable evidence-admission ledger. |
| Linked Data Event Streams 1.0 | Append-only immutable RDF members; version, order, transaction, shape, view, and retention terms | **Inherit.** Confirms semantic append-only publication and supplies a possible future publication or synchronization projection. It is not an evidence-admission or deterministic-projector protocol. |
| Blue Brain Nexus | Append-only global event history, event sourcing, SHACL-gated resources, revisions, historical reconstruction, graph and search projections | **Inherit, strongest pre-2026 systems convergence.** Requires an individual paper paragraph. It validates the log-to-KG architecture while leaving Malleus to compose proposal, review, assent, temporal, and evolution boundaries. |
| Event Knowledge Graphs | Events, entities, correlations, and directly-follows edges | **Inherit.** Confirms event-history-to-KG representation. Declarative source-to-EKG mapping needs its own cited source beyond the foundational 2021 EKG model. |
| SLOGERT | Automatically extracted log templates whose instances are instantiated or expanded into ontology-grounded RDF through OTTR | **Inherit.** Reuse its extraction and modular-template lessons. It does not supply Malleus's acceptance and replay authority. |
| OntoLogX | Learned raw-log extraction into ontology-grounded per-event KGs with syntax, SHACL, and semantic validation, iterative correction, and persist-only-valid gating | **Inherit and acquire technique.** Independently confirms ontology-guided extraction, typed checking, retry, and a commit gate. Malleus composes candidate identity, requested review and assent, bitemporal application, and ledger replay around that loop. |
| ActiveGraph, *The Log is the Agent* | Authoritative append-only agent log, deterministic typed graph fold, causal lineage, replay, fork, and diff | **Inherit, May 2026 preprint.** Independently confirms agent log-to-graph replay. Its ontology-bound evidence, epistemic-review, evolution, temporal, and integrity boundaries differ. |
| ActiveGraph, *Regimes* | Typed candidate patches, static checks, sandbox execution, in-sample evaluation, held-out validation, and logged promotion or discard | **Inherit, June 2026 preprint.** Independently confirms proposal, evaluation, gating, promotion, and replayable improvement as separate stages. Malleus tests a different complete lifecycle around them. |

### Claims, evidence, templates, mathematics

| Prior art | What it settled | Verdict |
|---|---|---|
| Nanopublications | Assertion/provenance/pubinfo package; ecosystem conventions for supersession and retraction by reference; active 2026 ecosystem; optional trusty URI integrity | **Inherit, strongest claims-work convergence in this set.** A nanopublication assigned a trusty URI can be content-addressed. The base model does not require that identity, typed closed-world admission, or an ordered acceptance protocol. Adopt or map to the three-part split rather than inventing a new one. |
| Micropublications | Claim + support/challenge argumentation down to evidence and methods (2014, dormant) | **Note.** Cite for claim/challenge links. |
| SEPIO / GA4GH VA-Spec | Assertion, Evidence Line, Evidence Item; typed profiles over a generic core; VA-Spec 1.0 balloted 2025 | **Inherit** for evidence structure. Exchange schema, no store, no gate. Its profile method is what LinkML-based Malleus would replicate; say so. |
| TMS, ATMS, and DISK | Assumptions, justifications, dependency tracking, retraction, inconsistent contexts, and evolving hypotheses | **Inherit.** Doyle and de Kleer ground tracked assumptions and justification-aware revision. Malleus composes those lessons with its ledger, provenance, bitemporality, and ontology evolution. |
| OTTR templates | Parameterized, typed, recursively expanded graph templates; industrial use; TGDK 2024 | **Inherit, strongest recipe convergence in this set.** Accepted design selects stOTTR 0.1.4 as the sole authored GraphRecipe v0 representation, expanded under the restrictive Malleus profile into target-neutral construction facts and then existing staging and assent. Only research-local GE-000 through GE-020 exist; no GraphRecipe capability ships. |
| OpenMath / Content MathML / OMDoc | Formula encoding with dictionary semantics; MathML 4 nearing CR (PR targeted Oct 2026) | **Reuse.** Inventing a formula encoding is the actual reinvention risk. Encode formulas in OpenMath or Content MathML; malleus adds the typed binding and the gate. |
| Wikidata P2534/P7235/P9758, MaRDI | Formulas resident in a KG with symbols linked to entities | **Inherit.** The binding half exists; Wikidata's property model does not itself define or execute a formula-evaluation protocol. |
| Wikifunctions | Definitions in a wiki KG executed by external evaluator backends; typed function-call and object validation; Wikidata access through 2026 | **Inherit.** Typed validation exists and provides a useful implementation reference; Malleus composes a different ontology-bound evidence-admission lifecycle around typed records. |
| Wolfram | Curated knowledgebase evaluated in-language | **Note.** Proprietary monolith, not formula-as-graph-data. |
| Event sourcing / CQRS | Append-only log as authority, rebuildable projections (Fowler 2005, Young 2010) | **Reuse.** Name the pattern, cite it, list what it lacks: gating, valid time, acceptance, content-addressed candidates. |
| Trusty URIs, git, IPLD | Content addressing of published artifacts | **Reuse (nearest relative: trusty URIs).** Delimit on staging vs publication. |

### Commercial landscape (Aug 2026)

The ontology-as-common-language thesis is commercially live and VC-amplified:
a16z published "The Palantirization of Everything" (Jan 2026) describing the
wave. Palantir Foundry's Ontology (object types, link types, Action types
with approval workflows) is the template. RelationalAI raised $75M (Dec 2025,
Snowflake Ventures) for a knowledge-graph coprocessor inside Snowflake.
Startups in the wave: Distyl AI ($175M Series B at $1.8B, Sept 2025, Palantir
alumni), Enhans (Seoul, ontology-based "AI OS," Samsung among 30+ clients,
Naver-backed), TextQL, Cognee, OntologyStudio, Algorix, Cerenovus, plus a
mid-market cluster (Adaptrix, DataWalk, itemis ANALYZE, One Data). Ontotext
and Semantic Web Company merged as Graphwise.

Matterhaul belongs on this list and is the company that motivated this map:
founded 2025, San Francisco, founder and CEO Shawn Razek. Pitch: an AI-native
platform for the physical-goods supply chain (manufacturers, distributors,
dealers) that sits above existing systems, unifies their data into one
intelligent layer, and runs AI agents for quoting, order entry, procurement,
and dispatch. Industry-association affiliations (NAW, ISA) indicate real
distribution-industry customers. Funding stage reported as Series A by the
author; not verified against a public source in this pass. Same verdict as
the rest of the wave: unified-semantic-layer thesis, no published mechanism
resembling a gated store or acceptance protocol.

No exact match was found in the reviewed public descriptions for the complete
Malleus composition of a gated store, one ledger authority, bitemporal
acceptance, and a portable constructor-bound contract. This is a limited audit
of published mechanisms, not evidence that the mechanism space is unoccupied.
Palantir's Action approvals deserve one sentence as a product-workflow analog
of the structural/epistemic split.

## Guardrails for future design

Standing orders for anyone (human or assistant) designing the planned
extensions. Each names what must be engaged before designing, what to adopt,
and what the actual contribution is.

**Claims and assumptions.**
Engage first: Doyle's TMS, de Kleer's ATMS, nanopublications, Wikidata
ranks/supersession, SEPIO/VA-Spec, DISK, and RDF 1.2 reifiers. Adopt the
assertion/provenance/pubinfo decomposition, explicit justifications and
dependencies, and a rank-or-supersession mechanism mapped into Malleus's
primitives. The candidate contribution is composition with typed admission,
ledger replay, provenance, bitemporality, and ontology evolution, not the
assumption primitive.

**Mathematical formulas.**
Engage first: OpenMath/Content MathML, Wikidata's defining-formula properties,
MaRDI, Wikifunctions. Adopt: an existing formula encoding; do not invent one.
Contribution: typed formula nodes whose symbol bindings are validated at write
time against the ontology, plus an execution contract where an external
engine reads formula + bound KG state and results return to the graph with
provenance. No exact match for that full loop has been found in the current
comparison set.

**Axioms and domain rules as data.**
Engage first: SHACL shapes-as-data, SPARQL 1.2 RL (WD, moving), and N3.
Adopt: representation mappable to SHACL/SRL rather than a bespoke rule
vocabulary. Contribution: the pinned-contract lifecycle (rules as gated,
versioned, hash-identified KG citizens whose acceptance is itself
ontology-checked), not the rule formalism.

**KG as state.**
Engage first: OpenCitations snapshot chains, RDF archive systems, Wikibase
revisions, XTDB. These version the past. Contribution: staged candidate
future states, content-addressed, admitted through an acceptance gate.

**Recipes (reusable subgraph patterns).**
The representation decision is made: stOTTR 0.1.4 is the sole authored
GraphRecipe v0 representation. A restrictive profile expands it into
target-neutral construction facts before existing staging and assent. SPARQL
CONSTRUCT and ontology design patterns remain comparison and interoperability
material, not alternative v0 authored syntaxes. GE-000 through GE-020 are
research-local; no GraphRecipe runtime ships.

## Paper checklist

Systems requiring an individual delimitation paragraph: TerminusDB, Fluree,
Stardog guard mode, TypeDB, XTDB, nanopublications, OTTR, Blue Brain Nexus,
RDF Stream Processing, Linked Data Event Streams, Event Knowledge Graphs,
OntoLogX, and both ActiveGraph preprints.

The paper should place novelty in the composed protocol and its empirical
results, while presenting the pieces below as inherited foundations:

- Do not say "nothing prevents invalid data from entering a store." The
  validating stores above confirm that write gating works and provide
  implementation experience to reuse.
- Treat SQL:2011 and XTDB as the foundation for the bitemporal mechanics.
- Treat event sourcing as the foundation for ledger authority and rebuilt
  projections.
- Treat LDES, Nexus, Event Knowledge Graphs, and ActiveGraph as independent
  confirmation that semantic append-only streams and event-history-to-KG
  projection are sound directions.
- Treat trusty URIs as the foundation for content-addressed RDF subgraphs.
- "Malleus encodes reality." Knowledge representation is a scoped surrogate
  carrying explicit ontological commitments.
- Describe current ledger integrity as local chain validation with optional
  caller-supplied checkpoints. `current()` may bind the complete selected
  prefix; historical `.as_of()` may bind both its selected prefix and,
  separately, its containing ledger. A selected historical prefix alone does
  not authenticate later tail records. Core retains no checkpoint store and
  supplies no external head witness, signature, trusted timestamp,
  transparency-log monitor, or complete projection-closure manifest. External
  witnessing belongs as a modular integrity-profile extension. Changing its
  persisted grammar may require a wire epoch, not a redesign of the semantic
  protocol.
- "A triple is the universal event." Contract facts are triple-shaped; protocol
  events and atomic candidate subgraphs carry different boundaries.
- Present any formula encoding, claim packaging, or template language as an
  adoption, restriction, or composition of established work unless a separate
  result supports a narrower claim.

Contribution candidates supported by the current survey: the composition;
ontology as a portable constructor-required artifact; content-addressed
pre-commit staging; hash-pinned rule contracts; the structural/epistemic
acceptance split. Their contribution depends on how they interact inside the
protocol and what the complete system demonstrates empirically, not on being
first individually.

## Deliberate boundaries (decided, not accidental)

Structural rejections are not protocol data. A refused write is recorded as
an `Operation` with `op_status=REJECTED` and a full `rejection_reason` in
the local `KnowledgeGraph.operations` audit, and a refused candidate
aggregates its reasons on `CandidateSubgraph.rejection_reason`. Those
records are execution-local: they never enter the ledger, and the accepted
projection carries no memory of what was refused. This is deliberate. The
ledger commits what was proposed and decided; what a caller attempted and
was structurally refused is that caller's diagnostic, observable at the
call site, not a protocol commitment. A future rejection-record capability
would need its own authority story before it belongs in the ledger.

## Unverified residuals

Stated so they are not silently absorbed as fact:

- RDFox: SHACL supported since v5 (2024), integrated with its incremental
  reasoner; whether it aborts transactions on violation was not established.
  Characterize as on-demand validation until verified.
- TerminusDB's core and schema checker being implemented in SWI-Prolog is
  prior knowledge, not verified this pass. Verify before the paper mentions
  it; if true it deserves acknowledgment next to malleus's Prolog contracts.
- TypeDB's exact latest 3.x version (3.4.1 referenced in their materials);
  a "$1B valuation" aggregator figure is not credible against ~$10.8M raised.
- XTDB v2.0.0 GA date (June 12, 2025) inferred from release sequence; the
  release page omits the year.
- LinkML 1.11.1 release date: PyPI says 2026-05-20; one GitHub fetch showed
  2024. PyPI metadata trusted here.
- SHACL 1.2 Core and SPARQL 1.2 RL are Working Drafts; RDF 1.2 is a Candidate
  Recommendation. Every statement about them carries an expiry date. Recheck at
  submission.

## Sources

Primary URLs are kept with the full research notes in `paper/research/`
(three files, one per sweep: standards and rules; claims, provenance, and
mathematics; typed stores, temporal systems, and the commercial landscape). Key
anchors include W3C TR pages for SHACL 1.2, SPARQL 1.2 RL, and RDF 1.2 status;
Kulkarni and Michels, SIGMOD Record 41(3), for SQL:2011; Fowler and Young for
Event Sourcing and CQRS; Kuhn and Dumontier ESWC 2014 for trusty URIs; Kuhn et
al. 2021 for nanopublication supersession and retraction; TGDK 2024 for OTTR;
vendor documentation for the compared stores; and a16z's "The Palantirization
of Everything" (Jan 2026).

The later semantic-log pass, its exact claim limits, and primary URLs are
preserved in `design/SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md`. Its typed research
notebook is `research/semantic_log_knowledge_projection_recon/`; that
notebook's ledger is review authority, not a substitute for the cited sources.

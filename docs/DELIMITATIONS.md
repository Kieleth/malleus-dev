# Delimitations

What malleus reuses, what it rejects, what it must be measured against, and what
it can honestly claim. This is the guard rail against reinventing the wheel,
for this repo and for every project building on it. It is also the evidence
base for the paper's related-formalisms section.

Research verified against primary sources in August 2026. Unverified items are
listed at the end, not silently mixed in.

---

## The one axis that separates malleus from everything below

Every surveyed system follows the same pattern: **describe and verify later**.
PROV describes provenance after the fact. SHACL reports violations on data
that already exists. Trusty URIs verify integrity after publication. Wikidata
ranks claims after they are written. Constraint reports, trust rankings,
validation dashboards: all post-hoc.

Malleus's pattern is **validate before existence**. The ontology is a required
constructor parameter; a graph without it cannot be built, and a record that
violates it never materializes. Every delimitation in this document reduces to
that axis, plus three mechanisms that ride on it: content-addressed staging of
pre-commit candidates, hash-pinned rule contracts, and a first-class state
machine between structural commit and epistemic acceptance.

## Four concessions to make loudly

Each ingredient of malleus, taken alone, has strong prior art. The paper is
safest conceding all four explicitly and citing them:

1. **Write gating exists.** TypeDB fails non-conforming inserts and terminates
   the transaction. Stardog's ICV guard mode fails any transaction that would
   violate constraints. GraphDB and RDF4J's ShaclSail validate on commit and
   roll back on violation. TerminusDB schema-checks every commit. Fluree
   enforces SHACL at transaction time. "Invalid data cannot enter the store"
   is established engineering, not a malleus invention.
2. **The bitemporal semantics are SQL:2011's, adopted deliberately.**
   Application time (valid time) vs system time (transaction time), half-open
   intervals, retroactive changes visible only in later transaction views.
   Canonical citation: Kulkarni and Michels, SIGMOD Record 41(3), 2012. XTDB
   v2 (GA 2025) implements full automatic bitemporality on the same model.
3. **Ledger as authority with a rebuilt projection is event sourcing.**
   Fowler 2005, Young 2010. The JSONL ledger is the event log; the NetworkX
   graph is a CQRS read model. Datomic and XTDB are both log-centric with
   derived indexes.
4. **Content-addressed subgraphs are trusty URIs.** Kuhn and Dumontier (ESWC
   2014) defined hash-embedded identifiers at the RDF-graph level; every
   nanopublication is a content-addressed subgraph. Fluree content-addresses
   commits; TerminusDB commits are immutable delta layers; git and IPLD are
   the generic ancestors.

## What malleus can claim

After the concessions, five things survive, each checked against the survey:

- **The composition.** No surveyed system combines gated writes, portable
  schema artifact, content-addressed staging, bitemporal acceptance, and a
  ledger authority. Fluree and TerminusDB come closest (immutable ledger,
  gated writes, content-addressed history, time travel) and both lack
  valid-time bitemporality and any acceptance state distinct from commit.
- **Ontology as a portable artifact, injected at construction.** Every gating
  store keeps its schema as database-resident state managed through its own
  DDL (TypeDB define/undefine, Stardog constraint sets, TerminusDB schema
  documents). Malleus's ontology is an external LinkML file, usable by code
  generators and other systems, whose loaded registry is the constructor
  parameter. No registry, no graph.
- **Content-addressing applied to pre-commit candidates.** Nanopubs bind
  content to identity at publication; Fluree and TerminusDB address committed
  history. Nothing surveyed stages a not-yet-committed candidate subgraph
  whose digest binds ontology hash, base state, and ordered writes through an
  acceptance workflow.
- **Hash-pinned rule contracts.** The rules lineage (SWRL, SPIN, SHACL-AF,
  SHACL 1.2 Rules) treats rules as inference producers or constraint bodies.
  No surveyed system gives a rule set a pinned identity (exact bytes hashed,
  versioned, bound into the check record) evaluated against isolated
  candidates. No analog found anywhere in the survey.
- **The structural/epistemic split as first-class protocol state.** The
  genuinely unoccupied cell. No surveyed database or KG system has a state
  machine between "structurally valid and recorded" and "accepted knowledge"
  (PROPOSED, ACCEPT, REJECT, DEFER, CONTEST). Nearest analogs are not stores:
  the nanopub assertion/provenance split, Palantir's Action approval
  workflows (product workflow, not graph semantics), and git's staging and
  merge-review, which operates on code, not typed knowledge.

## Formalism by formalism

Verdict vocabulary: **Reuse** (malleus consumes it, say so), **Reject**
(deliberate design refusal, with grounds), **Concede** (real overlap, needs an
explicit paragraph in the paper), **Note** (one line suffices).

### Semantic web standards

| Formalism | Status (Aug 2026) | Verdict |
|---|---|---|
| OWL 2 | Rec since 2012; DL reasoning niche in industry | **Reject.** Open world plus no unique-name assumption: a missing required property is "unknown," not a violation. Fifteen years of integrity-constraint literature (Tao and Sirin, AAAI 2010) documents that OWL natively cannot do closed-world checking. LinkML's gen-owl gives interop for free. |
| SHACL Core | Rec 2017; SHACL 1.2 Core still Working Draft (Aug 2026) | **Concede.** The default reviewer objection. SHACL defines a validation report over a materialized graph; malleus is a gate before materialization. SHACL-as-gate exists only as store-specific engineering (below), not in any W3C spec. |
| SHACL 1.2 Rules | WD 12 Aug 2026 | **Concede + watch.** Standardizes closed-world rules-as-data (SRL, stratified negation). Still inference, not gating; no rule-set content addressing; no firing provenance. Moving target: recheck at submission. |
| ShEx | CG report 2019, never Rec-track | **Note.** Same post-hoc model as SHACL, weaker standing. LinkML has gen-shex. |
| SWRL, SPIN | Legacy; SPIN formally superseded by SHACL | **Note.** Lineage material only. |
| N3 + EYE reasoner | CG report 2023; EYE very active | **Note.** Rules-as-data in a live non-Rec ecosystem; open-world defaults. |
| RDF 1.2 (RDF-star) | Concepts and Semantics at Candidate Rec, April 2026 | **Concede** for future claims work. `rdf:reifies` standardizes referring to a proposition without asserting it. Malleus claim design must answer "why not RDF 1.2 reifiers": packaging of multi-record units, typing, and the write gate. |
| Named graphs + PROV-O | RDF 1.1 datasets; PROV-O Rec 2013, stable | **Reuse (map onto).** Staged candidates are named-graph-shaped; acceptance events are PROV activities. PROV is passive vocabulary; malleus makes the structure a condition of materialization. |
| LinkML | Active, 1.11.1 (May 2026); validation explicitly post-hoc | **Reuse, foundational.** The modeling layer is not reinvented; it is consumed. LinkML ships no store, no write gate, no staging, no contracts. |

### Validating and versioned stores

| System | Mechanism | Verdict |
|---|---|---|
| TypeDB 3.x | Hard write gating against rich types; rule inference removed in 3.x in favor of explicit functions | **Concede.** Strongest prior art for gating. No temporal model, no portable schema artifact, no staging, no acceptance layer, no replayable ledger. |
| Stardog ICV guard mode | Opt-in per-database; violating transactions fail | **Concede.** Real commit-time gating since the 2010s. Constraints are DB-resident; no staging, no digests, no protocol. |
| GraphDB / RDF4J ShaclSail | SHACL validation on commit, exception on violation | **Concede.** Same family; SHACL subset limits; opt-in bolt-on. |
| TerminusDB | Closed-world git-like graph DB: every commit atomic and schema-checked, immutable layers, branch/diff/merge, time travel. Stewardship to DFRNT 2025, v12 current | **Concede, closest composite system.** Individual paragraph required in the paper. Lacks valid-time bitemporality (version time-travel only), acceptance distinct from commit, portable schema artifact, pinned rule contracts. |
| Fluree | Signed transactions on immutable ledger, content-addressed commits, SHACL at transaction time | **Concede, second-closest composite.** Same gaps: no valid time, no acceptance state, no pre-commit candidate addressing. |
| Neo4j / GQL / SQL-PGQ | ISO GQL published 2024; Neo4j whole-graph GRAPH TYPE is a 2026.02 preview, not production | **Note.** The mainstream property-graph world is only now standardizing schema. |
| Datomic | Log of immutable facts, derived indexes, transaction time only | **Note.** No valid time, attribute-level schema only. |
| XTDB v2 | Full automatic bitemporality on SQL:2011 lines, log-centric, schema-free | **Concede.** Direct prior art for Stage 7b temporal semantics. Schema-free and gate-free: any write materializes; one commit event where malleus has two. |
| Wikidata / Wikibase | Statement model with qualifiers, references, ranks; constraints advisory, never blocking | **Concede** for claims work. Operating proof that claims-with-context scale, and the established answer (ranks, deprecation, supersession) that a malleus claim design must match or map to. The constraint-violation backlog is the documented cost of soft constraints. |

### Claims, evidence, templates, mathematics

| Prior art | What it settled | Verdict |
|---|---|---|
| Nanopublications | Claim as content-addressed subgraph with assertion/provenance/pubinfo split; supersession by reference; active 2026 ecosystem (Knowledge Pixels registry) | **Concede, highest collision for claims work.** Nanopubs verify integrity post-publication, accept any RDF, no typed closed-world validation, no gate. Adopt or map to the three-part split rather than inventing a new one. |
| Micropublications | Claim + support/challenge argumentation down to evidence and methods (2014, dormant) | **Note.** Cite for claim/challenge links. |
| SEPIO / GA4GH VA-Spec | Assertion, Evidence Line, Evidence Item; typed profiles over a generic core; VA-Spec 1.0 balloted 2025 | **Concede** for evidence structure. Exchange schema, no store, no gate. Its profile method is what LinkML-based malleus would replicate; say so. |
| DISK Hypothesis Ontology | Evolving hypotheses with provenance | **Note.** The only near-precedent for assumptions. No widely adopted assumption primitive exists anywhere: genuinely open ground. |
| OTTR templates | Parameterized, typed, recursively expanded graph templates; industrial use; TGDK 2024 | **Concede, highest collision for recipes.** OTTR types check templates, not the materialized store; no content-addressed instantiation, no versioned instances. Differentiate on gated digest-addressed instantiation, or compile recipes to OTTR. |
| OpenMath / Content MathML / OMDoc | Formula encoding with dictionary semantics; MathML 4 nearing CR (PR targeted Oct 2026) | **Reuse.** Inventing a formula encoding is the actual reinvention risk. Encode formulas in OpenMath or Content MathML; malleus adds the typed binding and the gate. |
| Wikidata P2534/P7235/P9758, MaRDI | Formulas resident in a KG with symbols linked to entities | **Concede.** The binding half exists; nothing consumes it to compute. |
| Wikifunctions | Definitions in a wiki KG executed by external evaluator backends; Wikidata access through 2026 | **Concede.** The execution half exists; open editing, no typed validation, state lives in a separate system. |
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

None of these publish a mechanism resembling malleus: no gated store, no
ledger authority, no bitemporal acceptance, no portable schema artifact as a
construction requirement. Their existence is motivation, not competition: the
market validates the thesis while the mechanism space stays unclaimed.
Palantir's Action approvals deserve one sentence as a product-workflow analog
of the structural/epistemic split.

## Guardrails for future design

Standing orders for anyone (human or assistant) designing the planned
extensions. Each names what must be engaged before designing, what to adopt,
and what the actual contribution is.

**Claims and assumptions.**
Engage first: nanopublications, Wikidata ranks/supersession, SEPIO/VA-Spec,
RDF 1.2 reifiers. Adopt: the assertion/provenance/pubinfo decomposition and a
rank-or-supersession mechanism, mapped into the five primitives. Contribution:
claims validated against a typed ontology before they exist, unified with
Entity/Event/Signal/Relation. Assumptions are open ground; design freely
there, citing DISK.

**Mathematical formulas.**
Engage first: OpenMath/Content MathML, Wikidata's defining-formula properties,
MaRDI, Wikifunctions. Adopt: an existing formula encoding; do not invent one.
Contribution: typed formula nodes whose symbol bindings are validated at write
time against the ontology, plus an execution contract where an external
engine reads formula + bound KG state and results return to the graph with
provenance. Nobody closes that loop today.

**Axioms and domain rules as data.**
Engage first: SHACL shapes-as-data, SHACL 1.2 Rules (WD, moving), N3.
Adopt: representation mappable to SHACL/SRL rather than a bespoke rule
vocabulary. Contribution: the pinned-contract lifecycle (rules as gated,
versioned, hash-identified KG citizens whose acceptance is itself
ontology-checked), not the rule formalism.

**KG as state.**
Engage first: OpenCitations snapshot chains, RDF archive systems, Wikibase
revisions, XTDB. These version the past. Contribution: staged candidate
future states, content-addressed, admitted through an acceptance gate.

**Recipes (reusable subgraph patterns).**
Engage first: OTTR, then SPARQL CONSTRUCT and ontology design patterns.
Decide explicitly: differentiate (gated, digest-addressed instantiation
validated against the materialized store) or compile malleus recipes to OTTR
templates. Do not build a template engine without this paragraph answered.

## Paper checklist

Systems requiring an individual delimitation paragraph: TerminusDB, Fluree,
Stardog guard mode, TypeDB, XTDB, nanopublications, OTTR.

Claims that would be caught in review and must not appear:
- "Nothing prevents invalid data from entering a store." False; see the four concessions.
- Any novelty claim on bitemporal mechanics. SQL:2011 and XTDB own that.
- Any novelty claim on ledger + projection. Event sourcing owns that.
- Any novelty claim on content-addressed subgraphs as such. Trusty URIs own that.
- A new formula encoding, claim packaging, or template language presented as if no prior art existed.

Claims that survive scrutiny: the composition; ontology as portable
constructor-required artifact; content-addressed pre-commit staging;
hash-pinned rule contracts; the structural/epistemic acceptance split.

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
- SHACL 1.2 and RDF 1.2 are Working Draft / Candidate Rec respectively;
  every statement about them carries an expiry date. Recheck at submission.

## Sources

Primary URLs are kept with the full research notes in `paper/research/`
(three files, one per sweep: standards and rules; claims, provenance, and
mathematics; typed stores, temporal systems, and the commercial landscape). Key anchors: W3C TR pages for
SHACL 1.2 and RDF 1.2 status; Kulkarni and Michels SIGMOD Record 41(3) for
SQL:2011; Fowler (martinfowler.com/eaaDev/EventSourcing.html) and Young (CQRS
Documents, 2010); Kuhn and Dumontier ESWC 2014 for trusty URIs;
nanopub.net and the Knowledge Pixels registry; TGDK 2024 for OTTR; TypeDB,
Stardog, GraphDB, TerminusDB, Fluree, Datomic, and XTDB vendor documentation;
a16z "The Palantirization of Everything" (Jan 2026).

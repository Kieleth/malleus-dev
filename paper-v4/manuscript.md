# Malleus: An Executable Commitment Boundary for Model-Proposed Knowledge Graphs

Version: 0.9.0 working draft

Status: lean engineering draft. The source, selected text-layer reading, and compiled model-proposed ontology are frozen. Model population, ledger replay, four queries, and scoring remain in progress. No document graph or query result is claimed yet.

## Abstract

Language models can turn documents into structured claims, but generation alone does not explain when those claims become accepted system state. We present Malleus as an executable commitment boundary for model-proposed knowledge graphs. A model proposes an ontology and a source-located population. Deterministic components compile the ontology, validate an immutable change, record a decision, append accepted events to a ledger, and reconstruct the graph by replay. We evaluate the smallest complete path on one marine-seismology paper and four questions fixed before the run. The PDF text layer is extracted by a pinned reader and divided into stable blocks. Separate fresh model sessions propose the ontology and population. Queries are bound to ontology types before population and run only against replayed graph state. The evaluation reports compiler corrections, locator completeness, typed refusals, atomic admission, replay equality, and exact query answers. It does not test open-ended retrieval or claim that Malleus determines truth. [RESULT: insert the ontology, population, replay, and four-query outcomes after their artifacts are frozen.]

## 1. Introduction

A language model can read a paper and emit plausible JSON, triples, or graph writes. That output may be useful, but fluency is not an admission rule. A durable knowledge system still needs to answer concrete questions: Which source supported each value? Which schema made the proposed records legal? What checks ran? Who accepted the change? Can an invalid change fail without leaving partial state? Can the same graph be rebuilt after the working copy is deleted?

Malleus addresses that boundary. The model proposes; the system governs commitment. An ontology defines the domain language. A construction recipe expands a finite graph shape. An immutable change binds ordered operations to source, evidence, contract, and prior state. A recorded decision controls whether the change enters an append-only ledger. The graph is then a replayed view of accepted history, not a second write authority.

This is an engineering paper about that boundary, demonstrated on one document. The worked source is a 2025 Nature Communications article on deep earthquakes and carbon-dioxide degassing at the Mid-Atlantic Ridge. Four questions ask about the observation campaign, the location of deep microseismicity, two reported ranges, and the authors' preferred causal hypothesis. A fresh model session proposes the ontology. A separate fresh session proposes the facts and a source block for every value. The compiler and protocol may refuse malformed output. The observed result is reported without a hand-authored repair or evaluator fallback.

The graph must be load-bearing. The query process may see the replayed graph and the query binding, but not the PDF, extracted reading, model transcripts, answer key, network, or an embedding index. A separate scorer compares graph answers with a sealed key. If that isolation test passes, the result establishes only that these four fixed questions were answered without an embedding index in this tested path.

The paper makes three bounded contributions:

1. It states a small commitment protocol that separates model proposal, deterministic compilation, recorded decision, accepted history, replay, and query.
2. It connects an ontology and finite construction grammar to an enforced change-set representation with source locators and atomic admission.
3. It reports one end-to-end document run, including failures and a graph-only query test, without claiming general retrieval superiority or source truth.

## 2. Boundary and terms

An **ontology** defines legal record types, properties, relations, and controlled values. A **change set** is an immutable proposal containing ordered graph operations and the source, evidence, contract, and prior-state coordinates needed to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs graph state from that history. A **locator** names the selected-reading block supporting one proposed value. A **query** is a deterministic graph read fixed before population.

These objects separate concerns that a direct graph write collapses. The ontology says what can be expressed. The construction grammar says how typed inputs expand into a finite graph shape. The change set fixes one proposed transition. Checks and the recorded decision determine whether that transition enters history. Replay, rather than an ambient in-memory graph, produces the state that queries can inspect.

The evaluated path requires five invariants. First, model output remains outside accepted state until a decision authorizes admission. Second, every admitted record conforms to the identified ontology. Third, a failed or stale grouped change leaves no partial append. Fourth, deleting the working graph and replaying the ledger produces the same graph and receipt. Fifth, each reported query answer comes from graph records and not from hidden access to source text or the answer key.

Malleus conformance is not truth. A structurally valid, source-located claim can still be incomplete, misleading, or false. The experiment trusts the exact local implementation and declared artifacts within its environment. It does not authenticate the publisher, model provider, runtime host, evaluator, or storage owner. Those limits are part of the claim, not implementation trivia.

## 3. Protocol

The tested path is:

```text
PDF bytes
  -> pinned text-layer reader and stable blocks
  -> fresh model ontology proposal
  -> ontology compiler
  -> recorded evaluator acceptance of the compiled digest
  -> type-bound query definitions
  -> fresh model population with a locator per value
  -> generic construction recipes
  -> immutable change set and checks
  -> recorded decision and ledger admission
  -> deletion and replay
  -> graph-only queries
  -> separate exact-match scoring
```

### 3.1 Reading

The publisher PDF is retained locally, excluded from version control, and identified by digest. A paper-local reader uses one pinned Python dependency to extract the existing PDF text layer. It performs no rasterization and no OCR. The projector normalizes only line endings, retains extracted characters, groups wrapped lines through a sentence, blank, or page boundary, and assigns stable page and block identifiers. The complete selected reading is private because publishing transformed full text requires a separate rights review. Its digest is public and the extraction is reproducible from the publisher source.

Locators are part of the experimental contract. The population producer must attach a valid block identifier to every value. A locator does not prove a claim true, but it makes the proposed interpretation inspectable and lets the runner refuse unsupported or untraceable values before admission.

### 3.2 Ontology proposal and compilation

Ontology construction runs in a new model session with no access to this paper conversation or the sealed answer key. The session receives the selected reading, four questions, a narrow task brief, and retained copies of the supported Malleus inputs. It returns one ontology file and nothing else.

The compiler is the gate. If the proposal is structurally invalid, the exact compiler diagnostic may be returned to the same session at most twice. Every attempt is retained. There is no hand repair, restart, best-of selection, or model adequacy reviewer. Once an ontology compiles, one evaluator event records that exact digest and the evaluator actor id as the ontology used for population. This event does not certify semantic quality. Whether the ontology can preserve the document's answers is measured later by population and queries.

### 3.3 Query binding before population

Each competency question is translated into a native graph query after ontology compilation and before any population file exists. The binding may name record types, relation types, enum values, legal joins, and output fields. It may not name answer values, document phrases, block locators, entity counts, relation counts, or an exact graph closure. This prevents query authorship from deciding in advance how many records the population model must produce.

### 3.4 Population and construction

A separate fresh session receives the selected ontology, selected reading, generic recipe library, four questions, and population task. It returns one machine-readable population file. Each scalar or list value carries a block locator. If the compiler returns structural diagnostics, the same session gets one retry. There is no content review at this stage and no evaluator-authored population. A malformed output, refusal, or poor answer score remains the result.

The recipe library is construction vocabulary, not an answer key. Its templates may encode how entities, properties, and relations become operations under the selected ontology. They may not contain a document name, answer number, fixed entity identifier, or causal chain taken from the paper. Recipe expansion produces an ordered plan, and a small adapter converts that plan into the change set used by admission.

The change set is the enforced intermediate representation between generated population and accepted graph state. It binds the selected ontology, source evidence, locators, prior ledger and graph coordinates, operation order, dependencies, and content identity. Missing required data is a refusal. The runner does not invent a locator, type, endpoint, time, base state, or answer.

### 3.5 Decision, ledger, and replay

Checks examine source integrity, structural conformance, dependency order, relation endpoints, and the prior state named by the proposal. A complete accepted transaction is appended as one ordered unit. Compiler refusal, a non-accepting decision, stale state, or failed grouped application leaves the accepted ledger unchanged. The failed attempt and diagnostic remain available outside accepted state.

After admission, the runner serializes the graph result, deletes the working graph, reopens the ledger, and replays it. Equality is checked over the canonical graph state and replay receipt. Replay still depends on the identified implementation; the ledger is not self-executing and is not claimed to resist a malicious storage owner.

### 3.6 Query isolation and scoring

The query process receives only replayed graph state and the frozen query binding. It runs with no network and cannot open the PDF, selected reading, ledger source bytes, model inputs, transcripts, population proposal, or oracle. Source-reading and embedding entry points fail if called. The process returns raw graph witnesses and rendered answers. A separate evaluator then compares those answers with the sealed key.

## 4. Implementation and experiment

The experiment runs in an isolated worktree created from Malleus Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`. The relevant implementation includes a research ontology compiler, a restricted stOTTR-derived construction grammar, a bridge from recipe plans to change sets, append-only admission, replay, and native graph filters. These seams are research-local. The paper does not present them as a stable public API or general mapping language.

The worked source is Yu et al., *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, published in Nature Communications in 2025, DOI `10.1038/s41467-024-55792-9`. The publisher PDF has 11 pages and 6,921,046 bytes. The case uses prose only; figures, tables, open-ended synthesis, and specialist reinterpretation are excluded.

The four frozen questions are:

1. Which observation network and campaign produced the microseismicity data, and how many instruments were deployed?
2. Which ridge subsection is associated with deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth and calculated primary-melt CO2 ranges are reported, including units and estimate status?
4. What causal mechanism do the authors prefer, represented as a hypothesis rather than established fact?

The evaluator sealed the answers before the new run. Replacing the reading changed only the private locator map. A mechanical comparison confirmed that all four answer objects stayed equal and that all 22 rebound value locators resolve to selected-reading blocks. Neither model session can access the oracle.

The model-visible inputs for each session are copied once into a retained directory. Network access and writes outside the requested output are disabled. The record names the observable model, service date, task, input files, and diagnostic returns. Provider internals that the interface does not expose remain unknown.

The primary measures are the number and type of ontology compiler returns; population structural outcome and retry count; locator completeness; accepted entity and relation counts; typed refusal outcomes; equality after deletion and replay; exact answers to four graph queries; and attempted query-time source, network, or embedding access.

Natural refusals from ontology or population run count as negative cases. Synthetic mutations are added only for planned classes not observed naturally: source digest drift, missing or unknown locator, illegal type or endpoint, stale prior state, and failed grouped application. Each discovered error class gets a mechanical guard and focused test.

An existing Small Shop fixture supplies component evidence that the compiler, change-set bridge, accepted history, and replay can be composed. It is not a second document evaluation and does not supply any answer or fallback for this case.

## 5. Results

### 5.1 Frozen inputs and reading

The experiment uses five identity groups:

1. Source PDF: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology: `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`.
4. Ledger head and replay receipt: [RESULT].
5. Query binding: [RESULT].

The selected reader is `pypdf==6.16.2`, called with strict parsing and default text extraction. Two independent in-memory builds produced equal bytes. The final projection contains 186 blocks across 11 pages and none of the `CO,` corruption found in the retired reading. The sealed answers were unchanged when their locators were rebound.

### 5.2 Ontology and population

The fresh ontology session produced one proposal. It compiled on the first attempt into 1,401 validated facts, so no compiler diagnostic was returned to the model. The selected ontology digest is `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`.

One event by `actor:paper-v4-evaluator` accepted that exact digest for population. The event records authorization to continue, not an adequacy judgment. No reviewer, hand repair, restart, or alternate ontology contributed to the result.

Population attempts, structural diagnostics, and locator completeness: [RESULT]

Natural refusals and synthetic negative cases: [RESULT]

No ontology or population result will be replaced by a hand-authored recovery or evaluator population.

### 5.3 Admission, replay, and queries

Accepted entities and relations: [RESULT]

Ledger head and admission outcome: [RESULT]

Replay receipt equality and graph equality after deletion: [RESULT]

CQ-01 graph answer, exact match, and witness: [RESULT]

CQ-02 graph answer, exact match, and witness: [RESULT]

CQ-03 graph answer, exact match, and witness: [RESULT]

CQ-04 graph answer, exact match, and witness: [RESULT]

Query-time source reads: [RESULT]

Query-time network calls: [RESULT]

Query-time embedding operations: [RESULT]

Interpretation: [WRITE ONLY AFTER THE FIVE IDENTITIES AND RAW RESULTS ARE FROZEN]

## 6. Related work

Retrieval-augmented generation combines a generator with an external index and conditions output on retrieved passages [Lewis et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230-Abstract.html). Malleus addresses a different systems question: whether a proposed typed change becomes accepted, replayable state. This experiment has no matched retrieval baseline and cannot show that Malleus replaces or outperforms RAG.

Schema-guided extraction is established. SPIRES uses LinkML schemas and ontology grounding to populate knowledge bases from text [Caufield et al., 2024](https://doi.org/10.1093/bioinformatics/btae104). OntoLogX generates ontology-grounded graphs from cybersecurity logs, validates syntax and SHACL constraints, and repairs rejected candidates [Cotti et al., 2026](https://doi.org/10.1002/aisy.202501381). These systems rule out claims that Malleus is the first LLM extraction system, the first ontology-guided pipeline, or the first validate-before-persist design. The narrower contribution here is an identified boundary among proposal, recorded decision, immutable change, accepted ledger, and replayed state.

PROV-O provides an interoperable vocabulary for entities, activities, agents, derivation, and attribution [Lebo, Sahoo, and McGuinness, 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/). Malleus does not claim provenance as new. It makes source and evidence coordinates mandatory inputs to admission; formal PROV-O interoperability remains future work.

OTTR provides typed, parameterized templates for repeatable graph construction [Skjæveland and Karlsen, 2024](https://doi.org/10.4230/TGDK.2.2.5). The current construction grammar implements a restricted stOTTR-derived form for finite topology expansion. It does not claim full OTTR support or differential conformance with Lutra.

Blue Brain Nexus validates graph resources, records revisions in an append-only event log, and rebuilds query projections by replay [Sy et al., 2023](https://doi.org/10.3233/SW-222974). Zep combines temporal knowledge graphs with source episodes, embeddings, full-text search, graph traversal, and model-led edge invalidation [Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956). ActiveGraph treats an append-only run log as authoritative and the working graph as a deterministic projection [Nakajima, 2026](https://arxiv.org/abs/2605.21997). Malleus therefore does not claim append-only histories, temporal graphs, or replayed projections as novel. It tests a smaller executable commitment boundary before graph reconstruction.

## 7. Limitations

One document and four fixed questions cannot establish general ontology induction quality, domain robustness, or statistical performance. Questions whose answers the ontology does not represent will fail, even when a semantic search system might retrieve useful text.

The selected reading comes from a PDF text layer and still contains spacing and ligature artifacts. An earlier Tesseract reading corrupted question-critical `CO2` tokens; that reading and its ontology run are retained as history but excluded from evidence.

Exact-match scoring depends on an evaluator-authored key. Sealing the key before the run and hiding it from both model sessions reduces adaptation, but does not authenticate the evaluator or make the key infallible.

An accepted change is structurally valid under identified checks and a recorded decision. It may still be incomplete or false. The current compiler, construction bridge, and history seam are research-local, create-only for this case, and not a stable cross-language contract.

The graph-only query test covers a deliberately narrow interface. Even if it reports zero embedding operations, that says nothing about exploratory search, semantic similarity, unseen questions, or other documents. Semantic Re-entry, temporal correction, external effects, and autonomous follow-up changes remain future work.

## 8. Conclusion

Malleus treats generated structure as a candidate state transition, not as knowledge merely because a model emitted it. The ontology defines legal meaning, the change set fixes one proposed transition, a recorded decision controls ledger admission, replay reconstructs the graph, and fixed queries inspect only accepted state.

The completed reading and ontology stages fix one source, one source-located text layer, and one unedited model proposal that passed compilation. The remaining run will show, including failures, whether a fresh model session can supply a population that survives this boundary and answers four questions from replayed graph state. The paper's claim will stop at that observed result.

## Appendix A. Reproduction coordinates

1. Source PDF digest: frozen above.
2. Selected reading digest: frozen above.
3. Selected ontology digest: `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`.
4. Ledger head and replay receipt: [RESULT].
5. Query binding digest: [RESULT].

Reproduction command and declared environment: [RESULT]

## Appendix B. Claim-to-artifact index

[GENERATE AFTER THE FIVE IDENTITIES AND RESULT ARTIFACTS ARE FROZEN]

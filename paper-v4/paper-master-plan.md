# Malleus paper master plan

Version: 0.9.0

Date: 2026-09-02

Status: active. D5 isolation, D1 reading, and D2 with D6 ontology compilation and acceptance are complete. Type-based query binding is next. No document graph or query result is claimed yet.

## Objective

Publish a lean engineering paper that explains and executes the smallest complete Malleus argument. The target is a credible 80 percent paper, not the whole research program.

A reader should leave with four answers:

1. Generated text is a proposal, not accepted knowledge.
2. An ontology and compiler define the legal domain language.
3. A typed change crosses an explicit decision boundary into an append-only ledger.
4. The knowledge graph is rebuilt by replay and queried as accepted state.

## Working claim

For one fixed document and four questions, a fresh model proposes an ontology and a source-located population. Malleus compiles the ontology, validates the proposed change, records the decision, admits accepted events atomically, rebuilds a graph by replay, and answers the questions from that graph.

If the isolated query process opens no source text and no embedding index, the paper may report that bounded observation for this run. It will not claim that Malleus replaces RAG, answers arbitrary questions, or establishes source truth.

## Paper boundary

The paper contains one worked document:

- Yu et al., *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, Nature Communications, 2025.
- One publisher PDF, 11 pages, retained locally and identified by SHA-256.
- One selected text-layer reading produced by one pinned Python dependency.
- One fresh-session ontology proposal, with compiler diagnostics returned at most twice.
- One recorded evaluator acceptance event carrying the compiled ontology digest and evaluator actor id.
- One query binding fixed before population against ontology record types, relation types, and enum values. It does not fix graph size or answer values.
- One fresh-session population proposal, with one block locator per value and at most one structural retry.
- One generic construction recipe library. A recipe may encode construction form and types, never an answer value.
- One typed change, ledger admission, deletion, replay, four queries, and exact-match score.

The Small Shop fixture is an implementation baseline, not a second empirical case. The paper experiment remains pinned to Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`.

Excluded:

- An ontology adequacy rubric or model reviewer.
- Hand repair or evaluator-authored population.
- Best-of-run selection or fallback after a poor result.
- A general PDF ingestion product.
- A retrieval comparison or general anti-embedding claim.
- Cypher, SPARQL, Prolog, Semantic Re-entry, temporal correction, actions, effects, invoices, and payment.
- A stable public compiler, mapping grammar, or wire-format promise.
- Cross-language conformance.

## Six terms

An **ontology** defines legal domain record types, properties, relations, and values. A **change set** is one immutable proposal containing ordered operations plus the source, evidence, contract, and prior-state coordinates needed to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs accepted graph state from that history. A **locator** names the selected-reading block supporting one proposed value. A **query** is a deterministic graph read fixed before population.

## Five identities

The experiment freezes exactly five identity groups:

1. Source PDF digest: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading digest: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology digest: `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`.
4. Ledger head plus replay receipt: pending admission and replay.
5. Query binding digest: pending the type-based query freeze.

Source manifests, transcripts, diagnostics, tests, and copied model inputs remain retained evidence. They are not promoted into additional manuscript identity chains.

## Experiment

### Fixed questions

The four questions were fixed before the new run:

1. Which observation network and campaign produced the data, and how many instruments were deployed?
2. Which ridge subsection is associated with the deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth and calculated primary-melt CO2 ranges are reported, with units and epistemic status?
4. What causal mechanism do the authors prefer, represented as a hypothesis rather than established fact?

The answer key remains evaluator-only. D1 changed only its locators. The answer values are unchanged from the sealed oracle.

### Sequence

1. **Isolation, complete.** Run on branch `codex/paper-v4-lean`, created from clean Core `1611944`. The PDF and private files are ignored.
2. **Reading, complete.** `pypdf==6.16.2` reads the PDF text layer with `PdfReader(strict=True)` and `PageObject.extract_text()`. The projector changes only line endings, groups wrapped lines through a sentence, blank, or page boundary, and adds stable page/block locators. The selected reading has 186 blocks across 11 pages. It contains zero literal `CO,`. The prior raster and Tesseract path is retired and uncited.
3. **Ontology, complete.** A fresh session received the selected reading, four questions, supported ontology task, and retained copies of every model-visible Malleus input. Its first proposal compiled without a diagnostic return. No human edited or repaired it. One evaluator event records its digest and actor id for population, without an adequacy judgment.
4. **Query binding, next.** Before population, bind the four queries to ontology record types, relation types, enum values, joins, and output fields. The binding must not name document answers, numeric values, source text, locators, entity counts, relation counts, or an exact graph closure.
5. **Population.** A different fresh session receives only the selected ontology, selected reading, generic recipe library, four questions, and task instructions. It returns one machine-readable population file, with a selected-reading block locator for each value. One retry may receive structural compiler diagnostics only. There is no content review, evaluator-authored population, or fallback. A refusal, malformed result, or poor score is the result.
6. **Commitment.** The generic recipes expand the population into ordered operations. Each operation and property retains its source locator. Malleus compiles a change set, runs the declared checks, records the decision, and appends only a complete accepted transaction.
7. **Replay and query.** Delete the derived graph, reopen the ledger, replay it, and compare the canonical replay receipt and graph state. Run the four bound queries in a process that can see the replayed graph and query binding, but not the PDF, reading, model transcripts, answer key, network, or any embedding index. Score the outputs separately against the sealed key.

### Fresh-session rules

Ontology and population stages use new sessions with no earlier paper conversation. Each receives only its declared inputs. The session may write only the requested output. Network access is disabled. The exact model-visible files are copied into one retained input directory before the run. Observable model and service coordinates are recorded once; unobservable provider settings are named as limitations.

### Negative cases

Natural compiler or population refusals are the primary negative cases. Add a synthetic mutation only when the run did not produce the planned error class:

- source digest mismatch;
- missing or unknown reading locator;
- invalid record type, relation type, or endpoint;
- stale prior state;
- failed grouped application that must leave no partial append.

Each failure must have a typed diagnostic and a hard test for the error class. Failed candidates remain outside accepted history.

### Measures

Report exact observations, not statistical generalizations:

- ontology compiler attempts and diagnostics;
- population structural outcome, retry count, and locator completeness;
- accepted record and relation counts, plus natural and synthetic refusal counts;
- ledger head, replay receipt equality, and graph equality after deletion and replay;
- four query outputs and exact match against the sealed key;
- attempted query-time source reads, network calls, and embedding operations.

The ontology is adequate only to the degree measured by population success and query answers. No evaluator rubric supplies that conclusion.

## Implementation constraints

No additional Core feature is required. The paper-local code may use the research compiler, generic GraphRecipe bridge, private `KnowledgeChangeSet` and history seam, replay, and native graph queries present at Core `1611944`. It must not claim those research-local seams as stable public APIs.

Required fields fail loudly. The runner cannot synthesize a source digest, locator, type, relation endpoint, prior state, or answer when it is absent. Replacing an experimental mechanism removes its old active path. The retired OCR, recovery ontology, reviewer, fixed-closure query, and answer-encoding recipe remain under `paper-v4/retired/` for history and are excluded from tests and claims.

## Retained artifacts

Public repository material:

- this plan, raw ledger, and manuscript;
- source manifest, URL, license, and digest, but not the PDF;
- four competency questions;
- pinned dependency configuration and text-layer extractor;
- selected ontology, generic recipes, type-based query binding, runner, replay receipt, query outputs, score, and focused tests when produced;
- concise reproduction instructions and claim-to-artifact index.

Private or evaluator-only material:

- source PDF;
- selected reading text;
- sealed answer key and rebound locators;
- provider transcripts when redistribution is inappropriate.

## Manuscript shape

Target about 3,500 words:

1. Abstract, 170 words.
2. Problem and contribution, 500 words.
3. Protocol and six terms, 750 words.
4. Implementation and experiment, 850 words.
5. Results, 500 words.
6. Related work, 450 words.
7. Limitations and conclusion, 280 words.

Use one protocol figure and compact result tables only where they reduce prose. Define each of the six terms once. Keep the nonclaims explicit. Name SPIRES, OntoLogX, OTTR, PROV-O, Nexus, Zep, and ActiveGraph where relevant, conceding established prior art.

## Remaining order

1. Freeze the type-based queries.
2. Audit the recipe library for genericity, then run D3.
3. Compile, decide, admit, delete, replay, query, and score.
4. Fill result fields, cut the manuscript to target, and build the arXiv bundle.

## Submission gate

Submit only when:

- the five identity groups resolve to retained artifacts;
- no result sentence depends on a retired artifact;
- the document population is model-authored and no fallback exists;
- the graph is deleted and reproduced by replay;
- the query process cannot read source material or an embedding index;
- every reported answer comes from the replayed graph;
- exact commands reproduce the retained result from declared dependencies;
- related work and nonclaims match the evidence;
- the manuscript is internally consistent and approximately 3,500 words.

## Plan changelog

- 0.9.0, 2026-09-02: Applied author decisions D1 through D6. Moved to a pinned PDF text-layer reading, clean Core worktree, five-identity budget, fresh model-authored population, compiler-only ontology gate, one evaluator acceptance event, type-based query binding, and no fallback. Retired raster OCR, hand recovery, adequacy review, fixed graph closure, and answer-encoding recipes. D1 completed at the selected-reading digest above.
- 0.8.0, 2026-09-02: Selected a hand-authored recovery ontology after a one-shot adequacy review and froze a fixed-closure query binding. Superseded by 0.9.0.
- 0.7.0, 2026-09-02: Retained the Tesseract-era ontology proposal and adequacy refusal, then opened a recovery control. Superseded by 0.9.0.
- 0.6.0, 2026-09-02: Froze the raster OCR contract, questions, oracle, rubric, and block projection. The questions and sealed answer values survive; the OCR and rubric do not.
- 0.5.0, 2026-09-02: Froze the source and generic GraphRecipe-to-change component bridge.
- 0.4.0, 2026-09-02: Selected the document, native queries, GraphRecipe composition, and the then-current raster path.
- 0.3.0, 2026-09-02: Added OCR evidence-integrity planning.
- 0.2.0, 2026-09-02: Split ontology proposal from population and introduced the now-retired adequacy review.
- 0.1.0, 2026-09-02: Created the lean paper plan.

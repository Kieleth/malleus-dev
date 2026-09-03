# Malleus paper master plan

Version: 1.0.0

Date: 2026-09-02

Status: active. The experiment, reconciled lean manuscript, byte-exact retained-environment reproduction, 107-test focused gate, and lint gate are complete. The strict scorer returned `UNSCORABLE_ORACLE_SCHEMA_MISMATCH` with a null score, not 0/4. A complete paper-specific transitive environment lock and the arXiv bundle remain.

## Objective

Publish a lean engineering paper that explains and executes the smallest complete Malleus argument. The target is a credible 80 percent paper, not the whole research program.

A reader should leave with four answers:

1. Generated text is a proposal, not accepted knowledge.
2. An ontology and compiler define the legal domain language.
3. A typed change crosses an explicit decision boundary into an append-only ledger.
4. The knowledge graph is rebuilt by replay and queried as accepted state.

## Working claim

For one fixed document and four questions, a fresh model proposes an ontology and a source-located population. Malleus compiles the ontology, validates the proposed change, records the decision, admits accepted events atomically, rebuilds a graph by replay, and returns typed rows for the questions from that graph.

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
- One typed change, ledger admission, disposal and replay of the derived in-memory graph, four queries, and one strict score attempt.

The published Small Shop correction fixture is an implementation baseline, not a second empirical case. Its research milestone is annotated tag `research/small-shop-correction-replay-v1`, tag object `449ba25964a88ead86cc1aec337be1631cad9471`, at commit `e94f45c74475948dfebdc89247bfb070de0b778d`. The document experiment is pinned to later Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`.

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
4. Ledger head `sha256:a069c3ded48b3da1c6f022bab8601b16173ac90c64c812a4c74435b3085e43b6` plus replay receipt `sha256:6fccc6048d3444b9cbe4ea2bdca3101a7642a4e036a852d26e8fa21fbe03fb29`.
5. Query binding digest: `sha256:115009ff737600d63eb9761bfc11f69ee62cd11f41d60682772556f5fa56c6d9`.

Source manifests, transcripts, diagnostics, tests, and copied model inputs remain retained evidence. They are not promoted into additional manuscript identity chains.

## Experiment

### Fixed questions

The four questions were fixed before the new run:

1. Which observation network and campaign produced the data, and how many instruments were deployed?
2. Which ridge subsection is associated with the deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth and calculated primary-melt CO2 ranges are reported, with units and epistemic status?
4. What causal mechanism do the authors prefer, represented as a hypothesis rather than established fact?

The answer key remains evaluator-only. D1 v2 rebound its locators and reading metadata while preserving the ordered `question_id` plus `answer` projection byte for byte. Its legacy answer schema does not match the D6 typed query-row schema, so the frozen scorer cannot compare them without a post hoc adapter.

### Sequence

1. **Isolation, complete.** Run on branch `codex/paper-v4-lean`, forward-merged with exact Core `f9052b4`. The PDF and private files are ignored.
2. **Reading, complete.** `pypdf==6.16.2` reads the PDF text layer with `PdfReader(strict=True)` and `PageObject.extract_text()`. The projector changes only line endings, groups wrapped lines through a sentence, blank, or page boundary, and adds stable page/block locators. The selected reading has 186 blocks across 11 pages. It contains zero literal `CO,`. The prior raster and Tesseract path is retired and uncited.
3. **Ontology, complete.** A fresh session received the selected reading, four questions, supported ontology task, and retained copies of every model-visible Malleus input. Its first proposal compiled without a diagnostic return. No human edited or repaired it. One evaluator event records its digest and actor id for population, without an adequacy judgment.
4. **Query binding, complete.** The four native queries are frozen as typed source-relation-target cases with enum-constrained relation kinds and projected output fields. Matching returns zero or more rows; neither the binding nor executor requires a graph size or singleton result. The binding contains no document answer, numeric value, source text, locator, record identifier, entity count, relation count, or topology closure.
5. **Population, complete.** A different fresh session received only the selected ontology, selected reading, generic recipe library, four questions, and task instructions. Its first proposal compiled without a retry: 14 records, comprising eight entities and six relations, with 51 located assertions over seven reading blocks. There was no content review, evaluator-authored population, or fallback.
6. **Commitment, complete.** The generic recipes expanded the population into ordered operations. A canonical provenance map associates each record and property with its reading locator and recipe emission. Its digest enters the change set's evidence closure; locators are not inline change-set fields. The orchestrator mechanically verified source and locator integrity plus structural conformance before producing two `SATISFIED` receipts. The runner wrote 19 bootstrap anchors, comprising 18 artifact registrations and one source registration. Atomic admission then appended a five-event suffix: retained change set, proposal, two check events, and the policy-derived `ACCEPT` verdict. The complete ledger has 24 events.
7. **Replay and query, complete.** The runner disposed of the derived in-memory graph, reopened the source-bearing ledger, replayed it, and reproduced the receipt and graph state. This was not deletion of an external graph database. A separate query process received a source-free replay receipt containing the graph snapshot, the selected ontology and retained Malleus import needed to validate it, and the frozen query binding. It did not receive the PDF, selected reading, model transcripts, or answer key. Python-level guards recorded zero file-read, network, and embedding-import attempts. The four queries returned row counts `[1, 1, 2, 1]`.
8. **Scoring, complete.** The query result and scorer structure were frozen before evaluator-only scoring. An identity preflight first refused a stale v1 oracle coordinate. The evidence-backed D1 v2 correction preserved the ordered answer projection byte for byte and rebound only reading and locator metadata. With all three exact inputs bound, the scorer found that the v2 oracle preserves the older answer-object schema while D6 emits binding-shaped typed rows. No precommitted total adapter exists. It therefore returned `UNSCORABLE_ORACLE_SCHEMA_MISMATCH` with `score: null`. This is not a score of 0/4.

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
- ledger head, replay receipt equality, and graph equality after in-memory disposal, reopen, and replay;
- four query outputs and the strict scoring outcome, including a typed unscorable result if the frozen schemas do not align;
- attempted query-time source reads, network calls, and embedding operations.

The ontology is supported here only by structural population success and the returned query rows. The unavailable strict score prevents an answer-level adequacy claim. No evaluator rubric supplies one.

## Implementation constraints

The rebound Core baseline provides the private history and a pure domain-neutral KnowledgeChangeSet composer. The composer binds explicit sources, evidence, operations, valid time, and supersession to current history coordinates. It does not parse sources, choose domain semantics, run checks, admit, replay, or expose a public API. GraphRecipe lowering, document validation, queries, and the experiment runner remain paper-local.

Required fields fail loudly. The runner cannot synthesize a source digest, locator, type, relation endpoint, prior state, or answer when it is absent. Replacing an experimental mechanism removes its old active path. The retired OCR, recovery ontology, reviewer, fixed-closure query, and answer-encoding recipe remain under `paper-v4/retired/` for history and are excluded from tests and claims.

## Execution result

The fresh ontology and population both compiled on their first attempt. The model-authored population contains 14 records, 51 located assertions, and complete locator coverage over seven reading blocks. The two pre-admission checks were derived from retained inputs rather than asserted by the caller. After 19 source and evidence anchors, atomic admission appended a five-event suffix. Both checks were satisfied, the policy computed `ACCEPT`, and replay projected eight entities and six relations from the resulting 24-event history.

The run produced zero natural refusals. Focused mutations cover the five predeclared synthetic refusal classes: source identity, locator closure, type or endpoint conformance, stale prior state, and atomic grouped application.

After the first in-memory projection was discarded, ledger reopen and replay reproduced the retained receipt and graph state. The four type-bound queries returned one, one, two, and one rows respectively. Python-level query guards recorded zero source-file reads, network calls, and embedding imports. These counters describe the instrumented Python process, not an operating-system sandbox.

The strict score is unavailable. The frozen D1 v2 oracle and D6 query result use incompatible answer shapes, and no adapter was fixed before seeing the result. The retained score status is `UNSCORABLE_ORACLE_SCHEMA_MISMATCH` with a null score. The paper reports the returned rows and this evaluation failure; it does not turn the failure into 0/4 or claim exact answer agreement.

## Retained artifacts

Public repository material:

- this plan, raw paper-development ledger, and manuscript;
- source manifest, URL, license, and digest, but not the PDF;
- four competency questions;
- pinned dependency configuration and text-layer extractor;
- selected ontology, model-authored population, generic recipes, type-based query binding, runner, replay receipt, query outputs, typed score result, and focused tests;
- concise reproduction instructions and claim-to-artifact index.

Private or evaluator-only material:

- source PDF;
- selected reading text;
- source-bearing semantic ledger;
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

1. Freeze a complete paper-specific transitive environment lock.
2. Build and inspect the arXiv bundle, then perform the author review.

## Submission gate

Submit only when:

- the five identity groups resolve to retained artifacts;
- no result sentence depends on a retired artifact;
- the document population is model-authored and no fallback exists;
- the initial in-memory graph is disposed, and reopen plus replay reproduces its state;
- the source-free query package and Python-level access guards match the bounded isolation claim;
- every reported answer comes from the replayed graph;
- the oracle schema mismatch and null score are reported without an exact-match claim;
- exact commands reproduce the retained result from declared dependencies;
- related work and nonclaims match the evidence;
- the manuscript is internally consistent and approximately 3,500 words.

## Plan changelog

- 1.0.0, 2026-09-02: Applied D-0017. Rebound the isolated paper branch to exact Core `f9052b4`, accepted the published Small Shop correction tag as bounded research evidence, and accepted the later private composer as a private implementation seam. Preserved the PDF exclusion, five identities, frozen model inputs, and claim boundary.
- 0.9.0, 2026-09-02: Applied author decisions D1 through D6. Moved to a pinned PDF text-layer reading, clean Core worktree, five-identity budget, fresh model-authored population, compiler-only ontology gate, one evaluator acceptance event, type-based query binding, and no fallback. Retired raster OCR, hand recovery, adequacy review, fixed graph closure, and answer-encoding recipes. D1 completed at the selected-reading digest above.
- 0.8.0, 2026-09-02: Selected a hand-authored recovery ontology after a one-shot adequacy review and froze a fixed-closure query binding. Superseded by 0.9.0.
- 0.7.0, 2026-09-02: Retained the Tesseract-era ontology proposal and adequacy refusal, then opened a recovery control. Superseded by 0.9.0.
- 0.6.0, 2026-09-02: Froze the raster OCR contract, questions, oracle, rubric, and block projection. The questions and sealed answer values survive; the OCR and rubric do not.
- 0.5.0, 2026-09-02: Froze the source and generic GraphRecipe-to-change component bridge.
- 0.4.0, 2026-09-02: Selected the document, native queries, GraphRecipe composition, and the then-current raster path.
- 0.3.0, 2026-09-02: Added OCR evidence-integrity planning.
- 0.2.0, 2026-09-02: Split ontology proposal from population and introduced the now-retired adequacy review.
- 0.1.0, 2026-09-02: Created the lean paper plan.

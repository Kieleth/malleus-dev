# Malleus paper master plan

Version: 1.2.0

Date: 2026-09-03

Status: corrected v2 run complete through Codex preliminary inspection, clean environment reproduction, and arXiv source plus rendered-PDF inspection under D-0018. The author has now authorized one KISS v4 document run after the required Core execution gate closes. V4 uses one producer loop, a `source-assertion` history profile with `PARTIAL_IMPORT` origin, grounded packs, typed gaps, and no question input before replay. It supersedes v2 as the selected paper result only if the full run, inspection, and reproduction gates pass. Until then, v2 remains the selected evidence and every v4 artifact is provisional.

## Objective

Publish a lean engineering paper that explains and executes the smallest complete Malleus argument. The target is a credible 80 percent paper, not the whole research program.

A reader should leave with four answers:

1. Generated text is a proposal, not accepted knowledge.
2. An ontology and compiler define the legal domain language.
3. A typed change crosses an explicit decision boundary into an append-only ledger.
4. The knowledge graph is rebuilt by replay and queried as accepted state.

## Working claim

For one fixed document, a fresh model proposes an ontology without seeing the evaluation questions. A separate fresh model later proposes a source-located population with those questions visible. Malleus compiles the ontology, validates the proposed change, records the decision, admits accepted events atomically, and rebuilds a graph by replay. An adopter-owned query surface returns typed rows from that replayed graph, and an identified evaluator inspects them against exact source blocks.

If the isolated query process opens no source text and no embedding index, the paper may report that bounded observation for this run. It will not claim that Malleus replaces RAG, answers arbitrary questions, or establishes source truth.

## Paper boundary

The paper contains one worked document:

- Yu et al., *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, Nature Communications, 2025.
- One publisher PDF, 11 pages, retained locally and identified by SHA-256.
- One selected text-layer reading produced by one pinned Python dependency.
- One fresh-session ontology proposal from the selected reading without competency questions or question-derived semantic instructions, with compiler diagnostics returned at most twice.
- One recorded evaluator acceptance event carrying the compiled ontology digest and evaluator actor id.
- One adopter-owned query binding fixed after ontology compilation and before population. It does not fix graph size or answer values and does not enter knowledge-state identity.
- One fresh-session population proposal, with one block locator per value and at most one structural retry.
- One generic construction recipe library. A recipe may encode construction form and types, never an answer value.
- One typed change, ledger admission, disposal and replay of the derived in-memory graph, four queries, one source-grounded inspection, and one identified human ratification.

The published Small Shop correction fixture is an implementation baseline, not a second empirical case. Its research milestone is annotated tag `research/small-shop-correction-replay-v1`, tag object `449ba25964a88ead86cc1aec337be1631cad9471`, at commit `e94f45c74475948dfebdc89247bfb070de0b778d`. The document experiment is pinned to later Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`.

Excluded:

- An ontology adequacy rubric or model reviewer.
- Hand repair or evaluator-authored population.
- Best-of-run selection or fallback after a poor result.
- A general PDF ingestion product.
- A retrieval comparison or general anti-embedding claim.
- Cypher, SPARQL, question-answering Prolog, Semantic Re-entry, temporal correction, actions, effects, invoices, and payment.
- A stable public compiler, mapping grammar, or wire-format promise.
- Cross-language conformance.

## Six terms

An **ontology** defines legal domain record types, properties, relations, and values. A **change set** is one immutable proposal containing ordered operations plus the source, evidence, contract, and prior-state coordinates needed to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs accepted graph state from that history. A **locator** names the selected-reading block supporting one proposed value. A **query** is a deterministic graph read fixed before population.

## Five identities

The experiment freezes exactly five identity groups:

1. Source PDF digest: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading digest: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology digest: `sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed`.
4. Ledger head `sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b` plus replay receipt `sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796`.
5. Adopter query binding digest: `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`, excluded from the KnowledgeChangeSet evidence closure.

Source manifests, acquisition records, diagnostics, tests, and copied model inputs remain retained evidence. They are not promoted into additional manuscript identity chains.

## Experiment

### Fixed questions

The four questions were fixed before the new run:

1. Which observation network and campaign produced the data, and how many instruments were deployed?
2. Which ridge subsection is associated with the deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth and calculated primary-melt CO2 ranges are reported, with units and epistemic status?
4. What causal mechanism do the authors prefer, represented as a hypothesis rather than established fact?

The retired answer key remains sealed historical material and leaves the active evaluation path. The four question texts and their declared semantics remain frozen. Evaluation uses independently selected source blocks and narrative judgments, not a canonical expected-answer object.

### Sequence

1. **Isolation, complete.** Run on branch `codex/paper-v4-lean`, forward-merged with exact Core `f9052b4`. The PDF and private files are ignored.
2. **Reading, complete.** `pypdf==6.16.2` reads the PDF text layer with `PdfReader(strict=True)` and `PageObject.extract_text()`. The projector changes only line endings, groups wrapped lines through a sentence, blank, or page boundary, and adds stable page/block locators. The selected reading has 186 blocks across 11 pages. It contains zero literal `CO,`. The prior raster and Tesseract path is retired and uncited.
3. **Ontology, complete.** A question-independent fresh session received the selected reading plus generic Malleus ontology inputs, but no competency questions or question-derived semantic checklist. Attempt one was refused because `default_prefix` is outside the supported LinkML profile. The exact diagnostic was returned once; attempt two removed only that field and compiled into 4,146 validated facts. One event accepts its digest for population. This is one document-domain proposal, not a general builder or minimality result.
4. **Query binding and recipes, complete.** The paper-owned binding fixes only ontology record types, relation types, enum values, and projected properties. It fixes no record id, answer value, locator, cardinality, or graph closure, and remains outside admission evidence and replay identity. Nineteen ontology-specific construction templates compile and materialize an arbitrary valid graph without document values.
5. **Population, complete.** A different fresh session received only the corrected ontology, selected reading, ontology-specific generic recipes, four questions, and the closed task. Its first proposal passed the frozen envelope and ontology compiler without a retry. No human repair, content review, or fallback occurred.
6. **Commitment, complete.** Compiled 47 provenance assertions, derived both checks, composed one 13-operation change without query evidence, and admitted it atomically to a 23-event history after both checks were satisfied.
7. **Replay and query, complete.** The runner disposed the live objects, reopened the ledger, reproduced the graph, protocol state, and receipt, then queried the receipt-derived graph through the frozen adopter surface. The four row counts are `[0, 2, 4, 0]`; all guarded source-file, network, and embedding-import attempts are zero.
8. **Source-grounded inspection, preliminary complete and human ratification pending.** The protocol was frozen before corrected query output. A separate fresh Codex session inspected the exact rows against the selected reading without ontology, population, provenance, replay receipt, oracle, score, manuscript, or paper-ledger access. Its preliminary labels are `NOT_EVALUABLE/NOT_RESPONSIVE`, `SUPPORTED/PARTIAL`, `SUPPORTED/RESPONSIVE`, and `NOT_EVALUABLE/NOT_RESPONSIVE` for CQ1 through CQ4. These labels are not paper evidence until Luis independently reviews the rows and source blocks, then ratifies or corrects the record. Report categories and reasoning, never an aggregate score.
9. **Environment reproduction, complete.** A platform-specific lock fixes 89 distributions for CPython 3.12 on macOS arm64 and requires archive hashes. A new virtual environment installed only that lock, then reproduced the selected reading, all five public result files, and the private ledger byte for byte from the exact checkout. The complete document-paper and active v2 paper-local gate passed 184 tests. The lock identifies but does not vendor the interpreter or operating system; the ignored PDF and source checkout remain required inputs.
10. **arXiv bundle, complete.** The lean LaTeX source compiles without warnings, undefined citations, or box overflow into an eight-page PDF with embedded fonts. The final render is `sha256:6b243bafd7331a896a2571b1bcdc24fcf46163014fd72e06c86efae26ca8b25a`, and every page passed visual inspection. A publication-consistency guard binds duplicated manuscript and LaTeX claims to the frozen v2 result files. The final clean paper-local gate passes 189 tests.

### Fresh-session rules

Ontology and population stages use new sessions with no earlier paper conversation. Each receives a declared input set and is instructed to access only those files, make no network call or delegation, and write only the requested output. This is a task boundary over a shared workspace and tool surface, not an operating-system sandbox. The exact model-visible files are copied into one retained input directory before the run. Observable producer and task coordinates are recorded; unobservable provider settings are named as limitations.

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
- four query outputs and per-question source-grounded inspection findings;
- attempted query-time source reads, network calls, and embedding operations.

The ontology is supported here only by compilation, structural population success, returned query rows, and the limits exposed by source-grounded inspection. No evaluator rubric, exact-match oracle, or aggregate score supplies an adequacy claim.

## Implementation constraints

The rebound Core baseline provides the private history and a pure domain-neutral KnowledgeChangeSet composer. The composer binds explicit sources, evidence, operations, valid time, and supersession to current history coordinates. It does not parse sources, choose domain semantics, run checks, admit, replay, or expose a public API. GraphRecipe lowering, document validation, queries, and the experiment runner remain paper-local.

Required fields fail loudly. The runner cannot synthesize a source digest, locator, type, relation endpoint, prior state, transaction time, or answer when it is absent. Replacing an experimental mechanism removes its old active path. The retired OCR, recovery ontology, reviewer, fixed-closure query, and answer-encoding recipe remain under `paper-v4/retired/` for history and are excluded from tests and claims.

## Historical execution result and corrected-run status

The frozen v1 ontology and population both compiled on their first attempt. That run remains exact historical evidence, including its 14 records, 51 located assertions, 24-event history, replay equality, returned rows, and failed scorer. It is no longer the selected experiment because its ontology prompt was conditioned on the four questions.

The corrected v2 population is frozen at `sha256:d4c6fe42c7f96a86c3116c57bccd9c81e53c2ce6e62b421da714a1915ee79964`. It contains 13 records and compiles on its first attempt into 13 operations with 47 located assertions. Both admission checks were satisfied, and the accepted history replays to seven entities and six relations. The four frozen query row counts are `[0, 2, 4, 0]`; the empty CQ1 and CQ4 rows preserve the unconditioned ontology's missing semantics. Codex completed a source-grounded preliminary inspection, but human ratification remains pending.

The corrected run reports replay equality, exact query rows, and zero guarded access attempts. The frozen null score remains part of the v1 failure history and does not enter the selected result. The preliminary inspection remains explicitly nonhuman and cannot support a final evaluation claim until ratification.

## Retained artifacts

Public repository material:

- this plan, raw paper-development ledger, and manuscript;
- source manifest, URL, license, and digest, but not the PDF;
- four competency questions;
- pinned dependency configuration and text-layer extractor;
- selected ontology, model-authored population, generic recipes, type-based query binding, runner, replay receipt, query outputs, Codex preliminary review record, ratification guide, and focused tests;
- platform-specific input constraints, hash-checked transitive lock, clean-verification record, and guard tests;
- lean arXiv LaTeX source, verified bibliography, build instructions, and publication-consistency guard;
- concise reproduction instructions and claim-to-artifact index.

Private or evaluator-only material:

- source PDF;
- selected reading text;
- source-bearing semantic ledger;
- sealed historical answer key and rebound locators, plus the retired typed score result;
- private source-review material needed for human ratification.

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

1. Audit and bind the immutable Core artifacts for the full domain-history profile, grounded packs, and nascent-project playbook.
2. Execute one fresh, question-free v4 producer loop from the selected reading, retaining typed gaps and no fallback.
3. Dispose live state, reopen and replay the ledger, then bind and run evaluator-owned queries against the replayed graph.
4. Prepare source-grounded preliminary inspection for author ratification.
5. Reconcile the lean manuscript and arXiv source, reproduce from a clean checkout, and visually inspect the rendered PDF.
6. Publish the exact paper reproducer through an immutable tag or archive, obtain final author review, and submit.

## Submission gate

Submit only when:

- the five identity groups resolve to retained artifacts;
- no result sentence depends on a retired artifact;
- the document population is model-authored and no fallback exists;
- the initial in-memory graph is disposed, and reopen plus replay reproduces its state;
- the source-free query package and Python-level access guards match the bounded isolation claim;
- every reported answer comes from the replayed graph;
- the frozen scorer failure is historical only, and the selected result uses source-grounded human review without a numeric score;
- exact commands reproduce the retained result from declared dependencies;
- the exact paper reproducer is reachable through a published immutable tag or archive;
- related work and nonclaims match the evidence;
- the manuscript is internally consistent and approximately 3,500 words.

## Plan changelog

- 1.2.0, 2026-09-03: Accepted the KISS v4 execution cut under the author's overnight relay instruction. Selected one document and one producer loop, `source-assertion` with conservative `PARTIAL_IMPORT` origin, questions only after replay, typed gaps, no fallback, and no more than two evidence-triggered ontology revision rounds. The prior three-producer matrix remains diagnostic background. V2 remains selected until v4 passes its complete evidence and reproduction gates.
- 1.1.0, 2026-09-03: Applied D-0018. Preserved the completed question-conditioned run as history, selected a versioned rerun from ontology acquisition, removed competency questions and derived semantic targets from ontology construction, placed adopter query surfaces after replay identity, withdrew automated exact-match scoring, and selected source-grounded inspection with explicit human ratification.
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

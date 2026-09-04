# Malleus paper master plan

Version: 1.3.0

Date: 2026-09-04

Status: corrected v2 remains the selected evidence. The first KISS v4 producer
run is frozen as a structural refusal after three fail-fast grounding failures
exhausted its two-diagnostic budget. It produced no accepted ontology or
population. Core classified aggregate grounding diagnostics and a neutral
governed-history admission path as generic adopter gaps and is correcting them.
A separate v4 rerun requires a new immutable Core coordinate and frozen run
contract. It will keep one fresh single-session producer loop, typed gaps, and
no question input before replay. That rerun is frozen as run-02 under
`paper-v4/experiment-v4/run-02/`, bound to Core
`4881b3a040aaafc7600d009a16ae910084ae32c2`, tree
`f532210148cc43e84dfcd764742ff5cfffda10a4`, with an isolation-only spawn message
and the producer model recorded in the run contract. That rerun has executed:
run-02 is admitted and replayed at Core
`4881b3a040aaafc7600d009a16ae910084ae32c2`, ledger head `sha256:673e1085…` over
14 events, receipt `sha256:19b274f6…` reproduced byte for byte by the reopened
replay, 419 entities, 170 relations, 104 typed gaps, 186 of 186 blocks reviewed,
and a post-replay type-only binding returning 4, 32, 34 and 3 rows over CQ-01 to
CQ-04. It is awaiting preliminary review and ratification, staged under
`paper-v4/evaluation-v4/`, and it is not paper evidence until Luis ratifies.
Manuscript 1.2.1 on branch
`paper-v4-multimodel` remains the paper of record; the v4 result becomes a new
section of its successor. V4 supersedes nothing on its own: it is admitted to the
paper only if the run, inspection, reproduction, and paper gates all pass.

## Objective

Publish a lean engineering paper that explains and executes the smallest complete Malleus argument. The target is a credible 80 percent paper, not the whole research program.

A reader should leave with four answers:

1. Generated text is a proposal, not accepted knowledge.
2. An ontology and compiler define the legal domain language.
3. A typed change crosses an explicit decision boundary into an append-only ledger.
4. The knowledge graph is rebuilt by replay and queried as accepted state.

## Working claim

For one fixed document, one fresh model session proposes an ontology and then a
source-located document capture and population. The competency questions remain
withheld until replay. Malleus compiles the ontology, retains the capture,
validates the proposed change, records the decision, admits it atomically, and
rebuilds a graph by replay. An adopter-owned query surface, bound only after
replay, returns typed rows from that graph. An identified evaluator inspects
each row and its provenance trace against exact source blocks.

If the isolated query process opens no source text and no embedding index, the paper may report that bounded observation for this run. It will not claim that Malleus replaces RAG, answers arbitrary questions, or establishes source truth.

## Paper boundary

The paper contains one worked document:

- Yu et al., *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, Nature Communications, 2025.
- One publisher PDF, 11 pages, retained locally and identified by SHA-256.
- One selected text-layer reading produced by one pinned Python dependency.
- One fresh single-session producer loop from the selected reading, without
  competency questions or question-derived semantic instructions.
- Ontology compilation with diagnostics returned at most twice, followed by no
  more than two source-located, typed-gap revisions in the same session.
- One recorded evaluator acceptance event carrying the compiled ontology digest and evaluator actor id.
- One model-authored capture and population in that producer loop, with one
  selected-reading block locator per proposed value, explicit typed gaps, and
  no fallback or human repair.
- One atomic capture batch under the shipped `source-assertion` history profile.
- One adopter-owned query binding created after population, admission, disposal,
  reopen, and replay. It fixes types, relations, enums, and projected fields,
  never graph size, record identifiers, locators, or answer values.
- Four replay-derived queries, a public `trace_population_record` join for every
  witness, one source-grounded inspection, and one identified human ratification.

The published Small Shop correction fixture is an implementation baseline, not
a second empirical case. Its research milestone is annotated tag
`research/small-shop-correction-replay-v1`, tag object
`449ba25964a88ead86cc1aec337be1631cad9471`, at commit
`e94f45c74475948dfebdc89247bfb070de0b778d`. The first v4 execution was bound
to Core commit `6488ddbfc599e8899d269f8794810f352a5d1fe0`, tree
`6fc5e585e5058e7376ea1aef96fcb49b59107e5e`, merged only into the isolated
paper branch at paper commit `f8d96123f86b2af41d9c67353f952d56565cf6af`.
P6 passed at commit
`573c45b82725d6f444b70e5ff193302dac883e7b`, tree
`6704031dea824572b4d7163ba477c33175397fe7`. P7 has passed at commit
`465924f3e6b0dee64aafeecaeb68cb5e8beb6b41`, tree
`5281da97f17905da45e254fd044536cb67d3398e`. P8 passed at the execution
coordinate above, with installed skill digest
`sha256:ab0279f7b1bda382e45e490f19580805a150dc9159e5912269f9a38350e3fcc8`.

Excluded:

- An ontology adequacy rubric or model reviewer.
- Hand repair or evaluator-authored population.
- Best-of-run selection or fallback after a poor result.
- A general PDF ingestion product.
- A retrieval comparison or general anti-embedding claim.
- Cypher, SPARQL, question-answering Prolog, Semantic Re-entry, temporal correction, actions, effects, invoices, and payment.
- A new query language, general mapping grammar, or stable private wire-format
  promise.
- Cross-language conformance.

## Six terms

An **ontology** defines legal domain record types, properties, relations, and
values. A **change set** is one immutable proposal containing ordered operations
plus the source, evidence, contract, and prior-state coordinates needed to
interpret them. A **ledger** is the append-only accepted history. **Replay**
reconstructs accepted graph state from that history. A **locator** names the
selected-reading block supporting one proposed value. A **query** is a
deterministic graph read whose vocabulary binding is made after replay and does
not enter accepted knowledge identity.

## Five identities

The selected v2 evidence freezes exactly five identity groups. V4 keeps groups
1 and 2, then replaces groups 3 through 5 only after its terminal run succeeds:

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

1. **Isolation and reading, complete.** Work remains on
   `codex/paper-v4-lean`. The PDF and source-bearing ledger are ignored. The
   pinned `pypdf==6.16.2` text-layer path reproduces 186 blocks across 11 pages
   at the frozen source and reading digests. Raster OCR and Tesseract remain
   retired from the paper path.
2. **First-run Core execution gate, complete.** P6 supplies the audited public
   `source-assertion` profile and replay-to-source trace. P7 supplies the
   audited metrology, chronology, and research packs plus mechanical grounding
   and conformance. P8 supplies the audited generic nascent-project playbook.
   The failed run remains bound to the exact immutable P8 coordinate above.
3. **First producer loop, refused and frozen.** One fresh session received only the selected
   reading, frozen Core playbook, shipped profiles, and shipped packs. It first
   proposes and compiles the ontology. The runner may return typed compiler
   diagnostics at most twice. One evaluator event accepts the compiled ontology
   digest. Attempts 1 through 3 refused on successive direct-root grounding
   subjects because the public rite returned one subject per pass. No ontology
   was accepted and population did not start.
4. **Corrected rerun, pending Core freeze.** After independent audit of an
   aggregate grounding diagnostic and neutral checked admission path, freeze a
   new paper contract and start a separate fresh session. If compilation
   succeeds, the same session authors the document capture and neutral
   population plan. Competency questions remain withheld throughout. A
   source-located gap may trigger
   no more than two additive ontology revisions in the same session. Candidate
   captures and gaps are retained. Only the terminal population change is
   admitted. The run stops when another addition would require invention.
5. **Commitment and replay, pending.** The runner retains the exact reading,
   profile, capture, plan, census, gaps, and acceptance evidence; composes and
   checks one terminal change; admits it atomically; discards live state; then
   reopens the ledger and reconstructs the contract and graph by replay.
6. **Binding and query, pending.** After replay freezes, the evaluator binds the
   four questions only to record types, relation types, enum values, directions,
   and projected fields. Queries use the public replayed graph. Every witness is
   joined through `trace_population_record` to the retained assertion, block,
   modality, and attribution. Query execution reads no PDF, selected-reading
   file, network resource, or embedding index.
7. **Inspection, pending.** Codex prepares a preliminary record with separate
   judgments for source support and question responsiveness. Luis alone may
   ratify or correct it. No answer oracle, exact-match schema, or numeric score
   enters the active path.
8. **Reproduction and paper, pending.** A clean environment must reproduce the
   selected reading, admitted ledger, replay receipt, query binding, query
   output, and manuscript facts. The lean Markdown and LaTeX sources are then
   reconciled, built, rendered page by page, and visually inspected.

### Fresh-session rules

The single producer loop uses a new session with no earlier paper conversation.
It receives one declared input set and may access only those files, make no
network call or delegation, and write only its owned staging directory. This is
a task boundary over a shared workspace and tool surface, not an
operating-system sandbox. Exact model-visible bytes and observable producer
coordinates are retained. Provider settings that cannot be observed are named
as limitations.

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

The first-run Core path publicly exposes ontology compilation, a neutral
population plan, evidence retention, low-level change composition and
admission, reopen, replay, native graph reads, and `trace_population_record`.
It does not ship a neutral machine, history binding, or executor that derives
its generic admission-check outcomes. Core accepted this as a generic adopter
gap and is preparing a checked public helper. The shipped
`source-assertion` profile fixes the paper's semantic unit as one atomic capture
batch with `PARTIAL_IMPORT` origin and capture-order valid time. Core does not
extract assertions, invent records, choose the paper's ontology, define its
questions, or judge its answers. P7 and P8 supply the grounded packs and
generic producer playbook used by v4.

The active v4 runner uses only `malleus.compiler` public surfaces. The retired
paper-local GraphRecipe path remains historical and cannot enter active tests or
result identity. The paper still owns producer isolation, post-replay query
binding, source-free query guards, source-grounded inspection, and manuscript
claims.

Required fields fail loudly. The runner cannot synthesize a source digest, locator, type, relation endpoint, prior state, transaction time, or answer when it is absent. Replacing an experimental mechanism removes its old active path. The retired OCR, recovery ontology, reviewer, fixed-closure query, and answer-encoding recipe remain under `paper-v4/retired/` for history and are excluded from tests and claims.

## Historical execution result and corrected-run status

The frozen v1 ontology and population both compiled on their first attempt. That run remains exact historical evidence, including its 14 records, 51 located assertions, 24-event history, replay equality, returned rows, and failed scorer. It is no longer the selected experiment because its ontology prompt was conditioned on the four questions.

The corrected v2 population is frozen at `sha256:d4c6fe42c7f96a86c3116c57bccd9c81e53c2ce6e62b421da714a1915ee79964`. It contains 13 records and compiles on its first attempt into 13 operations with 47 located assertions. Both admission checks were satisfied, and the accepted history replays to seven entities and six relations. The four frozen query row counts are `[0, 2, 4, 0]`; the empty CQ1 and CQ4 rows preserve the unconditioned ontology's missing semantics. Codex completed a source-grounded preliminary inspection, but human ratification remains pending.

The corrected run reports replay equality, exact query rows, and zero guarded access attempts. The frozen null score remains part of the v1 failure history and does not enter the selected result. The preliminary inspection remains explicitly nonhuman and cannot support a final evaluation claim until ratification.

## Retained artifacts

Public repository material, retaining both the selected v2 evidence and the
eventual v4 record:

- this plan, raw paper-development ledger, and manuscript;
- source manifest, URL, license, and digest, but not the PDF;
- four competency questions;
- pinned dependency configuration and text-layer extractor;
- selected ontology, model-authored capture and population plan, typed gaps,
  post-replay type binding, runner, replay receipt, traced query outputs, Codex
  preliminary review record, ratification guide, and focused tests;
- platform-specific input constraints, hash-checked transitive lock, clean-verification record, and guard tests;
- lean arXiv LaTeX source, verified bibliography, build instructions, and publication-consistency guard;
- concise reproduction instructions and claim-to-artifact index.

Private or evaluator-only material:

- source PDF;
- selected reading text;
- source-bearing semantic ledger and exact retained capture assertions;
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

1. Audit the corrected Core aggregate-grounding and neutral-admission boundary,
   then bind a new immutable paper execution coordinate.
2. Freeze a separate rerun contract and execute one fresh, question-free
   producer loop from the selected reading, retaining typed gaps and no fallback.
3. Dispose live state, reopen and replay the ledger, then bind and run
   evaluator-owned queries against the replayed graph.
4. Prepare source-grounded preliminary inspection for author ratification.
5. Add the v4 result to the manuscript of record as a new section in the
   successor of 1.2.1, keeping the three-producer comparison and every 1.2.1
   result sentence; the lean v4 draft does not replace it and stays a support
   document. Then reproduce from a clean checkout and inspect every rendered
   PDF page.
6. Publish the exact paper reproducer through an immutable tag or archive,
   obtain final author review, and submit.

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

- 1.3.0, 2026-09-04: Applied the author's decisions of 2026-09-04. Bound the v4 rerun as run-02 to the current Core coordinate, cut the producer spawn message to isolation only, recorded the producer model and harness in the run contract, and kept manuscript 1.2.1 as the paper of record with the v4 result entering as a new section of its successor. The lean v4 draft is a support document and replaces nothing.
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

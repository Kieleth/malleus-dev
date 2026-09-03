# Malleus: Governing How Generated Knowledge Enters a Knowledge Graph

Working manuscript: 0.8.0

Date: 2026-09-02

Authors: [AUTHOR LIST]

Status: skeleton with retained OCR, adverse primary ontology result, selected post-primary recovery, and queries frozen before population. Population, replay, and query execution remain open.

## Abstract

Large language models can generate domain claims, but generation alone does not define when a claim becomes accepted knowledge. Malleus places a typed commitment boundary between model output and a knowledge graph. A domain ontology constrains legal records. A GraphRecipe construction artifact produces ordered operations. An immutable knowledge-change value binds those operations to exact source, evidence, contract, and base-state identities. In the private semantic-history profile studied here, an identified machine and policy govern the check and verdict sequence, one append-only history admits complete accepted transactions, and the knowledge graph is rebuilt as a view of that history rather than maintained as a second authority.

We define a bounded document experiment and report completed reading, ontology-proposal, compilation, and adequacy-review stages beside one implemented control. The exact 11-page publisher PDF is retained by digest. A declared local adapter rendered and read every page into a portable `malleus-ocr` evidence bundle. All 11 pages were accounted for as `READ`, coverage met its frozen 1.0 threshold, and a stricter paper-local guard verified one complete lineage chain for each page. A fresh model session then emitted an ontology. Its first attempt was structurally invalid; after one exact compiler diagnostic, its second attempt compiled to 1,632 neutral facts. A distinct one-shot reviewer nevertheless refused it because one generic count field could not preserve 19 deployed and 17 usable instruments as separate queryable assertions. The primary run stopped before population, as precommitted. A separately identified three-change recovery compiled to 1,648 facts and passed its own one-shot review with 39 supported witnesses and no unresolved item. It is selected only for the ledger, replay, and native-query control. The implemented Small Shop control already compiles a retained ontology closure, maps retained warehouse and inventory bytes into one accepted change, records a 25-event history, and reconstructs two entities and one relation by replay.

The primary model-only result is negative, not hidden or repaired. The completed stages do not establish document truth, general retrieval superiority, or autonomous ontology quality. They support a smaller distinction: structural validity is not semantic adequacy, and generated domain artifacts can remain proposals until they cross an explicit commitment boundary. The recovery-control graph and query results are not yet claimed.

## 1. Introduction

A language model can read a document and produce a plausible answer. That answer may be useful, but it leaves a basic systems question unresolved: when did generated text become accepted state? A transcript does not by itself identify the vocabulary used, the source occurrence that supports each value, the checks applied before commitment, the policy that admitted the change, or the state from which later queries were answered.

Retrieval does not close this boundary. A retrieval system can select relevant passages and pass them to a model, but retrieval and commitment are different operations. Finding text does not define a typed domain record. It does not establish which proposed relations are legal, whether a multi-record change is atomic, or how accepted state can be reconstructed after the working graph is discarded.

Malleus addresses this narrower problem. It treats generated artifacts as proposals outside accepted state. An ontology defines the admissible domain language. A construction grammar describes finite graph topology. An immutable intermediate representation binds proposed operations to exact source, evidence, contract, and base-state identities. A protocol records checks and the decision to accept, reject, or defer the proposal. In the selected semantic-history profile, one ordered history is authoritative and the knowledge graph is a disposable projection rebuilt from accepted events. The private experiment in this paper demonstrates that target for one controlled case; the public runtime has not fully cut over to this final-identity path.

This separation matters even when the final graph is tiny. A person could write three records by hand. The engineering question is whether the system can explain why those records exist, refuse an invalid change without leaving half-written state, and reconstruct the same queryable state from retained history. The graph is useful here because it is typed and inspectable, not because graph storage alone guarantees knowledge quality.

The evaluation combines one document case with one controlled fixture. In the document case, a fixed reading engine produced hypotheses and retained text from exact source bytes. Malleus OCR verified the evidence bundle but did not perform perception or decide transcription correctness. A fresh model session proposed a small domain ontology from the selected reading. Deterministic compilation accepted its corrected syntax, while a separate semantic review refused the resulting schema before population. A narrowly bounded post-primary correction is kept separate from that result and will supply the remaining systems control. In the Small Shop case, a deterministic research path already crosses retained source, ontology compilation, a knowledge change, private semantic history, and replay into a graph. Together the cases separate reading, proposal, review, and deterministic commitment.

The paper makes three bounded contributions:

1. It specifies a commitment boundary in which ontology, construction, knowledge change, assent, semantic history, and graph replay have separate jobs and identities.
2. It reports an executable research implementation of that boundary, including typed refusal and replay from retained history.
3. It reports a frozen adverse ontology-proposal result and defines a separate control for testing whether a document-grounded replay graph can answer prespecified structured questions without embedding retrieval in the tested path.

The paper does not claim that Malleus determines truth, replaces RAG, reveals model reasoning, or implements general autonomous knowledge maintenance.

## 2. Problem and scope

### 2.1 From generated text to accepted state

Suppose a model reads a marine seismology paper and emits the statement that a named region contains earthquakes at a stated depth. Several distinct assertions are hidden in that sentence:

- The region and earthquake observations are entities of declared types.
- The relation between them is legal under the domain ontology.
- The numerical value has a declared unit and range.
- A precise occurrence in one exact document supports the proposed value.
- The proposal was checked under an identified contract and policy.
- The accepted graph reflects the proposal only if the decision authorized commitment.

Untyped prose cannot enforce these distinctions. A graph can represent them, but a bare graph write need not retain why it was admitted. Malleus therefore treats graph construction as a governed state transition rather than a serialization task.

### 2.2 Terms

In the shipped protocol, a `SourceArtifact` is a typed record containing a caller-declared digest, length, media type, and unconstrained locator string. The public record does not fetch, hash, authenticate, or interpret the bytes or locator. The private semantic-history profile separately retains exact source bytes and checks them against their declared identity. The document experiment defines canonical page and hashed-block locators in a paper-local profile. None of these records establishes publisher or source-origin authenticity.

A Malleus OCR evidence bundle separates source representation, raster, region, reading attempt, text hypothesis, human correction, current selection, source class, policy declarations, and coverage census. The portable bundle records identities and digests. Selected text bytes remain a separate retained artifact. Capability `AUDIT_ONLY` means the verifier checks the bundle and writes nothing to a protocol ledger. It neither renders pages nor calls a reading provider.

A domain ontology defines legal classes, slots, value ranges, inheritance, and relation signatures. In Malleus it is a constitutive grammar for accepted domain records, not a bag of labels.

A GraphRecipe is an authored finite topology template. Malleus currently profiles stOTTR 0.1.4. A recipe does not select sources, decide identity, or authorize writes.

A `KnowledgeChangeSet` is an immutable, content-addressed proposal to change domain state. It binds the relevant contract, source and evidence closure, prior ledger and graph state, ordered operations, valid time, dependencies, and supersession data.

Assent is the protocol lifecycle around a proposed change. Proposal, checks, epistemic decision, action authorization, application, and external execution are distinct events. This paper exercises only the subset needed for knowledge admission.

The private semantic history is the authoritative ordered history used by the demonstrated profile. Append-only here describes the logical write contract. It is not a claim of external notarization or resistance to a malicious storage owner.

Under this optional profile, the accepted knowledge graph is a replay-derived view and not an independent write authority. Other public Malleus graph paths still permit direct structural writes and do not gain semantic-history claims from doing so.

### 2.3 Required invariants

The paper tests the following invariants:

1. Model output is not accepted state.
2. Every accepted record conforms to the identified ontology contract.
3. Every accepted operation belongs to one immutable change identity and names its prior state.
4. The evaluated private history changes only after a complete accepted transaction validates. Compiler refusal, terminal `REJECT` or `DEFER`, stale base, and failed accepted application leave that history and accepted state unchanged. A separate experiment evidence log retains each unsuccessful attempt and diagnostic.
5. Accepted graph state is derivable from retained history under the identified runtime contract.
6. Pending document-control pass condition: query answers must come from the replay-derived graph, not from source text, model context, or an embedding store.

### 2.4 Trust boundary

The model is an untrusted proposal producer. The deterministic kernel trusts exact local implementations and identified policy artifacts within the stated environment. The document provider, source authenticity, model provider, runtime host, and ledger storage are not made trustworthy by Malleus. The evaluation distinguishes these assumptions from structural conformance.

## 3. Protocol

### 3.1 Overview

```text
source bytes
  -> renderer and reading emitter
  -> OCR evidence bundle and retained reading bytes
  -> malleus-ocr verification and selected reading
  -> candidate domain artifacts
  -> validated contract and construction facts
  -> ordered proposed operations
  -> immutable KnowledgeChangeSet
  -> checks and epistemic decision
  -> one semantic and protocol history
  -> replayed accepted graph
  -> structured query result
```

Each arrow is a typed boundary. Intermediate artifacts have distinct identities so that a source edit, ontology edit, recipe edit, policy edit, or base-state edit changes the object being evaluated.

### 3.2 Document reading and evidence integrity

`malleus-ocr` is the integrity gate between the PDF and the text shown to the ontology-producing model. Before reading starts, the experiment freezes a `SourceClass`: required pages, coverage metric families and thresholds, temporal policy, inventory basis, and relevant handling policies. A declared adapter renders and reads each required unit, retains every attempt and selected text byte sequence, and emits a portable finished-reading bundle.

The bundle separates the original source digest from rendered-page digests, spatial region selectors, reader requests and responses, candidate text hypotheses, append-only human corrections, and the selected current reading. The public verifier checks every plane against the OCR ontology and then applies 17 typed integrity diagnostics. It also computes a three-valued census that distinguishes a unit that was read, a unit nobody checked, and a reading attempt that failed. The paper audit found that v0 resolves a hypothesis's attempt but does not require both records to name the same region. The document adapter therefore adds an explicit one-chain-per-page alignment guard and hostile cross-region tests without claiming that the public profile itself changed.

A conforming bundle proves a narrower property than OCR accuracy. Together, the public verifier and paper-local alignment guard show that each selected page reading has one typed path through retained identities to the declared source representation and that coverage was measured under rules fixed before ingest. The emitter also recomputes the exact source, renderer, reader, trained-data, and ontology hashes. These checks do not establish accurate transcription. The hidden answer oracle later judges whether the graph preserves the source-supported answers.

### 3.3 Ontology as a language contract

The ontology defines which records may enter the graph. Compilation resolves the supported ontology closure, rejects unknown or unsupported forms, and emits a canonical frontend-neutral representation. A reloadable structural view validates records without consulting the original LinkML files.

This intermediate representation matters for two reasons. First, the protocol can bind an identified compiled contract rather than an ambient source path. Second, another frontend can be compared at the neutral boundary rather than trusted because it uses a familiar syntax. The current paper demonstrates one LinkML frontend. It does not establish frontend equivalence.

### 3.4 Model-proposed artifacts

For the document case, one new session received only the selected reading artifact, a narrow task brief, the supported Malleus profile, and prespecified competency questions. It emitted only an ontology proposal. The first attempt contained an unsupported root field. The exact compiler diagnostic was returned to the same session, which removed that field and changed nothing else. The corrected source compiled. An independent reviewer then applied the frozen adequacy rubric once and refused the candidate. No primary population began, and no review feedback or retry was supplied.

The recovery control is separate. Its precommit permits only three changes: rename the generic network count as deployed count, add a required usable count, and bump the schema version. It changes neither the original candidate nor the frozen questions, oracle, locators, rubric, classes, enums, relation signatures, or other constraints. It received new source, resolver-configuration, fact-set, and compiled-contract identities. A distinct one-shot reviewer selected the exact recovery digest for control population. This distinction prevents a post-hoc repair from being presented as a successful primary proposal.

The selected recovery ontology's population stage will emit a machine-readable bundle containing construction artifacts, a validated operation/property-to-locator map, and a manifest. Each locator uses a canonical page, numbered text block, and block hash. The map will be retained by identity in the change-level evidence closure and will let an audit trace each projected property or relation endpoint back to a source block after replay. The graph projection itself need not contain provenance edges.

The proposal will be retained before validation. Structural compiler diagnostics may be returned within one session under a retry limit fixed in advance, but each attempt will remain visible. The hidden adequacy rubric is applied once to the final structurally valid ontology with no reviewer feedback or retry. An adequacy failure terminates the primary run. Restarts and best-of-session selection are forbidden. Missing required fields fail explicitly. The runner will not synthesize source identities, types, endpoints, locators, time values, or base coordinates on the model's behalf.

### 3.5 Construction grammar

Malleus GraphRecipe implements a restricted stOTTR-derived profile. The recipe expands typed invocations into target-neutral construction facts, which are assembled into dependency-ordered proposed operations. The grammar owns finite topology expansion. Separate artifacts own source selection, transformations, domain identity, collisions, provenance, admission, and authorization.

The executable recipe corpus reaches required scalar properties, two entities, and one relation; optional and multivalued behavior is not available for this case. The implementation has not passed differential conformance against Lutra. A paper-local adapter now connects an assembled plan to the final-identity knowledge change used by private semantic history. It requires the retained canonical plan digest, preserves operation order and dependencies, checks per-position member and operation alignment, and refuses unsupported signal or event operations.

The component test admits a two-entity, one-relation plan, reopens history, and reproduces the same canonical receipt and graph. It also proves atomic refusal for stale base and an invalid relation, and prevents the accepted path from using direct staging or graph mutation. Its recipe fixture and history contract come from separate compatible ontology inputs. It therefore establishes the generic seam, not same-ontology continuity or the document result. The document ontology and graph will stay inside this implemented subset.

### 3.6 Knowledge-change intermediate representation

The `KnowledgeChangeSet` is the write unit presented for admission. It includes the ordered operations and the identities needed to interpret them. It also anchors the ledger head and graph state against which the proposal was formed. A stale proposal therefore fails before application rather than overwriting newer accepted state.

This is the second enforced intermediate boundary. The compiled contract fixes legal meaning; the knowledge change fixes one proposed transition under that meaning.

### 3.7 Decision and atomic admission

The public Assent protocol can retain proposal, assessment, `REJECT`, and `DEFER` events in its `ProtocolLedger`. The private semantic-history profile evaluated here is a separate implementation and does not compose the public Assent, accepted-graph, or staging modules. Its machine and policy produce explicit check and verdict events, but history admission succeeds only for a complete sequence ending in `ACCEPT`. During replay, the `VERDICT_RECORDED` event applies the knowledge change. There is no distinct application event in RET-010.

A compiler refusal occurs before the private history. A terminal `REJECT` or `DEFER`, a stale base, or a failed accepted application refuses the whole candidate append and leaves private history and accepted state fixed. The experiment evidence log, not the authoritative semantic history, retains the unsuccessful candidate, outcome, and diagnostic.

Malleus does not infer that a structurally valid proposal is true. RET-010 records the actor identifier, checks, and identified policy associated with the accepted change; it does not establish that the actor had legitimate authority.

### 3.8 Ledger and replay

The demonstrated private history retains the contract, machine, policy, mapping, exact source bytes, change value, lifecycle events, and final verdict needed by its replay contract. Candidate replay validates the full append before history bytes are replaced. The accepted graph can then be discarded and reconstructed from the ledger without rereading ambient input files because the ledger embeds the retained bytes.

Replay still requires a compatible implementation of the declared contracts. "From the ledger" does not mean that raw JSONL explains or executes itself.

### 3.9 Querying accepted state

Queries run after replay and only against the accepted graph projection. The experiment uses the implemented deterministic native entity and relation filters. SPARQL and Cypher are outside paper four.

Competency questions were written before ontology proposal. After the recovery digest was selected and before population began, a separate step bound each question to an exact native query specification. The binding fixes an exact 15-entity, 20-relation closure, typed joins, ontology-enum predicates, causal topology, cardinalities, and output fields. It contains no document names, years, counts, numeric ranges, source locators, or expected answers. Twelve tests over fictional graphs verify that returned values come from graph records and that cardinality, context, and topology mutations refuse. This prevents post-hoc query authoring against populated answers.

Replay must read the source-bearing private ledger, so replay and query isolation are separate. The planned harness will add a bound graph projection package containing the graph snapshot and its identified structural contract, but no source bytes. A second process will receive only that package and the frozen queries. It will not be able to open the ledger, source text, model transcript, answer key, or an embedding index. This package, its loader, and its identity checks do not exist yet.

## 4. Implementation

### 4.1 Shipped runtime

Malleus 0.13.3 includes closed-world ontology validation, a typed NetworkX graph, atomic graph staging, protocol-ledger primitives, replay-derived accepted views, and trusted local Prolog verification. These components are public within the package, but each is optional and they do not by themselves form the document pipeline evaluated here. Public accepted-graph replay requires a caller-supplied ontology registry and exact graph base. Public ledger bytes alone do not reconstruct that graph.

### 4.2 Private compiler and semantic-history slice

The private research implementation compiles a supported LinkML subset into canonical neutral facts and a reloadable structural view. Identified machine and policy programs drive a generic interpreter. A separate private history module defines the final-identity `KnowledgeChangeSet`, ledger admission, reopening, and self-contained replay. This private path does not import or unify the public Assent, accepted-graph, or staging implementations.

The Small Shop RET-010 runner composes these pieces for one create-only change. Its mapping and time interpretation remain fixture-local Python behavior. Two check outcomes are supplied by the fixture rather than generated by retained check implementations. These boundaries are part of the result, not incidental implementation details.

The document experiment is pinned to Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3` and begins from a fresh empty ledger. It does not depend on older-ledger migration, the Malleus Code authorization workstream, or a public compiler API.

### 4.3 GraphRecipe slice

The research-local GraphRecipe implementation supports three small positive construction cases and seven frozen negative cases. It parses a restricted stOTTR-derived profile, retains canonical identity and lineage, expands terminal construction facts, assembles ordered operations, and stages them atomically through the public graph path. It is not a general OTTR interpreter and has no differential Lutra conformance result.

For the main document experiment, the paper-local adapter converts those ordered operations to canonical private `KnowledgeChangeSet` bytes and uses the existing accepted-only admission and replay interface. A hostile component test showed that a valid plan digest alone did not prevent operations from being swapped between member IDs. The corrected adapter now checks record identity and the closed operation-kind mapping at every position, and the self-digested swapped plan is refused. The generic bridge is implemented. Same-ontology continuity and the document-specific locator closure remain to be proved by the end-to-end runner.

### 4.4 OCR evidence-integrity profile

Malleus OCR ships at capability `AUDIT_ONLY`. Its portable `Bundle.document()` format separates source, raster, region, attempt, hypothesis, correction, selection, source-class, policy, and coverage records. `verify_bundle` validates each record against `ontology/domains/ocr.yaml` before checking cross-plane lineage, unique origins, append-only correction chains, selection consistency, coverage precommitment, and 17 typed diagnostic classes.

The official paper adapter pins `pdftoppm` 26.03.0, Tesseract 5.5.2, the English trained-data bytes, 300 dpi lossless PNG output, and one machine reading per page. Its combined focused and public-profile suite passed 177 tests; an independent hostile review also passed. The retained run emitted 56 bundle members plus its source-class and bundle records, retained 44 private sidecars, and published only identities and digests. The independent `malleus-ocr` CLI classified all 11 pages as `READ`, reported coverage 1.0 against 1.0, and emitted no diagnostic.

This remains an `AUDIT_ONLY` result. It does not judge transcription or source truth, and Malleus OCR still performs no perception and writes no protocol event. The adapter uses compensating rollback for handled publication failures, not crash-atomic multi-file publication. Its binaries are pinned exactly on the acquisition host; clean-container reproduction remains open.

### 4.5 Document and model harness

No general PDF-to-ontology pipeline exists in Malleus today. The paper harness supplies the document-specific renderer and reader, retained attempt and selected-text bytes, exact source checks, deterministic page-to-block projection, exact ontology acquisition record, compiler harness, independent adequacy records, and the frozen native-query binding. The primary candidate compiled but was not selected. The separately identified recovery was selected only for the control. The harness must still validate per-fact provenance, build the source-free graph projection package, and map the recovery ontology through the existing typed boundaries. The first case excludes figures and tables.

"Fresh" means one new provider session with no prior conversation and only enumerated readable files and tools. The retained acquisition used a new Codex worktree task, fixed the model and reasoning level, prohibited network and writes, and recorded the visible-file closure. Provider system instructions, sampling details not exposed by the task interface, and service nondeterminism remain uncontrolled. Credentialed model acquisition and deterministic reproduction from frozen proposal bytes are separate procedures.

Recon records the source investigation as an 11-event ledger. Independent validation and two byte-identical rebuilds passed. Recon is not the extraction engine or truth judge. Malleus OCR is the reading-integrity gate, while the paper-local adapter performs rendering and OCR.

### 4.6 Reproducibility state

The RET-010 milestone records a focused 140-test completion gate. During the 2026-09-02 paper audit, the default Conda interpreter exposed LinkML `1.10.0.post230.dev0+2909900a4` and LinkML Runtime 1.10.0. The compiler correctly refused them because project configuration pins both top-level distributions to 1.11.1. The local repository `.venv` contains 1.11.1 for both. Under that local environment, the validated-contract, knowledge-history, and Small Shop files passed together: 93 tests in 13.06 seconds. The `.venv` directory itself is not a retained environment artifact.

The paper freeze pins Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3` and tree `657ba6ce1be83064d104803ad5dad644d65b4352`. A separate machine-readable guard recomputes the pinned Assent ontology identity from repository bytes. The combined Core freeze, source freeze, bridge, private-history, and GraphRecipe gate passed 100 tests in 8.08 seconds under the configured local `.venv`; Ruff also passed. This is component verification in a dirty shared checkout, not the final clean-environment receipt.

The submission artifact must reproduce from a clean environment using only declared project configuration. Historical completion evidence and fresh paper reproduction will be reported separately.

Earlier paper work also contains document and model result summaries whose raw requests, responses, or ledgers were lost. They are classified as `REPORTED_SUMMARY_ONLY` and `LOST_PRIMARY_ARTIFACT`. No paper-four number or empirical claim may derive from them.

### 4.7 Why the evaluation target changed

An April 2026 pilot tested whether typed tools improved multi-turn reasoning coherence. Its own audit found that the baseline often outperformed the structured conditions and that the scenario measured memorized pharmacology more than stateful reasoning. Paper four reuses none of those efficacy numbers. That failure motivated the narrower conformance question evaluated here: whether proposed knowledge crosses an inspectable commitment boundary and replays correctly.

## 5. Evaluation

### 5.1 Design

The planned evaluation is a conformance-oriented case study, not a population-level benchmark. It will separate two sources of uncertainty:

- The document case tests a variable model proposal producer against fixed contracts and an independent oracle.
- Small Shop tests the deterministic commitment path with fully controlled input artifacts.

The completed manuscript will report exact counts and retained failures. It will not use significance tests for a sample of one document.

### 5.2 Document case

Source: *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, Nature Communications, 2025, DOI `10.1038/s41467-024-55792-9`. The 11-page publisher PDF is 6,921,046 bytes at `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9` and is available from `https://www.nature.com/articles/s41467-024-55792-9.pdf`. The article is licensed CC BY-NC-ND 4.0. The public experiment bundle will link to the publisher source and will not redistribute transformed full text unless a separate rights review clears it.

The source and reading contracts were frozen before the official run. They fix all 11 pages, a 1.0 page-coverage threshold, static document order, 300 dpi lossless PNG rendering, the exact local renderer, reader, and English trained-data bytes, one machine reading per page, no correction, local-only processing, no retries, and digest-only public output. The run retained every raster, request, response, and selected reading privately. Its public bundle and verification receipt expose identities and counts, not OCR text.

The independent CLI classified all 11 units as `READ`, reported complete coverage at 1.0 against 1.0, and emitted no diagnostic. The paper-local alignment gate also verified one complete source-to-selection chain per page. The official bundle has 56 members plus one source-class record and one bundle record. The selected page files contain 63,005 bytes and 9,683 whitespace-delimited words. These are acquisition counts, not measures of transcription quality.

Before this retained run, the experiment also fixed the text projection: strict UTF-8, line-ending normalization only, maximal runs of nonblank lines, stable page and block order, exact block hashes, no correction, and no public text. It produced 301 blocks. A sealed evaluator artifact binds every oracle answer to exact block IDs and hashes under a frozen support-adjudication guide.

Before the model run, an evaluator froze four competency questions, a hidden six-criterion ontology-adequacy rubric, a separate answer oracle, and an exact oracle-to-block locator binding. The questions cover acquisition, spatial association, two bounded quantities with units and epistemic status, and the authors' preferred causal hypothesis. Figures, tables, and free-form synthesis are excluded. The support guide fixes aliases, units, decimal equality, relation direction, epistemic status, locator correctness, and support classifications. The evaluation does not report fact-level recall because multiple ontology decompositions may be valid. The model saw the selected reading and questions but not the ambient PDF, rejected hypotheses, rubric, guide, oracle, or locator binding. This evaluates task-specific domain construction, not unconstrained ontology discovery.

The fresh-session manifest records model `gpt-5.6-sol`, high reasoning effort, service date, new task identity, exact prompt and file digests, network and write prohibitions, retry limit, Malleus commit, and retained responses. Provider decoding settings not exposed by the task interface remain unknown. The primary run permitted one session and two compiler-diagnostic retries, with no restart or best-result selection. It used one diagnostic retry. The adequacy review then ran once in a distinct session and ended the primary path.

The static document profile will use `ORDER_ONLY` valid time unless the source states an unambiguous domain-valid instant for a proposed fact. Publication, observation, and extraction times will not substitute for one another.

### 5.3 Measures

The primary measures are:

- Malleus OCR verification outcome, three-valued page census, declared coverage metrics, and selected-reading trace completeness.
- Number of reading attempts, human corrections, unreadable units, unattempted units, and failed attempts.
- Whether the ontology compiles under the declared subset.
- The number and type of compiler-guided correction rounds.
- Supported and unsupported accepted-claim counts under the frozen adjudication guide.
- Coverage of exact evidence locators.
- Exact match on the prespecified graph queries.
- Expected-outcome accuracy across paired valid and invalid cases.
- Equality of canonical receipt and graph state after deletion and replay.
- Query-time confirmation that no source text or embedding index was consulted.

The final condition will be tested mechanically in two stages. First, an isolated replay process receives the source-bearing ledger and produces a bound graph projection package containing the graph snapshot and identified structural contract. The package binds the source ledger head, replay receipt identity, contract identity, and graph-state digest. Second, an isolated query process verifies those bindings, receives only the package and frozen query definitions, runs without network access, and cannot see the ledger, document, extracted text, proposal bundle, transcript, or oracle. Source-reading and embedding entry points are replaced by failing sentinels, and a separate scorer consumes the query output. Any forbidden access or identity mismatch fails the test.

### 5.4 Negative mutations

The planned minimal negative corpus changes one controlled dimension at a time: source digest or OCR lineage, required property locator, entity type or relation endpoint, and grouped operation or base-state identity. A fifth validly shaped candidate receives an identified `VIOLATED` check outcome and must drive the machine to `REJECT`. Each invalid case will be paired with its unmodified valid input. Existing OCR conformance cases remain the component-level negative corpus; the document runner will add only an integration case proving that an invalid or incomplete reading bundle cannot reach ontology proposal. Each test must record the typed diagnostic plus experiment-log, semantic-history, acceptance, and graph identities. In the evaluated private profile, every unsuccessful candidate remains outside semantic history and is retained in the separate experiment evidence log.

A zero-refusal positive run is not enough. Without negative cases, it cannot distinguish a permissive gate from a correct one.

### 5.5 Small Shop control

The Small Shop source is a controlled transcription of event `e27` from Fahland's event-knowledge-graph example plus an explicit inventory lookup and fixture choices. Its independent oracle expects:

```text
SalesOrder("O1", order_number="O1")
InventoryUnit("X1", product_code="X")
OrderContainsUnit("contains:O1:X1", O1 -> X1)
```

The compiler oracle is not supplied to the compiler. The case tests source retention, ontology compilation, mapping, knowledge-change identity, protocol admission with two fixture-supplied receipt outcomes, query output, and replay after ambient inputs are removed. Its invalid source-bundle cases stop before ledger creation. They do not demonstrate policy-level rejection of an admitted proposal.

## 6. Results

### 6.1 Small Shop retained result

Repository documentation reports 735 canonical neutral contract facts and distinguishes their identity from the composed machine, policy, and history contract. The canonical RET-010 receipt retains the fact-set digest but not the count, so the final paper will use 735 as a result only after a machine-readable count or compiled artifact is frozen. One run appends 20 bootstrap events, then retains and proposes the knowledge change, records two supplied check receipts, and records the accepting verdict. The resulting 25-event history replays to two entities and one relation matching the independent oracle.

The retained negative corpus changes source content or selection inputs and expects typed pre-admission refusal before ledger creation. A separate test removes the ambient fixture, mapping, machine, and policy files, reopens the JSONL history, and compares an equal graph snapshot plus a byte-identical canonical receipt.

These are retained milestone results. The current paper audit also ran the three focused private files under the repository `.venv`, where all 93 tests passed. [RESULT: insert clean-environment receipt and commit identity.]

### 6.2 Document proposal result

Selected source: Yu et al., 2025, 11 pages, 6,921,046 bytes, `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.

Reading emitter and configuration identity: paper-local emitter `sha256:082e781046c9c8f560eb867b3537aa4f279cdc2262993ecd512e040d68cf9470`; frozen precommit `sha256:68580e74a1107af8b0de033f664fb5053d7c1ffd3ec14c53508d06c79f36fbda`; exact renderer, reader, and trained-data identities are retained in the verification artifact.

Malleus OCR verification, unit census, and coverage result: `FINISHED_READING`, 11 of 11 pages `READ`, zero diagnostics, strict alignment `PASS`, page coverage 1.0 against 1.0, `MET`. Bundle identity: `bundle:paper-v4:aa8ef9e5b924e03e44ca33d3e3616b24ed92535b8a4956dee7e46c26fee47315`.

Reading attempts and review corrections: 11 completed machine attempts, 11 hypotheses, 11 selections, zero human corrections, zero failed units, and zero unattempted units. The retained closure contains 44 files and 20,133,925 bytes; public artifacts contain no OCR text.

Selected-reading projection: 301 ordered blocks; private reading `sha256:0537411117e73b2611ade5088978ba7c8d8a4467d5b51b0c8941bc47f0d41261`; public digest-only manifest `sha256:74399ce57cbe512157c0afdea4bbca946bc2693a3ead69cdfc82b3d6f292c35c`.

Fresh-session attempts: two ontology outputs in one new `gpt-5.6-sol` session. Attempt 1 was refused because `default_prefix` is outside the compiler subset. The exact diagnostic alone was returned. Attempt 2 removed that field and made no other change. The second permitted correction was unused.

Compiled candidate: 15 selected domain classes and 1,632 canonical facts at validated fact-set identity `sha256:8b1aca802746ab7fe487af92a286e1242ae105adda9665ba68388688838ffce2`. This is a compiled candidate, not an accepted ontology.

Adequacy decision: `REFUSED_ADEQUACY`. Eligibility passed. `OA-01`, `OA-02`, `OA-04`, and `OA-06` passed; `OA-03` and `OA-05` failed. The reviewer produced 32 source-located witness rows. One row failed: the ontology's single `ObservationNetwork.instrument_count` cannot preserve deployed count 19 and usable count 17 as separate queryable assertions. All 32 rows had allowed source-block support, so this is a schema distinction failure rather than missing source evidence.

Primary accepted graph records: none. Population authorization was denied before a recipe, change set, semantic history, or graph was created.

Primary evidence-locator coverage, accepted-fact support, and query exact match: not applicable because no ontology was selected and no facts were admitted.

Interpretation: structural compilation and semantic adequacy are distinct gates. The compiler correctly accepted a schema within its supported syntax and constraints. The independent review correctly stopped a loss of meaning that only appears when two supported source values must remain separately queryable. The primary result is adverse and final. A separately frozen three-change recovery control will test the downstream systems path without changing this result.

Recovery-control decision: the exact three-change source compiled to 1,648 canonical facts at validated fact-set identity `sha256:c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332`. A second distinct one-shot reviewer returned `SELECTED_CONTROL`. Eligibility and all six adequacy criteria passed. All 39 witness rows were source-located and supported, with zero failed or unresolved items. This decision authorizes only post-primary control population against source `sha256:29fca9e9325c9d14e5070bcb4274c8704f9d1aaa058799e5a81f27cb5a5a99e9`.

Prepopulation query freeze: four query functions and the exact 15-entity, 20-relation graph closure were bound at `sha256:4eebc55bc86fa842d10bacc0e81e3a6e003569efb270e902533825fcac1c22d1`. The executor uses only the public graph query surface and retains raw record witnesses beside rendered output. Its fictional-data tests passed before any document population artifact existed. This is a design and component result, not a document-query result.

### 6.3 Refusal and replay result

Pre-admission cases refused with no semantic event: [VALUE]

Terminal `REJECT` or `DEFER` candidates refused from private semantic history and retained in the experiment evidence log: [VALUE]

Failed combined acceptance and application cases with no append: [VALUE]

Expected-outcome accuracy across paired controls: [VALUE]

Replay receipt equality: [VALUE]

Graph state equality: [VALUE]

Query-time source reads: [VALUE]

Query-time embedding operations: [VALUE]

Interpretation: [WRITE ONLY AFTER RAW ARTIFACTS ARE FROZEN]

### 6.4 Failure analysis

The ontology stage exposed three different failure classes. First, candidate 1 used an unsupported LinkML root field. The compiler returned one typed diagnostic, and candidate 2 removed only that field. Second, the first retained compiler precommit named the wrong resolver identity even though the compiled bytes were valid. That run is retained but excluded; a second precommit fixed the coordinates, and a hard test prevents their reuse. Third, candidate 2 passed structural compilation but failed semantic adequacy because one count slot conflated two source-backed roles. The one-shot review ended primary population, and the result test prevents any refused candidate from being recorded as selected.

The review-input rerun also exposed an ambient-environment mismatch. Conda supplied LinkML Runtime 1.10.0 and a different trusted `types.yaml`; the compiler refused it. The retained input manifest now fixes the project interpreter, distribution versions, resource size, and digest, with a hard test for drift. These are compiler-input and experiment-harness failures, not claims about source truth.

The recovery control is deliberately post-primary. Its only permitted semantic changes are an explicit deployed-count slot, an explicit usable-count slot, and a schema-version bump. It passed its separate review. Subsequent mapping, admission, replay, and query defects will be reported here with their guard tests. They will not be used to rewrite the primary result.

## 7. Related work

### 7.1 Retrieval and schema-guided extraction

Retrieval-augmented generation combines a generator with an external dense index and conditions output on retrieved passages [Lewis et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230-Abstract.html). Malleus addresses a different systems boundary: whether a proposed typed change becomes accepted, replayable state. The experiment does not compare retrieval quality and cannot support a claim that Malleus replaces or outperforms RAG.

Schema-guided LLM extraction is also established. SPIRES uses LinkML schemas and ontology grounding to populate knowledge bases from text [Caufield et al., 2024](https://doi.org/10.1093/bioinformatics/btae104). OntoLogX generates ontology-grounded graphs from cybersecurity logs, checks syntax and SHACL constraints, and repairs rejected candidates [Cotti et al., 2026](https://doi.org/10.1002/aisy.202501381). Malleus does not claim the first schema-guided extraction or persist-only-valid gate. Its narrower object is the separation among a model-proposed ontology, source-bound population, immutable base-bound change, explicit verdict, authoritative history, and replayed state.

### 7.2 Provenance and construction

PROV-O supplies an interoperable vocabulary for entities, activities, agents, use, generation, derivation, and attribution [Lebo, Sahoo, and McGuinness, 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/). Malleus does not replace that vocabulary or claim provenance as novel. It makes identified source, evidence, contract, prior state, checks, and verdict part of one admission boundary. Formal PROV-O interoperability remains future work.

OTTR provides typed, parameterized, recursively expanded templates for repeatable graph construction [Skjæveland and Karlsen, 2024](https://doi.org/10.4230/TGDK.2.2.5). GraphRecipe reuses a restricted stOTTR-derived form for finite topology expansion while leaving source mapping, evidence, identity, admission, and graph authority to separate artifacts. No claim of a new template formalism, full OTTR support, or Lutra conformance is made.

### 7.3 Authoritative histories and graph memory

Blue Brain Nexus validates graph resources, records revisions in an append-only event log, and rebuilds query projections by replay [Sy et al., 2023](https://doi.org/10.3233/SW-222974). Zep combines temporal knowledge graphs with source episodes, embeddings, full-text search, graph traversal, and LLM-led edge invalidation for agent memory [Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956). ActiveGraph independently makes an append-only run log authoritative and treats the working graph as a deterministic projection [Nakajima, 2026](https://arxiv.org/abs/2605.21997). These systems rule out novelty claims for append-only semantic history, temporal graphs, or replayed projections. Malleus instead tests one smaller commitment boundary in which ontology-constrained proposal, evidence binding, checks, verdict, and atomic history admission precede graph reconstruction. It makes no claim of comparable production maturity, agent-run forking, or general memory-retrieval superiority.

## 8. Limitations

The evaluation uses one document and one small controlled fixture. It cannot establish general ontology induction quality, cross-domain robustness, or statistical performance.

The document questions are prespecified and ontology-expressible. Free-form synthesis, exploratory search, semantic similarity, and questions whose answers were not modeled remain outside the graph-query result.

The planned document path forbids an embedding index and includes a mechanical query-isolation test. Until that result lands, the manuscript makes no empirical no-embedding claim. A passing case would still not show that embedding retrieval is unnecessary for other documents or questions.

An accepted proposal is structurally valid under identified checks and policy. It may still be incomplete, misleading, or false. Malleus does not establish publisher or source-origin authenticity, nor does it authenticate the human oracle, model provider, runtime host, or ledger storage.

The current compiler, semantic-history layer, and GraphRecipe implementation are research-local. The Small Shop mapping is fixture-specific, the population case is create-only, and several semantics remain in Python. Cross-language parity and a stable public wire contract are not demonstrated.

Malleus OCR is an audit profile, not a perception engine. The paper-local adapter supplies the renderer, reader, retained bytes, external hash checks, and stricter page-chain alignment. A conforming bundle still does not prove accurate transcription, source authenticity, quote fairness, or downstream factual support.

The GraphRecipe-to-history bridge has passed its component gate. Its positive test uses separate compatible recipe and history ontologies, so the document runner must still prove one selected ontology remains continuous through compilation, recipe expansion, change identity, admission, and replay.

Prolog is a validation monitor, not the graph query engine. It is absent from RET-010 and will remain outside the primary document case unless the selected domain supplies one compact, objective invariant and the external runtime dependency is captured reproducibly.

Semantic Re-entry, accepted-state correction, external action effects, and observation-driven follow-up changes are future work. Existing temporal and migration primitives do not establish re-entry.

## 9. Conclusion

Malleus starts from a modest premise: generated text should not become accepted knowledge merely because it is fluent or easy to store. For documents, that boundary begins before ontology construction: the reading itself needs retained attempts, review, coverage, selection, and source lineage. Ontology then defines the legal domain language, construction artifacts propose topology, a typed change binds evidence and state, the protocol records the decision, one private history owns accepted writes, and replay produces the queryable graph.

The completed Small Shop slice shows that this profile can be implemented for one controlled change with supplied receipt outcomes. In the document experiment, the fresh model proposal compiled after one syntax correction but failed independent semantic review, so the primary run ended before population. A separately identified recovery control tests only the downstream commitment, replay, provenance, and query path. If that control passes, the paper will establish a narrow point: a graph whose records are mechanically traceable through retained changes to source locators can answer fixed structured questions without an embedding index in this tested path, while keeping proposal, review, and commitment separate.

## Appendix A. Reproduction manifest

[INSERT exact repository commit, clean-environment identity, dependency lock, PDF digest, source-class digest, renderer and reading-engine identities, OCR bundle and selected-text digests, OCR verification identity, prompt digest, oracle digest, ledger digest, graph digest, and one configuration-backed reproduction command.]

## Appendix B. Claim-to-artifact index

[GENERATE from `paper-ledger.md` after the evidence freeze. Every result sentence must point to a retained primary artifact.]

# Malleus paper master plan

Version: 0.8.0

Date: 2026-09-02

Status: active working plan, primary ontology run refused, post-primary recovery selected, native queries frozen before population

## Objective

Publish a lean arXiv paper that explains and demonstrates the smallest complete Malleus argument. The target is a credible 80 percent paper, not a claim that every planned Malleus capability is complete.

The paper should let a reader answer four questions without reading the repository:

1. What problem does Malleus solve?
2. Where is the boundary between generated text and accepted knowledge?
3. What exact artifacts cross that boundary?
4. What has been executed, rejected, replayed, and queried?

## Working thesis

Malleus is a protocol for governing how generated claims enter a knowledge graph. A model may propose an ontology, source interpretations, and graph construction inputs. Deterministic components compile those proposals into typed, identified changes. In the private semantic-history profile evaluated here, only a complete accepted transaction enters the append-only history, and the knowledge graph is a replayed view of that history rather than an independent source of truth.

The single-document demonstration now targets this bounded result:

> For a fixed source document and prespecified questions, Malleus keeps a fresh model's structurally valid but semantically inadequate ontology outside the population and accepted-state paths. A separately identified minimal correction can then be reviewed and used to build a ledger-traceable, replayable knowledge graph whose structured queries create or consult no embedding index.

This does not establish that embedding retrieval is unnecessary in general. It does not compare retrieval quality, handle arbitrary questions, or prove the source claims true.

## The 80 percent boundary

The first paper includes:

- One exact document, retained by bytes and digest.
- One declared PDF renderer and reading emitter that retains every attempt and produces a portable Malleus OCR evidence bundle.
- One `malleus-ocr` verification gate over source, raster, region, attempt, hypothesis, review, selection, policy, and coverage identities.
- One fresh model session acting only as an untrusted proposal producer.
- One small ontology proposed by the model, compiled to a frontend-neutral contract representation, and assessed once against a frozen independent rubric. The primary candidate was refused and is reported as such.
- One post-primary controlled ontology correction, limited to the failed distinction, separately compiled and reviewed before it can be used for the end-to-end control. It cannot change the primary RQ1 result.
- One identified construction path using the restricted stOTTR-derived GraphRecipe profile and a paper-local adapter into the final-identity knowledge change.
- One immutable `KnowledgeChangeSet` that binds source, evidence, contract, base state, operations, and identity.
- One explicit proposal, check, and decision sequence whose accepted transaction materializes atomically during replay. A distinct application event is not claimed.
- One append-only semantic and protocol ledger.
- One graph deleted and reconstructed by replay.
- Three to five prespecified structured questions with independent source-located answers.
- Negative cases that distinguish compiler refusal, a terminal non-acceptance outcome, stale base, and failed atomic acceptance without partial accepted state.
- The existing Small Shop RET-010 vertical as independent engineering evidence and a regression fixture.

The first paper excludes unless the required implementation and evidence land before the evidence freeze:

- A general claim that Malleus replaces RAG.
- A retrieval benchmark against embedding systems.
- Semantic Re-entry or autonomous correction of accepted knowledge.
- A general PDF ingestion product.
- A general ontology induction benchmark.
- A stable public compiler or wire-format promise.
- Cross-language interpreter equivalence.
- External-world effects and observation loops.
- Both Cypher and SPARQL.
- Prolog merely for feature coverage. A Prolog check belongs only if the chosen domain yields one small, objective rule with a useful negative case.

## Paper object

The paper is an engineering research paper about a commitment boundary. It is not a paper about raw question-answering accuracy.

The central distinction is:

> The model proposes. Malleus governs commitment.

The graph must be load-bearing. The evaluation fails if the reported answers come from the model transcript, the PDF text, or an untracked cache instead of the replay-derived graph.

The one-ledger, replay-only architecture is the selected protocol target and the profile evaluated in this paper. The private RET-010 slice demonstrates it for one case. The current public runtime has not fully cut over to the final-identity `KnowledgeChangeSet` and one-history path.

## System slice to present

```text
fixed document bytes
  -> frozen source class, coverage rules, and reading policies
  -> declared renderer and reading emitter
  -> portable OCR evidence bundle plus retained reading bytes
  -> malleus-ocr verification, capability AUDIT_ONLY
  -> selected reading artifact
  -> model-proposed ontology
  -> ontology compilation and neutral contract representation
  -> independent adequacy review and ontology-digest selection
  -> competency-question-to-query binding
  -> model-proposed mapping and fact candidates
  -> GraphRecipe
  -> graph construction facts and ordered proposed operations
  -> operation/property-to-source-locator bindings
  -> immutable KnowledgeChangeSet
  -> checks and explicit epistemic verdict
  -> append-only semantic and protocol ledger
  -> replay-derived accepted knowledge graph
  -> prespecified structured queries
```

The reading engine ends at hypotheses and exact retained reading bytes. `malleus-ocr` verifies the bundle but neither performs perception nor writes the protocol ledger. The model begins from the selected verified reading and ends at proposal bytes. It does not compile, validate, accept, write the ledger, replay the graph, or score the result.

## What exists now

### Implemented and evidenced

- Public ontology, graph, protocol-ledger, temporal replay, and Prolog primitives exist in the repository.
- The private Small Shop RET-010 research path composes exact source bytes, a LinkML ontology, canonical neutral facts, an explicit mapping, one immutable change set, a 25-event ledger, and a replay-derived three-record graph. Repository documentation reports 735 facts, but the paper must freeze a machine-readable count or compiled artifact before treating that number as a result.
- RET-010 records a deterministic receipt, refuses tested invalid source bundles before history creation, validates each complete history append before replacement, discards its in-memory graph, removes the ambient fixture files, and reconstructs an equal graph by replay.
- The recorded RET-010 completion gate reports 140 focused passing tests. On 2026-09-02, the local repository `.venv`, which contains the versions pinned by project configuration, also passed the three private compiler, knowledge-history, and Small Shop files together: 93 tests in 13.06 seconds. The `.venv` directory itself is not retained evidence.
- GraphRecipe has a research-local, restricted stOTTR-derived profile, positive cases through two nodes and one relation, and frozen negative cases. It has not passed differential conformance against Lutra.
- The paper-local GraphRecipe adapter converts a retained `AssemblyPlan` into canonical `KnowledgeChangeSet` bytes without using GraphRecipe's direct staging path. Its component case preserves member order and dependencies, refuses misaligned or unsupported operations, admits through private history, and reopens to the same receipt and graph. This is component evidence, not yet the document result.
- Native graph queries can select typed entities and relations.
- Recon can retain literature works, claims, evidence, comparisons, and derived artifacts.
- `malleus-ocr` provides an `AUDIT_ONLY` evidence-integrity profile and portable bundle document. It verifies typed source-to-reading lineage, separation of identity planes, precommitted policy and coverage declarations, and 17 typed failure classes. Its focused suite passed 152 tests in 2.82 seconds on 2026-09-02.
- The selected 11-page publisher PDF is frozen at `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`. Its source manifest records the publisher URL, DOI, page count, byte length, and CC BY-NC-ND 4.0 license. Distribution of a derived full-text OCR corpus remains outside the paper bundle unless a separate rights review clears it.
- The paper-local emitter rendered all 11 pages with the exact pinned `pdftoppm` binary and read each raster with the exact pinned Tesseract binary and English trained data. It retained 44 private sidecars, emitted a digest-only public bundle, and passed the independent `malleus-ocr` CLI. All 11 pages are `READ`; page coverage is 1.0 against a threshold of 1.0; there are no corrections, failed units, or unattempted units. The bundle identity is `bundle:paper-v4:aa8ef9e5b924e03e44ca33d3e3616b24ed92535b8a4956dee7e46c26fee47315`.
- A paper-local alignment guard closes a public OCR v0 gap by requiring one page-specific raster, region, attempt, hypothesis, and selection chain per declared page. This is experiment evidence, not a claim that the public profile has changed.
- Four competency questions, a sealed answer oracle, and a sealed six-criterion ontology-adequacy rubric were frozen before model acquisition. A deterministic page-to-block projection rule was also frozen before the retained OCR run.
- The frozen projection produced 301 ordered blocks. The private model-visible reading is `sha256:0537411117e73b2611ade5088978ba7c8d8a4467d5b51b0c8941bc47f0d41261`; its digest-only public manifest is `sha256:74399ce57cbe512157c0afdea4bbca946bc2693a3ead69cdfc82b3d6f292c35c`. A sealed artifact binds the answer oracle to exact block IDs and hashes under a frozen support-adjudication guide.
- Recon now retains the document-selection and domain-investigation record. Its 11-event ledger validates, and two fresh builds are byte-identical to the retained build. Recon remains outside perception and truth adjudication.
- A machine-readable Core manifest pins commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`, Assent ontology 0.11.0, and grammar-4 semantic identity. A guard checks those coordinates against exact repository bytes.
- A fresh `gpt-5.6-sol` session emitted two ontology attempts. The first was structurally refused for unsupported `default_prefix`; the second removed only that field and compiled to 1,632 facts at validated fact-set identity `sha256:8b1aca802746ab7fe487af92a286e1242ae105adda9665ba68388688838ffce2`.
- A distinct one-shot reviewer found the compiled candidate semantically inadequate and denied population authorization. The deterministic eligibility gate itself passed. `OA-03` and `OA-05` failed because one generic `instrument_count` cannot preserve 19 deployed and 17 usable instruments as separate queryable assertions. The primary result is `REFUSED_ADEQUACY`, with one failed witness and no unsupported source witness.
- The exact review input package, reviewer precommit, raw reviewer output, structured result, and refusal receipt are retained. A runtime guard also proves that the ambient Conda LinkML types cannot silently replace the project-pinned module.
- The frozen post-primary correction changed only the two instrument-count properties and schema version permitted by its precommit. It compiled to 1,648 facts at validated fact-set identity `sha256:c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332`. A second distinct one-shot reviewer returned `SELECTED_CONTROL`: all six criteria passed, all 39 witness rows had allowed source-block support, and `unresolved_count` was zero. This authorizes population for the recovery control only and leaves the primary refusal unchanged.
- Four native queries are frozen at binding `sha256:4eebc55bc86fa842d10bacc0e81e3a6e003569efb270e902533825fcac1c22d1` against the selected recovery ontology and exact 15-entity, 20-relation closure. The executor uses only `query`, `query_relations`, and `get_node`. Its tests use fictional values and prove that returned scalars and rendered enum labels come from graph records. The binding contains no document names, numeric answers, reading locators, or source text.

Primary evidence anchor: git tag `research/small-shop-compiler-ledger-kg-v1`.

### Missing integration required by the document control

- Capture the pinned local renderer and OCR dependencies in a clean, configuration-driven environment and reproduce the retained reading result. The completed official run is host-local and does not yet support a clean-container claim.
- Prove same-ontology continuity in the document runner from the selected document ontology through GraphRecipe, `KnowledgeChangeSet`, admission, reopen, and replay. The generic component bridge exists, but its positive fixture intentionally does not establish the document result.
- Add an identified operation/property-to-locator binding artifact, retain it in the `KnowledgeChangeSet` evidence closure, and test per-record trace reconstruction. A global evidence bundle alone is insufficient.
- Add a source-free graph projection package, loader, canonical identity, and tests binding it to the source ledger head, replay receipt, compiled contract, and graph-state digest.
- Implement exact source-integrity and structural-conformance receipt producers in the Python harness, retain their identities and diagnostics, and state that the protocol validates their receipts. Do not imply language-neutral check execution.
- Add the document-specific runner, negative mutations, replay test, and canonical result artifact.
- Reproduce through project-pinned dependencies and retain a clean-run receipt. The default Conda interpreter contains LinkML `1.10.0.post230.dev0+2909900a4` and LinkML Runtime 1.10.0, and correctly fails the 1.11.1 identity guard. The local repository `.venv` contains 1.11.1 for both and passes the focused private path, but that directory is not itself a retained environment artifact.

### Minimum dependency on Malleus Core

No further Core feature is required for the paper experiment. Pin the experiment to Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`, and treat the private history interface as research-local rather than public or stable.

The composition belongs in the paper experiment. The new thin adapter converts one GraphRecipe `AssemblyPlan` into canonical `KnowledgeChangeSet` bytes, preserves operation order and dependencies, verifies each operation's retained member identity and operation kind, and requires the canonical plan digest in the evidence closure. It uses the existing `KnowledgeChangeHistory.admit`, `reopen`, and `replay` path. It does not modify the private history module or route accepted writes through GraphRecipe's direct staging path.

The component bridge gate is complete: one positive two-entity, one-relation case; equality after ledger reopen and replay; stale-base and invalid-relation refusals that leave ledger bytes and replayed state unchanged; refusal of self-digested member-operation identity and supported-kind mismatches; and an architecture guard against direct staging or graph mutation. The combined frozen gate passed 100 tests in 8.08 seconds under the configured local `.venv`. Same-ontology continuity, the locator map, and the actual PDF-derived graph remain document-runner work. Broader Core work, package promotion, Malleus Code authorization, same-file ontology migration, and Semantic Re-entry are not dependencies of paper four.

### Explicitly not implemented

- PDF rendering or reading by `malleus-ocr` itself. It renders nothing, calls no provider, and selects no engine. The completed renderer and reader are a paper-local adapter.
- Automatic ontology induction and PDF-to-population conversion as a Malleus pipeline.
- Cypher or SPARQL execution against the domain graph.
- Same-ontology composition from the selected PDF ontology through GraphRecipe and semantic-history replay. The generic paper-local bridge is implemented, but the document case has not used it.
- A successful primary ontology proposal. The frozen one-shot primary attempt ended in `REFUSED_ADEQUACY`; only the separately labeled recovery control may continue to population.
- Prolog inside RET-010.
- Semantic Re-entry.
- The proposed Small Shop quantity correction loop.

## Primary experiment: one document

### Research questions

RQ1. Does a fresh model session produce an ontology that passes both the declared compiler subset and the frozen independent adequacy rubric under the recorded primary protocol? For this run, the answer is no: structural compilation passed after one diagnostic correction, while independent adequacy failed.

RQ2. Can the evaluated Malleus profile turn a separately identified and selected recovery ontology plus population proposal into one change whose records are traceable to exact source blocks, admit an accepted transaction atomically, and derive accepted state only by ledger replay?

RQ3. Can the replay-derived graph answer the prespecified structured questions exactly, without consulting the document or an embedding index at query time?

RQ4. Do typed source, schema, evidence, dependency, and base-state mutations fail closed without partial ledger or graph state?

### Document selection criteria

The document must be legally redistributable or stably downloadable, text-native, bounded enough for full manual inspection, and rich enough to express entities, relations, measurements, evidence, and at least one hypothesis or classification. Its claims must be understandable without building a specialist scientific model.

The author selected Candidate A:

- Candidate A: [Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge](https://doi.org/10.1038/s41467-024-55792-9), Nature Communications, 2025. It is open access, 11 pages, marine, and contains instruments, regions, event classes, measured quantities, and causal hypotheses.
- Candidate B: [Project PROBES](https://pubs.usgs.gov/of/2001/0112/), USGS Open-File Report 01-112, 2001. It is public and operationally concrete, but longer and less compact.
- Candidate C: [The new earthquake locations and focal mechanisms catalogues for the western Ionian Sea, Italy](https://doi.org/10.1038/s41597-026-06979-w), Scientific Data, 2026. It offers a structured catalogue for validation, but is a larger data problem than the first two.

The exact Candidate A publisher PDF is frozen as 6,921,046 bytes across 11 pages at `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`. The source manifest records DOI `10.1038/s41467-024-55792-9`, the publisher landing and PDF URLs, and CC BY-NC-ND 4.0. The experiment can retain the source locally and cite the publisher copy. Publishing a transformed full-text OCR corpus requires a separate rights review.

For Candidate A, the experiment froze four competency questions covering the observation network and campaign, named ridge subsection and event location, depth and carbon-dioxide ranges, and the preferred causal mechanism. The independent answers, annotation closure, and exact source blocks were sealed before model acquisition.

### Frozen evaluation inputs

The experiment freeze must contain:

- Original document bytes, media type, license record, source URL, and SHA-256 digest.
- A precommitted Malleus OCR `SourceClass`, required-page inventory, coverage metrics and thresholds, temporal policy, rendering contract, selector profile, data-handling policy, and hostile-content policy.
- Renderer and reading-emitter identity, version, configuration, request and response identities, raw retained attempts, and selected reading bytes.
- A portable finished-reading bundle containing source, raster, region, attempt, hypothesis, review, selection, coverage, and policy records.
- A conforming `malleus-ocr` verification result. A passing result establishes evidence integrity under the profile, not correct transcription or source truth.
- Selected text using canonical page numbers, numbered text-block identifiers, and block hashes. The first case excludes figures and tables unless the chosen emitter preserves them deterministically.
- Three to five competency questions written before the model sees the task.
- A frozen ontology-adequacy rubric that names required semantic coverage without prescribing one unique decomposition.
- An identified reviewer who selects or refuses one exact ontology digest for the experiment before population begins.
- A hand-authored answer oracle, support-adjudication guide, exact annotation scope, and document locators, excluded from model and compiler inputs.
- A task brief stating the allowed ontology and recipe subset.
- Exact Malleus commit and dependency lock.
- Exact model identifier, service date, new session identity, prompt, visible context, tools, accessible paths, network policy, exposed decoding parameters, and transcript. Provider internals that cannot be observed must be named as limitations.
- One-session correction policy fixed before execution, including the maximum number of compiler-diagnostic retries. Restarts and selecting the best result across sessions are forbidden in the primary run.
- Exact native query specifications bound to the selected ontology digest and frozen before population.
- Valid-time policy. Use `ORDER_ONLY` for the static document case unless a proposed fact has an unambiguous domain-valid instant that the source states directly. Publication, observation, and extraction times are not interchangeable.

The model may see the selected reading artifact, task brief, and competency questions. It does not receive ambient PDF access, rejected reading hypotheses, the scoring rubric, or the answer oracle. This makes the experiment a task-specific ontology construction test, not a claim of unsupervised universal domain discovery.

Ontology proposal and population are separate stages. The first stage emits only the ontology candidate. Structural compiler diagnostics may be returned within the frozen retry limit. The independent adequacy rubric is applied once to the final structurally valid candidate, with no reviewer feedback or retry. The reviewer either selects one exact ontology digest for the experiment or terminates the primary run as an adequacy failure. Population starts only against a selected digest. An ontology edit during population is forbidden in the primary run. The selection record lives in the experiment evidence log; it is not presented as a private semantic-history event.

The primary run terminated at adequacy review. Its result remains immutable. To finish the systems demonstration without disguising that result, version 0.7.0 added a post-primary control. The control changed only the failed count distinction: it renamed `instrument_count` to `deployed_instrument_count`, added required `usable_instrument_count`, and bumped the candidate schema version. It received new source, resolver-configuration, fact-set, and compiled-contract identities. A distinct one-shot review selected that exact digest for control population. No other class, enum, relation, constraint, question, oracle, locator, or rubric changed. Any graph and query result from this ontology is a recovery-control result, never evidence that the fresh primary proposal passed.

### Required population bundle

After ontology selection, the separately retained population producer should emit exact files, not prose instructions:

- A LinkML ontology within the declared compiler subset.
- A small recipe library within the restricted stOTTR-derived profile. The main case must stay inside the implemented required-scalar, entity, and relation subset. Optional and multivalued recipe behavior is excluded.
- A source mapping or typed extraction artifact that binds each proposed value to a canonical page and hashed text block.
- An operation/property-to-locator binding artifact whose identity is retained in the change evidence closure.
- Candidate recipe invocations or population rows.
- A machine-readable manifest binding every member by digest.

Required fields must fail loudly when absent. The runner must not infer silent defaults for source identity, page location, record type, relation endpoints, valid time, or base-state coordinates.

### Run sequence

1. Freeze document, source class, reading policies, coverage rules, downstream questions, and independent oracle.
2. Run the declared renderer and reading emitter. Retain every request, response, hypothesis, review, selection, and selected text byte sequence.
3. Emit the portable finished-reading bundle and run `malleus-ocr` verification. A refusal terminates document acquisition; it is not silently repaired downstream.
4. Bind the verified bundle, selected reading, and their identities into the experiment evidence closure.
5. Start one new ontology session in the isolated acquisition environment with only the declared Malleus library, skill, selected reading, task brief, and questions.
6. Retain the ontology proposal and transcript before validation.
7. Return only structural compiler diagnostics within the frozen retry limit, then apply the hidden adequacy rubric once. The completed primary run terminated here with `REFUSED_ADEQUACY`.
8. Execute the separately frozen, narrowly bounded recovery control and select or refuse its exact digest in a new one-shot review. Completed with `SELECTED_CONTROL`.
9. Bind exact native query specifications to the selected recovery ontology digest before population begins.
10. Start population only against that digest and retain the complete population proposal before validation.
11. Compile recipe and mapping inputs to ordered operations plus per-property locator bindings.
12. Produce identified source-integrity and structural-conformance receipts in the deterministic Python harness.
13. Bind the operations, locator map, OCR bundle, selected reading, and evidence closure into one `KnowledgeChangeSet`.
14. Execute the protocol machine and policy. The private semantic history admits only a complete accepted transaction. All unsuccessful attempts and diagnostics go to the separate experiment evidence log.
15. Delete the derived graph and all ambient proposal inputs allowed by the replay contract.
16. Reopen the ledger and reconstruct the graph plus each record's audit trace to the retained locator map.
17. In a separate isolated process, execute only the frozen graph queries and send results to a separate scorer.
18. Run the minimal document mutations through the same entry point.

### Minimum negative cases

- Source digest does not match the frozen document.
- The OCR bundle has broken source-to-reading lineage, missing page coverage, or a selected reading whose digest does not match retained text.
- One proposed record is missing its property-to-block locator binding.
- One entity has the wrong type or one relation has an invalid endpoint.
- One grouped operation is invalid or the proposal names a stale base.
- One validly shaped candidate receives the identified check outcome `VIOLATED`, the machine reaches `REJECT`, and private semantic history remains unchanged while the evidence log retains the run.

Each mutation has its unmodified valid case as a paired control. Existing GraphRecipe conformance tests retain grammar-specific negatives; the document runner does not duplicate them.

Every error discovered while building the experiment must add a mechanical guard and a test for the error class.

### Measures

- Ontology compilation outcome and typed diagnostics.
- Number of correction rounds under the frozen policy.
- Supported and unsupported accepted-claim counts. Every accepted property and relation is classified under the frozen guide; no fact-level recall is reported.
- OCR unit census, declared coverage metrics, verifier outcome, and selected-reading trace completeness.
- Evidence-locator coverage for accepted facts.
- Exact answer match for prespecified questions.
- Expected-outcome accuracy across paired valid and invalid cases.
- Experiment-log, semantic-history, acceptance, and graph identities before and after each mutation. In the evaluated private profile, unsuccessful candidates remain outside semantic history and are retained only in the experiment evidence log.
- Canonical receipt equality after deletion and replay.
- Whether the query runner opens an embedding index or reads source text. The required answer is no for this bounded path.

The no-embedding condition needs a mechanical check with two isolated stages. Replay runs from the source-bearing private ledger and emits a bound graph projection package containing the graph snapshot and identified structural contract, but no source bytes. The package binds the source ledger head, replay receipt identity, contract identity, and graph-state digest. Query then runs in a different process and temporary directory with only that package, runtime, and frozen query definitions, and verifies those bindings before execution. Deny network access and omit the ledger, source document, extracted text, model transcript, proposal directory, and answer oracle. Replace source-reading and embedding entry points with failing sentinels. Send the query output to a separate scorer. Any attempted forbidden access or identity mismatch fails the run.

The sample is one case study. Report counts and exact failures, not significance tests or broad percentages presented as population estimates.

## Secondary experiment: Small Shop

RET-010 should stay in the paper because it already isolates the deterministic backbone from model variability. It establishes the source-to-contract-to-change-to-ledger-to-graph composition for one controlled create-only case with fixture-supplied check receipts. Its invalid source-bundle tests stop before ledger creation; they are not evidence of a policy-level `REJECT` event.

The proposed model interaction, Prolog violation, simulated action, new observation, and follow-up change span four additional integration seams. They move together to future work for paper four. This future extension must not be called Semantic Re-entry unless the actual re-entry contract, typed synthesis boundary, observation path, and tests exist. Current re-entry work is design-only and frozen.

## Query interface decision

The paper uses native Malleus Python queries. This is the implemented surface and proves structured retrieval with the least new machinery. SPARQL and Cypher are excluded from paper four.

## Claim discipline

The paper may claim:

- A bounded executable composition exists for fixed inputs.
- Generated artifacts remain proposals until deterministic admission.
- The accepted graph is reconstructed from one retained history in the demonstrated private profile.
- In the evaluated private profile, tested unsuccessful candidates remain outside semantic history and cannot partially change accepted state. The separate evidence log retains their exact inputs and diagnostics.
- Prespecified structured questions are answered from the replay-derived graph without embedding retrieval in the document experiment, if the results support it.

The paper must not claim:

- Malleus determines truth.
- An accepted claim is factually correct merely because it conforms.
- The ledger authenticates source bytes or resists a malicious storage owner.
- Malleus exposes or verifies hidden model reasoning.
- Malleus makes RAG obsolete.
- The composition is novel merely because known components are combined.
- The private compiler, GraphRecipe profile, or wire format is a stable public API.
- Semantic Re-entry, correction, general mapping, or cross-language parity exists before executable evidence lands.

## Novelty position

Do not lead with a novelty-by-conjunction claim. Provenance, ontology constraints, graph staging, rule checks, append-only histories, temporal projection, and controlled actions all have prior art.

The selected research object is the precise executable boundary and its measured behavior: model-produced proposal bytes, ontology-bound intermediate representations, explicit admission, one history authority, and replay-derived graph state. Its novelty remains provisional. The related-work section must reverify and compare primary work on S2CRA, selective revision and PVD, ontology-retrieval verification, ANNEAL, SkillDAG, OntoLogX, ActiveGraph and other log-to-graph systems, ClaimGarden, Sentinel, TOKI, PROV-O, and OTTR. If the residual difference remains architectural rather than empirical, say so.

## Manuscript structure

1. Abstract. State the boundary, method, measured case, result, and limits.
2. Introduction. Explain why fluent generation is not a commitment protocol.
3. Protocol. Define ontology contract, construction grammar, `KnowledgeChangeSet`, assent, ledger, and replayed graph.
4. Implementation. Separate shipped primitives, research-local slices, and the composed paper runner.
5. Evaluation. Specify the single-document case, negative mutations, replay test, and Small Shop evidence.
6. Results. Report exact counts, failures, query answers, and replay identities.
7. Related work. Compare against primary literature without universal negatives.
8. Limitations. State the truth, security, generality, implementation, and evaluation boundaries.
9. Conclusion. Restate the commitment-boundary result without expanding it.

## Artifact set for submission

The evidence freeze should contain:

- Paper source and rendered PDF.
- Master plan and raw ledger. The claim-to-artifact index is generated from ledger entries rather than maintained as a third manual authority.
- Exact selected source document and license metadata, or a stable fetch manifest if redistribution is prohibited.
- Renderer and reading-emitter configuration plus all declared dependencies.
- Exact selected reading bytes and source-region index.
- Portable Malleus OCR bundle document, verification result, unit census, coverage report, and retained attempt identities.
- Fresh-session task brief, prompt, environment manifest, transcript, and raw proposal bundle.
- Independent competency-question and answer oracle, source-locator set, ontology rubric, and support-adjudication guide. These artifacts must not assume that one ontology decomposition is uniquely correct.
- Document-case runner and all configuration-declared dependencies.
- Positive and negative test corpus.
- Generated protocol ledger, canonical receipt, replayed graph serialization, and query results.
- Small Shop retained evidence at a pinned git identity.
- Machine-readable reproduction manifest with checksums.
- Bibliography built from verified primary sources.
- A Recon bundle recording source selection, inspected claims, competing interpretations, search limits, and oracle revisions. Recon remains evidence infrastructure beside the experiment, not the PDF ingestion engine.

No result may depend on a local tool or service that is absent from project configuration.

Acquisition and deterministic reproduction are separate commands. The credentialed acquisition command may call the model and produces a frozen proposal bundle, but cannot promise byte-identical model output. The deterministic reproduction command begins from retained document, reading, and proposal bytes and must reproduce compilation, admission, replay, queries, and scoring without model credentials.

The master plan owns current scope, author decisions, and sequencing. This raw ledger owns observations, corrections, and plan-version history. The manuscript consumes both but is not a factual authority. The submission claim-to-artifact index is generated from numbered ledger entries.

## Work sequence and dependencies

1. Freeze the exact thesis, nonclaims, primary document, and query interface.
2. Quarantine every earlier model or document result whose raw requests, responses, or ledgers are missing. Those artifacts are `REPORTED_SUMMARY_ONLY` and `LOST_PRIMARY_ARTIFACT`, never paper-four evidence.
3. Pin a clean repository state and repair configuration-driven reproduction of RET-010.
4. Define the ontology rubric, proposal bundle, support-adjudication guide, and independent oracle before implementation.
5. Select and implement one configuration-declared PDF renderer and reading emitter for the Malleus OCR bundle. Done for the pinned local environment; clean-environment packaging remains open.
6. Freeze the source class and policies, produce a finished-reading bundle, pass OCR verification, retain selected reading bytes, and materialize the deterministic block projection. Done.
7. Complete and freeze the paper-local GraphRecipe-to-`KnowledgeChangeSet` component bridge against the pinned Core baseline. Done. Same-ontology document integration remains in step 8.
8. Retain the primary ontology refusal, then compile and independently review the frozen recovery control. Done. The primary is `REFUSED_ADEQUACY`; the separate control is `SELECTED_CONTROL`.
9. Freeze ontology-bound native queries, then build one recovery-control document runner through the existing protocol and ledger path.
10. Add stage-specific negative cases and replay-only reconstruction.
11. Retain the population proposal and all deterministic run artifacts without changing the ontology, oracle, or measures.
12. Score the primary refusal and recovery control separately.
13. Replace manuscript result placeholders with exact artifact-backed values.
14. Complete the primary-source related-work audit and claim-evidence check.
15. Render, inspect, reproduce from a clean environment, and freeze the arXiv bundle.

Paper writing proceeds with every step. The manuscript is not deferred until the experiments finish.

## Submission gate

The lean paper is ready when all of these are true:

- The thesis and nonclaims are frozen.
- The selected document bytes, query specifications, and GraphRecipe subset are frozen by digest.
- The deterministic path from retained document, reading, and frozen proposal bytes runs from one declared command in a clean environment. Model acquisition has a separate declared command and environment manifest.
- Every dependency and setup action is captured in configuration.
- All primary inputs, outputs, and identities are retained.
- The independent oracle predates the scored model run.
- The graph answers the frozen questions from replayed state.
- Negative cases prove atomic refusal for the claimed error classes.
- The graph can be deleted and reconstructed without ambient source or proposal files, within the stated replay boundary.
- The paper contains no result placeholder supporting a main claim.
- Every numerical claim points to a primary result artifact.
- Every related-work claim points to a verified primary source.
- A clean reproduction and manuscript render both pass.

Failure is publishable only if the thesis is narrowed to what the retained evidence actually supports. No hidden manual repair may be presented as protocol behavior.

## Closed author decisions for the primary slice

1. Primary document: Candidate A, the 2025 Mid-Atlantic Ridge paper.
2. Query surface: native Malleus Python queries.
3. Construction path: GraphRecipe is part of the central demonstration, with the missing adapter implemented in the paper experiment.
4. Reading emitter: faithful raster-to-text OCR through the existing Malleus OCR evidence profile.

These decisions authorize implementation but do not count as evidence that any missing component exists. The paper will not widen into Prolog, temporal correction, or re-entry before the bounded recovery control is complete.

## Plan changelog

- 0.8.0, 2026-09-02: Compiled the exact three-change post-primary recovery to 1,648 facts and retained new source, resolver-configuration, fact-set, and compiled-contract identities. A distinct one-shot reviewer selected the control with all six criteria passing, 39 supported witness rows, and zero unresolved items. Kept the adverse primary result fixed and authorized only the downstream recovery-control population.
- 0.7.0, 2026-09-02: Retained the two-attempt fresh ontology proposal and one-shot independent review. The structurally valid candidate failed `OA-03` and `OA-05` because one count field cannot distinguish 19 deployed from 17 usable instruments. Terminated the primary run without review feedback or retry, froze a separately labeled minimal recovery control, and kept the Core baseline unchanged.
- 0.6.0, 2026-09-02: Froze the renderer, reader, source class, policies, competency questions, sealed oracle, ontology rubric, and text-block rule; executed the single official 11-page OCR run; retained 44 private sidecars; passed strict paper-local alignment and independent `malleus-ocr` verification; and independently reproduced the 11-record Recon investigation. Kept clean-environment OCR reproduction, model acquisition, same-ontology admission, queries, and replay open.
- 0.5.0, 2026-09-02: Froze the exact publisher PDF and its license boundary, added machine-readable source and Core guards, completed the paper-local GraphRecipe-to-`KnowledgeChangeSet` component bridge, fixed adversarially discovered member-operation alignment gaps, and retained a 100-test verification receipt. Kept same-ontology document composition and OCR emission open.
- 0.4.0, 2026-09-02: Accepted the Mid-Atlantic Ridge document, native Malleus queries, central GraphRecipe composition, and faithful raster OCR. Pinned the current Core baseline and moved the thin GraphRecipe-to-`KnowledgeChangeSet` adapter into the paper experiment, leaving Core unchanged.
- 0.3.0, 2026-09-02: Added `malleus-ocr` as the mandatory document-reading integrity gate. Kept perception outside the verifier, added the missing emitter and retained-reading bridge, froze source-class and coverage inputs before acquisition, added OCR artifacts and measures, and opened the raster-OCR versus sibling born-digital reading-profile decision.
- 0.2.0, 2026-09-02: Applied three independent audits. Split ontology proposal from population, added independent ontology selection and per-fact locator binding, separated public Assent from the private semantic-history profile, moved the Prolog and re-entry episode to future work, narrowed negative cases, recommended native queries, split model acquisition from deterministic reproduction, and recorded the configured 93-test reproduction.
- 0.1.0, 2026-09-02: First evidence-based plan. Recentered the paper on a bounded document-to-ledger-to-replayed-KG demonstration. Kept Small Shop as the implemented deterministic backbone. Marked GraphRecipe integration, standard queries, PDF ingestion, and re-entry according to their actual implementation status.

# Malleus paper ledger

Ledger version: 1.0.0

Opened: 2026-09-02

Plan tracked: `paper-master-plan.md` version 1.0.0

## Operating rule

This is the raw, append-only record for the fourth paper attempt. New findings, decisions, contradictions, failures, and result identities get new numbered entries. Do not erase an earlier entry to make the history look cleaner. Correct it with a later entry that names the superseded statement.

The master plan owns current scope, author decisions, and sequencing. This ledger owns raw observations, corrections, and plan-version history. Any change to thesis, experiment scope, claim boundary, or submission gate increments the plan version and adds a corresponding entry here. The manuscript consumes both but is not a factual authority. A claim-to-artifact index will be generated from numbered ledger entries rather than maintained as a third manual ledger.

## Plan version history

### PV-0001

Date: 2026-09-02

Plan version: 0.1.0

Change: Created the lean paper plan from the current repository, prior paper lineages, and the three named Codex tasks.

Reason: The earlier lineages either pursued a different empirical question, attempted a much broader assent lifecycle, or never reached manuscript prose. The present implementation now supports a smaller and more concrete paper.

### PV-0002

Date: 2026-09-02

Plan version: 0.2.0

Change: Applied three independent evidence audits. Split ontology proposal from population; added an independent adequacy rubric, ontology-digest selection, frozen question-to-query binding, and validated per-fact locator mapping; distinguished public Assent from the private accepted-only semantic history; moved the Prolog, action, observation, and re-entry episode to future work; narrowed the negative corpus; recommended native queries; and split credentialed model acquisition from deterministic reproduction.

Reason: Version 0.1.0 blended separately implemented paths and left several claims untestable or circular. Version 0.2.0 makes the main claim match the actual seams and adds mechanical controls for its new evidence.

### PV-0003

Date: 2026-09-02

Plan version: 0.3.0

Change: Added Malleus OCR as the required document-reading evidence-integrity gate. Inserted source-class and coverage precommitment, a declared external renderer and reading emitter, a portable finished-reading bundle, retained selected text, OCR verification, and a bridge into the experiment evidence closure. Opened the choice between faithful raster OCR and a sibling born-digital reading profile.

Reason: The OCR profile supplies the missing typed source-to-reading lineage and coverage boundary, but it is `AUDIT_ONLY`. It does not itself render, read, retain text, recompute the digest of external PDF bytes, or write the semantic history.

### PV-0004

Date: 2026-09-02

Plan version: 0.4.0

Change: Closed the four primary-slice choices in favor of the Mid-Atlantic Ridge paper, native Malleus queries, central GraphRecipe composition, and faithful raster OCR. Pinned the Core experiment baseline and assigned the GraphRecipe-to-knowledge-change adapter to the paper experiment rather than Core.

Reason: The author instructed the work to assume the pending choices accepted and move forward. Repository inspection shows that the needed composition can be built outside Core from existing research-local values and that Core intentionally prevents GraphRecipe from becoming a dependency of the private history module.

### PV-0005

Date: 2026-09-02

Plan version: 0.5.0

Change: Froze the exact Core and document-source coordinates, implemented and hardened the paper-local GraphRecipe-to-knowledge-change component bridge, and moved those items from planned work to retained component evidence. Kept same-ontology document integration, locator closure, OCR emission, and clean reproduction open.

Reason: The source and bridge now have exact artifacts and mechanical tests. A hostile review found and forced repair of one operation-lineage defect before the bridge result was frozen. The resulting evidence supports only the generic component seam, not RQ2 or the PDF case.

### PV-0006

Date: 2026-09-02

Plan version: 0.6.0

Change: Froze the full reading contract, competency questions, sealed answer oracle, sealed ontology rubric, and deterministic block-projection rule. Executed the official retained 11-page raster OCR run, passed strict paper-local alignment and independent public-profile verification, and independently reproduced the Recon investigation.

Reason: Document reading has crossed from plan to retained evidence. The open critical path is now model acquisition and same-ontology commitment, not Core or PDF perception.

### PV-0007

Date: 2026-09-02

Plan version: 0.7.0

Change: Retained the fresh ontology proposal, exact compiler correction, sealed review inputs, and one-shot adequacy refusal. Terminated the primary population path as precommitted. Added a separately labeled post-primary recovery control restricted to the failed instrument-count distinction.

Reason: The model's structurally valid candidate could represent one instrument count but not preserve deployed count 19 and usable count 17 as independent queryable assertions. Hiding or silently repairing that failure would invalidate the experiment. The paper instead reports the adverse primary result and separates it from the systems control needed to exercise admission, replay, and querying.

### PV-0008

Date: 2026-09-02

Plan version: 0.8.0

Change: Retained the exact recovery compilation and its separate one-shot adequacy review. The corrected digest was selected for post-primary control population. Query authoring must now freeze against that digest before any population artifact is created.

Reason: The bounded correction resolves the one failed count distinction without changing the primary candidate or result. Separating selection, query freeze, and population prevents the control from adapting its ontology or queries to populated answers.

### PV-0009

Date: 2026-09-02

Plan version: 0.9.0

Change: Applied D-0011 through D-0016. Replaced raster OCR with a pinned PDF text-layer reading, retired hand repair and LLM adequacy review, limited the experiment to five identities, isolated it on Core 1611944, made a fresh model session the sole population producer, and rebound queries to ontology types rather than a fixed graph closure.

Reason: The retained OCR corrupted CO2 in question-critical text, the reviewer and hand repair introduced an experimenter-mediated result, the existing query binding fixed the graph before model population, and the shared checkout did not preserve the claimed Core baseline.

### PV-0010

Date: 2026-09-02

Plan version: 1.0.0

Change: Superseded only the Core coordinate in D-0014. Rebound the isolated paper branch to Core `f9052b4783100203318d4a21a0236f3851218af1`, admitted the published Small Shop correction tag as bounded component evidence, and admitted the later private KnowledgeChangeSet composer as a private implementation seam. Isolation, the ignored PDF, five paper identities, model inputs, and experiment order remain unchanged.

Reason: Luis explicitly approved the rebind after Core passed its local and remote publication gates. The newer baseline contains the completed correction evidence and a domain-neutral private composer needed by a second real consumer, without creating a public API or stable wire claim.

## Author decisions already expressed

### D-0001

Status: accepted

Decision: Optimize for a lean arXiv submission at roughly 80 percent of the larger research program.

Source: Author request, 2026-09-02.

### D-0002

Status: accepted

Decision: Keep the paper simple, use clean language, minimize jargon, and write the manuscript while the engineering evidence is produced.

Source: Author request, 2026-09-02.

### D-0003

Status: accepted

Decision: Center the explanation on the Malleus protocol, ontology, enforced intermediate representation, semantic ledger, construction grammar, and replay-derived knowledge graph.

Source: Author request, 2026-09-02.

### D-0004

Status: accepted

Decision: Investigate a single domain PDF as the primary thin end-to-end case and reuse Small Shop rather than rebuild it.

Source: Author request, 2026-09-02.

### D-0005

Status: accepted

Decision: Maintain a master plan, raw paper ledger, plan changelog, and manuscript from the first pass.

Source: Author request, 2026-09-02.

### D-0006

Status: accepted with implementation boundary recorded

Decision: Use `malleus-ocr` in the single-document path as the reading evidence-integrity gate.

Source: Author clarification, 2026-09-02.

Boundary: Malleus OCR verifies a portable bundle produced by an external renderer and reading engine. It is not itself the PDF ingestion or perception engine.

## Open decisions

### OD-0001

Status: author decision required

Question: Which source document should anchor the primary case?

Current options: the 2025 Mid-Atlantic Ridge paper, the 2001 USGS Project PROBES report, the 2026 western Ionian Sea catalogue paper, or another document evaluated against the same selection criteria.

Current evidence-based recommendation: the Mid-Atlantic Ridge paper. It is compact, open access, visually and scientifically interesting, and offers several distinct ontology elements without requiring a large external dataset.

### OD-0002

Status: author decision required

Question: Should the paper use the implemented native graph query API or add a SPARQL projection and runner?

Tradeoff: native queries keep the paper thin. SPARQL gives readers a standard query language but adds implementation and conformance scope. Cypher has no current implementation advantage.

### OD-0003

Status: author decision required

Question: Must GraphRecipe be composed into the document-to-ledger path before submission?

Tradeoff: composing it makes the grammar a demonstrated part of the central path. Leaving it separate allows faster execution but weakens the central grammar claim to design plus component evidence.

### OD-0004

Status: author decision required

Question: Which reading emitter should cross the Malleus OCR evidence boundary?

Option A: render pages and use a real raster-to-text OCR engine, preserving the current raster and region semantics. This is the faithful use of the existing profile but adds a rendering and OCR runtime.

Option B: use the born-digital PDF text layer and define a sibling reading profile with a text-layer representation and block selector. This suits a text-native paper but is materially new profile work.

Rejected shortcut: do not label text-layer extraction as if it read raster pixels.

## Resolutions of the recorded open decisions

The four questions above remain as historical records. The following decisions supersede their open status.

### D-0007

Status: accepted

Decision: Use the 2025 Nature Communications paper, *Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*, as the primary document case.

Source: Author instruction to assume the pending choices accepted, 2026-09-02.

### D-0008

Status: accepted

Decision: Use native Malleus Python queries. Do not add SPARQL or Cypher to paper four.

Source: Author instruction to assume the pending choices accepted, 2026-09-02.

### D-0009

Status: accepted

Decision: Compose GraphRecipe into the central document-to-ledger path. Implement the missing adapter in the paper experiment against a pinned Core baseline.

Source: Author instruction to assume the pending choices accepted, 2026-09-02.

### D-0010

Status: accepted

Decision: Use a faithful raster-to-text reading emitter through the existing Malleus OCR evidence profile. Do not create a born-digital sibling profile for paper four.

Source: Author instruction to assume the pending choices accepted, 2026-09-02.

### D-0011

Status: accepted

Decision: Use the PDF text layer through pinned `pypdf==6.16.2`, freeze one selected-reading digest, rebuild the block projection, and rebind oracle locators in evaluator-only storage. Raster, Tesseract, and `malleus-ocr` leave the active paper path. This supersedes D-0006 and D-0010.

Source: Author decision via overseer session, 2026-09-02

### D-0012

Status: accepted

Decision: Re-run ontology acquisition in a fresh session from the clean selected reading. Return exact compiler diagnostics to that session at most twice. Do not hand-repair the result. Retire the recovery ontology and Tesseract-era result from active evidence.

Source: Author decision via overseer session, 2026-09-02

### D-0013

Status: accepted

Decision: Freeze exactly five identity groups: source PDF, selected reading, selected ontology, ledger head plus replay receipt, and query binding. Keep one retained artifact per producing step, add tests only for real error classes, copy model-visible inputs instead of pinning living shared files, stop hostile reviews, bump the plan only for author decisions, and target a manuscript of about 3,500 words.

Source: Author decision via overseer session, 2026-09-02

### D-0014

Status: accepted

Decision: Run the experiment in an isolated clean checkout of Core `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`. Never commit the PDF. Ignore `paper-v4/source/*.pdf` and `__pycache__/`.

Source: Author decision via overseer session, 2026-09-02

### D-0015

Status: accepted

Decision: Give a fresh population session the selected ontology, selected reading, generic recipe library, and four questions. Require one population file with a block locator per value. Permit one structural retry. Use no evaluator-authored population and no fallback. Count natural refusals as negative cases before adding planned synthetic mutations.

Source: Author decision via overseer session, 2026-09-02

### D-0016

Status: accepted

Decision: Remove the ontology adequacy rubric and reviewer. The compiler is the ontology gate. Record one evaluator acceptance event with ontology digest and actor id. Bind queries only to record types, relation types, and enum values. Run queries against replayed graph state, then score separately against the sealed oracle.

Source: Author decision via overseer session, 2026-09-02

### D-0017

Status: accepted

Decision: Supersede D-0014 only as to its Core coordinate. Keep the work isolated on `codex/paper-v4-lean`, but rebind it to Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. The paper may consume and cite research tag `research/small-shop-correction-replay-v1` and the later private KnowledgeChangeSet composer, with no package-release, public-API, stable-wire, or general correction claim.

Source: Author decision via Malleus Core coordination, 2026-09-02

### D-0018

Status: accepted

Decision: Preserve the completed question-conditioned document run at commit `746a48b430a881fb683056330438562185e2fabb` as immutable historical evidence and create a versioned corrected run from ontology acquisition. The corrected ontology session receives the selected reading and generic Malleus ontology-construction constraints, but no competency questions, answer key, question-derived semantic checklist, or instruction to produce a question-sufficient ontology. The four frozen questions enter only after ontology compilation, for adopter-owned query binding, population, and source-grounded evaluation. Query surfaces are replaceable descendants of replayed graph state and do not enter the KnowledgeChangeSet evidence closure, ledger identity, or replay identity. Retire automated exact-match scoring and active oracle consumption. Evaluate returned graph rows through a separately frozen source-grounded inspection method with no numeric score, no answer-key comparison, and no graph repair. Codex may prepare a preliminary evidence inspection, but only an identified human may ratify the final record as human-reviewed. Core owns the replay-derived knowledge graph and its general read seams; the paper owns its questions, adapters, evaluation method, and schemas. Do not add Cypher or another query engine unless the existing Core read seam proves insufficient.

Source: Author architecture correction and boundary-2 selection via direct paper instruction and Malleus Core coordination, 2026-09-03.

## Raw findings

### E-0001, request boundary

Date: 2026-09-02

Observation: The author wants leverage for active interviews and offers, so release latency matters. The stated standard is a clear 80 percent contribution, not a maximal research system.

Impact: Prefer one inspectable case and a narrow claim over multiple half-integrated features.

### E-0002, April paper lineage

Date: 2026-09-02

Sources: `private/paper_thesis_April2026.md`, `private/paper_draft_for_review.md`, ignored `paper/paper.md`, and `experiments/journal/2026-04-08_paper_vs_reality.md`.

Observation: The first substantive paper studied multi-turn coherence across tool conditions. Its own later analysis reports that the baseline often beat tool conditions, C5 did not reliably beat C4, and the scenario measured memorized pharmacology more than stateful reasoning.

Impact: Do not reuse its efficacy claims or old result numbers. Reuse its discipline around fair controls, external scoring, retry limits, and failure accounting.

### E-0003, Malleus Moving lineage

Date: 2026-09-02

Sources: `/Users/luis/Projects/malleus-paper/malleus-moving/manuscript/ARGUMENT.md`, its claim-evidence matrix, and `malleus-moving/INQUISITION_PAPER_R1.md`.

Observation: This lineage produced the cleanest conceptual sentence: "The model proposes. Malleus governs commitment." Its hostile audit found stale Prolog descriptions, a wrong refusal denominator, lost or mutable evidence, and novelty claims stated more strongly than the evidence allowed.

Impact: Reuse the proposal-versus-commitment frame and the claim-evidence discipline. Every numerical statement in the new manuscript needs a retained primary artifact.

### E-0004, protocol rebuild lineage

Date: 2026-09-02

Sources: `/Users/luis/Projects/malleus-paper/paper-rebuild/MANUSCRIPT.md`, `NARRATIVE.md`, `EVIDENCE_FREEZE.md`, and `MISSING_ARTIFACTS.md`.

Observation: The rebuild drafted an abstract and introduction around typed proposals, explicit checks, acceptance, atomic commitment, and provenance. It also records five missing primary artifacts. Earlier controlled document and model results whose raw requests, responses, or ledgers are missing are classified as `REPORTED_SUMMARY_ONLY` and `LOST_PRIMARY_ARTIFACT`. Its full invoice and controlled-action lifecycle is broader than the current paper needs.

Impact: Preserve its truth boundary and proposal language. Drop the invoice narrative and action lifecycle from the main paper. No paper-four number or empirical claim may derive from the missing artifacts.

### E-0005, third dojo lineage

Date: 2026-09-02

Sources: `/Users/luis/Projects/malleus-paper-dojo/paper-dojo/MANUSCRIPT.md`, `CHARTER.md`, `THESIS_CANDIDATES.md`, and `CLAIM_EVIDENCE_LEDGER.md`.

Observation: The manuscript contains only a header and status. The third dojo did not start substantive paper prose. Its gate system and constructed-healthcare direction accumulated useful boundaries but blocked every planned manuscript claim.

Impact: Do not inherit the release ceremony. Retain the exact-claim, nonclaim, falsifier, and evidence-identity habits.

### E-0006, current Small Shop vertical

Date: 2026-09-02

Sources: `docs/index.md`, `docs/contract_compiler/index.md`, `research/ontology_driven_kg_realization/experiments/small_shop/pareto/ret010.py`, `test_vertical.py`, and `ret-010-research-receipt.json`.

Observation: RET-010 is the only current research path that composes retained source bytes, ontology compilation, neutral contract facts, explicit mapping, an immutable knowledge change, one protocol history, replay, and graph queries. The retained result contains 735 canonical facts, 25 ledger events, two entities, and one relation. The completion record reports 140 focused passing tests. Its invalid source-bundle cases refuse before ledger creation, and its two check outcomes are fixture-supplied.

Boundary: It is a private, create-only research slice. Python owns several semantics. Check outcomes are fixture-supplied. It does not use GraphRecipe, Prolog, effects, correction, or Semantic Re-entry.

Impact: Use RET-010 as the deterministic backbone and engineering control, not as proof of a general compiler, executed check layer, or policy-level rejection path.

### E-0007, current contract and protocol distinction

Date: 2026-09-02

Sources: `docs/ASSENT_PROTOCOL.md`, `docs/KNOWLEDGE_GRAPH_PROTOCOL.md`, and `design/contract_compiler/overseer/status.md`.

Observation: The intended target is one immutable `KnowledgeChangeSet`, one authoritative semantic and protocol ledger, and a replay-derived accepted temporal graph. Public runtime paths still contain earlier candidate and accepted-application mechanisms; the final-identity path is research-local.

Impact: Describe the demonstrated research composition exactly. Do not present every public Malleus path as already cut over to the final protocol.

### E-0008, GraphRecipe status

Date: 2026-09-02

Sources: `design/GRAPH_RECIPE_OTTR_PROFILE.md` and `research/ontology_driven_kg_realization/experiments/graph_recipe/`.

Observation: Malleus selected stOTTR 0.1.4 as the only authored GraphRecipe syntax. A research-local conformance slice lowers small recipes to ordered proposed operations and tests positive and negative cases. It currently stages through the public graph path, not RET-010's final-identity knowledge-change and ledger path.

Impact: The grammar-to-ledger bridge is the main missing seam if grammar is part of the central paper claim.

### E-0009, query status

Date: 2026-09-02

Sources: `src/malleus/kg.py` and RET-010's canonical receipt.

Observation: The graph supports deterministic native entity and relation queries. No Cypher engine, Neo4j adapter, SPARQL endpoint, or domain-graph RDF projection exists.

Impact: The first paper must choose one query surface. It cannot show Cypher or SPARQL as current functionality.

### E-0010, Recon status

Date: 2026-09-02

Sources: `docs/RECON_CONTRACT.md`, `.claude/skills/malleus-recon/SKILL.md`, and `src/malleus/recon/`.

Observation: Recon records literature sources, claims, evidence, comparisons, revisions, and derived artifacts. It does not download PDFs, extract text, induce an ontology, decide truth, or populate the accepted Malleus graph.

Impact: Use Recon beside the document experiment as its research and evidence log. Do not draw Recon inside the ingestion pipeline.

### E-0011, Prolog status

Date: 2026-09-02

Sources: `src/malleus/logic.py`, `src/malleus/prolog_verifier.py`, `tests/test_logic.py`, and `tests/test_prolog_verifier.py`.

Observation: Malleus has working graph-fact and trusted local Prolog verification primitives. RET-010 does not use them. SWI-Prolog is an external dependency not fully captured by the Python project configuration.

Impact: Prolog is optional for this paper. If used, its installation and exact rule program must be configuration-controlled and it must exercise a real case-specific failure.

### E-0012, Semantic Re-entry status

Date: 2026-09-02

Sources: Codex task `Malleus-semantic-reentry` and current repository delimitations.

Observation: Re-entry is deliberately frozen at design stage. The current Small Shop fixture lacks the quantities, demand, supply-gap, and amendment actions needed for the discussed `1Y` to `2Y` story. A simulated external action would not establish a world change; only new observed source bytes could support another accepted change.

Impact: Re-entry is future work for paper four. Calling the current update or migration primitives Re-entry would be false.

### E-0013, Malleus Core task

Date: 2026-09-02

Source: Codex task `Malleus Core`, formerly `REview Malleus worktrees now Malleus Core`.

Observation: The task completed and tagged the private Small Shop compiler-to-ledger-to-KG milestone, then continued governance work. The active checkout contains unrelated uncommitted Core changes. The latest authority-grant evolution changed persisted identities and is still exercising older fixtures.

Impact: Pin paper evidence to clean retained commits or tags. Do not build result claims on mutable working-tree state.

### E-0014, Malleus-code task

Date: 2026-09-02

Source: Codex task `Malleus-code`.

Observation: Its task report describes a retained historical accepted ledger with 84 events, 346,394 bytes, and a digest beginning `sha256:a521460`. The task established that evidence acceptance and action authorization are separate. A proposed action must be present in the original proposal, and the frontier needs a matching `AUTHORIZED` action state. Its next production step depends on exact Core authority-grant coordinates and a fresh ledger epoch.

Impact: Reuse the conceptual separation in limitations or future work. Do not make this unfinished cross-worktree integration a dependency of the lean paper.

### E-0015, current reproducibility mismatch

Date: 2026-09-02

Source: current environment audit by the Core evidence subtask.

Observation: The private compiler and Small Shop tests currently encounter LinkML `1.10.0.post230.dev0+2909900a4` and LinkML Runtime 1.10.0 while project configuration pins both to 1.11.1. The version guard fails with `TRUSTED_MODULE_MISMATCH`, followed by `IMPORT_READER_REFUSED`. Focused results were: validated contract, 2 passed and 16 failed; knowledge-change history, 2 passed and 45 failed; Small Shop vertical, 18 passed and 10 failed. Passing focused groups were: public protocol, 220; ontology, 163 with 2 skipped; KG, 107; Prolog, 39; Recon, 24; OCR audit, 152; LLM runner and session wiring, 37; machine-readable status, 12; private protocol machine, 48; GraphRecipe, 40.

Impact: Separate historical milestone evidence from a fresh reproduction claim. Repair the dependency through project configuration, then run the paper experiment from a clean environment.

### E-0016, documentation drift

Date: 2026-09-02

Source: current repository evidence audit.

Observation: `docs/IMPLEMENTATION_STATUS.md` still names Assent ontology 0.9.0 while `ontology/assent.yaml` and machine status report 0.11.0. The OCR package docstring says review-report recording is unimplemented while current status and handlers show it implemented. The retained GraphRecipe report also binds historical release and suite identities rather than current package 0.13.3.

Impact: Repair or explicitly freeze documentation versions before using implementation-status prose as paper evidence. Prefer exact source and current test artifacts over drifting summary pages.

### E-0017, ontology circularity and admission boundary

Date: 2026-09-02

Observation: Letting one model proposal define both the ontology and the facts that satisfy it would make structural compilation a weak adequacy test. Many ontology decompositions may be valid, so a single hidden gold ontology is also inappropriate.

Impact: Split the run into ontology proposal and population stages. Freeze an independent adequacy rubric, name the reviewer who selects one exact ontology digest for the experiment, and restart review and selection after any ontology edit. Keep the fact and answer oracle hidden. Do not present this selection record as a private semantic-history event.

### E-0018, stage-specific refusal semantics

Date: 2026-09-02

Observation: "Rejection leaves the ledger unchanged" is false for a retained protocol decision. Compiler refusal adds no semantic event. Protocol `REJECT` or `DEFER` grows the ledger while leaving accepted state fixed. A failed combined `ACCEPT` and application appends nothing.

Impact: Report ledger, acceptance, and graph heads separately for every negative case. Do not use RET-010's pre-admission source refusals as evidence of policy rejection.

### E-0019, prior empirical failure disclosure

Date: 2026-09-02

Observation: The April coherence pilot found that the baseline often beat structured conditions and that the scenario was not a clean stateful-reasoning test.

Impact: Disclose this as motivation for the narrower conformance paper. Reuse no prior efficacy number.

### E-0020, no-embedding mechanical condition

Date: 2026-09-02

Observation: Merely saying that the system did not use embeddings would be an unchecked process claim.

Impact: Isolate query execution with only ledger and query definitions, deny network access, remove document and proposal artifacts, and install failing sentinels at source-reading and embedding entry points.

### E-0021, source document reconnaissance

Date: 2026-09-02

Observation: The strongest initial candidate is the open-access 2025 Nature Communications paper on deep mantle earthquakes and CO2 degassing at the Mid-Atlantic Ridge. It is 11 pages and exposes a compact set of regions, instruments, earthquake groups, depths, concentrations, observations, and hypotheses. USGS Project PROBES is more operational but longer. The 2026 Ionian Sea catalogue offers structured validation but widens the data scope.

Impact: Ask the author to select the source before building extraction or ontology artifacts.

### E-0022, anti-RAG boundary

Date: 2026-09-02

Observation: A single document and a few structured queries cannot establish that embedding RAG is generally unnecessary. It can establish that the selected answers were obtained from replayed typed state without building or consulting an embedding index.

Impact: Use the bounded sentence in the thesis. A comparative RAG claim requires a matched baseline, broader query classes, and error analysis, which are outside the lean paper.

### E-0023, first-pass paper artifacts

Date: 2026-09-02

Observation: Created `paper-master-plan.md`, `paper-ledger.md`, and `manuscript.md` under `paper-v4/`.

Impact: Future paper work should update these artifacts in the same change. The manuscript now exists before the document experiment, with unsupported result slots marked explicitly.

### E-0024, configured environment correction

Date: 2026-09-02

Observation: E-0015 tested the default Conda interpreter, not the repository's configured `.venv`. The default interpreter contains the wrong LinkML versions and correctly triggers the compiler identity guard. The `.venv` contains LinkML and LinkML Runtime 1.11.1. Running `test_validated_contract.py`, `test_knowledge_change_history.py`, and the Small Shop `test_vertical.py` together under `.venv` produced 93 passing tests in 13.06 seconds.

Impact: The dependency guard and configured private path both behave as intended. A clean-environment receipt tied to the final paper commit is still required.

### E-0025, public and private decision histories

Date: 2026-09-02

Observation: E-0018 describes the public Assent `ProtocolLedger`, which can retain `REJECT` and `DEFER`. The private `KnowledgeChangeHistory` used by RET-010 is separate, imports none of the public Assent, accepted-graph, or staging modules, and admits only a complete sequence ending in `ACCEPT`. A non-accepting outcome or failed application leaves private semantic history unchanged.

Impact: The document experiment follows the private accepted-only behavior and retains unsuccessful candidates in a separate experiment evidence log. Do not describe public Assent and private semantic history as one composed runtime.

### E-0026, query-isolation correction

Date: 2026-09-02

Observation: E-0020 proposed giving the query process the private ledger while claiming source text was inaccessible. That ledger embeds retained source bytes, and replay decodes them.

Impact: Use two processes. Replay receives the source-bearing ledger and emits a bound graph snapshot. Query receives only that snapshot and frozen queries. A separate scorer receives query output and the hidden oracle.

### E-0027, per-fact provenance gap

Date: 2026-09-02

Observation: `KnowledgeChangeSet` currently binds a change-level evidence closure, while projected operations contain no enforced property-to-locator association and the graph does not gain automatic provenance edges.

Impact: Add a validated operation/property-to-locator artifact, retain its identity in the change evidence closure, and prove that each accepted record can be traced to a canonical page and hashed text block after replay. Until then, say "change linked to an evidence bundle," not "evidence-linked graph."

### E-0028, RET-010 fact-count evidence gap

Date: 2026-09-02

Observation: Repository documentation reports 735 neutral contract facts, but the canonical RET-010 receipt retains the fact-set digest rather than the count or compiled fact artifact.

Impact: Freeze a machine-readable fact count or the compiled artifact before 735 appears as a final paper result.

### E-0029, Malleus-code evidence eligibility

Date: 2026-09-02

Observation: The event count, byte count, and digest prefix in E-0014 came from a task report and are not backed by an artifact in this repository.

Impact: They are context only and are ineligible for the manuscript until the exact external artifact or retained task output is frozen.

### E-0030, source-artifact distinction

Date: 2026-09-02

Observation: The public `SourceArtifact` stores caller-declared identity metadata and does not fetch or authenticate bytes. The private semantic history separately retains exact source bytes and verifies them against the declared identity.

Impact: Keep publisher authenticity, public source metadata, private retained bytes, and byte-integrity checks as distinct claims.

### E-0031, ontology scoring simplification

Date: 2026-09-02

Observation: Fact-level recall is not well-defined when the model may choose among multiple valid ontology decompositions unless the evaluation imposes a reference decomposition and alignment rules.

Impact: Drop fact precision and recall. Score the frozen questions, classify every accepted property and relation as supported or unsupported, measure locator coverage, and report the ontology adequacy decision.

### E-0032, adequacy failure policy

Date: 2026-09-02

Observation: A hidden adequacy rubric conflicts with reviewer-guided ontology retries.

Impact: Permit only structural compiler-diagnostic retries within the one primary session. Apply the hidden adequacy rubric once to the final structurally valid ontology. Failure terminates the primary run.

### E-0033, query-package binding

Date: 2026-09-02

Observation: An isolated graph snapshot could be substituted unless it is bound to the actual replay result.

Impact: The graph projection package must carry and verify the source ledger head, replay receipt identity, contract identity, and graph-state digest before query execution.

### E-0034, actor and authority distinction

Date: 2026-09-02

Observation: RET-010 records an actor identifier but performs no authority or eligibility check. Public policy legitimacy and scope are separate unsolved questions.

Impact: Say "recorded actor" and "identified policy," not that an authorized actor admitted the change.

### E-0035, projection-package implementation gap

Date: 2026-09-02

Observation: Private replay currently returns an in-memory graph, contract view, and retained inputs. The source-free bound graph projection package proposed for query isolation has no schema, loader, canonical identity, or tests today.

Impact: Treat the package as required new implementation, never current capability.

### E-0036, local environment evidence boundary

Date: 2026-09-02

Observation: The default Conda LinkML version is `1.10.0.post230.dev0+2909900a4`, not a plain 1.10.0 release. The local `.venv` conforms to project pins and passes the focused path, but the directory itself is not a retained environment artifact.

Impact: Retain configuration, clean-environment identity, and a final reproduction receipt rather than citing the local environment as a reproducible artifact.

### E-0037, focused reproduction coordinates

Date: 2026-09-02

Observation: The 93-test focused run used repository HEAD `1f587ee354304ef58084bb12c9a829d696eca834` in an already dirty shared checkout, with local `.venv` LinkML and LinkML Runtime both at 1.11.1. The test process exited successfully in 13.06 seconds.

Impact: This is current corroborating evidence, not the final clean reproduction receipt and not authority over the historical tagged milestone.

### E-0038, Malleus OCR added to the paper path

Date: 2026-09-02

Observation: The author identified `malleus-ocr` as the missing document-side capability. Repository inspection confirms that it provides the right evidence-integrity vocabulary and verifier, but not perception.

Impact: The paper pipeline now starts with external reading acquisition followed by Malleus OCR verification. Recon remains beside the experiment as the research record.

### E-0039, exact OCR implementation boundary

Date: 2026-09-02

Sources: `src/malleus/ocr/__init__.py`, `src/malleus/ocr/bundle.py`, `src/malleus/ocr/verify.py`, `ontology/domains/ocr.yaml`, and `docs/IMPLEMENTATION_STATUS.md`.

Observation: Capability is `AUDIT_ONLY`. The profile has nine typed classes, a portable bundle document, distinct source, raster, region, attempt, hypothesis, review, and selection planes, precommitted source-class and policy records, a three-valued unit census, and 17 diagnostics. It renders nothing, calls no provider, retains only text digests inside the bundle, does not recompute a declared source digest from supplied external bytes, does not judge transcription truth, and writes nothing to a protocol ledger. No production OCR adapter has crossed the boundary.

Verification: Under the local repository `.venv`, `tests/test_ocr.py` passed 152 tests in 2.82 seconds on 2026-09-02.

Impact: Build one real, configuration-declared emitter; retain raw and selected text outside the bundle under policy; add an external-byte integrity receipt; and bind the verified bundle plus selected reading into the document experiment.

### E-0040, Core baseline correction

Date: 2026-09-02

Sources: Codex task `Malleus Core`, Git commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, and current repository state.

Observation: E-0013 described the authority-grant work while it was in progress. It is now complete and published at tree `657ba6ce1be83064d104803ad5dad644d65b4352`. Assent ontology 0.11.0 requires identity-bearing `scope_record_id` and `may_subdelegate`. The recorded grammar-4 semantic identity is `sha256:e62fcea2c480e62176346bdc6fa10ae9954418b1d3a8ee6409f0fac104b6ba54`.

Impact: Pin the document experiment to this Core coordinate and start a fresh empty ledger. Do not reinterpret an older accepted ledger under the new ontology. No further authority-grant or ontology-transition work blocks paper four.

### E-0041, GraphRecipe and private-history composition ownership

Date: 2026-09-02

Sources: `research/ontology_driven_kg_realization/experiments/graph_recipe/assembly.py`, `src/malleus/_contract_pipeline/knowledge.py`, architecture tests, and current focused verification.

Observation: `AssemblyPlan` already exposes ordered `ProposedOperation` values, member identities, dependency edges, lineage, and a plan digest. `KnowledgeChangeSet.from_bytes` accepts the corresponding canonical create-entity and create-relation form. `KnowledgeChangeHistory` already exposes replay coordinates, atomic `admit`, and `reopen(...).replay()`. An architecture guard keeps GraphRecipe and public staging out of the private history module. At current HEAD, the GraphRecipe and private knowledge-history suites passed together: 87 tests in 7.64 seconds.

Impact: Core needs no new feature. The paper experiment owns a thin adapter from `AssemblyPlan` to canonical `KnowledgeChangeSet` bytes, plus positive, replay, refusal, and no-direct-staging tests. Signals and events remain unsupported in this bridge because private change-set v0 accepts only entity and relation creation.

### E-0042, machine-readable Core freeze

Date: 2026-09-02

Sources: `paper-v4/experiment/core-baseline.json` and `paper-v4/experiment/test_core_baseline.py`.

Observation: The freeze records commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`, Assent ontology 0.11.0, exact ontology source digest `sha256:90830170573b52d7c73debb83c89bb278087607880675964e670d68fd7a1e234`, grammar 4, semantic identity `sha256:e62fcea2c480e62176346bdc6fa10ae9954418b1d3a8ee6409f0fac104b6ba54`, and a fresh `GENESIS` ledger epoch. The guard re-reads the ontology bytes from the pinned commit and recomputes the semantic identity.

Impact: The paper has all Core coordinates it needs. Later Core work is excluded unless the paper deliberately changes its baseline and plan version.

### E-0043, selected publisher PDF freeze and license correction

Date: 2026-09-02

Sources: `paper-v4/source/source-manifest.json`, `paper-v4/source/yu-et-al-2025-mid-atlantic-ridge.pdf`, the Nature Communications article page, and the Creative Commons deed.

Observation: The exact publisher PDF for Yu et al. is 6,921,046 bytes, PDF 1.4, unencrypted, contains no JavaScript, and has 11 pages. Its digest is `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`. All pages were rendered and visually inspected for completeness. The article is licensed CC BY-NC-ND 4.0, not CC BY.

Impact: The experiment source is fixed. The paper will cite or link the publisher copy. A transformed full-text OCR corpus will not enter the public artifact without separate rights review.

### E-0044, first bridge gate exposed an alignment hole

Date: 2026-09-02

Sources: first revision of `graph_recipe_change_set.py`, its focused tests, and independent adversarial review.

Observation: The first adapter revision reproduced the plan digest and checked only set equality between construction members and operation member IDs. Swapping the first two GE-020 operations and recomputing a self-consistent plan digest therefore assigned each operation to the wrong member while still producing a change set. The initial passing gate was insufficient and is not evidence.

Impact: A plan digest establishes byte identity, not semantic alignment among its fields. The adapter now needs a mechanical per-position member-operation invariant and a regression for a self-digested swap.

### E-0045, hardened component bridge result

Date: 2026-09-02

Sources: `research/ontology_driven_kg_realization/experiments/document_paper/graph_recipe_change_set.py`, `test_graph_recipe_change_set.py`, `paper-v4/experiment/bridge-verification.json`, and `test_bridge_freeze.py`.

Observation: The corrected adapter requires each ordered operation to match its retained construction member on record identity and the closed operation-kind mapping. Self-digested tests independently exercise record-identity and supported operation-kind mismatch; signal and event changes remain unsupported. The architecture gate rejects direct imports or references to public staging and graph mutation surfaces. The positive GE-020 component plan admits through `KnowledgeChangeHistory`; reopen and replay reproduce the same canonical receipt and graph. Stale-base and invalid-relation attempts leave ledger bytes, graph state, and machine state unchanged. The combined source-freeze, Core-freeze, bridge, private-history, and GraphRecipe gate passed 100 tests in 8.08 seconds, and Ruff passed, under the configured local `.venv` with Python 3.12.9, LinkML 1.11.1, and LinkML Runtime 1.11.1.

Impact: The grammar-to-history seam is implemented as paper-local component evidence. The test uses a GraphRecipe fixture ontology and a separately compiled compatible history contract, so it does not prove same-ontology continuity or the PDF result. Those remain required in the document runner.

## Claim and evidence register

### C-0001

Claim: Malleus separates generated proposals from accepted graph state in the implemented public protocol primitives and private RET-010 profile.

Status: supported in current implementation and protocol artifacts.

Evidence: protocol state machines, accepted graph tests, Small Shop RET-010.

Forbidden inference: accepted state is true in the external world.

### C-0002

Claim: The private RET-010 slice reconstructs the same accepted graph and canonical receipt from its retained JSONL history without rereading ambient fixture, mapping, machine, or policy files.

Status: supported by retained test and completion artifacts. The configured `.venv` passed the three focused private files on 2026-09-02; a clean final-commit receipt remains pending.

Evidence: `docs/index.md`, `ret-010-research-receipt.json`, and RET-010 replay tests.

Forbidden inference: the ledger is tamper-proof or sufficient without a compatible runtime.

### C-0003

Claim: Malleus has an enforced frontend-neutral contract representation and final-identity knowledge-change representation in the private research path.

Status: supported, research-local.

Evidence: `src/malleus/_contract_pipeline/`, private compiler tests, RET-010.

Forbidden inference: stable public API or general frontend support.

### C-0004

Claim: Malleus design selects stOTTR 0.1.4, and the research slice implements a restricted stOTTR-derived profile that lowers its bounded corpus to ordered operations.

Status: supported as design plus component implementation.

Evidence: GraphRecipe profile, frozen corpus, component tests.

Forbidden inference: GraphRecipe currently feeds the RET-010 semantic ledger or has established full OTTR conformance.

### C-0005

Claim: One fresh model session can produce an ontology selected under the frozen adequacy rubric and a construction bundle valid against that exact ontology digest.

Status: requires experiment.

Required evidence: isolated acquisition manifest, exact observable context, raw outputs, compiler diagnostics, retry history, adequacy decision, selected ontology digest, and accepted artifacts.

### C-0006

Claim: The replay-derived document graph answers the prespecified questions exactly without embedding retrieval.

Status: requires experiment.

Required evidence: preregistered questions and complete bounded oracle, ontology-bound query specifications frozen before population, per-fact locator map, graph snapshot, isolated query outputs, runtime I/O audit, and replay receipt.

Forbidden inference: Malleus outperforms RAG or answers arbitrary questions.

### C-0007

Claim: Paired valid and invalid document inputs produce their expected outcome, and unsuccessful candidates leave the private semantic history and accepted state unchanged while remaining inspectable in the experiment evidence log.

Status: requires experiment.

Required evidence: frozen paired corpus, before and after experiment-log, semantic-history, acceptance, and graph identities, plus typed diagnostics.

### C-0008

Claim: Malleus supports semantic re-entry for the paper case.

Status: not supported, deferred.

Reason: only design artifacts exist; the observation and accepted-change loop is not implemented.

### C-0009

Claim: Malleus does not need embedding RAG.

Status: prohibited at this scope.

Reason: the proposed case lacks a matched retrieval baseline and general query coverage.

### C-0010

Claim: Malleus determines whether a source claim is true.

Status: prohibited.

Reason: structural validity, retained evidence, and policy acceptance are not truth.

### C-0011

Claim: Malleus OCR verifies typed identity and lineage across a portable document evidence bundle and computes declared coverage outcomes.

Status: supported at capability `AUDIT_ONLY`; the focused suite passed 152 tests.

Evidence: OCR ontology, bundle carrier, verifier, CLI, status documentation, and `tests/test_ocr.py`.

Forbidden inference: Malleus OCR renders pages, performs OCR, validates external PDF bytes by recomputing their digest, stores selected text bytes, proves transcription accuracy, or writes to the semantic history.

### C-0012

Claim: The paper's selected PDF can be rendered and read into a conforming Malleus OCR bundle whose selected text is retained and admitted into the downstream evidence closure.

Status: requires experiment.

Required evidence: declared renderer and reading engine, configuration-managed dependencies, frozen source class and policies, exact requests and responses, portable bundle, OCR verification result, selected text bytes, source-integrity receipt, and downstream binding identity.

### C-0013

Claim: A bounded GraphRecipe entity-and-relation plan can be converted into a final-identity private `KnowledgeChangeSet`, admitted without direct staging, and reconstructed to the same graph and receipt after reopening history.

Status: supported as component evidence at the frozen paper-local adapter revision.

Evidence: E-0044 and E-0045, including the repaired member-operation alignment guards and 100-test combined gate.

Forbidden inference: the selected PDF ontology, source locators, or document-derived facts have completed this path.

## Next entry contract

The next paper change should append the frozen source class, renderer and reading-emitter contract, exact OCR outputs, competency questions, answer oracle, and same-ontology document-runner result. The clean-environment reproduction outcome remains required. Any change to the central experiment or main claim must bump the master plan.

### E-0046, OCR precommit frozen before retained reading

Date: 2026-09-02

Sources: `paper-v4/experiment/ocr-precommit.json`, `test_ocr_precommit.py`, exact local renderer and reader binaries, and the frozen source PDF.

Observation: The retained run is fixed to all 11 PDF pages, 300 dpi lossless PNG rendering with `pdftoppm` 26.03.0, and local English Tesseract 5.5.2 with one machine hypothesis and selection per complete page. The precommit digest is `sha256:68580e74a1107af8b0de033f664fb5053d7c1ffd3ec14c53508d06c79f36fbda`. It pins renderer, reader, trained-data, source, and OCR-ontology identities; forbids network, PDF text-layer access, `pdftotext`, preprocessing, credentials, and retries; retains raster, request, response, and selected bytes privately; and permits only digest-bearing public output. The current reproducibility claim is exact local binaries, not a clean container.

Correction: An exploratory all-page OCR probe happened before this precommit. It checked feasibility and produced no retained output. It is excluded from evidence and cannot be described as the scored or retained run.

Impact: The official emitter must consume this exact precommit once, refuse drift, publish nothing on partial failure, and expose no derived full text in public artifacts.

### E-0047, OCR profile requires a paper-local chain guard

Date: 2026-09-02

Sources: `src/malleus/ocr/verify.py`, the public OCR conformance corpus, and an adversarial bundle construction during the paper audit.

Observation: The public v0 verifier resolves a hypothesis `attempt_id` but does not require that the resolved attempt and hypothesis name the same region. A conforming-shaped bundle can therefore reuse one attempt as the origin of hypotheses for other page regions. The literal public-profile minimum for the 11-page case is smaller than the faithful one-chain-per-page experiment contract.

Impact: This is a real profile gap. The paper-local emitter must enforce one complete page-specific source to raster to region to attempt to hypothesis to selection chain. The faithful case contains 58 graph records and 56 bundle members: one source class, one source representation, 11 records in each of the five page planes, and one bundle. Cross-region attempt, hypothesis, and selection mutations require hard refusal tests. This guard closes the paper case only; it does not silently upgrade the public OCR profile.

### E-0048, questions and independent evaluation commitments frozen

Date: 2026-09-02

Sources: `paper-v4/experiment/competency-questions.json`, `evaluation-commitments.json`, and the sealed `private/paper-v4-evaluation/` artifacts.

Observation: Four model-visible questions were frozen before model acquisition. They cover acquisition, spatial association, two bounded quantities with units and epistemic status, and the authors' preferred causal hypothesis. Figures, tables, and free-form synthesis are excluded. A separate answer oracle and six-criterion ontology-adequacy rubric were sealed from the proposal producer. Their digests are respectively `sha256:95b206a8a8eac20f208854c2374ed8433187402d9ab1e50771003e412066b571` and `sha256:f73c86e2635afa78661acffc1cc5b8aeca6924d446d4a52e44fc7ac739936a10`; the public question-set digest is `sha256:5ec41374e32a8745963a0f0498e2044f225dec47a6cbfcfde1417752b27b9a92`.

Impact: The proposal task cannot see the oracle or rubric. Ontology review supplies no repair feedback and permits no retry after adequacy scoring. Exact OCR block locators remain to be bound after the retained reading exists.

### E-0049, Recon records the domain investigation

Date: 2026-09-02

Sources: `paper-v4/recon/`, an independent `malleus-recon validate`, two fresh builds outside the workspace, manifest hash checks, and ZIP validation.

Observation: Recon validates 11 ledger events and 11 current records: one evidence attachment, one review target, one work, four claims, and four `HAS_CLAIM` relations. It records zero refusals and zero supersessions. Two fresh builds are byte-identical to each other and to the retained build. The semantic Recon ontology identity is `sha256:58f26c833e4065951467f61c46ba6859609b7be3727ea18a80c4ae5ec6435476`; the ledger head is `sha256:5c1b62cbb0768e6bb485ed5e31f0f4630e53165363e6704e7e6ed1d619bcbdb1`; the ledger, build manifest, and bundle file hashes are respectively `5248068348f628501f39da89e3119394ef0c016825e566d45ac4c6e4d7a214fb`, `a417089fe48a9bf080418f52bddb40a6e55bf03c513f9f4b56250b642580f0c2`, and `5d076e8babeb6f2e8302432524bdab36e83bc88ff90fe835a96d4c261548993f`.

Impact: Recon is now retained evidence for source selection and domain investigation. Its locators are 1-based PDF pages plus phrase or prose anchors. It asserts no OCR block, bounding-box, or pixel locator and remains outside PDF perception, ontology selection, admission, and truth adjudication.

### E-0050, concurrent Small Shop correction is planned, not evidence

Date: 2026-09-02

Source: coordination message from the `Malleus Core` task.

Observation: Core is implementing a bounded sibling Small Shop temporal-correction fixture outside `paper-v4/`. No exact commit, tree, or receipt has been delivered to this paper task. Core explicitly asked that the result not be consumed or claimed while it is in progress.

Impact: Paper four remains pinned to the completed RET-010 and 93-test baseline. The new correction may be evaluated later as optional evidence, but it is not a dependency and cannot change any current manuscript result until exact artifacts arrive and the paper baseline is deliberately revised.

### E-0051, reading-block projection frozen before retained OCR

Date: 2026-09-02

Sources: `paper-v4/experiment/reading-projection-precommit.json` and `test_reading_projection_precommit.py`.

Observation: The block-projection contract was frozen at `2026-09-02T21:45:28Z`, before the official retained OCR run, at `sha256:47319b17cc2e37aab7593b08cc668405badf0caf4b610b8a268335c9fb1c9ee6`. It consumes all 11 selected page files, decodes UTF-8 strictly, normalizes only line endings, and defines a block as a maximal run of nonblank lines. Block bytes preserve line payloads, join them with LF, and add one terminal LF. Ordering and identifiers are fixed. Empty pages and text correction are forbidden.

Impact: Exact selected OCR bytes remain the retained evidence. The deterministic private block projection becomes the model input and locator surface. The public artifact may expose block identities, sizes, and digests, but no OCR text.

### E-0052, prior paper lineages supply framing, not results

Date: 2026-09-02

Sources: the April coherence drafts under `paper/` and `private/`, the archived `paper-rebuild` worktree at commit `18b6b4795ee68d38be0d2a8987807b0f2220c401`, the `paper-dojo` worktree at commit `eb3f0cd969639289dcb5677108cf49319d14a9b7`, and their retained audits and freeze records.

Observation: The April attempt studied multi-turn coherence and contains adverse pilot evidence rather than a completed efficacy result. The second attempt framed Malleus as an executable commitment protocol, but its central synthetic model request, response, and ledger artifacts are missing. The third attempt specified a comparative selective-risk experiment but left the manuscript blocked and ran no provider experiment. None supplies a paper-four empirical result.

Impact: Reuse only the commitment-boundary framing, truth limitation, independent-oracle discipline, load-bearing graph test, and exact evidence-map pattern. Exclude old efficacy claims, stale counts, action and payment scope, healthcare and CYP450 domains, comparative ablations, and any result whose primary artifacts are missing. Paper four needs one figure and three core statements: the model proposes; the ledger is authoritative; protocol conformance is not truth.

### E-0053, official retained OCR run passed

Date: 2026-09-02

Sources: `paper-v4/experiment/ocr-bundle.json`, `ocr-verification.json`, `ocr-execution-receipt.json`, `test_ocr_result_freeze.py`, and the private sidecars under `private/paper-v4-ocr/yu-2025-tesseract-v1/`.

Observation: Official retained run 1 completed at `2026-09-02T21:54:01Z`. The emitter digest was `sha256:082e781046c9c8f560eb867b3537aa4f279cdc2262993ecd512e040d68cf9470`; its focused tests plus the public OCR suite passed 177 tests, and an independent hostile review found no remaining functional blocker. The bundle digest is `sha256:46894b087d09d1a58f7ecac4fa135a6fdfdd80fd4b38078856022dcd44993f1d`; its identity and retained-sidecar closure are `bundle:paper-v4:aa8ef9e5b924e03e44ca33d3e3616b24ed92535b8a4956dee7e46c26fee47315` and `sha256:aa8ef9e5b924e03e44ca33d3e3616b24ed92535b8a4956dee7e46c26fee47315`. The verification digest is `sha256:23fdb70aa763129a29c9f4144a9e5200153f0d1f791366f522152297ed2a05dd`.

Result: All 11 declared pages are `READ` and accounted for. Page coverage is 1.0 against a 1.0 threshold, with `MET`; strict paper-local alignment passes; diagnostics, corrections, failed units, and unattempted units are zero. The bundle has 56 members: one source plus 11 rasters, 11 regions, 11 attempts, 11 hypotheses, and 11 selections. Including the source-class and bundle records yields 58 graph records. The private closure contains 44 files and 20,133,925 bytes. The selected readings contain 63,005 bytes and 9,683 whitespace-delimited words. Response and selected bytes are identical for every page. Public artifacts contain identities, counts, and digests but no selected text.

Independent check: `.venv/bin/malleus-ocr paper-v4/experiment/ocr-bundle.json` exited zero, classified integrity as sound and the claim as `FINISHED_READING`, and reproduced the complete 11-page census without a diagnostic.

Limits: This establishes the declared evidence chain and coverage, not transcription accuracy or source truth. Publication uses compensating rollback for handled rename errors and is not crash-atomic. The run binds exact local binaries; clean-container reproduction remains pending. Derived OCR text remains private pending separate rights review.

### E-0054, minimal related-work set verified

Date: 2026-09-02

Sources: the primary RAG paper; SPIRES; OntoLogX; the W3C PROV-O Recommendation; the 2024 OTTR framework paper; Blue Brain Nexus; Zep; and ActiveGraph.

Observation: The inspected literature already establishes dense-index retrieval, LinkML and ontology-guided LLM extraction, validation and correction before graph persistence, interoperable provenance vocabularies, typed graph templates, append-only graph histories, temporal graph memory, and replay-derived graph projections. Zep and ActiveGraph are preprints; Blue Brain Nexus was first available online before its 2023 journal issue.

Impact: Paper four cannot claim the first schema-guided extraction, validation gate, provenance model, graph template system, temporal KG, append-only semantic history, or replayed graph projection. The defensible comparison is narrower: Malleus tests one executable commitment boundary that binds model proposal bytes, ontology-constrained construction, exact evidence, prior state, checks, verdict, accepted history, and replay. Related work stays at eight core sources and makes no RAG-superiority or production-maturity claim.

### E-0055, selected-reading projection and oracle locators frozen

Date: 2026-09-02

Sources: `reading_projection.py`, its focused tests, `paper-v4/experiment/selected-reading-manifest.json`, `reading-projection-receipt.json`, `evaluation-locator-commitment.json`, and the sealed evaluator artifacts.

Observation: The deterministic projection consumed the exact OCR closure and produced 301 ordered blocks across 11 pages. Its private reading artifact is 111,920 bytes at `sha256:0537411117e73b2611ade5088978ba7c8d8a4467d5b51b0c8941bc47f0d41261`; the digest-only public manifest is 45,472 bytes at `sha256:74399ce57cbe512157c0afdea4bbca946bc2693a3ead69cdfc82b3d6f292c35c`. The implementation is `sha256:6a5c4867fb03191b61135fba32c1a73a6fcf4e22a9b56e0adb33475a625c3428`. Fourteen focused and 191 combined OCR and projection tests passed after hostile review exposed and forced repair of symlink redirection, partial bundle binding, incomplete sidecar validation, and trusted verification-summary defects.

Evaluation binding: A sealed locator artifact now maps all four oracle answers to exact block IDs and hashes; a sealed adjudication guide fixes normalization, exact-answer, support, ambiguity, and locator-coverage rules. The public commitment is `sha256:91ecdc7476c0c7f1b266f617d57295854a5fc312c0922444bad38bc739580f1f`. Both artifacts remain hidden from the proposal producer, and neither review feedback nor review retry is permitted.

Impact: The exact model-visible reading and evaluator-only locator closure now exist. Blocks are deterministic paragraph-like byte projections, not semantic segments. Raw selected page bytes remain authoritative, and public artifacts still expose no OCR text.

### E-0056, fresh-session ontology proposal frozen and dispatched

Date: 2026-09-02

Sources: `paper-v4/experiment/model-acquisition-precommit.json`, `model-acquisition-prompt.md`, `model-ontology-task.md`, and Codex task `01a06430-46af-7bd0-9098-ad857445738f`.

Observation: Before model acquisition, the proposal contract was frozen at `sha256:1590853f951e4e4080e08164cd0aef1fc8b4535b440948951a533388b8e22504`. It fixes a new task with no prior conversation, model `gpt-5.6-sol`, high reasoning effort, seven exact input files and digests, no network, no file writes, no subtasks, one delimited LinkML YAML document, and at most two same-session compiler-diagnostic retries. The answer oracle, locator binding, adequacy rubric, adjudication guide, earlier paper attempts, and Recon record are hidden from the producer. The task was dispatched as `Malleus Paper v4 Ontology Proposal`.

Assumption: The author said to freeze and proceed but did not choose a model or reasoning level. This run fixes the available `gpt-5.6-sol` model at high effort as an experiment coordinate. Provider system instructions, unexposed sampling settings, and service nondeterminism remain uncontrolled. The file-read restriction is an explicit task contract and will be checked from the retained task trace, not a claim of operating-system-enforced isolation.

Impact: No ontology or document result is claimed yet. A structurally invalid proposal may receive only compiler diagnostics in the same session under the frozen retry budget. The hidden adequacy review remains one-shot and supplies no feedback or retry.

### E-0057, Core correction remains outside the paper baseline

Date: 2026-09-02

Source: second coordination message from the `Malleus Core` task.

Observation: Core kept the paper pinned to commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`. Its bounded Small Shop correction proof remains under audit. That audit found mixed time-coordinate supersession, receipt grammar and role closure, and exact source-plus-mapping-to-change-set conformance gaps. Core explicitly withdrew all pre-repair hashes and has not supplied final coordinates.

Impact: The correction remains planned and unclaimed. Its intended narrow current-versus-historical-state result is not evidence for paper four. Semantic Re-entry, demand reasoning, actions and effects, invoice correction, Event nodes, public mapping or API claims, and general valid-time queries remain excluded.

### E-0058, fresh producer needed one compiler correction

Date: 2026-09-02

Sources: Codex task `01a06430-46af-7bd0-9098-ad857445738f`, two retained responses, `model-acquisition-receipt.json`, `ontology-compile-precommit.json`, and `paper-v4/experiment/ontology-compilation/`.

Observation: Candidate 1 was emitted after 289,036 ms with no input-identity drift, network, file write, subtask, or repository read outside the frozen contract and seven-file allowlist. The exact LinkML source reader refused the unsupported root field `default_prefix`. That exact diagnostic alone was returned to the same task. Candidate 2 removed the field and made no other change. It compiled under the official exact three-source harness without using the second permitted correction. The compiled artifact contains 1,632 facts at validated fact-set identity `sha256:8b1aca802746ab7fe487af92a286e1242ae105adda9665ba68388688838ffce2`; the artifact and compiler-receipt file digests are `sha256:cec07ba6cce324e7b3a5867a46818a3249923a1fb1d49577eea78c1717cf1dee` and `sha256:bd10af7086c7efb55478817e55e8c30956efa8c6395f3de574917855fdbf3054`.

Control: A nonretained test-helper probe was used to decide whether another producer correction was needed. It was disclosed before the official retained compiler run and is excluded in favor of the exact harness result. The official harness refuses input drift, unknown imports, unsupported fields, overwrite, and partial publication; its focused plus acquisition checks passed 11 tests.

Impact: The first structurally valid candidate now exists. It is not yet selected or accepted knowledge. The one-shot hidden adequacy review remains the next gate.

### E-0059, compiled IR now feeds GraphRecipe directly

Date: 2026-09-02

Sources: `compiled_graph_recipe_contract.py`, `test_compiled_graph_recipe_contract.py`, and an independent code-path audit.

Observation: The pre-existing GraphRecipe contract projector could not consume this paper ontology: it reparsed through `OntologyRegistry` and refused both enum-valued slots and the imported Malleus `timestamp` scalar. The paper task itself requires an enum-constrained `relation_type`, so bypassing that refusal by weakening the proposed ontology would have changed the experiment.

Correction: A paper-local adapter now projects an explicit closed tuple of domain record IRIs from the compiler's frontend-neutral `ValidatedContractCompilation` into `LogicalGraphContract`. It preserves qualified enum and class range identities, resolves compiled scalar ancestry to XSD terminal types, excludes unselected imported protocol classes, and refuses identity, selection, suffix, endpoint, expression, and plan/runtime-symbol drift. Its source and test digests are `sha256:2ca5374296ff94d7e09314f60c44225ed518641b1acd1ac974c9c600dfebbe3f` and `sha256:6e7af2f7471e5da63cb0d8909fc818bfcbb7246f157c88e091bef515cf01f1bc`. Sixty-one GraphRecipe and paper-bridge tests passed; Ruff and format checks were clean.

Impact: The construction grammar can now consume the same enforced compiler IR used by history replay rather than a second ontology interpretation. This is a repository-local evaluated bridge, not a shipped public API. The document ontology has not yet passed adequacy review or population.

### E-0060, first retained compiler run excluded for precommit drift

Date: 2026-09-02

Sources: `ontology-compile-precommit.json`, `ontology-compile-precommit-02.json`, both retained compilation directories, and `test_model_acquisition_result.py`.

Observation: The first official-retained compiler precommit named mapping-resolver identifiers, while the newly implemented harness emitted exact-memory-resolver identifiers. The compilation itself was deterministic and valid, but its resolver coordinates did not match the precommit. The mismatch was found before adequacy review.

Correction: The first output directory remains retained but is excluded from evidence. A second append-only precommit froze the harness's actual resolver ID, profile, configuration identity, source closure, output identities, and expected result. The corrected run reproduced byte-identical contract and receipt files: 1,632 facts, validated fact-set `sha256:8b1aca802746ab7fe487af92a286e1242ae105adda9665ba68388688838ffce2`, contract file `sha256:cec07ba6cce324e7b3a5867a46818a3249923a1fb1d49577eea78c1717cf1dee`, and receipt file `sha256:bd10af7086c7efb55478817e55e8c30956efa8c6395f3de574917855fdbf3054`.

Guardrail: A hard result test now requires the corrected precommit's resolver coordinates and output hashes to equal the retained receipt and files, and proves that the excluded first precommit does not match its run.

Impact: Only `ontology-compilation-02/` is authoritative for later review and population. This correction is an experiment-harness repair, not a second model retry.

### E-0061, ontology review input closure passed under the pinned runtime

Date: 2026-09-02

Sources: `ontology_review_inputs.py`, its focused tests, `ontology-review-input-manifest.json`, `schema-inventory.json`, and `review-eligibility.json`.

Observation: A deterministic paper-local gate recompiled the exact candidate, required corrected compiler precommit 02 and compiler run 2, selected exactly 15 domain classes, projected the compiler IR into the GraphRecipe logical contract, and verified the complete question, oracle, rubric, locator, selected-reading, public-manifest, and six-block evidence closure. It emitted an 84,002-byte schema inventory at `sha256:feeca8a149d7888b87dacbc1e69074a3fb2152168483a51c10146d84d6aa70c4` and a 2,739-byte `PASS` eligibility report at `sha256:8b123681923fb16276b48632a275d8637aca4495433b97fb74013c21ebae18e8`. The generator and test digests are `sha256:b2206de8f0f57aa0cb47a07aec4fc88dffadbfd74e354605c1b81eb374a82151` and `sha256:ce11fb2dbec01f25f63dced0a36302e3a46edc285431a66140c5ab622dd0b2d3`.

Failure and guardrail: An independent invocation first used ambient Conda Python. Its LinkML Runtime 1.10.0 `types.yaml` was 7,298 bytes at `sha256:582c6dc9299038cd907c07a1cfdf288451fcda631b1fdd885438849d968ee817`, not the pinned 1.11.1 module of 7,296 bytes at `sha256:1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00`. The compiler refused with `TRUSTED_MODULE_MISMATCH`. The retained manifest now fixes the interpreter, distribution versions, resource size, and resource digest. A hard test fails directly on any runtime or input-byte drift. The project `.venv` gate passed 15 review-input, freeze, and result tests after the review completed.

Impact: Review eligibility establishes exact input and compiler closure only. It does not score semantic adequacy and cannot select the ontology.

### E-0062, one-shot reviewer refused the primary ontology

Date: 2026-09-02

Sources: `ontology-review-precommit.json`, the raw reviewer output, `ontology-adequacy-result.json`, `ontology-adequacy-receipt.json`, and `test_ontology_adequacy_result.py`.

Observation: A distinct fresh `gpt-5.6-sol` reviewer at high reasoning effort consumed only the 14 precommitted files. Eligibility passed. `OA-01`, `OA-02`, `OA-04`, and `OA-06` passed. `OA-03` and `OA-05` failed. The review contains 32 witness rows, all paired with allowed source blocks. One row failed: `usable_instrument_count = 17`. The candidate exposes only `ObservationNetwork.instrument_count`; reusing it for both 19 deployed and 17 usable instruments would conflate distinct values or push the distinction into a generic label. The final status is `REFUSED_ADEQUACY` with `unresolved_count` 1.

Identities: The review precommit is `sha256:ec790c389b3f3f4aeb34d5c629ba8867801cd40f747a274763768f91f103d49c`. The provider output was 30,956 bytes at `sha256:0f3a787cde5b1aa2aeb36d6e322bf18af80c01d41e7fc806b861e9b30fc7a864`. The retained raw file appends one terminal LF and is 30,957 bytes at `sha256:afc6e960a599f0aa9e0f4f245cd602e0785545a0e109c6649ddd6eb101fc88b3`. The extracted result is 30,919 bytes at `sha256:b0efcf5019c16ebaef82d18e65c1021b3925a4b0000147360c2aa42eb6988f5c`. Schema, identity, criterion closure, witness counts, decision coherence, and locator membership are hard-tested.

Impact: The primary run ended before population, exactly as frozen. It supplies no selected ontology, graph, ledger, or query result. There is no reviewer feedback, retry, restart, or best-of selection. RQ1 is negative for this run. The refusal is evidence that compilation and semantic adequacy are separate gates.

### E-0063, post-primary recovery control frozen

Date: 2026-09-02

Source: `paper-v4/experiment/ontology-recovery-precommit.json` at `sha256:4a389e6c70a61f7938f86bf4495f8933b29a2b0ca14326114afdace09e3fa31b`.

Decision: Continue the systems experiment as a separately scored post-primary control. The only allowed semantic changes are to rename `instrument_count` as `deployed_instrument_count`, add required integer `usable_instrument_count`, and bump schema version 0.1.0 to 0.1.1. Class, enum, relation, other constraint, question, oracle, locator, rubric, and original-candidate changes are forbidden. The correction must compile to a new identity and pass one new independent review before population.

Impact: Any later graph or query result belongs to the recovery control. It cannot change the adverse primary result or support a claim that the fresh session independently produced an adequate ontology.

### E-0064, Core remains sufficient for the recovery-control vertical

Date: 2026-09-02

Sources: read-only audits of the pinned private history, GraphRecipe bridge, graph query API, candidate inventory, and frozen questions.

Observation: Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3` already supports the required one-change, create-only history. The remaining provenance map, source-free projection package, sorted native query functions, and document runner are paper-local. The temporal Small Shop correction is neither needed nor consumed. A provisional minimal graph after a valid recovery selection contains 15 entities and 20 relations, or 35 create operations; this is a design estimate until an exact recipe and plan are frozen and executed.

Impact: Do not wait for or cite the concurrent Core correction. The next gates are recovery selection, ontology-bound query freeze, population, admission, replay, isolated querying, and mutations.

### E-0065, frozen recovery ontology compiled

Date: 2026-09-02

Sources: `paper-v4/experiment/ontology-recovery-precommit.json`, `paper-v4/experiment/controlled-ontology-recovery.yaml`, `paper-v4/experiment/ontology-recovery-compilation/validated-contract.json`, `paper-v4/experiment/ontology-recovery-compilation/compile-receipt.json`, and `paper-v4/experiment/test_ontology_recovery.py`.

Observation: The recovery source changes exactly three values from the primary candidate: schema version 0.1.0 to 0.1.1, `instrument_count` to required integer `deployed_instrument_count`, and addition of required integer `usable_instrument_count`. The exact-memory compiler accepted it and emitted 1,648 canonical facts. The source is `sha256:29fca9e9325c9d14e5070bcb4274c8704f9d1aaa058799e5a81f27cb5a5a99e9`; resolver configuration is `sha256:3d1d1e92953efb97b03c7befcf66b65752c34cfb961ac39d317c5f0b4eae5902`; validated fact-set identity is `sha256:c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332`; validated-contract file digest is `sha256:4e5297a3844e55a17c21dbbbd94778f8426cad91a14f1f42e2c747ad8c2d72cd`; and compiler-receipt file digest is `sha256:f8843baa1802529de46df8410dcd16f14bdebc0a9db048850175654ecad2277b`.

Guard: Six recovery tests reproduce the semantic diff, source identities, compilation, fact count, contract bytes, and review-input closure. The full 80-test compiler and recovery gate passed under the project `.venv`; the focused recovery and review-result gate later passed 11 tests. Three older evidence files are intentionally left byte-frozen despite the repository-wide formatter preferring changes to them.

Impact: Compilation makes the recovery eligible for its precommitted review. It does not itself select the ontology or authorize population.

### E-0066, independent recovery review selected the control

Date: 2026-09-02

Sources: `paper-v4/experiment/ontology-recovery-review-precommit.json`, `private/paper-v4-evaluation/ontology-recovery-adequacy-review-raw.txt`, `private/paper-v4-evaluation/ontology-recovery-adequacy-result.json`, `paper-v4/experiment/ontology-recovery-adequacy-receipt.json`, and `paper-v4/experiment/test_ontology_recovery_adequacy_result.py`.

Observation: A fresh, distinct `gpt-5.6-sol` reviewer at high reasoning effort consumed only the 15 precommitted inputs. Its single output returned `SELECTED_CONTROL`. Eligibility and `OA-01` through `OA-06` all passed. The result contains 39 witness rows, all with `PASS` judgments and allowed `SUPPORTED` source blocks, with zero unresolved items. No feedback, repair, retry, or second attempt occurred.

Identities: The review precommit is `sha256:7d20563238d2de4a08e3db2a26127ce285598cc336eaf4bff70ac2811cf96a7d`. The provider output was 34,726 bytes at `sha256:d14cf727d220bd72834d12071865f4d6044aa64b11da57791f1284eec21fa6e2`. The retained raw file appends one terminal LF and is 34,727 bytes at `sha256:9449e97892eb35c4d7a116e931674e3afe5fa26a80918a7ed84eb464ee54d87b`. The extracted result is 34,671 bytes at `sha256:fbd6b609a854619b3931933932f39687f4e9fe2861076cfc1941c9631a92ce4c`. The selection receipt is `sha256:c61ca58167a2655b4d6b4a160559e158db32a5a2872f280d56b9e4c5e41d4841`.

Guard: Three tests validate the exact raw capture, JSON Schema, identity closure, six unique criteria, decision coherence, witness counts, and locator membership. They also assert that the primary receipt remains `REFUSED_ADEQUACY`, retains no selected ontology, and denies primary population.

Impact: Population is authorized only under classification `POST_PRIMARY_CONTROL` and only against recovery source `sha256:29fca9e9...`. The next step is to freeze the four native query definitions before creating population facts. The primary RQ1 result remains adverse and final.

### E-0067, native queries frozen before population

Date: 2026-09-02

Sources: `paper-v4/experiment/native-query-binding.json`, `research/ontology_driven_kg_realization/experiments/document_paper/native_query.py`, and `paper-v4/experiment/test_native_query_binding.py`.

Observation: The binding freezes four native queries against the selected recovery ontology, its compiler and review identities, Core `1611944`, and an exact closure of 15 entities and 20 relations. Query predicates use only exact record types, relation types, ontology enums, endpoints, topology, and cardinality. They do not filter any document name, year, count, numeric bound, or expected answer. The executor emits both raw semantic witnesses and rendered answers using only graph-returned values and frozen enum lexicalization.

Boundary: At query time the allowed graph methods are `query`, `query_relations`, and `get_node`. The intended runner inputs are one source-free projection and the frozen binding. PDF bytes, OCR text, source ledger, locator map, model transcript, answer oracle, embedding model, vector index, and network are forbidden. Oracle comparison belongs to a separate evaluator process.

Identities: The query binding is 8,424 bytes at `sha256:4eebc55bc86fa842d10bacc0e81e3a6e003569efb270e902533825fcac1c22d1`. The executor is 21,462 bytes at `sha256:336554a43ab87c53322e8422e4d1d410f28eb93696f391eba74111a0f26ecbf8`. The test is `sha256:dc5b93a215bfbc3a9d9041b2031bda2ae187bb035fcc0f361c9cc528017cb09e`.

Guard: Twelve query tests use a fictional sentinel graph. They verify exact input identities, graph closure, question order, public-API use, absence of source access, propagation of changed graph scalars and enums into output, and refusal of cardinality, context, and causal-topology mutations. Together with recovery selection and compilation guards, the focused gate passed 21 tests in 0.83 seconds; Ruff and formatting checks passed.

Impact: Query authorship can no longer adapt to the population. Population may now begin against the one selected control digest. No document graph or query result exists at this entry.

### E-0068, paper experiment isolated on the declared Core baseline

Date: 2026-09-02

Sources: worktree `/Users/luis/Projects/malleus-dev/.claude/worktrees/paper-v4-lean`, branch `codex/paper-v4-lean`, `.gitignore`, and initial paper boundary commit `6d685c5230d1b09cd2a140f94eb571aa37cf82a4` with tree `186bedcb829556997f18992a3573e0aabe8ffc27`.

Observation: The paper directory and document-paper harness were moved out of the shared main checkout into a worktree created from exact Core commit `1611944eb8856dbd4f25c2ea8bddbecdb970a3a3`, tree `657ba6ce1be83064d104803ad5dad644d65b4352`. The PDF is ignored by `/paper-v4/source/*.pdf`; Python caches are ignored by the repository-wide `__pycache__/` rule. The initial isolated boundary was clean, excluded the PDF and all private files, and passed 29 focused active harness tests.

Impact: D5 is complete. Later Core work and the shared main checkout cannot change the implementation under this experiment without an explicit baseline decision.

### E-0069, PDF text-layer reading selected

Date: 2026-09-02

Sources: `pyproject.toml`, `text_layer_reading.py`, its focused test, the source manifest, and private `paper-v4-text-layer/selected-reading.json`.

Observation: The active reader is `pypdf==6.16.2`, invoked as `PdfReader(strict=True)` followed by `PageObject.extract_text()`. The source digest and 11-page count are checked before extraction. Text correction is `NONE`; only CRLF and CR are normalized to LF. Wrapped lines are grouped until a sentence, blank, or page boundary, producing 186 stable blocks. Two builds were byte-identical. The selected reading digest is `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.

Raw quality check: The selected `pypdf` reading contains 31 literal `CO2` forms, 38 `CO` plus whitespace plus `2` forms, and zero `CO,` forms. A diagnostic run of host `pdftotext` produced 74 literal `CO2` forms, but that tool is not the selected dependency or retained reading. The paper must report the selected reader's result, not transfer the diagnostic count to it.

Errors and guards: The first import failed because `pypdf` was absent. The exact dependency is now in the project research extra and runtime version drift refuses under a focused test. Direct `pytest` initially could not import the repository namespace; the project test path now includes the repository root, and both direct and module invocations pass. The inherited blank-line projection collapsed each extracted page into one locator during a dry run. The final sentence-boundary projector has a test that prevents wrapped support from splitting into per-line blocks or collapsing into one page block.

Impact: D1 reading selection is complete. The earlier raster, Tesseract, and Malleus OCR artifacts do not support an active paper claim.

### E-0070, sealed oracle locators rebound without changing answers

Date: 2026-09-02

Sources: the original sealed evaluator oracle, the selected text-layer reading, and private `paper-v4-evaluation/answer-oracle.json` in the isolated worktree.

Observation: The four parsed answer objects are equal to the original sealed answer objects. The new evaluator-only oracle contains 22 value-to-block locators. Every locator resolves to one of the 186 selected-reading blocks, and the oracle's embedded selected-reading digest recomputes correctly.

Impact: D1 locator rebinding is complete. The population model cannot see the answer key. Later scoring may use these answers and locators, but the oracle is not a sixth public experiment identity.

### E-0071, pre-steer mechanisms retired from the active experiment

Date: 2026-09-02

Sources: `paper-v4/retired/pre-steer-experiment/`, `paper-v4/retired/tesseract-harness/`, and `paper-v4/retired/adequacy-review-harness/`.

Observation: The raster OCR run, hand-authored recovery ontology, adequacy tasks and receipts, fixed 15-entity and 20-relation query binding, and answer-encoding recipe are retained under `paper-v4/retired/`. Their executable tests and harness modules are outside active test discovery. Existing private OCR files were left untouched. The active experiment directory retains only the four frozen competency questions until new D2 and D3 artifacts are produced.

Impact: D2, D3, and D6 have no fallback to the old ontology, evaluator population, reviewer, or fixed graph closure. Historical ledger entries remain factual records of superseded work and are not current paper claims.

### E-0072, later Core correction publication is coordination only

Date: 2026-09-02

Source: coordination from the Malleus Core task after its publication gate.

Observation: Core published annotated research tag `research/small-shop-correction-replay-v1` at commit `e94f45c74475948dfebdc89247bfb070de0b778d`, tree `60f393403728aa25a256909618a94aba344d690b`, after local and remote gates. This coordinate arrived after D5 fixed the document experiment on Core `1611944`.

Impact: The tag is not adopted as a paper experiment identity and does not replace the document baseline. It may be reconsidered only through a later author decision.

### E-0073, fresh ontology compiles on its first attempt

Date: 2026-09-02

Sources: input freeze commit `3be6feb`, `paper-v4/experiment/ontology-run/task.md`, its five copied model-visible inputs, `ontology.yaml`, `acceptance.jsonl`, and the paper-local exact ontology compiler.

Observation: A contextless `gpt-5.6-sol` session at high reasoning returned one ontology proposal from only the declared task and inputs. The proposal compiled on its first attempt into 1,401 validated facts. The compiler returned no diagnostic to the session. The selected ontology digest is `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`. One canonical event by `actor:paper-v4-evaluator` records `ACCEPT_FOR_POPULATION` against that exact digest.

Boundary: The event authorizes the population stage. It does not assert semantic adequacy. No reviewer, answer key, hand repair, alternate ontology, or best-of selection contributed to the proposal or acceptance.

Error and guard: An initial post-run validation command accessed a nonexistent `ExactSource.sha256` attribute after compilation and raised `AttributeError`; it did not change either retained artifact. A focused test now recomputes the ontology digest from bytes, requires exactly one canonical acceptance record with the fixed actor and decision, recompiles against the copied Malleus input, and binds the accepted receipt to the recorded digest. The ontology compiler file passes eight focused tests.

Impact: D2 with D6 is complete. Query authors may now bind the four questions to ontology types before any population session sees the task.

### E-0074, type-only query binding frozen before population

Date: 2026-09-02

Sources: `paper-v4/experiment/native-query-binding.json`, the replaced `native_query.py`, the selected ontology, and `paper-v4/experiment/test_native_query_binding.py`.

Observation: The four questions reduce to typed source-relation-target cases. The binding names only query and question ids, source, relation, and target record types, relation enum types and values, case order, and projected ontology fields. It contains no record identifier, document answer, numeric answer, source phrase, locator, entity or relation count, singleton requirement, causal topology, or graph closure. The executor returns every matching row in stable order and reads only relations plus their endpoint nodes. The binding digest is `sha256:115009ff737600d63eb9761bfc11f69ee62cd11f41d60682772556f5fa56c6d9`.

Guard: Three focused tests validate the binding against the selected ontology, reject extra selectors and invalid types, enum values, endpoint directions, or output fields, propagate fictional graph values through multiple matching rows, and block file and network access during query execution. This directly prevents the retired fixed-closure and hidden-answer error class.

Learning: `OntologyRegistry` resolves relative import-map entries against the ontology file directory, not the process working directory. An initial validation probe passed a workspace-relative retained-input path and refused after duplicating the directory prefix. The active guard uses the exact absolute retained-input path.

Impact: Query authorship is frozen before D3. Population size, identities, values, and topology remain open to the fresh model session.

### E-0075, generic recipe library reaches one arbitrary valid plan

Date: 2026-09-02

Sources: `paper-v4/experiment/generic-recipes.stottr`, the selected compiled ontology, the compiled-IR GraphRecipe adapter, and focused tests.

Observation: The retained library defines the five terminal declarations and eight generic templates: named entity, observing system, bounded quantity, mechanism hypothesis, and four relation shapes. Constants are limited to ontology record types, property IRIs, operation kinds, and the five ontology-fixed enum values. Record ids, names, counts, bounds, units, relative positions, and mechanism text remain invocation variables. Thirteen arbitrary fictional invocations exercised every template, assembled into one aligned plan, and materialized atomically.

Infrastructure refusal and guard: The first full selected-ontology projection refused `QuantityCharacterizationRelation.target_id`, then would have refused `SpatialAssociationRelation.source_id`, because both legally range over the imported abstract `Entity` root rather than one selected concrete type. The paper-local adapter now permits that root only for positional relation endpoints. It remains nonconstructible, and an unselected class range on an ordinary property still refuses. Two focused tests preserve both sides of the rule.

Recipe-profile refusal and guard: The first arbitrary invocation run showed that the restricted stOTTR profile can lower float terms but does not accept `xsd:float` as a parameter declaration. The two numeric recipe parameters are now mandatory untyped terms; the selected ontology still enforces float values during plan staging. The every-template test preserves this path.

Provenance boundary: Neither `AssemblyPlan` nor the private `KnowledgeChangeSet` stores locators inline. D3 must produce a canonical provenance map from population record and property assertions to reading blocks and recipe emissions. The change set will bind that map through its evidence closure. The manuscript and plan no longer claim inline operation locators.

Impact: The construction vocabulary is frozen without document facts. D3 may now ask a fresh model session to supply the population and locators.

### E-0076, fresh population succeeds on its first attempt

Date: 2026-09-02

Sources: `paper-v4/experiment/population-run/population.json`, `paper-v4/experiment/results/population-plan.json`, `paper-v4/experiment/results/population-provenance.json`, and the active population compiler and tests.

Observation: A fresh population session returned one proposal, and the proposal compiled unchanged. No structural diagnostic or retry was needed, and the session did not refuse. The population contains 14 records: eight entities and six relations. Its provenance map contains 51 located assertions over seven selected-reading blocks. Every population-supplied record, property value, and relation endpoint has a selected-reading block locator. Ontology-fixed recipe constants and dependency emissions are not source-located population claims.

Boundary: This is structural and provenance success, not an evaluator adequacy judgment. No human-authored population, fallback, content review, or alternate candidate entered the run.

Impact: D3 is complete. The first and only population proposal proceeds to the declared checks and commitment boundary.

### E-0077, orchestrator derives both pre-admission checks

Date: 2026-09-02

Sources: `research/ontology_driven_kg_realization/experiments/document_paper/experiment_run.py` and `test_experiment_run.py`.

Observation: The paper-local orchestrator recompiles the exact selected ontology and population, then performs two verifications before it can construct check events. `source-locator-integrity` joins every population assertion to the selected reading, provenance record, plan member, emission id, expansion path, emitted fact, operation value, and relation endpoint. `structural-conformance` checks the plan against the compiled contract and ontology. Each verification produces a retained check contract and a result receipt that binds its exact inputs. Only a completed verification can produce `SATISFIED`; callers cannot supply that outcome. The policy requires both receipts and computes `ACCEPT` only when both are satisfied.

Guard: Focused mutations cover source identity, locator membership, provenance semantics and lineage, plan identity, JSON value type, plan-to-contract alignment, stale prior state, unsupported operations, and failed grouped application. No failed pre-admission case retains a check result in history or creates the ledger; provenance and source failures construct no check result. Admission failures cannot leave a partial append.

Impact: The two accepted check outcomes are mechanically derived experiment evidence, not fixture-supplied verdicts. This remains a paper-local orchestrator, not a public check framework or stable API.

### E-0078, one accepted change replays to the same graph

Date: 2026-09-02

Sources: private `paper-v4-run/semantic-ledger.jsonl`, `paper-v4/experiment/results/experiment-result.json`, and `paper-v4/experiment/results/replay-receipt.json`.

Observation: The runner first wrote 19 bootstrap anchors: 18 `ARTIFACT_REGISTERED` events and one `SOURCE_REGISTERED` event. Atomic admission then appended a five-event suffix comprising `KNOWLEDGE_CHANGE_SET_RETAINED`, `CHANGE_PROPOSED`, two `CHECK_RECORDED` events, and `VERDICT_RECORDED`. Both checks were `SATISFIED`, and the declared policy derived `ACCEPT`. The resulting 24-event source-bearing history projects eight entities and six relations. Its ledger head is `sha256:a069c3ded48b3da1c6f022bab8601b16173ac90c64c812a4c74435b3085e43b6`. The canonical replay receipt is `sha256:6fccc6048d3444b9cbe4ea2bdca3101a7642a4e036a852d26e8fa21fbe03fb29`; its graph-state digest is `sha256:e6ea3a3b5db5a7361dc87d955d89591097b7b8052d7a93fdce7b77c3db22f12a`.

Replay: The runner discarded the first derived in-memory graph object, disposed of the history object, reopened the private ledger from disk, and replayed it. Reopen reproduced the same ledger head, canonical receipt, graph digest, eight entities, and six relations. No external graph database was created or deleted.

Impact: The fourth manuscript identity group is resolved by the ledger head and replay receipt above. The graph-state digest remains a receipt field and raw evidence coordinate; it is not a sixth manuscript identity group.

### E-0079, query rehydration fails once and gains a contract-identity guard

Date: 2026-09-02

Sources: the first source-free query attempt, `query_replay.py`, and `test_query_replay.py`.

Failure: The first query attempt refused because the graph digest after typed rehydration differed from the replay receipt. Entity and relation records were unchanged. The mismatch came from the ontology coordinate inside the canonical graph snapshot: `KnowledgeGraph.from_records` used the selected ontology registry identity, while private replay had bound the graph state to the compiled validated-fact-set identity.

Root cause: The source-free replay receipt carried the validated-fact-set coordinate, but the first query rehydrator neither required nor restored it before recomputing graph identity. Comparing the two canonical digests therefore mixed two legitimate but different ontology coordinates.

Fix and guard: Query rehydration now requires a lowercase `validated_fact_set_sha256` in the receipt, reconstructs a typed graph from the source-free snapshot, restores that contract coordinate in the canonical snapshot used for identity, and then compares the result with the receipt's graph-state digest. Hard tests refuse a missing or malformed contract coordinate and any real graph-state mutation. A focused test reproduces the contract-view identity case.

Impact: The retained query result was generated only after this repair. The fix reconstructs replay's identity semantics; it does not waive graph equality or substitute an answer.

### E-0080, four queries run over source-free replay state

Date: 2026-09-02

Source: `paper-v4/experiment/results/query-result.json` at `sha256:0782f2892d242ec7c48bd243b4bfce67df89f990f7c1e30af75af2f0d8fa6909`.

Observation: The four frozen type-based queries returned row counts `[1, 1, 2, 1]` in question order. The result binds the selected ontology, query binding, replay receipt, and graph-state digest. The query invocation received the source-free replay receipt with its graph snapshot, the selected ontology, the retained Malleus import needed for ontology validation, and the frozen query binding. It did not receive the PDF, selected reading, source-bearing ledger, model transcripts, or answer oracle.

Isolation observation: Python-level guards were active around query execution. Recorded counters are `file_read: 0`, `network: 0`, and `embedding_import: 0`. These counters support the bounded observation that this run queried replayed typed state without consulting document text or an embedding index. They do not establish an operating-system sandbox or a general replacement for retrieval-augmented generation.

Impact: Query execution is complete. The query-result digest is retained internal evidence, not a sixth manuscript identity group.

### E-0081, stale oracle coordinate refuses before scoring

Date: 2026-09-02

Sources: E-0070, the retired evaluator-only v1 oracle, the corrected evaluator-only D1 v2 oracle, `query_score.py`, and `test_query_score.py`.

Failure: The first scoring attempt refused at the oracle identity guard because the scorer still named `sha256:95b206a8a8eac20f208854c2374ed8433187402d9ab1e50771003e412066b571`. That coordinate belongs to the unrebound v1 oracle. It does not contain the selected-reading coordinate or D1 value-to-block locators.

Evidence-backed correction: E-0070 recorded the locator-rebinding requirement before population, query execution, and result inspection. The corrected D1 v2 oracle binds selected reading `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17` and contains 22 value locators; all 22 resolve to its 186-block reading. The v1 and v2 ordered semantic projections are byte-identical. The projection is canonical JSON of `[{'question_id': entry['question_id'], 'answer': entry['answer']} for entry in oracle['answers']]`; it is 889 bytes at `sha256:f02daa92b21574acd54d3196a983243ce5a7c920e5b4101f798c1b02e2a857ec`. The complete corrected private oracle is `sha256:6f1564887aa908ac2cd0ff9f06e823ccf936ca18d24595252a0c04a6c0cc09b4`.

Guard: The scorer now requires the exact D1 v2 coordinate and has a hard test that excludes the retired v1 coordinate. The correction changes locator and reading metadata, not the four frozen answer objects. It occurred after the query result was committed, but its content is mechanically constrained by the pre-result E-0070 record and byte equality above.

Impact: The refusal prevented scoring against the wrong private artifact. The oracle remains evaluator-only and is not promoted into the five manuscript identity groups.

### E-0082, strict scoring is typed unscorable, not zero

Date: 2026-09-02

Source: `paper-v4/experiment/results/score.json` at `sha256:40ab6ce26591233b810d96c34b2624a3a50c6aa5b8d4f38429fd7a9a62cd8eb0`.

Observation: The scorer accepted the exact frozen query result `sha256:0782f2892d242ec7c48bd243b4bfce67df89f990f7c1e30af75af2f0d8fa6909`, query binding `sha256:115009ff737600d63eb9761bfc11f69ee62cd11f41d60682772556f5fa56c6d9`, and D1 v2 oracle `sha256:6f1564887aa908ac2cd0ff9f06e823ccf936ca18d24595252a0c04a6c0cc09b4`. The oracle uses the legacy four answer-object shape, while D6 query output uses cases and typed source, relation, and target rows derived from the frozen binding. No total adapter between these shapes was fixed before the result.

Result: `status` is `UNSCORABLE_ORACLE_SCHEMA_MISMATCH`, `score` is null, and the per-question result array is empty. This is not 0/4. No post hoc normalization, prose parser, partial-field score, or answer-value recipe was added.

Impact: Scoring is complete as a negative evaluation result. The manuscript may report the exact query rows and the schema failure, but it cannot claim exact answer match or ontology adequacy from the oracle.

### E-0083, focused active harness passes after typed scoring

Date: 2026-09-02

Source: retained project-venv test run at branch commit `b4e0d24` after document admission, query-result freeze, oracle-coordinate correction, and typed scoring.

Observation: The focused active paper harness passed 107 tests. The run covered reading and ontology guards, generic recipes, model-authored population compilation and provenance, orchestrated checks, atomic admission, reopen and replay, source-free graph rehydration, query binding and execution, strict input identities, the D1 v2 oracle coordinate, and the typed unscorable result.

Boundary: This is the focused active engineering result, not the final clean publication gate. Manuscript reconciliation, a final reproduction run, and the arXiv bundle remain open.

Impact: The executed document vertical is mechanically covered through query output. The final paper gate must include the corrected oracle-coordinate and typed-score tests as well as manuscript and bundle checks.

### E-0084, retained-environment reproduction and focused paper gate pass

Date: 2026-09-02

Sources: a new ignored run under `private/paper-v4-reproduction-01/`; the six committed files under `paper-v4/experiment/results/`; the retained private `paper-v4-run/semantic-ledger.jsonl`; the active paper test suite; and the current manuscript, plan, and ledger diff.

Observation: The public reading command regenerated 186 blocks across 11 pages at selected-reading identity `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`. A new frozen run, replay query, and strict score then regenerated all six committed result files byte for byte. The regenerated private semantic ledger also matched the retained ledger byte for byte at file digest `sha256:5779039b218a00cdc278c317f34cd7ec4b1e07997999ed8126411a7d99d253c9`.

Gate: The focused active paper harness passed 107 tests in 4.18 seconds with bytecode and pytest cache writes disabled. Ruff passed the active paper experiment and document-run modules. `git diff --check`, the five-identity scan, ignored-PDF and ignored-private checks, result-digest checks, and a primary-source citation audit also passed. The reconciled manuscript is 3,602 words.

Boundary: The byte comparison used the retained Python 3.12.9 project environment, not a newly installed environment. Exact observed top-level versions are recorded in Appendix A, but `pyproject.toml` does not freeze every transitive dependency. This is the final focused paper-local gate for this boundary, not the arXiv bundle gate or a package release.

Impact: The executed vertical and lean manuscript are ready for an isolated paper commit. A complete paper-specific transitive lock plus arXiv source and render inspection remain open.

### E-0085, question-independent ontology compiles after one structural correction

Date: 2026-09-03

Sources: D-0018; input-freeze commit `f5d8a83`; `paper-v4/experiment-v2/ontology-run/task.md`; its input manifest and four copied Malleus files; private selected reading `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`; both returned ontology attempts; the first compiler refusal; and the accepted compilation receipt.

Observation: A new context-free Codex subagent with no inherited turns received only the declared question-independent ontology task and five inputs. It did not receive the competency questions, an answer key, earlier ontology, Recon output, paper documents, source code, tests, or network access. Attempt one proposed a broad mid-ocean-ridge geodynamics vocabulary and was refused because the supported LinkML profile rejects root field `default_prefix`. The exact canonical diagnostic was returned to the same session. Attempt two removed only that line. Its ontology bytes are `sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed` and compile into 4,146 validated facts at validated-fact-set identity `sha256:bc178b7c9125d5edefd43df45f1a2949e815b17da27668308b0ae728f3f6f4ad`. The accepted contract bytes are `sha256:292f8777ea24ad06de82c70bd87f1c049eb457fd34b742e2d5db12dd0e6233ae`; the compile receipt is `sha256:d4595bf34eeed2aaa743e18703eadee7324c89bc2f257c88379405279ea62c69`.

Boundary: The compiler establishes structural validity only. The proposal is broader than the old question-shaped ontology, and no human edited its domain semantics. It is not evidence for minimality, adequacy, or a general Malleus ontology builder. One canonical acceptance event authorizes the next stage against this digest without judging meaning.

Impact: Bind the frozen questions to this ontology through a paper-owned query surface, prepare ontology-specific value-generic recipes, and freeze both before a fresh population session. Missing question semantics must remain visible as query or review results; they do not authorize ontology repair.

### E-0086, query ownership and source-grounded review method frozen

Date: 2026-09-03

Sources: D-0018; the automated-score RCA; `experiment_run.py`; `frozen_experiment.py`; `human_review.py`; `paper-v4/evaluation-v2/`; and 57 focused harness tests.

Observation: The failed v1 scorer exposed two separate contract errors. The paper had no typed composition from replay-derived query rows to its legacy answer objects, and its evaluation inputs contradicted the intended independent inspection boundary. The author rejected both a Core-owned evaluation contract and a paper-local exact-match adapter. The corrected build runner therefore accepts no query bytes, retains no query artifact in its change-set evidence, and emits no query coordinate in its knowledge-build result. Every build coordinate and path is now explicit. A hard test fixes the complete admitted evidence-key closure, so a renamed query or adapter artifact cannot silently enter accepted history.

Review freeze: Before any corrected query result existed, the paper froze source-grounded review protocol `sha256:04cf6bc131d018acc541d0ee9812b18c1a3d40b58b4bc003536598e2d4621d43`. It fixes only the source, selected reading, question set, judgment labels, evidence surface, and authorship order. Corrected ontology, ledger, receipt, query-binding, and query-result coordinates remain pending until those stages exist. The validator checks identities, row coverage, block membership, labels, and authorship state. It never selects a judgment. Codex may record a preliminary inspection, but only Luis can create paper evidence by ratifying or editing it.

Open reproduction defect: Removing the implicit v1 runner also removed its command-line entry point. The current manuscript still names that old module command, which now exits without performing a run. A new explicit v2 driver and a regression test for observable outputs are required before any reproduction or publication claim.

Impact: Automated scoring and answer-oracle consumption leave the selected path. Querying is an adopter-owned read over replayed state. Evaluation is a separately frozen, source-grounded record with honest human authorship.

### E-0087, v2 construction profile, recipes, and query binding frozen

Date: 2026-09-03

Sources: D-0018; `population_compile.py`; `experiment_run.py`; `paper-v4/experiment-v2/generic-recipes.stottr`; `paper-v4/experiment-v2/native-query-binding.json`; their focused tests; and the accepted v2 ontology.

Observation: The v1 population compiler embedded its schemas, namespaces, and record-to-template mapping. Reusing it for the question-independent ontology would therefore have made a v2 run depend on hidden v1 choices. Population compilation now requires one immutable `PopulationRecipeProfile`. It names the population, reading, and provenance schemas, graph-recipe profile, recipe and member namespaces, and the complete concrete record-to-template mapping. There is no production fallback. The complete experiment requires the profile explicitly and verifies the configured provenance schema rather than a v1 constant.

Audit corrections: A real non-v1 end-to-end test exposed one hidden v1 provenance check, which is removed. Two proposed profile fields were also removed. XML Schema term typing remains one coherent compiler choice, and the invocation namespace is private because changing it cannot affect a retained successful-run identity. Focused tests now exercise each effective adopter choice independently and refuse unknown, abstract, nonconstructible, duplicate, or untemplated mappings.

Natural construction refusal: The first logical-contract selection omitted the two abstract endpoint-range classes `GeoscienceObject` and `DomainObservation`. Contract derivation refused because a class-valued slot range was outside the selected record set. The corrected selection retains both as abstract, nonconstructible contract types. A hard test proves they cannot be mapped to population recipes.

Frozen artifacts: The nineteen generic templates are 9 entity constructors and 10 relation constructors at `sha256:7324dbe955a7f0395d878c4e6198704a4fa11c296b79a66c8a30729ab4fbb968`. They contain ontology-fixed types and relation enums but no document value, population record id, source locator, answer, or graph size. An arbitrary 21-operation fixture expands, stages, and materializes against the compiled ontology. The paper-owned query binding is `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`. It contains 1, 2, 4, and 6 direct typed cases for the four frozen questions and fixes no document value, record id, locator, count, cardinality, or closure.

Expressibility boundary before population: CQ1 can bind a method to instruments but the ontology has no campaign, observing-system or network record, acquisition relation, or instrument-count quantity. CQ2 can bind seismic occurrence to a feature and feature membership to a larger feature, but has no relative-position predicate for "beneath" the ridge axis. CQ3 is representable through quantitative observations and their target relations. CQ4 can bind process components and observations, but has no hypothesis wrapper, epistemic or author-preference property, or typed direction of motion. These are empirical limits of the unconditioned proposal. They are not repaired before population.

Verification: 66 combined population, runner, frozen-path, recipe, and query-binding tests pass. Ruff and `git diff --check` pass.

Core boundary: The existing replay receipt and `KnowledgeGraph` read methods support all frozen cases. No missing Core seam or Core capability request exists at this boundary.

Impact: Query binding and generic construction are frozen before any v2 population exists. The next fresh session may see the questions, ontology, selected reading, recipes, and population grammar, but it may not see this binding, an answer key, prior population, manuscript, ledger, or earlier model transcript.

### E-0088, v2 population acquisition inputs frozen

Date: 2026-09-03

Sources: D-0018; `paper-v4/experiment-v2/population-run/task.md`; its input manifest and three public input copies; private selected reading `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`; `population_acquisition.py`; and focused tests.

Observation: The model-visible task is 6,036 bytes at `sha256:00cca7d26cd37260fd3bf056f55e96f6562cad25f9d1c951d2fac43f916825c2`. Its declared read set contains only the task, selected ontology, generic recipe library, four frozen questions, and selected reading. The ontology, recipe, and question copies match their frozen sources byte for byte. The task forbids network access, delegation, other repository files, prior paper artifacts, query binding, and answer material. It permits one output file and no other write.

Population boundary: The producer must use opaque ordered ids with no answer-bearing text. Names may denote records but may not carry a count, location, direction, relationship, causal clause, epistemic qualifier, or any fact lacking a typed property or relation. The task explicitly forbids substituting an observation method for a campaign, one instrument for a network, invented individuals for an aggregate count, or unqualified causal edges for a proposed mechanism. A sparse graph is allowed. A model refusal is a terminal negative result, not input to ontology compilation or a reason to retry.

Mechanical guard: A new structural classifier distinguishes a valid proposal envelope from a terminal model refusal before compilation. It refuses malformed JSON, unknown schemas, malformed refusal objects, and any record id outside the exact ordered `urn:malleus:paper-v4:v2:record:NNN` sequence. The later ontology compiler remains responsible for values, fields, locators, types, and endpoints. Domain meaning is not reviewed or repaired at this stage.

Coordinate correction: A read-only driver audit found that the first recipe conformance test recompiled the accepted ontology under a different root locator. Its validated facts were unchanged, but its contract and compile-receipt bytes differed. The test now uses the accepted locator `paper-v4:mid-ocean-ridge-geodynamics` and byte-compares both recompilation outputs to the frozen accepted contract `sha256:292f8777ea24ad06de82c70bd87f1c049eb457fd34b742e2d5db12dd0e6233ae` and receipt `sha256:d4595bf34eeed2aaa743e18703eadee7324c89bc2f257c88379405279ea62c69`.

Verification: 17 acquisition-freeze, classifier, recipe, and exact-coordinate tests pass. Ruff and `git diff --check` pass. No v2 population output exists at this entry.

Impact: The input boundary is frozen before the new context-free producer runs. Any structural defect may be returned once to the same session. A semantic omission or poor result is retained unchanged and receives no fallback.

### E-0089, transaction time becomes an explicit experiment coordinate

Date: 2026-09-03

Sources: the read-only v2 driver map; `experiment_run.py`; and its configuration and complete-history tests.

Observation: The paper runner hard-coded transaction time `2026-09-02T00:00:00Z`. Reusing it for the corrected run would place every v2 anchor and admitted event before the experiment occurred. Selecting wall-clock time at execution would instead make byte-identical reproduction impossible.

Correction: `PaperExperimentConfiguration` now requires one explicit timezone-aware ISO 8601 transaction time, validates it at construction, and passes it to the complete history run. There is no default. A hard test substitutes a different valid value and proves that every ledger event uses exactly that coordinate. Invalid text refuses before compilation.

Boundary: The v2 transaction value itself is not chosen at this entry. It will be frozen with the explicit v2 driver after the model population exists and before admission. Existing unversioned internal proposal and evidence ids remain safe only because each experiment uses a new isolated ledger. They are not claimed as a public namespace.

Verification: 29 runner and frozen-publication tests pass. Ruff and `git diff --check` pass.

Impact: The corrected history will not carry a fabricated old timestamp or a nondeterministic runtime timestamp.

### E-0090, first v2 population proposal compiles unchanged

Date: 2026-09-03

Sources: input-freeze commit `c6b7986`; context-free producer task `population_v2_producer`; `paper-v4/experiment-v2/population-run/population.json`; its acquisition record; the exact v2 ontology, recipes, reading, profile, and compiler; and the explicit v2 driver tests.

Observation: A new subagent with `fork_turns` set to `none` received only the five declared model-visible files and owned only `population.json`. It returned the success schema at `sha256:d4c6fe42c7f96a86c3116c57bccd9c81e53c2ce6e62b421da714a1915ee79964`. The frozen envelope accepted its 13 opaque sequential record ids. Exact compilation against the accepted ontology coordinate and private selected reading succeeded on the first attempt, producing 13 ordered operations at plan identity `sha256:fa1194aa705c36ff6ef06bc3d7bcadbeb4297d44c95a3558e5946fb97dbc09e6` and 47 provenance assertions. No structural diagnostic was returned.

Boundary: No one reviewed or changed the proposal's domain meaning before this result. There was no population retry, human repair, evaluator-authored fact, fallback, query result, or answer comparison. The proposal contains seven entity records and six relation records. Their relevance and source support remain for the separately frozen post-query inspection.

Driver freeze: The explicit v2 driver binds this exact population, the accepted ontology locator and bytes, copied LinkML types, copied protocol machine, accepted ontology event, recipes, source and reading identities, and the complete population profile. It verifies the frozen compilation coordinate before build. The query binding is digest-checked before build but is passed only to source-free replay querying, never to population compilation, change-set evidence, ledger admission, or replay identity. The command requires repository, reading, private-run, result, and transaction-time arguments. Missing arguments exit with status 2 instead of the prior silent no-op.

Verification: 26 acquisition, coordinate, driver, recipe, ordering, query-failure, and CLI tests pass. Ruff and `git diff --check` pass. A query refusal test proves that a valid build bundle remains intact while no query-result file is created.

Impact: The producer's first result is frozen without semantic selection. The next step is one exact build, disposal, reopen, replay, and query invocation. The ledger and result directories do not exist at this entry.

### E-0091, v2 admission, replay, and adopter queries complete

Date: 2026-09-03

Sources: driver-freeze commit `eb63c93`; the private `paper-v4-v2-run/semantic-ledger.jsonl`; the five files under `paper-v4/experiment-v2/results/`; an independent private reproduction; and 52 focused build, replay, query, CLI, and result-freeze tests.

Execution: The exact driver ran with explicit transaction time `2026-09-03T09:11:42Z`. Population compilation produced 13 operations and 47 source-located assertions over four selected-reading blocks. Source-locator integrity and structural conformance were both derived as `SATISFIED`; the policy computed `ACCEPT`. Seventeen artifact anchors, one source anchor, one retained change set, and four protocol events produce one 23-event history. Its private file digest is `sha256:df5327be6abfabfb49342a0663185d81b8a8056211108ca759ea7cac2901e828`; its head is `sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b`.

Replay: The admitted live objects were discarded. Reopen and ledger-only replay reproduced the graph snapshot, machine state, and canonical receipt. The receipt is `sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796` and binds the same ledger head, 4,146-fact contract, and graph-state digest `sha256:d692b8e96e291801832fcaebf4aa56dcf845851e79b94894c0f479384d69ebd3`. The replayed graph contains seven entities and six relations.

Query: The paper-owned adapter received only the replay receipt, selected ontology and retained Malleus import, plus binding `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`. It returned row counts `[0, 2, 4, 0]` for CQ1 through CQ4. The two CQ2 rows cover seismic occurrence at a feature and feature membership; the four CQ3 rows cover two quantitative characterizations, constituent concern, and material location. CQ1 and CQ4 return no rows. This matches the pre-population expressibility boundary without repairing the ontology or population. The result is `sha256:78cc2c8dc42dc10a4f46d41c95e7c751134460bc1147619e067a8f5822b0be7a`.

Isolation observation: During the in-process query region, guarded file reads, socket or name-resolution calls, and imports of the named embedding or vector packages were each zero. This is a narrow execution observation, not an operating-system sandbox or a general comparison with embedding retrieval.

Reproduction: A second invocation into new ignored directories, using the same explicit transaction time, reproduced the semantic ledger and all five result files byte for byte. The public result digests are build result `sha256:bd0361d7fb01554db87723f725ce01eeeb42739bf556c5f8717c52245408c9bc`, plan `sha256:fa1194aa705c36ff6ef06bc3d7bcadbeb4297d44c95a3558e5946fb97dbc09e6`, provenance `sha256:2d4ce493d7d757e648cc782ff835e555554bfae73c9876a85170e74948ce5b03`, query result as above, and replay receipt as above.

Boundary: No score, oracle, source reading, source locator, population file, or manuscript was passed into the guarded query region. The Python guard cannot rule out lower-level or preexisting access outside that region. Query binding remains absent from build evidence and all accepted-state identities.

Impact: Admission, disposal, reopen, replay, and source-free adopter queries are complete. The exact rows are now frozen for independent source-grounded inspection. They have not yet been rated or ratified by a human.

### E-0092, exact review inputs frozen after query output

Date: 2026-09-03

Sources: pre-output review protocol `sha256:04cf6bc131d018acc541d0ee9812b18c1a3d40b58b4bc003536598e2d4621d43`; `paper-v4/evaluation-v2/review-input-manifest.json`; the selected ontology; replay receipt; query binding; query result; and 21 review-protocol and input-freeze tests.

Observation: The post-query manifest is `sha256:181e1447a9b7d56e816816d1105f5084114e287e90d5547423fefd1d74568e28`. It fills the five stage coordinates that the protocol deliberately left pending: ontology `sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed`, ledger head `sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b`, replay receipt `sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796`, query binding `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`, and query result `sha256:78cc2c8dc42dc10a4f46d41c95e7c751134460bc1147619e067a8f5822b0be7a`.

Boundary: The review method, judgment labels, question set, source identity, and reading identity remain byte-unchanged from their pre-query freeze. The inspector may see only the review task and protocol, this manifest, blank record, selected reading, competency questions, query binding, and query result. The selected ontology and replay receipt are validator inputs, not evidence for the inspector. Oracle, canonical answers, scores, model transcripts, population, provenance, manuscript results, and result-bearing ledger entries remain withheld.

Verification: The manifest resolves every stage digest to the exact retained artifact, its ledger head to the replay receipt, and the query's three input coordinates to the manifest. The selected result set contains no score file.

Impact: Preliminary inspection may begin without changing the method after seeing the rows. It remains Codex-authored work and cannot become paper evidence until Luis reviews and ratifies or edits it.

### E-0093, blind Codex preliminary inspection complete

Date: 2026-09-03

Sources: `paper-v4/evaluation-v2/review-task.md`; review protocol `sha256:04cf6bc131d018acc541d0ee9812b18c1a3d40b58b4bc003536598e2d4621d43`; review input manifest `sha256:181e1447a9b7d56e816816d1105f5084114e287e90d5547423fefd1d74568e28`; private selected reading; frozen competency questions, query binding, and query result; and `paper-v4/evaluation-v2/review-record.preliminary.md` at `sha256:4ccab912c693d0f751276d45ad58d9536c4ce75552d337b39b3fab6ddc97e574`.

Execution: A fresh Codex subagent with no inherited paper turns was instructed to open only the review task, protocol, manifest, blank record, selected reading, competency questions, query binding, and query result. Its post-run provenance report listed exactly those eight files. It reported no access to or reliance on the ontology, replay receipt, oracle, canonical answer, score, population, provenance, manuscript, paper ledger, prior result summary, external source, or source PDF. This is a declared and reported session boundary, not an operating-system file sandbox.

Preliminary findings: CQ1 received `NOT_EVALUABLE` source support and `NOT_RESPONSIVE` question responsiveness because the query returned no rows despite source blocks describing the network, campaign, and instrument count. CQ2 received `SUPPORTED/PARTIAL`: its two rows are source-supported and reach RC2 through the ridge axis, but they omit the deep qualifier and weaken “beneath” to occurrence at the axis. CQ3 received `SUPPORTED/RESPONSIVE`: four rows expose both reported ranges, units, estimate status, subjects, constituent, and RC2 association. CQ4 received `NOT_EVALUABLE/NOT_RESPONSIVE` because no causal or epistemic row was returned despite source blocks stating the preferred mechanism.

Mechanical boundary: The existing validator resolves the review record through the exact frozen manifest to every returned row and every cited selected-reading block. It accepts the record only as `PRELIMINARY_COMPLETE`. With `require_human_ratification=True`, it refuses the same bytes with `human ratification is required for paper evidence`. A result-specific regression freezes the record digest, labels, full row coverage, locator closure, and refusal boundary. Twenty-three focused review tests pass; Ruff and `git diff --check` pass.

Impact: The preliminary record is a prepared inspection, not human evidence and not an aggregate score. `paper-v4/evaluation-v2/ratification-guide.md` gives Luis the exact review order and forward path. Only a distinct `HUMAN_RATIFIED` record accepted by the validator may support the manuscript's final source-grounded evaluation claims.

### E-0094, clean hash-locked environment reproduces v2 bytes

Date: 2026-09-03

Sources: `paper-v4/environment/requirements.in`; `retained-versions.txt`; `requirements-cp312-macos-arm64.lock`; `environment.json`; `verification.json`; a new virtual environment at ignored path `/private/tmp/malleus-paper-v4-lock-verify`; a new ignored reproduction under `private/paper-v4-v2-lock-verify`; and the complete document-paper plus active v2 paper-local tests.

Resolution: Copying the active environment with `pip freeze` was rejected because it contained a machine-local editable Git coordinate, the unrelated `malleus-code-lab` project, provider SDKs, and broad development tools. The retained input instead names eight direct roots and constrains the exact 89-distribution resolution observed for the paper run. `uv 0.11.2` resolved it for CPython 3.12 and `aarch64-apple-darwin` with cutoff `2026-09-03T09:11:42Z`; every pinned distribution has one or more archive SHA-256 hashes. Binary-only resolution was also rejected after `antlr4-python3-runtime==4.9.3` supplied no compatible wheel. The final lock permits its required source archive rather than silently changing the dependency set.

Clean verification: CPython 3.12.9 on macOS 15.7.9 arm64 created an empty virtual environment. `pip 26.0.1` installed only the hash-checked lock successfully. Running the checked-out source with `PYTHONPATH=.:src` reproduced the 186-block selected reading, all five public v2 result files, and the source-bearing private ledger byte for byte. The ledger digest is `sha256:df5327be6abfabfb49342a0663185d81b8a8056211108ca759ea7cac2901e828`. The complete document-paper and active v2 paper-local gate passed 184 tests in 7.02 seconds. The environment lock guards add three passing tests for exact lock bytes, complete package and hash coverage, exclusion of machine-local or unrelated projects, verification claims, and the source-execution boundary.

Refusals and guardrails: The first clean driver attempt placed private output under `/private/tmp` and correctly refused because source-bearing runs must remain below the repository's ignored `private/` root. Re-running under a new repository-private directory succeeded. A normal install of the repository package then exposed a second boundary: the distributable package intentionally excludes private `src/malleus/_contract_compiler.py`, which this research experiment imports. The environment manifest now requires the exact checkout on `PYTHONPATH`, and a hard test proves both that declaration and the private module's package exclusion. No compatibility adapter or fallback was added.

Boundary: The lock is complete for the identified CPython 3.12 macOS arm64 environment, not a cross-platform guarantee. It identifies but does not vendor the interpreter or operating system and permits all resolver-listed archives for each pinned release rather than one chosen wheel. Reproduction still requires the ignored publisher PDF at its frozen digest. The hash-locked third-party environment does not turn private research seams into public or stable APIs.

Impact: The transitive-environment item is closed. The remaining nonhuman publication work is the arXiv source and rendered-PDF inspection; human ratification remains a separate author action.

### E-0095, lean arXiv bundle compiles and passes visual inspection

Date: 2026-09-03

Sources: `paper-v4/arxiv/main.tex` at `sha256:d6d3da6265d4cfad0c88b632e575930f5786868a8d6143769e5231676f920a71`; `references.bib` at `sha256:e1c746380ac520b5f72b5601b4e8f85275bcff988f0b3d92f0c1ee49df85cf2d`; `README.md` at `sha256:49467f6bbc2f6737502ad3312eb7389b1ee356646b6298a5959728fd589916ba`; `paper-v4/test_publication_consistency.py`; final rendered PDF `output/pdf/malleus-paper-v4.pdf` at `sha256:6b243bafd7331a896a2571b1bcdc24fcf46163014fd72e06c86efae26ca8b25a`; and the final paper-local gate.

Observation: The LaTeX source carries the lean corrected manuscript, one native protocol figure, two result tables, two appendices, and nine verified references. It names Luis Guzman Lorenzo without inventing an affiliation or email. The main text is about 3,500 words before references. Four-step pdfLaTeX and BibTeX compilation produced an eight-page, 226,058-byte letter-size PDF. The final log contains no warning, undefined citation or reference, overfull box, underfull box, or error. All fifteen fonts are embedded and subset; metadata contains the expected title and author; the PDF is unencrypted and has no form or JavaScript.

Visual verification: All eight pages were rendered to 144-dpi PNG images and inspected. The title, abstract, protocol figure, both tables, long hashes, code paths, appendices, hyperlinks, and reference wraps remain within the page and readable. No clipping, overlap, broken glyph, blank required content, or malformed page was observed.

Correction and guard: The first parent-level BibTeX invocation supplied an absolute auxiliary-file path. TeX Live refused to create the corresponding log under its `openout_any` policy. Running BibTeX from the dedicated build directory with the source directory on `BIBINPUTS` succeeded. A second bibliography pass exposed that `plainnat` cannot sort a `techreport` with editors but no authors. The PROV-O entry now uses an editor-bearing book-style record with W3C as publisher and Recommendation as note, preserving the editors' actual role without a warning. The source-bundle instructions retain the simpler clean build from their own directory. The new publication-consistency test derives row counts, access counters, graph counts, and import-closure size from frozen JSON, checks the atomic five-event wording and paper reproducer coordinate in both publications, excludes stale v1 scorer language, and closes every cited BibTeX key.

Final gate: A clean hash-locked CPython environment passed 189 tests across the complete document-paper implementation, active v2 paper artifacts, source-review boundary, environment lock, and publication guard in 6.89 seconds. Ruff passed the same active code and guards. `git diff --check` passed. A final factual audit found no remaining digest or count mismatch, stale v1/scorer language, human-review overclaim, undefined blocking jargon, or reproduction-command defect.

Boundary: The PDF is a reviewed build artifact, not a human-ratified answer evaluation. The exact executable paper snapshot is local commit `8e818103e6867e326544123a30abe756bdd45117`, tree `455e91e3110d1789fb3db8c8a902bc2e87c4eb04`. It contains the v2 code, artifacts, and environment lock but not the later prose. It is not yet reachable through a public immutable tag or archive, and the paper states that limit. Neither the PDF digest nor this code coordinate enters the five experiment identity groups.

Impact: All nonhuman experiment, reproduction, manuscript, source-bundle, compilation, and visual-QA work is complete. Submission still requires Luis's source-review ratification, publication of the exact executable snapshot, and final author review.

### E-0096, executor handover separates paper work from the Core gate

Date: 2026-09-03

Sources: approved executor plan `handover/2026-09-03-paper-executor-plan.md` as amended through Core handover commit `7e9563e8ac32ed2504f990d592e1f4638a584efb`; `design/KNOWLEDGE_PACKS.md`; Core population handover `handover/2026-09-03-core-population-v2.md`; frozen branch `paper-v4-multimodel` at tag `paper-v4-multimodel-v2`, commit `ca8c9de276808ec56d0237f57192c942712fbd1b`; and a read-only run of the active paper and document tests in its retained CPython 3.12.9 environment.

Observation: The handover introduces the missing contract between ontology and ledger mechanics. A `DomainHistoryProfile` states what one change means. The document case selects `source-assertion`; Small Shop selects `state-version`. Assertions in the document profile are retained capture evidence linked to graph fields, not automatically Claim or Event records. The same physical history and replay machinery can therefore serve two semantic-ledger choices without pretending that Core selected either domain meaning.

Core gate: The neutral population compiler has a verified P1 cut. P2 governed integration remains under correction for declarative retention-event role binding and has no accepted final coordinate at this entry. The public facade, document adapter, ontology-supersession replay, full profile, packs, and nascent-project skill required by the approved v4 loop are not yet verified. A selected v4 run must not start against moving private seams.

Parallel evidence: The three frozen producer runs remain useful baseline evidence. In the retained environment, 198 active document-paper, v2, v3-fidelity, review, environment, and publication tests pass with `PYTHONPATH=.:src`. The runs differ sharply in vocabulary and query rows while all admit and replay. Human ratification records exist for all three. This evidence diagnoses ontology variability; it does not supply the new history-profile execution.

KISS finding: The parallel manuscript is about 5,000 Markdown words and the approved v4 matrix adds three single-session producers, one staged-session variant, packs, typed gaps, and as many as two ontology revisions. Executing all of that would answer a larger question than the original thin paper. The smallest coherent paper argument is the distinction among domain vocabulary, domain-history meaning, and accepted replayable change. Whether the v4 matrix stays in this paper or moves to follow-on work is an author scope decision and is not taken here.

Action that does not wait: `paper-v4/experiment-v4/brief-to-skill-map.md` removes paper and question rules from the future common skill, and `paper-v4/experiment-v4/spawn-message.md` reduces the experimenter input to isolation plus the selected-reading path. No Core code, result identity, baseline, manuscript claim, or plan version changed.

### E-0097, Core public population boundary passes independent paper audit

Date: 2026-09-03

Sources: Core implementation commit `d758d40bd084a25c0ca17cdb80720686f4d67a95`, tree `e0fca1db8bc0a50ce5821ba7308686b98382a265`; final governance tip `add4535f757551b6ed30b449e19c31fc97769e1e`, tree `df2c0b7acafc44ff2d45ed9195d13b73577b0979`; `malleus.compiler`; `malleus-compiler contract`; public adopter, integration, ledger, and package artifacts in an isolated read-only clone.

Observation: The public facade compiles exact LinkML source bytes, compiles and prepares the neutral population plan, admits a governed change, reopens and replays history, and exposes the replayed graph's native query methods. The public adopter test admits Small Shop states `B/Y/1@e4` and `B/Y/2@e7`, returns quantity 2 as current, and retains the exact `e4` to `e7` supersession without importing private or research Python modules. Event population refuses as `FAMILY_NOT_ADMITTED`, and the CLI rejects a raw ontology digest.

Verification: The exact final tree passed 326 population, history, public-facade, and graph tests; 199 integration tests; and the ledger checker at 370 entries, head `OVR-000370` / `sha256:7f9bbf9b16de54e32fd365a199e8cce1265b3615a297af9984b26694a346a2c5`. A direct wheel and the wheel rebuilt from its source distribution were byte-identical at `sha256:01e091baa32df38708f53c2285a4b4ee131096861d18255fb7aff50eb0c2c78e`; both distribution artifacts passed `twine check`, and the installed command compiled the exact Small Shop ontology sources.

Boundary: This proves a supported import path and installed command in packages built from that source. It does not stabilize a `private-v0` wire, invent mappings, select domain-history meaning, populate Events, implement Semantic Re-entry, or establish a package release. The paper experiment remains pinned to its selected v2 coordinate until a new run is authorized and complete.

Impact: Core P3 no longer gates paper design. The document adapter, ontology-supersession replay, full profile, packs, and skill still gate the approved v4 execution.

### E-0098, vocabulary and history meaning are separate causes of graph variance

Date: 2026-09-03

Sources: frozen `paper-v4-multimodel` branch at commit `ca8c9de276808ec56d0237f57192c942712fbd1b`; the three retained run manifests, ontology receipts, population receipts, replay receipts, query results, and human review records; `paper-v4/experiment-v3/summarize_runs.py`; `design/KNOWLEDGE_PACKS.md`; and `paper-v4/experiment-v4/semantic-ledger-contract.md`.

Observation: Artifact-derived comparison gives ontology entity/relation counts of 15/33, 20/18, and 8/8; population sizes of 13, 6, and 2; and CQ row counts of `[0,2,4,0]`, `[0,0,0,1]`, and `[0,0,0,0]` for gpt-5.6-sol, Claude Opus 5, and Claude Sonnet 5. All three produced 23-event histories and replayed successfully. The differing graphs therefore expose proposal vocabulary and capture choices, not a failure of atomic admission or replay.

Producer evidence: The retained Sonnet and Opus population reports both say that point-valued ontology fields could not represent source ranges without invention and that the preferred causal mechanism could not preserve its hypothesis status. Sonnet also reports refusing to turn an aggregate instrument count into invented individual instruments. The old protocol left these as absent records plus post-run prose. The v4 contract should expose them during population as source-located `INTERVAL_NOT_EXPRESSIBLE`, `MODALITY_NOT_EXPRESSIBLE`, and `AGGREGATE_ONLY` gaps.

Finding: Packs can reduce reinvention of quantity, time, research, and modality terms. A separate `DomainHistoryProfile` is still required because an ontology does not say whether one accepted change is an assertion, state version, event, or commitment. Under `source-assertion`, there is a further representational risk: a captured `HYPOTHESISED` causal assertion may project as an unqualified graph relation if modality remains only in retained evidence. An optional `SourceAsserted` mixin does not mechanically prevent that flattening.

Impact: The paper must explain vocabulary, history meaning, evidence-bearing population, and replay projection as four separate concerns. A bounded Core inquiry asks the later full-profile and pack pieces to enforce either queryable qualification, Claim reification, a typed provenance join, or refusal. This is not a P3 or P4 blocker and does not select the Core representation.

### E-0099, paper work can advance while v4 execution waits

Date: 2026-09-03

Sources: `handover/2026-09-03-paper-executor-plan.md`; `handover/2026-09-03-core-population-v2.md`; Core P3 PASS in E-0097; and the KISS priority in D-0001 and D-0002.

Observation: Re-running now would recreate the retired paper-local interface. The approved no-brief experiment needs the document adapter, ontology-supersession replay, full history profile, packs, and nascent-project skill. Those Core pieces are not frozen at this entry. Paper-owned isolation text and the brief-to-skill mapping are complete.

Provisional cut for author review: use one document and one default single-session v4 loop in the lean paper. Retain the existing three-producer evidence as diagnostic background. Move the new three-producer matrix and strict staged-session variant to follow-on work. This removes repeated experiment cells without weakening the central claim that a model proposal crosses an explicit, source-grounded, replayable commitment boundary.

Boundary: This is a recorded recommendation under the overnight autonomy instruction, not an accepted author decision. It does not increment the master plan, change the selected result, or authorize a run.

Impact: Continue with paper prose, a dependency-stable run manifest, and harness isolation specifications. Start no v4 model population until the Core execution gate closes.

### E-0100, author accepts the KISS v4 run and overnight relay

Date: 2026-09-03

Sources: the author's instruction to resume the paper and PDF capture as soon as Core finishes, to coordinate exact Core needs through the existing Core task, and to produce a new paper-ready result from rich replay-derived graph queries; the KISS priority in D-0001 and D-0002; and the provisional cut in E-0099.

Decision: Execute one document and one fresh single-session producer loop. Use the shipped `source-assertion` history profile with origin `PARTIAL_IMPORT`, because the run cannot prove exhaustive capture of every assertion in the reading. Withhold competency questions, query binding, answer material, prior runs, and manuscript results from ontology construction and population. Bind evaluator-owned queries only after population and replay freeze. Permit at most two compiler-diagnostic returns and at most two ontology revision rounds triggered by source-located typed gaps. Allow no hand repair, alternate producer, or fallback. Retain the prior three-producer comparison as diagnostic background and move a new matrix and staged-session variant outside this paper.

Boundary: V2 remains the selected result until the v4 Core gate, producer loop, admission, replay, query, inspection, and clean-reproduction gates all pass. Codex may prepare a preliminary source-grounded inspection overnight, but only Luis can ratify it as paper evidence. No current v2 identity or result is rewritten by this decision.

Guard: `paper-v4/experiment-v4/run-contract.json` records the executable boundary without population facts or answer values. Its focused tests require one loop, no fallback, question-free construction, post-replay querying, source-free query execution, and an unbound Core gate that prevents premature execution.

Impact: Master plan 1.2.0 accepts the lean v4 cut. Paper-only preparation continues while Core finishes the remaining public profile, pack, and playbook pieces.

### E-0101, v4 source and selected-reading preflight reproduces byte for byte

Date: 2026-09-03

Sources: ignored publisher PDF at the path fixed by `paper-v4/source/source-manifest.json`; the retained CPython 3.12 environment with `pypdf==6.16.2`; the committed text-layer projector; the selected v2 reading under `private/paper-v4-text-layer/`; and a new ignored preflight under `private/paper-v4-v4-preflight/`.

Observation: The source PDF recomputes to `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`. A fresh strict text-layer extraction produced 11 pages and 186 stable blocks at `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`. The regenerated selected-reading bytes are identical to the retained selected reading.

Boundary: This verifies only the source and reading inputs. It does not start the v4 producer loop, select an ontology, inspect document claims, bind Core, or create another manuscript identity. The scratch reading remains ignored and private.

Impact: The v4 run can reuse the exact selected reading without introducing PDF or extractor drift. Its next external dependency remains the frozen Core execution gate.

### E-0102, public replay-to-source trace and full Small Shop path pass paper audit

Date: 2026-09-03

Sources: Core commit `8e8917533283009d152d3db97329335c663456c3`, tree `f38eae64b9050abce2538ce68d307147abf3968d`; RED `3912c3fc0510ec11291b22651c3547632ca213f0`; GREEN `0a4667acb8fb6605f0ab5b4e74ced7e6a9194582`; governance entry `OVR-000376`; the public Small Shop population fixture and retained evidence; public `malleus.compiler` trace surface; and an independent detached checkout.

Observation: A fresh run from an empty output directory reproduced the committed Small Shop evidence byte for byte. It contains 48 ledger events, five accepted changes, one additive ontology revision, ten historical records, and nine current records. The history bytes are `sha256:cd08faafbce7685f6432ade0549f53b87c8213f74e5e332a45d3ab691daa6739`; evidence is `sha256:b2eeae42456fd6dc2d8cd87808e7f7bceab14382f9179a14abeea1d4cdc7a1c1`. The detached audit reproduced 420 population, history, revision, public-facade, and graph tests plus all 194 Small Shop tests.

Paper impact: `trace_population_record` reconstructs and verifies the path from one replayed graph record through its accepted change, population plan, history profile, field derivations, and retained source and evidence bytes. For document captures, the evidence includes the source assertion and its modality. The paper can therefore query graph topology and join returned records to source assertion, locator, and modality without a paper-local compatibility adapter or a new Core query contract.

Boundary: The five Small Shop plans remain adopter-authored and select the minimal `state-version` profile. This evidence adds no mapping language, universal history semantics, Event population, Semantic Re-entry, effects, stable wire, or release claim. The paper does not rebind its executable baseline at this entry. Its v4 run still waits for the full `DomainHistoryProfile`, grounded packs, and nascent-project playbook.

### E-0103, the active paper gate is explicit

Date: 2026-09-03

Sources: the failed broad collection command over `paper-v4/`; the exact active paper and document test paths; and the locked CPython 3.12 environment.

Observation: A directory-wide pytest invocation collected superseded tests under `paper-v4/experiment/` and historical tests under `paper-v4/retired/`. An otherwise correct explicit invocation also failed when its subprocess lacked the repository and `src` import roots. Neither failure changed repository or experiment state.

Guard: `paper-v4/active-test-manifest.json` names the active test roots, the two excluded historical roots, import roots, and pytest import mode. `paper-v4/run_active_tests.py` validates every path, refuses paths outside the repository or inside excluded history, sets the exact import roots, and runs the manifest. A paper-local test hardens those exclusions.

The first README edit named the verifier's temporary environment directly. That host-local path was replaced by the documented repository-local environment variable. A test now refuses `/private/tmp` in publication instructions.

Impact: The active gate now has one reproducible command. Superseded experiments cannot silently re-enter a v4 pass count.

### E-0104, v4 questions and human review are frozen outside the producer loop

Date: 2026-09-03

Sources: the four existing document competency questions; the accepted D3 and D6 decisions; the v2 source-grounded review method; and the public replay-to-source trace verified in E-0102.

Decision: Keep the four question texts but freeze them as a new v4 artifact at `sha256:fdb5458ed16eda84be844c1ac3c2a72fa8e18a9feb06367c922fae1c3f688a86`. The producer cannot read this artifact. It enters only after ontology, capture, population, admission, and replay have frozen. A new v4 review protocol at `sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379` keeps the two qualitative judgments from v2 and adds the verified graph-row-to-capture trace as review material.

Boundary: The protocol contains no answer oracle, canonical answer, exact-match rule, numeric score, schema symbol, record identifier, or source locator. Codex may create a preliminary record. Only `actor:luis` may ratify it as paper evidence.

Impact: Query richness will be judged through responsive graph rows plus their source and modality traces, without letting the questions shape the ontology or population.

### E-0105, the frozen multi-producer comparison isolates the v4 vocabulary failures

Date: 2026-09-03

Sources: annotated tag `paper-v4-multimodel-v2`, tag object `c9f2bd6dda0cb9a40c5d124230641a81a0261d8d`, commit `ca8c9de276808ec56d0237f57192c942712fbd1b`; its three run manifests, ontologies, population records, replay receipts, query results, and human-ratified review records.

Observation: All three runs accepted, recorded 23 ledger events, reopened, replayed, and made zero forbidden query-time source, network, or embedding accesses. Their graph populations were 13, 6, and 2 records, and their question row counts were `[0,2,4,0]`, `[0,0,0,1]`, and `[0,0,0,0]`. The invariant event count therefore says nothing about semantic coverage. Human review, not row count, found only one fully responsive result: the bounded quantities in CQ-03 from the first run.

Failure classes: The runs independently exposed missing interval support, aggregate-only counts, source fields made mandatory without evidence, unnamed domain entities, and causal relations unable to carry hypothesis status. These map to the v4 typed gaps `INTERVAL_NOT_EXPRESSIBLE`, `AGGREGATE_ONLY`, `REQUIRED_FIELD_ABSENT_IN_SOURCE`, `TYPE_ABSENT`, `RELATION_ABSENT`, and `MODALITY_NOT_EXPRESSIBLE`. In two runs, the word “proposed” or its equivalent existed only in ontology prose, so emitting the causal edge would have flattened epistemic status.

Reuse: V4 keeps deterministic type-bound native traversal, runtime witness identifiers, source-free query guards, and separate judgments for source support and question responsiveness. It retires pre-population query binding, the closed constructible subset, direct-edge-only limits, and question-guided population.

Impact: This comparison is diagnostic background, not another v4 matrix. It explains why grounded packs, typed gaps, a declared history profile, and record-to-capture trace are needed before one new KISS run.

### E-0106, P6 closes the document history semantics after three audit corrections

Date: 2026-09-03

Sources: Core commit `573c45b82725d6f444b70e5ff193302dac883e7b`, tree `6704031dea824572b4d7163ba477c33175397fe7`; corrective GREEN `17c4a8c64b597eb5dd5aaebf623c39ef8f721692`; report commit `bcfa787`; governance head `OVR-000379` / `sha256:60808e07abbea8c3e0470b86323e0fd73cbcbd32d1903c024acba8c5eca27023`; and an independent detached audit.

Audit history: The first P6 draft called the source-assertion origin `EMPTY`, which would have treated one imported paper as the whole domain. The second called each change an assertion while the adapter emitted one multi-assertion plan with one valid time. The first GREEN then declared capture-order time only in profile text while accepting an arbitrary source date, and its capture grammar could not retain assertion-specific times. A later GREEN fixed the code but tests silently repaired stale checked-in examples. Core accepted each reproducer before governance freeze.

Final rule: The shipped profile at `sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5` defines one atomic capture batch as a `COMPOSITION` with origin `PARTIAL_IMPORT`. The adapter owns change valid time and emits `ORDER_ONLY(capture_id)`. Each retained assertion may independently carry nonempty lexical `assertion_time` and `domain_time`; omission remains omission. Modality and time reach graph results through `trace_population_record`. Retraction is not admitted by this profile.

Verification: The exact committed example generator reproduced its raw reading, capture, plan, change, census, and profile artifacts and left the detached checkout clean. The complete Pareto and ledger gate passed 497 tests. No remaining P6 seam request exists.

Impact: E-0100's `ASSERTION` shorthand is superseded. P6 is verified. The v4 run remains blocked only on P7 grounded packs plus the grounding rite and P8's nascent-project playbook.

### E-0107, active v4 prose is rebound to the accepted execution contract

Date: 2026-09-04

Sources: author decision E-0100; the v4 run contract; audited Core P6 commit
`573c45b82725d6f444b70e5ff193302dac883e7b`, tree
`6704031dea824572b4d7163ba477c33175397fe7`; and the public
`trace_population_record` seam.

Observation: The machine-readable v4 contract already required one
question-blind producer loop and post-replay query binding, but active master
plan prose still described the selected v2 path: two producer sessions,
question-visible population, pre-population query binding, private history, and
paper-local GraphRecipe lowering. Those statements contradicted E-0100 and the
verified public P6 boundary.

Correction: Active v4 prose now names one fresh single-session producer loop,
one atomic capture batch, questions withheld until replay, terminal-change-only
admission, public Core population and replay calls, and a required replay
record-to-retained-assertion trace for epistemic status. Historical v1 and v2
results remain unchanged. The five v2 identity groups remain selected until a
complete v4 run replaces only ontology, ledger plus replay receipt, and query
binding identities.

Guard: A focused consistency test first failed on both the stale plan language
and the broad `QUERYABLE_OR_TYPED_REFUSAL` modality placeholder. It now rejects
those superseded active-path statements and requires the accepted v4 boundary.
The focused contract gate passes 9 tests; the complete active paper gate passes
198 tests.

Boundary: This entry records no new author decision and does not bump the master
plan version. It does not bind unfinished P7 or P8 bytes, create population
facts, alter selected v2 evidence, or start the producer run.

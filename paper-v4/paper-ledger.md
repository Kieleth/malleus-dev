# Malleus paper ledger

Ledger version: 0.8.0

Opened: 2026-09-02

Plan tracked: `paper-master-plan.md` version 0.8.0

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

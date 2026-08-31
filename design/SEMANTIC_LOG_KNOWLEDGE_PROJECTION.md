# Semantic Log and Accepted Knowledge Projection

Status: non-authoritative literature and design synthesis. Current-capability
statements are observational and must defer to code and implementation-status
documents.

The semantic-history and replay profile is optional. It adds a retained
authority, historical replay, and accepted-view reconstruction to the base
protocol. An adopter may omit it and retain only the guarantees of the lower
profiles it implements. The current JSONL ledger and NetworkX projector are a
reference implementation of this profile, not universal storage requirements.

Evidence pass: 2026-08-28.

## The exact question

Under what explicit closure assumptions can an ontology-bound protocol history
determine one accepted temporal knowledge-graph view?

This is narrower than asking whether Malleus can encode reality. An ontology
selects the distinctions a system will represent. It is a scoped,
purpose-relative model, not reality itself. The ledger records what the
protocol recognized and decided, not everything that happened in the domain.
The accepted graph represents protocol-governed commitments, not factual truth
by definition.

Within this optional profile, the target thesis is:

> Given a declared contract and complete retained input closure, Malleus can
> treat one ordered protocol ledger as the authoritative history of admitted
> protocol records and derive accepted temporal knowledge views from it under
> identified projectors and interpretation rules.

The literature supplies established versions of logs, event sourcing, RDF,
temporal graphs, ontology-guided extraction, and log-to-graph projection. That
independent convergence corroborates mechanisms Malleus reached empirically
and gives the project techniques, failure cases, and comparison oracles to
reuse. The contribution candidate is the protocol that composes proposal,
structural validation, semantic admission, requested review with an
independence policy, epistemic decision, valid-time interpretation, evolution,
and replaceable projection behind explicit contracts, plus the results of
testing that complete composition. Complete cross-version replay identity
remains a design target.

## What exists now

The current implementation already provides:

1. One JSONL protocol ledger with contiguous sequence numbers, nondecreasing
   transaction time, actor and ontology identities, typed payloads, previous
   hashes, and event hashes.
2. Content-addressed protocol records inside those event envelopes.
3. Explicit graph-base and candidate-subgraph artifacts.
4. Atomic coupling of a candidate-bound acceptance decision and accepted graph
   application in one protocol event.
5. Replay that restages writes, recomputes identities, and rebuilds an accepted
   NetworkX read model.
6. Transaction-prefix and valid-time views, explicit supersession,
   indeterminate temporal membership, and optional caller-supplied
   selected-prefix head and event-count checks. Historical `.as_of()` can
   separately check the containing ledger head and event count.

These are call-time checks over identities already returned by
`AcceptedGraphView`. They add no view field, persisted wire member, ontology
term, capability stage, or release claim.

Several limits are equally important:

1. The API is logically append-only, but each append physically rewrites the
   complete file through an atomic same-directory replacement.
2. A filesystem actor can rewrite and rehash the entire ledger. It can also
   remove complete trailing records while leaving a valid hash-linked prefix.
   Detecting a different complete rechain requires an authentic, independently
   retained expected complete-ledger head. That head, or an applicable expected
   complete-ledger event count, can detect clean suffix removal. Direct replay
   and `current()` apply their expectations to the complete ledger. Historical
   `.as_of()` can separately check both its selected prefix and the containing
   ledger. Its selected-prefix check alone survives later-tail removal and does
   not authenticate that tail. Byte truncation of the final record is rejected
   by the terminal-newline check.
3. The mandatory first `EXTERNAL_SNAPSHOT_ANCHORED` event stores an opaque
   snapshot digest inside the ledger. It is neither a graph base nor an
   external witness of the ledger head. A later `GraphBaseArtifact` binds
   metadata and digests for a graph supplied out of band.
4. Core Malleus has no signature, transparency service, trusted timestamp,
   remote witness, signed checkpoint, or split-view detector.
5. Core Malleus currently derives an in-memory NetworkX accepted view. Generic
   SQLite, central-store, portal, or arbitrary-backend materialized views are
   not shipped capabilities.
6. Current ledger replay requires a caller-supplied `OntologyRegistry`.
   Accepted-graph projection additionally requires the exact graph base supplied
   out of band. Ledger bytes alone cannot reconstruct that graph. Current
   records do not bind an `EffectiveContract`, projector identity, reader
   identity, complete interpretation identity, or a declared side-input set.
7. Structurally refused writes remain caller-local diagnostics. They are not
   protocol events, so the ledger is not a record of every attempted system
   change.

The accurate integrity claim is therefore **ordered and chain-validated, with
optional caller-supplied prefix and containing-ledger checkpoints**. Direct
replay checks the complete ledger. `current()` checks its complete selected
prefix. Historical `.as_of()` distinguishes the selected prefix from the
containing ledger. A selected-prefix checkpoint alone does not authenticate
later tail records. "Externally anchored," "provable," and "tamper-proof" are
not current core properties.

## The log-primary model

Jay Kreps's 2013 essay is the modern architectural synthesis that most directly
matches this design. It treats a log as an ordered history of what happened,
with tables and indexes as projections. It also says that the log is only the
infrastructure. Metadata, schemas, compatibility, and evolution remain to be
solved.

Martin Kleppmann develops the operational consequence: read stores can be
materialized views maintained by independent translation processes and rebuilt
from retained history. This supports replaceable projectors, independent
testing, and recovery from a bad view implementation. It does not mean that a
log must always be the source of record, or that every database connected to a
log is automatically a projection.

For Malleus, complete semantic projection closure is a proposed two-stage
contract:

```text
accepted_history(t) =
  fold(projector, initial_base, verified_protocol_prefix(t), side_inputs)

view(t, v) =
  resolve(accepted_history(t), interpretation_profile, valid_time=v)
```

The result is deterministic only if every argument that can affect the fold is
identified, retained, and available. A future closure contract should produce a
typed refusal for a missing argument and mechanically localize divergence. The
current core has neither a generic closure manifest nor a divergence localizer.

The proposed qualification rule for an external Malleus projection is:

1. Its complete authoritative input is the retained protocol history plus
   declared side inputs.
2. It has no independent write path that changes governed state.
3. Its projector and interpretation identities are pinned.
4. A full rebuild and an incremental build converge on the same declared
   output identity.

If a store accepts independent writes, it is another authority and needs an
explicit reconciliation protocol. Calling it a materialized view would hide
that boundary.

## Where the semantics come from

The log does not acquire semantics merely because its payload uses tuples. A
record is interpreted under a contract.

| Component | Protocol role |
|---|---|
| Ontology and effective contract | Select the vocabulary, types, constraints, reference rules, and sanctioned commitments |
| Identified protocol event | Record one ordered protocol transition with actor, time, version, and integrity context |
| Typed record or candidate subgraph | Carry the proposed or decided semantic content |
| Evidence and review records | Bind claims to sources and record what the requested reviewer assessed; independence remains a policy requirement |
| Epistemic decision | Select which structurally valid proposal becomes accepted protocol knowledge |
| Projector | Execute the declared fold from protocol history into one view |
| Accepted temporal KG | Materialize the commitments accepted under one transaction and valid-time interpretation |
| Migration receipt | Record and grade an asserted ontology-identity transition; current receipts do not carry or execute a reader, mapping, or query rewrite |

This yields a more precise decomposition:

```text
contract composition  = alphabet, grammar, and allowed commitments
protocol event        = identified and ordered protocol transition
candidate subgraph    = atomic semantic proposal
assent                = epistemic admission decision
ledger                = retained protocol history
projector             = interpreter and fold; explicit version identity is proposed
accepted temporal KG  = materialized protocol-governed view
```

The word "knowledge" refers to accepted epistemic state inside the declared
protocol boundary. It does not convert acceptance into correspondence truth.

## Encoding as a semantic state-transition protocol

The useful extension of the log model is not to put "semantics" inside log
bytes. It is to bind each admitted change to the vocabulary and rules that make
the change interpretable. Three levels must remain separate:

1. A **domain occurrence** is something claimed to have happened in the modeled
   world. It may be incomplete, disputed, or observed late.
2. A **semantic proposal** is a typed assertion or atomic candidate subgraph
   about that occurrence or another domain object, with valid time and evidence
   where required.
3. A **protocol event** records what Malleus did with that proposal in
   transaction order: register, review, accept, reject, defer, or apply.

The ontology and admission contract determine which proposals are expressible
and admissible. The linear ledger retains protocol order and integrity context.
The projector folds accepted graph operations and later resolves valid time.
The KG contributes identity, typed relations, provenance, dependency, and
supersession structure that a generic event log does not supply.

This is an encoding of **protocol-governed commitments about a selected domain**,
not a lossless encoding of the domain and not a claim that every real-world
change appears in the ledger. The closure question is empirical: for a declared
domain boundary, can every admitted semantic transition be represented and can
every materialized assertion be traced back to its governing history and
interpretation inputs?

## Representation layers that must remain distinct

Malleus has three implemented representation layers and one accepted atomic
contract-fact grammar:

1. Protocol JSON event envelopes.
2. Typed content-hashed protocol records inside event payloads.
3. Graph operations and candidate subgraphs that change accepted graph state.
4. Exact frontend-neutral `{subject, predicate, object}` contract facts,
   accepted by OD-005. The production compiler and runtime API do not exist,
   `ContractFactSet` remains `Candidate`, and stable public fact identities are
   blocked on OD-009.

A subject-predicate-object fact is the selected canonical semantic fact atom
for contract meaning. It is not yet a public or persisted wire artifact, a
complete domain event, or a universal protocol event. Many changes require
several claims to be admitted atomically. RDF graphs also erase duplicate
occurrence and ordering, so a bare triple set cannot replace the ordered event
envelope.

The ledger should stay linear for atomic ordering, integrity, and replay.
Causality, derivation, dependency, and supersession belong as typed edges in
the Malleus KG. A causal subgraph can be acyclic without introducing a second
authoritative DAG system.

## The DNA analogy, repaired

The existing documents call both the ontology and the ledger "DNA." Neither
mapping is sufficient on its own. The useful analogy is distributed across the
system:

| Biological metaphor | Malleus analogue |
|---|---|
| Alphabet and grammar | Ontology plus effective contract |
| Encoded change unit | Typed record or atomic candidate subgraph |
| Heritable history | Ordered retained protocol ledger |
| Expression machinery | Reader, projector, rules, and runtime profiles; pinning their identities is a target closure requirement |
| Expressed state | Accepted temporal KG view |
| Selection boundary | Designed validation, review, and assent, with no faithful biological equivalent |

This captures the user's original intuition without turning it into an
architecture claim. The ledger carries history. The contract determines how
records can mean. The projector expresses that history as a graph. None of the
parts alone is the DNA.

The analogy stops where the guarantees begin. DNA does not carry evidentiary
citations. Biology also does not provide accountable protocol arbiters,
deterministic replay contracts, or independently retained ledger heads. Use the
analogy to generate experiments, not as evidence.

## Intellectual lineage

### Representation and ontological commitment

McCarthy and Hayes's situation calculus models actions and the situations they
produce. Kowalski and Sergot's Event Calculus instead starts from local events
that initiate or terminate time-varying fluents. Its database examples
explicitly allow later updates about past events. This is closer to Malleus's
separation of transaction order from domain-valid time than a simple
"current-state" database is.

Davis, Shrobe, and Szolovits define a knowledge representation as an imperfect
surrogate, a set of ontological commitments, a fragmentary theory of
reasoning, a computational medium, and a medium of expression. Gruber defines
an ontology as an explicit specification of a conceptualization. Together they
make the phrase "encode reality" too strong. Malleus encodes selected,
contract-governed claims about a domain.

Temporal RDF and later temporal-KG work provide the distinction between when a
claim is recorded and when it is asserted to hold. Malleus deliberately uses
that distinction rather than deriving temporal semantics from ledger sequence.

### Revision and evolving meanings

Doyle's truth-maintenance system and de Kleer's assumption-based extension
already establish assumptions, justifications, dependency tracking,
inconsistent contexts, retraction, and belief revision. Malleus inherits
dependency-aware revision from this lineage. Its narrower research question is
how to bind those mechanisms to immutable protocol history, evidence, valid
time, and explicit acceptance.

Ontology evolution adds a separate fault line. Noy and Klein distinguish it
from ordinary schema evolution because a change can alter the meaning of
existing knowledge, not only its storage shape. Ontology identity,
compatibility classification, interpretation of old records, data
transformation, and query rewriting are therefore separate objects. A linear
ledger preserves which contract identity governed an old record, but it does
not by itself say how a new reader should interpret that record.

Malleus has one released mechanism and one current-source mechanism that must
not be conflated. Bitemporal supersession revises accepted domain assertions
without mutating old events. Current source beyond the released `0.13.3`
package boundary adds a generic `MigrationReceipt`; Recon is its only source
consumer. The receipt records and grades an asserted ontology-identity
transition, but does not carry the transformation or reader needed to cross it.
Complete contract evolution therefore still requires an identified migration
plan and compatible reader, or a typed refusal.

### Logs and materialized views

Database recovery logs, state-machine replication, event sourcing, Kreps's
log-centric integration model, and Kleppmann's materialized-view architecture
establish the core log-to-view pattern. Malleus should cite and reuse it
directly.

Kreps is not the intellectual origin of append-only logs. His essay is the
clearest modern synthesis and the most direct bridge from database logging to
system-wide data integration.

### Independent convergence in semantic systems

These systems independently reached mechanisms that Malleus also reached from
its product and evidence constraints. They corroborate the direction, supply
techniques to acquire, and show which integration questions deserve empirical
tests:

| Work | What it confirms or contributes | What Malleus composes around it |
|---|---|---|
| RDF Stream Processing, including C-SPARQL, CQELS, and RSP-QL | Time-annotated RDF streams, continuous semantic queries, windows, reporting policies, and formal result semantics | Acquire explicit window, evaluation, and reporting-policy identities; compose them with durable evidence admission and accepted-state replay |
| Linked Data Event Streams 1.0 | Append-only immutable RDF members, ordering terms, versions, transactions, shapes, multiple views, and retention declarations | Acquire immutable-member, version, retention, publication, and synchronization machinery as a projection of the Malleus authority |
| Blue Brain Nexus | Global append-only event history, event sourcing, SHACL-gated resources, revisions, historical reconstruction, and graph/search projections | Acquire event-sourced reconstruction, validation, and projection tests; compose them with Malleus proposal, review, assent, temporal, and evolution boundaries |
| Event Knowledge Graphs | Events and entities represented together, with correlation and per-entity order | Acquire event/entity correlation and explicit order relations inside the typed KG while retaining the protocol ledger as the write authority |
| SLOGERT | Automatically extracted log templates whose instances are instantiated or expanded into ontology-grounded RDF through OTTR | Acquire OTTR-based extraction and modular-template techniques; compose them with accepted temporal state and epistemic control |
| OntoLogX | Learned extraction from raw logs into ontology-grounded per-event KGs, with syntax, SHACL, and semantic validation, iterative correction, and persist-only-valid gating | Independently confirms the proposal, typed-check, retry, and commit-gate loop; Malleus composes candidate identity, requested review and assent, temporal application, and ledger replay around it |
| ActiveGraph, *The Log is the Agent* | Authoritative append-only agent log, deterministic typed graph fold, replay, forks, diffs, causal lineage, and retained model/tool responses | May 2026 preprint; Malleus's ontology-bound evidence, epistemic-review, temporal, evolution, and integrity boundaries differ |
| ActiveGraph, *Regimes* | Typed candidate patches, static checks, sandbox execution, in-sample evaluation, held-out validation, and logged promotion or discard | June 2026 preprint; independently confirms the value of proposal, evaluation, gating, promotion, and replayable improvement as separate stages |
| Nanopublications and trusty URIs | Atomic assertion packages with assertion provenance and publication information; a nanopublication assigned a trusty URI can have content-derived identity | Acquire assertion, provenance, and publication packaging plus optional content-derived identity; compose them with ordered acceptance and replay |

This independent convergence corroborates the architecture and supplies
mechanisms, failure cases, and tests to reuse. The RDF Stream Processing
lineage, for example, shows that window, evaluation, and reporting policies are
interpretation inputs that must be identified if a streaming projection is
expected to replay. The research question is whether Malleus's complete
protocol composition creates new capabilities or measurable behavior at the
boundaries between these pieces.

### Neurosymbolic systems

Garcez and Lamb's account, first circulated as a 2020 preprint and published in
peer-reviewed form in 2023, requires principled integration of learned models
with symbolic representation and reasoning. The ledger, ontology, and KG alone
are symbolic. Under the operational criterion proposed in this document, a
Malleus deployment is neurosymbolic when a learned component proposes or
extracts candidate content and the symbolic protocol validates, constrains,
reasons over, or returns typed failures that affect the next proposal.

The useful loop is:

```text
source
  -> learned proposal
  -> typed candidate
  -> symbolic contract and rule checks
  -> requested review under an independence policy, or another policy decision
  -> accept, reject, defer, or retry with typed failure evidence
  -> replay-derived accepted graph
```

OntoLogX supplies recent extraction, iterative correction, and persist-only-
valid gating. Malleus's narrower additions are candidate identity, requested
review and assent, temporal application, and ledger-bound replay. Neither
substitutes for the other.

### Adjacent improvement-protocol framing

Anthony Butler's March 2026 essay, *From AutoResearch to
Proof-of-Improvement*, is useful practitioner framing, not primary research
evidence. Its main reusable observation is an asymmetry: proposing an
improvement can be expensive while evaluating a fixed candidate against a
predeclared objective can be cheaper. That maps onto Malleus's existing
separation of external execution, pinned monitoring, epistemic control, and
hash-linked protocol history.

The terminology and network design do not transfer. Malleus records replayable
checks, observations, decisions, and attestations. It does not produce a formal
proof that one candidate is better, so `Proof-of-Improvement` should not become
a Malleus term without a stronger proof boundary. Candidate derivation and
experiment lineage belong as typed, acyclic relations inside the Malleus KG;
the linear protocol ledger remains the integrity, atomic-ordering, and replay
authority. The essay's staking, slashing, open-network consensus, and zero-
knowledge extensions are speculative relative to Malleus's current
single-writer and trusted-rule boundary.

A future research-local improvement contract could precommit:

1. Baseline and candidate identities.
2. Metric direction and minimum accepted delta.
3. Evaluation corpus and split identities.
4. Repetitions, seeds, and tolerance.
5. Budget and stopping rule.
6. Verifier identity and independence requirement.

That object should not enter core before a real consumer exists and passes the
normal independent-consumer gate.

### Integrity and witnessing

A local hash chain detects edits, insertions, deletions, and reorderings that no
longer satisfy the envelope and chain rules. Clean removal of complete trailing
records leaves a valid prefix and is not detected by chain validation alone.
A different complete rechain requires an authentic, independently retained
expected complete-ledger head. That head, or an applicable expected complete-
ledger event count, can detect clean suffix removal. Direct replay, `current()`,
and the containing-ledger arguments on historical `.as_of()` expose those
checks. The selected-prefix arguments on `.as_of()` verify only the cutoff
prefix. Core provides no checkpoint store and no generic external witness. RFC
9162 shows the stronger transparency-log boundary: signed tree heads, inclusion
and consistency proofs, monitors, and a response to inconsistent views. Even
that protocol needs monitoring or gossip to expose equivocation.

External ledger-head witnessing is therefore a possible Malleus extension, not
a present property. It should remain separable from semantic admission. A
cryptographically consistent history can contain false claims, and a
well-supported claim can live in a history that lacks an external witness.

The protocol should expose integrity as a replaceable contract. A witness can
consume a committed ledger head and emit a signed checkpoint,
transparency-log receipt, trusted timestamp, or another attestation while the
domain ontology, evidence admission, assent state machine, and graph projector
remain unchanged. Replacing the event-hash or signature grammar may require a
new integrity profile or persisted-wire epoch, but not a new semantic fabric.
This is the same modularity rule applied elsewhere in Malleus: strengthen or
replace one stage through typed boundaries and conformance tests.

## Existing decisions this synthesis does not reopen

1. LinkML 1.11.1 remains the pinned, replaceable first-party contract frontend
   and compiler baseline for v0. This is accepted future design. Current core
   directly interprets LinkML-shaped YAML through `OntologyRegistry`; it does
   not execute official LinkML semantics. The lasting boundary is the
   frontend-neutral contract fact set and LinkML-free compiled runtime.
2. A custom contract frontend may replace LinkML only by producing the same
   normative intermediate and passing the same conformance suite.
3. stOTTR 0.1.4 under the Malleus GraphRecipe Profile v0 remains the selected
   authored topology-template representation. OTTR expands finite topology; it
   does not govern evidence, admission, provenance, migration, or effects.
4. Within the semantic-history and replay profile, the protocol ledger remains
   the one linear write authority.
5. Causal and dependency relations remain typed KG structure, not a separate
   DAG subsystem.
6. Contract facts, protocol events, graph operations, and accepted views remain
   separate representations.

LDES is worth evaluating later as a publication or synchronization projection.
It should not become a second authority without a consumer and a separate
decision.

## Candidate dependency facts

These tuples capture the synthesis without promoting it into the canonical
foundation graph. "Implemented," "accepted design," and "proposed" remain
separate states. The `slkp:` implementation subjects and predicates are local
observational pseudotuples, not canonical `mfg:` vocabulary.

```turtle
# Implemented, locally observed rather than canonicalized
slkp:ProtocolLedger slkp:orders slkp:ProtocolEvent .
slkp:ProtocolRecord slkp:recordedIn slkp:ProtocolEvent .
slkp:CandidateSubgraphArtifact slkp:contains slkp:TemporalWrite .
slkp:AcceptedGraphApplication slkp:applies slkp:CandidateSubgraphArtifact .
slkp:AcceptedGraphProjector slkp:derives slkp:AcceptedGraphView .
slkp:AcceptedGraphView slkp:dependsOn slkp:ProtocolLedger .

# Accepted design, not production runtime
mfg:LinkMLFrontend rdf:type mfg:ContractFrontend .
mfg:EffectiveContract mfg:composedOf mfg:ValidatedContractFactSet .
mfg:EffectiveContract mfg:interpretedUnder mfg:NormativeAdmissionProfile .
okg:GraphRecipe mfg:representedBy okg:MalleusGraphRecipeProfileV0 .

# Canonical Candidate objects
mfg:ContractCompilationResult mfg:binds mfg:ContractFrontend .
mfg:ContractCompilationResult mfg:produces mfg:ContractFactSet .
mfg:AcceptedTemporalGraphVersion mfg:identifiedBy mfg:AcceptedTemporalGraphVersionHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:SourceProtocolLedgerHead .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:ContractCompositionHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:CanonicalStructuralStateHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:TemporalMetadataDigest .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:AcceptanceHead .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:MaterializationHead .

# Proposed local extension, not canonical
slkp:CompleteProjectionClosure mfg:binds mfg:AcceptedTemporalGraphVersionHash .
slkp:CompleteProjectionClosure mfg:binds mfg:ProjectionImplementation .
slkp:CompleteProjectionClosure mfg:binds mfg:ProjectionProfile .
slkp:CompleteProjectionClosure mfg:binds slkp:SuppliedGraphBaseIdentity .
slkp:CompleteProjectionClosure mfg:binds slkp:SuppliedGraphBaseDigest .
slkp:CompleteProjectionClosure mfg:binds slkp:ReaderIdentity .
slkp:CompleteProjectionClosure mfg:binds slkp:InterpretationProfile .
slkp:CompleteProjectionClosure mfg:binds slkp:DeclaredSideInputSetDigest .
slkp:CompleteProjectionClosure mfg:binds slkp:TransactionCoordinate .
slkp:CompleteProjectionClosure mfg:binds slkp:ValidTimeCoordinate .
slkp:CompleteProjectionClosure mfg:binds slkp:OutputDigest .
slkp:IntegrityProfile slkp:consumes mfg:SourceProtocolLedgerHead .
slkp:IntegrityProfile slkp:produces slkp:ExternalHeadAttestation .
slkp:ExternalHeadAttestation slkp:witnesses mfg:SourceProtocolLedgerHead .
```

The implemented `AcceptedGraphView` also consumes the exact caller-supplied
`KnowledgeGraph` base and explicit transaction and valid-time parameters. Those
inputs are not canonical foundation-graph classes, so the implemented block
does not invent tuples for them.

`CompleteProjectionClosure` and every `slkp:` term are proposed locally by this
document. The implemented pseudotuples describe observed code relations; they
do not declare ontology terms. The closure terms extend, rather than duplicate,
the canonical Candidate
`AcceptedTemporalGraphVersionHash`, `ProjectionImplementation`, and
`ProjectionProfile` vocabulary. Their purpose is to make "this store is a
materialized view" checkable by binding the exact base identity and digest,
reader, projector, interpretation profile, side inputs, view coordinates, and
output digest. No such closure object is implemented or promoted into the
foundation graph.

## Empirical program

The right empirical target is relative closure, not universal completeness or a
formal proof:

> For a declared domain contract and retained input closure, every admitted
> state transition has an identified semantic representation; every
> materialized assertion traces to accepted protocol events and pinned
> interpretation machinery; and rebuilding yields the declared projection.
> Future closure instrumentation should localize any divergence mechanically.

That statement can be attacked with executable cases:

1. Full replay and incremental replay produce the same graph and projection
   identity.
2. A future closure manifest causes a missing graph base, ontology, reader,
   projector, timezone database, or declared side input to refuse instead of
   guessing.
3. Reordering, deleting from the middle, duplicating, or mutating a ledger event
   breaks envelope or chain validation unless the history is consistently
   rechained. Clean suffix removal leaves a valid prefix. Direct replay,
   `current()`, and the historical containing-ledger checks detect a different
   complete rechain only when given an independently retained expected complete-
   ledger head. That head, or an applicable expected complete-ledger event
   count, can detect clean suffix removal. A historical selected-prefix
   checkpoint alone does not authenticate any later tail.
4. Two independently witnessed incompatible heads expose equivocation. This
   remains a future extension until an external witness exists.
5. A retroactive domain correction changes valid-time views only in transaction
   prefixes that include the correction.
6. A late event preserves transaction order while asserting an earlier valid
   time.
7. A multi-record semantic change is accepted or rejected atomically.
8. A causal order different from ledger order is represented in KG edges
   without changing the linear integrity order.
9. A future migration plan and compatible reader preserve a declared view for a
   total migration, expose explicitly indeterminate records for a partial
   migration, and refuse across a hard break. Current migration receipts alone
   do not perform these transformations.
10. LinkML and an independently implemented custom frontend produce the same
    frontend-neutral contract facts for the shared conformance corpus.
11. An OTTR GraphRecipe expansion and an independently authored expected
    operation set converge before admission.
12. Swapping the projector changes projection identity even if one observed
    output happens to match.
13. A derived SQLite or portal view can be deleted and rebuilt without an
    independent write or manual repair.

These cases belong in the Gedankenexperiment and CI program only after their
input contracts, independent oracles, and expected failure classes are fixed.
Passing examples alone would not establish closure.

## Claim language

Defensible:

> When the semantic-history and replay profile is selected, Malleus uses one
> ontology-bound protocol ledger as the authoritative history for
> replay-derived accepted temporal knowledge views.

> The design composes established log, event-sourcing, temporal-KG,
> knowledge-representation, provenance, and neurosymbolic lineages behind an
> evidence-admission protocol.

> Its local envelope and hash-chain checks detect changes that violate the
> recorded sequence, payload identities, or hash links. An authentic,
> independently retained expected complete-ledger head supplied to direct
> replay, `current()`, or the historical containing-ledger check detects a
> different complete rechain or clean suffix removal, barring a hash collision.
> An expected complete-ledger event count can also detect clean suffix removal.
> A historical selected-prefix checkpoint alone does not authenticate any later
> tail.

Not defensible:

- Malleus encodes reality.
- The ledger is factual truth.
- A triple is the universal event format.
- Every system change is recorded.
- Every store is already a Malleus materialized view.
- Malleus invented semantic logs or event-sourced knowledge graphs.
- The ledger is externally anchored, tamper-proof, or formally proven.
- Replay proves that accepted claims are true.
- The protocol is complete without a declared domain and input closure.

## Research record

The focused Recon notebook is
[`research/semantic_log_knowledge_projection_recon/`](../research/semantic_log_knowledge_projection_recon/).
Its current validated projection metrics are recorded in the notebook primer.
The ledger is the notebook authority;
`build/*` contains deterministic navigation projections. Recording a claim
there does not make the claim true or replace the primary source.

The older
[`research/malleus_library_protocol_recon/`](../research/malleus_library_protocol_recon/)
already covers event sourcing, transactions, temporal databases, revision, and
provenance. The focused notebook adds the missing direct lane for Kreps,
Kleppmann, semantic event streams, event and situation calculus, temporal RDF,
semantic-log systems, and independently convergent log-to-KG systems.

## Primary sources

- Jay Kreps, ["The Log," 2013](https://www.linkedin.com/blog/engineering/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying).
- Martin Kleppmann, ["Turning the Database Inside-Out," 2015](https://martin.kleppmann.com/2015/03/04/turning-the-database-inside-out.html).
- Martin Fowler, ["Event Sourcing," 2005](https://www.martinfowler.com/eaaDev/EventSourcing.html).
- Randall Davis, Howard Shrobe, and Peter Szolovits,
  ["What Is a Knowledge Representation?", 1993](https://courses.csail.mit.edu/6.803/pdf/davis.pdf).
- Thomas Gruber,
  ["A Translation Approach to Portable Ontology Specifications," 1993](https://tomgruber.org/writing/ontolingua-kaj-1993.pdf).
- John McCarthy and Patrick Hayes,
  ["Some Philosophical Problems from the Standpoint of Artificial Intelligence," 1969](https://www-formal.stanford.edu/jmc/mcchay69/mcchay69.html).
- Robert Kowalski and Marek Sergot,
  ["A Logic-based Calculus of Events," 1986](https://www.cs.brandeis.edu/~cs112/cs112-2004/newReadings/Kowalski-Sergot.pdf).
- Claudio Gutierrez, Carlos Hurtado, and Alejandro Vaisman,
  ["Introducing Time into RDF," 2007](https://doi.org/10.1109/TKDE.2007.34).
- Daniele Dell'Aglio, Emanuele Della Valle, Jean-Paul Calbimonte, and Oscar
  Corcho,
  ["RSP-QL Semantics," 2014](https://doi.org/10.4018/IJSWIS.2014100102).
- Davide Francesco Barbieri et al.,
  ["C-SPARQL," 2010](https://doi.org/10.1142/S1793351X10000936).
- Danh Le-Phuoc, Minh Dao-Tran, Josiane Xavier Parreira, and Manfred Hauswirth,
  ["A Native and Adaptive Approach for Unified Processing of Linked Streams and Linked Data," 2011](https://doi.org/10.1007/978-3-642-25073-6_24).
- [Linked Data Event Streams 1.0, 2026](https://semiceu.github.io/LinkedDataEventStreams/releases/1.0.0/index.html).
- Sy et al.,
  ["Blue Brain Nexus," 2023](https://doi.org/10.3233/SW-222974).
- Stefan Esser and Dirk Fahland,
  ["Multi-Dimensional Event Data in Graph Databases," 2021](https://doi.org/10.1007/s13740-021-00122-1).
- Dirk Fahland,
  ["Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs," 2022](https://doi.org/10.1007/978-3-031-08848-3_9).
- Andreas Ekelhart, Fajar J. Ekaputra, and Elmar Kiesling,
  ["The SLOGERT Framework for Automated Log Knowledge Graph Construction," 2021](https://doi.org/10.1007/978-3-030-77385-4_38).
- Cotti et al.,
  ["OntoLogX," 2026](https://doi.org/10.1002/aisy.202501381).
- Yohei Nakajima,
  ["The Log is the Agent," 2026 preprint](https://arxiv.org/abs/2605.21997).
- Yohei Nakajima,
  ["Regimes," 2026 preprint](https://arxiv.org/abs/2606.10241).
- Artur d'Avila Garcez and Luis C. Lamb,
  ["Neurosymbolic AI: The 3rd Wave," 2023](https://doi.org/10.1007/s10462-023-10448-w),
  first circulated as a 2020 preprint.
- Jon Doyle,
  ["A Truth Maintenance System," 1979](https://doi.org/10.1016/0004-3702(79)90008-0).
- Johan de Kleer,
  ["An Assumption-Based TMS," 1986](https://doi.org/10.1016/0004-3702(86)90080-9).
- Natalya Noy and Michel Klein,
  ["Ontology Evolution: Not the Same as Schema Evolution," 2004](https://doi.org/10.1007/s10115-003-0137-2).
- [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/) and
  [SHACL](https://www.w3.org/TR/shacl/).
- [Nanopublication Guidelines](https://nanopub.net/guidelines/working_draft/).
- Tobias Kuhn et al.,
  ["Nanopublications: A Growing Resource of Provenance-Centric Scientific Linked Data," 2021](https://doi.org/10.7717/peerj-cs.387).
- [SPARQL 1.2 RL](https://www.w3.org/TR/sparql12-rl/).
- [RFC 9162, Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162.html).

## Adjacent public framing

- Anthony Butler,
  ["From AutoResearch to Proof-of-Improvement," 2026](https://abutler.com/from-autoresearch-to-proof-of-improvement-decentralising-optimisation-and-discovery/).
  This essay is recorded as practitioner framing, not primary research
  evidence.

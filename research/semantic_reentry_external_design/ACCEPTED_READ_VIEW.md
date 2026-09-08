# Accepted read-view boundary

Role: REFERENCE_IMPLEMENTATION of an adopter-side read adapter for the selected
compiler-enabled history and experimental finite action attachment. This is an
in-memory input to pure Re-entry, not a new Core context, protocol record,
checkpoint, persisted view, ledger or accepted authority.

Claim: freeze one actual public KnowledgeHistoryReplay and its corresponding
public KnowledgeChangeContext into immutable, graph-free inputs. The smallest
counterexample is a changed graph, swapped receipt, protocol body or context
coordinate passing as the same accepted input. All must refuse before a value
is returned. The adapter performs no retention, admission, model invocation,
source capture or effect.

Reuse the Core context factory, replay receipt, protocol replay identity,
canonical graph export, exact retained inputs and immutable ContractView.
Compare every context coordinate with the supplied replay. Verify the receipt
digest and its ledger, contract and graph coordinates. Reconstruct only a
disposable validation graph from the exported records and compare its complete
state digest. Bind protocol bytes through the receipt's protocol replay
identity. Verify every retained input's identity and exact agreement between
the context and replay, including role and media type. Never accept a caller's
new digest as a substitute for these existing references.

Input authority comes from the caller obtaining the replay and context from
the owning Core history. This adapter checks consistency, not authenticity of
arbitrary Python objects. It does not authenticate actors, sandbox Python,
protect against a caller forging the entire history/context pair, or replace
the owning append boundary's fresh-head check. A later ledger advance is
detected when a fresh context is compared or the proposal is submitted, not by
this frozen value autonomously reading the filesystem.

The output retains the existing immutable context and contract reader plus
canonical receipt, graph-record and protocol bytes. Decoded accessors return
defensive copies. No writer, graph, replay object, path or callback is retained.
The output has no new public identity: its receipt identity is Core's existing
receipt identity. Different valid history heads can have the same graph.

Local typed refusals are MALFORMED_INPUT for missing/wrong kinds or invalid
retained data, and STALE_BASE for inconsistent accepted coordinates or contents.
Missing action attachment refuses; it is not an empty satisfied lifecycle.
No default protocol state, source or quantity is supplied.

Conformance covers real Core replay, every context coordinate, mutable graph
tampering, receipt and protocol swaps, retained-byte/role tampering, missing
attachment, immutable and defensive outputs, deterministic freezing, and
unchanged ledger bytes. The test reuses the existing historical Shop run only
to exercise this read adapter. That run includes historical e7 and is explicitly
not the supplier effect E2E or its initial-source setup.

This boundary does not interpret the goal, authorize a candidate, establish
episode closure or prove source agreement. Those are subsequent Re-entry
contract and lifecycle checks. Replacement remains unproved until a different
implementation satisfies the same suite. No new extension mechanism is added.

Dependency tuples: ReadAdapter implements AcceptedReadBoundary; ReadAdapter
consumes KnowledgeHistoryReplay and KnowledgeChangeContext; ReadAdapter
produces graph-free immutable inputs; ReentrySynthesizer consumes those inputs;
all are governed by the selected history/action profiles. Existing Core receipt
and retained-input identities bind the derivation.

Pre-action checks: no server, endpoint, dependency installation, production
replacement, Core modification or external effect. Tests precede the adapter.

## Accepted lineage for episode closure

The pure consumer also needs to distinguish accepted changes from retained candidate
bytes. Extend this same local view with two required immutable tuples:
`accepted_change_sets`, containing Core's existing KnowledgeChangeSet values in replay
order, and `record_history`, containing sorted record-ID/KnowledgeRecordHistory pairs.
No new public type or change identity is introduced, and no graph/replay/writer is
retained. These are trusted Core-factory reads, not independently authenticated proofs.

Before returning, verify canonical KCS identity/value consistency and unique change
IDs; bind the last accepted KCS to the receipt using the actual history binding;
check every history entry against its accepted KCS operation and valid time; require
reciprocal supersession links and intervals; and match active history IDs to graph
exports. All required lineage must agree, or freezing refuses with STALE_BASE.
The consumer cannot populate accepted changes by scanning retained input bytes.

Tests cover immutable exact lineage, dropped/reordered/duplicated accepted changes,
missing or altered history and broken supersession. A real newly composed KCS retained
only as evidence must not enter the accepted tuple or active graph. Existing no-I/O,
defensive-copy and complete-coordinate tests still apply. Goal satisfaction and the
observation-to-accepted-KCS relationship remain separate consumer checks.

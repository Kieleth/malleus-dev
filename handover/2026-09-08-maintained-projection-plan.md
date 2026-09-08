# Maintained ledger-fed graph: activated contract

Luis approved this Core slice after the Shop shipment-policy proof. It is a
`REFERENCE_IMPLEMENTATION` within the optional semantic-history profile, not
a new protocol, knowledge identity, storage format or acceptance policy.

Claim: an in-memory reader advances from complete, verified committed suffixes
and returns the same graph, retained provenance, temporal record history,
contract revisions and action-protocol state as full replay. Full replay is
the recovery path and comparison oracle. The smallest falsifier is one unequal
receipt or history field after the existing supplier correction episode.

Reuse the existing history fold, graph validation, hash-linked JSONL reader and
supplier Re-entry walkthrough. Add a public `KnowledgeHistoryProjection.open`
reader with `refresh` and `current`; both reads require an exact expected full
head and count. `current` never refreshes silently. A stale view refuses.
Returned graphs are disposable copies, not accepted-state writers.

Keep continuation state private and in memory. It includes the active contract,
retained inputs, proposals, accepted changes, temporal history, machine and
action-program fold, historical graphs and verified envelope cursor. Publish
continuation and cursor together only after the entire suffix succeeds.
Incomplete knowledge admission or action transaction, changed prefix, malformed
suffix, duplicate IDs or wrong expected coordinates leave the prior view intact.

TDD sequence:

1. Commit RED for supplier full/incremental parity, protocol-only advancement,
   defensive reads, stale and corrupt suffix atomicity, and work counters.
2. Extract one resumable semantic fold used by both paths. Apply only new graph
   records and retire explicitly superseded records, retaining existing checks.
3. Exercise additive contract revision and partial shipments, plus the existing
   history, KG and protocol suites. Record exact results and limitations.

Work boundary: suffix events alone are decoded and semantically folded after
opening. Ordinary changes do not recreate unaffected graph records. Because
JSONL commits replace the file, refresh still hashes the retained prefix to
detect replacement or truncation. Graph copies, canonical digests, index copies
and receipt snapshots may still scale with history/state size. Contract revision
deliberately revalidates the whole graph. This is not constant-time I/O or
admission, a persistence benchmark, or a disk checkpoint implementation.

Excluded: database, service loop, multi-writer support, authenticated witnesses,
new persisted projection closure, external effects, new Re-entry scenario,
Assent cutover, dependency/package experiments, release and remote push.

Dependency view for the existing Core runtime workstream:

| Subject | Relation | Object |
|---|---|---|
| Maintained reader | implements | Semantic-history read projection |
| Maintained reader | consumes | Verified JSONL prefix and committed suffix |
| Maintained reader | governedBy | Retained contract, machine, policy and history binding |
| Maintained reader | produces | Existing KnowledgeHistoryReplay and receipt |
| Replay output | derivedFrom | One authoritative knowledge history |
| Reference implementation | conformsTo | Maintained-reader, supplier and shipment conformance tests |

The source commit identifies this reader implementation. No separately
versioned projector wire or CompleteProjectionClosure artifact is introduced.
Replacing the implementation would require the same conformance observations;
no second implementation or cross-language replacement is claimed here.

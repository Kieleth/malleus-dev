# Default source-input constructors

Luis approved this bounded Core cleanup after the fresh supplier-file proof.

## Contract before implementation

Role: REFERENCE_IMPLEMENTATION of the existing OPTIONAL_PROFILE selected by
`STRUCTURAL_HISTORY_BUNDLE`. No base protocol invariant or custom binding changes.
The CLI and two Shop runners are concrete consumers of duplicated construction.

Claim: public `structural_source_anchors` and `structural_evidence_anchor` build
the existing immutable `KnowledgeAnchorInput` values from exact bytes, explicit
record IDs and media type. The source constructor returns the ordered artifact
and source pair; the evidence constructor returns one evidence anchor. Neither
reads a file, receives history, appends, admits, invents an ID, or interprets a
source. Existing `append_anchors` owns validation and atomic persistence.

Input errors use `KnowledgeChangeRefusal(MALFORMED_HISTORY)`: content must be
exact bytes and IDs/media type must be nonempty strings. Empty byte content is
valid. Duplicate or conflicting history identities remain the ledger's check.
The constructors use the shipped bundle's existing event vocabulary only;
custom bindings continue to use `KnowledgeAnchorInput` directly. No new wire,
profile or capability-negotiation mechanism is introduced.

Smallest observation: exact equality with independently authored current event
bytes, no-I/O construction, changed content changes its digest, batch refusal
preserves history bytes, and complete Shop replay reproduces frozen evidence.
Reuse: canonical JSON/digest functions, KnowledgeAnchorInput, the installed
machine and binding, append_anchors, the existing CLI and Shop tests.

Dependency projection:

```text
DefaultSourceInputConstructors implements DefaultStructuralInputConstruction
DefaultSourceInputConstructors consumes ExactBytesAndExplicitRecordIDs
DefaultSourceInputConstructors produces KnowledgeAnchorInput
DefaultSourceInputConstructors governedBy STRUCTURAL_HISTORY_BUNDLE
CompilerCLI consumes KnowledgeAnchorInput
DefaultShop consumes KnowledgeAnchorInput
FreshShopImport consumes KnowledgeAnchorInput
KnowledgeChangeHistory.append_anchors consumes KnowledgeAnchorInput
DefaultSourceInputConstructors conformsTo SourceInputConstructorTests
```

Replaceability is not claimed. Byte parity is a regression check, not evidence
of a different conforming engine. Mapping, source observation, normalization,
domain correction, runtime policy, arbitrary binding generation, dependency
updates, package/version changes, release and publication are excluded.

The same slice clarifies an already author-endorsed distinction in Core's
principles: structural validity, source faithfulness and use-specific sufficiency
need separate support. Replay proves reconstruction; it does not prove the
other two or world truth. No evaluation API or mandatory coverage policy is added.

## Execution evidence

Pending RED, GREEN and integration checks. The shared paper/research worktree
is excluded; work runs in an isolated local clone of `63a05659`.

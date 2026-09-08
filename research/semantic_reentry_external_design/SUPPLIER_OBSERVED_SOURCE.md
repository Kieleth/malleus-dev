# Observed supplier source to existing KCS

REFERENCE_IMPLEMENTATION under the compiler-enabled state-version and experimental
one-action profiles. The bounded source mapping and evidence policy are the approved
ADOPTER_CHOICE. Tests are CONFORMANCE_FIXTURE, not a new public protocol contract.

Claim: exact independently captured supplier bytes can prepare one existing KCS
through ordinary population compilation. Only separate admission replaces e4 with
reentry-amendment-1. A FAILED receipt remains FAILED even when supporting observed
bytes justify that replacement. This establishes observed source meaning, not cause.

`prepare_observed_supplier_change` takes only required keyword inputs: owning Core
history and expected full head/count; immutable original-context, observation and
outcome-contract IDs; exact expected observer implementation identity; canonical
operator bytes; fresh population source/artifact, binding-evidence and plan IDs;
selected history profile; actor and transaction time. It returns the existing
PopulationPreparation, or None for a verified unchanged capture. None does not mean
the goal is satisfied. No source path, captured-byte override, oracle or receipt
payload is accepted as a mapping input.

Before retention, resolve applied observation, execution, dispatch and action,
their exact hashes, original proposal-context association, selected outcome contract
and retained observer implementation. Recover actual captured bytes from that
observation's SourceArtifact. Its logical locator and execution/contract provenance
must agree with the action. The original context supplies the retained goal, mapping
and pre-state bytes. Require the unique current target to match that pre-state and
its accepted source trace, without requiring today's whole domain to equal the old
proposal domain. Legitimate unrelated accepted progress is not silently undone.

Invoke the existing pure map_observation on those bytes and the explicit operator.
The operator must agree with the accepted action. INDETERMINATE refuses. Unchanged
bytes with CONTRADICTED yield None without retention. The research-v2 mapper
supports actual quantity 2 with CONFIRMED and actual quantity 3 with CONTRADICTED.
Both can prepare the observed replacement; only 2 meets the exact-two goal.
The observation result is checked separately from mapping support, and an
inconsistent verdict refuses. Unsupported quantities or source fields
remain evidence, not invented facts. Execution SUCCEEDED is never a prerequisite.

Population requires RETAINED_SOURCE while protocol capture is SOURCE_ARTIFACT.
Use public structural_source_anchors to register a distinct source/artifact pair
containing exactly the captured bytes. Do not relabel the original retained input.
Retain a canonical local binding document as ordinary RETAINED_EVIDENCE. Its grammar
is malleus.reentry.observed-source-binding/research-v1, with exact original-context,
observation, outcome-contract and captured-source references; population source and
artifact IDs; the original goal/mapping references; and the declared operator.
Record hashes, raw byte digests and source IDs remain distinct.

The existing population plan names that source, binding evidence and the exact
two-file mapper/coordinator implementation identity. It preserves all four mapped
fields, the declared new occurrence, ORDER_ONLY time and explicit supersession.
Compile and prepare using the actual fresh replay after retention. No graph writer,
private Core import, substitute KCS or canned assessment participates. The adapter
does not import an executor or observer implementation. It consumes their artifacts.

Return before admission. The caller invokes the normal admission gate, whose stale
base guard remains authoritative. Individual Core appends are atomic; the retention,
compilation and preparation workflow is not one transaction. Static invalid input
refuses before retention. A later compilation/storage failure can leave retained
evidence, never an accepted replacement. No automatic retry or episode closure is
introduced by this stage.

Conformance: actual successful and failed-after-write captures prepare the replacement;
unchanged capture emits no KCS or writes; stale inputs, wrong observation/contract/
implementation/operator and reused source IDs refuse; preparation preserves the
entire domain frame; stale admission refuses; only admission changes the target;
all other records and temporal history survive; JSONL-only reopen traces the new fact
through population binding evidence to the exact applied observation and bytes.
Pure mapping, executor and observer must not run during admission or replay.

Dependencies: observation closure supplies captured source and original mapping;
pure mapper supplies population fields; public retention supplies ordinary source
and binding evidence; public compiler/preparation produces KnowledgeChangeSet;
Core admission alone changes the accepted domain; Core trace/replay recovers lineage.

Excluded: new Core objects, source authenticity, causality, demand fulfilment,
effect dispatch, full synthesis contract, episode satisfaction, empirical replacement,
full E2E claims, server calls, installations and Core/ontology/locked-fixture/paper edits.

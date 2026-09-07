# Check producers and invocation/output contracts

Status: proposed content contract for review. Both implementations are UNBOUND.
No callable in this document is exported or implemented. The research checks
exercise declarations and lexical content, never a producer or an assessment.

## Ownership and signatures

The proposed Core-owned pure producer signatures are:

```text
type_check(*, invocation, verified_inputs, record_contract) -> MonitorOutput
direct_grant_check(*, invocation, verified_inputs, record_contract) -> MonitorOutput
```

An adopter selects legitimate policies and grants and supplies exact typed
inputs and the equality-scope association. Core defines the finite structural
and direct-grant predicates; the producer implementation ownership and exact
bytes require review before either signature becomes executable. A producer
gets no history writer, graph writer, clock, source store or effect adapter.
No producer may append its own assessment or choose final control. The owning
history validates outputs and recomputes policy control separately.

The proposed persistence successor consumes explicit expected full head/count,
ordered event bodies and retained input bytes. It stages and commits once.
This packet selects no new public callable name for that operation.

`invocation.schema.json` closes the proposed explicit invocation envelope.
`monitor-contract.json` binds ordered input roles and output identities. Reference
shapes are not input contents: `verified_inputs` must contain the actual retained
full typed record wrappers or exact artifact bytes, verified against each role's
reference. Interval, equality-scope and current-context contents use the contracts
in this packet; O uses the previously frozen original-context schema. A digest
with no resolved bytes or record is not an executable input.

`retained-input-origins.json` now records those origins as definition data.
All monitor records and byte carriers must be applied before invocation; only
the context/proposal transaction itself may resolve its newly staged context.
A retained current-context artifact refers to its real prior prefix, not to
the later prefix produced by retaining it. Runtime must verify that prefix and
independently compare current action/domain coordinates. No history resolver
or concrete producer is supplied by the table.

## Three orders that must not be conflated

1. Invocation inputs follow the exact semantic-role sequence in
   `monitor-contract.json`. TYPE has proposal/action/record-contract. DIRECT_GRANT
   has the nine declared roles, with executor_id an explicit scalar.
2. MonitorSpecificationArtifact.input_artifact_ids names only static retained
   ProtocolArtifact dependencies and is canonical unique order, with matching
   input_artifact_record_hashes. Dynamic proposal/action records and a literal
   executor ID cannot be inserted in that artifact list. Monitor specs and
   policies precede proposals; no circular future-proposal hash is introduced.
3. Assessment.input_record_ids contains the unique actual retained record IDs
   consumed for that invocation, including proposal and required dependencies.
   Exact order is declared in the selected producer contract. A scalar executor
   ID is bound by the typed invocation and assessed action/actor fields, not
   disguised as a ProtocolArtifact ID.

The actual static dependency set, producer-input retained artifact wrapper and
concrete record IDs must be instantiated and reviewed with the real producers.
The present envelope does not instantiate them. This is a remaining executable
binding obligation, not a claimed completed monitor package.

The carrier choice is now accepted in `INPUT_BINDING_DECISION.md` and
`input-bindings.json`: SourceArtifact describes exact bytes for the five
declared byte-input roles. It does not define those bytes' role or validity.
Record references retain record hashes; byte references name the carrier ID
and raw-byte digest. Neither aliases the source artifact's semantic hash.
There is no lookup fallback to the predecessor candidate table.

The research `input_preflight.validate_input_specimen` checks the supplied
ordered role inputs against full concrete record wrappers, compiled record
shapes, recomputed record/source hashes, exact bytes and the existing content
parsers. TYPE's supplied compiled-contract payload must equal the selected
validation-contract bytes. Original-context contents must be that specific
variant, not an initialization object. JSON role contents are canonical; the
preflight does not normalize bytes or fetch a source locator.

The binding declares `required_collections`, not presence-only fields. Every
such field must contain a list: empty is structurally valid, null is not.
Record canonicalization errors become INPUT_RECORD_SHAPE refusals with the
lower-layer cause retained. See `INPUT_PREFLIGHT_CORRECTION.md` for the
consumer-discovered defects, retained RED cases and corrected evidence.

This is a specimen consistency check, not history resolution. It checks only
the invocation's role inputs; monitor and implementation references receive
envelope shape checking only. Event metadata and policy/context associations
still need the event programs. The result explicitly scopes itself to
INVOCATION_ROLE_INPUTS, says retention_verified is false, and says
runtime_executed is false. Supplying a complete specimen cannot establish that
records were applied, dependencies were complete, state is current, or a
producer ran. Raw context IDs are not silently equated to carrier record IDs.

## Fields and hash domains

`monitor-output-fields.json` is the research field census for six selected
record variants: completed TYPE/authority assessments, their failure records,
and their unavailable assessments. Groups remove repeated field descriptions;
each path names a field origin, not an executable operation or a new wire.
The test-only constructor materializes lexical specimens and validates them
against compiled Assent. It does not resolve records or run a checker.

The `closure` origins deliberately remain unbound. They require the exact
resolved input and provenance record sequences, not lists guessed from IDs.
They differ per output: an unavailable assessment cites its failure record,
while that failure cannot cite itself. The `computed` origins likewise require
actual producer results. Test witnesses are neither verified inputs nor check
evidence. The census cannot make the check package executable.

These are minimal selected variants, not all optional Assent field combinations.
Logical fields are absent. The direct-grant variants carry the exact evaluated
grant; an absent-grant variant is not silently substituted. Completed outputs
omit `monitor_failure_id`; unavailable outputs bind it to the paired failure.
The failed check's error code supplies the unavailable reason code. Failure
classification and message originate in actual check execution, never ambient
caller metadata. The final record hash includes all selected fields and omits
only itself, using the existing Assent record-hash operation.

Every output uses the full existing Assent record type and validates under its
exact compiled contract. Metadata comes from explicit invocation input:

| Output field | Derivation |
| :--- | :--- |
| id | output_ids.assessment, or output_ids.failure for MonitorFailure; distinct unused IDs |
| generation_event_id | invocation.event.id |
| generated_at | invocation.event.generated_at, same as enclosing transaction time |
| responsible_actor_id / responsible_role | invocation.event fields, validated against the event's permitted role |
| proposal_id / proposal_content_hash | exact applied proposal id/content_hash |
| base_acceptance_head | proposal A for TYPE; current post-ACCEPT A for authority |
| monitor_id / monitor_hash | exact MonitorSpecificationArtifact id/content_hash |
| monitor_version | that monitor's artifact_version, never implementation.version |
| assessment_kind | TYPE or AUTHORITY, agreeing with concrete assessment type and monitor |
| input_record_ids / source_record_ids | exact role-bound retained dependencies and required provenance, unique and resolved |
| content_hash | existing record_hash with exact record type and every field except content_hash |

Authority outputs additionally derive action_proposal_id/action_content_hash,
evaluated_actor_id, authority_policy_id/hash and evaluated_authority_grant_id/hash
from their exact inputs. The referenced grant must be the grant actually
evaluated, including in a VIOLATED/BLOCK path. A failed check may not silently
switch to a different grant.

The monitor record's monitor_implementation_hash must match actual reviewed
producer bytes. A check-contract or specification digest cannot stand in for
those bytes. A lexical digest can pass an invocation shape test but does not
establish implementation identity or readiness. No implementation placeholder
is upgraded to a runnable instance by this packet.

## Computed outcomes and unavailable outputs

TYPE computes exact record conformance for the proposal/action against the
retained compiled contract and finite subset. Success is SATISFIED; a known
structural violation is VIOLATED with computed reasons. Unavailability is not a
structural violation. It yields MonitorFailure plus UnavailableAssessment,
both with the same invocation context and one atomic failure event.

DIRECT_GRANT computes grantee/executor match, action-type membership, exact
scope equality, may_subdelegate false and interval containment. It emits the
existing AuthorityAssessment with checked and violated predicate lists. It
does not establish grantor legitimacy or a scope hierarchy. Unavailability
yields MonitorFailure plus UnavailableAuthorityAssessment in one atomic event.

Computed outcomes, reasons, rationale and checked/violated predicates cannot be
supplied as invocation inputs. Failure metadata uses the existing failure
category/error-code vocabulary and explicit paired IDs; no silent clock or ID
allocator supplies them. Both records bind identical proposal/action/policy/
monitor/A context, and the unavailable assessment points to the paired failure.
UNKNOWN cannot be fabricated by omitting a required producer output.

The declared TYPE policy selects REJECT for VIOLATED, DEFER for UNKNOWN, with
REJECT precedence; all satisfied selects ACCEPT. Authority keeps the existing
all-satisfied AUTHORIZE, any-violated BLOCK, otherwise CLARIFY rule. The policy
evaluator, not the producer or caller, supplies the final verdict and evaluation
hash. Exact policy, monitor and ruleset records remain to be instantiated.

## Execution gate

Required before a positive executable claim: actual producer byte identities,
retained full input wrappers/static dependencies, explicit invocation metadata,
computed output records, conformance including paired failures, and replay
validation through the reviewed event programs. These are UNEXECUTED obligations.
The current test counts cover only static/content definitions and the actual
Assent multi-valued grant declaration. They cannot justify dispatch eligibility.

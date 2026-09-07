# One-history action contract definition

Status: definition for independent review, not an executable profile or a new
public wire. The operator approved this finite definition after the semantic
design and compiler compatibility gate. Runtime implementation, source effects,
observer execution, shared-main changes, merge and push remain excluded.

Role: OPTIONAL_PROFILE, with a research-local CONFORMANCE_FIXTURE. The bounded
one-consumer exception applies only to the already selected supplier proof.
The default structural history, standalone Assent and existing KCS identity
retain their current meanings. The source design and supplier fixture remain
owned by Semantic Re-entry, at `f221c0994df530170c80726be29ff876d3dd195e`.

## Contract before construction

Claim: define inspectable, closed initialization and original-context shapes,
their identity recipes, finite typed execution obligations and exact producer
binding requirements without hiding an implementation in a string or callback.

Smallest observation: the schema accepts complete shape witnesses, rejects
missing/extra/mistyped fields, and has no self-hash cycle. The finite instruction
grammar rejects unknown opcodes and operands. Every required operation has
explicit inputs, outputs, refusal semantics and side-effect boundaries. The
current interpreter must still refuse the proposed grammar.

Reuse: compiled complete Assent, existing record/event hash recipes, existing
acceptance-result-head formula, retained KCS context and atomic staging. No new
domain-change identity, ledger or graph is introduced.

Excluded: executable monitor instances without real producer bytes, policy
legitimacy, generic expression language, automatic monitor invocation, action
runtime, supplier subtype implementation, migration and portability claims.

## Coordinates and identity

`contexts.schema.json` closes two candidate artifacts. It is a shape contract;
stateful prefix/reference validation is an execution obligation, not a JSON
Schema guarantee. Neither artifact carries its own digest. Its identity is
`sha256:` plus SHA-256 of UTF-8 canonical JSON, using the existing
`malleus.ledger.canonical_json` recipe. Object-key order does not matter; array
order and every value do. No field is excluded from these two identities.

Full log position consists of `head` and `event_count`. Domain context consists
of the effective contract, KCS acceptance head, materialization head and graph
digest. Action acceptance has its own digest. Equal string types do not make
these coordinates interchangeable.

Initialization pins an actually verified prefix and domain state plus exact
profile, record contract, machine, binding and policy references. The initial
action-acceptance head is the initialization artifact's content identity. It
becomes active only through the new profile's validated initialization event,
once per history. Constructing the artifact alone changes nothing. Existing
domain state and KCS heads remain untouched. An absent producer/program prevents
an executable initialization instance; it does not acquire a placeholder hash.

The original proposal context pins a verified full prefix, its domain context,
current action-acceptance head, initialization identity, exact proposal/action
IDs and stable episode key, policies, goal, preservation, mapping and pre-state
source. It contains IDs, not hashes of the not-yet-introduced proposal/action.
The later event binds this context identity to those exact record hashes. This
avoids a context/action self-reference cycle without dropping the association.

Proposed ordering for review: retain every required input first; capture the
original context at that verified prefix; register that context; record the
proposal immediately next. The registration must be the sole intervening
event. The proposal checks that the original domain and action-acceptance
coordinates remain current. This specifies the formerly unnamed designated
prefix rule and does not permit arbitrary log movement or silent rebasing.
This ordering is a newly explicit detail of the definition, not a runtime
behavior already accepted or implemented.

Action-only ACCEPT computes the next action head with the existing
`acceptance_result_head`, previous action head, proposal/decision record hashes,
and an empty revision-hash list. Never pass a KCS acceptance head in its place.
Authority and dispatch require current action and domain context. Execution
and observation may describe an applied dispatch after domain movement; they
cannot authorize another effect or update the KG. A resulting KCS uses a fresh
verified context after actual evidence retention.

## Finite execution vocabulary

`instructions.schema.json` defines typed declarations for this proposed cut.
`capabilities.schema.json` defines the separate TYPE and direct-grant producer
binding shapes. These are research definitions, not accepted program grammars.
Operands are explicit paths from the enclosing event, an applied record,
original context, verified current state, an identified artifact or a prior
instruction result. Paths are nonempty ordered field/index components.
Unknown roots, missing values, invalid paths and forward/local cycles refuse;
there is no ambient lookup, expression evaluation or callable import.

The program is a finite ordered list, with no recursion, jumps, loops or
user-supplied code. An array operand is consumed only by the named finite-list
operation, not by a general loop. Every output is single-assignment. Required
capabilities and their exact implementation identities must resolve before any
event runs. Unsupported capability is a refusal, not a fallback to Assent's
Python event handlers.

| Instruction | Required semantics |
| :--- | :--- |
| VALIDATE_RECORD | Validate the entire typed record against its exact retained compiled contract, including inherited/nested fields and absence/null distinctions. Return the same immutable record or refuse. |
| HASH | Use exactly the selected existing VALUE, RECORD or ARTIFACT recipe. RECORD excludes only content_hash; ARTIFACT uses the exact named artifact contract. Unknown recipes refuse. |
| RESOLVE_RECORD | Resolve ID, exact type/subtype and record hash in applied prefix or explicitly declared earlier same-batch introductions. Missing or ambiguous references refuse. |
| REQUIRE_COMPARE | Compare typed operands with EQ, NE, LT or LE. No coercion. Time operands require timezone-aware instants and compare actual instants; unbounded interval ends are handled only by the interval instruction. |
| REQUIRE_UNIQUE | Require unique keys in the declared finite record list and absence from the named replay index when supplied. Composite keys are ordered tuples, not concatenated strings. |
| REQUIRE_COVERAGE | Match the exact required monitor ID/hash pairs to one output each, including proposal, action, actor, policy and acceptance context. Missing, extra, duplicate or mismatched outputs refuse. |
| REQUIRE_INTERVAL | Verify a declared inner interval lies within the outer interval. Starts are included, ends excluded; an absent outer end is unbounded, an absent inner end needs an unbounded outer end. No timezone inference. |
| SELECT_CONTROL | Apply the identified policy's explicit outcome map and precedence to its complete validated check set. Recompute the existing evaluation hash. No outcome or verdict may be supplied as a shortcut. |
| INTRODUCE_RECORDS | Stage the finite validated record list and its declared dependencies, enforcing global ID/hash/provenance consistency. Publish nothing until the owning atomic batch commits. |
| SET_PROTOCOL_STATE | Stage only declared protocol indexes or the action-acceptance head. Domain graph, contract, KCS list and KCS heads are forbidden targets. |

VALUE hashing reuses `content_digest`; RECORD reuses `record_hash`. ARTIFACT is
not a universal hash shortcut: its exact retained contract must identify the
existing schema-specific semantic-hash projection. Event-envelope hashing
remains the ledger owner's job and is not an instruction.

These declarations define required capabilities, not implementations. Detailed
event-to-instruction programs and their static operand resolution remain a
reviewed successor artifact. The schema alone is not a complete portable
interpreter or a substitute for event semantics in the accepted source design.

## Check-producer binding, not fabricated assessments

TYPE consumes exact proposal/action records and the retained compiled record
contract. A real producer must compute the existing TypeAssessment from those
inputs. This establishes structure, not source truth, usefulness or authority.
Known violations yield VIOLATED; producer unavailability yields the existing
paired failure/unavailable records. The proposed policy maps VIOLATED to REJECT
and UNKNOWN to DEFER, with REJECT taking precedence.

The direct-grant producer consumes exact proposal/action, intended executor,
grant, scope association, requested interval, authorization policy and current
action/domain contexts. It computes exact actor/action-type/scope equality,
no-subdelegation and interval-containment predicates. It uses the existing
AuthorityAssessment, or paired unavailable records. All SATISFIED selects
AUTHORIZE; any VIOLATED selects BLOCK; otherwise UNKNOWN selects CLARIFY.
Missing checks are not UNKNOWN results and do not permit a decision.

Both require a MonitorSpecificationArtifact binding actual implementation
bytes, version and ordered input artifact IDs/record hashes. The specialist
confirmed that neither new producer exists. Their implementation hashes and
valid monitor/policy instances remain UNBOUND. Specification digests identify
these requirements, never the absent implementations. Ruleset references must
also resolve to real typed retained artifacts. No empty ID satisfies that gate.

The proposed binding shape separates the check contract from the implementation
ID, version and byte digest, and closes the input roles for each producer.
It does not contain a caller-selected outcome or an import/callback. A null,
UNBOUND or specification-only implementation cannot instantiate that shape.
Schema validation alone cannot prove that digest-named implementation bytes
exist or execute the declared checks. Those are still runtime conformance
obligations. Shape tests use labeled synthetic witnesses, never live monitors.

## Review and completion boundary

This packet is a finite definition candidate, not a completed executable
contract freeze. The designated-prefix ordering above and the exact instruction
vocabulary need independent review against the already approved semantics.
Still required before runtime RED: concrete event programs/static operand
closure, actual producer and interpreter identities, instantiated initialization
and original context over a real verified prefix, and positive/negative
lifecycle fixtures. These are explicit missing artifacts, not successful gates.

Definition consumes ApprovedOneHistorySemantics
Definition consumes VerifiedCompiledAssent
Definition produces ClosedContextShapes
Definition produces FiniteInstructionShapes
Definition requires ActualCheckProducerBindings
FutureProtocolAppend conformsTo ReviewedDefinitionAndLifecycleFixtures

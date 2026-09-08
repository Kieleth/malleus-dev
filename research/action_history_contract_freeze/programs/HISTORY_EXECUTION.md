# Owning-history execution cut

This is a chronological execution journal. Statements about unfinished stages
below describe their recorded boundary, not the latest implementation. Read
[`../EXECUTABLE_HANDOFF.md`](../EXECUTABLE_HANDOFF.md) for current scope and the
final verification section for the latest tested coordinate.

This private implementation step serves the approved executable action
milestone. It is not the complete action profile or a consumer handoff.

Claim: an explicitly selected, retained finite program set can execute a
declared logical-event transaction inside the existing KnowledgeChangeHistory.
The existing JSONL append gate validates the full candidate prefix before it
writes. Replay reads that same prefix, never a filtered second history.

Observation: a two-event neutral registration succeeds together, a bad second
event leaves exact prior bytes unchanged, and reopening recovers its introduced
records and protocol indexes. KCS composition after it uses the actual full
head/count. Protocol execution cannot change the graph or KCS heads.

Reuse: the existing finite validator/interpreter, compiled record contract,
JsonlLedger append_many, KnowledgeChangeHistory replay and retained evidence.
The generic pure implementation moves to private Core modules; research keeps
thin imports and fixture loaders, never a second interpreter or fallback.

## Explicit data boundary

`malleus.finite-protocol-bundle/private-v0` binds exact compiled record-contract
bytes, instruction schema, index/capability profile, constants and named
transactions. Each transaction declares its ordered logical event types and
one finite program. An explicit selection event names an already retained
evidence artifact and its digest. A history selects once; replacement requires
a future migration decision. Selection is not an authority grant.

The interpreter admits only its exact installed instruction grammar. The bundle
retains that grammar for inspection and identity, not as permission to redefine
operators, lookup scopes or unknown fields. A permissive caller-supplied schema
refuses before selection or execution. Supporting another grammar requires an
explicit interpreter capability, not a schema-validation bypass.

`append_protocol_events` accepts a transaction name, exact expected full
head/count and a nonempty ordered tuple of event drafts. Each draft carries
event ID/type, actor, transaction time, data and named raw retention inputs.
Each retention input name is a program-local role, not the retained record ID.
Its explicit `record_id` names the introduced record. This lets the same
identified source-registration program bind different source IDs without
changing program paths or treating a role name as a global identifier.
The envelope records the selected bundle identity, transaction identity and
zero-based ordinal. The complete selected sequence is required. No partial
transaction may survive append or replay, including a transaction split by an
ordinary KCS or evidence event.

The fixed interpreter input frame is:

- `event.<zero-based ordinal>`: owner-verified header, caller data and verified
  retention metadata/content. Programs declare closed schemas for these frames.
- `current.context.value`: actual pre-transaction full head/count, domain
  contract, KCS acceptance/materialization heads, graph digest and action head.
- `artifact.constants.value`: exact constants from the selected bundle.
- `artifact.selection.value`, when explicitly declared: owner-derived bundle,
  compiled record-contract, instruction grammar, profile and history-binding
  identities. Initialization can bind the real selected definitions without
  embedding the bundle's own hash inside itself. No caller supplies this frame.
- `current.state.value`, when explicitly declared: a copy of the actual prior
  protocol fold state. The program declares its closed shape. It is read input,
  not another state authority or a way to supply replacement state. The existing
  finite effects remain the only route to stage protocol-index changes.

There are no caller-supplied applied records or trusted current-state objects.
RESOLVE_RECORD uses only prior protocol introductions. Introductions cannot
reuse any retained, machine, domain-history or protocol record ID. Raw bytes
retained by a transaction must bind a record introduced by that transaction;
the selected finite program enforces its record/byte/role semantics. The owner
computes the byte digest and length. No code is loaded from retained data.

Replay produces protocol state beside, not inside, the domain KG. Its identity
is included in the receipt only when the optional program set is selected.
Unselected histories preserve the previous receipt shape and bytes. Existing
KCS admission and standalone Assent retain their contracts.

## Exclusions and dependencies

This step does not make the neutral test transaction an action lifecycle. It
does not authenticate a grantor, perform an effect, invoke checks during replay,
or prove that an arbitrary selected program is the accepted action profile.
The complete identified action programs and real producer/output binding still
have to cross this gate. No main integration, stable wire, public promotion,
multiwriter guarantee, new ledger, arbitrary callback or profile fallback.

The bounded registration authoring module now binds the existing source,
grant, monitor and policy instruction definitions to that owner frame. A
retained RULE_SET uses the existing ProtocolArtifact record, with its exact
byte digest. The owning ledger test registers actual producer implementation
and definition bytes, four monitor records and the two policies, then reopens
without invoking the authoring module. Six tests pass, including five
misbound-monitor refusals with exact byte preservation. This two-input,
two-monitor conformance variant does not claim every possible policy arity.
Registration establishes identity and shape, not legitimacy or check execution.

The initialization program now binds all four selected definition roles and
both applied policies to actual full-prefix/domain coordinates. It retains the
closed checkpoint through a SourceArtifact, derives the action head from its
content, and enforces one initialization. The first isolated run passes eight
tests, including seven atomic refusal cases. No action has been proposed by
this test. Initializing the action profile does not mutate accepted knowledge.

The interpreter reuses at most four immutable parsed record contracts keyed by
their complete bytes. It never caches state, record checks, decisions or
refusals. A hard test checks byte-key separation, failed-load revalidation and
view immutability. This is parsing reuse, not another persistence authority.

The follow-on integration fixture starts with the actual populated public
Shop run rather than an empty neutral graph. All nine initialization tests
pass. It retains five KCSs, one contract revision, the supplier e4/e7 lineage,
and the exact existing current records through initialization and JSONL-only
reopen. The source and record-contract identities remain separate from the
domain effective contract. This is initialization over the current Shop state,
not a supplier amendment, an effect, or a completed action lifecycle.

The regression command covering programs, owning transactions, retention,
selection and knowledge history passes 473 tests, with initialization tested
separately above. The optional owner-state input adds three passing tests for
actual prior-state reads, stale claims and forged claims. An initial test setup
mixed two fixture clocks; the corrected helper requires one exact transaction
time, leaving the ledger's monotonic-time guard unchanged.

Exact definition validation is also reused with a 32-entry bound. Profiling one
selected bundle found eight repeated static program checks, with schema
metavalidation accounting for most of its load. The key includes the complete
canonical program, profile and instruction schema. Changed definitions are
rechecked; failures are not cached. Runtime operands, state, records, producer
outputs and admission are still checked on every execution. The definition
reuse, owner-state, finite-executor and check-producer gate passes 76 tests.

## Remaining execution work

The actual context/proposal definition now crosses the owning gate as one
atomic pair. It retains the original context, introduces the complete concrete
LocalAction and ProposedSubgraph records, then sets PROPOSED/PENDING and their
associations. It reads the real initialization index, verifies the complete
retained checkpoint against that identity, resolves both selected policies and
all four retained context-source references. The source-registration recipe
checks byte, artifact and record identities separately. No caller-supplied
current state or applied records are trusted.

Thirteen tests pass, including twelve refusals with exact reason codes and
byte preservation: incomplete transaction, wrong member, stale full/domain/
action coordinates, wrong initialization, forged checkpoint, wrong source
record/bytes, wrong artifact semantic hash, wrong policy and reused action key.
The combined populated Shop initialization and proposal gate passes 22 tests.
The same 13-test proposal selector took 428.81 seconds before static-definition
reuse and 47.90 seconds after it. These are local observed runs, not a benchmark
or performance guarantee. The graph, KCSs and action head remain unchanged.

This proves the protocol transaction with the previously selected neutral
LocalAction specimen. It does not yet prove a concrete supplier amendment or
the complete shared consumer boundary. Next bind the real check outputs,
epistemic decision/transition, authority assessment,
authorization, dispatch, terminal execution receipt and separate observation.
The pure check/control tests do not replace those integration stages. Robotics
and Semantic Re-entry remain blocked on that complete shared handoff, not on
each other. This isolated work has not changed main or either consumer.

The owning-history regression gate now passes 499 tests, including all program,
initialization, proposal, source, selection, state and knowledge-history tests.
The next read-only orchestration step executes both selected TYPE monitors on
the actual replayed proposal and action, selected record-contract bytes and
retained producer definition/implementation. Six tests pass: real deterministic
outputs and five forged invocation/identity refusals. The helper accepts only
history and invocation, not a record map, compiled bytes or outcome. It returns
the prefix coordinates alongside the existing pure computation result and
writes nothing. These outputs are not yet admitted assessments or permission.

The next transaction now admits those actual TYPE outputs. Separate declared
programs handle completed assessments and an atomic MonitorFailure plus
UnavailableAssessment pair. They resolve the applied proposal, action, selected
policy and monitor, record-contract source, original context and exact static
input closure. They check full records, hashes, metadata, provenance, monitor
version, original domain coordinates and action head. One assessment per
proposal/monitor is enforced. No checker runs inside append or replay.

The ten assessment tests pass, including real producer success and controlled
unavailability, misbinding refusals, a bad second record that discards the
staged failure, and an intervening ledger event that makes the computed append
stale. The combined program/history gate passes 515 tests in 223.96 seconds.
The graph, record lineage, KCS list and action head remain unchanged. This is
the bounded one-open-proposal, two-static-input conformance variant. Retaining
check judgments does not authenticate the producer process or establish source
truth. Epistemic decision and permission still follow as separate stages.

The action-only epistemic decision now executes through that same history.
It resolves the real applied assessments and monitor specifications, binds the
selected policy/ruleset and original domain state, then invokes the existing
pure control capability. Supplied output snapshots must match complete applied
records. The decision's verdict, evaluation identity, ordered assessments and
trigger list must equal recomputation. The complete decision and transition
are introduced atomically. ACCEPT hashes the existing acceptance-result
preimage with no revisions and advances only the action head. No decision
variant can apply a KCS or grant permission.

Twelve focused tests pass in 72.59 seconds: actual successful TYPE producers
lead to ACCEPT; real engine unavailability leads to DEFER; nine binding/state
refusals plus the exact transition-time guard preserve prior bytes. The latter
first failed because instant equality admitted a differently written event
time; exact string equality now preserves the existing TransitionRecord
contract. The preceding broad gate passed 526 tests in 296.14 seconds before
that final time guard; the final focused rerun includes its correction. Ruff,
format and diff checks pass. REJECT and CONTEST effects are declared variants,
not claims that an actual TYPE producer reached them in this owning-history
fixture. The independent existing control tests retain their negative verdict
coverage. Authorization, dispatch and observation still await integration.

Current-context capture now verifies the actual pre-event full prefix, domain
coordinates, action head, initialization and both applied policies before
retaining the canonical content. Its verified index preserves the content
identity for later authority admission. It reuses source-registration checks;
ordinary source registration alone does not populate that verified index.
Eight tests pass in 75.61 seconds. Two execute the real DIRECT_GRANT producer
on applied grant/action/policy records and retained scope, interval and original
and current contexts. The exact executor computes SATISFIED; another grantee
computes VIOLATED with GRANTEE_MATCH. Computation changes no ledger bytes and
leaves permission PENDING. Five forged context variants refuse before retention.
The positive capture reopens with unchanged domain and action heads. These
checks establish shape/identity and the specified grant comparisons, not grant
legitimacy, authenticated actors, an effect, or an admitted authority judgment.

Arity clarification: the current finite program bundle is exercised with one
proposal in the history, not multiple closed proposals plus one open proposal.
Its closed state-read schemas intentionally refuse additional proposal entries.
General multi-action workflows remain outside this bounded first-lifecycle
conformance cut; no general concurrency or scheduling claim is made.

Authority assessment admission now resolves the applied ACCEPT, proposal,
action, selected policy/monitor, exact grant and retained input closure. Both
original and current contexts must match their retained SourceArtifact bytes;
the current context must additionally exist in the verified capture index.
Current A/D and pending authorization are rechecked at admission. Real
SATISFIED and VIOLATED outputs enter as judgments, not permission. A real
failure produces MonitorFailure plus UnavailableAuthorityAssessment together.

All 12 focused authority tests pass in 103.22 seconds, including bad second
record rollback, context/grant/actor/monitor/closure/duplicate refusals and an
ordinary-source bypass control. In that control a pure checker can compute on
retained context-shaped input, but admission refuses because it was not
captured against the owning prefix. Replay invokes no producer and preserves
KG, KCS heads and action head. The shared field-census authoring helper retains
the exact previous TYPE schema digest. No interpreter operation or domain
ontology was added. Authorization/control and the remaining effect-record
lifecycle are still pending; no consumer-unblock or main-integration claim.

Authorization now recomputes the existing policy from two actual applied
authority judgments. The accepted proposal, selected monitors, exact grant,
executor, verified context and current A/D must agree. AUTHORIZE checks the
grantee, permitted action type and validity interval inside the assessed
grant. BLOCK and CLARIFY retain explicit null validity. The full decision and
transition commit together and change only permission indexes, not A or D.

The initial missing-stage RED produced 12 setup errors. Corrected GREEN passes
13 focused tests in 146.84 seconds: actual grant outcomes reach all three
verdicts, nine adversarial branches assert their exact typed refusal and byte
preservation, and the shared authority read prefix is mechanically effect-free.
The authoring constants preserve the policy and decision as distinct objects;
the static checker caught their first accidental name collision. The last
completed preceding broad gate passed 547 tests in 469.64 seconds and does not
include authorization. Ruff, format and diff checks pass for this slice.
Dispatch, execution and observation remain unfinished. This local finite
conformance variant is still not a public consumer handoff or main integration.

Dispatch eligibility is now executable. It requires the actual applied
authorization index and full decision/action records, the authorized executor,
current A/D through verified retained context, and an unexpired interval. A
nonblank adopter-declared adapter ID is retained, not invoked or authenticated.
The one dispatch per action index is enforced before introduction. Nine
focused tests pass in 108.04 seconds after the nine missing-stage RED errors.
They cover actual permission, no domain/head change, JSONL-only reopen, absent
permission, wrong executor/head/context, exclusive expiry, blank adapter,
incomplete provenance and a second dispatch. The first test run caught a
fixture call to retained_bytes on the writer; the actual API is on replay.
No production API was changed to accommodate that fixture mistake. Execution
receipts and independent observations remain the next unimplemented stages.

Terminal receipt admission is now GREEN: 11 tests pass in 129.78 seconds after
11 missing-stage RED errors. SUCCEEDED, FAILED and ABORTED receipts reference
the actual applied dispatch, match its executor, and bind a strictly positive
execution interval after dispatch to the event time. Exact result bytes are
retained with the receipt in the same append. Invalid references, executor,
times, status, bytes, retention association or duplicate terminal receipt
refuse without a write. Reopen reproduces the state and retained bytes; no
observation index or graph change is implied. These are synthetic receipt
conformance cases, not evidence that a supplier or robot effect happened.

Independent observation and outcome-contract registration now pass 17 focused
tests. Contracts bind the exact observer implementation source and the existing
outcome-contract semantic hash. Two corrective REDs showed that blank contract
version/type strings bypassed the existing digest contract's nonblank rule;
the selected input schemas now enforce that rule without regex. Observation
requires an applied execution, exact contract and actual SourceArtifact,
matching observation type/time, a distinct nonblank observer, closed outcome
and a unique execution/contract pair. Receipt bytes cannot substitute for the
observed source. Backward enclosing time is refused by the owning ledger;
misbound observation time is separately refused by the finite program.

The two additional real-Shop composition tests pass. Starting with RET-010,
the existing contract revision, settlement facts and B/e4, the actual historic
e7 KCS invalidates earlier permission before dispatch. Conversely, after a
valid dispatch the same real domain correction does not prevent recording a
FAILED receipt and independent CONFIRMED observation. The failure stays
failed; neither status changes knowledge. All five KCSs, the revision and the
RET-010 complement survive. A fresh process reopens a directory containing
only JSONL, refuses research/test imports, and reproduces ledger, graph and
protocol identities. The correction is independent of the synthetic action,
not a claim that it caused e7 or performed a supplier effect.

The exact final observation-plus-Shop selector passes 19 tests in 316.16
seconds. The preceding regression selector passes 580 tests in 861.19 seconds,
through terminal receipts, excluding the then-unimplemented observation file
and before the new Shop composition file existed. These are separate runs,
not a claimed single combined 599-test gate. The selected declarations and
tests have Ruff/format/diff checks. The reference programs remain bounded to
one first-revision LocalAction, two TYPE/direct-grant monitors, one dispatch
and finite intervals. The provisional consumer surface and remaining limits
are described in `../EXECUTABLE_HANDOFF.md`. Nothing was merged into main,
pushed, released or changed in either consumer's checkout.

FiniteProtocolBundle governs ProtocolTransaction
KnowledgeChangeHistory consumes FiniteProtocolBundle
ProtocolTransaction consumes VerifiedPrefix
ProtocolTransaction produces ProtocolReplay
ProtocolReplay preserves DomainProjection
ActionLifecycle dependsOn ProtocolTransaction

## Integration evidence during execution work

The full current Shop selector reports 205 passed and five frozen-evidence
comparison failures. The same five tests pass at original Core `2a112405`.
The first differing full-Shop ledger entry is the retained compiled contract:
only its producer digest and resulting evidence digest differ. The producer is
the already repaired compiler `51c019d49c3cd7d75330e02c5d728a873254cc4b56ca122dda078b15c25bcb3f`,
not the original `5eb3ca2ba74e8cee3d8e7f5d4710ae026f728ffa5923d215a00c40716c03edcf`.
These are not action-program effects.

The existing independent compatibility probe was rerun on exported original
Core and this isolated implementation. All six scenarios pass exact parity
under the already frozen `gate.json` difference list: fresh Shop, document,
object-event, public population, showcase and correction. No new excluded
field, golden rewrite or skipped failure was introduced. The raw current Shop
selector is not claimed green. Frozen evidence remains evidence of its exact
historical producer, while current behavioral parity remains separately tested.

## Consumer-found schema boundary correction

A read-only Semantic Re-entry audit of `1ed23e002b81229b97997f08f5157c23a55112ec`
found that `$dynamicRef` escaped the finite schema check. A missing local
reference then raised a JSON Schema implementation exception instead of a typed
refusal. Nonlocal spellings also passed definition and bundle checks; neither
the consumer nor Core executed a nonlocal reference or made a retrieval call.

The corrective RED sequence is `0882806`, `5bec065`, `d4719d0`. The first run
had 12 failures and 8 passes; the second had 14 failures and 8 passes. Four
additional instruction-schema controls failed against the intermediate working
correction. The final test file has 26 cases. It covers schema-position versus
ordinary-data distinctions, nested value schemas, unused profile schemas,
owning bundle refusal and selection refusal with exact ledger-byte preservation.

GREEN is `5d0addafc3155cd795ab4bc99da0791489bc492c`, tree
`1a1d3b7a4b52d05790d59e6ba1fa4c11ac2bbdda`. Its focused schema, static-definition,
executor, owning-history and exact-definition-reuse selector passes 139 tests
in 11.67 seconds. The production change is confined to `finite_program.py`.
Value schemas now have an explicit keyword set per primitive type. Only
`properties` and `items` contain nested value schemas; names and `const`/`enum`
values remain ordinary data. References, dialect changes and hidden applicators
are outside this subset. The instruction-schema scan separately allows local
ordinary references, rejects dynamic references, and visits schema positions
only. The owning interpreter still requires its exact installed instruction
grammar. No new operation, capability, callback or policy was added.

The initial final-regression run at `1ed23e0` was interrupted after 145 passes
when this defect arrived. It is not a completed gate. The earlier 86-event
packaged-replay check also belongs to `1ed23e0`, not this corrected successor.
Neither superseded result is used as final verification of the correction.

## Consumer-found registration constraint correction

The same consumer audit found that grant scope/permission strings and monitor
version strings could be whitespace-only after real registration. Core expanded
the reproducer across the 12 fields already listed in
`lifecycle/registration-nonblank-gap.json`. It did not invent a new census or
tighten unrelated fields. RED `c6a375d` produced 12 failures and 5 passes: five
malformed records were admitted, while seven fields refused later or under a
different guard rather than the declared input constraint.

GREEN `28fe109faee16f3756387077846d2c7fb5dc0da9`, tree
`b9f48dc3e3c0c37bbad3f1ef58d1d1264843dae9`, adds 17 authoring lines that bind the
existing census to actual record input schemas, including list item schemas.
The selected artifact retains those constraints and the existing interpreter
enforces them. No interpreter operation or policy vocabulary changed. The old
gap document remains historical evidence; its field census now has executable
coverage. All 45 registration, nonblank and prerequisite tests pass in 24.46
seconds. Every malformed case preserves exact prior ledger bytes and the
reopened receipt. Four positive cases preserve nonblank values with surrounding
whitespace, including `" AMEND "`, without normalization.

At the preceding schema-fix coordinate the mechanism partition passed 497
tests. Its three concurrent lifecycle partitions were interrupted after 34, 9
and 8 passes when the registration finding arrived. They are not completed
gates. Final verification starts afresh from `28fe109` below.

The complete bundle exposed a composition error in that intermediate candidate:
grant permission items now declared `nonblank`, while the action's fixed
`LOCAL_ACTION` literal still declared only STRING. The existing static checker
correctly refused their membership comparison. The completion partition had 30
setup errors, not 30 runtime failures; the other lifecycle partitions were
interrupted. This candidate is superseded and is not an integration handoff.

Corrective RED `45c08df` reproduces that complete-bundle failure directly.
GREEN `73d1a527dd237e5546d86d5c0470e9e056d41e16`, tree
`2717844476020b97002752f83d02e2091ebf1c00`, adds five authoring lines making the
existing fixed literal's nonblank refinement explicit. It changes no accepted
action value and does not relax the checker or tighten an unrelated free-text
field. The full-bundle guard plus registration/prerequisite selector passes 46
tests in 74.60 seconds. Final lifecycle verification restarts from this exact
implementation.

## Final verification at the corrected implementation

Implementation `73d1a527dd237e5546d86d5c0470e9e056d41e16`, tree
`2717844476020b97002752f83d02e2091ebf1c00`, passes all four disjoint final
partitions: mechanism 497, prerequisites/proposal/decision 74, permission 42,
and receipt/observation/real Shop composition 30. Total: 643 passed, zero
failures, errors or skips. The 37 test files cover every test file in the
action-program directory plus seven owning-kernel/history/schema files. This
is the selected action gate, not a full repository CI claim. Exact selectors,
observed environment and results are in `../execution-verification.json`.

A clean source archive of that exact implementation built a wheel with no
isolation, installation or network access. A fresh process imported Core from
the extracted wheel, refused research/test imports, and reopened the final
86-event Shop log. It reproduced five KCSs, one contract revision, B/e7 quantity
2 superseding B/e4, the unchanged domain complement, the FAILED receipt and the
independent CONFIRMED observation. It also verified the packaged schema guard
and the corrected retained nonblank declarations. This uses existing declared
dependencies; it is not a new clean-install or sdist-parity claim.

Wheel SHA-256 is
`6830bf19e033f6eeaed1b5e6dbdb1fdc282d5c288934dc46d6d21455fa8c73a7`.
Final history SHA-256 is
`d56a92c543930680849de70116cd3dee5865c48d40a677cfae317ab39ce22a2c`.
The final bundle is
`sha256:410660217793de1d5ce405888915693b65fc08b7c03e2ca7a5834e3a554ca477`.
Full ledger, graph and protocol identities are in the verification receipt.

The consumer independently passed 175 correction tests at the earlier
`28fe109` boundary. That establishes the two reported fixes, not its review of
the later literal refinement or this final lifecycle. The corrected exact
handoff is ready for independent consumer verification. Their domain action
variants, effects, observations and synthesis remain their work, not additional
Core prerequisites. Neither consumer's experiment gates the other.

Self-inquisition: `protocol_role_is_explicit` and
`optional_profile_stays_optional` hold at this bounded action profile. Without
selection, a structural-only history acquires no action obligations or action
state. The Python kernel executes declared operations; action-specific rules
and the nonblank field census remain identified data. No root ontology, graph
write port, effect callback, second ledger or fallback was added. Main and both
consumer checkouts remain untouched. Review and main integration are separate
from this isolated implementation approval.

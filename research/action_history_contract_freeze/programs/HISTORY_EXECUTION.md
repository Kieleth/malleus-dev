# Owning-history execution cut

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

The actual action context/proposal program must next cross this same owning
gate as one atomic pair. The neutral pair test is not that proof. Then bind
the real check outputs, epistemic decision/transition, authority assessment,
authorization, dispatch, terminal execution receipt and separate observation.
The pure check/control tests do not replace those integration stages. Robotics
and Semantic Re-entry remain blocked on that complete shared handoff, not on
each other. This isolated work has not changed main or either consumer.

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

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

`append_protocol_events` accepts a transaction name, exact expected full
head/count and a nonempty ordered tuple of event drafts. Each draft carries
event ID/type, actor, transaction time, data and named raw retention inputs.
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

FiniteProtocolBundle governs ProtocolTransaction
KnowledgeChangeHistory consumes FiniteProtocolBundle
ProtocolTransaction consumes VerifiedPrefix
ProtocolTransaction produces ProtocolReplay
ProtocolReplay preserves DomainProjection
ActionLifecycle dependsOn ProtocolTransaction

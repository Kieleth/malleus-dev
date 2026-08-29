# Small Shop Graph Realization experiment charter

Status: frozen research-local experiment boundary

Canonical fixture: `OKG-FX001`, Small Shop Fulfilment

Checkpoint: `OKG-CP002`

Selection decision: `OKG-D013`

This charter defines the first empirical thread for the deterministic Malleus
compiler. It records research intent and test boundaries. It does not define a
public API, write accepted knowledge, or grant authority to its private journal.

## Authority boundary

The compiler is a deterministic partial function over exact, closed inputs. It
produces exact artifacts or an exact typed refusal.
Independent oracle bytes are test evidence and are never execution input.

An optional ontology-builder/corrector skill may propose exact ontology, patch,
or configuration bytes. The skill is an external, untrusted proposal producer.
Its candidate bytes enter the ordinary evidence and protocol-review path.
Only accepted exact bytes become compiler input.
Compiler execution and replay never invoke the skill.

The private research journal in this directory records experiment intent and
evidence coordinates. It is not `ProtocolLedger`, `JsonlLedger`, the accepted
knowledge graph, the contract-compiler overseer ledger, or any runtime authority.
It cannot accept a proposal or change a projection.

## Frozen RET ladder

The cases run in this order. A later case may depend on the accepted projection
from an earlier case, but no case may silently manufacture its prerequisite.

### RET-000, contract without population

Compile the fixture ontology into an `EffectiveContract`. The ontology contains
zero ABox population and produces zero `ProposedOperation` values.

### RET-010, order and one physical unit

Starting from an empty accepted graph base, produce exactly:

1. `O1` as one sales-order entity.
2. `X1` as one distinct physical inventory-unit entity.
3. `OrderContainsUnit(O1, X1)` as one Entity-to-Entity relation.

The result must pass through ordered operations, isolated staging, a
proposal-bound protocol decision, protocol replay, and accepted projection.
Direct GraphRecipe materialization is not GREEN.

### RET-020, fixed-arity payment settlement

After `I1` and `I2` exist in the verified base, add exactly:

1. `P1` as one payment entity.
2. One settlement from `P1` to `I1`.
3. One settlement from `P1` to `I2`.

This case tests the fixed-arity two-invoice recipe only. It makes no generic
fan-out or cardinality claim.

### RET-030, published corrections

Represent the supplier-order `B` correction from `1Y` at `e4` to `2Y` at `e7`.
Then represent the bounded `I2` correction at `e9` without inventing an invoice
value absent from the source. The temporal binding must name what is superseded.

### RET-040, Event-to-Entity RED

The `e27` packing occurrence correlates an Event with `O1`, `X1`, `X2`, `Y1`,
and `R4`. Under `OD-010`, current relation endpoints are Entity-to-Entity. This
case must return a typed refusal or the named gap
`EVENT_ENTITY_CORRELATION_REPRESENTATION_UNSELECTED`. It must not broaden the
endpoint model implicitly.

### RET-050, per-entity Event ordering RED

Per-entity Event ordering remains a typed gap. The initial profile does not
claim Event-to-Event relation support or an accepted derivation rule. Use the
named gaps `EVENT_EVENT_DIRECTLY_FOLLOWS_ENDPOINT_REFUSED_BY_OD_010` and
`PER_ENTITY_ORDER_DERIVATION_PROFILE_UNSPECIFIED` where applicable.

### RET-060, exact replay

Given the exact declared inputs and the exact accepted protocol history, replay
must produce the same declared accepted projection. Replay consumes retained
bytes and recorded artifacts only.

## Permanent physical-identity guard

`Y1` and `Y2` are distinct physical items. They are not revisions, aliases,
corrections, or superseding records of each other. Any attempt to supersede
`Y1` with `Y2`, or `Y2` with `Y1`, must refuse as an identity collapse.

## Meaning of GREEN

GREEN means that ordered `ProposedOperation` values were staged atomically,
bound to an accepted protocol decision, replayed from the protocol history, and
observed in the accepted projection. Direct GraphRecipe materialization, direct
graph mutation, or a journal entry alone never counts as GREEN.

The public ABox encoding profile and any Event-endpoint expansion are deferred.
Neither is selected by this charter.

## Deferred fixture choices

The following choices remain `DEFERRED`. This charter records no selection:

1. `RET-010` source occurrence.
2. `X1` to `X` transformation.
3. Relation-type literal.
4. Valid-time, calendar, and timezone policy.
5. Passive versus gating review.
6. Evidence-sufficiency rule.

Each choice requires an explicit decision and a failing test before its first
implementation consumer.

## Journal staging

Journal version 1 accepts only `OPERATOR_DECISION_RECORDED` and
`INTENT_RECORDED`, the kinds required by the truthful seed. The following kinds
remain future work and must be added TDD-first when the first real consumer
exists:

1. `INPUT_SET_FROZEN`
2. `ORACLE_FROZEN`
3. `RUN_RECORDED`
4. `MUTATION_RECORDED`
5. `VERIFICATION_RECORDED`
6. `REPLAY_RECORDED`
7. `FINDING_RECORDED`

The seed contains no run, mutation, verification, replay, finding, input-freeze,
or oracle-freeze claim.

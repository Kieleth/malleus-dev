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

## Approved RET-010 fixture bundle

The approved research direction retains `e27` as the source occurrence, derives
Entity-to-Entity candidate pairs, and selects only `O1` and `X1`. Deriving that
view from `e27` does not create or support an `e27` Event node. Event correlation
support remains `RET_040_REMAINS_TYPED_RED`, so RET-040 remains typed RED.

The `X1` to `X` transform is an explicit total lookup from `X1` to `X`. The
relation-type literal is `ORDER_CONTAINS_UNIT`. The source-time grammar is
`%d-%m %H:%M`, normalized to `2000-05-07T17:00:00Z`. The synthetic year and UTC
are fixture-derived temporal provenance, not claims made by the publication.

Review is passive exact review. It records the check but does not accept input
and has no acceptance authority. Evidence sufficiency means a closed
derivation package. Its claim is scoped to deterministic derivation from the
declared inputs, not real-world truth.

The exact selected values are:

1. `source_occurrence: RETAIN_E27_DERIVE_ENTITY_PAIRS_SELECT_O1_X1`
2. `x1_to_x_transform: EXPLICIT_TOTAL_LOOKUP_X1_TO_X`
3. `relation_type_literal: ORDER_CONTAINS_UNIT`
4. `source_time_grammar: %d-%m %H:%M`
5. `normalized_valid_time: 2000-05-07T17:00:00Z`
6. `temporal_provenance: FIXTURE_DERIVED_SYNTHETIC_YEAR_AND_UTC`
7. `review_semantics: PASSIVE_EXACT_REVIEW_NOT_ACCEPT_AUTHORITY`
8. `evidence_sufficiency: CLOSED_DERIVATION_PACKAGE`
9. `event_correlation_support: RET_040_REMAINS_TYPED_RED`

The earlier journal decision remains an immutable statement that these choices
were deferred at that time. The appended decision records their later approval.

## Journal staging

Each v1 record hash uses this exact preimage, encoded as canonical JSON via `malleus.ledger`:

```text
record_hash = content_digest({"domain_separator":"malleus:research:small-shop-journal:v1","record":record_without_record_hash})
```

The v1 evidence vocabulary is closed to these role and path pairs:

- `RUNNING_DOMAIN_CHECKPOINT` -> `design/GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md`
- `ONTOLOGY_REALIZATION_DESIGN` -> `design/ONTOLOGY_DRIVEN_KG_REALIZATION.md`

Both pairs occur exactly once in every v1 seed payload. The repository commit,
tree, committed blob bytes, SHA-256 digest, and byte length remain mandatory.

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

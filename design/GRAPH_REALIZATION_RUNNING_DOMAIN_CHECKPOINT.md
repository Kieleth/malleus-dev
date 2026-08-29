# Graph Realization running-domain checkpoint

Checkpoint ID: `OKG-CP002`

Recorded: 2026-08-28

Selection authority: author

Decision: `OKG-D013` selects fixture object `OKG-FX001`

Status: Small Shop Fulfilment locked; exact source and oracle artifacts remain
to be authored

Purpose: preserve the domain selection, its literature lineage, the concrete
protocol boundary it must exercise, parallel-session ownership, and the exact
resumption point before implementation.

This checkpoint records no shipped capability. The authoritative fixture
definition is the `OKG-FX001` section in
[`ONTOLOGY_DRIVEN_KG_REALIZATION.md`](ONTOLOGY_DRIVEN_KG_REALIZATION.md).

## 1. Locked selection

The canonical running domain for Graph Realization is **Small Shop
Fulfilment**. `OKG-D013` is the accepted selection decision. `OKG-FX001` is the
fixture object it selects. The selection is binding for:

1. Explanations of ontology, EffectiveContract, ABox population, semantic
   proposals, protocol events, ledgers, and KG projections.
2. Research-local Gedankenexperiments and TDD.
3. The first complete source-to-accepted-KG conformance fixture.
4. Compiler and realization boundaries that need a domain consumer.
5. Public documentation once the relevant capability is promoted.

Physics and chemistry remain later independent stress domains. They may test
units, uncertainty, measurement, instrument identity, competing models, and
ontology evolution. They do not replace or delay `OKG-FX001`.

The fixture is synthetic and informed by Fahland's example, not copied source
data. Shop vocabulary remains fixture-only and does not enter the Malleus root
ontology. Existing `GE-000` through `GE-020` fixtures remain frozen historical
evidence. Replacing `OKG-FX001` requires a superseding decision and
dependency-impact analysis. `OKG-D013` does not override contract-compiler
`OD-010`.

## 2. Why this domain

The scenario is inherited from Fahland's
[Event Knowledge Graph chapter](https://doi.org/10.1007/978-3-031-08848-3_9),
which uses orders, supplier orders, physical items, actors, invoices, payments,
corrections, and multi-entity events. It is understandable without specialist
training while still forcing identity, temporal, mapping, revision, and
multi-source questions.

The fixture composes bounded techniques from:

1. [SLOGERT](https://doi.org/10.1007/978-3-030-77385-4_38), heterogeneous log
   lifting and OTTR templates.
2. [Blue Brain Nexus](https://doi.org/10.3233/SW-222974), append-only revision
   and replayed projections.
3. [OntoLogX](https://doi.org/10.1002/aisy.202501381), ontology-guided
   validation and correction before persistence.

Those sources do not establish Malleus's combined protocol. They confirm and
inform selected components. Malleus must still test its own composition.

## 3. Fixed conceptual closure

The first complete fixture must retain, at minimum:

```text
Actors:             R1, R2, R3, R4, R5
Customer orders:    O1, O2
Supplier orders:    A, B; e4 records B as 1Y and e7 updates B to 2Y
Product kinds:      X, Y
Inventory units:    X1, X2, X3, Y1, Y2
Invoices:           I1, I2; e9 records an update to I2
Payment:            P1, settling I1 and I2
Warehouse event:    e27 packs O1 with X1, X2, Y1 by R4
```

`Y1` and `Y2` are distinct physical items. They are never versions, aliases, or
superseding records of each other.

The first retained source closure must use several deterministic source roles,
not one preassembled graph file. Explanatory filenames are:

```text
orders.csv
supplier-orders.json
warehouse.jsonl
invoices.csv
payments.csv
```

Exact bytes, qualified symbols, locators, content digests, authorship, and
expected artifacts remain separately owned outputs. This checkpoint must not be
used as an oracle generator.

## 4. Required vertical path

Every complete worked example must preserve this sequence:

```text
LinkML contract source
  -> exact source and import closure
  -> neutral contract facts
  -> EffectiveContract
  -> retained domain occurrence
  -> mapping + transformation + identity + recipe invocation
  -> atomic semantic graph patch or typed gap
  -> ordered ProposedOperation values
  -> isolated candidate staging
  -> evidence and other named checks
  -> proposal-bound epistemic decision
  -> append-only protocol event sequence
  -> accepted temporal KG projection
  -> replay and realization attestation
```

The occurrence, semantic proposal, protocol event, ledger entry, and accepted KG
assertion are distinct identified objects. No implementation may collapse them
into one subject-predicate-object tuple or one generic event.

### 4.1 Compiler authority boundary

The Malleus compiler is fully deterministic. Exact, closed input bytes produce
exact compiled artifacts or an exact typed refusal. It does not invoke a person
or generative system to complete missing meaning.

An optional Malleus ontology-builder/corrector skill may propose exact ontology
or patch bytes from an existing ontology or retained project evidence when no
ontology exists. The skill is an untrusted proposal producer outside the
compiler. Its bytes enter ordinary evidence, review, and decision handling.
Only accepted exact bytes become compiler input. Replay uses retained bytes and
recorded artifacts and never calls the skill.

## 5. Required positive and RED threads

The accepted GREEN ladder is:

1. **GREEN 1, self-contained creation.** Create `O1`, distinct physical item
   `X1`, and fixture-defined `OrderContainsUnit(O1, X1)` in an empty graph base.
   This must reach ordered `ProposedOperation` values, atomic staging, decision,
   replay, and the accepted graph without a privileged compiler write path. The
   paper supports the association through `e27`; the direct predicate name,
   direction, and standalone allocation source are declared fixture semantics.
   This derived Entity-to-Entity view does not satisfy the RED `e27`
   correlation obligation.
2. **GREEN 2, existing-base settlement.** After `I1` and `I2` exist, create
   `P1` and two `PaymentSettlesInvoiceRelation` records. The fixture recipe
   `PaymentSettlementTwoInvoices` is fixed at two invoice arguments. It does
   not claim generic collection expansion, arbitrary fan-out, or cardinality
   enforcement.
3. **GREEN 3, actual correction.** Represent the supplier-order `B` change from
   `1Y` at `e4` to `2Y` at `e7`, then retain the bounded `I2` update at `e9`.
   The fixture must define the state or claim identity being superseded. Because
   the paper does not expose the changed invoice value, it may not invent that
   value as a paper claim. GraphRecipe stops at `ProposedOperation`; a separate
   temporal binding owns valid time, supersession, acceptance, and application.

The primary RED thread is the warehouse packing occurrence:

```text
e27 correlates with O1, X1, X2, Y1, and R4
```

Fahland's event model also requires per-entity event order. The accepted
`OD-010` Malleus profile permits only Entity-to-Entity relation endpoints. The
current runtime therefore cannot silently represent Event-to-Entity or
Event-to-Event relations. The first experiment must return a typed gap or
refusal. Endpoint broadening, typed reference projection, or another encoding
requires a separate accepted design decision and migration analysis.

The first experiments should use these exact status codes where applicable:

```text
EVENT_ENTITY_CORRELATION_REPRESENTATION_UNSELECTED
EVENT_ENTITY_RELATION_ENDPOINT_REFUSED_BY_OD_010
EVENT_EVENT_DIRECTLY_FOLLOWS_ENDPOINT_REFUSED_BY_OD_010
PER_ENTITY_ORDER_DERIVATION_PROFILE_UNSPECIFIED
MULTIVALUED_RETAILER_RECIPE_OUTSIDE_IMPLEMENTED_GE000_GE020_SLICE
```

Additional mandatory RED cases are:

1. An ontology without population inputs produces zero ABox records.
2. A root `instances` field or arbitrary unlisted LinkML field refuses the
   complete compilation.
3. A missing mapping, transformation, identity rule, recipe binding, or required
   evidence item blocks plan construction.
4. An identity collision cannot be resolved by input order or adapter behavior.
5. A description-only edit changes source attestation but preserves semantic
   contract identity.
6. A required-field, range, identity, or used-prefix change changes the relevant
   semantic identity and closes impact over dependent artifacts.
7. Any attempt to supersede `Y1` with `Y2`, or vice versa, refuses as a physical
   identity collapse rather than becoming a temporal correction.

## 6. Evolution thread

The first ontology evolution starts with shipment represented only as an
activity associated with an order. A later contract introduces `Shipment` as a
first-class entity so one order may have partial shipments and independent
tracking identities.

The migration experiment must classify every affected ontology fact, mapping,
transformation, identity rule, recipe, population plan, construction plan,
accepted graph record, projection, and reader. Old ledger history remains
unchanged. A new accepted realization carries explicit lineage.

This ontology-evolution thread follows the GREEN 3 data-revision baseline. The
first baseline corrects declared state under one contract. The later thread
changes the contract itself and therefore requires wider dependency closure.

## 7. Parallel-session ownership

At this checkpoint:

1. This literature-reinforcement task owns the `OKG-FX001` explanation in
   `ONTOLOGY_DRIVEN_KG_REALIZATION.md` and this checkpoint.
2. The **Review Malleus worktrees** task owns the compiler program, integration
   DAG, workstream assignments, pause and reanchoring transaction, governance
   ledger, and unified integration gates.
3. Existing unrelated research and paper drafts in the shared worktree remain
   user-owned and untouched.

The author's direct sequencing instruction in the worktree-review task takes
precedence over older queued wording that placed this fixture after `CC-R08`.
The compiler lane is being reanchored around `OKG-FX001` now.

## 8. Exact resumption point

Resume by fixing independently owned source scenarios and human-authored
expected artifacts for the conceptual closure above. Then build the smallest
vertical experiment that demonstrates:

```text
RET-000 -> ontology alone produces an empty population
RET-010 -> GREEN 1 creates O1, X1, and OrderContainsUnit in an empty base
RET-020 -> GREEN 2 adds P1 and two settlement relations after I1 and I2 exist
RET-030 -> GREEN 3 versions B state at e7 and retains the bounded I2 update at e9
RET-040 -> RED e27 Event-to-Entity correlation returns the named OD-010 gap
RET-050 -> RED per-entity Event-to-Event order returns the named OD-010 gap
RET-060 -> later source integration preserves deterministic replay
```

Only after these objects are visible should the design select the missing public
ABox graph-patch profile or change relation endpoint semantics. Do not implement
an encoding merely to make the RED event case pass.

## 9. Repository observation

The selection began from observed `main` commit `c6e3616`, which activated the
compiler oracle workstreams. This commit is a coordinate, not a frozen worktree
claim. Parallel sessions may advance `main`; subsequent durable integration must
bind the exact commit and tree it validates.

No source corpus, oracle, ontology, recipe, compiler, runtime code, public API,
or shipped behavior was created by this checkpoint.

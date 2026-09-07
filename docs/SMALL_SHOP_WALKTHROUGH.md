# Small Shop end-to-end walkthrough

## Start here: can we explain why the graph says quantity 2?

A supplier-order file contains two reports: quantity `1` at `e4`, quantity `2`
at `e7`. A database can store the latest number. This example asks for more:
which source row supplied it, what allowed it into the graph, what it replaced,
and whether we can rebuild that answer without the original working files.

This repository-local run answers those questions through the public `malleus.compiler`
API. It also carries the shop's order, inventory, invoices and payment through
the same path:

```text
Ontology bytes -> compiled contract: what records are allowed
Source bytes + authored population plans: what we propose to record
Checks + admission -> one append-only history: what was accepted
Reopen + replay -> knowledge graph: what can now be queried
Record trace -> retained plan and source: why this record is here
```

The compiler does not invent an ontology or decide that a later report is a
correction. In this fixture, the author explicitly selects the `state-version`
profile and supplies the `e4` to `e7` replacement in the plan. Malleus checks and
executes that declaration. Structural acceptance is not proof that the source
is true or that the author's mapping captures everything it means. It does not
establish epistemic acceptance or authorize an action.

The runner uses Core's `create_structural_history` and
`admit_structural_change` helpers. Core checks each prepared change and records
the structural outcome; the example does not author `SATISFIED` results or load
a Shop-specific admission policy. This shipped default is one optional
implementation, not a requirement of every Malleus adopter. Source registration
and the source-to-record mapping remain explicit adopter work.

From a configured environment at the repository root, run the default-admission
example:

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.default_admission.run --output build/small-shop-default-admission
```

Choose a new output directory. The runner refuses an existing directory and
cannot overwrite a previous run. It writes `history.jsonl` and `evidence.json`;
use the read-only code below to reopen that history. The result is 50 ledger
events, five accepted changes, one additive ontology revision, ten historical
records and nine current records. This is the complete **selected fixture**,
not the whole shop domain.

Inspect the actual inputs and outputs in order:

| Part | Exact artifact | What to look for |
| --- | --- | --- |
| Ontology | [Target schema](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_full_public_v1/input/tbox/small-shop.yaml) | `SupplierOrderState` and its required properties |
| Source | [Supplier rows](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl) | The two quantities, with no date or replacement field |
| Plan template | [e7 population plan](../research/ontology_driven_kg_realization/experiments/small_shop/public_population/plans/supplier-e7.json) | Field derivations, explicit supersession and chosen valid time |
| Run inputs | [Default-run input list](../research/ontology_driven_kg_realization/experiments/small_shop/default_admission/inputs.json) | Exact source, ontology and template paths, in the declared step order |
| Contract and history | Generated `build/small-shop-default-admission/evidence.json` | Structural-bundle identity, revision count and exact ledger digest |
| Graph and provenance | The generated evidence file's `graph`, `queries` and `records` | Quantity `2` currently, with the retained `e4` predecessor and source trace |

The runner retains the linked plan template and changes only its contract
identity to bind Core's selected structural bundle. The resulting plan is also
retained in the ledger. Source values, field derivations, valid times and
supersession rules are unchanged. Generated evidence describes this new run;
it does not replace any committed predecessor receipt.

### Ask the rebuilt graph

After running the command above, this code reads the ledger, not a saved graph:

```python
from pathlib import Path
from malleus.compiler import KnowledgeChangeHistory, trace_population_record

replay = KnowledgeChangeHistory.reopen(
    Path("build/small-shop-default-admission/history.jsonl")
).replay()
row = replay.graph.query("SupplierOrderState", supplier_order_id="B")[0]
trace = trace_population_record(replay, row["id"])
print(row["ordered_quantity"])
print(trace.record_history.supersedes_record_id)
for derivation in trace.derivations:
    if tuple(derivation["path"]) == ("properties", "ordered_quantity"):
        print(derivation["locator"])
```

It prints `2`, `supplier-order-state:B:e4`, and `row:1:quantity`. The locator
uses zero-based rows. The trace also returns the exact retained source bytes,
not just a path that might now point to a different file. A test executes this
exact snippet and verifies that reading it leaves the ledger unchanged.

### Four distinctions we test, not assume

These are separate conformance cases. They are not four hidden modes of the
five-plan run above.

| Input decision | Replayed result | What it proves |
| --- | --- | --- |
| Two supplier reports, no replacement instruction | Both quantities remain current | Later recording alone does not mean correction |
| Explicit `e7` replacement of `e4` | Only quantity `2` is current; quantity `1` remains in history | Correction changes the view without erasing its predecessor |
| Neither report states a valid date | `NONE_STATED` with explicit null survives the plan, change and trace | Recording order is not an invented domain date |
| A synthetic clerk-note capture declares that its graph cannot express modality | `MODALITY_NOT_EXPRESSIBLE` remains in retained evidence after reopen | A declared limitation is visible, not silently promoted into a graph fact |

The first three use the retained supplier rows. The fourth is explicitly a
synthetic companion fixture, not extra data attributed to the literature.
A gap is declared by the adopter; passing the capture census does not prove
that every source meaning was captured or every missing relation discovered.

Run the full path and these controls together:

```bash
python -m pytest -q tests/contract_compiler/pareto/test_default_shop_walkthrough.py tests/contract_compiler/pareto/test_small_shop_default_admission.py tests/contract_compiler/pareto/test_unstated_valid_time.py tests/contract_compiler/pareto/test_capture_coverage_boundary.py
```

### Import a fresh supplier file

The run above uses authored plans. A second example now starts with a new
supplier file and generates its plan through a small Shop-owned adapter.
Its two synthetic orders, SYN-C and SYN-D, report quantities 3 and 5. They
are test data, not extra observations attributed to the retailer paper.

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.fresh_import.run --output build/small-shop-fresh-import
```

This runs the complete Shop first, then imports both rows in one additional
change. Reopen yields six changes, twelve historical records and eleven
current records, with every previous record preserved. No source date is
invented: both new records carry explicit `NONE_STATED` valid time. Malformed
rows refuse before retention; stale admission refuses without further writes.

See the {download}`fresh-import guide <../research/ontology_driven_kg_realization/experiments/small_shop/fresh_import/README.md>`
for the source format, explicit mapping, queries and limits, and its
{download}`recorded evidence <../research/ontology_driven_kg_realization/experiments/small_shop/fresh_import/evidence.json>`.
The adapter owns the mapping. Core supplies compilation, admission, history
and source trace without any Shop-specific runtime change.

### Earlier evidence is still evidence

The older [public-population evidence](../research/ontology_driven_kg_realization/experiments/small_shop/public_population/evidence.json)
records a 48-event run with an explicit fixture policy. It remains a tested
lower-level example, not the default admission path above.

The detailed walkthrough below describes an earlier fixture-specific runner.
Its recorded files are preserved, not recomputed in place. A compiler
diagnostic edit changed the producer fingerprint and therefore the histories'
fingerprints without changing these graph results. The
[6 September correction evidence](../research/ontology_driven_kg_realization/experiments/small_shop/evidence_2026_09_06/correction/explanation.json),
[occurrence evidence](../research/ontology_driven_kg_realization/experiments/small_shop/evidence_2026_09_06/object_event/evidence.json),
and [showcase evidence](../research/ontology_driven_kg_realization/experiments/small_shop/evidence_2026_09_06/showcase/explanation.json)
record the current runs separately.
Their tests require exact current bytes and protect the earlier files by hash.
The 48-event public-population evidence already matched and was not rewritten.

## Historical showcase in detail

> **Scope:** The remaining sections explain the earlier research-local showcase. The
> runner, mappings, query facade, and evidence formats are private surfaces,
> not stable public APIs or wire contracts.

The showcase joins three controlled Small Shop fixture bundles in one run. It
starts with retained source bytes and a closed ontology dependency set. Only
the ontology closure is compiled into neutral contract facts. Fixture-specific
source mappings then turn selected source rows into five immutable
`KnowledgeChangeSet` values. A declarative machine, check contract, and policy
admit those changes to one append-only ledger. Replay of that ledger derives a
nine-record current knowledge graph, and read-only queries expose both current
facts and their accepted history.

The point is not the size of the graph. The point is that meaning, mapping,
checks, decisions, history, and projection remain separate and inspectable.

The original showcase below remains frozen evidence. A newer sibling
[public-path conformance run](../research/ontology_driven_kg_realization/experiments/small_shop/public_population/evidence.json)
now sends the same complete five-stage dataset through `malleus.compiler` using
five canonical neutral population plans. It also records one additive ontology
revision, reopens one history, and traces every current and superseded record
back to its retained plan, field derivations, source bytes, and mapping bytes.

## 1. Start with controlled source bytes

The baseline source says that warehouse event `e27` packed order `O1` with
unit `X1`, while a separate lookup identifies the unit's product:

```json
{"activity":"Pack Shipment","actor":"R4","event_id":"e27","items":["X1","X2","Y1"],"order":"O1","time":"07-05 17:00"}
```

```text
inventory_unit_id,product_code
X1,X
```

The correction source records two ordered states for supplier order `B`:

```json
{"event_id":"e4","product_code":"Y","quantity":1,"supplier_order_id":"B"}
{"event_id":"e7","product_code":"Y","quantity":2,"supplier_order_id":"B"}
```

The settlement bundle supplies two invoice identities and one payment event:

```text
invoice_id
I1
I2
```

```json
{"event_id":"e30","invoice_ids":["I1","I2"],"payment_id":"P1"}
```

These are controlled fixture transcriptions attributed to Table 1 of Dirk
Fahland's chapter,
[*Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs*](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9).
The supported publication claim for `e30` is that `P1`, `I1`, and `I2`
co-occur. The direction `P1` settles `I1` and `I2` is declared by the
[settlement fixture](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_settlement_v1/input/attribution.json),
not asserted as a source-native direction by the chapter.

Inspect the exact
[warehouse JSONL](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/sources/warehouse.jsonl),
[inventory CSV](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/sources/inventory-units.csv),
[supplier history](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl),
[invoice CSV](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_settlement_v1/input/sources/invoices.csv),
and [payment JSONL](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl).

## 2. Compile meaning, then map population

The ontology compiler closes the settlement ontology over its imports and
emits 1,040 frontend-neutral facts. The
[recorded explanation](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/explanation.json)
contains these representative facts:

```json
[
  {"object":"https://malleus.dev/schema/Entity","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://malleus.dev/schema/small-shop-fulfilment/SalesOrder"},
  {"object":"https://malleus.dev/schema/Entity","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://malleus.dev/schema/small-shop-fulfilment-correction/SupplierOrderState"},
  {"object":"https://malleus.dev/schema/Relation","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://malleus.dev/schema/small-shop-fulfilment-settlement/PaymentSettlesInvoiceRelation"}
]
```

The effective contract binds that structural meaning to the selected machine,
policy, and history contract. Its identity is
`sha256:0c43eac9537c1fbc5102f3b805dc3e6a17530e7ab1f573020fe2d9a559da67a3`.

Population is a separate step. The
[baseline mapping](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/mapping.json),
[settlement mapping](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/settlement-mapping.json),
and [correction mapping](../research/ontology_driven_kg_realization/experiments/small_shop/correction/mapping.json)
produce this fixed sequence:

| Stage | Immutable change | Proposed records |
| --- | --- | --- |
| 1 | `change:RET-010:genesis` | `O1`, `X1`, and `contains:O1:X1` |
| 2 | `change:SHOP-PAYMENT-SETTLEMENT:invoice-base` | `invoice:I1` and `invoice:I2` |
| 3 | `change:SHOP-PAYMENT-SETTLEMENT:P1:e30` | `payment:P1`, `relation:P1:I1`, and `relation:P1:I2` |
| 4 | `change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4` | `B`, product `Y`, quantity `1`, occurrence `e4` |
| 5 | `change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e7` | `B`, product `Y`, quantity `2`, occurrence `e7`, superseding the `e4` record |

### What `genesis` means here

In the original frozen showcase, `genesis` is a fixture name, not a formal
`KnowledgeChangeSet` role. Its first change is recognizable because it is the
first accepted population over an empty graph. Its ledger base already contains
49 contract, protocol, and source events, and it is not a complete seed
snapshot: invoices and the initial `B@e4` state enter through later changes in
test-ladder order.

That original runner uses a fixture-specific state-versioning pattern, not a
reusable Small Shop ledger vocabulary. Its mappings use labels such as
`INITIAL_DOMAIN_STATE`, `CORRECTION`, and
`FIXTURE_ORCHESTRATED_EXISTING_BASE`. They are retained inside the bound mapping
artifacts, but are not carried as typed change-role fields into, or interpreted
by, Core's generic change-set format.

The newer public-path run makes the previously implicit history choice
explicit. Every population plan binds the shipped `state-version` profile. It
declares:

- history starts with the first accepted change over an empty graph;
- completeness covers only the declared sources, not the whole world;
- one semantic unit is one state version;
- adding creates a state version, while correction and transition supersede an
  older version;
- `valid_time` is domain time and ledger order is transaction time;
- replay projects current non-superseded records.

This contract explains why `B@e4` stays in history while only `B@e7` appears in
the current graph. It does not turn `genesis` into a special operation, claim
that the first change is complete, or create a Small Shop-specific ledger.

Another adopter may choose source-attributed assertions, business events, REA
commitments, or another history model. Core now supplies closed, hashed profile
artifacts so that choice is explicit and retained. It validates and binds the
chosen declaration; it does not yet execute arbitrary projection rules from profile
text. The `object-event` profile now admits Event records and qualified
Event-to-Entity participation records through the same change-set, admission,
ledger, and replay path. That support is selected explicitly and does not
reinterpret this state-version history. Record-family admission follows the
profile's declared ontology roles, not its semantic-unit label, so another
profile may describe Events without claiming that each change is an occurrence.

Each change's source closure is bundle-wide: eight baseline members, six
settlement members, or five correction members. The retained check receipt's
`selected_records` field is the narrower row-level trace used to recompute that
specific mapped change. These are different claims. The closure binds the
whole controlled bundle; `selected_records` identifies the rows used by the
mapping.

All 19 fixture source members, including the supplier-history member containing
the `e7` row, are anchored together during bootstrap. The five stages are
therefore staged admission of pre-provisioned sources, not live observation.
The run program records this arrival model as `PREPROVISIONED_BOOTSTRAP`. Their
order follows the frozen test ladder, not business-event chronology.

## 3. Admit five changes to one ledger

The
[machine](../research/ontology_driven_kg_realization/experiments/small_shop/correction/machine.json)
defines the legal lifecycle. The
[source-mapping check](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/checks/source-mapping-conformance.json)
recomputes each declared source-to-change mapping. The
[policy](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/policy.json)
requires that check and maps `SATISFIED` to `ACCEPT`, `VIOLATED` to `REJECT`,
and `UNKNOWN` to `DEFER`.

The resulting ledger is compact enough to summarize exactly:

| Event range | Contents |
| --- | --- |
| 1-11 | Register and retain the validated contract, effective contract, history binding, run program, entrypoint, machine, policy, check contract, and three mappings. |
| 12-49 | Register and retain all 19 fixture source members, two events per member. |
| 50-54 | Admit the baseline change. |
| 55-59 | Admit the invoice-base change. |
| 60-64 | Admit the payment-settlement change. |
| 65-69 | Admit the `B@e4` change. |
| 70-74 | Admit the superseding `B@e7` change. |

Each five-event admission retains its check receipt and change, then records
proposal, check, and verdict. Source, mapping, or graph-shape drift refuses
before mutation. A refusal during a later stage leaves the earlier ledger bytes,
accepted receipt, and graph unchanged.

## 4. Replay derives the current graph

The committed [graph evidence](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/graph.json)
contains six nodes and three relations, nine current records in total:

```text
SalesOrder("O1", order_number="O1")
InventoryUnit("X1", product_code="X")
OrderContainsUnit("contains:O1:X1", O1 -> X1)
Invoice("invoice:I1", invoice_number="I1")
Invoice("invoice:I2", invoice_number="I2")
Payment("payment:P1", payment_number="P1")
PaymentSettlesInvoiceRelation("relation:P1:I1", payment:P1 -> invoice:I1)
PaymentSettlesInvoiceRelation("relation:P1:I2", payment:P1 -> invoice:I2)
SupplierOrderState("supplier-order-state:B:e7", B, Y, quantity=2, occurrence=e7)
```

The superseded `supplier-order-state:B:e4` is absent from the current graph but
present in record history. It has quantity `1`, starts at `e4`, ends at `e7`,
and points to its replacement. The current record has quantity `2` and points
back to the `e4` record.

The recorded coordinates are:

| Coordinate | Recorded value |
| --- | --- |
| Neutral contract facts | `1,040` |
| Effective contract identity | `sha256:0c43eac9537c1fbc5102f3b805dc3e6a17530e7ab1f573020fe2d9a559da67a3` |
| Ledger events | `74` |
| Ledger and acceptance head | `sha256:741853f06741d9bbf89a1d574578e57c49749dd144cce2095c568a0d65bcd415` |
| Materialization head | `sha256:72679ae14f363f4bcebe7a31ce42b63770ed852875908fade78f23f6749f7f3c` |
| Current graph records | `9` |
| Current graph digest | `sha256:b92787c8bb07e977416c7b4996ef5dd60544becbe0ca7a39b9075756ba43a6a0` |
| Receipt identity and file SHA-256 | `sha256:09b81985d03c810678704178fa3fb4c26f76b2b0077eb3bf9a3456e0d675ad41` |
| Retained run-program identity | `sha256:7096c3f82e3f96aa7e1efa6f11a120bb2b3a6c441520d66589408fd8895885c6` |

Reopening uses replay from the ledger alone, not recompilation from the ledger
alone. Replay loads retained compiled contract and protocol artifacts and does
not reread ambient fixture or mapping files. It also does not rerun ontology
closure or LinkML compilation. The current Python implementation of those
contracts is still required.

## 5. Query current facts and provenance

The [recorded query answers](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/queries.json)
show:

| Query | Recorded answer |
| --- | --- |
| `order-contents O1` | `O1` contains `X1` through `contains:O1:X1`. |
| `payment-settlements P1` | `P1` settles `I1` and `I2` through two typed relations. |
| `current-supplier-order B` | The current state is product `Y`, quantity `2`, occurrence `e7`. |
| `supplier-order-history B` | `B@e4` has quantity `1`; `B@e7` has quantity `2` and supersedes it. |
| `state-after-change change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4` | The accepted graph at that named change still contains the quantity `1` record. |
| `record-change-provenance relation:P1:I1` | The relation joins to the exact settlement change, its six-member source closure, and its seven-artifact evidence closure. |

The provenance answer labels its scope
`CHANGE_LEVEL_NOT_PER_OPERATION_CAUSALITY`. It identifies the immutable change,
contract, mapping, sources, evidence, valid time, and accepted-state
coordinates. It does not claim that each source member caused each individual
operation.

The newer public population path can go one level deeper. The conformance
fixture at
`research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_contract_revision_v1/README.md`
uses `trace_population_record(replay, "supplier-order-state:B:e7")` to verify
and return the retained `state-version` profile, population plan, four field
derivations, exact supplier-history source bytes, accepted change set, and the
`B@e4` supersession link. The trace is rebuilt after reopening the ledger and
does not write to it.

The frozen showcase on this page predates the neutral population plan and
composes its changes through the earlier direct change-set path. Its
change-level provenance remains valid, and `trace_population_record` correctly
returns `POPULATION_PLAN_NOT_BOUND` for those historical changes. The newer
public-path fixture leaves that evidence untouched and rebuilds the same
nine-record current graph through five explicit population plans. Its trace
therefore reaches retained source and mapping bytes for all ten current and
superseded records. The read API never invents a missing plan for the older
history.

Run and query the same path from the repository root:

These commands execute the current runner into `build/`. Its fingerprints
match the separate current evidence generation, not the historical coordinate
table above; the graph answers remain the same.

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.run --output build/small-shop-showcase
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.query --history build/small-shop-showcase/history.jsonl order-contents O1
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.query --history build/small-shop-showcase/history.jsonl payment-settlements P1
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.query --history build/small-shop-showcase/history.jsonl supplier-order-history B
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.query --history build/small-shop-showcase/history.jsonl record-change-provenance relation:P1:I1
python -m research.ontology_driven_kg_realization.experiments.small_shop.showcase.evidence --output build/small-shop-showcase-evidence
python -m pytest -q research/ontology_driven_kg_realization/experiments/small_shop/showcase
```

Run the complete dataset through the public population and history boundary:

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.public_population.run --output build/small-shop-public-population
python -m pytest -q research/ontology_driven_kg_realization/experiments/small_shop/public_population/test_run.py
```

That run records 48 ledger events, five accepted changes, one additive contract
revision, ten historical records, and nine current records. Its committed
[evidence](../research/ontology_driven_kg_realization/experiments/small_shop/public_population/evidence.json)
binds the exact ledger bytes and contains the graph, selected queries, and a
verified record-level provenance trace for every accepted record.

### Run the packing occurrence as an event

The state-version run answers, "What is the current shop state, and what did it
replace?" The object-event run answers a different question, "What happened,
and which enduring objects participated?" Keeping these as separate histories
makes the adopter's semantic choice visible instead of hiding it in Python.

The controlled `e27` source row says actor `R4` packed order `O1` with items
`X1`, `X2`, and `Y1`. The sibling fixture imports the optional
`object-event.yaml` vocabulary, compiles its project ontology, and admits one
change containing five Entities, one `PackShipmentEvent`, and five qualified
`EventParticipation` records. An `ORDER`, `ACTOR`, or `ITEM` qualifier says how
each Entity participated. These records are not ordinary Relations, and the
ordinary relation query remains empty.

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.object_event.run \
  --output build/small-shop-object-event
python -m pytest -q \
  research/ontology_driven_kg_realization/experiments/small_shop/object_event/test_run.py
```

The [recorded object-event evidence](../research/ontology_driven_kg_realization/experiments/small_shop/object_event/evidence.json)
matches an independently hand-authored fixture oracle. It records one accepted
change in a 14-event ledger, reopen and replay, a graph digest of
`sha256:1e9a8d5ec12b349f13f6322a051a0d7ed7153565de8c15c31900a61e3be699ba`,
ledger bytes digest
`sha256:2db22588e3b06f331006bd2f8c1bf149ec917c1a7174506d069e9e042f35c620`,
contract identity
`sha256:90c8bc3e02e34d12a6b1c3c8d9cd8a5dcba3927c42922f15eb34b8aea30efd47`,
and source identity
`sha256:6ff31debb3603892de9d015f4e412da9f40a4add384f3f939b506ab7066e640e`.
It does not claim Event-to-Event ordering, infer product codes absent from the
source row, or make the fixture ontology part of the Malleus protocol.

The committed evidence is
[explanation.json](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/explanation.json),
[graph.json](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/graph.json),
[queries.json](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/queries.json),
and [receipt.json](../research/ontology_driven_kg_realization/experiments/small_shop/showcase/evidence/receipt.json).

## Why this matters

Meaning and decisions are explicit. Ontology facts, source mappings, machine,
check, policy, and every accepted change have identified bytes. Invalid drift
refuses before it can partially mutate accepted history. The graph is
disposable because deterministic replay rebuilds it from the ledger. Frontend,
policy, check, storage, and projection adapters can be replaced only within
their declared protocol boundaries and only when conformance preserves the
same meaning and decisions.

## Exact boundary

Generic Core covers ontology closure and contract compilation, immutable
`KnowledgeChangeSet` values, ledger admission, replay, record history, and the
underlying graph query primitives. The named Small Shop source mapping and
read-only query facade remain research-local. ABox mapping is fixture-specific
Python. The public population compiler accepts an already-authored plan; it
does not invent this mapping.

This showcase does not yet identify the query program or its dependency
closure. Operation-level causality, arbitrary transaction-prefix queries,
Cypher, generic collection fan-out, scoring and evaluation, effects,
Event-to-Event ordering, and Semantic Re-entry are deferred. The fixed two-invoice mapping
proves only this declared case. The graph-at-change query addresses a named
accepted change, not an arbitrary ledger prefix or general valid-time query.

# Malleus documentation

Malleus is a protocol for making semantic change explicit. It separates the
meaning a domain declares, the change someone proposes, the checks applied to
that change, the decision to accept or refuse it, and the knowledge graph
derived from the accepted history.

Adopters do not have to use one fixed software stack. They can select the
profiles they need, replace implementations behind the same contracts, or stop
before semantic history entirely. Start with the
[protocol boundary taxonomy](protocol-boundary-taxonomy) for those boundaries.

For the current five-change demonstration, read the
[Small Shop end-to-end walkthrough](SMALL_SHOP_WALKTHROUGH.md). It extends the
historical milestones below with settlement, one ledger, replay-derived current
state, named queries, and exact change-level provenance.

The newer
[full public-path conformance evidence](../research/ontology_driven_kg_realization/experiments/small_shop/public_population/evidence.json)
executes all five changes through `malleus.compiler`, records one additive
ontology revision, and verifies every current and superseded record back to its
retained population plan, field derivations, source bytes, and mapping bytes.
It keeps the earlier research evidence unchanged.

## First compiler-to-ledger-to-knowledge-graph proof

> **Status:** Working research milestone, 3 September 2026.
> The path is executable and tested in this repository. Packages built from
> this source expose its generic executor through `malleus.compiler` and its
> contract compiler through `malleus-compiler contract`.
> Public here means an import path and installed command, not stable wire formats.
> The fixture
> mapping, high-level runner, evidence formats, and release remain research
> work.

**The first real Malleus compiler-to-ledger-to-knowledge-graph path is
complete.** That sentence has a narrow meaning: the first scoped, research-only
end-to-end slice passes its completion gate. One controlled example now crosses
the selected source-to-history-to-graph boundaries. This does not mean the
general Malleus compiler is finished.

### The question this answers

I do not want a knowledge graph that merely looks plausible. I want to point at
one fact and ask: Why is this here? Which exact source did it come from? Which
mapping interpreted that source? Which ontology constrained the resulting graph
records? Which check results were recorded? Which policy accepted the change?
Can I delete the graph and rebuild the same state from its history?

The final graph in this example contains three records. Anyone could write
those records by hand. That is not the achievement. The achievement is that
Malleus can explain why they exist, refuse a broken run without half-written
state, throw the graph away, and reconstruct the same result from retained
history.

This is the point of the compiler, ledger, and graph working together. The
contract compiler turns the selected ontology meaning into a reloadable
structural contract. Separate machine, policy, and mapping artifacts drive
what may enter the governed history. The ledger preserves the retained inputs,
proposal, supplied check receipts, and accepted verdict. The graph is the
current view produced from that history, not a second source of truth.

### Why this is a project milestone

Before this run, the new contract-compiler, declarative-machine, and
knowledge-change pieces had been proven separately, but not together. We chose
a deliberately small pet domain and made one small knowledge change cross the
whole selected path. The domain is small enough to inspect by hand and real
enough to expose the handoffs between source data, ontology, mapping, policy,
history, and graph construction.

No LLM is needed to compile, decide, or replay this path. The measured result is
deterministic under the retained inputs and current Python implementation.

In plain English, the parts have these separate jobs:

| Part | Job |
| --- | --- |
| Ontology | Defines the legal words and shapes in the domain. |
| Contract compiler | Turns the selected ontology meaning into canonical facts and a reloadable structural contract. |
| Mapping | Says exactly which source values become which proposed graph operations. |
| Machine and policy | Enforce lifecycle constraints, required receipts, and how their outcomes select a verdict. |
| Knowledge change | Seals one proposed domain-state change together with its inputs, base state, operations, and identity. |
| Ledger | Keeps the retained evidence, proposal, receipts, and decision in one append-only history. |
| Knowledge graph | Presents the accepted view derived by replaying that history. |

### Use the public boundary

The public `malleus.compiler` facade exposes the reusable executor used below:
exact-source LinkML contract compilation, population-plan compilation, governed
admission, reopen, replay, and access to the replayed graph's query methods. A
caller supplies every ontology source as exact bytes under the locator used by
the root or its imports:

```python
from malleus.compiler import compile_linkml_contract

compiled = compile_linkml_contract(
    root_locator="my-domain",
    sources={"my-domain": ontology_bytes, "linkml:types": linkml_types_bytes},
)
```

`malleus-compiler contract` compiles exact named LinkML source files. It is a
convenience frontend to the same function, not a second compiler:

```bash
malleus-compiler contract \
  --root my-domain \
  --source my-domain path/to/my-domain.yaml \
  --source linkml:types path/to/linkml-types.yaml
```

The command emits canonical validated-contract bytes. It never accepts a bare
ontology hash. The Python facade exposes the later population and history
steps, but it does not invent a source mapping, policy, machine, or domain
history model. Those remain explicit adopter inputs. Formats still named
`private-v0` may change before a compatibility contract is published.

### Populate from a document without hiding the gaps

Structured rows are not the only possible source. The optional
`adapt_document_assertions` frontend accepts exact reading bytes, a capture
that quotes specific passages, and graph records proposed by the adopter. It
checks that every quoted passage occurs in the named text block and that every
record field points back to a captured assertion. It then emits the same
neutral population plan used by row adapters:

```python
import json

from malleus.compiler import adapt_document_assertions

compiled = adapt_document_assertions(
    reading_bytes=reading_bytes,
    capture_bytes=capture_bytes,
    capture_id="capture:inspection-note",
    plan_id="plan:inspection-note:1",
    contract_identity=effective_contract.identity,
    records=proposed_records,
    supersessions=[],
    valid_time={"kind": "INSTANT", "value": "2026-03-02T00:00:00Z"},
)
population_plan = json.loads(compiled.canonical_plan_bytes)
```

The adapter does not invent `proposed_records`, accept them, or write the
knowledge graph. The ordinary population compiler validates the emitted plan
against the selected ontology contract. Admission and replay remain separate.
Captured assertions stay retained ledger evidence rather than becoming graph
records.

The result also contains `canonical_census_bytes`. Its two independent axes
say which source blocks were reviewed and which captured assertions were fully,
partly, or not formalised. A quoted range that the ontology only models as one
number, for example, becomes a typed gap instead of disappearing.

The current minimal `source-assertion` profile preserves assertion modality in
the retained capture. It does not guarantee that modality is visible in an
ordinary graph query unless the adopter's ontology models it. The later full
history-profile contract must either require that qualification, reify the
claim, or provide a typed provenance join. Until then, do not present an
unqualified projected edge as proof that a source asserted it as fact.

### Trace an accepted record back to its source

`trace_population_record` is a read-only join over information already retained
by the public population path. Starting with one accepted graph-record ID, it
resolves the record history, accepted change set, canonical population plan,
selected domain-history profile, field derivations, source bytes, and evidence
bytes:

```python
from malleus.compiler import trace_population_record

trace = trace_population_record(
    history.replay(),
    "supplier-order-state:B:e7",
)

assert trace.history_profile.profile_id == "state-version"
assert trace.record_history.supersedes_record_id == (
    "supplier-order-state:B:e4"
)
quantity = next(
    item
    for item in trace.derivations
    if item["path"] == ("properties", "ordered_quantity")
)
assert quantity["locator"] == "row:1:quantity"
```

The function performs no I/O and changes neither the ledger nor the graph. It
recompiles the retained plan against the contract and accepted state that
preceded the change, then checks that the resulting operations, closures,
valid time, and supersession equal the accepted change set. Missing, ambiguous,
or inconsistent provenance returns `PopulationTraceRefusal`; it is never
guessed.

For the document adapter, the same trace reaches locator `asr:001` and the
exact retained capture containing its verbatim statement and `STATED`
modality. Interpreting that capture remains an adapter-level concern. The
generic trace exposes its exact bytes but does not turn the assertion into a
graph record.

This is an inspection view, not another persisted artifact or authority. It
works for changes that bind a neutral population plan and profile. Older or
manually composed change sets fail with `POPULATION_PLAN_NOT_BOUND`.

### Grow the ontology without starting a new history

A useful ontology will change. Starting a second ledger every time a project
adds a field would hide the connection between old and new knowledge. Malleus
can now record one narrow kind of ontology revision inside the same history.

The caller compiles the revised ontology, keeps the protocol machine and policy
unchanged, then asks the history to derive the revision:

```python
from malleus.compiler import (
    compile_linkml_contract,
    compose_partial_effective_contract,
)

current = history.replay()
revised = compile_linkml_contract(
    root_locator="my-domain",
    sources={
        "my-domain": revised_ontology_bytes,
        "linkml:types": linkml_types_bytes,
    },
)
revised_partial = compose_partial_effective_contract(
    validated_fact_set_sha256=revised.artifact.validated_fact_set_sha256,
    normative_profile=current.partial_contract.normative_profile,
)
revision = history.compose_contract_revision(
    revision_id="revision:catalog-v2",
    target_validated_contract_bytes=revised.artifact.artifact_bytes,
    target_partial_contract_bytes=revised_partial.canonical_bytes,
    reason="add the product category needed by retained gaps",
    issued_at="2026-09-03T00:00:00Z",
)
history.record_contract_revision(
    revision=revision,
    transaction_time="2026-09-03T00:00:00Z",
    actor_id="actor:maintainer",
)
```

The executor does not trust a label saying what changed. It compares the two
compiled fact sets and derives `ADD_CLASS`, `ADD_SLOT`, or `ADD_ENUM_VALUE`.
Those additions are admitted by the public `CONTRACT_REVISION_POLICY`. An
`ADD_IMPORT` remains a legal grammar term but the current policy refuses it.
Removing or changing an existing semantic fact also refuses.

The recorded revision contains the target contract, the exact ledger and graph
coordinates it follows, the derived changes, and a migration receipt. Replay
loads the old contract, reaches that event, validates the accepted graph under
the new contract, and continues. Later knowledge changes name the new contract
identity. Earlier records and change sets remain in the same ledger.

This is an additive revision path, not a general migration engine. It does not
rewrite old records, change the protocol machine, admit new imports, or decide
how an adopter should model domain history.

### Follow one fact through the system

The source material is deliberately ordinary. The warehouse scenario is a
controlled transcription of event `e27` in Table 1 of Dirk Fahland's 2022
chapter, [*Process Mining over Multiple Behavioral Dimensions with Event
Knowledge Graphs*](https://doi.org/10.1007/978-3-031-08848-3_9). One warehouse
record says that packing event `e27` handled order `O1` and items including
physical unit `X1`:

```json
{"activity":"Pack Shipment","actor":"R4","event_id":"e27","items":["X1","X2","Y1"],"order":"O1","time":"07-05 17:00"}
```

A [fixture manifest](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/manifest.json)
records that attribution. The JSONL encoding, separate inventory lookup,
selected row, synthetic year, and UTC interpretation are Malleus fixture
choices, not claims made by the source publication.

A separate inventory lookup says what `X1` is:

```text
inventory_unit_id,product_code
X1,X
```

The fixture explicitly selects event `e27`, order `O1`, and unit `X1`. Its
ontology says a `SalesOrder` has an order number, an `InventoryUnit` has a
product code, and `OrderContainsUnit` must point from the former to the latter.

After the proposed change is accepted and replayed, the graph contains exactly:

```text
SalesOrder("O1", order_number="O1")
InventoryUnit("X1", product_code="X")
OrderContainsUnit("contains:O1:X1", O1 -> X1)
```

The source also mentions `X2`, `Y1`, and event `e27`. They do not become graph
records because the mapping does not propose them. Malleus does not turn every
value it sees into a node. In this slice, `e27` remains retained evidence.

### What we built to make that happen

1. Malleus retains and hashes the exact controlled inputs. The compiled contract
   records the identity and supported meaning of the full ontology dependency
   set; it does not copy every imported ontology file into one artifact.
2. The LinkML frontend compiles the selected ontology meaning into neutral
   facts and a structural view that reloads without LinkML or the original
   ontology files.
3. Separate versioned and hashed machine, policy, and mapping artifacts declare
   the example's event names, order, receipt identities, verdict mapping,
   source selection, and three graph operations.
4. The executor creates one immutable `KnowledgeChangeSet`. It binds the
   contract, retained source and evidence identities, the anchored history and
   empty prior accepted graph, three ordered operations, valid time, and its own
   digest.
5. One JSONL history records 20 bootstrap retention and registration events,
   followed by the change set, its proposal, two fixture-supplied check
   receipts, and the final verdict. That is 25 events.
6. Before replacing ledger bytes, candidate replay validates every event and
   successfully stages the accepted change against a fresh graph. A failed
   append changes neither retained history nor accepted state.

The two supplied receipts say that source integrity and structural conformance
are `SATISFIED`. The machine verifies their expected identities and outcome
vocabulary. The identified policy maps `SATISFIED` to `ACCEPT`, `VIOLATED` to
`REJECT`, and `UNKNOWN` to `DEFER`.

This first slice does not execute the check implementations or retain them as
artifacts. The fixture supplies their outcomes, while source and structural
validation run elsewhere in Python. Python also still owns mapping and time
interpretation, machine opcode semantics, knowledge-change validation, and
graph projection. Those are explicit limits, not hidden claims of a
language-neutral compiler.

### Inspect the evidence

The prose above is only a guide. These are the exact committed inputs and
checks behind it:

| Stage | Exact bytes | What they establish |
| --- | --- | --- |
| Source | [manifest](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/manifest.json), [warehouse JSONL](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/sources/warehouse.jsonl), [inventory CSV](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/sources/inventory-units.csv), [selection](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/configuration/ret-010-selection.json), [time context](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/configuration/time-context.json) | The cited source row, lookup value, selected occurrence, and explicit time interpretation. |
| Domain meaning | [Small Shop ontology](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/input/tbox/small-shop.yaml) | The selected classes, slots, ranges, inheritance, and relation value. |
| Executable contracts | [mapping](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/mapping.json), [protocol machine](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/machine.json), [policy](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/policy.json) | The source selection and operations, legal event transitions, required receipts, and verdict mapping. |
| Independent expectation | [hand-authored answer key](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment/oracle/ret-000-ret-010.json) | The expected logical entities, relation, and valid time. It is not compiler input. |
| Execution | [runner](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/ret010.py), [end-to-end tests](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/test_vertical.py) | Compilation, admission, atomic refusal, replay, and oracle comparison. |
| Verification | [input report](../conformance/contract_compiler/v0/evidence/CC-021.json), [answer-key report](../conformance/contract_compiler/v0/evidence/CC-022.json), [completion report](../conformance/contract_compiler/v0/evidence/CC-R11.json) | The independently recorded boundaries and exact file identities used by the completed experiment. |

The compiler emits 735 canonical neutral facts for the retained ontology
closure. These are three representative facts, shown without translating them
back into LinkML:

```json
[
  {"object":"https://malleus.dev/schema/Entity","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://malleus.dev/schema/small-shop-fulfilment/SalesOrder"},
  {"object":"https://malleus.dev/schema/Relation","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://malleus.dev/schema/small-shop-fulfilment/OrderContainsUnit"},
  {"object":"ORDER_CONTAINS_UNIT","predicate":"https://malleus.dev/contract-facts/enumValue","subject":"https://malleus.dev/schema/small-shop-fulfilment/ShopRelationKind"}
]
```

The complete validated fact set has identity
`sha256:80730e44e1bc1efd878cd2723e3af950d409defb68a629deb8c55515c6336f6c`.
The composed contract has the different identity
`sha256:ed170fd1434eb247c2b098a136f2b050021f9d1677d0477be9a69be5d6b63a17`
because it also binds the selected machine, policy, and history contract. This
is the distinction between the ontology-derived structural meaning and the
whole executable agreement for this run.

The generated ledger is intentionally not checked in. It is 280 KB because it
retains source and compiled artifact bytes. Its readable lifecycle is:

| Event numbers | Contents |
| --- | --- |
| 1-4 | Retain the validated contract, composed contract, history binding, and mapping. The composed contract contains the machine and policy bytes. |
| 5-20 | For each of the eight exact source members, register its source artifact and then the retained source. |
| 21 | Retain knowledge change `sha256:cc5ce1cf6f9521f5299fbc9a981f6dba6949afaabd3730b2f81037b51c5912af`. |
| 22 | Propose that exact change. |
| 23-24 | Record the two fixture-supplied `SATISFIED` check receipts. |
| 25 | Record the `ACCEPT` verdict. The ledger head is `sha256:3e07988bafd28a481c5eece5bfdad533ddbb63c93e862b9192944e04c8af3574`. |

The [recorded canonical receipt](../research/ontology_driven_kg_realization/experiments/small_shop/pareto/ret-010-research-receipt.json)
is the compact evidence snapshot. It is an exact result of this private
research experiment, not a supported API, stable schema, or compatibility
promise. Its query result is:

```json
{
  "entities": [
    {"id": "O1", "order_number": "O1", "type": "SalesOrder"},
    {"id": "X1", "product_code": "X", "type": "InventoryUnit"}
  ],
  "relations": [
    {"key": "contains:O1:X1", "relation_type": "ORDER_CONTAINS_UNIT", "source_id": "O1", "target_id": "X1", "type": "OrderContainsUnit"}
  ]
}
```

Install the development dependencies, generate the complete history, and run
the exact receipt check:

```bash
pip install -e '.[dev]'
python -m research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 --ledger build/small-shop-ret010.jsonl
python -m pytest -q research/ontology_driven_kg_realization/experiments/small_shop/pareto/test_vertical.py::test_recorded_research_receipt_regenerates_from_the_exact_history
```

Running the module again reopens the same ledger and prints the same receipt.
The test regenerates the result independently and compares its bytes exactly.

### Try to break it

The negative tests copy the fixture, alter one input, and run the same path. For
example, appending one space to the warehouse source changes its digest. The
run refuses with `SOURCE_DIGEST_MISMATCH` before creating a ledger or partial
graph. Other cases cover a missing source, wrong selected event or item,
ambiguous inventory lookup, and ambiguous source time:

```bash
python -m pytest -q research/ontology_driven_kg_realization/experiments/small_shop/pareto/test_vertical.py -k invalid_source_bundle
```

### The delete-and-rebuild test

The test discards the derived graph and removes the ambient fixture, machine,
policy, and mapping files. It reopens the JSONL history with the current Python
runtime, reloads the compiled contract and other retained artifacts, and
reconstructs the same graph and byte-identical receipt.

So "from the ledger alone" means replay does not reread the ambient fixture,
machine, policy, or mapping files. It still needs an implementation of the
declared contracts and its runtime dependencies, which is Python today. Replay
loads the compiled facts; it does not rerun LinkML compilation.

This proves deterministic derivation under the named inputs and policy. It does
not prove that the warehouse statement is true in the world. Evidence,
acceptance, and truth remain different claims.

### Correct one fact without rewriting the past

The initial proof creates a graph. The next question is harder: what should
happen when a source later says something different?

If software overwrites `1` with `2`, it can show the selected latest value but
the path that produced it is gone. If it merely stores both values, the graph
appears to claim that both are current. The bounded correction proof does
neither. It keeps the earlier state in the history, records exactly what
replaced it, and derives a current graph containing only the replacement.

The controlled source contains two rows from the Small Shop example:

```json
{"event_id":"e4","product_code":"Y","quantity":1,"supplier_order_id":"B"}
{"event_id":"e7","product_code":"Y","quantity":2,"supplier_order_id":"B"}
```

These are controlled transcriptions of supplier order `B` in Table 1 of the
same [Fahland chapter](https://doi.org/10.1007/978-3-031-08848-3_9). The
publication establishes their order, not timestamps, so the fixture preserves
only `e4` before `e7`. It does not invent dates.

The run starts from an empty graph and accepts three knowledge changes into one
58-event history:

1. Create the existing `O1`, `X1`, and `OrderContainsUnit(O1, X1)` baseline.
2. Record supplier order `B`, product `Y`, quantity `1`, from `e4`.
3. Record supplier order `B`, product `Y`, quantity `2`, from `e7`, explicitly
   superseding the `e4` record.

The current graph is therefore:

```text
SalesOrder("O1", order_number="O1")
InventoryUnit("X1", product_code="X")
OrderContainsUnit("contains:O1:X1", O1 -> X1)
SupplierOrderState("supplier-order-state:B:e7", B, Y, quantity=2)
```

The old `B@e4` state has not disappeared. The history records that it began at
`e4`, ended at `e7`, and was replaced by `B@e7`. A query for the graph
immediately after the accepted `e4` change returns quantity `1`; the current
graph returns quantity `2`.

This run closes a gap in the first proof. For every proposed change, an exact
source-and-mapping check reloads the retained source row and mapping, derives
the expected operation, valid-time label, and supersession, then compares that
result with the sealed knowledge change. A structurally legal substitution of
quantity `999` for source quantity `1` refuses. A separate structural check
proves that the exact operations apply to the prior accepted state. Both checks
name the digest of the exact Python executor that ran them, and their canonical
receipts are retained before the policy can accept the change.

Receipt retention, proposal, checks, verdict, and graph application form one
failure-atomic ledger batch for each change. If any later step refuses, neither
the receipts nor a partial change remains in the history. Reopening the JSONL
history regenerates the same receipt, explanation, and graph bytes without
reading the ambient source, mapping, machine, policy, or check files.

The answer key stays independent. It states by hand that `B@e4` is replaced by
`B@e7` and that `O1`, `X1`, and their relation remain unchanged. Runtime does
not read it. Tests compare the completed replay with it afterward.

Run the complete bounded proof with one command:

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.correction.run --output build/small-shop-correction
```

The command writes `history.jsonl`, `receipt.json`, `graph.json`, and
`explanation.json`. The generated history is intentionally not checked in;
the three smaller canonical evidence files are.

| Stage | Exact bytes | What they establish |
| --- | --- | --- |
| Source | [manifest](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/manifest.json), [e4/e7 JSONL](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl), [selection](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/configuration/shop-supplier-order-correction-selection.json) | Exact source bytes, source order, zero-based row selection, and bounded attribution. |
| Domain meaning | [ontology extension](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/tbox/small-shop-correction.yaml) | The typed `SupplierOrderState` shape added to the existing Small Shop vocabulary. |
| Executable contracts | [mapping](../research/ontology_driven_kg_realization/experiments/small_shop/correction/mapping.json), [machine](../research/ontology_driven_kg_realization/experiments/small_shop/correction/machine.json), [policy](../research/ontology_driven_kg_realization/experiments/small_shop/correction/policy.json), [run program](../research/ontology_driven_kg_realization/experiments/small_shop/correction/run.json) | Exact source selection, operations, lifecycle, required checks, and verdict rule. |
| Executed checks | [source-and-mapping contract](../research/ontology_driven_kg_realization/experiments/small_shop/correction/checks/source-mapping-conformance.json), [structural contract](../research/ontology_driven_kg_realization/experiments/small_shop/correction/checks/structural-conformance.json), [executor](../research/ontology_driven_kg_realization/experiments/small_shop/correction/run.py) | The named check semantics and exact fixture entrypoint bytes used to produce retained receipts. |
| Independent expectation | [hand-authored answer key](../research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/oracle/shop-supplier-order-correction.json) | Expected current state, history, supersession, and preserved baseline. It is never execution input. |
| Recorded result | [receipt](../research/ontology_driven_kg_realization/experiments/small_shop/correction/evidence/receipt.json), [current graph](../research/ontology_driven_kg_realization/experiments/small_shop/correction/evidence/graph.json), [explanation](../research/ontology_driven_kg_realization/experiments/small_shop/correction/evidence/explanation.json), [tests](../research/ontology_driven_kg_realization/experiments/small_shop/correction/test_correction_vertical.py) | The exact replay result, its provenance chain, and the positive and refusal cases. |

The compiled ontology fact set has identity
`sha256:0af9eb01495af3c7ed063cb8ca340b63b475eb72feeb2f81fe9be48720fd515e`.
The whole effective contract, including machine and policy, has identity
`sha256:5710e7464c0b737c6275bbf662bf797c920f0eb3d169341dde5734a5eab3669a`.
The 58-event ledger ends at
`sha256:01d1ea5ab6276fe878a71fa67922bdf10f032d9dd3c6dc22f9f15cc2faf1c4aa`.
The current graph has digest
`sha256:52652ddb7425562e36cd7f430a3c483b761067320a4eba30b8195fabcebe1645`.

This is still a research-local proof, not a stable public interface. The
fixture runner contains substantial low-level protocol assembly that should
become a generic composer only after another consumer proves the right seam.
The run does not provide a general mapping language or a general valid-time
query. Its graph-at-change result means the state immediately after one
accepted change. It also excludes Semantic Re-entry, demand reasoning,
actions, effects, invoice correction, and Event-node projection. Full graph
snapshots per accepted change are adequate for this small proof but need a
delta or prefix-replay strategy before large histories. The retained executor
identity covers the fixture entrypoint, not the imported Core, RET-010, Python,
or environment dependency closure. A portable executor closure remains future
work. This fixture aligns transition-level and record-level supersession, but
Malleus has not yet selected a general law saying whether those two relations
must always align.

### Small Shop is the proving ground, not the protocol

This example selects Malleus's optional semantic-history profile. The reusable
boundary and the fixture choices remain separate:

| Reusable boundary exercised here | Small Shop choice |
| --- | --- |
| Retain selected inputs and bind declared sources, artifacts, and base coordinates by identity. | Warehouse JSONL, inventory CSV, and the selected `e27` row. |
| Compile one frontend into a neutral structural contract. | LinkML 1.11.1 and the Small Shop ontology subset. |
| Interpret versioned and hashed machine and policy data. | Artifact and source registration plus proposal, check, and verdict event kinds; two supplied receipt identities; and a three-outcome verdict mapping. |
| Propose one immutable knowledge change. | Create `O1`, create `X1`, then relate them. |
| Admit through one append-only history. | The fixture's actor, record names, lifecycle values, and valid time. |
| Derive accepted state only by replay. | The typed `SalesOrder`, `InventoryUnit`, and `OrderContainsUnit` graph. |

The generic machine and history code does not know what an order, inventory
unit, or warehouse event is. Those words and values live in the fixture's
ontology and versioned, hashed artifacts.

The correction support follows the same boundary. Generic history code knows
only that one typed record may replace another compatible typed record under
one shared valid-time kind. This fixture separately binds its `ORDER_ONLY`
labels to source order. `SupplierOrderState`, `B`, `Y`, `e4`, `e7`, and their
source mapping remain fixture data. Another adopter can use the same history
rule with different nouns, sources, checks, mappings, and graph shape.

Another domain supplies its own ontology, sources, mapping, checks, policy, and
representation. A future frontend can replace LinkML only if conformance proves
that it produces the same neutral meaning. This slice designs that seam but
does not yet demonstrate a second frontend or language. An adopter may also
omit semantic history, but then it cannot claim the replayable accepted-state
provenance demonstrated here.

### What this proves, and what it does not

The recorded initial-population completion gate contains 140 focused passing tests, strict Sphinx
HTML, doctest, and link checking, and an independent clean audit. It proves that
the selected pieces compose for one initial, create-only population case. It
also proves tested refusals are atomic and that the derived graph is disposable.

The follow-on correction seam passes 208 focused tests across the frozen
initial proof, correction inputs and answer key, generic record history, exact
source-and-mapping checks, atomic refusal, and reopen. It proves one bounded
record correction without changing the frozen initial fixture bytes.

This was a focused research gate, not a release gate. The generic compiler and
history executor are now packaged behind a public Python facade, and contract
compilation has an installed command. Still missing are stable wire contracts,
a general mapping contract, broad ontology support, a supported interface for
executed and retained check implementations, general update and correction
behavior, external effects and observation, public bitemporal queries,
Semantic Re-entry, and a second-language interpreter proving cross-language
parity.

See the [technical compiler notes](contract_compiler/index.md) and
[implementation status](IMPLEMENTATION_STATUS.md) for the exact boundary.

## Documentation map

```{toctree}
:maxdepth: 2

ADOPTION_GUIDE
SMALL_SHOP_WALKTHROUGH
ARCHITECTURE
ASSENT_PLAN
ASSENT_PROTOCOL
DELIMITATIONS
EFFECT_PROTOCOL
IMPLEMENTATION_STATUS
KNOWLEDGE_GRAPH_PROTOCOL
ONTOLOGY_PROTOCOL
PRINCIPLES
RECIPES
RECON_CONTRACT
contract_compiler/index
reference/index
```

The repository validates these public pages locally. Site deployment and a
release remain separate. The executable example below proves the documentation
toolchain itself, not the compiler runtime.

```{doctest}
>>> {"manifest": "validated"}["manifest"]
'validated'
```

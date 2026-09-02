# Malleus documentation

Malleus is a protocol for making semantic change explicit. It separates the
meaning a domain declares, the change someone proposes, the checks applied to
that change, the decision to accept or refuse it, and the knowledge graph
derived from the accepted history.

Adopters do not have to use one fixed software stack. They can select the
profiles they need, replace implementations behind the same contracts, or stop
before semantic history entirely. Start with the
[protocol boundary taxonomy](protocol-boundary-taxonomy) for those boundaries.

## First compiler-to-ledger-to-knowledge-graph proof

> **Status:** Working research milestone, 2 September 2026.
> The path is executable and tested in this repository.
> It is not yet a stable public API. It is not an installed command,
> file-format promise, package feature, or release.

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
| 25 | Record the `ACCEPT` verdict. The ledger head is `sha256:3d055403ccbe39266e89c44cd49b63f14a909d1c6ca4eb65fe7afa38b7912bad`. |

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

Another domain supplies its own ontology, sources, mapping, checks, policy, and
representation. A future frontend can replace LinkML only if conformance proves
that it produces the same neutral meaning. This slice designs that seam but
does not yet demonstrate a second frontend or language. An adopter may also
omit semantic history, but then it cannot claim the replayable accepted-state
provenance demonstrated here.

### What this proves, and what it does not

The recorded completion gate contains 140 focused passing tests, strict Sphinx
HTML, doctest, and link checking, and an independent clean audit. It proves that
the selected pieces compose for one initial, create-only population case. It
also proves tested refusals are atomic and that the derived graph is disposable.

This was a focused research gate, not a release gate. The full repository and
package suites were deliberately outside the milestone. Still missing are a
supported public compiler API and command, a general mapping contract, broad
ontology support, executed and retained check implementations, update and
correction behavior, external effects and observation, public bitemporal
queries, Semantic Re-entry, and a second-language interpreter proving
cross-language parity.

See the [technical compiler notes](contract_compiler/index.md) and
[implementation status](IMPLEMENTATION_STATUS.md) for the exact boundary.

## Documentation map

```{toctree}
:maxdepth: 2

ADOPTION_GUIDE
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

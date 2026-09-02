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
complete.** Complete here means one controlled example crosses the selected
source-to-history-to-graph boundaries and can rebuild its result from retained
history. It does not mean the general Malleus compiler is finished.

In plain English, the pieces have these jobs:

| Piece | Job |
| --- | --- |
| Ontology | Defines the words a domain may use and the shape of valid records. |
| Compiler | Turns that declared meaning into an exact, neutral contract a machine can execute without guessing. |
| Knowledge change | States one proposed change to domain knowledge as an immutable value. |
| Ledger | Keeps the evidence, proposal, checks, and decision in one append-only history. |
| Knowledge graph | Presents the current accepted view rebuilt from that history. |

### The Small Shop example

The source material is deliberately ordinary. One warehouse record says that
packing event `e27` handled order `O1` and items including physical unit `X1`:

```json
{"activity":"Pack Shipment","actor":"R4","event_id":"e27","items":["X1","X2","Y1"],"order":"O1","time":"07-05 17:00"}
```

A separate inventory lookup says what `X1` is:

```text
inventory_unit_id,product_code
X1,X
```

The fixture's explicit selection asks for order `O1` and unit `X1` from that
warehouse record. Its ontology declares that:

- a `SalesOrder` has an order number;
- an `InventoryUnit` has a product code;
- `OrderContainsUnit` must point from a `SalesOrder` to an `InventoryUnit` and
  must use the relation type `ORDER_CONTAINS_UNIT`.

After admission and replay, the graph contains exactly:

```text
SalesOrder("O1", order_number="O1")
InventoryUnit("X1", product_code="X")
OrderContainsUnit("contains:O1:X1", O1 -> X1)
```

This precision matters. The source also mentions `X2`, `Y1`, and event `e27`,
but the selected mapping does not ask Malleus to create them. The compiler does
not guess that every source value should become a graph node. In this first
case, `e27` remains retained evidence rather than an accepted Event entity.

### What happened between source and graph

1. Malleus retained the exact source and ontology bytes and computed their
   identities.
2. A LinkML frontend translated the ontology into a neutral contract
   representation, canonical facts, and a reloadable structural view.
3. Identified machine, policy, and mapping data described the event sequence,
   required checks, decision rule, source selection, and graph operations.
4. The executor produced one immutable `KnowledgeChangeSet` bound to those
   inputs and to an empty accepted base.
5. One JSONL ledger recorded the retained artifacts, source registrations,
   proposal, check results, acceptance decision, and atomic application.
6. Replay folded that accepted change into a fresh graph and returned the three
   records shown above.

Python executes this measured path, but the example's protocol names,
transitions, checks, verdict mapping, and source mapping live in identified
data. The generic history layer has no Small Shop vocabulary and receives no
graph writer. Some structural contract admission still lives in Python, so the
repository does not yet claim that every portable rule has moved into an
interpreter-neutral artifact.

### Why the ledger matters

A saved graph can tell us what it contains. It cannot, by itself, prove which
source bytes, ontology, mapping, checks, or decision produced that state.

This run records 25 immutable semantic and protocol events. The test then
throws away the derived graph, reopens the retained JSONL history without
consulting ambient fixture, machine, policy, or mapping files, and reconstructs
the same graph and byte-identical receipt. Tested refusals leave both the prior
history and accepted graph unchanged.

That proves deterministic derivation under the named inputs and policy. It does
not prove that the warehouse statement is true in the world. Evidence,
acceptance, and truth remain different claims.

### What is reusable and what belongs to the fixture

This example selects Malleus's optional semantic-history profile. The reusable
boundary and the Small Shop choices remain separate:

| Reusable boundary proved here | Small Shop choice |
| --- | --- |
| Retain exact inputs and their identities. | Warehouse JSONL, inventory CSV, and the selected `e27` row. |
| Compile an adapter's output into a neutral contract. | LinkML 1.11.1 and the Small Shop ontology subset. |
| Execute identified machine and policy artifacts. | Two required fixture checks and a strict three-outcome verdict mapping. |
| Propose one immutable knowledge change. | Create `O1`, create `X1`, then relate them. |
| Admit through one append-only history. | The fixture's actors, record names, and exact lifecycle values. |
| Derive accepted state only by replay. | The typed `SalesOrder`, `InventoryUnit`, and `OrderContainsUnit` graph. |

Another domain may use different sources, ontology terms, mapping, checks,
policy, and graph representation. Another frontend may replace LinkML if it
produces the same neutral contract. An adopter may also omit semantic history,
but then it cannot claim the replayable accepted-state provenance demonstrated
here.

### Evidence and current limits

The recorded completion gate contains 140 focused passing tests, strict Sphinx
HTML, doctest, and link checking, and an independent clean audit. A fresh run
produces the graph above, and a second run reproduces it from the ledger alone.
See the [technical compiler notes](contract_compiler/index.md) and
[implementation status](IMPLEMENTATION_STATUS.md) for the exact boundary.

This was a focused research gate, not a release gate. The full repository and
package suites were deliberately outside the milestone. Still missing are a
supported public compiler API and command, a general mapping contract, broad
ontology support, update and correction behavior, external effects and
observation, public bitemporal queries, Semantic Re-entry, and a second-language
interpreter proving cross-language parity.

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

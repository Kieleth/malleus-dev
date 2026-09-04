# Full Small Shop public-path conformance run

This fixture runs the complete five-stage Small Shop dataset through the public
`malleus.compiler` facade. It is the integration proof for the population work,
not a new protocol layer.

The useful simplification is that the domain choices are visible as data. Five
small canonical population plans say which source bytes support which records,
where each field came from, which history profile applies, and what the `e7`
record supersedes. One runner executes those plans. It does not contain a
second source mapper or import the older research runners.

## What crosses the path

| Input or mechanism | This fixture uses |
| --- | --- |
| Domain ontology | Small Shop base contract, then one additive revision adding supplier orders, invoices, payments, and settlement relations |
| Source bytes | Warehouse JSONL, inventory CSV, invoice CSV, payment JSONL, and supplier-order JSONL |
| Population | Five exact neutral plans in [`plans/`](plans/) |
| Domain history choice | The shipped minimal `state-version` profile |
| Governance | The shipped declarative machine and required-check policy |
| History | One append-only `KnowledgeChangeHistory` containing five accepted changes and one contract revision |
| Projection | Reopen and replay derive the current `KnowledgeGraph` |
| Explanation | `trace_population_record` verifies every current and superseded record back to its retained plan, derivations, sources, and evidence |

Run it from the repository root:

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.public_population.run \
  --output build/small-shop-public-population
```

The command writes `history.jsonl` and `evidence.json`. Running it again reopens
the same history and emits byte-identical evidence without changing the ledger.
The committed [`evidence.json`](evidence.json) is the expected result of a fresh
run.

The recorded result contains five accepted knowledge changes, one ontology
revision, ten historical records, and nine current graph records. Supplier
order `B@e4` remains in history with quantity `1`; `B@e7` supersedes it and is
the only current supplier-order state, with quantity `2`. The current graph
also contains order `O1`, inventory unit `X1`, invoices `I1` and `I2`, payment
`P1`, and their three typed relations.

## Exact boundary

This is a conformance fixture. The plans are adopter-authored and their format
is still private. The run proves deterministic compilation, admission,
contract revision, replay, query, and provenance trace for this selected
state-version model. It does not claim a general mapping language, a universal
domain-history model, Event population, Semantic Re-entry, external effects,
or a stable wire format.

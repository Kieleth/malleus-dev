# Full Small Shop public-path conformance run

This fixture runs the complete five-stage Small Shop dataset through the public
`malleus.compiler` facade. It is the integration proof for the population work,
not a new protocol layer.

For a source-to-answer explanation and an executable read-only query, start
with the [Small Shop walkthrough](../../../../../docs/SMALL_SHOP_WALKTHROUGH.md).
It separates this five-plan run from the companion controls for reports without
correction, unstated valid time and retained capture gaps.

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
| Domain history choice | The shipped full `state-version` profile |
| Governance | The shipped declarative machine and the required-check policy, whose one check Core runs itself |
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

The profile makes the fixture's history semantics explicit: the accepted unit
is a state version, valid time is domain time, corrections supersede prior
versions, and replay selects current non-superseded records. Its genesis scope
is the declared source set, not a claim that the first change describes the
whole shop.

## The check the policy requires, and the one that was removed

`pareto/policy.json` requires one check contract, `structural-conformance`, a
`malleus.check-contract/v1` `CORE_BUILTIN` document at
`sha256:4cef2ab7e63c87ff3b3290026b6c0b1335b01cea18e30b353adfaf6ce52b8bd9`
naming `malleus.core.operations-apply-atomically` version `1`. The runner
retains that document at bootstrap and then hands Core the change set:
`check_and_admit_change_set` resolves the required contract against what this
history retains, runs the builtin over the state the change would produce,
mints the receipt and writes `CHANGE_PROPOSED`, `CHECK_RECORDED` and
`VERDICT_RECORDED`. No outcome is written here any more.

The policy required a second check before this run, `retained-source-integrity`
at `sha256:8208a29397002098d74498c4956f5a86d10526f8e4cf806feae4fe769074c19d`.
It is gone. That identity matched no file in the repository: no contract
document, no rule layer, nothing Core or anyone else could have run. The
`CHECK_RECORDED` event this runner wrote for it carried `outcome: SATISFIED`
as a literal, so it attested a check that never existed. Removing it removes an
attestation, not a guarantee. `pareto/policy.json` moved from
`sha256:c0ec653f...` to `sha256:433f2f9b...` with it, and `pareto/mapping.json`
from `sha256:4e8851c5...` to `sha256:ba4291a2...`, which is why every plan in
[`plans/`](plans/) was re-cut: the partial effective contract each plan pins is
composed from that policy, and `ret010.json` pins the mapping as evidence.

## Exact boundary

This is a conformance fixture. The plans are adopter-authored and their format
is still private. The run proves deterministic compilation, admission,
contract revision, replay, query, and provenance trace for this selected
state-version model. It does not claim a general mapping language, a universal
domain-history model, Event population, Semantic Re-entry, external effects,
or a stable wire format.

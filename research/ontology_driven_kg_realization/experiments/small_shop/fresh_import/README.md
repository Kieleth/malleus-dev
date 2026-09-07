# Fresh supplier-file import

## Contract, before implementation

This is a `CONFORMANCE_FIXTURE`, not new Core policy. It tests whether a
Shop-owned adapter can turn a fresh supplier file into a neutral population
plan and use the public compiler, default structural admission, ledger,
reopen, graph queries, and source trace without changing Core.

The new file is synthetic. Orders SYN-C and SYN-D are invented test data,
not additional observations from the published retailer example. The two
rows state quantities 3 and 5. They state no domain date or ordering.

The `ADOPTER_CHOICE` is recorded in mapping.json: each row describes one
SupplierOrderState, identity comes from its unique source occurrence, fields
copy without normalization, and valid time is explicitly NONE_STATED. This
import adds records; it never infers a replacement from a repeated order ID.
The selected optional profile is state-version with Core's default structural
admission bundle. Without history, there is no claim about accepted replay.

The adapter consumes exact JSONL bytes and supplied source, plan and contract
identities. It produces the existing private-v0 neutral plan. Malformed JSON,
duplicate keys or occurrence IDs, missing/extra fields, empty identifiers, and
non-integer or negative quantities refuse as SupplierImportRefusal before any
retention. These are this file format's rules, not universal supplier rules.
All nonempty lines are rows, numbered from zero for row:N:field locators.

The coordinator retains exact source, mapping and adapter bytes, compiles and
prepares the plan, then uses Core admission. Preparation and admission are
separate transactions. A stale preparation refuses without further writes;
already successful evidence retention is not rolled back. Replay alone derives
accepted state. The pure mapper receives no history or graph handle.

Dependency projection:

```text
supplier adapter consumes synthetic supplier rows
supplier adapter governedBy mapping.json
supplier adapter produces PopulationPlan
PopulationPlan governedBy state-version
public Core admission consumes PopulationPlan and retained inputs
replayed graph derivedFrom KnowledgeChangeHistory
source trace derivedFrom replayed record and retained plan
fresh-import tests evidence the complete composition
```

The smallest proof imports both rows after the complete existing Shop run,
reopens from a copied ledger alone, checks quantities and exact source locators,
and proves all previous records unchanged. Independent malformed-input and
stale-state tests prove refusal at the stated boundaries. A second run must
reproduce the same ledger and report bytes.

Excluded: generic mapping DSL, schema changes, source truth, supplier effects,
automatic correction, Semantic Re-entry, release/version changes, and an
independently replaceable adapter claim. Another implementation would need to
produce the same plan and pass these cases before replaceability is claimed.

## Run and inspect

From this repository's configured environment:

```bash
python -m research.ontology_driven_kg_realization.experiments.small_shop.fresh_import.run --output build/small-shop-fresh-import
```

The output directory must not already exist. `shop/history.jsonl` is the one
history: it first records the original five Shop changes and its contract
revision, then the new two-row import as a sixth change. `shop/evidence.json`
is the preserved pre-import report. `evidence.json` reports the extended
history, row counts, source digest, quantities and every field locator.

The IDs `supplier-import:synthetic%3Areceipt%3AC` and
`supplier-import:synthetic%3Areceipt%3AD` encode the occurrence strings without
normalizing them. Repeated occurrence IDs refuse; repeated supplier-order IDs
do not mean supersession. Blank JSONL lines do not count as rows.

Read the new records using the same public interface as any adopter:

```python
from pathlib import Path
from malleus.compiler import KnowledgeChangeHistory, trace_population_record

replay = KnowledgeChangeHistory.reopen(
    Path("build/small-shop-fresh-import/shop/history.jsonl")
).replay()
print(replay.graph.query("SupplierOrderState", supplier_order_id="SYN-C"))
trace = trace_population_record(replay, "supplier-import:synthetic%3Areceipt%3AC")
print(trace.derivations)
print(trace.sources[0].content.decode("utf-8"))
```

The expected quantity for SYN-C is 3. Its quantity locator is
`row:0:ordered_quantity`. SYN-D has quantity 5 at `row:1:ordered_quantity`.
The trace retains the complete source file, exact mapping and adapter bytes,
not a reconstructed imitation of the input.

This slice closes initial fresh-file import only. Later work can add an
explicit supplier-correction contract, another source format, or an external
observer when a real consumer requires them. None runs as an implicit fallback.

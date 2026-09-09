# Shipment explanation, evidence before verdict

Status: implemented Shop-only read-side extension, built tests first. It does not change
the recorded population, the ontology, the selected admission policy, or Core.

The question is why O2 waited for payment. The retained section 1 passages give
the author's explanation and the rule of at most one unpaid invoice. The graph
provides the separate creation, receipt, clearing, packing and shipping records.
These are different evidence: neither chronology nor co-participation proves
causation, and an absent clearing record does not prove an unpaid balance.

The smallest useful observation compares the accepted import checkpoints after
e28 and e30, and the final graph. These are ledger reconstruction positions,
not inferred business times. Read them with the existing public
`KnowledgeHistoryReplay.graph_at_change`, without writing or cropping a ledger.
All context remains the retained source commentary, not knowledge claimed to
have been available at those business times.

Reuse the exact connected history, retained mapping, public graph queries and
record trace. A Shop read specification binds the context bytes, selected order
scope and numeric rule. The invoice inventory comes from the retained invoice
creation rows; missing records or links cannot shrink it into a passing count.
Clearance is evidence of the recorded clearing occurrence, not a permanent
zero balance. Actual shipment eligibility remains undetermined without a
complete customer account and explicit invoice status evidence.

The report exposes a lower/upper bound check over explicit invoice statuses.
Only separately labeled synthetic inputs exercise SATISFIED and VIOLATED.
The real source supplies no unpaid-status snapshot, so it must not receive
either verdict by default. A missing customer identifier is preserved, not
filled with an invented party. No payment or invoice amount is invented.

Tests must cover both checkpoints, reopen, exact source and rule identities,
missing invoice/receipt/link evidence, wrong-invoice correspondence, duplicate
status inputs, unknown scope, and unchanged accepted history and graph. A
supplier-only earlier update must not change the invoice assessment. Synthetic
damaged read views are test controls, never replacement source histories.

The earlier Prolog shipment fixture checks unit exclusivity at admission. This
reader checks an explicit count bound and evidence availability, so it does not
reuse that different rule, call its result authorization, or add a rule engine.
No Event ordering model, action execution, universal projection contract,
external integration, new dependency, push or release is part of this slice.

## What the reader now explains

| Accepted import checkpoint | Recorded clearance | What the rule check can conclude |
|---|---|---|
| After e28, O1's shipment row | No clearing occurrence yet for I1 or I2 | Cannot determine the unpaid count. No clearing row is not an unpaid balance. |
| After e30, the clearing row | P1 is connected to clearing both I1 and I2; its receipt is e29 | The two clearings are represented. The complete customer account is still not supplied. |
| Final graph | Both clearings remain; O2 is packed at e33 and shipped at e34 | The source's explanation and its supporting records are inspectable, not independently proven causal or authorized. |

The read report quotes the retained shared-customer, shipment-rule and delay
passages with their exact source digest and locators. It joins invoices to their
orders, P1 to the two invoices, and O2 to X3/Y2 and its packing/shipping records.
The `gaps` array names absent or mismatched graph evidence only. Even when that
array is empty, `account_completeness` stays `NOT_ESTABLISHED` and the unpaid
limit remains `CANNOT_DETERMINE`. Known clearance is not a claim that an invoice
stays paid forever or that no other customer invoice exists.

`source_witnesses` exposes the invoice-ownership derivations. Each other reported
occurrence is also a public trace target. For example, trace
`participation:e30:invoice:I2` to inspect the clearing's exact source fields:

```python
from malleus.compiler import KnowledgeChangeHistory, trace_population_record

replayed = KnowledgeChangeHistory.reopen("/tmp/shop-connected-history.jsonl").replay()
trace = trace_population_record(replayed, "participation:e30:invoice:I2")
for derivation in trace.derivations:
    print(dict(derivation))
```

## Run and inspect

Use the existing configured repository environment. Create a fresh history with
the connected runner, then read three checkpoints. The reader never writes it:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run /tmp/shop-connected-history.jsonl
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.shipment_explanation /tmp/shop-connected-history.jsonl --at-occurrence e28
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.shipment_explanation /tmp/shop-connected-history.jsonl --at-occurrence e30
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.shipment_explanation /tmp/shop-connected-history.jsonl
```

The original producer's `account.shipment_eligibility = NOT_EVALUATED` stays
frozen. This separate reader performs the bounded evidence check, binds its own
specification and implementation, and reports the result separately. Its
[receipt](shipment_explanation_receipt.json) identifies the exact three report
digests and unchanged history. No historical receipt was rewritten.

## What remains

This closes the source-backed payment explanation, not the whole chapter's
behavioral analysis. A stronger eligibility verdict needs an explicitly bounded
customer invoice inventory and status evidence at a declared business checkpoint.
The source does not supply that, so it is an evidence requirement, not a Core
blocker. Per-object domain ordering, further warehouse sources, human source
ratification and any publication remain separate parts of the Shop plan.

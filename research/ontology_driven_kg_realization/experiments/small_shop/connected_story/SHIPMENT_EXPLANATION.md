# Shipment explanation, evidence before verdict

Status: approved Shop-only read-side extension, tests first. It does not change
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
filled with a invented party. No payment or invoice amount is invented.

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

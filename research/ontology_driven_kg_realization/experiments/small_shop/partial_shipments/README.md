# Two partial shipments, one retained Shop history

This is a synthetic conformance extension, not more data from the retailer
paper. Order `SYN-PS-ORDER` contains two distinct units. Shipment `SYN-S1`
carries the first; `SYN-S2` carries the second. Their tracking IDs stay distinct.
No domain date is stated, so the plans use `NONE_STATED`.

Run the existing complete default Shop first. Admit the synthetic order under
that existing ontology. Add Shipment vocabulary through one additive contract
revision, then admit each shipment with its order and unit relations. Reopen
from the ledger alone, query the remaining unit after each stage, and trace
both shipments to exact retained source rows. Previous Shop records and the
original ledger prefix must remain intact.

`expected.json` is the independently authored answer key. The runner must not
read it. This exercises the existing public compiler, state-version profile,
structural admission, revision, query and trace. It adds no protocol rule,
stock allocation, delivery authorization, effect, re-entry or source-truth
claim. It is the additive entity/independent-tracking portion of the planned
shipment evolution, not migration of an existing shipment activity into an
entity. A later domain policy must decide over-shipment and fulfilment rules.

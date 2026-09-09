# Connected Shop model, selected direction

Luis accepted the ontology-led direction on 2026-09-08. This is a Shop
`ADOPTER_CHOICE`, tested as a `CONFORMANCE_FIXTURE`, not a Core ontology or a
universal replacement policy. The earlier two-row probes remain unchanged.

The claim is one source-produced account of the retained 21 occurrences, with
enduring objects, occurrence participation and explicitly versioned quantities
kept distinct. The observation is the replayed account: B still denotes one
supplier order, e4 and e7 both remain, quantity two supersedes quantity one,
and Y1 and Y2 remain different physical units. I2's unknown changed value
stays unknown. Every populated field points back to retained input.

## One definition per responsibility

- `ShopObject` groups the enduring identities named in source columns. Its
  concrete types distinguish orders, supplier orders, units, invoices, payments
  and actors. An actor identifier is not a claim about authorization.
- `ShopOccurrence` is a reported activity with its exact printed time text.
  Qualified `ShopParticipation` records join it to its named objects. Direct
  object relationships in the reader are joins over those occurrences, not
  extra asserted graph edges or inferred causality.
- `RecordedOrderState` is an abstract Shop category. `SalesOrderState` and
  `SupplierOrderState` carry explicit product quantities belonging to an
  enduring order. It is not a physical unit, an occurrence or a protocol event.
  Each recorded state is immutable. Supersession changes the current view,
  not the retained predecessor bytes.
- The profile names this state category once. The selected Core instruction
  uses subtype matching. Python does not contain another replacement-type
  allowlist. This restriction checks record categories, not the truth of an
  update or arbitrary same-owner identity semantics.
- The source adapter emits exact plans, including explicit state replacement.
  Core does not infer business effects from activity names. The adapter's
  source-column, activity and quantity mappings are retained data.

The shared state category has a concrete purpose: one admission boundary for
two typed order-state families. It is not a new generic State primitive or a
hierarchy built for hypothetical future consumers.

## Source and identity rules

Use the retained table and source boundary without changing their bytes.
Namespace identifiers by source role. A/B identify supplier orders, not supplier
parties. Product quantities come only from the explicit `order_details_text`
grammar. Item identifiers remain physical identities; do not infer product
properties from their spelling. Each occurrence is recorded once with all its
listed participants. Objects first mentioned together with an occurrence are
introduced in that same atomic change, not as an unexplained graph base.

One change per table row is an import transaction grouping, not an assertion
that table position is domain order. Retain every printed time unchanged and
use `NONE_STATED` for the unresolved knowledge-valid coordinate. No year,
timezone, calendar repair or elapsed-time conclusion is inferred. A supplier
update must find exactly one active state for the same order and product;
otherwise the adapter refuses instead of guessing a predecessor.

The four context passages remain separately retained evidence. This run does
not create an invented customer ID or an unpaid balance from missing payment
rows. The eligibility rule and its completeness assumptions remain the next
read-side deliverable. A recorded shipment is never suppressed to satisfy a
rule. The invoice update and unresolved dates carry explicit typed gaps.

## TDD and reuse

Reuse public contract compilation, neutral population plans, source/evidence
anchors, structural admission, the selected transition program, full replay,
maintained replay and record trace. No private Core import, direct accepted
graph write, manual successful check outcome or new runtime is permitted.

First freeze tests for the connected account, category-based replacement,
source-field accounting and replay. Implement the new sibling, then run all
Shop tests. The independent source expectations are never producer inputs.
No event-derived projection engine, generic mapper DSL, source-truth proof,
arbitrary history migration, external action, package change or release is in
this work.

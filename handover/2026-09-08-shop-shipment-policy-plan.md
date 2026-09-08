# Shop shipment-policy proof

Luis selected the bounded next test: a physical inventory unit must not be
assigned to two distinct shipments. This rule is an `ADOPTER_CHOICE`, not a
Malleus invariant. Its selected Shop admission policy is an `OPTIONAL_PROFILE`.
The runner is a research-local `REFERENCE_IMPLEMENTATION`; tests and exact
synthetic inputs are `CONFORMANCE_FIXTURE`.

## Claim and sequence

The rule stays in an identified rule artifact. Existing Core compilation,
staging, rule execution, policy evaluation, admission and replay do the work.
A duplicate assignment must refuse without changing the prior ledger or graph.
A legitimate second shipment must admit and survive reopen with its evidence.
Structural validation alone does not establish this policy.

First prove the existing Prolog checker can consume a graph backed by the
compiled contract view. Inspection found that the checker calls
`registry.verifies`, which the compiled view does not implement. Its raw-source
registry counterpart does. The first RED tests cross this exact public boundary
with the existing shipment vocabulary, valid and duplicate assignments, and a
wrong rule-contract ontology identity. A Core compatibility repair, if selected,
must accept only the compiled view's exact identity, not raw-source identity,
legacy grammar aliases, or an unrelated contract. Do not reparse the ontology
through `OntologyRegistry` to bypass the compiler.

Then compose the rule with an explicitly selected admission policy in a fresh
Shop conformance history. Do not silently migrate the completed structural-only
history to a stronger policy. Reuse the existing synthetic order and shipment
sources and keep that predecessor run unchanged.

Dependency sketch:

```text
compiled Shop contract -> staged candidate -> generic rule checker
identified shipment rule -> actual check result -> selected policy
selected policy -> ordinary KCS admission -> one history -> replay/query
```

## Bounds

The smallest observation is two distinct shipment IDs referencing one unit,
compared with two distinct units. Preserve exact source, rule, contract,
candidate and result identities. Required inputs are explicit; missing data
and failed execution cannot mean a successful check.

No delivery, stock availability, source truth, generic fulfilment engine,
multi-writer safety, retraction, policy migration, new rule language, new
dependencies, packaging, release, push, Robotics or Re-entry changes are selected.
The existing Prolog executor runs trusted local rules only. Its process boundary
is not an untrusted-code sandbox. Any newly required public contract or broader
mechanism must be surfaced before implementation, not hidden in the fixture.

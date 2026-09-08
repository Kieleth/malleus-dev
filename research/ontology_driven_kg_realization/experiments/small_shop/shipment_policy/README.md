# One physical unit, one shipment

The previous [partial-shipment example](../partial_shipments/README.md) proves
that two shipments and their unit assignments can be recorded and replayed.
A well-shaped record can still describe a bad assignment. This sibling adds
one selected Shop rule: **a physical unit cannot belong to two distinct
shipments at the same accepted state**.

The rule is an adopter choice, not a Malleus invariant. Its admission policy is
an optional profile. This runner is a research-local reference implementation
and the synthetic rows/tests are conformance fixtures, not evidence of delivery.

## The example

Order `SYN-PS-ORDER` contains physical units `SYN-PS-X1` and `SYN-PS-X2`.

| Candidate | Actual rule result | Admission |
|---|---|---|
| First shipment carries X1 | SATISFIED | Accepted |
| Second shipment also carries X1 | VIOLATED, with both associations and X1 as witnesses | Rejected, no admission bytes appended |
| Second shipment carries X2 | SATISFIED | Accepted |

The negative case has its own retained [source rows](duplicate-unit.jsonl).
It does not change the original positive source or pretend that X2 was X1.
The existing row mapper reads the explicitly selected source. No source truth
or physical-world effect follows from these synthetic associations.

## What executes what

[rules.pl](rules.pl) defines the business rule. [logic.yaml](logic.yaml) pins
its contract, compiled ontology identity, rule manifest and execution timeout.
[policy.json](policy.json) requires that exact check contract and maps its
actual outcome to ACCEPT, REJECT or DEFER. The existing generic
[machine artifact](../correction/machine.json) records checks and derives the
verdict; this sibling does not add another interpreter.

The runner compiles the Shop ontology and selects this policy in a **fresh**
history. It retains the bootstrap, sources, mapping and rule bytes. Population
preparation retains the plan. Admission stages the exact KCS operations over
the current graph, runs the existing trusted Prolog checker, and submits its
real result to the selected policy. It never accepts a caller-supplied outcome.

The atomic admission batch contains the KCS, check receipt, proposal, check and
derived verdict. A rejected check leaves the exact pre-admission ledger and
accepted graph unchanged. The prior preparation remains visible: retained
source or plan bytes are not accepted domain records. The rejected check is
reported to the caller, not persisted by this acceptance-only transaction.

An accepted receipt binds the KCS, retained population plan, candidate and base
graph digests, compiled ontology, rule contract/bytes, engine version, facts
and witnesses. Reopen reads the retained history alone and does not rerun
Prolog. It preserves an execution attestation, not independent proof that an
engine ran. Low-level caller-authored machine events remain a trusted boundary;
this runner is not an anti-forgery mechanism or an untrusted-rule sandbox.

## Run

Use the configured repository environment, including its existing SWI-Prolog
dependency. The chosen history file must not already exist:

```sh
python -m research.ontology_driven_kg_realization.experiments.small_shop.shipment_policy.run --history /tmp/shop-shipment-policy.jsonl
```

The command prints the refusal, final shipment query and exact identities. It
leaves the inspectable ledger at the requested path. Two invocations with fresh
paths produce identical history/report bytes in the tested environment.

The only Core runtime repair is `ContractView.verifies`, allowing the existing
logic checker to verify the compiled identity. It accepts no legacy ontology
aliases. All domain names, rules and selection remain outside Core.

This episode supports insert-only Entity/Relation changes and the exact
fixture types. It does not migrate the older structural-only history, process
cancellation or reassignment, enforce stock availability, check delivery,
support subclasses as a new rule family, or claim a generic fulfilment system.
Those are separate choices, not missing pieces of this proof.

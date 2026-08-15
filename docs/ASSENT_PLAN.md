# Thin AssentPlan

`AssentPlan` runs the epistemic monitors that a proposal already committed to
through its exact `EpistemicPolicyArtifact`. It is an optional convenience
layer over `ProtocolLedger`. Replay remains authoritative.

## Small example

An invoice proposal names one exact type monitor in its policy. The plan binds
that monitor ID and record hash to a callable adapter. The adapter receives
read-only copies of:

1. the exact proposal;
2. the exact monitor specification;
3. the monitor's declared input artifacts.

If the adapter completes, it returns a `MonitorEvent` carrying its typed
assessment. If it raises or returns a record that the protocol refuses, the
plan records the existing atomic pair:

```text
MonitorFailure + UnavailableAssessment(UNKNOWN)
```

The plan calls each adapter once. It never retries a failure and never turns a
failure into a satisfied assessment.

## Logical monitor

A logical monitor returns two events: its `LogicCheckRecord` plus witnesses,
then its `LogicalAssessment`. Malleus validates and commits that pair through
one failure-atomic ledger replacement. Both events enter or neither does.

This is one monitor-run boundary. The complete plan is not an atomic
transaction. A later monitor may fail after an earlier monitor completed, and
the ledger retains both facts.

## Explicit inputs

`AssentPlan` contains only the proposal ID and record hash plus a canonical
tuple of `MonitorStep` values. Each step supplies:

- exact monitor ID and record hash;
- one adapter;
- explicit event, failure, and unavailable-assessment IDs;
- explicit time, actor, role, failure category, and error code.

Before any adapter runs, the plan reopens the ledger and checks exact policy
coverage, proposal and monitor hashes, declared monitor inputs, failure fields,
record-ID availability, and whether a monitor already produced an output.
There are no inferred monitors, IDs, actors, times, or error categories.

## Boundary

`AssentPlan` is runtime conduct, not canonical knowledge, so it is not another
ontology record and is not persisted. The events it produces carry the
provenance. This follows the existing separation:

```text
AssentPlan runs declared adapters
ProtocolLedger validates and records their outputs
Replay reconstructs authoritative state
Policy evaluation selects epistemic control afterward
```

This first version does not:

- choose monitors or policies;
- decide `ACCEPT`, `REJECT`, `DEFER`, or `CONTEST`;
- run authority monitors;
- authorize or dispatch actions;
- retry, schedule, queue, resume, or parallelize work;
- discover plugins or serialize plans;
- claim whole-plan or multi-writer atomicity.

An authority plan may be added only when its action, actor, grant, policy, and
failure context can remain equally explicit. A general workflow engine is not
part of this protocol boundary.

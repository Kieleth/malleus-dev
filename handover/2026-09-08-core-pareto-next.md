# Core Pareto sequence: faster checks, reconciled backlog, partial shipments

Luis approved this sequence: test-performance debt and backlog reconciliation,
then the partial-shipment Shop exercise with TDD. Starting point is
`0cdf8ed306a8a4b3b38a1d2635c7dc6dc7077ed1`, overseer entry 432.
Robotics integration and Semantic Re-entry remain consumer-owned.

Core owns `scripts/contract_compiler_ledger.py`,
`tests/test_governance_git_scan.py`, the current backlog/status documentation,
the new partial-shipment fixture and its tests, and the next overseer append.
No action program, action producer, Re-entry code, acolyte skill, or public
runtime contract is being changed. Consumers may validate in isolated clones;
do not land into the shared index or append Core governance concurrently.

## Bound slices

| Deliverable and role | Claim and smallest observation | Reuse | Exclusions |
|---|---|---|---|
| Governance validator optimization, `REFERENCE_IMPLEMENTATION` | Validate the same current repository with one durable-ancestry scan per call; changed refs and document bytes must still refuse on the next call. Compare the unchanged governance/integration suites and measured timings. | Existing Git reachability rules, JSON schemas, hash chain and document guards. | No skipped checks, persistent cache, schema relaxation, dependency or package change. |
| Current backlog view, `REFERENCE_IMPLEMENTATION` | Separate completed bounded capabilities from formal work still pending, with links to exact receipts. | Existing program, append-only overseer history and handovers. | No second DAG, retroactive edits to receipts, activation or completion of formal workstreams. |
| Partial-shipment exercise, `CONFORMANCE_FIXTURE` | Compile a base Shop ontology, admit initial records, add Shipment vocabulary through the existing additive revision, admit two independently tracked partial shipments, then reopen and query their retained provenance while preserving the initial history. | Public compiler, state-version profile, structural admission, contract revision, replay and trace. | No new Core runtime semantics, effects, re-entry, general migration, fulfilment policy or claim of source truth. |

The shipment records are explicitly synthetic adopter data, not missing facts
from the published retailer case. Shipment identity and its order relation are
`ADOPTER_CHOICE`. The lowest selected profiles are the compiler-enabled,
state-version and structural semantic-history profiles. Without selecting
history, the example makes no persistence, accepted-history or replay claim.
This covers the additive entity/independent-tracking portion of the evolution
thread in `design/GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md`, not an
activity-to-entity migration or a complete fulfilment system.

Dependency sketch:

```text
validator optimization -> unchanged governance/integration tests
existing completion receipts -> reconciled backlog view
base ontology + retained synthetic sources -> initial admitted Shop records
target ontology -> additive ContractRevision -> shipment PopulationPlans
PopulationPlans -> structural admission -> one history -> replay/query/trace
```

Each change starts with a discriminating failing test where behavior changes.
The Shop exercise starts by testing the missing fixture runner against an
independent expected result. A runtime gap, if found, is reported before this
fixture acquires new protocol semantics. Commit locally; no remote push.

## Initial measurement

The prior clean default-suite receipt attributes 424.025 seconds to integration
and 374.867 seconds to ledger tests, about 69% of that run. A current cProfile
of one `load_ledger` call at the starting commit reports 432 entries, 839 Git
subprocesses, 22.778 seconds total and 17.641 seconds in subprocess calls.
Profiling adds overhead; these are observations, not a benchmark claim.

The implementation currently runs `cat-file` and ancestry checks per commit
reference. There are 416 references to 331 distinct commits. The bounded fix
is a per-call HEAD/evidence-tag ancestry snapshot, not a cache of validation
results across calls. Current bytes, schema, chronology, references and hashes
remain checked each time.

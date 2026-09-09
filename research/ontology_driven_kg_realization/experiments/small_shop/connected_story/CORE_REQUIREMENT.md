# Shop history selection: enforceable declarations versus retained labels

Status: request for Core contract classification. No Core implementation is
authorized by this file. Shop has not selected or frozen its candidate profile.

## Consumer requirement

In the connected Shop story, one history must retain domain occurrences and
explicit state changes without treating them as the same thing. The proposed
small cut preserves supplier-order occurrences e4 and e7, changes B's quantity
from 1 to 2 through state-record supersession, and reconstructs both meanings
after reopen. It does not infer state changes by executing event descriptions.

Core baseline: released `v0.14.0`, commit
`e2b9e77912f9b36fdbfe2fca310548a789bffb4d`, tree
`162325eb0048816654d2df5b6b0f00270d06385d`. Final validation used an isolated
export of this release plus only the Shop files at `5ea6c903`, excluding
concurrent Core edits. Local Shop and unrelated consumer commits are later
than the release; they do not represent a runtime rebind.

## What works

`history_probe.py` uses only exported Malleus APIs, installed root vocabulary,
an existing Shop ontology and the proposed adopter profile. It compiles,
retains exact table bytes, prepares two plans, admits with Core-generated checks,
reopens and traces. Three tests pass: the joined behavior, state-only Event
refusal, and byte-identical repeated history.

Result: 18 protocol events, two change sets, seven historical records and six
current records: one supplier-order entity, one active state, two occurrences
and two event participations. Both state versions remain in history.

## Remaining contract question, with executable witness

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.core_contract_probe
```

This starts that same history, then proposes replacing an Event and its
participation, despite the candidate profile declaring
`correction: EXPLICIT_SAME_TYPE_STATE_SUPERSESSION` and
`ontology_roles.state: [SupplierOrderState]`.

Observed on the baseline: `ADMITTED`; e7 remains retained but is superseded by
`e7:replacement-probe` in the current view. There is no historical-byte mutation
or replay failure. The generic structural executor accepts the supplied valid
operations. The profile's text labels do not add an executable restriction.
This witness does **not** assert that arbitrary custom labels already have a
Core-defined operational meaning, or that Core's structural guarantee is broken.

Please classify the smallest supported path:

1. Can Shop express and bind a type/family-specific supersession rule through
   existing public policy/check contracts, while keeping the default structural
   checks and atomic admission? Supply the exact public route and its guarantee.
2. Which profile fields are enforced capabilities and which are retained
   declarations? Can the proposed mixed record history be described honestly
   without claiming an event-derived projection or a profile rule interpreter?
3. If this requires a missing public Core contract, provide that seam in Core.
   Shop will wait instead of adding a private importer, a handwritten successful
   check receipt, or a preflight that is falsely claimed to enforce admission.

The intended replacement policy itself remains a Shop choice for Luis. Core
owns the executor contract, not retail semantics. No new DSL, general planner,
profile migration, Event-to-Event relation, evaluation or Re-entry is requested.
Continue independent source-accounting work, but hold final history-model
selection and the connected population until this boundary is explicit.

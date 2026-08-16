# Design note: the commitment lifecycle facade

Status: **design under grooming, not a capability.** Roadmap item B1. Nothing
described here exists. Do not cite it as a malleus feature.

Written because a benchmark adapter came out at 807 lines and two more are
queued behind it, and copying a lifecycle three times is how a comparison
stops being a comparison.

## The gate, applied to this design before designing

- **Claim.** One lifecycle implementation can drive N benchmark adapters,
  with each adapter supplying only its domain content.
- **Smallest discriminating observation.** The existing SciFact adapter is
  reproduced with no lifecycle code in it and identical ledger output, byte
  for byte, against the recorded run.
- **Artifact to reuse.** `AssentPlan` and its `MonitorStep` /
  `MonitorFailurePlan` shape; the existing digest and record builders in
  `accepted.py`, `control.py`, `source.py`; the SciFact adapter as the
  reference trace.
- **Excluded.** Everything in the Exclusions section below, and core.

---

## 1. Evidence

**Measured on the reference adapter**, not estimated:

| | lines |
|---|---|
| generic lifecycle | 644 |
| domain content | 105 |

The domain content is two functions, and they already share a signature:
`candidate_writes(case, proposal) -> writes` and
`structural_issues(case, proposal) -> tuple[str, ...]`. Everything else is
lifecycle.

**Consumer survey across the fleet.** Every project importing malleus was
checked for level-5 usage. Result: `ProtocolLedger`, `malleus.assent`,
`malleus.accepted` and `AssentPlan` appear in exactly two files outside the
library and its tests, both inside the research program. No external adopter
uses the assent protocol at all. The fleet sits at levels 1 to 3.

That single fact sets the abstraction axis. There is no population of
external orchestration users to generalise over, so generalising for them
would be inventing requirements. **The axis that exists is
benchmark-to-benchmark**, and the only observed variation along it is the two
functions above plus an ontology.

**The canonical spine**, read off the reference adapter in order:

```
anchor external snapshot
  → register sources (claim, document, proposal)
  → register graph base
  → register candidate subgraph
  → register rules artifact
  → register monitor specification
  → register epistemic policy
  → assemble proposal members
  → record PROPOSAL_RECORDED
  → run AssentPlan (monitors)
  → evaluate epistemic policy
  → on ACCEPT: acceptance head, accepted application
  → record EPISTEMIC_DECIDED with transition
```

`AssentPlan` covers exactly one of those thirteen steps. That is the gap, and
it is not a defect in `AssentPlan`.

## 2. What the 644 lines actually are

This is the design's load-bearing observation, and it is easy to get wrong.

The repetition is **not** in the semantics. Each artifact kind has a
deliberately distinct semantic hash pinning a different field set:
`source_artifact_digest`, `candidate_artifact_digest`,
`graph_base_artifact_digest`, `monitor_specification_digest`,
`epistemic_policy_digest`. Collapsing those into one generic builder would
destroy the property they exist to provide. Do not data-drive the digests.

The repetition is **bookkeeping**: build a record, append it under the right
`EventType`, keep its `(id, hash)`, and thread that pair into three later
steps that must cite it exactly. Thirteen steps, six artifacts, and every one
of them cited downstream. That threading is the bulk of the 644.

So the facade owns the bookkeeping and touches none of the semantics.

## 3. The design, three layers

### Layer 1: `LedgerSession`, the bookkeeper

```python
class Ref(NamedTuple):
    id: str
    hash: str

@dataclass(frozen=True)
class ArtifactKind:
    """Declared once per kind. Six instances, a module-level tuple."""
    record_type: str
    event_type: EventType
    digest: Callable[..., str]

class LedgerSession:
    def register(self, kind: ArtifactKind, **fields) -> Ref
    def cite(self, kind: ArtifactKind) -> Ref     # KeyError if not registered
    def record(self, event_type: EventType, payload: dict) -> None
    @property
    def registered(self) -> tuple[tuple[str, Ref], ...]
```

`cite()` raising on an unregistered kind is the point: today the adapter
threads raw strings between eight call sites, and a typo there produces a
dangling citation that only replay catches. The session makes the citation
graph explicit and makes a missing prerequisite a loud failure at the call
site.

`registered` exists so the result can state its own coverage. See §5.

### Layer 2: `CommitmentLifecycle`, the spine as data

Mirrors the shape `AssentPlan` already established, because a second
orchestration idiom in the same library is a `single_source` violation
waiting to happen.

```python
@dataclass(frozen=True)
class Phase:
    name: str
    run: Callable[[Context], None]
    required: bool = True

@dataclass(frozen=True)
class CommitmentLifecycle:
    phases: tuple[Phase, ...]
    def run(self, context: Context) -> LifecycleResult

@dataclass(frozen=True)
class LifecycleResult:
    outcome: str                       # from the policy, never computed here
    ran: tuple[str, ...]
    skipped: tuple[tuple[str, str], ...]   # (phase, reason)
    refs: Mapping[str, Ref]
```

The thirteen steps become thirteen named phases in one tuple, which is
readable in one screen and diffable when it changes. The 274-line
`run_proposal` becomes a declaration.

### Layer 3: `BenchmarkAdapter`, the four slots

```python
class BenchmarkAdapter(Protocol):
    name: str
    ontology_path: Path
    def sources(self, case) -> Mapping[str, bytes]: ...
    def candidate_writes(self, case, proposal) -> tuple[TemporalWrite, ...]: ...
    def structural_issues(self, case, proposal) -> tuple[str, ...]: ...
```

A `Protocol`, not a base class: nothing is inherited, nothing is overridden,
and a benchmark stays a plain module. SciFact's 105 lines fit these slots
with no remainder, which is the acceptance test for the whole design.

## 4. Exclusions, stated so they cannot creep

- **No plugin system.** Three adapters, imported by name. No entry points, no
  discovery, no config file, no registry with a decorator.
- **No retries, scheduling, resume, or concurrency.** That is
  `monitor-execution-orchestration`, which is on the not-implemented list and
  stays there.
- **No authority or authorization arm** until a benchmark needs one.
- **No abstraction over the digests.** §2.
- **Not in core.** §6.
- **No new EventTypes.** If a phase needs one, that is a protocol change and
  goes through the ontology, not through the facade.

## 5. Hazards this design must not reproduce

Six self-inquisitions in one week found orchestration defects of exactly the
kind this facade could introduce. Designing against them now is cheaper than
healing them in round seven.

1. **The result states its own coverage.** `LifecycleResult.skipped` is not
   optional decoration. A run that skipped four phases and a run that
   completed must be distinguishable without reading a log. Round four
   granted a purity seal from an instrument that had judged nothing, and the
   header said `0 rites disabled`.
2. **No phase may swallow a refusal.** A phase either completes or the
   lifecycle stops with the reason attached. Round five: an unknown condition
   that passes is worse than one that fails, because it fails silently and
   only once.
3. **The facade never computes a verdict.** It calls
   `evaluate_epistemic_policy` and records what came back. An orchestrator
   that can decide is an arbiter, and `arbiter_is_accountable` then applies to
   it: judge identity, version, inputs, reason. Keep it a router and the rite
   does not attach.
4. **No `except Exception`.** 0.8.0 introduced the first one in `src/`, in the
   orchestrator, and it swallowed the plan's own contract violations
   alongside the adapter's. Catch named types.
5. **Nothing is auto-created from a default.** Every artifact is registered
   explicitly. A convenience that invents a missing graph base is a
   `silent_drop` with better manners.
6. **A skipped required phase denies the result.** The floor goes on the
   outcome, not on a flag, which is round five's lesson stated as a design
   constraint: put the floor where it cannot be tuned away.

## 6. Where it lives, and when it moves

**Research-local first**, in the benchmark package beside its adapters. Not
in `src/malleus/`.

The reason is the promotion rule, and it is not bureaucracy: an API designed
from one example encodes that example's accidents permanently, because core
evolution is add-only once instances exist. Today there is one adapter and
two prospective ones.

**Designed so promotion is a move, not a rewrite.** Three conditions, all
checkable:

- the harness core imports nothing from any benchmark package;
- `BenchmarkAdapter` is the only surface a benchmark implements;
- adapter three lands without changing the harness.

When the third adapter lands unchanged, the shape has stopped moving and the
facade has three consumers. That is the moment to propose it for core, with
three worked examples instead of one.

If instead adapter two forces a harness change and adapter three forces
another, that is the design telling you the abstraction is wrong, and it is
much cheaper to hear that in a research package than in a published API.

## 7. Open for grooming

- Does `Context` carry the ledger, the clock and the case, or is the clock a
  phase-level input? The reference adapter uses a fixed `at(minute)` helper,
  which is right for determinism and needs a home.
- Should `structural_issues` return codes or typed records? Codes today; the
  `provenance_typed` rite argues for typed once a second benchmark shows
  whether the code sets overlap.
- Is `sources()` returning raw bytes correct, given that `SourceArtifact`
  records a declared digest and never reads bytes? Returning bytes lets the
  harness compute the digest honestly, which is stronger than the library's
  own boundary. Probably keep it, and note the asymmetry.

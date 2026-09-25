# Temporal Core workstream

Forward note, 2026-09-24: gate G4 is written. [g4/DECISION.md](g4/DECISION.md) is
the memo for the author's choice of representation and first Core cut;
[g4/COMPARISON.md](g4/COMPARISON.md) holds the cross-witness table, the paper
assessment of a native temporal store, specimen defects and triaged open choices.
Nothing is selected until the author decides.

Status: implementation paused for bitemporal design research, 2026-09-24.
Isolated development; no integration or release claim.

Current author direction: challenge the proposed path with worked thought
experiments across the existing flows before choosing it. Start with
[GEDANKENEXPERIMENTS-01.md](GEDANKENEXPERIMENTS-01.md) and
[STORAGE-FLOWS-01.md](STORAGE-FLOWS-01.md). Their G0 to G4 research gates precede
the next runtime contract/implementation decision. No backend is selected.

Author correction: all accepted versions must remain queryable in the KG.
Temporal/context selection determines their use; a selected-state graph is not
the entire knowledge model. See [bitemporal research](BITEMPORAL-RESEARCH-01.md).
The previous structural-first admission recommendation is withdrawn, not chosen.

Author decision, 2026-09-24: implement the smallest Core support for corrections,
state transitions and historical queries. Keep later temporal reasoning visible
in the roadmap. Calculations consume identified temporal premises; this work
does not automatically recompute them.

Base: `ebff70f72dc4cd67b2f910b88575e558a2824728`, tree
`7b9a81fb35c5cb2016830c289915a359fed7162f`.
Branch: `codex/core-temporal`. The main checkout and UMR worktree are not ours
to edit. Main has active history/revision changes; integration needs coordination.

## Claim and boundaries

An optional temporal extension to semantic history must distinguish when a
proposition applies from when it was accepted. A correction of a prior report
must not assert that the world changed when the correction arrived. A historical
read must expose only evidence and contracts available at its selected position.

Role of the semantics: `OPTIONAL_PROFILE`, over compiler-enabled semantic history.
Role of Python APIs: `REFERENCE_IMPLEMENTATION`.
Role of authored examples and expected answers: `CONFORMANCE_FIXTURE`.
Domain-specific temporal roles and decisions to accept corrections: `ADOPTER_CHOICE`.
No additional mandatory base-protocol rule is introduced.

Smallest falsifier: the same selected domain date yields the wrong price after
an accepted correction, or a historical read includes later evidence. Reuse the
existing ledger fold, contract artifacts, source retention, `ValidTime` and
Assent temporal semantics where applicable. Do not add a parallel state store.

Without the extension, existing histories retain their existing semantics.
There is no silent migration or relabelling of capture order as domain time.

## Milestones and progress checks

| Milestone | Deliverable | Completion evidence | State |
|---|---|---|---|
| T0 | Scope, examples, expected answers, journal, isolated checkout | Named cases and pre-implementation expectations | Complete |
| T1 | Public-API baseline and capability map | Existing behavior reproduced, limitations demonstrated | Complete, bounded baseline |
| T2 | Exact historical knowledge-position read | RED then GREEN; no future evidence/contract leakage; no writes | GREEN locally, integration pending |
| T3 | Explicit correction versus transition semantics | Same-period correction and actual transition produce different expected views | Paused: version graph, temporal selection and check scope under review |
| T4 | Domain-time selection at a historical knowledge position | Late and future-effective evidence, half-open boundaries, explicit unknowns | Pending |
| T5 | Calculation-consumer contract | Changed selected premises identified; old execution remains explainable; no auto-execution | Pending |
| T6 | Integration and distribution checks | Existing consumers preserved, clean package and relevant suites | Pending |

Dependencies: T0 -> T1 -> T2 -> T3 -> T4 -> T5 -> T6. T2 is useful alone but is
not bitemporal querying. T3 must specify corrections to an already retired
version and interval scope before changing the persisted grammar. T4 must reuse
existing precision handling where its meaning matches, not treat an uncertain
transition window as a duration.

Each implementation step starts with a failing test. Record the command,
observed result, implementation and limits in [JOURNAL.md](JOURNAL.md).
Expected answers are authored before runtime changes and are not regenerated
from the implementation. No paid model or extraction step is needed.

Next-stage preparation is [NEXT-STAGE.md](NEXT-STAGE.md), with a separate
[draft answer key](expected-views-v1.json). It sequences representation approval,
exact semantic contract, RED tests, Core implementation, consumer proof and
integration. P0 in that packet is prepared; it does not complete T3 or authorize
runtime work. The initial nodes-versus-properties choice was under-specified.
[The representation comparison](REPRESENTATION-OPTIONS-01.md) separates assertion
identity, Core-owned temporal queries and storage, and presents a researched
recommendation for approval. No representation has been selected.

## Reading order

1. This plan and [JOURNAL.md](JOURNAL.md).
2. [Controlled situations](situations.json).
3. [Historical-read contract](CONTRACT-01.md).
4. [Dependency graph](design.ttl).
5. [Measured baseline](BASELINE-01.md) and [correction design draft](CONTRACT-02-DRAFT.md).
6. [First implementation results](RESULTS-01.md).
7. [Bitemporal research and author correction](BITEMPORAL-RESEARCH-01.md).
8. [Earlier correction admission scope](CHECK-SCOPE-02.md), recommendation superseded.
9. [Next-stage review packet](NEXT-STAGE.md) and its authored answer key.
10. [Representation options and recommendation](REPRESENTATION-OPTIONS-01.md).
11. [Cross-flow thought experiments](GEDANKENEXPERIMENTS-01.md),
    [storage constructions](STORAGE-FLOWS-01.md) and the inspected evidence manifest.

## Later, not smuggled into this cut

- General temporal inference, recurrence, geological calendars and UMR mappings.
- Automatic extraction or judgment of temporal meaning from prose.
- Automatic recomputation, scheduling or external effects.
- Arbitrary interval splitting, retraction and competing-history reconciliation.
- Unified Assent migration, a second backend, multi-writer coordination.
- Source truth, real-world freshness, authenticated clocks or policy authority.

These exclusions constrain this first implementation, not the eventual uses.
The computational consumer must keep assumption/report basis, calculation
version, input identities and temporal selection separate. Equal numerical
results do not make executions interchangeable.

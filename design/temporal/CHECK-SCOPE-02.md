# T3 admission scope, before changing the history grammar

Supersession note, 2026-09-24: the author rejected treating historical values as
outside the KG. The recommendation below is withdrawn. Its existing-path
observations remain evidence, but they do not determine the future graph model.
See [BITEMPORAL-RESEARCH-01.md](BITEMPORAL-RESEARCH-01.md). No option was selected.

Status: measured existing path plus proposed correction obligations. No new
correction operation, wire grammar, check policy or temporal projector is active.

## Finding

Both compiler history and the separate Assent temporal path encode replacement
as an end boundary on the prior record. Compiler history rejects a replacement
whose instant is not later than the prior start. Both reject a replacement of
an already superseded record. Neither link alone expresses correction of our
account of an unchanged period.

An additional obligation appears at admission. Existing Prolog checks receive
the graph after the candidate replaces current records. They do not receive a
query over the candidate's affected historical periods. The structural builtin
receives history as well, but its existing operation checks still implement the
same replacement semantics. This is correct for the existing contract, not a
newly discovered bypass in shipped correction support. That support is absent.

Sources inspected:

- `src/malleus/_contract_pipeline/knowledge.py`, `_apply_change`.
- `src/malleus/accepted.py`, `validate_temporal_writes`.
- `src/malleus/_contract_pipeline/admission.py`, `_check_stage`, `_check_base`,
  `_run_check`.
- `src/malleus/_contract_pipeline/check_contract.py`, `CheckRequest`,
  `_operations_apply_atomically`.

The executable controls in `test_temporal_check_scope.py` observe the request
and then invoke the real check unchanged. They supply no check outcome.
One uses a synthetic price state and the structural builtin. The other uses
the existing authored order fixture and its actual Prolog rule. The latter
replaces quantity 2 with quantity 5: the rule sees quantity 5 alone, while
quantity 2 remains in retained record history. This establishes existing check
scope, not the correctness of any proposed historical rule policy.

Observed verification: both controls passed, including actual Prolog execution.
The combined run with the 30 existing temporal tests passed 32 tests. See
TEMP-007 in JOURNAL.md for the command and the corrected observer setup failure.

Implementation detail discovered while observing: `CheckRequest.candidate_graph`
is annotated `KnowledgeGraph` but receives a `CandidateSubgraph`. Its `overlay()`
returns the graph inspected here. The actual Prolog executor already consumes
that staged candidate correctly. The inaccurate annotation is recorded for
cleanup; it is not evidence that Prolog received the wrong records.

## What the next operation must preserve

A domain-state period and an accepted account of that period are separate
identities. A real transition starts another period. A correction changes the
selected account of one period without changing its start or end. The original
account remains available at its earlier knowledge position.

For the controlled price example:

| Accepted knowledge position | Account of 1 May to 12 May | Account from 12 May |
|---|---|---|
| Original report plus later transition | 750 cents | 800 cents |
| After correcting the earlier report | 775 cents | 800 cents |

Clarified after author correction: 775 and 800 must be able to coexist as
qualified versions in the full KG. A selected view must not present both as the
same currently applicable price. Checks of an ended period must inspect the
appropriate versions and context, not omit them because today's state differs.

Relations need the same discipline: a relation to an exact historical record
cannot silently become a relation to its corrected account. The selected
representation must either keep that exact reference, explicitly replace it,
or refuse an invalid projection. No automatic endpoint rewriting is authorized.

## Decision needed before the next runtime RED

The author has approved correction versus transition and the KISS scope. The
remaining choice is the admission guarantee for this new operation:

1. **Structural scope first.** Check the affected historical representation
   against the ontology, preserve exact references, and refuse correction under
   a custom domain-rule policy until its historical check scope is defined.
   Do not fall back to structural acceptance when custom checks are selected.
2. **Historical domain checks now.** Define the states each rule must inspect,
   which policy/ontology version governs the correction, and receipts binding
   those states. Execute those checks before accepting the correction.

Recommendation: option 1 for this first synthetic Core cut. It must be a named,
explicitly selected extension, not a weaker path into existing rule-governed
histories. Option 2 remains a required integration milestone before those
adopters can use corrections. This recommendation is not an author decision.

Choosing a policy's time scope is not an interpreter detail. Reusing today's
policy, replaying the period's old policy, and checking every affected domain
snapshot can produce different verdicts. No implementation should decide that
by accident.

## Sequencing after the decision

1. Freeze an addressable correction contract, with its declared semantics,
   supported operation families, reference behavior and refusal rules.
2. Freeze REDs for active-period and ended-period correction, repeated correction,
   stale targets, type/time mismatch, unsupported policy and partial failures.
3. Implement through the existing immutable change-set, check and replay path.
   Preserve existing histories' meanings by explicit version/profile selection.
4. Verify both a price state and a differently shaped scientific account with
   unstated domain time. Reopen, historical reads and maintained reads must agree.
5. Add domain-time selection and later calculation-premise comparison. No
   automatic execution or invented temporal precision.

No source extraction, truth assessment, external effect or paid model run is
needed for these synthetic controls.

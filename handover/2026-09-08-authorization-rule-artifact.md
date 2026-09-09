# Authorization rules as identified data

## Approved cut

Luis approved the next step from the
[authorization comparison](2026-09-08-authorization-conformance.md): move the
verdict rules into an identified artifact, preserving existing behavior.

Role: `REFERENCE_IMPLEMENTATION` of the existing optional Assent authorization
profile. The finite action capability consumes the same implementation. This
does not change the base protocol or oblige other profiles to use this recipe.

1. Claim: outcome mapping, precedence and trigger membership come from exact
   identified data, not authorization-specific Python branches.
2. Observation: the existing nine-case answer table, frozen pre-change policy
   and evaluation hashes, generic-label rules, typed missing/corrupt-artifact
   refusal, and the existing owning-history tests.
3. Reuse: version-1 authorization policy identity already binds outcome mapping
   and precedence. Keep that hash preimage, assessment ordering, evaluation-hash
   recipe and public signatures unchanged. Read one pinned packaged resource
   before pure use, retain immutable parsed values, and do not add fallback.
4. Exclusions: caller-selectable policy semantics, new ontology terms, public
   DSL, a new ledger epoch, changed prior histories, Assent state-machine
   replacement, second interpreter, Shop or consumer edits.

The private artifact has a closed shape: grammar identifier, outcome-to-control
map, highest-first precedence and triggering controls. A generic interpreter
performs lookup, membership and ordered selection. Nonempty exact monitor
coverage remains a separate existing admission obligation. The default loader
pins exact resource bytes to the existing version-1 semantics; a different
artifact does not silently reinterpret a version-1 policy.

Dependencies remain in the existing Assent replacement backlog. The internal
rule interpreter consumes the identified control artifact; both the policy
digest and authorization evaluator consume its values; finite control calls
that evaluator. No new public stage or parallel policy authority is introduced.

## Evidence

TDD and integration results will be recorded at the completed boundary.

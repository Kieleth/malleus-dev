# Sequential actions in one Shop history

Status: approved implementation scope, RED first.

## Contract

This is an optional reference profile, not a new protocol invariant. One action
may be active at a time. Its independently registered observation closes that
episode. A successor uses the actual updated history, fresh checks and a fresh
authorization. Every immutable record and cumulative uniqueness index survives.

The smallest integration witness is two complete action lifecycles in one real
Shop history, with the existing independent e4-to-e7 knowledge correction between
them. Reopening the retained log must recover both lifecycles, the correction,
and the original Shop records. The synthetic actions do not cause that correction.

## Implementation boundary

Reuse the existing finite interpreter, keyed state effects, control evaluators,
and KnowledgeChangeHistory. Author a separately selected profile with explicit
current pointers and an observed-before-successor gate. Bind each action payload
hash to an exact retained source artifact. Do not change the original single-action
profile, its receipts, or any published historical example.

No new instruction, public SDK, robot or supplier effect, concurrent actions,
retry policy, scheduling, or recovery from a non-executing decision is authorized
by this slice. A missing interpreter instruction requires another operator decision.

## TDD observations

1. The original profile remains unchanged; the new definition uses existing
   opcodes and retains cumulative indexes while moving current pointers.
2. An early successor, a mismatched payload, and reused checks, authorization,
   dispatch or observation refuse without changing ledger bytes.
3. A context captured before the intervening knowledge correction refuses.
4. Both real check producers run for both actions; replay invokes neither.
5. The same transaction programs handle both actions. Reopen from the log alone
   recovers the same graph and protocol state.

Tests and final coordinates will be recorded here after execution. No GREEN or
consumer-readiness claim is made by this plan.

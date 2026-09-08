# Sequential actions in one Shop history

Status: implemented and tested, optional repository-local reference profile.

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

This contract does not authorize a broader consumer-readiness or release claim.

## Implementation journal

The existing keyed state instruction is sufficient. The optional definition
preserves cumulative indexes and immutable records, and maintains separately
named current pointers. Its transaction programs are reused for each episode;
there are no first-action and second-action interpreter branches.

RED `f85b7ed` requires the missing pointer projection. RED `49953bd` requires
the missing two-action integration driver. The driver reuses the original
record/check/control constructors with explicit episode identifiers and clock
offsets. Their default values preserve the original one-action fixture.

The first real run completed both lifecycles around the independent Shop
correction. A subsequent negative probe found that registering another outcome
contract let an observation about the previous execution reopen the gate while
the next action was active. The test reproduced successful append where refusal
was required. The profile correction resolves observation to execution to
dispatch and requires that dispatch to belong to the current action before
setting READY. This is a data-program guard, not a Python runtime branch.

Payload binding establishes exact retained bytes and provenance, not the meaning
or safety of an adopter's payload. Receipt and observer inputs are synthetic
conformance records. Actual execution and actual observation remain adopter
responsibilities. Source registration happens separately before the atomic
context/proposal transaction. No effect is invoked by this test driver.

The first combined test invocation had six passes and five failures. Its negative
witnesses used old transaction timestamps, so the ledger correctly refused them
before the intended action-binding guard. Corrected witnesses use fresh event
and record IDs, current timestamps and the appropriate actual stage. They require
the protocol-program refusal, not the ledger's malformed-history exception, so
duplicate-ID or chronology failure cannot masquerade as this binding proof.

## Final evidence

The from-empty Shop integration has **106 ledger events**, two actions, four real
TYPE judgments, four real direct-grant judgments, two separate epistemic decisions
and authorizations, two dispatches, two synthetic terminal receipts and two
independent-role observation records. The intervening ordinary Shop correction
leaves five knowledge change sets and one contract revision. Current supplier
quantity is two; the prior quantity-one record remains explicitly superseded.

The new suite passed **13 tests**, no skips, in 288.49 seconds. The original
Shop-action, owning-history and keyed-instruction regression passed **45 tests**,
no skips, in 158.79 seconds. The fresh-process test denies every `research` and
`tests` import and recovers the same ledger head/count, graph and protocol digest.

Exact commands in the configured project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/action_history_contract_freeze/programs/test_sequential_profile.py research/action_history_contract_freeze/programs/test_sequential_history.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/action_history_contract_freeze/programs/test_shop_action_composition.py tests/contract_compiler/pareto/test_finite_protocol_history.py research/action_history_contract_freeze/programs/test_keyed_effect.py
```

`research/action_history_contract_freeze/sequential-verification.json` records
this exact run. It is historical evidence, not a live golden that future producers
must impersonate. Source and governance commits bind the coordinate separately.

## Consumer cut and remaining work

Authoring entry: `programs/sequential_bundle.py:add_sequential_actions`, taking
the existing complete reference bundle. The existing public
`KnowledgeChangeHistory.select_protocol_programs`, `append_protocol_events`,
`replay` and `reopen` execute the retained result. No Python executor instruction
or domain transition branch was added. The existing single-action definition is
unchanged. Choose the new profile before the first action; this does not migrate
an already-selected single-action history.

This closes the bounded sequential-profile proof. It does not implement a robot
or supplier adapter, execute an external effect, prove an observation true, add
Semantic Re-entry, or generalize the two-monitor reference arities. Handling
non-executing decisions, retries, concurrent actions, dynamic instruction-level
lookup, profile migration and a consumer authoring SDK remain future work.

Self-review: the rules reside in identified optional profile data; historical
indexes and records remain intact; knowledge changes use the existing KCS path;
payload identity is not payload meaning; an observation must belong to the active
action; and replay invokes no producer. Runtime, ontology, package configuration,
original lifecycle definitions and historical receipts are unchanged. No network,
installation, downstream edit or remote push was performed. The unrelated older
historical Shop comparisons are outside this slice, so full repository GREEN is
not claimed.

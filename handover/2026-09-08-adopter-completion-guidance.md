# Adopter completion and permission boundary

Luis requested this generic prevention rule through the paper coordinator.
Core owns both skills and their validation; no paper artifact or producer run
is part of the change.

## Bounded contract

Role: `REFERENCE_IMPLEMENTATION` guidance for an adopter-selected workflow,
with a `CONFORMANCE_FIXTURE` for the existing capture-accounting limit. This
is not a new protocol invariant, evaluator or mandatory report grammar.

1. Claim: before dispatch, compare the intended outcome with permitted edits,
   inputs, feedback and budget. Preserve specific unresolved gaps instead of
   reporting an inventory or finished attempt as substantive completion.
2. Observation: the installed Core skill reaches the shared adopter rule; a
   neutral captured relationship blocked by task permissions still yields a
   mechanically valid no-change plan with that exact unresolved gap.
3. Reuse: existing skill installer, source-coverage guidance, bounded revision
   loop, document adapter and neutral plan compiler. No new evaluator.
4. Exclude: judging source entailment, automatically validating task permission
   or substantive reconciliation, extending budgets, authorizing edits, running
   producers, changing runtime/ontology/policy, rebinds, release or push.

The navigation/installed-byte guard verifies instruction delivery only. The
runtime test verifies accounting and retained gap data, not model obedience or
semantic completion. No current Core mechanical surface supplies that latter
judgment.

## Implementation and evidence

Test-first commit: `4d7511fb4335dcade5189e3e420dff030d53aaa9`.
The installed-reference test failed because the pre-dispatch link was absent;
the accounting counterexample already passed. This is **one delivery failure
and one pass**, not a failing semantic evaluator or a production defect.

Guidance commit: `d1125f6a196bd7892feae4320ec22d5f2171d474`, tree
`2720458e2a17dabac8099cb8affe8addc615ac71`. Exactly two skills changed:

- `.claude/skills/malleus-acolyte/SKILL.md`: the shared outcome/permission rule,
  linked from the existing revision loop. SHA-256
  `a7508dee74b0b1e9e1dde8ce021e6a509408e13165081093e6497b8d9f127deb`.
- `.claude/skills/malleus-dev/SKILL.md`: a short reference from the existing
  pre-dispatch gate. SHA-256
  `30ee132553f4eb42943161f858457bf6f6050d93793cd1255b1cc5006eecc96f`.

The synthetic source says A links to B. Its explicit gap names the missing
`ObjectLink` endpoints and the task's prohibition on relationship edits.
The public adapter reports one reviewed block and one unformalized assertion;
the compiler returns `NO_DOMAIN_CHANGE` with zero operations. The exact capture
and gap survive. It does not infer permission, repair the relationship or decide
whether the objective was achieved. This test exercises existing accounting,
not semantic reconciliation, admission or a producer's response to instructions.

Both new tests plus the existing capture-boundary suite passed **8 tests**.
Ruff, formatting and both skill quick validators pass. The configured shared
checkout also passed all **108 Inquisitor tests**.

In a clean detached local clone of the guidance commit, the exact combined
selector passed **115 tests, one skip**, with an empty final Git status:

```sh
git cat-file -e 3ec7192df52107300eef69a4476b6fa70f84a2bb:src/malleus/kg.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -rs --tb=short -p no:cacheprovider tests/contract_compiler/pareto/test_adopter_completion_boundary.py tests/contract_compiler/pareto/test_capture_coverage_boundary.py tests/test_inquisition.py
```

The skip is the optional private doctrine, absent from committed bytes. An
earlier archive-only run failed the existing historical Git-object guard;
the detached clone supplies those objects rather than bypassing the guard.

The tests invoke the real Codex project installer into a temporary directory,
compare both installed skills byte-for-byte and resolve the installed Core
skill's link to the adopter section. This is not a wheel build, a global skill
refresh or proof that a model obeys the rule. No runtime, ontology, policy,
consumer rebind, unlimited retry, new evaluator or report grammar was added.
Source faithfulness, coverage and mechanical acceptance remain separate.

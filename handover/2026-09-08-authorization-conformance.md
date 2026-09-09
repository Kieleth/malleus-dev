# Authorization comparison, bounded Core work

## Approved scope

Luis selected fundamental Core work after moving Shop development to another
task, then approved the authorization comparison. This is evidence for the
existing handwritten-Assent replacement item in the
[Core backlog](2026-09-08-core-backlog.md), not a new migration or workstream.

Role: `CONFORMANCE_FIXTURE`. Lowest affected profile: the existing optional
finite action authorization profile and its `ASSENT_AUTHORIZATION_CONTROL_V1`
capability. Adopters not selecting that profile acquire no new obligations.

1. Claim: both existing control entry points obey the documented authorization
   outcome rule for two authority monitors, including precedence, trigger order
   and independence from supplied assessment order.
2. Observation: run all nine outcome pairs against a literal answer table,
   through the standalone evaluator and finite executor. Deliberately corrupt
   a shared verdict rule and prove that the table detects it even when both
   entry points agree.
3. Reuse: existing neutral monitor/policy/assessment builders, finite executor,
   control capability, and authenticated authorization history tests.
4. Exclude: a production Assent cutover, new policy semantics, a second
   interpreter, a public wire, Shop or consumer edits, and packaging work.

The outcome rule comes from
[Assent's replay contract](../docs/ASSENT_PROTOCOL.md#replay-derived-state):
all satisfied means AUTHORIZE; any violated means BLOCK; otherwise an unknown
means CLARIFY. Both violated and unknown assessments remain in the ordered
trigger list, including when BLOCK wins.

## Findings

Inspected base: `55c038438ed67197b7e3345b9c80a885a7b6cf17`.
No production defect was demonstrated. The existing control comparison had a
testing limitation: it used the same calculator to generate expected and actual
outputs. Its module description also called that recipe independent. The
description is corrected and the new answer table does not call a calculator
to produce expected verdicts or triggers.

| Responsibility | Standalone Assent | Finite action path |
|---|---|---|
| Accepted proposal, exact action, current context and terminal state | Python replay guards | Declared program resolves applied records, compares context and stages transitions |
| Assessment coverage, actor, policy and monitor bindings | Replay guards plus evaluator | REQUIRE_COVERAGE plus SELECT_CONTROL capability |
| Outcome precedence and trigger selection | Python evaluator | The same Python evaluator through a named capability |
| Grant actor, permitted action type and interval containment | Python replay guards | Declared comparisons and REQUIRE_INTERVAL |
| Source dependencies, record introduction and atomic publication | Owning ProtocolLedger | Owning KnowledgeChangeHistory and finite program execution |
| Grant legitimacy and scope meaning | Adopter policy and assessments | Selected authority policy/checks, not inferred by the generic executor |

Inspection sources: [standalone authorization](../src/malleus/assent.py),
[declared authorization builder](../research/action_history_contract_freeze/programs/authorization_bundle.py),
[control capability](../src/malleus/_contract_pipeline/finite_control.py), and
[shared calculator](../src/malleus/control.py). The table is a code map, not a
claim that every possible authorization history has been compared.

The finite profile is intentionally narrower: exactly two authority monitors,
one epistemic decision, no relied-on claim versions, one grant even for a
non-authorizing decision, and bounded authorization intervals. Standalone
Assent supports broader forms. These differences are not corrected silently
and prevent claiming the finite profile as a complete replacement.

## Executable evidence

The [literal table](../research/action_history_contract_freeze/programs/authorization_conformance_cases.json)
and [neutral tests](../research/action_history_contract_freeze/programs/test_authorization_conformance.py)
add 30 checks:

- One check that all nine outcome pairs occur exactly once.
- Eighteen checks of the nine pairs in both input orders. Both entry points
  must match the authored verdict, policy-ordered assessment IDs and trigger
  IDs. Execution must leave inputs and supplied protocol state unchanged.
- Eight shared refusal cases: missing/duplicate output, stale head, wrong
  action, actor, policy hash, monitor hash or monitor version. Each entry point
  must return its existing typed error and leave inputs unchanged.
- Three injected-fault checks, one for each verdict. Both entry points agree
  on the deliberately wrong result, but the independent expectations reject it.

There was no production RED or production GREEN change. The discriminating
failure is a test-local mutation of the shared rule, restored by pytest. This
is conformance-test strengthening, not a fabricated runtime bug fix. Expected
hashes are still compared between the two paths, not independently specified.

Focused command, using the existing project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/action_history_contract_freeze/programs/test_authorization_conformance.py research/action_history_contract_freeze/programs/test_control_executor.py tests/test_control.py
```

Result: **123 passed**. Scoped Ruff and formatting checks pass.

Separate owning-history regression command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_protocol.py research/action_history_contract_freeze/programs/test_authorization_history.py
```

Result: **251 passed**. These are the existing standalone protocol and finite
authorization-history suites, not 251 new comparisons. The finite history suite
reuses its existing fixture; the new answer-table tests are domain-neutral.
Together the two selections pass **374 tests**, including the 30 new tests.
This is not a new full-repository or packaging gate.

## Remaining foundation, not activated here

The immediate next design cut is the authorization control capability itself:
specify its outcome mapping, precedence, trigger selection and evaluation-hash
contract as identified data before replacing its Python-specific policy logic.
Reuse this table as the first acceptance corpus. Do not change existing policy
identities or old history interpretation implicitly. Full transition parity
and deletion of the old production path remain later gates.

This slice does not establish cross-language execution, a second conforming
implementation, full authorization-history equivalence, monitor execution or
trustworthiness. No Core runtime, public API, ontology, installed package, Shop
fixture or downstream consumer changes.

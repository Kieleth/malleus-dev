# Finite action definition: review handoff

Status: REVIEW_REQUIRED. The definition packet and its shape tests are complete
for independent review. The executable action contract is not complete or
approved. No runtime, producer, actual action context or lifecycle proof is
supplied by this packet.

## Read in order

1. [Definition and unresolved choices](DEFINITION.md).
2. [Context shapes](contexts.schema.json): initialization and immutable original
   proposal context; full history, domain and action coordinates stay separate.
3. [Finite instruction shapes](instructions.schema.json): ten bounded operations,
   explicit operand paths and refusal names; no arbitrary code or direct KG write.
4. [Check-producer binding shapes](capabilities.schema.json): TYPE and direct-grant
   semantic inputs, separate contract and implementation references, pure effects.
5. [Byte bindings](definition-inputs.json) and [tests](test_definition.py).

The byte-binding file is review metadata, not a second protocol artifact or
ledger. Its local-file table covers the definition, schemas and tests. Its own
bytes and this report are identified by the enclosing Git commit. The upstream
semantic documents are pinned at f221c099; their older compiler-blocked wording
is superseded by the separate completed compatibility packet at ff0e1b3.

## TDD and exact evidence

Initial RED: `0706a55c74edfe4ded1007b32c37e526b44ed048`, 24 failed and
2 controls passed before the schemas existed. A copied test-file digest was
caught while assembling the byte bindings. The added hash/omission guard is in
RED `c9c122841e084163f8335be81500967b759f244f`; a clean detached checkout of
that commit reproduces 26 failed and 2 passed because the schemas and binding
file are absent. No failure was marked xfail or skipped.

Definition GREEN: `1a34d48f0b6f105bcb1d5af460d5c9ff23c5fa0e`, tree
`b9f6f7714cc1e7d058b58a81207e3171963eb989`. A separate clean detached checkout
at that exact coordinate passed the following single selection: **140 passed,
zero skipped**. It contains 28 definition tests plus the existing compiler and
compatibility-gate controls. Ruff, format and diff checks passed; the detached
checkout remained clean. The report commit adds only this file.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider \
  research/action_history_contract_freeze/test_definition.py \
  tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
  tests/contract_compiler/pareto/test_contract_alternatives.py \
  tests/contract_compiler/pareto/test_public_compiler.py \
  tests/test_assent_ontology.py \
  tests/test_compiler_compatibility_gate.py --tb=short
```

Execution used the existing configured project interpreter at
`/Users/luis/Projects/malleus-dev/.venv/bin/python`; no packages were installed.
JSON Schema validation uses the already-declared development dependency.
Source and evidence binding checks perform no network lookup.

The current public machine parser explicitly refuses the proposed grammar in
the tests. The remaining tests check shapes and identity bookkeeping, not
state transitions or whether a check producer is honest. In particular, a
syntactically valid implementation digest does not prove executable bytes
exist. Both real producer implementations remain UNBOUND.

## Required review and next dependency

Review the newly explicit context-registration/proposal ordering and the exact
instruction/operand vocabulary. Neither was silently promoted to accepted
runtime behavior. Then close the event programs, static operand/index
resolution, monitor invocation/output metadata, and referenced interval,
scope-association and current-context content contracts. The existing full
Assent record contract remains the output authority, not these shape schemas.

Real TYPE and direct-grant producer bytes, their identities and conformance
tests are absent. So are a new interpreter, real initialized contexts, and the
one-history action lifecycle corpus. Do not manufacture those inputs or label
this packet an executable freeze. Runtime implementation still requires its
own reviewed boundary and authorization.

## Scope and self-inquisition

All seven created files are under `research/action_history_contract_freeze`.
Production source, ontology, package configuration, existing tests/scripts,
Small Shop, paper and governance files are byte-unchanged from ff0e1b3 by Git
comparison. Shared main was not edited; nothing was merged or pushed.

`protocol_role_is_explicit`: a proposed OPTIONAL_PROFILE definition, tested by
a CONFORMANCE_FIXTURE under the approved bounded one-consumer exception.
`optional_profile_stays_optional`: no default structural bundle or standalone
Assent meaning changes. `protocol_authority_is_data`: instructions are proposed
data, not an opaque callback or a hidden handler implementation.
`single_ledger_knowledge_change`: context shape separation does not introduce
another log, KCS identity or accepted-graph writer.

This is not a full repository or package gate, a consumer rebind, portability,
replacement, policy legitimacy, source truth, external execution, or an E2E
action result. The repaired compiler's nine historical exact-receipt failures
remain visible in GATE.md; this definition slice does not rewrite or hide them.

## Independent review and RED-ordering clarification

The separate Re-entry review at `86c624934b88fd31cdc1286f29249534baeaa238`,
tree `f0043806b922c7b8eeb8f7c78699068a58562fe3`, reproduced the exact 140-test
selection on packet `63e1c3b`, with zero failures, errors or skips. Its report
`research/semantic_reentry_external_design/CORE_DEFINITION_REVIEW.md` is bound
by SHA-256 `8f11fd3d295051d5cd67ca492702363bf3649cb2e47f993d6fb1aa1c4f004151`.
Core read that report and verified its digest and commit/tree. The review
passes definition integrity and the reported shape-only scope; executable
readiness stays open. Its synthetic probes confirm declared shape limits,
not action behavior or new repaired runtime defects.

The requested wording correction is guarded by RED `4be731f`: the targeted
test failed before the edit. Implementation identities and live contexts gate
successful executable freeze, not genuinely failing tests. Reviewed semantics,
fixtures and expected refusals precede implementation; missing implementations
continue to refuse real runs. No runtime work is authorized by this correction.
The complete 140-test selection passes again after the correction, with zero
skips; Ruff, format and diff checks pass. The local byte bindings are updated
to the successor definition and test bytes.

Adjacency remains an operator decision, not accepted by the independent
recommendation. The next program packet must state whether context registration
and proposal share one atomic batch. If separate commits are allowed, it must
define orphan-registration behavior after refusal. No transaction shape,
cancellation, retry or orphan recovery policy has been selected. The ten
operations stay candidates until complete event programs demonstrate sufficiency.

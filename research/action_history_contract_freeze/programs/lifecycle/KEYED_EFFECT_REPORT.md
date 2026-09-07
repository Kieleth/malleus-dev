# Explicit keyed assignment: definition complete

Status: implemented in the research definition and static checker only.
The action runtime is not activated or implemented by this slice.

Luis approved the refinement after checkpoint `8d341b0`. The decision is in
`KEYED_EFFECT_DECISION.md` and the current definition's accepted-decision list.
The earlier `REPORT.md` remains the immutable pre-approval checkpoint report.

## Coordinates and scope

- Base: `8d341b0c1f323f2bcace30a2e14a7768d848bfe6`.
- RED: `e4f88cd2b9ddaf7466cf155ed468a0734ed6bf42`.
- GREEN: `e11fd463957082410491ffcb93178fcb7b784a35`.
- GREEN tree: `989d0e2bf7ade3415578592e23bda6d2e6f73530`.

All 13 changed paths are inside `research/action_history_contract_freeze`.
The implementation updates the research validator, instruction schema,
explicit fixture keys, tests and current decision/document bindings.
No production path, ontology, package,
main checkout, shared governance ledger or adopter repository changed.
Nothing was merged, pushed or installed.

Exact GREEN SHA-256 identities:

| File | SHA-256 |
| :--- | :--- |
| instructions.schema.json | `6c61d2b56efdc2c8d2b4d32651f6116e6ed031499a6aa580f1fcf532f35310e4` |
| programs/packet_validator.py | `139f713bba1af7f8102a221172a33da4552274d51803c30d1edaf6eae8379685` |
| programs/lifecycle/execution.json | `867e8d8cc8e2ed48ce9dd243227ef144ff17fe9b7bcea716b241c7c442006698` |
| programs/lifecycle/KEYED_EFFECT_DECISION.md | `a6acc3e792cb3ef68c535109bd3e164ff48fae2c9d36355505c70a33c94204d9` |

## Observed tests

Core reproduced both commits in a clean detached local clone, with the existing
project environment, no network, bytecode or pytest cache writes. This was a
self-check, not an independent consumer audit.

The focused selector was `programs/test_keyed_effect.py` plus
`programs/lifecycle/test_execution_program.py` under the research directory.
RED: 19 failed, 9 passed, zero skipped. GREEN: 29 passed, zero skipped. GREEN
includes one additional current-approval/readiness guard.

The complete selected research/compatibility gate at exact GREEN passed
260 tests, zero skipped, in 17.64 seconds:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. \
/Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest \
-q -p no:cacheprovider -c pyproject.toml \
research/action_history_contract_freeze/programs \
research/action_history_contract_freeze/test_transaction_decision.py \
research/action_history_contract_freeze/test_definition.py \
tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
tests/contract_compiler/pareto/test_contract_alternatives.py \
tests/contract_compiler/pareto/test_public_compiler.py \
tests/test_assent_ontology.py tests/test_compiler_compatibility_gate.py --tb=short
```

Changed-Python Ruff and format checks, aggregate diff check and clean clone
status passed. The existing byte-binding test detected the expected changed
instruction digest during development; current definition bindings were
updated without rewriting prior commits or reports.

## What is now expressible

An index assignment supplies ordered string-key operands. The profile declares
their schemas and the entry's value schema. Static checking refuses absent,
malformed, unresolved, future-result, wrong-type and wrong-arity keys. Composite
keys preserve operand order. Indexed uniqueness checks share that key shape.
The old keyless index assignment refuses rather than falling back to inference.
Scalar action-head assignment stays keyless. Input definitions stay unchanged
on both successful and refused checks.

The complete 18-instruction receipt candidate is now statically valid. Its
explicit key is the receipt's dispatch ID and its value is the receipt ID.
Preserving all other entries, staging insert/replacement and atomic commit are
declared semantics. No index update or ledger transaction executed here.

## Completion boundary

Lowest affected role: research OPTIONAL_PROFILE; tests are CONFORMANCE_FIXTURE.
The Malleus development skill kept the approved refinement out of production
and kept fixture success separate from protocol/runtime authority.

Full-history input resolution, actual retained compiled-contract/dependency
binding, result-byte retention, remaining lifecycle variants, real check
producers and monitor bindings remain unfinished. This is not an authorization,
dispatch, receipt admission, external effect, accepted-KG write, persistence
proof or cross-language replacement result. Runtime implementation still needs
its separately reviewed scope and authorization. The supplier-model and
robotics coordination notices introduced no change to that boundary.

# Execution-receipt definition checkpoint

Status: PARTIAL, BLOCKED_KEYED_EFFECT. This is not a completed action program.

## Immutable evidence

Base: `7f2f850ff3eca10fc86edbe0a763761f90949344`.

RED: `a5f4b266e32a5697f808e2d53aae5b55509b04e0`.
The five new tests fail because the proposed program file is absent. This is
artifact-first RED, not a runtime failure reproduction.

Candidate: `911b16be7178bbfad55d434bc98c86a96776bcfa`.
Tree: `79f732634631de071b8f491da58fb95ded5456a4`.
The new tests pass with the retained candidate, including the requirement that
its unsupported keyed effect refuses. The complete program remains invalid
under the unchanged instruction grammar.

SHA-256:

- execution.json: `0344c0686af6d0ea4d31ae02d9ef1f3f54447ddd671329f53f5a655a480cb00c`
- test_execution_program.py: `9d0700ff7fd3572f3624db35340348d15330be1ad4d9d13f5334253c10e3dec6`
- KEYED_EFFECT_DECISION.md: `d6fd58737bd5b2587d5c1a59f2713b05695234cbaaf888450a8114a7ae6bf408`

## Reproduction

Executed from a clean detached local clone at each exact coordinate, using the
existing project environment. No dependency installation or network was used.
The RED selector is the single new `test_execution_program.py` file: 5 failed,
zero passed or skipped. The candidate's same focused selector passed 5 tests
in the working checkout. The following combined selector at the exact candidate
in the clean clone passed 236 tests, zero skipped, in 17.17 seconds:

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

Changed-test Ruff and format checks, base-to-candidate diff check and clean
clone status passed. This is a Core self-check, not an independent audit or a
full repository/package gate.

## What this establishes

The 17-instruction prefix has statically resolvable typed operands. It states
the selected event/actor/time/hash/reference and uniqueness obligations as data.
Concrete minimal dispatch and receipt examples validate against both compiled
Assent and the retained input schemas. A wrong dispatch-time type refuses.

The final effect cannot yet express which index entry to assign. Its candidate
`keys` operand refuses mechanically. The proposed refinement and its unchanged
transaction boundary are in `KEYED_EFFECT_DECISION.md`; they await Luis.

## Scope and non-claims

Lowest affected role: research OPTIONAL_PROFILE; tests are CONFORMANCE_FIXTURE.
Neither the example nor its defaults become a base protocol invariant. The
Malleus development skill keeps the newly discovered instruction decision
proposed, rather than implementing it as hidden Python logic.

No instruction schema, static validator, production code, ontology, public API,
main checkout, paper artifact or shared governance ledger changed. The only
changed paths are this report, `LIFECYCLE.md`, and the four lifecycle files named
above or in the RED commit. Nothing was merged or pushed.

No runtime program executed. The static fixtures do not authenticate replay
state, resolve actual retained contracts/dependency closure, check retained
result bytes, cover every optional record variant, establish monitor bindings,
admit a receipt, or prove persistence, atomicity, portability or replacement.
Full lifecycle programs and those bindings remain unfinished. Approval of the
keyed definition would not itself authorize runtime implementation.

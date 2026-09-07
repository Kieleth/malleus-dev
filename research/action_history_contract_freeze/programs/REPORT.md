# Action program definition handoff

Status: research static/content checks GREEN; complete executable event programs
NOT COMPLETE; runtime NOT AUTHORIZED. The context/proposal transaction choice
is CLOSED by Luis's decision at `4cf8efe`. No downstream acknowledgement is a
prerequisite for that decision.

## Exact delivery

Read `NEXT_DECISION.md`, `LIFECYCLE.md`, then `MONITORS.md` in this directory.
The first gives the one instruction choice found so far. The second is a full
lifecycle obligation map, not executable JSON programs. The third defines
monitor roles and output bindings, while keeping real producer identities,
verified input instances and static dependency records explicitly unbound.

The research validator checks declared operand paths and basic types for the
ten candidate instructions, result/dependency order, declared capabilities and
protocol-only state targets. It also checks interval contents, context/scope
shapes and monitor contract definitions. Input schema declarations are not
authenticated runtime records. No instruction executes. These callables live
only in `programs/packet_validator.py`; nothing is exported from Malleus.

The invocation schema validates explicit ordered references and metadata, not
the actual resolved input contents or computed output records. Real TYPE and
direct-grant producers are absent. The whole existing compiled Assent contract,
not this reference envelope, remains the intended record-validation boundary.

## TDD and reproduced evidence

Initial RED `ee19916` preceded implementation. Additional tests were committed
at `8d20044`, `7d1bb18`, `e045295` and final RED
`73ac0b50864f8ea37295d720501f90a622f83ae4`.
An isolated detached checkout of final RED reproduced **54 failed, 1 passed**
for the `programs` directory: the validator and definition bytes were absent.
The passing control validates existing first-revision absent/null behavior.
No failure was skipped or marked xfail.

GREEN is `e7ed30c8e075c070e22daf50ee17b5b17165180a`, tree
`a3edae8768e60632c3d6a4e91b5a7056102e286a`, directly after final RED.
A separate clean detached checkout reproduced **214 passed, zero skipped**:
55 new checks plus 159 preceding definition and compatibility controls.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider -c pyproject.toml \
  research/action_history_contract_freeze/programs \
  research/action_history_contract_freeze/test_transaction_decision.py \
  research/action_history_contract_freeze/test_definition.py \
  tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
  tests/contract_compiler/pareto/test_contract_alternatives.py \
  tests/contract_compiler/pareto/test_public_compiler.py \
  tests/test_assent_ontology.py \
  tests/test_compiler_compatibility_gate.py --tb=short
```

The interpreter was the existing configured
`/Users/luis/Projects/malleus-dev/.venv/bin/python`. No installation or network
was used. Ruff check, Ruff format check and aggregate diff check passed; the
verification checkout remained clean. The report commit adds only this file.

## Exact instruction gap

Existing `src/malleus/assent.py:1943` independently requires the action type to
belong to `grant.permitted_action_types`. The existing ontology declares that
field multi-valued. A test compiles the actual Assent closure and validates the
multi-valued grant. `missing-membership.json` retains an attempted IN comparison
and independent positive/negative values. The frozen instruction schema refuses
the attempt. A passing refusal test does not make the operation expressible.

Recommendation for Luis: one finite exact STRING membership instruction,
`REQUIRE_MEMBER`, with scalar and list operands and a typed refusal. It adds no
callback, expression evaluator, grant restriction or state mutation. It is not
implemented or accepted here. After the decision, complete the JSON event
programs and test their closure before reviewing a runtime implementation cut.
This is not a claim that membership is the only gap a completed program can find.

## Review identities and scope

SHA-256 at GREEN:

| File | SHA-256 |
| :--- | :--- |
| packet_validator.py | 8539270f8fef0a8b95130241a9c6e8d1c27d87f74d265c72f89c64abd885a00b |
| LIFECYCLE.md | f7bac83c6f47f5ea9ff8a6b51c716c660bc53ef632d0064e1e260fe8fe12487a |
| MONITORS.md | d750c39506aa55718f5180211360e4b1d4b096612bc90b21df0c460e80898877 |
| NEXT_DECISION.md | dbce26a315b488412b4e9b74d6dd62c40ecf882cf9a5143147f1f885415dd464 |
| missing-membership.json | d86b6952cb9ca4586685a9948cac4f53ff7a2b3ba08790cd82deb89951be93af |

The enclosing Git tree binds all schema and test bytes. From `4cf8efe`, changes
are confined to this new `programs` directory. Shared main, production,
ontology, paper, supplier data, package configuration and governance were not
modified. Nothing was merged or pushed.

The lowest affected role is a proposed OPTIONAL_PROFILE; the validator and
synthetic specimens are CONFORMANCE_FIXTURE evidence. This does not change a
protocol invariant or grant authority to a fixture. The Malleus development
skill kept runtime effects and check implementations outside this definition
cut. One history and KCS domain authority remain unchanged.

Non-claims: no executable freeze, transactional persistence proof, initialized
action context, computed assessment, dispatch, effect, independent observation,
E2E action result, replacement, portability, public API, consumer rebind or full
repository/package gate. The preceding compiler compatibility debt stays
visible in `../GATE.md`; these checks do not clear it.

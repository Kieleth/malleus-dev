# Canonical string-list definition evidence

The approved language addition is complete as a research definition and static
check. It is not an implemented action interpreter. The preceding pending
choice is closed by `SORTED_LIST_DECISION.md`; it needs no renewed approval.

## What changed

`REQUIRE_SORTED_UNIQUE_STRINGS` has three explicit fields: opcode, values and
refusal. Its required execution semantics are strict lexicographic Unicode
code-point ordering, uniqueness, complete string-list typing and no mutation.
Empty or singleton lists satisfy this check only. Nonblank/nonempty conditions
remain separate. Comparison, indexed uniqueness and capability schemas keep
their preceding meanings.

The static checker adds five lines to require an array with a declared string
item schema. It resolves operands through the existing path checker. It does
not compare actual list values or call Assent handlers. Field selection and
refusal names are explicit data in `registration-list-checks.json`, whose two
fragments select grant action types and monitor input IDs. These are typed
field projections, not full records or complete registration programs.

`sorted-list-cases.json` retains fifteen expected value outcomes for a future
interpreter. Eleven well-typed string-list witnesses are also checked against
the existing Assent helper, without mutation. Four malformed cases are frozen
requirements, not executed instruction results. The cases distinguish order,
duplicates, emptiness, case, whitespace, composed/decomposed Unicode and
code-point versus UTF-16 ordering. No normalization or silent repair is added.

## Exact lineage and checks

Base: `c72368d046b9cfc5fe571da583bc06c17152ba6e`.

RED: `2bcba0c44d49313c1eb5cc0d649628404f48244e`, tree
`e8054a2f2adf574b82c63bbb061c43d001e61054`. The focused selector below produced
**17 failed, 27 passed, zero skipped**. Fourteen new definition tests failed;
the expanded opcode/shape guards and stale test-file byte binding account for
the other three. The stale binding is bookkeeping evidence, not behavioral TDD.

GREEN: `e60810f4ed3389e8ded646feec6fb31f455ea6d7`, tree
`d7dcb9cfefd21b0f0de77535ef596fea12c596f9`.

Focused selector: **44 passed, zero skipped**.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider \
  research/action_history_contract_freeze/programs/test_sorted_list_definition.py \
  research/action_history_contract_freeze/test_definition.py --tb=short
```

The selected research/compatibility gate passed in both the owner checkout
and clean detached checkout: **375 passed, zero skipped**. This is not the
complete repository suite or an independent audit.

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

The configured interpreter was
`/Users/luis/Projects/malleus-dev/.venv/bin/python`. Clean verification ran at
`/private/tmp/malleus-sorted-list.QRbYc6/repo`, detached at GREEN. Git status
remained empty. Changed-Python Ruff and format checks and base-to-GREEN diff
checks passed. No dependency installation, network or package build was needed.

SHA-256 at GREEN, paths relative to the enclosing research directory:

| Path | SHA-256 |
| :--- | :--- |
| `instructions.schema.json` | `7f7bb23c4af8369eae7326873bb189d3546a5dcb9d31057dcae5cb9814dd54d1` |
| `programs/packet_validator.py` | `fa11fcae2cbbf64d27e7c3901ab38859c9d3e6cfcabcf17564a1925539424713` |
| `programs/SORTED_LIST_DECISION.md` | `e3466c3d4f5965c4a1b89cb67e1aafe68f7c057bfe34208c1f36e0121fd1abbf` |
| `programs/registration-list-checks.json` | `31ab2cc953deb73f94dd016545b36bee47bc1bbd2252f9a3e85bf51f42216851` |
| `programs/sorted-list-cases.json` | `7abbf5b523f6bcd2042c7d4c011f02e2db1f5c2062a80fe6fae7dd00e8a5a757` |
| `programs/test_sorted_list_definition.py` | `67c4f47cd9dc40ac802f61b45c0bd557833f145ad2db703c22cc420205bd67c3` |

## Scope review and remaining work

The Malleus development skill kept this at OPTIONAL_PROFILE definition and
CONFORMANCE_FIXTURE scope. The rule remains selected by the action profile,
not imposed on every domain ontology or every list. The generic static branch
contains no grant/monitor field selection. No unrestricted capability or
second authority was added. The original unsupported comparison/scalar-key
witness and prior report remain byte-identical historical evidence.

Full grant, monitor and policy registration definitions remain unfinished.
This addition removes one known expressibility gap; it does not establish that
every later lifecycle rule is expressible. Authentic input views, producer
bindings, preparation, atomic persistence and replay require later work and
their own evidence. The proposed read-only preparation implementation remains
outside this definition approval.

No proposed instruction ran, no history input was authenticated, and no event,
check producer, action or KCS was executed or appended. There is no new claim
of runtime refusal, transaction rollback, authorization, source truth,
durability, concurrency, E2E execution or cross-language parity. The entire
base-to-GREEN delta is nine paths under the isolated research directory.
Production, ontology, package configuration, shared main, governance, paper
and adopter files are unchanged. Nothing was merged or pushed. This report
is a subsequent documentation-only commit.

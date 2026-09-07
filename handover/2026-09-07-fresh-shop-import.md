# Fresh Shop import, then publication

Luis selected the fresh supplier-file proof before reviewing and publishing
the already-completed Core batch. This adds an adopter, not a Core feature.

## Bound slice and result

Role: CONFORMANCE_FIXTURE. The exact supplier grammar, identity mapping and
nonnegative-integer rule are ADOPTER_CHOICE, recorded in the sibling mapping
artifact. The selected OPTIONAL_PROFILE is state-version plus the existing
default structural-admission bundle. Nothing requires other adopters to use
this mapping, history model or ledger implementation.

The claim, dependency projection, pure/mutating stages, refusal boundaries,
replacement criterion and exclusions were recorded before implementation in
`research/ontology_driven_kg_realization/experiments/small_shop/fresh_import/README.md`.
No schema, runtime, public API, dependency, package or release change is made.

The complete existing Shop runs first. A new JSONL file supplies synthetic
orders SYN-C/X/3 and SYN-D/Y/5. Each row becomes one SupplierOrderState, with
four source-located fields, no inferred supersession and explicit NONE_STATED
valid time. The mapper receives source bytes and supplied identities, not a
history or graph writer. Mapping data loads at module import; the mapping call
performs no I/O. The coordinator retains exact source, mapping and adapter
bytes, prepares the neutral plan, then calls the existing admission helper.

After discarding live history and reopening from a copied ledger alone:
six change sets, one contract revision, twelve historical records, eleven
current records, 59 ledger events. The previous ten historical records remain
unchanged, including B/e4 and its B/e7 replacement. Both new records recover
the exact file and all four field locators. Two fresh executions produce
identical ledger and report bytes.

This does not establish source truth, epistemic acceptance, autonomous source
observation, supplier execution, automatic correction, Semantic Re-entry,
stable private wire or cross-implementation replaceability.

## TDD and findings

RED `c3829d9` records the source, mapping, contract and tests. Its twelve tests
fail because the adapter/coordinator are absent. GREEN
`747581b45bafa6a2f289be861e50e273905cff37`, tree
`9566ccdb98b34ca92c927ac8cd57a82c7da03808`, passes all twelve tests.

The tests include a changed input quantity, no-I/O mapping, eight malformed
row cases, actual public admission/reopen/trace, source and implementation byte
retention, deterministic repetition, unchanged prior state, stale admission
after an evidence-only append, and the absence of private Core imports or
caller-authored check outcomes. Invalid rows preserve exact pre-call ledger
bytes. Stale admission preserves the state after earlier evidence retention;
preparation and admission are not falsely described as one transaction.

Two integration mistakes were caught and corrected before GREEN:

1. The mapper referenced a non-exported grammar constant. Its mapping now
   names the documented private plan grammar explicitly. The live public-path
   tests guard against replacing API execution with string-only checks.
2. The mapping's root metadata used the plan discriminator `grammar`, making
   it look like a second plan in retained evidence. Core refused an ambiguous
   trace. The mapping now uses `plan_grammar` to describe its output, without
   claiming to be that output. The full trace test guards the distinction.

The original Shop fixture and predecessor evidence were not modified. A new
frozen report sits in fresh_import/evidence.json; each execution writes its
own output directory and refuses an existing destination.

## Validation

Environment: the repository's configured `.venv`, CPython 3.12. No installation
or dependency change. Executed in an isolated local clone, leaving shared
paper/research dirt untouched.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_fresh_shop_import.py
```

Twelve passed. The documented module command also ran successfully. Ruff and
scoped diff checks passed. The complete compiler Pareto plus Shop selection
passed 767 tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop --tb=short
```

In this local clone the interpreter was supplied by absolute path from the
configured workspace environment. The doc follow-up now executes the command
parsed from the fresh-import README rather than merely importing the runner.
That test and the repository example AST check passed. Strict HTML correctly
refused the new walkthrough before its governance digest was rebound. After
that rebind, strict HTML, repository example AST and current-ledger projection
checks passed together: three passed. The validator was not relaxed.

The exact final documentation/ledger selector is:

```text
tests/test_docs.py::test_strict_html_build_is_source_pure
tests/test_docs.py::test_repository_python_examples_are_ast_checked
tests/test_contract_compiler_ledger.py::test_overseer_ledger_and_projection_are_current
```

An initial invocation used a nonexistent ledger test name and collected no
tests. It was corrected from the actual on-disk test declaration; only the
three-test rerun above is evidence. No full-repository or package gate is
claimed for this fixture-only addition.

Frozen run coordinates:

- source SHA-256: `82f9db1da18a9187ed1c1839e761b719e63f64881e912264d631361325f419ea`
- ledger SHA-256: `c20c0c802b695a34983de1245b8f20cd3eba6ecbf2ce580ac213c316fe0cba7f`
- ledger head: `sha256:41fb98f6d364f1a61d1afbe3012730cf0d77c6d91fbe5b623962efbae8cea396`
- receipt identity: `sha256:cda391487e8088eea4d8780e4e183bff6058a2f934e55e15f3d1ee625218a8d1`

Publication review covers the existing local Core batch from remote main
`dfa367aee7848a69cf6999b158ba1a1057c50b38`: capture-accounting clarification,
explicit unstated time, read-only composition, refreshed historical evidence
and the default-admission guide. The current slice adds only new adopter
files/tests and a guide section. No uncommitted paper or unrelated research
bytes are included. Normal Git publication needs a narrow user exception to
the MCP-only server rule because the available connector cannot transport
the exact existing commit objects. No remote write has been performed.

While the Shop work ran in isolation, the separately approved Re-entry slice
landed at `c88e9a46a34b913528bbaa73c52e751d2db864a8`. Its task reports 1,321
passed plus one preserved historical xfail, followed by two smoke tests.
That result is not added to the Shop count. Its fifteen added paths are
research-only. Core runtime bytes are identical between that landing and the
base used here; the local merge preserves both exact histories.

## Scoped self-inquisition

`protocol_role_is_explicit`: fixture and adopter mapping, not universal rules.
`optional_profile_stays_optional`: no new requirement on Core or other adopters.
`protocol_authority_is_data`: existing contract/profile/bundle unchanged;
supplier choices are explicit mapping data and the implementation is retained.
`single_ledger_knowledge_change`: the new records enter one immutable change
through ordinary admission; replay alone derives the graph. These checks pass
for this slice. No root ontology rite was needed because no schema changed.

Future work remains bounded and unselected: explicit supplier correction,
another input format, external observer, or a separately demonstrated adapter
replacement. No new generalized mapping engine is justified by this example.

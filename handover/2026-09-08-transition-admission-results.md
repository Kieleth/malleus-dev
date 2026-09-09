# Selected transition admission: result

Core GREEN: `1385223eb274e63d98cc334d6dba6ecd54ed4007`, tree
`a0414f0b7ef53110683b19e9e3d14cac73bab30c`. The three-file production change is
`src/malleus/_contract_pipeline/machine.py`,
`src/malleus/_contract_pipeline/knowledge.py`, and `src/malleus/compiler.py`.

## Outcome

An adopter can now select an identified, pure restriction on record
replacement. The owning knowledge-history fold derives the exact transition
inputs and enforces the selected rule before candidate-state publication,
including on full replay and maintained incremental replay. A successful
caller-authored check event does not override it.

The optional machine grammar `malleus.protocol-machine/private-v1` adds the
closed rule section specified in the [plan](2026-09-08-transition-admission-plan.md).
The selected profile supplies role/type choices; the program supplies explicit
`EXACT` or `SUBTYPE` matching and refusal code. The interpreter has no Shop
class names or second replacement-type list. Referenced types resolve through
the compiled contract. Existing private-v0 artifacts keep their prior meaning.

No new public Python symbol was added. Existing
`create_structural_history` gains the explicit optional `transition_program`
keyword. It accepts only the rule extension of the exact installed structural
machine. `admit_structural_change` recognizes that extension and still generates
its own structural check events; caller-supplied outcomes remain absent from
the helper signature. Other custom machines still require their separately
selected orchestration contract, not this helper.

The public Shop fixture starts from empty history, compiles its real retained
ontology and e4/e7 source bytes, prepares e4, admits it, prepares its e7
replacement, then exercises both literal expected outcomes. With the shipped
state-version role `Entity`, `EXACT` refuses the concrete SupplierOrderState
replacement; `SUBTYPE` admits it and reopens at quantity 2 with e4 retained as
the predecessor. That is a test of explicit matching, not a recommendation
that every Entity should be replaceable. The adopter can bind a narrower role.

Neutral tests also prove ordinary Event addition, forbidden Event replacement,
allowed state replacement, renamed domain types, unknown/missing profile and
type bindings, stale coordinates, empty-role refusal and exact replay parity.
An adversarial test writes a valid envelope chain without the owning admission
check. Full replay, reopen and incremental refresh all refuse that forbidden
replacement; the maintained reader keeps its prior published state.

## TDD and verification

1. Contract freeze: `56639221`.
2. Initial RED: `29508f3b`, 26 failures at the absent machine rule section.
3. Corrected/helper RED: `57537d20`. The first implementation exposed two
   fixture mistakes: missing-profile evidence had removed all evidence, and
   the hostile-envelope test omitted the explicit validation bypass. Correct
   those inputs, then add three public-helper cases. On the partial runtime,
   26 passed and those three failed at the absent constructor keyword.
4. Exported immutable `57537d20` with no production changes reproduced all
   29 failures. No implementation bytes were copied into that archive.
5. GREEN `1385223e`: 29 focused cases passed. Ruff and formatting checks passed
   on all three changed runtime files and the new test file.

Commands use the existing declared project environment, with
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q
--tb=short -p no:cacheprovider` followed by these selectors:

| Selector | Result |
|---|---|
| `tests/contract_compiler/pareto/test_transition_admission.py` | 29 passed |
| `test_protocol_machine.py`, `test_knowledge_change_history.py`, `test_maintained_projection.py`, all under `tests/contract_compiler/pareto` | 152 passed during development |
| `research/ontology_driven_kg_realization/experiments/small_shop` | 246 passed |
| `tests/contract_compiler/pareto` | 738 passed during integration |

The broad regressions are development runs, not an immutable exported-tree
audit. The focused 29 cases were rerun after the final runtime cleanup. These
selections overlap and must not be summed into a unique-test total. This is
not a full repository or release gate. No package or dependency files changed.

The first documentation run returned 126 passed and 3 refused builds because
the changed compiler documentation had not yet received its successor journal
digest. The existing strict guard identified that exact planned revision;
no validator or historical entry was changed. Final documentation and ledger
rerun: **291 passed**, comprising 129 documentation tests and 162 overseer
ledger tests. This includes strict Sphinx HTML and doctest. The closing journal
validates 453 entries. Draft journal validation also rejected abbreviated Git
references; they were resolved to full object IDs before sealing. The existing
mechanical guards remain unchanged.

## Boundaries and handoff

This is a `REFERENCE_IMPLEMENTATION` for an explicitly selected
`OPTIONAL_PROFILE` of compiler-bound semantic history. Domain role selection
remains `ADOPTER_CHOICE`; the neutral and Shop cases are `CONFORMANCE_FIXTURE`.
Core adds no generic Shop vocabulary or default domain replacement policy.

The verified transition view is private and immutable. It contains exact KCS,
contract/profile and base coordinates plus prior/new types derived from the
owning prestate. It is not another persisted identity, ledger or graph. The
existing profile parser is reused at the history boundary rather than copied.
Only the owning fold can give that view its verified status.

Pure guards run on retained data. Existing external engine receipts remain
attestations; replay does not prove the engine ran, authenticate sources or
establish their truth. Earlier successful population preparation remains a
separate transaction; a later rule refusal preserves admission bytes but does
not erase the preparation evidence.

The connected-Shop task owns selection and its final consumer rerun. Its
current profile's descriptive correction string does not gain new semantics
automatically. Semantic Re-entry's isolated consumer evidence remains pinned
to its original Core source tree and requires a new compatibility receipt
before a later Core-owned landing. Neither consumer was changed here.

Excluded: general policy language, callbacks, arbitrary capabilities, full
history-profile interpreter, rule/profile migration, old-history rewriting,
Assent cutover, Event-to-state derivation, a second interpreter, packaging or
dependency changes, release and push. Other handwritten structural rules are
not claimed to have moved into portable programs by this slice.

# Retained inputs and atomic proposal: definition evidence

Status: research-local STATIC_VALID_PARTIAL. No runtime activation.

## What changed

The input-origin table identifies the existing applied records and retained
SourceArtifact bytes needed by the two selected checks. It preserves raw-byte,
semantic-artifact and protocol-record identities as different things. The
executor ID remains a scalar. The original context is available from earlier
staging only inside the approved pair; monitor invocation requires its applied
carrier. A retained current-context artifact names a verified historical
prefix, with current action/domain coordinates checked separately.

The context/proposal specimen has 69 existing instructions. It declares full
minimal SourceArtifact, LocalAction and ProposedSubgraph records and full
selected policy records. It checks coordinate types, explicit metadata/member
bindings, keyed protocol-state targets and staged dependency order. The
accepted transaction instance is included exactly, not changed. There is no
domain-state or action-acceptance-head write in this specimen.

No new instruction, Python executor, producer, public symbol or wire is added.
LocalAction is the existing synthetic compatibility type, not a new supplier
action contract. Optional record variants outside this finite specimen remain
outside its claim.

## RED and GREEN

| Commit | Observation |
| :--- | :--- |
| `fa3a272a33ed11ff06f7948bee9cd69dfc099bb4` | Initial RED: 10 failed because the two definition files were absent. |
| `40ee8aa45055cb3d1509317461705764603340c9` | Candidate plus compatibility RED: 2 failed, 11 passed. Existing policy references use the record hash; the candidate used the artifact hash. Its epistemic-policy shape also omitted six required fields. |
| `3d6b249754f5614d76832f6a84f04bebc6a42f45` | Further RED: 3 failed, 11 passed. Added a guard against equating episode metadata with independent action/proposal lineage keys without a selected rule. |
| `43ad32b6fc1492c134ffa3d949efa8ee75ff85f4` | Corrected GREEN: 14 focused tests passed. Tree `38ee23e4623d68512f34a12688b65ceb13b95c2e`. |

The initial role-order test was corrected to read the existing monitor table's
actual top-level keys. Before GREEN, a mechanical formatting error also
converted long explanatory strings to objects. Two failing type assertions
caught that class; GREEN preserves the values and keeps those assertions.
These were authoring errors, not production defects or new protocol choices.

Existing Assent evidence for the policy correction is `_proposal` and
`_artifact_ref` in `src/malleus/assent.py`: the latter compares `content_hash`.
The policy record shapes are checked against the real compiled Assent view,
including ruleset bindings and outcome/precedence lists. No fields are removed
to make the shape tests pass.

## Reproduction

Both the working checkout and a clean detached checkout of GREEN passed the
following selected research/compatibility suite: **345 passed, zero skipped**.
This is not the complete repository suite. The new file contributes 14 tests.

Use the already configured project environment, with no installation:

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

Actual interpreter: `/Users/luis/Projects/malleus-dev/.venv/bin/python`.
The owner and clean validation checkouts were respectively
`/private/tmp/malleus-action-contract.X6QNEw/repo` and
`/private/tmp/malleus-output-fields.vrZhR0/repo`. The latter stayed clean.
Changed-test Ruff and format checks and the aggregate base-to-GREEN diff check
passed. This is owner-run clean-snapshot evidence, not an independent audit.

Exact GREEN SHA-256 file identities:

| File, relative to `programs/` | SHA-256 |
| :--- | :--- |
| `lifecycle/context-proposal.json` | `303ad945a5415c3adf66b6abed34ee4e4eb3aa912c42caff3c50fb4e0365dc57` |
| `retained-input-origins.json` | `523fe2120410b880940ca74b26e8abf0d7d6d05fd6895b9b9fa992f3be231a79` |
| `lifecycle/test_context_proposal.py` | `73a54b338fc666ba0205c2fc3339b37484630df4da06989ac07ab1c9d067b041` |

## Remaining boundary and next executable deliverable

This closes one static specimen, not the entire event-program packet.
Initialization and prerequisite registration still need their concrete
declarations. The owning history must provide full applied record/index views,
authenticate original/current context and prerequisite byte references, bind
flat retention ID/digest fields to the complete SourceArtifact, and validate
the complete ordered source closure. Those obligations remain listed in the
data, not implemented as implicit Python decisions.

The current KnowledgeHistoryReplay exposes retained byte members and generic
machine state. That is not already a validated full Assent record/index view
for this proposed profile. In particular, caller dictionaries or syntactically
valid hashes must not be cast into such a view. Monitor producers and their
exact static dependency sets remain separately unbound.

The next executable target is a research-only **read-only preparation proof**:
from an owning verified prefix, resolve retained prerequisites, validate the
whole proposed pair and return staged records/index changes or typed refusal,
without appending either event. Its prerequisite is the remaining declaration
closure above. A synthetic static-schema pass cannot stand in for that proof.
Actual persistence follows separately, testing that an invalid second event
leaves exact prior bytes and state unchanged.

No additional semantic choice or opcode was found necessary for this static
slice. Executing instructions, resolving actual action-history state and
committing events remain outside this authorization. A bounded approval for
the read-only research interpreter would be needed before that implementation,
not an implicit activation by this report.

## Non-claims

Nothing here proves applied retention, authenticated replay inputs, monitor
execution, source truth, policy legitimacy, authorization, atomic persistence,
power-loss durability, concurrency, portability, supplier effects or a full
action lifecycle. No action or KCS ran. Existing public APIs, production code,
ontology, package configuration, shared main, Core governance ledger, paper
and adopter files are unchanged. No merge or push occurred. The enclosing
report commit supplies the final packet coordinate without rewriting GREEN.

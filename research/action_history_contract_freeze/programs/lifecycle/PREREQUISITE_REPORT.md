# Prerequisite registration definition evidence

The bounded definition cut is complete. Full registration conformance is not.
Four research specimens state the checks for registering a grant, a monitor,
an epistemic policy and an authorization policy. Their status is
`STATIC_VALID_PARTIAL`; no proposed instruction has been executed.

## What is now explicit

Each specimen retains the complete selected Assent record shape, metadata
bindings, record hash, global-ID check and introduction order. Grants bind the
grantor to the recording actor, canonicalize nothing, require a sorted unique
permission list and declare a strictly increasing finite validity interval.

Monitors and policies name their applied dependencies by record ID and record
hash, and require those dependencies in provenance. Policies distinguish
epistemic monitors from authority monitors. The epistemic ruleset's record hash
and artifact hash remain separate. Monitor and policy semantic hashes use
ordinary `HASH VALUE` after explicit comparisons of every varying preimage
field to its source record field. Authorization outcome controls retain the
existing fixed meanings.

The variants are a finite-ended grant, a monitor with two SourceArtifact
inputs, and policies with two monitor references. These counts and dependency
shapes are fixture choices, not new Assent limits. The preimage field map is
test-side definition metadata, not an executable mapper or new language.

Tests validate full shape/hash witnesses against compiled Assent and compare
preimages with the existing functions in `src/malleus/control.py`:
`monitor_specification_digest`, `epistemic_policy_digest` and
`authorization_policy_digest`. Distinct hashes expose swapped dependency
positions and swapped ruleset hash categories. These witnesses have no
authenticated applied history and are not claimed as admitted registrations.

The plan's initial phrase about hash-category refusal was too broad. The
static checker can reject an unresolved operand but cannot distinguish two
digest-shaped runtime values by their shape. The tests check the declared
paths and independent hash recipes; actual resolution remains a runtime duty.
The successor plan corrects that wording without changing the checker.

## Exact lineage and checks

Base: `016d0461077a080e83fbf7776cab3e4461d694da`.

RED: `e7c4ba6014f487114ccec608734dc195c6b03115`, tree
`d1a3c0fac1d502ccd9746a23db2ba36fea86a23c`.
The focused selector produced **22 failed, zero passed, zero skipped** because
the registration definitions were absent. This is definition TDD, not evidence
of runtime refusal. The exact RED was reproduced in the clean checkout.

GREEN: `448db9d83c8d9b7fd6aad5769a93cb0872296101`, tree
`229801583087df80d6f8f01265cc1a65b80e5c56`.
Focused result: **22 passed, zero skipped**. GREEN also strengthens the test
witnesses with distinct dependency hashes and correctly computed artifact and
record hashes; it adds no runtime implementation.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider \
  research/action_history_contract_freeze/programs/lifecycle/test_prerequisites.py --tb=short
```

The bounded research/compatibility gate passed in both owner and clean
detached checkouts: **397 passed, zero skipped**.

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

Interpreter: `/Users/luis/Projects/malleus-dev/.venv/bin/python`.
Clean checkout: `/private/tmp/malleus-prerequisite.Dx5hrG/repo`, detached at
GREEN. Changed-Python Ruff/format checks and base-to-GREEN diff checks pass;
the checkout remains clean. This is not a full repository gate, independent
audit, package test or cross-language execution result.

SHA-256 at GREEN, paths in this directory:

| Path | SHA-256 |
| :--- | :--- |
| `PREREQUISITE_PLAN.md` | `4aafe1f348fd29ff7f3f84d4433c63f234316395678577c29bf993ccf7adbfc7` |
| `test_prerequisites.py` | `01e4da0a98bea3dcd992b1403625825fe5a74559d39af33995c097bf6630f563` |
| `grant-registration.json` | `0bc466c442e89c85b696f9066d3e328d1ecf5887d1b54c0289183dcc179ad7de` |
| `monitor-registration.json` | `da2f7b41928b0521a193ef537f8ab69d210668f4414e672c5fdf03cd65799633` |
| `epistemic-registration.json` | `b768178857f53d6c80fe278bc2bf0d990d31bab63ed10f16fe2b25b607e8b6c6` |
| `authorization-registration.json` | `5c296bdf18701460b7207ae8416dc00650a980d53421a44814aac154100b1878` |
| `registration-nonblank-gap.json` | `9e56cc7d8daa95ed7e1d1a96b550233cdac3a27ce49573936e9c14cf76998ee5` |

## Limits and next dependency

The exact whitespace-only grant witness passes compiled record and JSON shape
checks but is refused by Assent's `_nonblank_values`. Sorting and uniqueness
do not close it. The gap artifact records the corresponding grant, monitor and
policy field obligations. No regex, normalization, callback, instruction or
typed capability has been added to conceal this missing constraint.

Other arities/optional variants, authenticated input views and source closure,
concrete monitor/policy instances, instruction execution, preparation, atomic
persistence and replay remain unfinished. Definition review must retain these
gaps before any interpreter can claim registration conformance. This report
does not select a new constraint mechanism or authorize runtime work.

The Malleus development skill kept this at OPTIONAL_PROFILE research and
CONFORMANCE_FIXTURE scope. No fixture became protocol authority. There is no
new execution, authorization, transaction, source-truth, durability or E2E
claim. Production, ontology, public exports, package configuration, shared
main, governance, paper and adopter files are unchanged. Nothing was merged
or pushed. This report, the corrected plan wording and the lifecycle status
update form a subsequent documentation-only commit.

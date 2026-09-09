# Authorization rules as identified data

## Approved cut

Luis approved the next step from the
[authorization comparison](2026-09-08-authorization-conformance.md): move the
verdict rules into an identified artifact, preserving existing behavior.

Role: `REFERENCE_IMPLEMENTATION` of the existing optional Assent authorization
profile. The finite action capability consumes the same implementation. This
does not change the base protocol or oblige other profiles to use this recipe.

1. Claim: outcome mapping, precedence and trigger membership come from exact
   identified data, not authorization-specific Python branches.
2. Observation: the existing nine-case answer table, frozen pre-change policy
   and evaluation hashes, generic-label rules, typed missing/corrupt-artifact
   refusal, and the existing owning-history tests.
3. Reuse: version-1 authorization policy identity already binds outcome mapping
   and precedence. Keep that hash preimage, assessment ordering, evaluation-hash
   recipe and public signatures unchanged. Read one pinned packaged resource
   before pure use, retain immutable parsed values, and do not add fallback.
4. Exclusions: caller-selectable policy semantics, new ontology terms, public
   DSL, a new ledger epoch, changed prior histories, Assent state-machine
   replacement, second interpreter, Shop or consumer edits.

The private artifact has a closed shape: grammar identifier, outcome-to-control
map, highest-first precedence and triggering controls. A generic interpreter
performs lookup, membership and ordered selection. Nonempty exact monitor
coverage remains a separate existing admission obligation. The default loader
pins exact resource bytes to the existing version-1 semantics; a different
artifact does not silently reinterpret a version-1 policy.

Dependencies remain in the existing Assent replacement backlog. The internal
rule interpreter consumes the identified control artifact; both the policy
digest and authorization evaluator consume its values; finite control calls
that evaluator. No new public stage or parallel policy authority is introduced.

## Implemented boundary

The ten-line installed
[`authorization-control-v1.json`](../src/malleus/authorization-control-v1.json)
is now the source of outcome mapping, precedence and trigger membership.
Exact identity:
`sha256:2164015909de89d798c80432b9239016b439cf56da54e33a56dd6a8b92d6817a`.
`malleus.control.AUTHORIZATION_CONTROL_IDENTITY` selects these bytes, not a
mutable file's current meaning. Missing, malformed or changed bytes refuse.
The loader runs at module import and caches immutable values, so evaluation
does not read resources.

The private
[`OutcomeControlRules`](../src/malleus/_control_rules.py) interpreter validates
the identified closed artifact. It maps each outcome, records every declared
trigger in monitor order, and selects the first present control in highest-first
precedence. Unknown outcomes and empty or unknown control collections refuse.
The interpreter contains no authorization outcome or verdict vocabulary.

Both existing authorization entry points use these values. The handwritten
mapping function and precedence branches are removed. Record binding, monitor
validation, grant checks, the evaluation-hash preimage and state transitions
remain in their existing implementations. This is not removal of every piece
of Assent logic from Python.

Compatibility has two distinct identities. Existing version-1 policy hashes
already include the mapping and precedence, and their bytes remain unchanged.
The full new resource identity additionally covers explicit trigger membership
and grammar. That resource is a fixed implementation dependency, not a new field
retroactively inserted into old policy or evaluation records. Arbitrary rule
selection is not exposed to callers. A changed version-1 file cannot pass the
fixed resource pin; a future different policy needs its own explicit contract.

## Evidence

RED: `77eaf346`, 23 expected failures and 71 passes. The failures identify the
absent artifact/parser/loader and the old mapping still being present. The
passing cases include nine pre-change evaluation-hash controls captured from
`f867e23b`; they are compatibility evidence, not an independent verdict oracle.

GREEN: `a7c54fa8`, exactly seven implementation/test/document/manifest files.
Shop-owned commits occurred between these checkpoints. They are not part of
this Core diff or its authorization evidence.

Commands below use the existing declared project environment. They disable
bytecode and pytest cache writes.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_control.py research/action_history_contract_freeze/programs/test_authorization_conformance.py research/action_history_contract_freeze/programs/test_control_executor.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_protocol.py research/action_history_contract_freeze/programs/test_authorization_history.py research/action_history_contract_freeze/programs/test_check_executor.py
```

Results: **160 passed**, then **273 passed**. The first selection includes the
prior independent nine-case answer table, exact old hashes, malformed-rule and
missing-resource refusals, non-authorization labels, and a test-local changed
precedence/trigger set which demonstrably changes execution. That injection is
test evidence, not a production override. The second selection checks existing
owning histories and real check producers. It is not a new full-repository gate.

Scoped Ruff and diff checks pass. A local build using the declared build backend
without build isolation produces an sdist and wheel; twine checks both. Both
archives contain the rule module and resource. The local wheel was installed
with no index, no dependency resolution and no bytecode compilation into a
fresh temporary target. Isolated Python selected that installed package,
verified its path and resource identity, and ran **99 control tests**, all
passing. Dependencies came from the existing project environment, so this is
not a fresh dependency-installation or complete package-profile claim.

Built artifacts, not published releases:

- Wheel: `sha256:35515a9d1ce8a86129996fe4ed3d1cc591b6c4d950f6ced4f5b16dcb28dfa738`.
- Sdist: `sha256:b5451910e29890c50f12d156b4b4b0d6c93254d84f3e4504bfc95ceefd70983f`.

The strict HTML check initially refused the pending package-manifest digest
before the append-only document revision. Its existing guard was not weakened.
The draft ledger explanation also exceeded its existing length limit and was
shortened before commit. Final checks pass: **180 ledger/CI tests** and **two
documentation tests**, including strict source-pure HTML and Python-example
validation. The ledger validates 451 entries. These corrections changed neither
runtime behavior nor validation policy.

## Non-claims and next dependency

No new release, ontology, policy schema, stable wire, consumer SDK, history
epoch, public override, monitor trust claim or cross-language conformance.
The resource is installed, not newly embedded into historical ledger records.
Two callers of this interpreter still do not prove independent implementation.

The next unfinished foundation is the remaining declared authorization and
transition contract, including its evaluation-hash projection and the broader
forms supported by standalone Assent. This slice does not activate that work or
quietly broaden the finite action profile.

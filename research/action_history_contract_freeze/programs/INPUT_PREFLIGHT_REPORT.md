# Supplied check-input preflight

Status: the carrier choice is accepted and research preflight is implemented.
Action runtime and retained-history binding are not implemented by this slice.
This supersedes the pending carrier selection in `INPUT_CARRIER_REPORT.md`,
not that report's historical evidence or outstanding runtime obligations.

## Exact coordinates

- Base: `407fbee93b40e4427c4e2756614cbc2d22f96e1e`.
- Selection: `f84c565be5a5ffd63c6aa11865ac7ee428bce0a0`.
- RED: `f17072f501876b84270c5ab0bfd569c62a4e764e`.
- GREEN: `6e6d2884cd3410f9b3d2877be264c075b1cfae30`.
- GREEN tree: `9e7e1a2c888a0511cf98e8cd20ad9c99236e4e0a`.

Everything remains in `research/action_history_contract_freeze/**` in the
isolated checkout. No production, public ontology/API, packaging, shared main,
shared governance ledger, paper or adopter files changed. No merge or push.

## What changed

`input-bindings.json` selects the existing SourceArtifact carrier for the
compiled record contract, scope association, requested interval, original
context and current context. It replaces the candidate table without a lookup
fallback. Each role still has a separate content parser. No new artifact kind
or public grammar was introduced.

The research function `input_preflight.validate_input_specimen` checks only
the supplied invocation's ordered role inputs. It uses the existing compiled
record validator, record hash, source-field constructor and content parsers.
It checks concrete record families, required fields, record IDs and hashes,
source artifact identity, byte length and digest, and role contents. TYPE's
record-contract bytes must exactly match the selected validation contract.
Explicit metadata and roles remain in the binding data. Nothing is fetched.

Tests construct full TYPE and DIRECT_GRANT specimens. Refusals cover missing
records or bytes, changed payloads, wrong or abstract types, omitted fields,
swapped identity categories, malformed content, caller-supplied outcome and
different compiled-contract bytes. Valid SourceArtifact identity alone cannot
make arbitrary contents valid for a role. Both success and refusal preserve
the supplied specimen.

The result is scoped to `INVOCATION_ROLE_INPUTS` and reports
`retention_verified: false` and `runtime_executed: false`. Monitor and
implementation references receive envelope shape validation only. No monitor
ran, assessment was produced, policy evaluated, action authorized, history
written or accepted graph changed.

## Reproduced evidence

A clean detached local clone reproduced RED: 23 failed because the new
preflight module was absent. GREEN adds four coverage cases, giving 27
preflight tests. The focused preflight plus carrier selector passed 38 tests
in the working checkout. These are not 27 independently failing RED cases.

The exact combined selector below passed 320 tests, zero skipped, in both
the working checkout and clean detached GREEN. Changed-Python Ruff and format
checks, aggregate diff check and clean checkout status passed. This is Core
self-validation, not an independent consumer audit or the full repository gate.

Run from the exact checkout using its configured project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest \
  -q -p no:cacheprovider -c pyproject.toml \
  research/action_history_contract_freeze/programs \
  research/action_history_contract_freeze/test_transaction_decision.py \
  research/action_history_contract_freeze/test_definition.py \
  tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
  tests/contract_compiler/pareto/test_contract_alternatives.py \
  tests/contract_compiler/pareto/test_public_compiler.py \
  tests/test_assent_ontology.py \
  tests/test_compiler_compatibility_gate.py
```

The actual interpreter was
`/Users/luis/Projects/malleus-dev/.venv/bin/python`. RED uses only
`programs/test_input_preflight.py`; the focused GREEN selector adds
`programs/test_input_carrier.py`, both relative to this research directory.

Exact GREEN SHA-256 identities:

- input-bindings.json: `c9d86db4748091b9c64e2ba42f8aa916f13f622c11f370aae0eb0551c6c0c3e4`.
- input_preflight.py: `3f729acb8926c3ca591b64f9a874babfa1ff4e0bf5110c9aba21226febf19989`.
- test_input_preflight.py: `9eef05e44d8c69934fa1f59b3d526b7ba443c970bdf0c0a1fd15981693b52b89`.
- INPUT_BINDING_DECISION.md: `9cabe3c12516dd8043f4cc5d0c78b9075b207470ebb51bb196c8a3720acfea6d`.

## Remaining boundary

A consistent supplied package is not an applied history. Still unbound:
retention events and prefix membership, content-ID associations, static
monitor dependencies, provenance ordering, current state, producer identities,
and lifecycle event programs. Dynamic inputs cannot silently become static
monitor dependencies. The next binding must resolve from the owning history,
not promote this supplied-record dictionary into another authority.

The Malleus development skill kept this an OPTIONAL_PROFILE research change
with CONFORMANCE_FIXTURE evidence. It prevented static inspection from being
reported as protocol execution or retained-history verification.

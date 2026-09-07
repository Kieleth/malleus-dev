# Check-output fields: static definition complete

Status: research definition only. No producer or action executor was added.

## Coordinates

- Base: `ba058d2b8505a6ac4648b1d65cb9b95af5891b19`.
- RED: `adabf0202bebffec138501816dbf70f072857cb4`.
- GREEN: `9d828a5aaac6320ffe9cd001a11ee2bc8fec72a9`.
- GREEN tree: `5d9ebba3317adaf20b57a551ff1f84f1f4f96b48`.

GREEN changes only the field census and `MONITORS.md`, following the separate
RED plan/test commit. This report is a successor record of those observations.
All changes stay under `research/action_history_contract_freeze/programs` in
the isolated checkout. No production, ontology, package, shared-main, paper,
adopter, or shared-governance path changed. Nothing was merged or pushed.

Exact GREEN SHA-256 identities:

| File | SHA-256 |
| :--- | :--- |
| monitor-output-fields.json | `d9132985598b0b48dc9d9bf24afd0dd80daf5b0e442f3a0e32b118919aa7c9be` |
| test_monitor_output_fields.py | `7cc21a997872a1f0e82b7903d61840a6546fc4b1ad745a02d8467f332254a15b` |
| MONITORS.md | `b0903362ecccddde9558b4488538c8b4c74d78d12d9a28793578639ba6c4eb71` |

## What was established

The census covers TypeAssessment, AuthorityAssessment, the TYPE and authority
MonitorFailure variants, UnavailableAssessment, and
UnavailableAuthorityAssessment. Shared groups preserve the same metadata,
proposal, monitor and authority origins across the failure pair.

Tests construct static specimens from labeled lexical witnesses. Each specimen
contains every required field of its real compiled Assent type, contains no
unknown field, and passes record validation. Removing any required field fails
that validation. The existing record-hash operation binds every selected field
except its own hash. These tests do not validate whole input records or prove
those inputs were ever retained.

Separate guards check monitor record hash versus artifact/implementation hash,
monitor version versus implementation version, proposal head versus current
action head, explicit event metadata, computed-output ownership, failure IDs
and shared context, and the exact evaluated grant on a violated authority
specimen. The test-only lookup raises on missing computed input instead of
filling a result. It does not compute a predicate or enforce runtime admission.

## Reproduction

Core reproduced RED and GREEN in a clean detached local clone using the
configured project environment, without network or installation. This is a
self-check, not an independent audit.

Focused selector:
`research/action_history_contract_freeze/programs/test_monitor_output_fields.py`.
RED: 22 failed, zero passed, zero skipped, because the census file was absent.
GREEN in the working checkout: 22 passed, zero skipped.

Exact clean GREEN combined selector:

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

Result: 282 passed, zero skipped, in 18.16 seconds. Changed-Python Ruff and format
checks, aggregate diff check, and clean clone status passed. No full-repository,
package, lifecycle, or Small Shop E2E run is claimed by this slice.

## Remaining work and non-claims

Field origin is now inspectable, but actual retained input wrappers and exact
input/source closure ordering remain UNBOUND. The census deliberately exposes
those unresolved origins. Its lexical witnesses are not authenticated records,
retention artifacts, computed assessments or evidence of authorization.

Next definition work must bind the real input categories and dependencies,
including the retained compiled record contract and scope/interval/context
contents, without relabeling them as unrelated artifact kinds. Complete event
programs and static checking remain required. Producer bytes, executable
initialization, interpreter implementation, atomic persistence, replay and
external effects are still absent from this research slice. No new runtime or
artifact-kind decision is made here.

The Malleus development skill kept the lowest affected role at research
OPTIONAL_PROFILE, with tests classified as CONFORMANCE_FIXTURE. The census is
not a protocol invariant, public grammar, alternate executor, portability
proof or runtime authorization. Existing transaction and instruction decisions
remain unchanged.

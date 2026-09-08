# Maintained history projection: results

The [approved contract](2026-09-08-maintained-projection-plan.md) is implemented.
This is Core's reference reader for the optional semantic-history profile.
It is not a new authoritative graph, policy, database or background service.

## What changed

The supplier example has an accepted quantity of one while the action runs and
the new source is observed. Only the admitted knowledge change makes the
accepted quantity two. A maintained reader now follows those committed steps
without executing the old history again. Its output matches full replay,
including source evidence, the superseded quantity-one record, action-protocol
state and every historical graph.

The partial-shipment example independently proves additive ontology revision:
retain the prior Shop, add shipment vocabulary, then admit two shipments. The
maintained reader follows the new contract and both shipments. Reopening JSONL
alone still reconstructs the same state.

## Public boundary

Import `KnowledgeHistoryProjection` from `malleus.compiler` and call
`KnowledgeHistoryProjection.open(history_path)`. After admission returns its
replay result, call `reader.refresh(expected_head_hash=result.ledger_head,
expected_event_count=result.ledger_event_count)`. Read the already-published
position with the same arguments to `reader.current`.

Both return the existing `KnowledgeHistoryReplay`. Graph queries, retained
inputs, record history and `trace_population_record` remain the existing read
surface. Returned graphs are defensive copies. Their local operation logs are
not history evidence; retained KCS and record history carry that evidence.

`current` performs no disk access. It refuses an unexpected full head/count.
`refresh` validates a committed suffix and publishes its graph, continuation
indexes and cursor together. Bad or changed prefix bytes, truncation, gaps,
duplicate IDs, incomplete admission or action transaction, and interrupted
staging leave the prior published view intact. A retry with a valid complete
history succeeds. No method writes accepted facts or the ledger.

## TDD and coordinates

- RED: `7c29da51`, eleven failures for the absent public reader.
- GREEN: `851913c0ccecb1a3e5445a9abd89072d8f486c27`, tree
  `fb37f24e44dcc51b1b47edc0e5b76072448be103`.
- Thirteen maintained-reader tests include the two full consumer examples,
  corruption, stale reads, isolated returned graphs, interrupted publication
  and incomplete action-transaction guards.

Core changes are limited to the existing JSONL envelope reader, graph staging,
knowledge-history fold, and one facade export. Full and incremental replay use
one semantic fold. The previous reconstruct-every-record application loop was
replaced, not retained as a hidden alternative. Existing structural refusal
semantics remain; the regression suite also caught and preserved the existing
missing-endpoint diagnostic wording.

## Validation

At the GREEN source bytes:

- Reader/history/KG/finite-program/Assent protocol: **469 passed**.
- Complete Shop research plus five Pareto Shop integration files: **253 passed**.
- Targeted Recon incremental/replay checks: **7 passed**, 129 not selected.
- Final governance/documentation/integration/status selection: **507 passed**.
- Scoped Ruff and diff checks passed. Formatting checks passed for the modified
  compiler/history/test files; unrelated whole-file formatting in the older
  graph and ledger modules was not swept into this slice.

All listed executions have zero skipped tests. The existing Shop evidence
generation passes unchanged. No receipt regeneration or identity exclusion was
needed. JUnit receipts are retained locally under
`/tmp/malleus-maintained-projection.5vcLbJ/` as `core.xml`, `shop.xml` and
`recon-read.xml`, plus the final `governance-docs.xml`.

| JUnit receipt | SHA-256 |
|---|---|
| `core.xml` | `143e128825b7f4f800beb7192a0586e89cfa3d53775a9032c0c5652a37b8a521` |
| `shop.xml` | `bae06f76668c50554d7157696fe21660d02272ea526799dc3fd3f1b324d9188b` |
| `recon-read.xml` | `2b85962b7a5068db3169444b05d04892cbc1907cd99eeee4fd052ca7b8b8b227` |
| `governance-docs.xml` | `de068bf9a5754904d4d052e2f99ae6b46736f9f60bf66d22d3e55f10dabf28ae` |

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_maintained_projection.py tests/contract_compiler/pareto/test_knowledge_change_history.py tests/test_kg.py tests/contract_compiler/pareto/test_finite_protocol_history.py tests/test_protocol.py --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_small_shop_default_admission.py tests/contract_compiler/pareto/test_small_shop_contract_revision.py tests/contract_compiler/pareto/test_fresh_shop_import.py tests/contract_compiler/pareto/test_default_shop_walkthrough.py tests/contract_compiler/pareto/test_partial_shipments.py --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_recon.py -k 'incremental or replay or ledger_edit' --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_governance_git_scan.py tests/test_contract_compiler_ledger.py tests/test_contract_compiler_integration.py tests/test_docs.py tests/test_status.py --tb=short
```

## Measured work and limits

The mechanical guard observes two new changes: exactly two new entity
constructions and eight new machine events, with only the exact appended bytes
decoded. Reading or refreshing the same position executes no events and
constructs no records.

One local timing observation used the completed supplier history, advancing
from 69 to 73 events. Full replay took 0.540 seconds, refresh took 0.050 seconds,
and an already-current read took 0.000036 seconds. These are single observations,
not throughput, cold-start, admission or persistence measurements. Initialization
and writes were excluded. The input has 15,881,950 bytes and SHA-256
`7e5f27170de460ea851511b5406b0e94341970a51a2a2bd1c5e49b97f4d61cbf`;
the suffix is 5,828 bytes. Both paths produced receipt
`sha256:fb0b7412f6d5b84c801d547a4950a9c553c7d0f0a0d9325ab33a6cddf81b42c7`.

Refresh still hashes the retained prefix because JSONL commits replace the file.
Defensive graph copies, continuation/index copies, canonical digests and receipt
snapshots still scale with state. Contract revision deliberately revalidates the
whole graph. Full replay initializes/rebuilds the reader. Optimizing these costs
or persisting a checkpoint is future work, not a reason to add storage now.

## Scope review

Self-inquisition: the lowest affected profile is semantic history. The reader
is a `REFERENCE_IMPLEMENTATION`; supplier and shipment scenarios remain
`CONFORMANCE_FIXTURE` inputs. Their business vocabulary did not enter Core.
An adopter without this reader retains full-replay semantics, but not maintained
read performance. No replacement projector, CompleteProjectionClosure wire,
source truth, external effect, multi-writer safety, package build, release or
remote push is claimed. Robotics and Re-entry still own their application use.

Append-only governance validates 440 entries at OVR-000440, head
`sha256:207250c5db25ee37352dde4942cdda1e1a051ae055dd38907b18197e1a65a14a`.
It binds the implementation, tests, selected contract and current status/backlog
without rewriting earlier entries. The closure changes no GREEN runtime byte.
The result report is a subsequent evidence receipt, not another state authority.

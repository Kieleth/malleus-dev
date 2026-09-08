# Supplier Semantic Re-entry: evidence and landing packet

Status: focused proof GREEN; unified 387-test gate and final delivery audit in progress.
This packet does not authorize a merge, push or publication.

## What this proves

The accepted synthetic source says e4/B/Y/1. The selected contract-local goal
requires B/Y quantity exactly two. The pure synthesizer proposes the existing
SupplierOrderAmendment ActionProposal subtype against pinned accepted state.
Real checks and authorization permit one controlled source attempt. An
independent observer captures actual file bytes. An ordinary observation-linked
KCS is separately prepared and admitted. Replay then yields the replacement
record and fresh evaluation emits nothing.

| Checkpoint | Accepted quantity | What it establishes |
| :--- | :--- | :--- |
| Initial source admitted | 1 | Accepted source-derived starting state |
| Candidate, TYPE/ACCEPT, authorization | 1 | Proposed and permitted action, not a changed supplier |
| Dispatch and execution receipt | 1 | One recorded attempt, not observed state |
| Independent capture and observation | 1 | Retained evidence, not accepted knowledge |
| Observed-source KCS prepared | 1 | A candidate, not an accepted correction |
| KCS admitted and history replayed | 2 | Accepted source-derived replacement |
| Fresh goal evaluation | 2 | SATISFIED, no candidate, retention or effect |

The new occurrence is `reentry-amendment-1`, never preloaded e7. O1, X1,
`contains:O1:X1` and all unmentioned accepted records/history survive.
The goal is order-record amendment, not delivery, available inventory or
demand fulfilment. Quantity three is valid source data but fails this goal.

A failed-after-write receipt may coexist with observed quantity two and an
accepted correction. The receipt remains FAILED; no causal inference follows.
A success receipt with unchanged source leaves accepted quantity one and the
episode refuses further work. One episode permits one candidate and one
attempt, with no automatic retry.

## Reproduce in the pinned research checkout

Dependency configuration is the existing `pyproject.toml` and its `dev` extra;
the compiler's identified offline environment is already configured by Core.
No dependency, installation, network call or paid service was added by this slice.
The executed environment used Python 3.12.9, LinkML/runtime 1.11.1, NetworkX
3.6.1, PyYAML 6.0.3, tzdata 2026.3, pytest 9.1.1 and jsonschema 4.26.0.
No clean-install or release claim is inferred from these test runs.

From the checkout root with its configured Python environment, the exact
selection comes from the checked manifest. A unique temporary directory keeps
other pytest sessions from deleting retained evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python - <<'PY'
import json
from pathlib import Path
import tempfile
import pytest

gate = json.loads(Path(
    "research/semantic_reentry_external_design/supplier-reentry-gate.json"
).read_bytes())
artifacts = Path(tempfile.mkdtemp(prefix="malleus-supplier-reentry-gate-"))
print(f"Retained test evidence: {artifacts}", flush=True)
raise SystemExit(pytest.main([
    "-c", "pyproject.toml", "-p", "no:cacheprovider", *gate["tests"],
    "-q", "--tb=short", f"--basetemp={artifacts / 'tests'}",
    f"--junitxml={artifacts / 'result.xml'}",
]))
PY
```

For the complete action path alone, select
`test_supplier_reentry.py::test_synthesized_action_observed_kcs_and_fresh_quiescence`.
It executes ordinary success, failed-after-write and unchanged-success cases.
Tests use real Core producers and admission; only controlled source-write faults
are injected. Expected-output files are comparisons, never observation inputs.

Existing public `malleus.compiler_cli query` and `trace` commands can inspect
the produced `history.jsonl` without running the synthesizer, executor or observer.
For example, pass `query --ledger <history.jsonl> --type SupplierOrderState`
or `trace --ledger <history.jsonl> --record-id supplier-order-state:B:reentry-amendment-1`.
The replacement exists only in the two supporting-observation cases.

## Exact scope and order

The integration branch is `codex/semantic-reentry-e2e`, based on Core
`90146c380994621a2f8df25876affd03fc9e57e3`, tree
`609979f5d356ebb43c1288d80ea8f4f53d1f2613`. Current production is
`a056077ea13955d9de3db7e98e54b973d0967bd4`, tree
`3fce91549bd58027b0fa49d37a4a9418dba17b11`. The selected gate is
`0d0773e6af51d9cbd20a836cea22484365aa0547`, tree
`aa435079fbd38b7d7c57de94a0feb9c04cadcac8`.

The dependency order is:

1. The verified Core one-history handoff.
2. Carried approved Re-entry contracts, case and pure components (`983629f`).
3. Supplier action schema/program, accepted read input and initial source.
4. Initialization, proposal/checks, authorization, executor and observer.
5. Observed-source KCS preparation and accepted-lineage read extension.
6. Pure contract/synthesis, linked episode closure and refusal repairs.
7. Compatible replay witness, unified gate and final evidence/audit packet.

Use the isolated branch's recorded order. Individual RED commits are evidence,
not independently landing-ready releases. Later Core work requires a target
diff and rerun of this gate before transfer; a clean source-tree match alone
does not certify changed experimental program builders or policies. No rebase,
cherry-pick or merge into another task's checkout has been performed.

All base-to-head changes are inside `research/semantic_reentry_external_design`.
The substantial cumulative diff includes the preserved design/audit history and
test-first stage commits, not changes to Core or paper work.

## Limits

This remains one research-local reference implementation. The action record
subtype is not new shared vocabulary. Program authoring and actual check
producers consume the reviewed repository-local Core experiment boundaries;
not every authoring helper is a public stable API. KCS preparation/admission
and replay use the existing public facade. No private graph writer exists.

Re-entry is goal-directed synthesis, not inverse replay or semantic decoding.
Canonical protocol values round-trip as bytes; different histories may yield
the same current graph. Model agreement is not PutGet about the world.
Interfaces select identified implementations, but empirical replacement by a
second independent implementation remains unproved. Multiple actions,
concurrent source writers, retries, real suppliers and robotics are excluded.

See `MALLEUS_INQUISITION.md` and `supplier-reentry-progress.json` for scoped
judgments, preserved failures and exact completed results. The final unified
result and file-hash manifest must be present before this packet claims delivery.

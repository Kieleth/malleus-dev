# Semantic Re-entry, one Shop episode

The question is simple: can a derived finding return as a constrained proposal
without gaining permission to write the accepted KG or execute an action?

This walkthrough starts with supplier order **B, product Y, quantity 1** and
an explicit goal: **make the supplier's order record say quantity 2**. The
synthesizer derives a shortfall of one and proposes an amendment. The goal is
contract-local input, not an invented customer-demand fact in the Shop KG.

## Run it

From this repository checkout, using its configured Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m research.semantic_reentry_external_design.supplier_walkthrough /tmp/malleus-shop-reentry-example
```

The output directory must not exist, and its parent must exist. Choose a new
name for another run. An existing file, directory or symlink refuses before
compilation. No input fixture is edited. Only the new output directory is
written, including its controlled `supplier.jsonl` file. An interrupted or
refused run keeps its partial artifacts; it does not retry or overwrite them.

Dependencies are declared in the existing root `pyproject.toml`, including its
`dev` extra used by these research check producers. This is a
repository command, not an installed-package command. It uses the pinned Core
and research-local adapters in this checkout, with no network or paid calls.
The fixed September 8 timestamps are reproducible fixture coordinates, not a
claim about when the command actually ran.

## What to watch

| Checkpoint | Supplier file | Accepted KG | Meaning |
| :--- | :--- | :--- | :--- |
| `accepted_start` | 1 | 1 | Initial source admitted, explicit goal is 2 |
| `proposal_only` | 1 | 1 | One pinned ActionProposal, no effect or ledger write |
| `executed_not_observed` | 2 | 1 | Authorized executor changed the local file, receipt is not a fact |
| `observed_kcs_not_admitted` | 2 | 1 | Independent capture produced a KCS candidate, still not accepted |
| `admitted_and_replayed` | 2 | 2 | Ordinary admission and replay expose the replacement fact |
| `quiescent` | 2 | 2 | Fresh evaluation returns no candidate and performs no write |

Those quantities and ledger coordinates are read at each stage, not printed
from an expected-output transcript. The command refuses if the measured
boundaries disagree. The program authorizes one controlled file amendment
under its explicit fixture grant. The synthesizer itself receives only its
immutable contract and read view, never the file path or history writer.

Open these files to inspect the actual run:

- `walkthrough.json`: six checkpoints, source/graph digests and ledger prefixes.
  This completion report exists only after all six stages succeed.
- `reentry-contract.json`, `original-context.json`, `action-proposal.json`:
  the exact inputs and candidate. The output is the existing
  `SupplierOrderAmendment` subtype of `ActionProposal`.
- `observed-source.jsonl`, `observed-change-set.json`: captured bytes and the
  ordinary `KnowledgeChangeSet` they justified proposing.
- `history.jsonl`: the sole authoritative history. The other files are
  inspection copies, not another authority. Each checkpoint also has a JSON
  file, useful if a later stage refuses.

The replacement occurrence is `reentry-amendment-1`. It supersedes e4 in the
current view while retaining e4 in history. O1, X1, `contains:O1:X1` and the
other unmentioned records and history remain unchanged. The historical Shop
e7 correction and the expected-after oracle are not execution inputs.

## Scope and reuse

Classification: `REFERENCE_IMPLEMENTATION`, a runnable composition of the
existing compiler-enabled state-version and experimental single-action history
profiles. Without these selected profiles, this composed guarantee is not
claimed. Checkpoint reports are diagnostic artifacts, not protocol vocabulary.

The core rule is broader than this example: derived output re-enters through
a pinned proposal. An epistemic correction can propose a KCS; an external
change must first propose an action. An action's model prediction validates
the proposed action, not the world. Execution success alone never closes the
knowledge loop. The actual source must be observed, mapped, admitted and replayed.

This proves a local order-record amendment, not delivery, available inventory,
customer-demand fulfilment, policy legitimacy, production supplier integration,
general planning or exactly-once delivery. One goal, one permitted action,
one attempt, explicit refusal, no retry. It adds no Core API or ontology term.
Different models, synthesizers and strategies have explicit boundaries; this
walkthrough does not establish replacement by a second independent implementation.

The original completed 388-test proof and its hashes remain unchanged. See
[the handoff](SUPPLIER_E2E_HANDOFF.md) for its negative cases and retained
evidence, including failed execution after a real write and success with no
source change. The new command is tested independently in
`test_supplier_walkthrough.py`, including a fresh process that forbids test
imports and oracle reads, pre-admission and final JSONL-only replay, and output
collision refusals. Its execution evidence is separate from the original proof.

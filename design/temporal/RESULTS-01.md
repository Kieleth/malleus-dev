# Temporal Core: first implementation result

This is local, uncommitted work on `codex/core-temporal`. It is not integrated,
packaged or released. All examples are authored synthetic controls.

## What works now

Core can reconstruct an earlier accepted state with the ontology, source
evidence and record history available at that exact point. Later evidence and
ontology changes cannot appear in that earlier result.

For example, first accept a reported price of 750 cents. Later accept a price
of 800 cents. Selecting the saved earlier position returns the original graph
and original receipt, including its evidence, even after closing and reopening
the history. A separate test accepts an ontology revision and confirms that
selecting the earlier position returns the earlier ontology too.

Core already supported old graph snapshots. The new capability is the complete
earlier replay context, selected without copying or truncating the stored
history. `KnowledgeChangeHistory.replay_at` checks the caller's selected and
containing checkpoints against one read of the ledger. It also validates the
containing history, so a valid old prefix cannot hide later semantic corruption.
Checks are relative to the supplied checkpoints, not an authentication service.

## What this does not answer yet

The new reader answers “what had been accepted at this position?” It does not
yet answer “what price applied on 5 May, according to what we knew later?”

The controlled baseline demonstrates why the distinction matters:

| Case | Existing behavior | Work still needed |
|---|---|---|
| Price changes from 750 to 800 on 12 May | The earlier record is retained and its period closes at the new start | Select the applicable state by domain date |
| A later report corrects the original 1 May price | Same-start replacement refuses | Explicit correction semantics, without inventing a 12 May price transition |
| Correct an earlier period after a later transition | Replacement of the retired record refuses | Correct that period without displacing the later state |
| A future price change is accepted early | Latest graph selects the accepted replacement | Keep acceptance separate from present applicability |
| Domain time is unstated | Unstated time is preserved | Do not interpret it as timeless or fabricate a date |

Calculations remain consumers. This work neither recalculates a result nor
turns a hypothetical execution into evidence for corrected reported inputs.

## Evidence

The new historical-read tests first produced **18 expected failures**, with
five existing-behavior controls passing. Each failure reached the missing read
method. Implementation reused the existing replay executor.

The final combined selector passed **337 tests**: both new temporal test files,
the capability declaration, documentation checks and compiler governance suite.
The new temporal files account for **30 tests** in that selector. Command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/test_capability_declaration.py tests/test_docs.py tests/contract_compiler/pareto/test_temporal_history.py tests/contract_compiler/pareto/test_historical_position.py tests/test_contract_compiler_ledger.py
```

Additional overlapping selectors passed for maintained projections, existing
history/revision/public compiler behavior and temporal precision. Exact counts,
the RED evidence and workflow errors are in [JOURNAL.md](JOURNAL.md). Do not sum
these selectors as independent tests. Ruff, formatting, ledger validation and
diff whitespace checks passed. No full Core CI or package gate has been run.

The earlier result reproduces its receipt and retained input set, refuses
incomplete admissions and finite transactions, and leaves ledger bytes unchanged.
The tests also cover a semantically corrupt later suffix with recomputed envelope
hashes. Arbitrary valid prefixes are not proof of separately persisted append
batches; use saved checkpoints from completed public calls.

## Next design boundary

The proposed next cut is correction of an existing period's account, not editing
its dates. Example: 750 from 1 May, 800 from 12 May, then a correction of the
earlier price to 775. Latest knowledge should yield 775 for 5 May and still 800
for 20 May. An earlier knowledge position must still yield 750 for 5 May.

This requires explicit correction lineage. Merely allowing equal timestamps
through the existing replacement guard would not implement it. The persisted
representation and treatment of relations need resolution before the next RED;
see [CONTRACT-02-DRAFT.md](CONTRACT-02-DRAFT.md).

# Contract compiler overseer ledger protocol

This directory contains coordination history for the contract-compiler
program. It records what happened, when, who had authority, why it happened,
and which stable evidence or design records support it. It is not semantic
design authority and it does not report shipped capability.

## Storage model

Each event is one immutable JSON block in [`entries/`](entries/). Splitting
events by file keeps reviews small and avoids one unbounded prose document.
Filenames, entry IDs, and sequences are contiguous: `OVR-000001.json`, then
`OVR-000002.json`, and so on.

[`ledger.schema.json`](ledger.schema.json) is the machine contract. Unknown
fields, missing required data, duplicate JSON keys, non-UTC timestamps, invalid
references, sequence gaps, and malformed type-specific payloads fail closed.
Decision blocks require the operator actor. A correction appends a new block
that points backward to the superseded entry; history is never edited in place.
Correcting a decision also requires the operator. If the removed entry affects
projected state, the correction requires a later typed replacement.

Each entry hashes its canonical content except `entry_hash`. The grammar named
`malleus-canonical-json-v1` uses UTF-8 JSON, Unicode text as written, sorted
object keys, no insignificant whitespace, and no nonfinite numbers. The digest
is SHA-256 with the `sha256:` prefix. `previous_entry_hash` creates the chain.

[`head.json`](head.json) pins the expected block count, final ID, and final
hash. It catches suffix removal while that separate local anchor remains
unchanged. It does not prevent a coordinated rewrite of blocks and head.
CC-000 will bind those values from the validated integration manifest, which
supplies the external anchor.

## Authority and scope

The canonical protocol graph owns accepted semantic design. The execution
program owns dependencies and gates. Decision documents own alternatives and
rationale. Evidence manifests own commands, commits, digests, and results. A
ledger block records the event and references those authorities instead of
copying them.

The overseer ledger accepts only cross-program events:

* operator decisions;
* workstream state transitions;
* material revisions to governing documents;
* verified facts that change the program;
* bounded observations and coordination acts.

Raw command output, test logs, full architecture arguments, and routine worker
notes stay in referenced workstream evidence. Each workstream will receive its
own ledger namespace under CC-000. A worker cannot write overseer decisions or
change another workstream's state.

Immutable verification reports live under [`evidence/`](evidence/). A ledger
reference pins the report bytes, not a mutable design document. Reports may
record the observed digest of a mutable artifact; the containing Git history
retains that historical snapshot once integrated.

Before sealing a new report, verify every reported byte length and source
digest against the working snapshot:

```text
python scripts/contract_compiler_ledger.py verify-evidence path/to/report.json
```

## Bounded projection

[`status.md`](status.md) is generated from the validated blocks. It contains
only the ledger head, current accepted decisions, current workstream states,
active blockers, and the latest ten events. Its size stays bounded as history
grows.

Repository validation uses:

```text
python scripts/contract_compiler_ledger.py check
```

After appending and sealing one reviewed block, regenerate the projection with:

```text
python scripts/contract_compiler_ledger.py render
```

The `hash` command prints the canonical digest for a draft whose sequence and
previous hash are already set. The next block and `head.json` must then bind
that result. `check` refuses gaps, forward references, broken transitions,
unresolved IDs, observations used as gate evidence, and projection drift.

These commands are development tooling. Their dependency is declared in the
`dev` extra. Sphinx may later render the same source data, but it will not
become a competing ledger.

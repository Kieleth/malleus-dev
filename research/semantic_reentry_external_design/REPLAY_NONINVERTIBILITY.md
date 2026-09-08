# Replay non-invertibility witness

Classification: CONFORMANCE_FIXTURE under compiler-enabled semantic history and
the existing state-version profile. No new protocol vocabulary or guarantee is
introduced. Without those profiles this test makes no claim.

Claim: the current accepted graph does not uniquely identify its protocol
history, even when both histories independently reopen and replay correctly.

Smallest observation: complete the existing source-backed e4-to-e7 correction,
copy its history as one independent conformance run, and append one explicitly
authored evidence artifact to the other run through public append_anchors.
Both current graph exports and accepted KCS sequences must remain identical.
The containing histories, head/count, receipts and retained evidence must differ.
Each run has exactly one authoritative JSONL history, never a second writer for
one run's accepted state.

Reuse: the unchanged real-Core Shop fixture, exact correction source and plan,
public preparation/admission, KnowledgeChangeSet serialization, and public
KnowledgeChangeHistory append/reopen/replay. The additional artifact is a
conformance note, not a supplier observation, goal, action or accepted fact.

Exclusions: no external action, new source capture, KG mutation, new update
strategy, alternative genesis policy, graph-to-history decoder or full external
Re-entry E2E. The earlier proposed genesis-at-two versus correction-to-two
witness remains reserved. This smaller witness is sufficient to falsify a
unique inverse from the current graph to the full history.

Exact protocol-value round-trip and semantic replay are tested separately:
every accepted KCS still parses to its original value and bytes. Both log
histories replay, but a graph-only inverse could not choose between them.
That is why a Re-entry Contract must bind accepted context and preserved
information, rather than treating a graph as a serialization of its log.

The expected observations are assertions in test_replay_noninvertibility.py.
An existing mechanism may already satisfy a new conformance test; this packet
must not fabricate a failing implementation or claim a repaired Core defect.
Executed results and exact coordinates follow.

## Executed result

The final run uses Core `2af45e03ee7d7bf528cef8db42c0798e6d99685b`, tree
`11704829d941e126424ee0e7138a74c8d2195b5b`. The retained compiled producer is
`sha256:51c019d49c3cd7d75330e02c5d728a873254cc4b56ca122dda078b15c25bcb3f`.
The two focused tests pass. The explicit relevant selection passes 112 tests,
with no failure, error or skip. The selection and observations are retained in
[replay-noninvertibility-result.json](replay-noninvertibility-result.json).

| Observed value | Short history | Extended history |
| --- | --- | --- |
| Protocol events | 28 | 29 |
| Current supplier record | B/Y/2 at e7 | B/Y/2 at e7 |
| Complete current graph | Identical | Identical |
| Accepted KCS sequence and record history | Identical | Identical |
| Complement and original supplier source | Identical | Identical |
| Authored conformance note retained | No | Yes |
| Ledger head, bytes and receipt | Different | Different |

Both histories reopen from directories containing only their JSONL file.
Every accepted KCS passes exact value/byte round-trip. Repeating the bound
witness reproduces its graph, history and receipt hashes. The logical conclusion
is narrow: a unique inverse from this current graph to the full log cannot
exist. Re-entry therefore needs information beyond the projected graph.

The first invocation passed its graph assertions but loaded Core from the wrong
checkout because pytest discovered the consumer's configuration. That run is
excluded from the selected-Core result. A session preflight now requires the
declared Core root, checks loaded module origins and the exact clean Git commit,
and the witness checks the retained compiler producer. Repeating the faulty
invocation refuses at setup before creating the Shop. A separate hard negative
test rejects another checkout. The successful invocation explicitly selects
the audited Core configuration with `-c pyproject.toml`.

From the exact Core checkout, with its existing configured dependencies:

```sh
MALLEUS_REENTRY_CORE_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. \
  python -m pytest -q -p no:cacheprovider --import-mode=importlib -c pyproject.toml \
  /path/to/semantic_reentry_external_design/test_replay_noninvertibility.py
```

Changed-file Ruff and formatting pass. Core stays unmodified. This is new
consumer conformance evidence, not a Core repair or an action-runtime result.
The earlier bounded compiler gate remains separate; its raw historical receipt
mismatches were not rerun or reclassified as part of this 112-test selection.

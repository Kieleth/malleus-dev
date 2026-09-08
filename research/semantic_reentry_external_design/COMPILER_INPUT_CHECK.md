# Independent compiled Assent input check

This CONFORMANCE_FIXTURE checks a prerequisite of the proposed action contract
under the compiler-enabled OPTIONAL_PROFILE. It is not action execution or a
new protocol object. The previous design, supplier fixture and gate evidence
remain unchanged.

The operator approved Core's calendar-date compatibility repair, then the
additional enforcement of the existing class alternatives and slot conditions.
Neither approval changes the ontology or authorizes an action runtime.

## Boundary and oracle

`test_compiled_assent_input.py` compiles the exact shipped Assent closure through
`malleus.compiler.compile_linkml_contract`. It checks all three input byte
hashes before compilation. Its independent synthetic cases transcribe the five
existing `ValidTime` branches from `ontology/assent.yaml`, not from the compiler
output. None of these values is a supplier observation or an action timestamp.

Each case checks valid structure, omission of every required component, and
every forbidden time-form field, including an explicitly present null. A
separate check preserves the declared calendar-day timezone-database pin.
Validation uses the public artifact reader with source-byte reads and registry
construction forbidden. This checks source-free validation, not an entire
runtime installation without build dependencies.

No test asserts timestamp truth, interval ordering, source faithfulness,
authorization, dispatch, observation, KCS admission or a changed graph. Passing
these checks cannot establish the proposed action/history composition.

## Frozen RED

Core date-only candidate:
`591cea9bf2682d52071197aa15ba31e531552ed5`, tree
`21c011f65491dcc78894fd6be14ce0ada5134876`.

An immutable archive of that commit produced **11 failures and 5 passes** in
1.56 seconds. All five valid forms passed. Required branch components,
forbidden fields and the branch-specific database pin were ignored. The tests
therefore distinguish retaining the rule from enforcing it after reload.

Invocation, from the selected Core checkout with its declared dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider \
  -c pyproject.toml /path/to/semantic_reentry_external_design/test_compiled_assent_input.py
```

The selected checkout supplies both the public compiler and the exact ontology
bytes. A mismatched closure fails its hash check rather than substituting data.
Changed-file Ruff and formatting checks pass. No successor GREEN is claimed
by this RED commit. Core owns the implementation; this packet owns only the
independent consumer checks.

## Independently verified successor

Core commit `5c559c2d141c03b26f5b60ab4e2707f42f47c248`, tree
`76fba63bdd6bfd3664eb6e190125ec32604e0261`, passes the same sixteen consumer
checks without changing them. The combined consumer, date/record, generic
alternative, public-compiler and Assent-ontology selection passes **108 tests**
in 10.68 seconds against an immutable export of that commit. The source hashes,
selectors and RED/GREEN coordinates are retained in
[compiler-input-result.json](compiler-input-result.json).

The broader Re-entry selection is **67 passed, 1 failed**, not GREEN. Its
remaining failure compares a new run with frozen old execution evidence.
An independent complete Shop artifact comparison against the pre-repair
producer finds exactly two changed leaves: the producer attestation and its
evidence hash. Semantic facts, their identity, the metamodel and source
attestations remain equal. The retained artifact bytes nevertheless differ,
which propagates into new execution-history hashes. No old receipt, equality
test or oracle was rewritten to suppress that distinction.

This closes the demonstrated compiler input defect. It does not finish the
executable action contract, authorize an action runtime or declare the full
landing gate green. Disposition of historical execution evidence remains
separate from enforcing the already-declared ontology constraints.

Core's final handoff is `1be958e88dce865c8e785638d1c15508c92bd1d2`, tree
`8334a558442eb64ec90973d6d0ab08eba3b85ce6`. Its only change after the verified
runtime is the compatibility report. That report records the current-wide
gate as **1165 passed, 9 failed, 1 preserved historical xfail**, and the same
nine historical selectors as **9 passed** under their original producer.
Those broader counts are Core-reported evidence, not a second independent run
by this packet. The report hash and full coordinates are recorded in the JSON.

Landing order remains conditional: resolve the explicit successor-evidence or
per-producer gate disposition, land Core's approved compatibility repair, then
this consumer conformance packet. The action contract's remaining grammar and
bindings still need definition. No merge, push, runtime rebind, new action
record, supplier effect or paper edit is included here.

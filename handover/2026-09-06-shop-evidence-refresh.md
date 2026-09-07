# Small Shop evidence and readable proof

## Approved cut

Role: CONFORMANCE_FIXTURE for the optional compiler-enabled semantic-history
profile. Domain mapping, replacement and time choices remain ADOPTER_CHOICE.
This is not a protocol, compiler, ontology or package change.

Claim: current runners reproduce their exact recorded evidence, while earlier
evidence remains byte-identical. The walkthrough explains what the complete
five-plan run proves and distinguishes it from the separate no-correction,
unstated-time and declared-gap controls.

Observation: exact regeneration of all three failing Shop outputs, immutable
historical hashes, unchanged graph results, and public-path replay/trace tests.
Reuse: the existing correction, object-event, showcase and public-population
runners, plus the existing Shop time and capture tests. No new runner or
evidence framework is needed.

Excludes: new domain facts, automatic correction inference, semantic
completeness, model comparison, pure re-entry composition, paper work, package
changes, release and remote publication. No historical ledger is rewritten.

Pre-action check: local fixtures/tests/docs only, no server or endpoint;
no dependencies or missing-input defaults. Existing byte equality stays strict.

## Root cause and RED

Base: `7c5fdb491721122b6e0c7243862935acc8303a1f`.
The three failing nodes are:

- correction/test_correction_vertical.py::test_checked_in_evidence_is_exactly_regenerated
- object_event/test_run.py::test_ret040_admits_reopens_replays_queries_and_traces
- showcase/test_evidence.py::test_regeneration_is_canonical_byte_identical_and_matches_runner

These paths are relative to
`research/ontology_driven_kg_realization/experiments/small_shop/`.
The declared project environment reproduces 3 failures at the base. An archive
of `ca0d121ab81dcefb06e20f06a83ac1da3d1a1ab8`, the direct parent of
`e4fa5fd340100a62f1d6470d1c9c579b48289d05`, reproduces 3 passes.

That successor improved the INVALID_RANGE diagnostic in `elaborate.py` without
changing the accepted schema set. `_evidence` hashes five producer files,
including `elaborate.py`. Changed producer bytes change the retained validated
artifact, hence the history and downstream receipt identities. Both graph
files remain exact; object-event observations, contract, source, plan, profile
and graph identity remain exact. The differing explanation/query fields are
artifact, change, check and history identities, not changed shop answers.

Correction and showcase retain their last historical generation at the existing
paths. Object-event also retains its original `evidence.json`. New current
expectations live together in `evidence_2026_09_06/`. Tests compare current
outputs exactly and separately guard the historical hashes. A later producer
change must be reconciled explicitly, not masked by dropping identity fields.

The showcase evidence command's existing default points at frozen files.
Move that default to `build/`, with a hard test. Explicit output paths remain
caller-controlled.

## Validation and disposition

Pending implementation and focused validation. This record does not yet claim
GREEN or a full-repository pass.

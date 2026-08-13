# Implementation Status

Malleus package version `0.2.0` implements the
`stage-4-structural-staging` boundary.

This is a capability boundary, not a claim that the research program is
complete. The machine-readable source is `malleus.IMPLEMENTATION_STATUS`.

## Implemented

- Stage 2: closed-world ontology and typed-graph validation
- Stage 3: separate assessment, epistemic-decision, and authorization state machines
- Stage 7a: strict single-writer protocol ledger and deterministic replay
- Stage 4: isolated proposed-subgraph staging and failure-atomic structural materialization

The Stage 4 boundary includes deterministic candidate and graph-state digests,
ordered intra-candidate dependencies, stale-base detection, ontology matching,
complete candidate-overlay verification for the current domain bridge, and
mutation-free rejection.

## Not implemented

- `general-graph-to-prolog-compilation`: ontology-driven graph-to-Prolog compilation
- Versioned proof records for every logical assessment
- `policy-selected-monitoring-control`: monitor completeness and control selection
- `assent-gated-materialization`: structural commits caused by accepted decisions
- `accepted-graph-projection`: a current accepted-state view
- `bitemporal-as-of-replay`: valid-time and transaction-time reconstruction
- `action-execution`: execution after authorization

Stage 4 materialization is structural and assumes one writer. It does not prove
truth, epistemic acceptance, authorization, or multi-writer correctness.

## Release boundary rule

Every completed implementation stage must update all of these in the same
commit:

1. `IMPLEMENTATION_STATUS` in `src/malleus/status.py`
2. The package version in `pyproject.toml`
3. This document
4. `CHANGELOG.md`
5. Status and stage guardrail tests

The distribution build and installed-wheel smoke test must pass before that
stage is published.

Package versions and ontology versions are independent. The current root
ontology is `0.4.0`; the assent ontology is `0.1.0`.

## History

| Package | Boundary | Included work |
|---|---|---|
| `0.1.0` | Initial typed graph | Root ontology, typed graph, compatibility hashing, optional domain verifier |
| `0.2.0` | `stage-4-structural-staging` | Stages 2, 3, 7a, and 4 |

# Implementation Status

Malleus package version `0.3.0` implements the
`stage-5-general-logic-monitoring` boundary.

This is a capability boundary, not a claim that the research program is
complete. The machine-readable source is `malleus.IMPLEMENTATION_STATUS`.

## Implemented

- Stage 2: closed-world ontology and typed-graph validation
- Stage 3: separate assessment, epistemic-decision, and authorization state machines
- Stage 7a: strict single-writer protocol ledger and deterministic replay
- Stage 4: isolated proposed-subgraph staging and failure-atomic structural materialization
- Stage 5: domain-neutral typed graph compilation, pinned trusted rules,
  isolated logical execution, exhaustive violation witnesses, and immutable
  logic-monitoring records

The Stage 5 boundary compiles public graph snapshots through one versioned fact
contract, binds ontology and exact rule bytes through a pinned logic contract,
runs every check in a fresh SWI-Prolog process, and validates the complete rule
manifest and violation set. A concrete `LogicContractArtifact` lets replay
verify ontology, fact-contract, rule manifest, timeout, and separate ruleset
record, raw-byte, and semantic-contract hashes. Completed executions produce
content-addressed `LogicCheckRecord` and `ViolationWitness` records. Translation, execution,
timeout, and malformed-result failures cannot report `SATISFIED`; the protocol
records them as `MonitorFailure` plus a logical `UNKNOWN` assessment.

## Not implemented

- `policy-selected-monitoring-control`: monitor completeness and control selection
- `proposal-candidate-semantic-binding`: mechanical binding from protocol proposal content to the checked candidate
- `assent-gated-materialization`: structural commits caused by accepted decisions
- `accepted-graph-projection`: a current accepted-state view
- `bitemporal-as-of-replay`: valid-time and transaction-time reconstruction
- `action-execution`: execution after authorization
- `untrusted-rule-program-sandboxing`: safe execution of uploaded or otherwise untrusted rule programs

Stage 5 accepts only trusted, pinned local rule programs. Logic-check records
are content-addressed execution attestations with replay-validated bindings,
not formal proof certificates or guarantees of engine-level reproducibility.
A check identifies a proposal and a candidate digest, but does not yet establish
that the proposal was compiled into exactly that candidate. Stage 4 materialization
remains structural and single-writer. Neither stage proves truth, epistemic
acceptance, authorization, or multi-writer correctness.
Candidate, state, and fact digests in a check are monitor attestations until
Stage 7b supplies the missing proposal-to-candidate and accepted-state binding.

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
ontology is `0.4.0`; the assent ontology is `0.2.0`.

## History

| Package | Boundary | Included work |
|---|---|---|
| `0.1.0` | Initial typed graph | Root ontology, typed graph, compatibility hashing, optional domain verifier |
| `0.2.0` | `stage-4-structural-staging` | Stages 2, 3, 7a, and 4 |
| `0.3.0` | `stage-5-general-logic-monitoring` | Stage 5 generic compilation, isolated execution, and replay-validated records |

# Core population piece 5: additive contract revision

Status: implemented in Core, awaiting independent overseer verification.

## Coordinates

- RED commit: `bcf877b798f4e2d82abacdf263ac471f1875357f`
- GREEN commit: `30970a397b840542b5395247ae24a695a2cb2cb4`
- GREEN tree: `95d5adcc347b2ba8258b9cc31ea2b7e766b5b3f1`

## What changed

One `KnowledgeChangeHistory` can now cross an explicit additive domain-contract
revision without starting a second ledger. The revision is a canonical,
content-addressed artifact. It binds the exact history coordinates it follows,
the old contract identity, the complete target validated and partial contract
artifacts, mechanically derived change kinds, the revision-policy identity,
and one migration receipt.

The active policy is data, exported as `CONTRACT_REVISION_POLICY`. It admits
`ADD_CLASS`, `ADD_ENUM_VALUE`, and `ADD_SLOT`. It keeps `ADD_IMPORT` in the same
grammar and refuses it. The executor derives these terms from the two compiled
fact sets and retained import closures. The caller does not declare them.

Replay begins with the original retained bootstrap. At the revision event it
re-derives the delta, verifies the receipt and exact prior coordinates, rebuilds
the accepted graph under the target contract, and rebinds the unchanged
protocol-machine state to that contract identity. Later knowledge change sets
must name the new identity. Old and new change sets, record supersession, and
the current graph all reconstruct from the same JSONL history.

## Public surface

`malleus.compiler` exports the policy, revision value and typed refusal values.
`KnowledgeChangeHistory` adds `compose_contract_revision` and
`record_contract_revision`. The lower-level deterministic compiler remains
available as `compile_contract_revision`.

## Mechanical evidence

- The RED commit collected eight tests and failed all eight because the
  revision surface did not exist.
- At GREEN, all eight revision tests pass.
- The test history admits two records under version 1, records one revision
  containing all three admitted change kinds, then supersedes one old record
  and creates a new-class record under version 2.
- Clean reopen reproduces the graph, both contract-bound change sets, the
  record supersession history, and the revision artifact.
- Separate tests derive each admitted kind, refuse an added import by policy,
  refuse a non-additive semantic change, and preserve exact ledger bytes for a
  stale or forged revision.
- The complete contract-compiler Pareto suite passes 308 tests. The focused
  revision, history, governed-population, and public-compiler seam passes 145
  tests. Ruff and formatting checks pass for the changed Python surface.

## Non-claims

This is not a general ontology migration engine. It supports only additive
classes, slots, and enum values under one fixed policy. It does not admit a new
import, remove or alter an existing semantic fact, transform an old record,
change the protocol machine or epistemic policy, materialize Event records, or
choose a domain-history model. The wire grammars remain private. Packs, the
full `DomainHistoryProfile`, Semantic Re-entry, and paper-specific behavior are
outside this piece.

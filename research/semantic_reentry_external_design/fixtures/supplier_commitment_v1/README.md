# Synthetic supplier fixture inputs

This is a CONFORMANCE_FIXTURE input/oracle freeze, not a running action loop
or an accepted protocol contract. It records the equality-to-two, one-attempt
cut the operator approved after the semantic contract review at `7d64747`.
It does not waive the requirement for an exact compiled action record contract.

## Attribution and roles

`input/supplier-before.jsonl` contains exactly the first row of the canonical
Shop supplier history, e4/B/Y/1. The original two-row source remains untouched:
`research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl`,
sha256 `a441c49f325670e09d9fc09fd8e6510669258bed1d5532cfb2b1104c4eceb081`.
Selection into this new one-row file is an explicitly authored synthetic
scenario, not a claim that the published fixture's source changed.

`oracle/supplier-after.jsonl` is the independently specified expected result:
B/Y/2 with synthetic occurrence `reentry-amendment-1`. This new occurrence is
authored test data, not e7, an observed event, or a real supplier commitment.
No implementation may preload it as an observation. The future observer must
read actual executor-produced bytes; the test compares them with this oracle.

`oracle/expected.json` freezes expected observations for the success path and
selected negative cases. None is a result of execution. In particular, the
eight quantity-one checkpoints distinguish action records and KCS preparation
from the ninth checkpoint, ordinary KCS acceptance.

`case.json` declares the goal, stable episode/action key, one operator,
source identities, complete four-field mapping, explicit supersession,
ORDER_ONLY time and preservation. It is not a population plan, Re-entry
runtime invocation, ActionProposal or KCS. It therefore contains no invented
compiled contract, ledger head, monitor implementation or acceptance identity.
Those inputs must come from actual Core compilation and a future identified
implementation, never a placeholder digest or this fixture's filenames.

`source.schema.json` is an adopter-owned closed source-row grammar. Its integer
quantity does not imply the equality goal is satisfied or the sole 1-to-2
operator is applicable. A well-formed quantity three remains representable
source data but supplies no solution under this frozen operator. This JSON
Schema neither substitutes for the Assent ontology nor validates protocol
records. It is exercised through the already declared jsonschema dependency;
no installation or network resolution is required.

## Boundaries and gate

The initial RED run of `test_frozen_supplier_inputs.py` had four failures and
twelve setup errors, all naming absent fixture/schema files. These tests check
file availability, exact source identities, explicit input/oracle separation,
required/closed source fields, types and declared expected outcomes. They do
not execute synthesis, effect delivery, observation, admission or replay.

No supplier amendment subtype or typed protocol instance is frozen here yet.
Core's public compilation of the exact Assent closure currently refuses the
LinkML date range. Core owns that reproducible blocker and the next scope
decision. Removing declarations, replacing date with string or making up a
compiled identity would not close it. The executable-contract freeze remains
blocked even when these source/oracle checks pass.

No runtime, canonical fixture, ontology, source-to-KCS adapter, policy producer,
executor, observer or shared main is modified by this input freeze. The earlier
semantic draft and audit packets remain unchanged.

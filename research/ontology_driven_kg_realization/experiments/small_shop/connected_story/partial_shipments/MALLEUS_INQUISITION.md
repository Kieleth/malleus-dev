# Connected shipment adopter self-check

Scope: Shop-owned `CONFORMANCE_FIXTURE` plus explicit `ADOPTER_CHOICE` of
vocabulary and source mapping. This report does not assess all Malleus Core,
change protocol authority, or act as independent review.

## Mechanical result

Run against [shop.yaml](shop.yaml), with exact bundled `malleus` and
`object-event` import paths, in the declared repository environment:

```text
ROOT ONTOLOGY PROFILE PURITY SEAL GRANTED. The schema may serve.
```

The inspector reports zero disabled mechanical or judgment checks and two
notes: Signal has no concrete subtype and no type carries the Agent mixin.
Both are outside this fixture: it creates neither Signals nor actors with
decision authority. The new predicates are pinned and all relation endpoints
are narrowed. The test executes the same inspector command.

## Judgment against the source and write path

- **Explicit authority and optionality.** [run.py:35](run.py) reuses the
  connected history's exact normative profile. The schema revision adds data
  structure only. No fixture-specific Python branch is installed as Core
  protocol authority. Other adopters need not select this Shop model.
- **One accepted history.** [start, run.py:35](run.py) verifies the complete baseline
  bytes. [Preparation and admission, run.py:226](run.py) use public Core contracts;
  there is no direct accepted-graph write. Tests preserve every earlier
  historical record and compare full with maintained projection at all three
  new admissions.
- **Source boundary and provenance.** [input_boundary.json](input_boundary.json)
  pins the unchanged synthetic rows, not additional chapter observations.
  [The mapper, run.py:114](run.py) copies supplied values and names every property and
  endpoint's source field. Plans retain the mapping and adapter bytes. Reads
  recover those witnesses through public record trace. Tests check all eleven
  new record IDs, not a sample.
- **Vocabulary is used.** Shipment and each new relation have a writer in
  `plan_for` and a reader in the reused `shipment_view`. Remaining-unit counts
  are derived by that query, not stored as hand-authored facts. The runtime
  does not read the independent expected-results file.
- **Preservation.** The InventoryUnit product slot is optional for existing
  data. Tests compare the old and successor declarations after removing only
  the stated additions, and prove an older unit still lacks product_code.
  Chapter shipment explanations and ordering comparisons keep their results.
- **Actual refusals.** Missing relation endpoints and missing tracking IDs
  must produce typed population refusals before preparation writes. Changed
  source bytes and a wrong prefix must refuse before revision or retention.
  The tests compare exact before/after ledger bytes for each case.

## Explicit limits, not silently closed findings

- **Duplicate assignment remains outside the selected policy.** A separate
  isolated control actually admits two assignments of the same unit, then
  checks that the other unit remains unassigned. It prevents the structural
  result from being reported as business-rule enforcement. The earlier
  [stricter proof](../../shipment_policy/README.md) is unchanged. Same-history
  policy evolution needs a Core capability and separate approval.
- **No physical effects.** Source rows assert associations and tracking IDs;
  they are not an observation of carrier execution or delivery. There is no
  domain timestamp or invented association to a chapter order.
- **No whole-import atomicity.** Each Core write is atomic, but a later failed
  step can leave earlier successful writes. Interrupted-run resume and a
  whole-import transaction are not implemented or tested.
- **No universal replay/portability claim.** Repeatability is checked against
  this exact repository implementation and declared dependency environment.
  A second interpreter or different dependency baseline has not been tested.

The local names and grounding statements reuse the existing synthetic model;
they are not attributed to the chapter or presented as borrowed standard terms.
No new Core heresy, dependency change, release change or upstream repair is
required for this approved structural cut.

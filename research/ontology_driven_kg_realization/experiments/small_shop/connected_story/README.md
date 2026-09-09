# Connected Shop, source boundary first

This is the new Shop adopter project. It does not replace the frozen predecessor
examples. The original source/probe baseline is released `v0.14.0`; the connected
successor consumes Core's later selected transition rule at the exact coordinate
in [run_receipt.json](run_receipt.json). No Core source is modified here.

## Current connected run

The [selected ontology-led model](MODEL.md) now drives one source-produced
history across all 21 retained table rows. It records both orders, both supplier
orders, five distinct units, invoices, payment and all occurrences. B's current
quantity is two; its quantity-one state is retained as superseded. The reader
joins P1 to both invoices and each packed order to its physical units through
their recorded occurrences. I2's changed value remains unknown.

Run from the repository's declared development environment, using a new output
path. The first command creates the retained history and prints its graph and
account. The second reads that file without writing it:

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run /tmp/shop-connected-history.jsonl
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run /tmp/shop-connected-history.jsonl --reopen
```

The run is 21 domain changes expressed by 121 protocol ledger events. It has
107 historical records, 106 current records and three explicit source gaps.
These counts include the qualified participation links; they are not a semantic
completeness score. Exact reproducibility coordinates are in the
[receipt](run_receipt.json), and the [self-check](MALLEUS_INQUISITION.md) separates
mechanical guarantees from source interpretation.

Shipment eligibility is explicitly `NOT_EVALUATED`. The context passages are
retained evidence, not yet a checked customer/payment rule. This completes the
connected table population, not every deliverable in the broader Shop plan.

The source slice retains all 21 rows of Fahland's Table 1, its exact published
image, and four selected context excerpts. [source_boundary.json](source_boundary.json)
binds the bytes and accounts for each column. [table-1.png](sources/table-1.png)
is the independent visual reference for the transcription, not generated from
our rows. Credit: Dirk Fahland, 2022, *Process Mining over Multiple Behavioral
Dimensions with Event Knowledge Graphs*, Table 1 and section 1,
[publisher](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The source manifest
lists our transcription changes. This attribution applies to the retained source
and its transcription, not a claim that they are original Malleus data.

## Inspect it

Using the repository's declared development environment:

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary
PYTHONPATH=src:. .venv/bin/python -m pytest -q research/ontology_driven_kg_realization/experiments/small_shop/connected_story/test_source_boundary.py
```

The inventory prints one locator and planned disposition per nonempty table
field. It checks exact source hashes, omitted or duplicated rows, field closure
and identifier-list shape. It does not claim that the planned records exist.
Context excerpts remain evidence and rule inputs, not domain facts admitted by
the inventory command. A human has not yet ratified the transcription or its interpretation.
The human-readable [coverage table](SOURCE_COVERAGE.md) separates what each row
contains from what the connected run still needs to build. Exact test and replay
receipts are in [VALIDATION.md](VALIDATION.md).

[Expected story](EXPECTED_STORY.md) makes the next connected run concrete:
nine source-backed questions cover order quantities, physical units, invoice
links, payment and the limits of the shipment explanation. These are independent
test expectations, not populated graph results or inputs to the mapper.

## Do not repair the source by guessing

- `e6` and `e8` visibly print `00-01` in the published table. Preserve those
  strings. Year and timezone are absent throughout. No calendar instants or
  elapsed-time claims are generated here.
- Use Table 1's `e33` and `e34` for the second order's packing and shipping.
  Other chapter views are not automatically aliases of this identifier scheme.
- `e9` records an invoice update, not the field or value changed. We can
  represent that occurrence; we cannot invent a replacement amount.
- `Y1` and `Y2` are different physical units. The quantity change from one Y
  to two Y belongs to supplier order B, not a replacement of one unit by another.
- `A` and `B` are Supplier Order column identifiers here. Supplier parties
  mentioned in the prose are not silently given those same object identities.
- Row order is a transcription coordinate, not proof of event order.

Additional warehouse rows, synthetic partial shipments and performance analysis
remain outside this first source boundary. Four context excerpts explain the
shared-customer scope, the quantity correction and the payment condition; they
do not constitute a transcript of the entire chapter.

## Results and decisions

- Source-boundary RED: `9268617e`, missing inventory implementation. The first
  invocation also exposed a test import setup error; the committed RED uses the
  correct absolute import and fails specifically for the missing module.
- GREEN: seven source-boundary tests pass. This proves source accounting and
  refusal of specified corruption classes, not semantic completeness or truth.
- History compatibility RED: `cacc2e4e`. The public-only probe now passes three
  tests: two occurrences plus state replacement survive reopen and trace;
  the unmodified state-only profile refuses Event population; repeated inputs
  produce identical ledger bytes. It covers two of the 21 source rows, not
  the full connected story.
- The probe creates 18 protocol events, two change sets, seven historical and
  six current records. Its profile and ontology are proposals, not the final
  selected Shop model. [The Core contract request](CORE_REQUIREMENT.md) records
  the remaining rule-enforcement boundary. No new public Core capability is
  claimed.

To reproduce only the compatibility probe, pass a new ledger path:

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.history_probe /tmp/shop-history-probe.jsonl
```

The earlier probe runner retains printed source times as text. Its provisional `NONE_STATED`
choice makes no calendar-time claim; the selected connected successor retains
that bounded choice explicitly. It also reuses the predecessor's
`SupplierOrderState.source_occurrence_id` field rather than silently changing
that established vocabulary in the probe. The connected model retains the
domain-occurrence reference and uses public trace for source provenance.

## Core restriction delivered, new witness

The [restricted-history witness](RESTRICTED_HISTORY.md) consumes Core's explicit
transition rule in a new history. State correction succeeds, occurrence
replacement refuses, and full replay, incremental replay and reopen agree.
Both exact and subtype matching are tested. The earlier structural-only probe
above retains its original behavior; no old receipt is rebound. The remaining
choice was the Shop policy, not an unresolved Core implementation. The later
selection in MODEL.md uses one ontology state category and subtype matching;
the two old probes keep their original meaning and receipts.

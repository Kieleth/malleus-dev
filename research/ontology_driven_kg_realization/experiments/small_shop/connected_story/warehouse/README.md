# The warehouse fills the gap between unpacking and packing

The earlier Shop run knows that X1 was unpacked and later packed into order O1.
It cannot show what happened between those observations. Figure 14 of
[Fahland's 2022 chapter](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9/figures/14)
supplies the missing warehouse rows. This Shop-owned extension uses those rows
in the same Malleus history. It is an adopter/conformance example, not a new
Core capability or a universal logistics model.

For X1, the displayed path becomes:

```text
Unpack e10       Scan e12       Store e13       Retrieve e22       Pack e27
04-05 11:00     04-05 13:00    04-05 13:15     07-05 11:15        07-05 17:00
```

X1's earlier receipt event e6 still has the source's unusable `00-01` date. It
remains visible but unplaced, not repaired to make the path look complete.
The source prints `DD-MM HH:MM`. Ordering those coordinates is the existing
display convention, not a derived year, timezone, elapsed duration or proof of
complete directly-follows adjacency.

Another useful observation is now testable from the same graph: Y1 was unpacked
at 10:45 and Y2 at 11:00 on 07-05, but Y2 was scanned at 13:00 and Y1 at 15:00.
The order reverses between unpacking and scanning. This supports asking the
chapter's queue questions next. It does not establish the cause or a calculated
shipment delay. Y1 has no Store or Retrieve row in the selected source; neither
is manufactured.

## What changes, and what stays

The original Table 1 history is constructed first. The extension checks its
exact bytes, records an additive contract revision introducing only `SCAN`,
`STORE` and `RETRIEVE` in `ShopActivity`, retains Figure 14 and the mapping,
then admits one change per warehouse row. Each change contains one new
`ShopOccurrence` and one new `ShopParticipation` linking it to an existing
`InventoryUnit`. The source supplies no actor, machine, warehouse-location or
order column, so the extension creates none.

There are now 34 occurrences and 75 participation records. The 17 enduring
objects are unchanged. The earlier B quantity correction stays accepted and
its predecessor stays retained. The old 21-row history is an exact byte prefix,
not a regenerated replacement. Every new property has a row-and-field
derivation back to the retained Figure 14 transcription; the original PNG is
also retained as evidence. Core's public compiler, contract revision, structural
admission and replay execute the change. No private Core import or direct
accepted-graph write is used.

Both sources use the same printed event IDs without renumbering: Figure 14's
e31/e32 are Retrieve, while Table 1's e33/e34 remain Pack Shipment and Ship.
Other chapter figures are not silently reconciled with these two sources.

The selected domain-history profile and subtype-based correction rule do not
change. `NONE_STATED` still means no calendar instant or domain-order token was
derived. Importing warehouse rows later does not assert that they occurred
after the previously imported shipments.

## Reproduce and inspect

Use the repository's declared development environment. The output path must be
new for the from-empty command. No additional installation is required here.

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse.run /tmp/shop-warehouse-history.jsonl --from-empty
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse.run /tmp/shop-warehouse-history.jsonl --reopen
```

The first prints the run receipt. The second only reads and prints object paths
and warehouse event witnesses. For a separately reproduced exact Table 1
history, use `--append` instead of `--from-empty`. A different prefix, including
an already extended history, refuses before writing. Admission is transactional
per change, not for the entire multi-row importer. An interrupted import may
retain a valid partial prefix; automatic mid-run resume is not implemented.

The warehouse reader is a separate two-source report using the existing
object-view function. The old one-source reader and its frozen receipt remain
unchanged. Its stricter Table 1 boundary is not relaxed to accept other data.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/test_warehouse.py
```

## Relation to the chapter and remaining work

### What this milestone demonstrates

We already had a story about orders, units, invoices and payments. Another
source then supplied warehouse observations. We connected it without replacing
the old story or building a separate graph:

- **Shared identity:** the warehouse's X1 is the existing inventory unit X1.
- **Recorded model growth:** three new activity values enter through an explicit
  schema revision, preserving the earlier schema and history.
- **Better explanations:** X1 gains its intermediate warehouse steps; Y1 and Y2
  reveal a reversal between unpacking order and scanning order.
- **Inspectable evidence:** each added property points to its source row and
  field, with source bytes and mapping retained.
- **Reconstruction:** reopening the ledger produces the same graph and answers;
  the earlier payment explanation and B quantity correction remain intact.

Shop supplied vocabulary, mapping and importer code. Core supplied the existing
compiler, admission and replay mechanisms without modification. This is a
bounded demonstration of a reusable protocol, not automatic interpretation of
arbitrary sources or proof that the source is true.

Section 6.1 adds these same warehouse events to existing units. We now reproduce
that source-to-unit extension and its per-unit displayed paths. Malleus adds a
recorded schema change, exact source retention, checked change admission,
preserved earlier history, and reconstruction from that history. These are
separate guarantees from process discovery or performance analysis.

Next compare narrowly defined ordering and queue observations with the chapter.
Elapsed-time, FIFO completeness, causal explanations and counterfactual delay
need their own declared evidence/time boundaries. Synthetic partial-shipment
data remains a separate future extension. There is no external warehouse,
shipment authorization, action execution, new Core feature or release claim.

### Evidence and publication status

Executable GREEN is `557adf6f38e591fe22cb163fabc43e2be54c037e`, tree
`19b5e3856e29807253f6df20a48c9017cd4ff1b6`. Its clean detached checkout passed
344 Shop and transition-admission tests with zero skips, including all 12
warehouse cases. The exact command and result are in the
[validation journal](../VALIDATION.md); [receipt.json](receipt.json) binds the
reconstructed history and read report. Documentation completion is recorded at
`ef97018f1426d58febb185352e5b3156f211b8b8`.

On September 14, Luis requested milestone documentation and a cross-session
release assessment. Shop recommends publishing this as an evidence-backed
research milestone. Overlord coordinates project documentation and the release
recommendation; Core owns package changes and release verification. A new
package version, tag and publication are not selected by this Shop record.
The 344-test result is not a full Core or package-release gate. Existing Paper,
Robotics, Re-entry and Code experiment pins must not move implicitly.

## Attribution

Dirk Fahland, *Process Mining over Multiple Behavioral Dimensions with Event
Knowledge Graphs*, 2022, DOI `10.1007/978-3-031-08848-3_9`, Figure 14.
Original image and adapted JSONL are covered by
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The image is unchanged.
Transcription renames four headers, wraps Item values in arrays and changes the
serialization. No printed value is corrected. Exact source URLs, hashes,
inspection date and limits are in [source_boundary.json](source_boundary.json).
The chapter is trusted input for this experiment under Luis's decision, not
independent evidence of an external warehouse's truth.

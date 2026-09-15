# What can the Shop evidence reproduce about warehouse order?

**One observed reversal is reproducible. Complete first-in, first-out behavior
is not established.** This comparison reads the existing connected history;
it imports no new evidence and changes no accepted record.

## Start with two physical units

The retained records say:

| Unit | Unpacked, Table 1 | Scanned, Figure 14 |
| --- | --- | --- |
| Y1 | e20, `07-05 10:45` | e26, `07-05 15:00` |
| Y2 | e21, `07-05 11:00` | e24, `07-05 13:00` |

Y1 was unpacked first, but Y2 was scanned first. These are different inventory
units, not successive versions of one unit. The report reaches their events
through the shared unit identities and includes the retained source row/field
witnesses for both the observations and the unit links.

Printed times use the existing relative `day-month hour:minute` convention.
They are not converted to calendar instants: no year or timezone is invented,
and no elapsed duration is calculated.

## Comparison with the chapter

Fahland's [section 6.2](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9)
uses activity and item paths to examine warehouse queues. It identifies Y2
overtaking Y1, X1/X2 overtaking X3, and first-in, first-out ordering for
Scan-to-Store and Store-to-Retrieve. Our narrower test compares entry and exit
order directly; it does not reproduce the chapter's activity graph or
performance-spectrum method.

Five declared units make ten unordered pairs per stage pair. Missing data
does not remove a unit from that denominator.

| Stage pair | Order preserved | Order reversed | Cannot compare |
| --- | ---: | ---: | ---: |
| Unpack to Scan | 5 | 1 | 4 |
| Scan to Store | 6 | 0 | 4 |
| Store to Retrieve | 6 | 0 | 4 |

The single observed reversal agrees with the chapter's Y1/Y2 example. All four
Unpack-to-Scan comparisons involving X3 remain undetermined: its retained e8
unpack time is `00-01 10:30`, unusable under our declared rule. The chapter's
prose and diagrams supply further precedence assertions, but they are not
inputs to this report. This is a limit of the selected evidence, not a
refutation of the chapter.

For the other two queues, Y1 has no retained Store or Retrieve observation.
The other four units yield six preserved pairs each. That supports **no
reversal among comparable observations**, not a complete FIFO certificate.
FIFO means first in, first out. The chapter's delay and counterfactual
explanations are outside this comparison.

## The rule, separate from the expected answer

[ordering_spec.json](ordering_spec.json) selects the five units, their ITEM
participation role and the three stage pairs. It contains no expected result.
[ordering.py](ordering.py) applies the same small rule to every pair:

1. Require one observation at each stage for each unit. Keep missing units,
   missing observations and repeated activities as explicit uncertainty.
2. Require usable printed coordinates and a strictly forward stage pair for
   each unit. Do not use row order or identifiers to repair time.
3. Compare the two units' entry order with their exit order. Matching orders
   are preserved; opposite orders are reversed. Ties remain undetermined.

This is a Shop read model, not a new protocol policy or persisted ordering
graph. The existing Core replay and public record-to-source trace suffice.
The prior history, ontology, source bytes, mapping and receipts are unchanged.
Source truth remains the experiment's trust assumption.

## Reproduce

First create the exact warehouse history using the
[existing from-empty command](README.md#reproduce-and-inspect). Then read it:

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse.ordering /tmp/shop-warehouse-history.jsonl
```

The JSON includes every pair, reasons for uncertainty, observation witnesses,
the replay identity and exact source/reader identities. The compact
[ordering receipt](ordering_receipt.json) binds its full report digest and
counts. It is separate from the unchanged warehouse history receipt.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/test_ordering.py
```

Tests distinguish reversal from preservation, uncertainty from missing data,
and identifier order from actual printed order. Integration checks use a
fresh history, full reopen, maintained replay, the command above and exact
source witnesses. The ledger bytes must remain unchanged by all reads.
Results and immutable coordinates are in the
[validation journal](../VALIDATION.md).

## What this adds to the Malleus demonstration

The previous milestone connected another source to existing units. This one
uses that connection to answer a cross-source question and exposes exactly
where the evidence stops. The answer can be regenerated from the retained
history and traced to the source fields, without modifying the domain graph.

It does not establish a general process-mining engine, speed or quality
advantage over the chapter, exhaustive warehouse coverage, a cause of delayed
shipment, or an intervention that would improve it. Further source precedence,
duration analysis and hypothetical queue policy need separate explicit cuts.
The remaining three extensions are recorded in the
[Shop TODO](../../CONNECTED_STORY_PLAN.md#todo-after-the-first-connected-run).

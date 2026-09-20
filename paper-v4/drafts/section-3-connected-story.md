# Draft: Section 3 and Appendix B from the connected Shop story

This file is a draft for the authors, not manuscript text. The manuscript is
unchanged. Every figure between the two rules below was read from a run made
while preparing this draft, and each one is bound by
`paper-v4/test_shop_connected_calibration.py`, which rebuilds the history from
empty into a temporary directory and compares. Nothing here is taken from a
handover or from prose in a README.

The draft replaces the three-fixture Section 3 with the one connected history
and keeps the shipment-policy fixture as the only separate history, because the
connected history's own refusal is a transition-rule refusal and cannot express
a retained domain rule. The alternatives the authors must rule on are listed
after the draft.

The text between the rules obeys the submission builder's constraints: tables
have exactly four columns, there are no markdown lists, every JSON exhibit is a
complete parseable document, and no prose outside a table separator contains a
double hyphen, which LaTeX would set as an en dash. Command modes are therefore
named in words rather than as flags, which is what the current appendix does.

---

## 3. Results with no model: the Small Shop

The Small Shop is a controlled transcription of Fahland's chapter on event
knowledge graphs, a multi-object order-fulfilment example we did not design
([Fahland, 2022](https://doi.org/10.1007/978-3-031-08848-3_9)). Table 1 supplies
21 rows covering orders, inventory units, invoices, payments and supplier
orders; Figure 14 supplies 13 warehouse observations of the same units. Both
transcriptions are retained in the history with their exact bytes and with the
published images they were read from, adopter-authored plans map rows to
records, and nothing is generated. A command that reads the source without
populating anything assigns a disposition to each of the 123 nonempty fields in
those 21 rows and reports none unaccounted. The two sources enter one history,
in the stages below. Each stage checks the exact prefix it expects and refuses
before writing if it does not match, so a reader can run the chain twice and
compare bytes.

| Stage | Accepted changes / revisions | Ledger events | What the history holds |
| --- | ---: | ---: | --- |
| Table 1 population | 21 / 0 | 121 | Seventeen enduring objects, 21 occurrences and 62 qualified participations; 107 historical records, of which 106 are current; supplier order B at quantity 1 the one superseded record, quantity 2 current, and both source occurrences e4 and e7 retained; three typed source gaps where the table prints no usable date and no changed invoice value; 895,257 bytes. |
| Figure 14 warehouse extension | 34 / 1 | 193 | The same 17 objects, now carrying 34 occurrences and 75 participations; 133 historical records; one additive contract revision introducing only SCAN, STORE and RETRIEVE; the previous 895,257 bytes an exact prefix; 1,646,996 bytes. |
| Synthetic partial shipments | 37 / 2 | 216 | A separately labelled synthetic order with its own two units and two shipments, admitted into the same history through a second additive revision; 144 historical records; units not yet assigned to a shipment queried after each step as 2, 1, then 0; the previous 1,646,996 bytes an exact prefix. |

Counts are cumulative over the one history. Four properties of the gate are
visible here without any model.

A correction does not rewrite the past. Quantity 1 at source occurrence e4 stays
in the ledger as the one record the history supersedes, only quantity 2 at e7 is
projected, and both occurrences remain current events.

A second source joins the objects the first source created. Figure 14's X1 is
the inventory unit Table 1 unpacked, not a new object with a similar name, and
X1's displayed path becomes Unpack e10 at 04-05 11:00, Scan e12 at 13:00, Store
e13 at 13:15, Retrieve e22 at 07-05 11:15, Pack e27 at 17:00. The earlier bytes
are a prefix of the later ledger, not a regenerated approximation of it.

A vocabulary can grow without a new history. The three warehouse activity values
enter through one contract revision that makes three enum additions and nothing
else, and the four synthetic shipment classes and two slots through a second
that only adds. Each revision names as its base the contract identity the
records before it were admitted under, and it appends rather than rewriting
them.

A refusal costs nothing at admission. A candidate that replaces the
invoice-update occurrence e9 and its two participations, instead of adding to
them, is refused as TRANSITION_RULE_REFUSAL under the rule
REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE, with the three refused record identifiers
named. The ledger bytes are identical from the start of admission to after it,
and the replayed graph and change sets are unchanged. Preparing that candidate
retains its evidence in an earlier separate transaction, and that retention
stays; the refusal rolls back admission, not preparation.

Reads run over the replayed history and append nothing. The per-object reader
returns 17 views over one registry of occurrences: invoice I2 shows creation e5,
update e9 and clearing e30, and that same e30 appears in the I1 and P1 views
rather than being copied into each. The ordering comparison asks, for the five
inventory units, whether the order in which they enter a warehouse stage
survives to the order in which they leave it. Five units make ten unordered
pairs per stage pair. Unpack to Scan preserves the order in 5 pairs, reverses it
in 1 and cannot compare 4; Scan to Store and Store to Retrieve each preserve 6
and cannot compare 4. The single reversal is Y2 over Y1: Y1 was unpacked at
07-05 10:45 and scanned at 15:00, Y2 was unpacked at 11:00 and scanned at 13:00.
Section 6.2 of the chapter reports the same overtake. The four Unpack-to-Scan
pairs that cannot be compared are the four involving X3, whose unpack time is
printed 00-01 10:30 and is unusable under the declared rule; in the other two
stage pairs they are the four involving Y1, which has no retained Store or
Retrieve observation. Every undetermined pair carries its reason, and a unit
with missing observations stays in the denominator.

What the fixture does not show matters as much. Printed times are retained as
text: no year, timezone, calendar instant or elapsed duration is derived, and
row order is a transcription coordinate rather than domain order. That no
comparable pair reverses in the other two stage pairs is not a first-in,
first-out certificate, and no cause of any delay is computed. Structural
admission alone does not reject a duplicate unit assignment, and the synthetic
cohort is labelled synthetic rather than presented as further chapter data.
Reopening any stage under the pinned implementation reproduces that stage's
receipt.

One refusal the connected history cannot express has its own fixture. A Prolog
rule retained in that fixture's own history and executed at admission gives 3
accepted changes and 32 ledger events, and the candidate assigning unit
SYN-PS-X1 to a second shipment is refused as VIOLATED with three witness records
and no admission bytes appended, after which the legitimate second unit is
admitted. That fixture needs SWI-Prolog, which the connected chain does not.

## Appendix B. The Small Shop, run today

The chain runs from the repository root in its configured environment, into a
history path that must not exist yet. The connected runner is the module
research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run
with a history path argument. The warehouse extension is its sibling
warehouse.run in append mode on that exact history, and the read-only ordering
comparison is warehouse.ordering on the same path. The synthetic extension is
partial_shipments.run, also in append mode. Each stage verifies the
digest of the prefix it expects and of its own source bytes before it writes
anything, and a wrong prefix refuses before any write. The whole chain needs no
tool beyond the repository's declared environment. The separate shipment-policy
fixture is shipment_policy.run with a history path argument, and that one needs
SWI-Prolog on the path. The figures in Section 3 were read from runs made while
writing this draft.

Every record carries its derivations back to a retained source row and field.
The reader prints six witnesses for the Scan observation of unit X1. The three
below are the occurrence's own; the other three bind the participation record
participation:e12:item:X1 to the event identifier and item list of the same row:

```json
{
  "e12": {
    "event_type": "SCAN",
    "time_text": "04-05 13:00",
    "units": ["item:X1"],
    "witnesses": [
      {
        "locator": "row:0:event_id",
        "path": ["properties", "source_identifier"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      },
      {
        "locator": "row:0:time_text",
        "path": ["properties", "time_text"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      },
      {
        "locator": "row:0:activity",
        "path": ["properties", "event_type"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      }
    ]
  }
}
```

The refused occurrence replacement changes nothing at admission. Its own
preparation is a separate earlier transaction, and the evidence that transaction
retained stays in the ledger:

```json
{
  "occurrence_replacement": {
    "candidate_plan_id": "plan:hostile:replace-e9",
    "change_sets_unchanged": true,
    "graph_unchanged": true,
    "ledger_unchanged": true,
    "preparation_retained_evidence": true,
    "reason": "TRANSITION_RULE_REFUSAL",
    "refusal_code": "REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE",
    "refused_record_ids": [
      "e9:hostile",
      "participation:e9:actor:R2:hostile",
      "participation:e9:invoice:I2:hostile"
    ]
  }
}
```

The policy runner's report records its own refused candidate:

```json
{
  "duplicate_unit": {
    "ledger_unchanged": true,
    "outcome": "VIOLATED",
    "violations": [
      {
        "rule_id": "ONE_SHIPMENT_PER_UNIT",
        "violation_code": "UNIT_ASSIGNED_TWICE",
        "witness_record_ids": ["SYN-PS-X1", "ships_unit:SYN-S1:SYN-PS-X1", "ships_unit:SYN-S2:SYN-PS-X1"]
      }
    ]
  }
}
```

Reopening any stage with the public history class and replaying it reproduces
that stage's receipt. The Table 1 ledger is
1c989c554b9aa68e97226c0efc6355496723613f17e901bb7689a4c4da28acbe, the warehouse
ledger is
32798a67f4b2d5b6fab2de102ae6c4b41087f04ae794547517497232256ac333 and the
synthetic ledger is
15c7c1eff28ff59496fd937de19181f649e9c8c9c4c1e895cf56252f434bd204. The fixtures
are conformance evidence for the structural path over a transcribed published
example and a labelled synthetic cohort; they establish no source truth, no
semantic completeness and no physical delivery.

---

## Choices the authors must make

**Keep or drop the three old fixtures.** Recommendation: drop the default
admission (50 events) and old partial shipments (71 events) rows, keep the
shipment-policy fixture. The connected history strictly dominates the first two
on every axis they demonstrate, and it carries its own refusal; the policy
fixture is the only place a retained domain rule executes at admission, which
structural admission alone does not do.

**Include the ordering comparison or only the history figures.** Recommendation:
include it. Without it the section reports only what was written; with it the
section reports a question answered from the connected history that neither
source answers alone, and the four undetermined pairs are the section's
strongest honesty signal.

**Include the payment-context fixture S1 as a fourth row.** Recommendation: no,
not in this draft. It is uncommitted, lives in a Codex clone and is being
assessed separately, so nothing in it can be bound by a calibration test that
reruns from this checkout. Add it after it lands on main and reruns green.

**Table layout under the 4-or-8-column rule.** Recommendation: the four-column
stage table above, with the shipment-policy fixture as prose rather than a
fourth row. Mixing a cumulative one-history stage sequence with a separate
history in the same table misreads as four separate fixtures.

**Appendix B exhibits.** Recommendation: three exhibits, replacing the old
default-admission derivation with the connected-story record trace (e12, showing
a Figure 14 row reaching a Table 1 object), adding the transition-rule refusal,
and keeping the Prolog policy refusal. The first two are new evidence; the third
is the only exhibit for the fixture kept from the old section.

**Registering the calibration test.** Not a choice this draft makes.
`paper-v4/active-test-manifest.json` lists `paper-v4/test_shop_calibration.py`
at line 80 and does not list the new file. Whoever lands the manuscript edit
decides whether the new test replaces that entry or joins it, and that file has
uncommitted changes from another session, so it was not touched here. The new
test takes about three minutes because it rebuilds the history from empty.

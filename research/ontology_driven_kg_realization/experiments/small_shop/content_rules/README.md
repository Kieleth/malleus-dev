# Two content rules on the Shop path

The [connected story](../connected_story/README.md) admits Table 1 through the
structural gate alone. A structural gate reads shape: closed fields, declared
types, present endpoints, a derivation behind every property and at least one
derivation on every record. It never reads what a record says. The fault-injection control on the paper's document path
made that concrete: 55 broken records, 35 refused, 20 admitted, and 15 of the 20
visible only to a human reading the source
(`paper-v4/experiment-v4/fault-injection-01/RESULTS.md`).

This directory adds the layer that was never applied: an adopter-owned policy
with a pinned Prolog check that runs at admission over the candidate graph. Two
rules. A violated outcome refuses the whole atomic admission.

The rules are an adopter choice, not a Malleus invariant. The policy is an
optional profile, this runner is a research-local reference implementation, and
the synthetic candidates and tests are conformance fixtures. None of it is
evidence of delivery.

## The two rules

[rules.pl](rules.pl) carries both. [logic.yaml](logic.yaml) pins the contract,
the compiled ontology identity, the rule manifest and the timeout.
[policy.json](policy.json) requires that exact check contract by digest and maps
its outcome to a verdict. The shape follows the existing
[shipment-policy fixture](../shipment_policy/README.md); this directory adds no
second interpreter.

### NO_CONFLICTING_QUANTITY

Two records asserting a different quantity for the same order and product are a
disagreement, and the candidate is refused.

The rule is keyed on the Shop's quantity slots: same `order_id`, same
`product_code`, same value kind, different `ordered_quantity`. It is not keyed on
a `RecordedOrderState` subtype test, because `m_record/3` carries the record type
as the caller spelled it while `m_subtype/2` carries registry URIs, so a rule
cannot join a record to its ancestors. See
[CORE_REQUIREMENT.md](CORE_REQUIREMENT.md), last section.

**Scope is current records only.** The check runs over the accepted graph with
this change's retirements already removed, which is the same base Core applies
the change to (`_apply_change` calls `_without_records` on the superseded IDs
before creating anything). History scope would be wrong here and Table 1 says so:
row e7 supersedes supplier order B's `1·Y` state with `2·Y`. Both versions stay
in the record history, 107 historical records against 106 current. A rule reading
history would see `1` and `2` for the same order and product and refuse an
honest, explicitly recorded correction. A correction is not a conflict.

**What it catches.** A second live quantity for a subject that already has one,
whether it arrives in the same change set or a later one. The synthetic
`conflict` candidate does exactly that and is refused.

**What it cannot catch.** A wrong quantity that nothing disagrees with. One
record saying `9·X` where the source says `2·X`, with no second record, is
consistent and admitted. That is rule 1's job, and rule 1 is not here.

### NO_EMPTY_RECORD

A record carrying no property at all is refused.

This started as the document path's `RECORD_WITH_NO_SOURCE_NO_FIELDS`, admitted
there because `UNDERIVED_FIELD` is computed over a record's `properties` keys and
its two relation endpoints, so a record with neither had nothing required of it.
Core has since closed the half of that hole a structural gate can see: the plan
compiler's `UNDERIVED_RECORD` refuses any record carrying no derivation at all,
whether or not it has properties. The half left here is not a structural
question: a record that names the source it came from and then says nothing.
Every concrete Shop type declares required slots, but the imported `Entity` base
class does not, so a record typed `https://malleus.dev/schema/Entity` with
`"properties": {}` and one derivation on its `type` passes the compiler and the
structural check. The synthetic `empty` candidate is exactly that record: it
derives `type` from `row:0:event_id`, so Core admits it and `NO_EMPTY_RECORD` is
what refuses it.

The rule applies to every record kind, relations included. Table 1 carries no
relations, so this is not a false positive here. An adopter with legitimately
property-free relations would need to narrow it, and should.

**What it cannot catch.** A record with one meaningless property. The rule reads
presence, not adequacy.

## Rule 1 is not here

The original specification had a third rule: for every property that carries a
derivation to a source cell, the value must equal, or after a whitespace and case
normalisation be contained in, the retained cell text. It was measured against
the honest population before anything was built, and it refuses **145 of the 294
retained derivations**. Ruled out of this gate and moved to the document path,
where the transcription reading it assumes actually holds.

Three mechanisms, all of them honest Shop mapping:

| mechanism | n | value | cites | cell text |
| :-- | --: | :-- | :-- | :-- |
| mapping constant, absent from the cell | 62 | `ACTOR` | `row:0:actor_ids[0]` | `R1` |
| minted record identity, containment runs the other way | 69 | `actor:R1` | `row:0:actor_ids[0]` | `R1` |
| declared label-to-enum translation | 14 | `CREATE_ORDER` | `row:0:activity` | `Create Order` |

`qualifier` comes from `mapping.json`, not from the cell it cites. `entity_id`
and `order_id` are prefixed record identities, so the cell is contained in the
value rather than the value in the cell. `event_type` is a `ShopActivity` enum
member; seven of the 21 rows pass on case alone, the five `Unpack` rows and the
two `Ship` rows, and the other fourteen do not, including `Place SO` to
`PLACE_SUPPLIER_ORDER`, an abbreviation expansion that no character-level
normalisation reaches.

The normalisation was not widened to make them pass. The Shop's derivations say
"this cell is why this value is here", not "this value is the text of this cell".
That is a different claim from the document path's, where a record transcribes a
sentence, and it is why the rule belongs there.

## The outcome grammar: refuse or admit, nothing else

The desired behaviour for a conflict is to admit the change and record the
disagreement. The policy grammar cannot express it, and this was checked at the
site rather than assumed:

- `PolicyProgram.outcome_verdicts` maps each outcome to one of
  `ACCEPT`, `CONTEST`, `DEFER`, `REJECT` (`machine.py:22`).
- `_select_verdict` returns the first verdict in `precedence` that any required
  check produced (`machine.py:1184`).
- `knowledge.py:2066` refuses the whole change with `REJECTED_CHANGE` whenever
  the terminal verdict is not the binding's `accept_verdict`, which is `ACCEPT`
  (`profiles/structural-history-binding.json`).

So `CONTEST` and `DEFER` are refusals under other names. A satisfied outcome is
recorded, in `CHECK_RECORDED` with its receipt; a violated one is reported to the
caller in-process and persists nothing. Both synthetic candidates confirm it:
`REJECTED_CHANGE`, and the ledger bytes after the attempt are byte-identical to
the bytes before it.

Gate 1 therefore refuses. Admit-and-record would need a Core decision about a
verdict that admits while persisting a violation, and about where that violation
record lives. It is not requested here: the standing ruling is that cross-evidence
conflicts are review dispositions in the review-coverage checker, not admission
events.

## The honest population

21 Table 1 rows, built through the connected story's own adapter, admitted into a
fresh history under the policy. **Zero refusals.** 21 accepted changes, 107
historical records, 106 current: 23 entities, 21 events, 62 event participations,
no relations.

The domain records are identical to the connected story's. Its committed receipt
(`../connected_story/run_receipt.json`) is reproduced by the unpolicied baseline
in the same run, so the comparison is against a verified control, not a quoted
number.

- `graph.export_records()` equal, family by family.
- Record history equal: the same 107 IDs, the same types, the same properties,
  the same `supersedes_record_id` and `superseded_by` on each.
- The 21 retained plans equal apart from one field, `contract_identity`, which
  binds the effective contract and therefore moves when the policy does.

### What the selected policy costs in the ledger

Measured with the probes off, so the difference is only the policy: 143 events
against the connected story's 121.

| event type | policied | connected |
| :-- | --: | --: |
| `ARTIFACT_REGISTERED` | 57 | 35 |
| `SOURCE_REGISTERED` | 2 | 2 |
| `KNOWLEDGE_CHANGE_SET_RETAINED` | 21 | 21 |
| `CHANGE_PROPOSED` | 21 | 21 |
| `CHECK_RECORDED` | 21 | 21 |
| `VERDICT_RECORDED` | 21 | 21 |

Every difference is a retention. Added, 23: one check receipt per admission
(`receipt:change:plan:shop-connected:<event>`, 21 of them, each binding the change
set identity, the plan identity and the full check result), plus
`shop:content-rules:logic` and `shop:content-rules:rules`. Removed, 1:
`malleus:structural-admission-check/v1`, Core's structural check contract, which
this policy replaces.

Of the 36 retained records both ledgers hold, 22 differ in bytes and 14 are
identical. The 22 are `malleus:bootstrap:partial-effective-contract`, which
carries the normative profile and therefore the policy, and the 21 plans that
bind its identity. The 14 identical ones include the validated contract, so the
compiled ontology is unchanged: both sources, both source artifacts, the mapping,
the adapter, the source boundary, the table image, the history binding, the
domain history profile and the three gaps artifacts.

## What executes what

The runner selects the policy in a fresh history before the first record and
retains the rule bytes in the bootstrap. It reuses the connected story's own
compiled ontology, machine program, history profile, sources and row adapter
unchanged; the plans are that adapter's, not this directory's.

At each admission it re-reads the retained rule bytes, checks them against the
loaded contract, checks that the history's policy names that exact contract
identity, stages the change's exact operations over the retirement-adjusted
accepted graph, and submits the real Prolog result to the policy. It never
accepts a caller-supplied outcome. The rule identity is bound into every change
through the policy inside the partial effective contract, which each plan's
`contract_identity` names; the installed `CheckRecord` schema has no field for a
receipt artifact, so the receipt is retained alongside under a matching ID rather
than referenced from the check event.

Reopen reads the retained history alone and does not rerun Prolog. It preserves
an execution attestation, not independent proof that an engine ran. Caller
authored machine events remain a trusted boundary; this is not an anti-forgery
mechanism or an untrusted-rule sandbox.

## Run

Requires the configured repository environment and its SWI-Prolog dependency.
The history path must not already exist.

```sh
PYTHONPATH=src:. .venv/bin/python -m \
  research.ontology_driven_kg_realization.experiments.small_shop.content_rules.run \
  /tmp/shop-content-rules.jsonl

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q \
  -p no:cacheprovider \
  research/ontology_driven_kg_realization/experiments/small_shop/content_rules/test_content_rules.py
```

## What this is not

- Not rule 1. Nothing here reads a value against the text it cites, and the
  fact contract cannot: see [CORE_REQUIREMENT.md](CORE_REQUIREMENT.md).
- Not a document-path result. Gate 2 runs these rules under Core
  `c95dba7b86bb61487bda9a52458e1ea47cce20ab` and reruns the 20 admitted faults.
  It is a separate step and was not run.
- Not a general conflict detector. The quantity rule knows three Shop slot names.
- Not a claim about the other faults in the catalog. A coherent relocation and a
  repointed locator are invisible to both rules, as they are to the structural
  gate.
- No Core change. Nothing under `src/malleus` was read into this directory or
  modified.

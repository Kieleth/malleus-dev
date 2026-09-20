# Three Core findings from a staged-acquisition run

Written for the Core session. Nothing here asks for a change; each finding is
an observation with a pinned reproducer, and the decision about what, if
anything, Core does with it belongs to Core.

The observations come from a two-stage model run on the Shop sources
(`private/shop-progressive-01/`, run D). Stage A's producer was a fresh model
session given one evidence file, a given ontology, and a runner. The findings
are stated domain-neutrally: none of them is about the Shop, and two are
reproducible with no domain content at all.

Core coordinate throughout: `e7937b89917c8da7ee4a08acc22e99ad12b9985b`,
governance head `OVR-000462`. Line numbers are that commit's.

---

## 1. `UNKNOWN_GAP_KIND` names no permitted value

### What happens

A population plan may declare typed gaps. The plan compiler accepts six kinds
and refuses everything else:

`src/malleus/_contract_pipeline/population.py:141`

```python
_GAP_KINDS = frozenset(
    {
        "AGGREGATE_ONLY",
        "INTERVAL_NOT_EXPRESSIBLE",
        "MODALITY_NOT_EXPRESSIBLE",
        "RELATION_ABSENT",
        "REQUIRED_FIELD_ABSENT_IN_SOURCE",
        "TYPE_ABSENT",
    }
)
```

`population.py:1492`

```python
if kind not in _GAP_KINDS:
    raise _refuse(
        PopulationPlanRefusalReason.UNKNOWN_GAP_KIND,
        f"unknown gap kind: {kind}",
    )
```

The refusal names the value it rejected. It does not name one that would be
accepted.

### Why that mattered

The producer had no way to learn the vocabulary. It is not in the refusal, there
is no public accessor for `_GAP_KINDS` (`dir(malleus.compiler)` has nothing
matching `GAP`), and the producer's declared inputs did not contain it. The set
is written down in two places, neither of which a producer reaches: the private
frozenset above, and `design/KNOWLEDGE_PACKS.md:128`.

The producer probed roughly 5,700 candidate values, then wrote `gaps: []` and
reported `PARTIAL`, recording the nine gaps it had identified in prose in its
session log instead. The evidence it read supports nine typed gaps and the
ledger carries none.

### The third-party consumer's position

A typed refusal that names no permitted value is a refusal the caller cannot
act on. Every other closed vocabulary a plan carries has the same shape: the
caller learns the permitted set by reading Core's source, or by guessing.

### The documentation does not match the code either

`design/KNOWLEDGE_PACKS.md:126` describes a gap as naming "a source block, a
question id or none, a kind, and one sentence". The implemented field set is
closed and is four different fields (`population.py:1481`):

```python
_exact(
    gap,
    frozenset({"kind", "locator", "source_id", "statement"}),
    PopulationPlanRefusalReason.MALFORMED_PLAN,
    "gap fields are not closed",
)
```

There is no `block` and no `question id`; there is a `locator` and a
`source_id`. A producer working from the design document writes a gap that
refuses with `MALFORMED_PLAN`.

### Reproducer

Any plan, no domain content needed:

```python
plan["gaps"] = [{"kind": "NOT_A_REAL_KIND", "source_id": <a listed source>,
                 "locator": <a locator in it>, "statement": "one sentence"}]
```

refuses with `unknown gap kind: NOT_A_REAL_KIND`. Substituting any of the six
listed above is accepted.

### What the adopter did about it locally

The run's own runner now reads `_GAP_KINDS` and puts the permitted set into its
own refusal detail, and states the six with one line each in the producer's
procedure. That is an adopter reaching into a private name because no public one
exists, and a test asserts the two agree so a rename in Core breaks the adopter
loudly rather than leaving a stale list in a prompt. It is a local patch over
the finding, not a fix for it.

---

## 2. A `NO_DOMAIN_CHANGE` refusal leaves an `ARTIFACT_REGISTERED` event

### What happens

`prepare_population_change` registers the plan artifact in the ledger, and the
absence of a domain change is discovered after that. When a caller submits a
plan carrying no records, the call refuses and the plan artifact's
`ARTIFACT_REGISTERED` event remains. Every later event hashes on top of it, so
the refusal is visible in the ledger's identity forever.

### Which part is Core's and which is the caller's

Stated precisely, because the two are easy to blur:

- **Core's behaviour**: the retention of the plan artifact happens inside
  `prepare_population_change`, and the `NO_DOMAIN_CHANGE` status is returned
  after it. Core's own contract for this is a question for Core: a refusal that
  has already appended to the ledger is not atomic in the sense a caller is
  likely to assume, and nothing in the refusal says so.
- **The caller's guard, and its hole**: the run's runner wraps admission and
  compares the ledger bytes before and after to raise `PARTIAL_EFFECT` when a
  refusal left something behind. That comparison sits on the generic exception
  path. The runner raised its own typed refusal for the no-records case and
  re-raised it directly, so its own guard never ran for the one refusal class
  that actually leaves an effect. That hole is the adopter's, not Core's, and it
  is worth naming because it is the shape an adopter guard naturally takes: the
  guard covered the failures it imagined and missed the one it had authored.

The finding for Core is the first bullet. The second is offered because it shows
how an adopter can hold a correct-looking partial-effect guard and still miss
this.

### Evidence

In the run's stage-A history the orphan is at sequence 9, 1,899 bytes, artifact
id `probe`. It is why that history has 22 ledger events rather than 21. The
producer ran several thousand other probes in the same session; all of them
refused with `MALFORMED_PLAN` or `UNKNOWN_GAP_KIND`, which refuse before any
effect. The ledger holds exactly one orphan artifact. That arithmetic is the
confirmation: one refusal class leaves an effect and the others do not.

A reconstruction of the same history that skipped this one probe produced the
correct graph and the correct export digest but 21 events, different check
receipts and a different replay receipt. It is kept as evidence.

### Reproducer

Nine lines, no domain content, at
`private/shop-progressive-01/recovery/stage-a/RECOVERY.md` line 177, in the
section "The one thing that had to be replayed, not skipped". The isolation
workspace is
`private/shop-progressive-01/recovery/stage-a/diagnostics/probe-ws/`, and the
21-event reconstruction that omits the probe is
`private/shop-progressive-01/recovery/stage-a/diagnostics/attempt-1-no-probe/`
(`history.jsonl` `04c139e6a904ae91a3f2424596630811afd754f4b00c97a886ffb5c1ee9e6ebb`).

In outline: submit a plan with `records` empty, `gaps` empty, `derivations`
empty. The call refuses with `NO_DOMAIN_CHANGE`. Replay the history and count
the events.

---

## 3. The per-slot source relation requirement, behind two rule failures

### The requirement, as Core's roadmap states it

`ROADMAP.md` E3, agreed 2026-09-17 (`E-0430`):

> The compiled ontology does not say whether a slot's value is copied from the
> source (a number, a unit, a formula), tallied from it (a count) or authored by
> the producer (a record's name, a category). Every "value must be in the
> source" rule needs that distinction and none can be specified without it.

Two cells measured that, independently, before the requirement was agreed. They
are offered here as the evidence behind it rather than as a new claim.

### Cell one: the paper's document path

The first attempt at a value-in-source rule refused **216 of 236** honest
records (paper ledger `E-0426`, `E-0430`). Those records were not wrong; the
rule had no way to tell a copied value from an authored one.

### Cell two: the Shop's structured-row path

The same rule was measured against an honest, already-admitted population
before anything was built on it, and it refuses **145 of the 294** retained
derivations. Every one of the 145 is correct Shop mapping, and they fall into
exactly three mechanisms, which is what makes the cell useful:

| mechanism | n | value | cites | cell text |
|---|---|---|---|---|
| mapping constant, absent from the cell | 62 | `ACTOR` | `row:0:actor_ids[0]` | `R1` |
| minted record identity, containment runs the other way | 69 | `actor:R1` | `row:0:actor_ids[0]` | `R1` |
| declared label-to-enum translation | 14 | `CREATE_ORDER` | `row:0:activity` | `Create Order` |

62 + 69 + 14 = 145. None is a transcription of the cell it cites, and none is a
defect. A derivation on this path says "this cell is why this value is here",
not "this value is the text of this cell", and the compiled contract carries
nothing that distinguishes the two claims. The rule was ruled out of that gate
rather than widened, because widening the normalisation to admit
`Place SO` to `PLACE_SUPPLIER_ORDER` would have admitted almost anything.

Two paths, two shapes of source, the same failure for the same reason. That is
the argument for putting the distinction in the ontology and carrying it through
the compiled contract and the fact contract, which is what E3 asks for.

### Where the cells are

The Shop cell, its three mechanisms and the ruling that followed are at
`research/ontology_driven_kg_realization/experiments/small_shop/content_rules/README.md`,
section "Rule 1 is not here"; the fact-contract side is in `CORE_REQUIREMENT.md`
beside it, which records 549 compiled facts, none provenance-bearing, against
294 retained derivations in the same history. The paper cell is in the paper
ledger at `E-0426` and `E-0430`.

### Two adjacent observations, not evidence for E3

Both came out of writing the adopter rules and are about what a rule can ask,
not about slot provenance. They are recorded here because they were found in the
same work, and they should not be read as supporting E3.

- A rule cannot join a record to its declared type hierarchy. `m_record/3`
  carries the record type as the caller spelled it and `m_subtype/2` carries
  registry URIs, so a rule about a category has to be written about particular
  slot names instead. Recorded at the site in the same `CORE_REQUIREMENT.md`.
- A record can name its source and say nothing. The plan compiler refuses a
  record with no derivation at all, but `UNDERIVED_FIELD` is computed over a
  record's `properties` keys and its two relation endpoints, so a record typed
  as an imported base class that declares no required slots, carrying
  `"properties": {}` and one derivation on `type`, passes compilation and the
  structural check. Only an adopter rule refuses it.

## What this handover is not

It is not a change request and carries no proposal for Core's public surface.
Findings 1 and 2 are reproducible with no domain content; finding 3 is a design
observation with two concrete cells behind it. No Core file was read into the
run's workspaces, and nothing under `src/malleus` was modified by the work that
produced these.

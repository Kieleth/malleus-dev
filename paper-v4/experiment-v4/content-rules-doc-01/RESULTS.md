# Gate 1: what the three rules refuse in run-23's honest population

**Gate 1 is not zero.** Under the policy, run-23's own honest population is
refused. `VALUE_IN_CITED_TEXT` refuses 216 of the 236 records that cite an
assertion, on 420 record-and-slot pairs. `NO_CONFLICTING_QUANTITY` refuses one
pair of records. `NO_EMPTY_RECORD` refuses nothing. The whole atomic admission
is refused with `REJECTED_CHANGE` and the ledger keeps its eleven retention
events; no admission event was written.

Gate 2 was therefore not reached and nothing was tuned. The rules, the
exclusions, the normalisation and the conflict definition are exactly the ones
[README.md](README.md) states, written before the run.

## Coordinates

| | |
| :-- | :-- |
| Core | isolated candidate `e7937b89`, fact contract version 3 |
| base population | run-23's admitted capture and records, read only |
| compiled ontology | `sha256:67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd` |
| check contract | `sha256:4f41c5d8c6dc1d93156b96c698580d390c4c2b346e74df7bed4055d1049d84ae` |
| policy | `sha256:167751588ad56aea92f28967f13c1ac387ae688a494c3a23ed86714e82e6b875` |
| engine | SWI-Prolog 10.0.2, one fresh process, 6,405 facts |
| provenance supplied | 2,720 derivations, 333 retained sentences |
| private outputs | `private/paper-v4-content-rules-doc-01/` |

## The control: Core's hardening refuses nothing here

Run-23's own `run.py`, unmodified, against the same exported Core, on the same
honest population: **admitted**, 417 entities, 1 event, 22 relations, a
fourteen-event ledger. Core's four changes at `e7937b89` — `UNDERIVED_RECORD`,
`LOCATOR_NOT_DERIVED`, `SOURCE_BINDING_REQUIRED` and the version-3 fact
contract — refuse nothing in this population. Everything below is the rule
layer, not the structural gate.

The control's plan, census, gaps, export and trace summary are byte-identical
to run-23's frozen ones. Its replay receipt is not:
`sha256:f3a014b1e347f093fd06be722b41c112705d60fbd32ffcb9e5d1aa27be501f75`
against the frozen `sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec`.
The single semantic difference is one field of the validated contract
artifact, `evidence.producer.sha256`, which binds the compiler's own source.
Core moved, so that digest moved, and the artifact identity, the ledger head,
the change-set identity and the receipt follow from it. No domain artifact
differs.

## Gate 1, per rule

| rule | records refused | pairs refused | of what population |
| :-- | --: | --: | :-- |
| `VALUE_IN_CITED_TEXT` | 216 | 420 | 236 records cite an assertion; 204 of the 440 carry no `assertion_locator` and are out of the rule's reach |
| `NO_CONFLICTING_QUANTITY` | 2 | 1 violation | 48 records carry both `subject` and `quantity_kind`, in 45 groups, 3 of which hold more than one record |
| `NO_EMPTY_RECORD` | 0 | 0 | all 440 records; every one carries at least `name` |

Distinct honest records refused across all three rules: **216**. The two
`NO_CONFLICTING_QUANTITY` witnesses are already among the 216.

Twenty records pass `VALUE_IN_CITED_TEXT`. All twenty are `Claim` records whose
only in-scope property is `name`; their other slots are the excluded
`assertion_locator`, `statement_sha256`, `assertion_modality` and `subject`.

## `VALUE_IN_CITED_TEXT`: the mechanisms

Every refused pair carries one mechanism label, assigned by observations fixed
before the run: whether the normalised value occurs in the cited sentence, in a
sentence this slot's own derivation names, in any sentence the record is
derived from, in any retained sentence at all, and whether an integral float
would match without its trailing zero. Each refusal was cross-checked against
the rule's own verdict; there are **no disagreements** between the description
and what Prolog refused.

| mechanism | pairs | what it is |
| :-- | --: | :-- |
| `IN_NO_RETAINED_SENTENCE` | 265 | The value occurs in no retained sentence of the capture. |
| `FLOAT_SPELLED_WITH_A_TRAILING_ZERO` | 122 | The value is an integer carried in a float slot. Prolog prints it with a trailing `.0` and the sentence writes the integer, so the two differ by two characters and nothing else. |
| `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | 30 | The value occurs somewhere in the capture, but not in the sentence this record cites and not in any sentence this record is derived from. |
| `NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT` | 3 | The value is a number the sentence states in another form. |

By slot:

| slot | pairs | mechanism, and why it is honest |
| :-- | --: | :-- |
| `name` | 214 | All `IN_NO_RETAINED_SENTENCE`. `name` is the producer's label for the record: a composed phrase saying which quantity of which feature the record holds. It identifies the record; it is not a phrase lifted from the sentence, and the source never writes it. 91 of the 216 refused records are refused on `name` alone. |
| `value_upper` | 66 | 64 trailing-zero floats, 1 in another sentence, 1 number written another way. A bound the source states as a whole number is carried as a float. |
| `value_lower` | 59 | 54 trailing-zero floats, 3 in another sentence, 2 numbers written another way. |
| `quantity_kind` | 21 | 13 in no sentence, 8 in another sentence. The slot holds the source's wording of the reported quantity as the producer phrases it, plural or singular, with the qualifier the record needs. |
| `count_scope` | 20 | All in no sentence. What a count includes, phrased by the producer. |
| `claim_kind` | 16 | All in no sentence. A category the producer assigns to a claim, in the producer's own words, not the source's. |
| `count` | 7 | All in another sentence. The integer occurs elsewhere in the capture but not in the cited sentence. |
| `analyte` | 6 | All in another sentence. The record carries the chemical formula; the cited sentences carry the same formula with the subscript separated from the element by a space, because the reading's text layer renders subscripts that way. The declared normalisation collapses runs of whitespace and never deletes a space, so the two do not match. |
| `estimation_proxy` | 4 | 2 in no sentence, 2 in another sentence. |
| `uncertainty` | 3 | All trailing-zero floats. |
| `numerator_kind` | 2 | Both in another sentence. |
| `ratio_value` | 1 | A trailing-zero float. |
| `unit` | 1 | In another sentence. |

Four representative rows, by record identity and slot, with the value described
rather than quoted:

| record | slot | mechanism | what the value is |
| :-- | :-- | :-- | :-- |
| `claim:fig3-panels` | `claim_kind` | `IN_NO_RETAINED_SENTENCE` | A two-word producer category for a figure caption. |
| `ratio:co2-rb` | `ratio_value` | `FLOAT_SPELLED_WITH_A_TRAILING_ZERO` | A three-digit whole number the sentence states without a decimal point. |
| `gchem:rc2-co2-minimum` | `analyte` | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | A three-character chemical formula; the cited sentence separates the subscript with a space. |
| `obs:profile-halfwidth` | `value_lower` | `NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT` | A two-digit bound the cited sentence writes with a plus-or-minus sign and with the reading's text layer spacing the digits apart. |

Every refused pair, with its exact value and the exact cited sentence, is in
`private/paper-v4-content-rules-doc-01/honest/results/refused-detail.json`.
The public `outcomes.json` beside this file carries all 420 rows by record
identity, slot, mechanism and the five observations, with no value and no
sentence, because of the leak rule.

## `NO_CONFLICTING_QUANTITY`: one pair, and why it is honest

One violation, code `QUANTITY_DISAGREEMENT`, witnesses `obs:bdb-isotherm` and
`obs:h1-isotherms`. Both concern the subject `geo:bdb`, both set
`quantity_kind` to the same string, both set `unit` to the same string, both
set `value_qualification` to `EXACT`, and neither sets `determination`,
`depth_reference` or `melt_stage`. The bounds differ: one carries an exact
point with an `uncertainty`, the other carries a two-ended interval.

It is not a disagreement in the source. Two things the definition does not look
at separate them:

1. **Modality.** The first record's `assertion_modality` is `STATED`; the
   second's is `HYPOTHESISED`, because the source is setting out an explanation
   it goes on to weigh rather than asserting a value. `assertion_modality` is
   not in the declared qualifier list, so the rule reads a hypothesis and a
   convention as two live values for one quantity.
2. **How an interval is encoded.** One record carries a centre in both bounds
   with the tolerance in `uncertainty`; the other carries the two ends in the
   bounds. `uncertainty` was deliberately excluded from the qualifiers, on the
   stated ground that it is part of the value rather than part of what the
   value is about. On this pair that decision is what makes the two encodings
   compare as different values.

The qualifier list did separate the other two multi-record groups: in both,
`value_qualification` differs (`EXACT` against `OPEN_LOWER_BOUND`, and
`APPROXIMATE` against `OPEN_UPPER_BOUND`), so neither produced a violation.

## `NO_EMPTY_RECORD`: nothing

Every one of the 440 records carries at least `name`. The rule reaches every
record kind and refuses none. Core's `UNDERIVED_RECORD` already refuses a
record with no derivation at all, so what is left for this rule on this path is
a record with a source and nothing said, and run-23's producer wrote none.

## The refusal left the history where it was

After the refused admission the ledger holds eleven events, ten
`ARTIFACT_REGISTERED` and one `SOURCE_REGISTERED`, and
`sha256:62cb6a5e5d2207ebaa6fceb9db6b7560a19353d249e46125793a9705e22be9d9`.
None of the four admission events (`KNOWLEDGE_CHANGE_SET_RETAINED`,
`CHANGE_PROPOSED`, `CHECK_RECORDED`, `VERDICT_RECORDED`) appears. The bytes
after the attempt equal the bytes before it. A violated outcome persists
nothing: the policy grammar maps `VIOLATED` to `REJECT`, and any terminal
verdict other than `ACCEPT` refuses the whole change.

## The synthetic probe

Trial `a-01` of `fault-injection-01`'s frozen catalog, which that cell admitted
under Core `c95dba7b` with nothing in the run's own artifacts to show for it,
is refused here: `REJECTED_CHANGE`, ledger unchanged, and the injected value
refused under `VALUE_NOT_IN_CITED_TEXT/analyte` on the record the catalog
targets, with the mechanism moving from `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE`
to `IN_NO_RETAINED_SENTENCE` because the synthetic value is in no sentence at
all.

**What that does and does not establish.** It establishes that the policy is
selected, that Prolog really runs, that a violated outcome refuses the whole
atomic admission, and that the rule reads the injected value. It does **not**
establish that the layer separates a fault from an honest record: the honest
value in that same slot is already refused, so the probe produces the same 420
pairs as the honest run and the fault changes only one row's mechanism. With
gate 1 at 216 records, no refusal on this population discriminates.

## What was not done

- **Gate 2 was not reached.** The twenty faults `fault-injection-01` admitted
  were not rerun through this policy. Gate 1 is the condition for that step and
  gate 1 is not zero.
- **Nothing was tuned.** No rule, exclusion, normalisation or qualifier was
  changed after a result. What a false positive costs is Luis's decision.
- **Only run-23.** The paper's other six model-produced populations were not
  rebuilt under this policy.
- **No Core change.** Nothing under `src/malleus` was read into this directory
  or modified. The candidate Core was consumed through `git archive` alone.
- **The rule is silent where it cannot read.** A record citing a locator with
  no retained text produces no violation and no `UNKNOWN`; the engine returns
  violations only. Every locator in this capture has retained text, so the case
  did not arise here.

## Counterfactual counts, measured after gate 1, nothing applied

These are counts over the 420 frozen rows in `outcomes.json`. **No rule,
exclusion, normalisation or qualifier changed.** `rules.pl`, `policy.json` and
`logic.yaml` are the files gate 1 ran with, the check contract is still
`sha256:4f41c5d8c6dc1d93156b96c698580d390c4c2b346e74df7bed4055d1049d84ae`, and
nothing was rerun. They exist so the cost of each option Luis has is a number
rather than a guess.

The counterfactual waives a refused pair when either condition holds:

1. the slot is one of the four producer-composed label slots, `name`,
   `claim_kind`, `count_scope` or `quantity_kind`; or
2. the mechanism is `FLOAT_SPELLED_WITH_A_TRAILING_ZERO`, that is, an integral
   float compared equal to its integer spelling.

A record remains refused when at least one of its pairs is waived by neither.

| | records | pairs |
| :-- | --: | --: |
| gate 1, as run | 216 | 420 |
| label slots waived alone | 89 | 149 |
| integral floats waived alone | 216 | 298 |
| **both waived together** | **20** | **27** |

The two waivers are far stronger together than either apart, because the two
classes cover disjoint records: 127 records are refused only on label slots and
every one of the 216 also carries at least one non-float refusal. Neither
waiver alone reaches a useful number; both together leave twenty records.

### What is left, by slot and mechanism

Twenty-seven pairs on twenty records.

| slot | pairs | mechanism | what it is |
| :-- | --: | :-- | :-- |
| `count` | 7 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | An integer the capture holds somewhere, but not in the sentence the count record cites. |
| `analyte` | 6 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | The subscript spacing: the record carries the formula, the cited sentence separates the subscript by a space. |
| `value_lower` | 3 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | A non-integral bound the capture holds elsewhere. |
| `value_lower` | 2 | `NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT` | The plus-or-minus bounds, including one where the reading's text layer spaces the digits apart. |
| `estimation_proxy` | 2 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | The element an estimate was derived from, named in another sentence. |
| `estimation_proxy` | 2 | `IN_NO_RETAINED_SENTENCE` | The same slot where the producer's wording appears in no sentence at all. |
| `numerator_kind` | 2 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | The same subscript spacing, in a ratio's numerator kind. |
| `value_upper` | 1 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | |
| `value_upper` | 1 | `NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT` | |
| `unit` | 1 | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | |

By mechanism, counting a record once per mechanism it carries: 19 records
`IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE`, 2 `IN_NO_RETAINED_SENTENCE`,
2 `NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT`. By record type: 12 pairs on
`GeochemicalObservation`, 7 on `CountObservation`, 6 on
`GeophysicalObservation`, 2 on `ElementRatio`.

The twenty records:

| record | remaining slots |
| :-- | :-- |
| `cnt:location-categories` | `count` |
| `cnt:min-obs-per-event` | `count` |
| `cnt:new-focal-mechanisms` | `count` |
| `cnt:relocation-iterations` | `count` |
| `cnt:subsections` | `count` |
| `cnt:velest-iterations` | `count` |
| `cnt:velocity-models` | `count` |
| `gchem:eq-atlantic-co2-avg` | `analyte`, `estimation_proxy` |
| `gchem:eq-atlantic-co2-max` | `analyte`, `estimation_proxy` |
| `gchem:rc2-co2-minimum` | `analyte` |
| `gchem:rc2-co2-primary-calc` | `estimation_proxy`, `value_lower` |
| `gchem:rc3-co2-ba` | `analyte` |
| `gchem:rc3-co2-primary-calc` | `estimation_proxy`, `value_lower` |
| `gchem:rc3-co2-rb` | `analyte` |
| `gchem:swir-co2-highest` | `analyte` |
| `obs:magnitude-completeness` | `value_lower`, `value_upper` |
| `obs:profile-halfwidth` | `unit`, `value_lower`, `value_upper` |
| `obs:velocity-perturbation` | `value_lower` |
| `ratio:co2-ba` | `numerator_kind` |
| `ratio:co2-rb` | `numerator_kind` |

### The conflict pair is not among them

`obs:bdb-isotherm` and `obs:h1-isotherms` are both waived out of rule 1 by the
counterfactual: every rule-1 pair they carry is a label slot or an integral
float. `NO_CONFLICTING_QUANTITY` would still refuse both, so the distinct
honest records refused under the counterfactual would be **22**, not 20: the
twenty above plus those two, on the conflict rule alone.

### What this does not say

It does not say the waivers are right. Waiving the four label slots concedes
that `name`, `claim_kind`, `count_scope` and `quantity_kind` are producer
wording rather than transcribed values, which is a claim about what those slots
are for and needs a ruling, not a count. Waiving integral floats concedes that
the rule should compare numbers numerically rather than by spelling, which is a
change to the declared normalisation. Both are decisions; only their cost is
measured here.

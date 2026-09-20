# The census: what each candidate would refuse, and why

**Every refusal on both honest populations is a rule defect. There are no graph
defects and no undecided refusals.** 127 refusal rows across five candidates,
two populations, two scopes and every declared reading; 0 classified
`GRAPH_DEFECT`, 0 classified `UNDECIDED`.

Under the reading each candidate was written for, the counts are small enough
to read one by one:

| candidate | run-23 | Shop | reach on run-23 |
| :-- | --: | --: | :-- |
| (a) `NO_CONFLICTING_QUANTITY`, shipped qualifier list | 1 violation, 2 records | not declared | 55 records in 54 groups |
| (a) the same, `assertion_modality` added | **0** | not declared | 55 records in 55 groups |
| (b) `INTERVAL_SANITY` | **0** | not declared | 216 record-and-slot pairs |
| (c) `NUMBER_IN_CITED_TEXT`, `UNGLUED`+`FREE` | 1 refusal, 1 record | **0** | 214 pairs; Shop 6 |
| (c) the same, `GLUED`+`ATTACHED` | 1 refusal, 1 record | **0** | as above |
| (c) the same, `GLUED`+`FREE` | 51 refusals, 34 records | 0 | as above |
| (d) `UNIT_IN_SOURCE`, `GLUED` | 1 refusal, 1 record | not declared | 103 records |
| (e) `FORMULA_IN_SOURCE`, `GLUED` | **0** | not declared | 24 pairs |
| (e) the same, `UNGLUED` | 8 refusals, 8 records | not declared | as above |

For comparison, and measured by the earlier cell rather than here: the rule
these replace, "every property value appears in the cited sentence, whitespace
and case folding only", refused 216 of run-23's 236 citing records on 420
record-and-slot pairs, and the same family refused 145 of the Shop's 294 honest
derivations. Typed comparison and one declared normalisation move that to three
distinct refusals, all of them rule defects with a named cause.

## Coordinates

| | |
| :-- | :-- |
| Core | `private/shop-progressive-01/runtime`, commit `e7937b89`, fact contract version 3, asserted by `test_census.py` before any measurement |
| document population | 440 records, 236 carrying `assertion_locator`, 333 retained assertions, 2,720 derivations |
| document ontology | `sha256:67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd`, run-23's own, asserted |
| document extraction | `malleus.compiler.adapt_document_assertions` over copies of run-23's inputs; the derivation list is byte-order-identical to run-23's frozen `results/population-plan.json`, asserted |
| Shop population | 21 Table 1 rows, 106 current records, 294 derivations, 130 distinct cell locators, all 130 resolved |
| Shop ontology | `sha256:e82f3569b9be903fd060e1e878bfd6d433140df751141b0efd6dbdd41aa34058` |
| private outputs | `private/paper-v4-rule-census-01/`, `git check-ignore -v` confirmed before the first write and asserted in the suite |

Nothing under `private/paper-v4-v4-run-23/` was opened for writing; the census
copies the six closure files, the reading and the population into its own
private workspace first, which `test_census.py` asserts. Nothing under
`src/malleus` was read into this directory or changed. No Prolog ran, no policy
was composed, no history was admitted, and no model was called.

## RED before GREEN

Two RED runs on the normalisation, because the spec gained an axis between
them, and one on the census.

| suite | RED | GREEN |
| :-- | :-- | --: |
| `test_normalise.py`, first | 67 failed, 1 passed | |
| `test_normalise.py`, after the `FREE`/`ATTACHED` axis | 9 failed, 60 passed | 74 passed |
| `test_census.py` | 3 failed, 3 passed, 21 errors | 32 passed |
| whole cell | | **106 passed** |

The first RED ran against a stub that declared the public surface and raised
`NotImplementedError`, so the failures are per behaviour rather than one
collection error. `ruff check` and `ruff format --check` are clean on all four
files.

**Two disclosures about the specification, both before any count existed.**

1. The task's declared normalisation and its numeric parsing collide. Closing
   a space between a letter and the digit after it is what makes a formula
   match its sentence; it also welds the digits of an honest number onto the
   word in front of them. The census therefore measures candidate (c) under
   three readings and reports all three, rather than picking one. The axis was
   added to `README.md` and to `normalise.py` after the first implementation
   showed the collision and before the census ran.
2. The task names five numeric slots. The compiled contract declares eight with
   a `Float` or `Integer` range on a type this population uses:
   `assertion_confidence`, `publication_year` and `strength` as well. Reading
   the contract rather than the named list is what
   `DECLARED_DISTINCTIONS_ONLY` asks for, so both were measured. They give
   identical refusal rows on run-23, asserted by a test, because
   `assertion_confidence` and `strength` are set on no record and
   `publication_year` is set only on the 80 `ReferencedWork` records, none of
   which cites an assertion. The difference between a named list and a declared
   range is zero here, and it is zero as a measured fact rather than as an
   assumption.

## The declared normalisation, as it ran

Declared once in [`normalise.py`](normalise.py), applied to every string this
cell compares, sentence and slot value alike. In order: the seven ligatures
U+FB00 to U+FB06 become their letters; a hyphen followed by whitespace inside a
word closes; one whitespace character beside a `.` or `,` that sits between two
digits is removed, and so is one whitespace character directly between two
digits, both to a fixed point; under `GLUED` only, one whitespace character
between a letter and the digit after it is removed; whitespace runs collapse to
one space and the ends are stripped; `str.casefold()`.

The numbers read out of a normalised string: signed digit runs with an optional
decimal point, where `-` and U+2212 are signs only when no digit or `.`
precedes them and an en or em dash never is; the twenty-eight number words
`zero` to `twenty` plus the tens, each bounded as a word, so `tendency` yields
nothing and `twenty-five` yields 20 and 5 rather than 25; `a ± b` additionally
yielding `a-b` and `a+b`; thousands separators not read, so `1,234` yields 1
and 234. Comparison is exact through `decimal.Decimal`, so `991.0` equals `991`
and `1.50` equals `1.5`.

What the capture's 333 retained sentences hold, counted rather than assumed: 90
ligatures; 5 decimal points with a whitespace character beside them; 89
digit-whitespace-digit pairs; 102 hyphen-whitespace breaks inside a word; 110
dash-separated number pairs; 209 letter-whitespace-digit pairs, 38 of them the
carbon-dioxide formula and 4 the water formula; 10 plus-or-minus signs; 22
percent signs, 6 of them directly after a number; 1 U+2212 minus sign; and no
spaced thousands separators.

## Candidate by candidate

### (a) `NO_CONFLICTING_QUANTITY`

Reads `subject` (declared range `Entity`), then `quantity_kind`, `count_scope`,
or `numerator_kind` with `denominator_kind` (all `String`) as the quantity
identity, then `value_lower`/`value_upper` (`Float`), `count` (`Integer`) or
`ratio_value` (`Float`) as the value, with the eleven declared qualifiers in
the group key.

On run-23: 55 records enter the comparison, in 54 groups. One group holds two
records and they carry different bounds, so one violation, witnesses
`obs:bdb-isotherm` and `obs:h1-isotherms`. That is the same violation and the
same two witnesses the Prolog rule produced in `content-rules-doc-01`, reached
here by a separate implementation in Python, which is the cross-check the
result rests on.

With `assertion_modality` (declared range `AssertionModality`) added to the
qualifier list: 55 groups, none holding more than one record, **zero
violations**.

On the Shop: the compiled contract declares no `subject`, no `quantity_kind`,
no `count_scope` and no `numerator_kind`, so the rule as written reads nothing
there. That is a shape difference between the two consumers, not a pass. The
Shop's own already-shipped conflict rule keys on `order_id`, `product_code` and
`ordered_quantity`; measured separately under the label
`SHOP_OWN_CONFLICT_KEYING`, it finds zero violations on the six current
quantity states, and it is not counted as candidate (a).

### (b) `INTERVAL_SANITY`

Four typed clauses, no text read: `value_lower <= value_upper`,
`uncertainty >= 0`, `count >= 0`, `ratio_value >= 0`. Reach is every record
that sets the slot, citation or not, because the rule reads no sentence: 88
`value_lower`, 98 `value_upper`, 22 `count`, 5 `uncertainty`, 3 `ratio_value`.

**Zero refusals on run-23.** The clause is not vacuous: a test plants an
inverted pair on one record that declares both bounds and the clause fires.

On the Shop: none of the four slots is declared. The nearest declared analogue,
`ordered_quantity >= 0` (`Integer`), is measured separately under the label
`SHOP_NON_NEGATIVE_QUANTITY` and finds zero.

### (c) `NUMBER_IN_CITED_TEXT`

Reads `value_lower`, `value_upper`, `uncertainty`, `count` and `ratio_value`,
which are the `Float` and `Integer` ranges the contract declares on the types
that also declare `assertion_locator`. 214 record-and-slot pairs are in reach of
the cited scope; 2 more set a bound on a record that cites nothing and are out
of reach of a rule that compares against a citation.

| reading | run-23 refusals | records | by slot |
| :-- | --: | --: | :-- |
| `UNGLUED`+`FREE` | 1 | 1 | `value_lower` 1 |
| `GLUED`+`ATTACHED` | 1 | 1 | `value_lower` 1 |
| `GLUED`+`FREE` | 51 | 34 | `value_lower` 26, `value_upper` 18, `count` 7 |

On the Shop: `ordered_quantity` is the one numeric-ranged slot, six current
records set it, and **all six values are found in the cell the record's own
derivation names, under all three readings**. Six values is a thin second
consumer and this file says so rather than presenting it as a strong pass; what
it does establish is that the candidate is not document-shaped, because it
reads a declared numeric range and a resolved locator and the Shop supplies
both.

The `GLUED`+`FREE` reading is degenerate and is reported, not dropped. 50 of
its 51 refusals carry the same value that both other readings find in the same
sentence; the gluing has welded the number onto the word in front of it, so no
free-standing number is left to parse. All 51 were read individually against
their cited sentences.

### (d) `UNIT_IN_SOURCE`

Reads `unit`, declared `String` on four types; 103 records set it and cite an
assertion. **One refusal**, `obs:profile-halfwidth`, under both normalisation
profiles and both scopes.

### (e) `FORMULA_IN_SOURCE`

Reads `analyte`, `numerator_kind` and `denominator_kind`, all declared
`String`; 24 record-and-slot pairs in reach.

**Zero refusals under `GLUED`.** Under `UNGLUED`, 8 refusals on 8 records,
`analyte` 6 and `numerator_kind` 2; every one is the carbon-dioxide formula
whose subscript the reading's text layer sets off with a space, and every one
matches under `GLUED`. This is the single case where the letter-to-digit gluing
earns its place.

## The two scopes are identical here

Widening from the cited sentence to every sentence the record derives from
changes nothing: 1 and 1 for (c) under `UNGLUED`+`FREE`, 51 and 51 under
`GLUED`+`FREE`, 1 and 1 for (d), 8 and 8 for (e) under `UNGLUED`, 0 and 0 for
(e) under `GLUED`. Every refusal that survives the cited scope survives the
derived one too, because none of them is a value the record found in another of
its own sentences. The suite also asserts the derived scope is never wider than
the cited one, so the equality is a measured result and not an artefact of
reading the same text twice.

This is worth stating plainly because the earlier rule's largest residual class
was exactly "the value is in a sentence the record does not cite". Under typed
comparison that class is empty.

## Classification, per class per mechanism

127 rows, every one `RULE_DEFECT`.

| candidate | reading | mechanism | rows | class |
| :-- | :-- | :-- | --: | :-- |
| `NO_CONFLICTING_QUANTITY` | | `QUANTITY_DISAGREEMENT` | 1 | `RULE_DEFECT` |
| `NUMBER_IN_CITED_TEXT` | `UNGLUED_FREE` | `IN_NO_RETAINED_SENTENCE` | 2 | `RULE_DEFECT` |
| `NUMBER_IN_CITED_TEXT` | `GLUED_ATTACHED` | `IN_NO_RETAINED_SENTENCE` | 2 | `RULE_DEFECT` |
| `NUMBER_IN_CITED_TEXT` | `GLUED_FREE` | `IN_NO_RETAINED_SENTENCE` | 2 | `RULE_DEFECT` |
| `NUMBER_IN_CITED_TEXT` | `GLUED_FREE` | `MATCHES_UNDER_ANOTHER_DECLARED_READING` | 100 | `RULE_DEFECT` |
| `UNIT_IN_SOURCE` | `GLUED` | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | 2 | `RULE_DEFECT` |
| `UNIT_IN_SOURCE` | `UNGLUED` | `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE` | 2 | `RULE_DEFECT` |
| `FORMULA_IN_SOURCE` | `UNGLUED` | `MATCHES_UNDER_THE_OTHER_PROFILE` | 16 | `RULE_DEFECT` |

Row counts double where a refusal holds under both the cited and the derived
scope. Three distinct records carry all the non-degenerate refusals.

### The three distinct rule defects

**One, the conflict pair.** `obs:bdb-isotherm` and `obs:h1-isotherms` report
the same quantity kind of the same subject with different bounds. One is
`STATED` and the other is `HYPOTHESISED`: the source states a convention, and
then sets out an explanation it goes on to weigh. The shipped qualifier list
does not read `assertion_modality`, so the rule compares a hypothesis against a
convention and calls it a disagreement. The records and their citations are
right. Adding the qualifier removes the refusal and adds no other.

**Two, the bare plus-or-minus.** `obs:velocity-perturbation` carries a
symmetric perturbation as a negative lower bound and a positive upper bound.
The cited sentence states it once, as a plus-or-minus with no left operand. The
declared grammar reads `a ± b` and produces `a`, `b`, `a-b` and `a+b`; from a
bare `± b` it produces `b` alone, so the negative end is unreachable. The
record and its citation are right; the grammar is one production short. The
production was **not** added. Adding it after seeing the count is the tuning
this cell exists to avoid, and whether the grammar should read a bare
plus-or-minus as a two-ended interval is a definition for Luis, not a repair.
The cost of not adding it is exactly one refusal on this population.

**Three, the character-spaced caption.** `obs:profile-halfwidth` carries a
two-letter unit. Its cited block is a figure caption whose text layer sets a
long run of it one character at a time, so the two letters of the unit are not
adjacent in the retained bytes. The declared normalisation closes letter-to-
digit spacing and hyphen breaks; it does not close spacing inside a word, and
widening it to do so would join unrelated words throughout the reading. The
record is right about the unit the source states. The mechanism label this
refusal carries, `IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE`, is
technically true and misleading: the unit does occur in other sentences, but
that is not why this one refused. The labels were fixed before the run and were
not rewritten to fit; the reason line in the private file carries the real
cause, and so does this paragraph.

### No undecided refusals

Every one of the 127 rows is matched by an entry of the declared classification
table in [`census.py`](census.py), and a row matching no entry falls to
`UNDECIDED` and fails a test. There is nothing on this population that could
not be decided by reading the record and its cited sentence.

### No graph defects

None of the five candidates found a wrong value or a wrong citation in either
honest population. Two specific suspicions recorded at ledger entry E-0430,
formed from sentence heads alone and marked unconfirmed there, were checked
against the full records and the full cited sentences and neither survives:

- The seven `CountObservation` records that the earlier rule refused because
  their integer appeared in no cited sentence all cite a sentence that states
  the number as an English word. One of them, the record about relocation
  iterations, cites a sentence that states two numbers, six catalogue links and
  five iterations; the record carries five, which is the one its own scope
  names. The citation is correct.
- The geochemistry records naming the two ridge segments each cite a sentence
  that names the segment the record is about. Several of those sentences name
  both segments and give a value for each; in every case the record carries the
  value the sentence gives for its own segment. No segment is confused with
  another.

**What that does and does not establish.** It establishes that these candidates
refuse no honest record for a reason other than their own definition, and that
the two suspicions raised earlier do not hold. It does not establish that
run-23's population is faithful to its source. The candidates read five numeric
slots, one unit slot and three formula slots; they never read `name`,
`description`, `claim_kind`, `count_scope`, `quantity_kind` or
`estimation_proxy`, which is most of what a producer writes, and the ontology
declares nothing that would let a rule tell a copied value from an authored one.
That gap is the Core requirement E-0430 recorded and it is unchanged.

## What could not be done

- **The cell is not registered under the paper gate.**
  `paper-v4/active-test-manifest.json` is modified in the working tree by
  another session, so nothing was added to it and no private fixture was
  pinned in `answer-demonstration/test_gate_integration.py`. Registration of
  this cell, with `private/paper-v4-rule-census-01` pinned, is owed; it is the
  same debt `content-rules-doc-01`, `bridge-01` and `fault-injection-02`
  already carry.
- **The Shop is a thin second consumer for (c) and no consumer at all for (a),
  (b), (d) and (e).** Its compiled contract declares one numeric slot, set on
  six current records. A candidate that reads a unit, a formula or a quantity
  kind has one consumer in this census, which by `CENSUS_FIRST` makes it an
  adapter for the document path until a second shaped consumer exists. Saying
  so is the point of measuring both.
- **Only run-23.** The paper's other six model-produced populations were not
  measured.
- **No fault population.** The census measures honest populations only. What
  each candidate would catch is not measured here, and the fault catalogue was
  not rerun. E-0430 already recorded that the catalogue holds nothing candidates
  (a) and (b) could catch.
- **The `GLUED`+`ATTACHED` reading is more permissive than it looks.** It reads
  the digits of a segment name or a figure number as numbers, so a wrong value
  that happens to equal one of them would pass. It is reported because it is a
  defensible reading of the task, not because it is the safer one.
- **No rule was chosen, adopted, proposed or recommended.** That is Luis's call
  from the table above.

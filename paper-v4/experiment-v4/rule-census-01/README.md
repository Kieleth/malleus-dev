# A census of five candidate adopter rules over two honest populations

Read-only. Nothing here is a rule. No Prolog, no policy, no check contract, no
gate, no admission, no history is written by the census itself. The output is a
table per candidate per population, a classification of every refusal, and the
code that produced both. Luis picks rules from the table; this cell picks
nothing and recommends nothing.

The cell exists because a rule was chosen once without this table.
`VALUE_IN_CITED_TEXT` refused 216 of 236 honest run-23 records
([content-rules-doc-01/RESULTS.md](../content-rules-doc-01/RESULTS.md)) and the
same family refused 145 of 294 honest Shop derivations
([small_shop/content_rules/README.md](../../../research/ontology_driven_kg_realization/experiments/small_shop/content_rules/README.md)).
The RCA and Luis's rulings are ledger entry E-0430; the six rules they produced
are `Choose an adopter rule` in
[`.claude/skills/malleus-dev/SKILL.md`](../../../.claude/skills/malleus-dev/SKILL.md).
`CENSUS_FIRST` is the one this cell executes.

Everything in this file was written before the census ran. Nothing in it was
changed after a count.

## Coordinates

| | |
| :-- | :-- |
| Core | the export at `private/shop-progressive-01/runtime`, commit `e7937b89`, fact contract version 3 |
| document population | run-23's admitted capture and records, read only, from `private/paper-v4-v4-run-23/producer` |
| document derivations | the plan `malleus.compiler.adapt_document_assertions` emits from that capture, cross-checked against run-23's frozen `results/population-plan.json` |
| Shop population | the honest Table 1 population, built through `connected_story.run.run_story` |
| private outputs | `private/paper-v4-rule-census-01/`, confirmed ignored by `git check-ignore -v` before the first write |

Core is put first on `PYTHONPATH` and the test command clears the repository's
own pytest `pythonpath` with `-o pythonpath=`, the way
[content-rules-doc-01/README.md](../content-rules-doc-01/README.md) states, so
neither the working checkout's `src` nor an installed wheel can shadow it.
`test_census.py` asserts the resolved `malleus.__file__` and the fact contract
version before any measurement, the way
`private/shop-progressive-01/d0/tests/test_environment.py` does.

### Why the Shop population is built through `connected_story`, not `content_rules`

`content_rules/run.py` and `fact_census.py` were read for how; neither is
imported and neither is modified. They are untracked and another session may be
editing them. `content_rules/run.py:honest_plans` calls
`connected_story.run.build_plan` for every Table 1 row and its README records
that the resulting domain records are identical to the connected story's, so
this census calls the same adapter through `run_story` and reads the retained
plans out of the history, which is what `fact_census.py` does. The
`connected_story` tree in the Core export is byte-identical to the working
checkout's.

## The two populations

**Document.** 440 records; 236 of them carry `assertion_locator`. 333 retained
assertions, each with an id and a verbatim statement. 2,720 field derivations,
each naming one assertion id as its locator.

**Shop.** 21 Table 1 rows; 106 current records, 107 historical. 294
derivations, each naming a cell as `row:N:field`. The source is a JSONL whose
cells are short strings, not sentences.

They have different shapes on purpose, which is what `CENSUS_FIRST` asks for: a
candidate that only makes sense on one of them is an adapter for that one, and
this file says so per candidate rather than leaving it to be discovered later.

## The declared normalisation

Declared once, in [`normalise.py`](normalise.py), and applied identically to
every string compared in this cell: to a sentence, to a cell, and to a slot
value. No candidate declares its own.

Applied in this order:

1. **Ligatures.** Each of U+FB00 to U+FB06 becomes its letters: `ﬀ`→`ff`,
   `ﬁ`→`fi`, `ﬂ`→`fl`, `ﬃ`→`ffi`, `ﬄ`→`ffl`, `ﬅ`→`st`, `ﬆ`→`st`.
2. **Hyphen-space breaks inside a word.** A letter, then `-`, then one or more
   spaces, then a letter, loses the hyphen and the spaces: `sig- ni` → `signi`.
3. **Spaced digit sequences.** One whitespace character on either side of a `.`
   or a `,` that sits between two digits is removed: `1 . 5` → `1.5`,
   `7.`+newline+`2` → `7.2`. One whitespace character directly between two
   digits is removed too: `1 0` → `10`, `1 5 0` → `150`. Both are applied until
   they reach a fixed point. Neither joins a digit to a letter. The capture
   holds 5 decimal points with a whitespace character beside them and 89
   digit-whitespace-digit pairs, most of the latter from passages the text
   layer renders one character at a time.
4. **Letter-to-digit gluing.** One whitespace character between a letter and a
   digit that follows it is removed: `CO 2` → `CO2`, `H 2O` → `H2O`. It never
   runs the other way, so `H 2 O` becomes `H2 O` and not `H2O`. **This step is
   the one ambiguity in
   the task that changes a count, so it is measured both ways and neither
   reading is preferred.** It closes `CO 2` and `H 2`, which is what makes a
   formula match its sentence; it also closes `of 1`, `the 2` and `at 1`, which
   destroys a standalone number the sentence really states. The capture holds
   209 letter-space-digit occurrences, 38 of them `CO 2` and 4 `H 2`.
5. **Whitespace.** Every maximal run of space, tab, newline, carriage return,
   vertical tab, form feed and no-break space becomes one space; leading and
   trailing runs are removed.
6. **Case.** `str.casefold()`.

Two normalisation profiles are declared, and every text-reading candidate is
measured under both:

- `GLUED`: steps 1 to 6.
- `UNGLUED`: steps 1, 2, 3, 5, 6. Step 4 omitted.

Nothing else is normalised. No punctuation stripping, no Unicode NFKC, no unit
folding, no accent folding, no stemming, no number reformatting.

## The number grammar

Declared once, in [`normalise.py`](normalise.py), over a normalised string.

A token is a run of digits with an optional single `.` and at most one group of
digits after it. Thousands separators are not read: `1,234` yields `1` and
`234`, and the census reports how often that shape occurs rather than
special-casing it.

- **Sign.** A `-` or U+2212 immediately before a digit is a sign only when the
  character before it is not a digit and not a `.`. An en dash U+2013 or em
  dash U+2014 is never a sign, so `1.5–2.0` yields `1.5` and `2.0`, not `-2.0`.
- **Number words.** `zero` to `twenty`, and `thirty`, `forty`, `fifty`,
  `sixty`, `seventy`, `eighty`, `ninety`, each as a whole word. A compound such
  as `twenty-five` yields `20` and `5`, its two parts, and never `25`. The
  census reports whether any compound occurred.
- **Plus-or-minus.** `a ± b`, where both are tokens already parsed, also yields
  `a-b` and `a+b`.
- **Ranges.** `a–b`, `a—b` and `a to b` yield both ends, which the token scan
  already supplies; the rule exists so the dash is never read as a sign.
- **Percentages and units.** Left aside. `5%` yields `5`; `12 km` yields `12`.

**A digit run written against a letter.** Two readings, both measured, neither
preferred, because this is the second thing in the task that changes a count:

- `FREE`: a number is a digit run the text writes on its own, with no letter
  and no digit immediately before it. `RC3` yields nothing; `CO 2` yields `2`
  under `UNGLUED` and nothing under `GLUED`, because gluing has closed the
  digit onto its element.
- `ATTACHED`: every digit run is a number wherever it sits. `RC3` yields `3`,
  `co2` yields `2`. This reading is provably independent of the normalisation
  profile, and `test_normalise.py` asserts that rather than assuming it.

The two axes interact, and the interaction is the finding rather than a detail:
under `GLUED` and `FREE`, `a value of 991 metres` normalises to `a value of991
metres` and yields **no number at all**, because the same step that makes `CO2`
match `CO 2` also welds `991` to the word before it. The census therefore
reports candidate (c) under three readings, `UNGLUED`+`FREE`,
`GLUED`+`ATTACHED` and `GLUED`+`FREE`, and states plainly that the third is
degenerate rather than quietly dropping it.

**Disclosure.** This second axis was not in the first version of this file. It
was added after the first implementation of `normalise.py` showed that the
task's single declared normalisation and its numeric parsing collide on
`of 991`. It was added before any census ran and no count existed when it was
added, so nothing here was tuned to a result. The first RED and the RED after
the axis was added are both in [RESULTS.md](RESULTS.md).

Comparison is numeric and exact, through `decimal.Decimal`, never by spelling.
A float slot value is converted with `Decimal(repr(value))`, an integer with
`Decimal(value)`. `991.0` equals `991`. `1.50` equals `1.5`. No tolerance.

## The five candidates

Each names the slots it reads and the declared range in run-23's compiled
contract that justifies reading them. A candidate reads no slot the compiled
ontology does not declare with that range, and approximates no distinction the
ontology lacks (`DECLARED_DISTINCTIONS_ONLY`). Where the ontology cannot say
whether a value is copied from the source, tallied from it, or authored by the
producer, the candidate does not guess: it reads the range and nothing else.

### (a) `NO_CONFLICTING_QUANTITY`

Exactly as [content-rules-doc-01/README.md](../content-rules-doc-01/README.md)
defines it: two current records that state a different value for the same
quantity of the same subject.

- **Same subject**: `subject`, declared range `Entity` on `Claim`,
  `CountObservation`, `ElementRatio`, `GeochemicalObservation` and
  `GeophysicalObservation`. A record that does not set it is not compared.
- **Same quantity kind**, by the mixin the record wears: `quantity_kind`
  (`String`) for `Quantified`; `count_scope` (`String`) for `Counted`;
  `numerator_kind` and `denominator_kind` (`String`) together for `Ratio`.
- **Different value**: the pair (`value_lower`, `value_upper`), both `Float`;
  or `count`, `Integer`; or `ratio_value`, `Float`. An absent bound differs
  from any number.
- **Qualifiers that must agree**: `unit`, `determination`,
  `value_qualification`, `depth_reference`, `melt_stage`, `analyte`,
  `estimation_proxy`, `begins_at`, `ends_at`, `temporal_precision`,
  `temporal_reference_system`. Agreement means neither sets the slot, or both
  set it equal. `uncertainty` is deliberately not a qualifier.
- **Scope**: current records. Run-23 carries zero supersessions.

Measured twice: **without** `assertion_modality` in the qualifier list, which
is the shipped definition, and **with** it added. `assertion_modality` is
declared with range `AssertionModality` on the same five types that declare
`subject`.

Shop reach: the Shop's compiled contract declares neither `subject` nor
`quantity_kind` nor `count_scope` nor `numerator_kind`, so this definition
reads nothing there and refuses nothing there for that reason and no other. The
Shop's own already-shipped conflict rule keys on `order_id` (`ShopObject`),
`product_code` (`String`) and `ordered_quantity` (`Integer`); that is a
different rule and is measured separately under the label
`SHOP_OWN_CONFLICT_KEYING`, never counted as candidate (a).

### (b) `INTERVAL_SANITY`

Typed, internal to one record, no text read.

- `value_lower <= value_upper` when both are set. Both `Float`.
- `uncertainty >= 0` when set. `Float`.
- `count >= 0` when set. `Integer`.
- `ratio_value >= 0` when set. `Float`.

Each clause fires only when its slots are set; an absent slot is not a
refusal. Comparison is `Decimal`.

Shop reach: none of the four slots is declared in the Shop's compiled contract.
The nearest declared analogue is `ordered_quantity >= 0`, `Integer`, measured
separately under the label `SHOP_NON_NEGATIVE_QUANTITY`.

### (c) `NUMBER_IN_CITED_TEXT`

Numeric slots only: `value_lower`, `value_upper`, `uncertainty` (`Float`),
`count` (`Integer`), `ratio_value` (`Float`). Those five are exactly the slots
this contract declares with a `Float` or `Integer` range on a record type that
also declares `assertion_locator`; no string slot is read and no slot is
excluded by name.

The value must be numerically equal to one of the numbers the grammar above
parses from the normalised text in scope, under each of the three declared
readings: `UNGLUED`+`FREE`, `GLUED`+`ATTACHED` and `GLUED`+`FREE`.

Shop reach: `ordered_quantity`, `Integer`, the Shop's only numeric-ranged
slot. Measured.

### (d) `UNIT_IN_SOURCE`

The `unit` slot, declared range `String` on `CountObservation`,
`GeochemicalObservation`, `GeophysicalObservation` and `SeismicEvent`. Its
normalised value must occur as a substring of the normalised text in scope.

Shop reach: no `unit` slot is declared. Nothing measured.

### (e) `FORMULA_IN_SOURCE`

`analyte` (`String`, on `GeochemicalObservation`), `numerator_kind` and
`denominator_kind` (`String`, both on `ElementRatio`). Each normalised value
must occur as a substring of the normalised text in scope.

Shop reach: none of the three is declared. Nothing measured.

## The two scopes

Candidates (c), (d) and (e) are measured under both, so the two can be
compared. The scopes are not a choice this cell makes.

- `CITED`: on the document, the statement of the assertion the record's own
  `assertion_locator` names, which is the scope `VALUE_IN_CITED_TEXT` used. On
  the Shop there is no record-level citation slot, so the narrow scope is the
  cell that this slot's own derivation names. That difference is a shape
  difference between the two consumers, stated here rather than smoothed over.
- `DERIVED`: every sentence, or cell, that any derivation of that record names.

## The classification

Every refusal carries exactly one class, assigned by reading the record and the
text it cites.

- `RULE_DEFECT`: the record and its citation are right and the candidate is
  wrong about an honest value.
- `GRAPH_DEFECT`: the record is wrong. Its value or its citation does not match
  the source.
- `UNDECIDED`: neither can be established from what is retained. The reason is
  written out per refusal.

A candidate is never edited to lower its count. Where a candidate's definition
is wrong, [RESULTS.md](RESULTS.md) says so and keeps the count.

## Outputs

- [`RESULTS.md`](RESULTS.md): the tables, the RED and GREEN test counts, every
  `UNDECIDED`, and what could not be done.
- [`outcomes.json`](outcomes.json): one row per refusal, by record id, slot,
  candidate, scope, profile, mechanism and class. No value, no sentence.
- `private/paper-v4-rule-census-01/`: the same rows with the value and the
  text, plus one line of reason per refusal.

## Leak rule

No public file in this directory shares a 60-character normalised run with the
selected reading. `test_census.py` applies `fault-injection-01`'s own check
over every public file here, `RESULTS.md` and `outcomes.json` included. Public
rows carry ids, slots, mechanisms and classes only; a `GRAPH_DEFECT` row names
the record and the slot and describes the defect in the census author's words
without quoting the sentence. The Shop source is a public synthetic table and
is not covered by this rule.

## What this is not

- Not a rule. Nothing here runs at admission and nothing is proposed for
  adoption.
- Not a Core change and not a request for one. Nothing under `src/malleus` was
  read into this directory or modified.
- Not a verdict on run-23's population. A `GRAPH_DEFECT` here is one reader's
  reading of one sentence, recorded so Luis can see it, not a correction.
- Not a claim about the paper's other six model-produced populations. Only
  run-23 and the Shop were measured.
- Not a replacement for the review protocol. It verified question answers, not
  citations, so zero refusals was never established on this dimension
  (E-0430, cause 4).

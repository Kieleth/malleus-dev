# Four adopter rules on the document path

`rule-census-01` measured five candidates read-only over two honest
populations and refused to choose ([RESULTS.md](../rule-census-01/RESULTS.md),
ledger entry E-0432). Luis chose four of them from that table: the conflict
rule with `assertion_modality` added to the qualifier list, interval sanity,
numbers in the cited text over the numeric slots, and formulas in the cited
text over the formula slots. The unit rule is dropped. This cell installs those
four as an adopter `PolicyProgram` selected at admission on run-23's path, runs
the honest population through it, and then reruns `fault-injection-01`'s frozen
catalogue of 55 faults with the rules on.

Every definition in this file was written before any rule ran, and none was
changed after a count. Two things were corrected afterwards and are marked as
such: the Run section's commands, to the exact invocations that were used, and
the sentence below about which Core gate 2's subprocesses import.

The policy is an `ADOPTER_CHOICE`: an optional profile, a research-local
reference implementation and a set of conformance fixtures. Nothing under
`src/malleus` was read into this directory or changed.

## Coordinates

| | |
| :-- | :-- |
| Core | the working checkout at `d867c3ab`, whose `src/malleus` is byte-identical to `e7937b89` (ledger E-0437) |
| fact contract | version 3, which carries `m_derivation/4` and `m_source_text/3`; asserted at collection |
| base population | run-23's admitted capture and records, read only, from `private/paper-v4-v4-run-23/producer` |
| compiled ontology | run-23's own closure, root `paper-v4-project`, `sha256:67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd`, pinned in `logic.yaml` |
| history profile | `SOURCE_ASSERTION_PROFILE`, run-23's own |
| engine | SWI-Prolog, executed by Core's `PrologVerifier` in one fresh process per check |
| private outputs | `private/paper-v4-content-rules-doc-02/`, `git check-ignore -v` confirmed before the first write |

The suite asserts before any measurement that the imported `malleus` is the
pinned Core by a digest over the modules `git archive <pin> -- src/malleus`
carries, and that `malleus.logic.FACT_CONTRACT_VERSION` is `3`. On 2026-09-19
that pin moved from `e7937b89`, 52 modules
`sha256:d57f3cc9b8af9dcd1245e92e956f23b7d63351d4a9bbce2100909ab5949b1355`, to
`d89a0c4718654249ad678eaff62e7b1daba30b6f`, 53 modules
`sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04`,
the sealed Core carrying the one-call atomic admission
`malleus.compiler.check_and_admit_population_plan`; the one module added was
`_contract_pipeline/admission.py`. On 2026-09-21 it moved again, to
`5641bbf1f64b68b2d4e71b9d67726c5beb078f6e`, 54 modules
`sha256:487b426a4d6ed2cc5742ba262c8a1eb8f991469cb017765c3d9eb238ee4703a1`,
the sealed Core that closes the two-step admission door and folds the
structural admission check into a v1 `CORE_BUILTIN` check contract; the module
added is `_contract_pipeline/check_contract.py`. E-0436 is the rule that moves
it. Re-run on each new pin the cell is 56 passed, with every measurement in
`outcomes.json`, `fault-outcomes.json` and `RESULTS.md` unchanged, and the
fact contract still version 3. The four adopted rules were measured on
`d867c3ab`, which `RESULTS.md` names, and that coordinate does not move.
The gate runs this cell in its `5641bbf1` pinned group, against that export;
gate 1 and the cell's own command import the checkout's `src`, whose tracked
bytes are the same tree. Gate 2 goes through
`fault-injection-01/run_faults.py`, which exports `src/malleus` at the commit
it is given with `git archive` and puts it first on `PYTHONPATH` for every
trial; it is given `d867c3ab`, and the working tree carries no modification
under `src/`, so both paths import the same bytes.

## Prolog is the only admissible check implementation, and why

Asked first, before anything was written. Core's check contract admits a
pinned Prolog rule program and nothing else:

- `LogicContract.load` closes the contract's fields against
  `logic.CONTRACT_FIELDS` and refuses any key outside them. The only
  implementation the contract can name is `rules_file`, whose bytes are hashed
  into `ruleset_hash` and from there into `contract_hash`.
- `PrologVerifier._execute` concatenates `fact_declarations(version)`, the
  compiled facts, its own JSON runner and `contract.rules_source` into one
  program and runs `swipl` on it. It is the only verifier Core ships.
- `LogicCheckResult` is a plain dataclass. Its `engine_name` and
  `engine_version` are set by the verifier that produced it; nothing in the
  contract, the policy or the protocol machine identifies a check
  implementation. `structural-history-machine.json` records a check as
  `check_contract_id`, `check_contract_identity`, `outcome`, `policy_identity`,
  `proposal_id` and `receipt_id`, and no more.

So a Python check would be an outcome the caller authored, with no identity the
contract could pin. `content-rules-doc-01/README.md` states the same boundary
of its own runner ("It never accepts a caller-supplied outcome") and the architectural
law's `EXECUTOR_ONLY` forbids the escape hatch. The normalisation and the
number grammar are therefore implemented in Prolog, in `rules.pl`, and their
equivalence to `rule-census-01/normalise.py` is proved on a shared fixture
table before the rules are trusted (see "Equivalence" below).

## Where the declarations live, and why not in `logic.yaml`

Luis ruled that the formula slots are an explicit adopter declaration in the
policy's `logic.yaml`, with a comment pointing at `ROADMAP.md` items E2 and E3.
Core refuses that file: `LogicContract.load` calls `_exact_fields` against
`CONTRACT_FIELDS`, so a `formula_slots:` key makes the contract unloadable and
the whole policy unusable. A YAML comment is not a field and no rule can read
one.

The declarations are therefore in `rules.pl`, which is the one place the
contract pins by digest (`ruleset_hash` into `contract_hash` into
`policy.json`), with the `ROADMAP.md` pointer written at the declaration block;
`logic.yaml` carries a comment saying so. This is a mechanical deviation from
the ruling, not a preference, and it is reported as one.

## Derived from the compiled ontology, and declared by the adopter

Luis: "needs to be from ontology upwards always". What the compiled contract
can supply, it supplies, and `test_content_rules_doc_02.py` asserts each of
these against the contract rather than against a list written by hand:

| declaration | how it is derived | value on run-23's contract |
| :-- | :-- | :-- |
| `numeric_slot/1` | every slot the compiled contract declares with range `Float` or `Integer`, on any declared type | 9 slots: `assertion_confidence`, `count`, `publication_year`, `ratio_value`, `strength`, `uncertainty`, `value`, `value_lower`, `value_upper` |
| `subject_slot/1` | every slot declared with range `Entity` on a type that is not a `Relation` subtype | 1 slot: `subject`. `source_id` and `target_id` are also `Entity`-ranged and are excluded because they are relation endpoints, emitted as `m_relation/4` and never as property facts |

The census read five numeric slots by name. Reading the declared range instead
adds `assertion_confidence`, `publication_year`, `strength` and `value`; the
census measured that the wider set gives identical rows on run-23, because the
first three are set on no citing record and the fourth on none at all
(E-0432). A test asserts that here too rather than assuming it.

What the compiled ontology cannot supply, and what is therefore declared in
`rules.pl` beside the derived facts, each validated against the contract by a
test that refuses a slot the contract does not declare or declares with the
wrong range class:

| declaration | why the ontology cannot supply it |
| :-- | :-- |
| `formula_slot/1`: `analyte`, `numerator_kind`, `denominator_kind` | All three are declared `String`, exactly like `name`, `description`, `quantity_kind` and `count_scope`. The contract carries no marker separating a value copied from the source from one the producer authored. This is the per-slot source relation E-0430 recorded as a Core requirement; `ROADMAP.md` items E2 and E3 carry it. |
| `qualifier/1`, twelve slots | Same gap, from the other side: `unit` and `analyte` are `String`, `determination`, `value_qualification`, `depth_reference`, `melt_stage`, `temporal_precision` and `assertion_modality` are enums, `begins_at` and `ends_at` are `DateTime`, `estimation_proxy` and `temporal_reference_system` are `String`. Nothing in the contract says which of them qualify a quantity. |
| `quantity_identity/2` and `quantity_value/2` | The compiled contract flattens inheritance: `effective_slots` on `Ratio` returns `name`, `description` and `tags` alongside `numerator_kind` and `ratio_value`, and the slot-use facts carry `onClass` for inherited slots too, so "the slots this type declares itself" is not recoverable. A range-only derivation would put `name` and `description` in the quantity identity. |
| `bound_pair/2` and `non_negative_slot/1` | The contract declares `value_lower` and `value_upper` as `Float`. It does not declare that one is a lower bound of the other, or that a count cannot be negative. |

## The four rules

### (a) `NO_CONFLICTING_QUANTITY`

Two current records that state a different value for the same quantity of the
same subject refuse the candidate. The census's candidate (a) with
`assertion_modality` added to the qualifier list, which is the reading Luis
adopted.

- **Same subject**: both records set the same value for a `subject_slot`
  (derived: range `Entity`, non-relation type).
- **Same quantity kind**: both set, and set equal, every `quantity_identity`
  slot of one family. Three families are declared: `QUANTITY`
  (`quantity_kind`), `COUNT` (`count_scope`), `RATIO` (`numerator_kind` and
  `denominator_kind` together).
- **Different value**: the tuple of `quantity_value` slots differs, an absent
  slot differing from any number. `QUANTITY` is the pair
  (`value_lower`, `value_upper`); `COUNT` is `count`; `RATIO` is `ratio_value`.
- **Qualifiers that must agree**, or the two records are not reporting the same
  quantity: `unit`, `determination`, `value_qualification`, `depth_reference`,
  `melt_stage`, `analyte`, `estimation_proxy`, `begins_at`, `ends_at`,
  `temporal_precision`, `temporal_reference_system`, **`assertion_modality`**.
  Agreement means neither record sets the slot, or both set it equal.
- **Scope**: current records, with this change's retirements already removed.
  Run-23 carries zero supersessions.

`uncertainty` is declared `Float` on `Quantified` and on `Ratio` and is in
neither the identity, the qualifiers nor the value, which is the shipped
definition `content-rules-doc-01` fixed and the census measured. Moving it into
the value tuple is a definition change and is not made here.

### (b) `INTERVAL_SANITY`

Typed, internal to one record, no text read. Each clause fires only where its
slots are set.

- `value_lower <= value_upper` when both are set (`bound_pair`).
- `count >= 0`, `ratio_value >= 0`, `uncertainty >= 0` (`non_negative_slot`).

Every slot named is asserted to be a declared `numeric_slot`.

### (c) `NUMBER_IN_CITED_TEXT`

For a record that carries a non-empty `assertion_locator`, every property whose
slot is a declared `numeric_slot` and whose fact kind is `integer` or `float`
must carry a value numerically equal to one of the numbers the declared grammar
reads out of the retained text at that locator.

The locator is the record's, not the property's, the way
`content-rules-doc-01`'s rule 1 defined it. The census measured that widening
the scope to every sentence the record derives from changes no count on run-23.

Comparison is numeric and exact, never by spelling: a float slot value is
converted through its shortest round-trip printing into an exact decimal, so
`991.0` equals `991` and `1.50` equals `1.5`. No tolerance.

### (e) `FORMULA_IN_SOURCE`

For a record that carries a non-empty `assertion_locator`, every property whose
slot is a declared `formula_slot` must carry a value that, after the declared
normalisation of both sides, occurs as a substring of the retained text at that
locator. A value that normalises to the empty string is contained in every text
and never refuses.

### What the rules do not read

`name`, `description`, `claim_kind`, `count_scope`, `quantity_kind`,
`estimation_proxy`, `unit` and every enum are read by no rule, except where a
slot appears in the conflict rule's key. That is most of what a producer
writes. The gap is the one E-0430 recorded and it is unchanged.

## The declared normalisation

`rule-census-01`'s, the `GLUED` profile, declared once in `rules.pl` and
applied identically to every string this cell compares, to a sentence and to a
slot value alike. In order:

1. **Ligatures.** Each of U+FB00 to U+FB06 becomes its letters.
2. **Hyphen-space breaks inside a word.** A letter, then `-`, then one or more
   whitespace characters, then a letter, loses the hyphen and the whitespace.
3. **Spaced digit sequences.** One whitespace character on either side of a `.`
   or a `,` between two digits is removed, and one whitespace character
   directly between two digits is removed. Both to a fixed point.
4. **Letter-to-digit gluing.** One whitespace character between a letter and
   the digit after it is removed, so `CO 2` matches `CO2`. It never runs the
   other way: `H 2 O` becomes `H2 O`.
5. **Whitespace.** Every run of space, tab, newline, carriage return, vertical
   tab, form feed and no-break space becomes one space; the ends are stripped.
6. **Case.** Folded.

Nothing else: no punctuation stripping, no Unicode normalisation, no unit
folding, no accent folding, no stemming, no number reformatting.

Gluing is the step the census measured both ways. It is what makes a formula
match its sentence, and it also welds an honest number onto the word before it,
which is why the number reading below is `ATTACHED`.

## The declared number grammar

`rule-census-01`'s, the `ATTACHED` reading, plus one production Luis added.
Over a normalised string:

- A token is a run of digits with an optional single `.` and one group of
  digits after it. Thousands separators are not read: `1,234` yields `1` and
  `234`. An exponent is not read: `1e5` yields `1` and `5`.
- **`ATTACHED`**: every digit run is a number wherever it sits, so `RC3` yields
  `3` and `co2` yields `2`. The known permissiveness is stated rather than
  hidden: under this reading the digits of a segment name or a figure number
  are read as numbers, so a wrong value that happens to equal one of them
  passes.
- **Sign.** A `-` or U+2212 immediately before a digit is a sign only when the
  character before it is neither a digit nor a `.`. An en dash or em dash is
  never a sign, so `1.5–2.0` yields `1.5` and `2.0`.
- **Number words.** `zero` to `twenty` and the tens, each bounded on both sides
  by a character that is not an ASCII lowercase letter, on the folded text, so
  `tendency` yields nothing and `twenty-five` yields `20` and `5` rather
  than `25`.
- **Plus-or-minus.** `a ± b` yields `a`, `b`, `a-b` and `a+b`.
- **A bare plus-or-minus.** `± b` with no left operand yields the interval from
  minus `b` to plus `b`, so `-b` and `b`. Luis, from the census's second rule
  defect: "teach grammar please, indeed". This production is the one difference
  from `rule-census-01/normalise.py`, it is declared here before the run, and
  the fixture table below marks every row where it makes the two differ.

## Equivalence with `rule-census-01/normalise.py`

The normalisation and the grammar now exist twice, in Python for the census and
in Prolog for the rule. `equivalence.py` runs one shared fixture table through
both and compares: the normalised string must be equal, and the set of numbers
read must be equal, except on the rows carrying a bare plus-or-minus, where the
Prolog is expected to produce exactly the extra negative end and the table says
which. The table is every string that appears in
`rule-census-01/test_normalise.py`, plus the bare plus-or-minus cases.

Numbers are compared as exact rationals on both sides, so no float printing
enters the comparison.

If the two disagree on any other row, this cell stops and reports. Neither
implementation is tuned to the other.

The same comparison is also run over every retained sentence and every string
slot value of run-23's population, in the private directory, and the count is
reported. That corpus check is evidence, not a fixture: a disagreement there is
reported the same way.

## The three rule defects the census found, and what each rule does about them

The census classified every refusal on both honest populations as a rule
defect, with three distinct ones (E-0432).

| defect | record | what this cell does |
| :-- | :-- | :-- |
| The conflict pair: one record `STATED`, the other `HYPOTHESISED`, compared as two live values for one quantity | `obs:bdb-isotherm`, `obs:h1-isotherms` | `assertion_modality` is in the qualifier list, so the two are not compared. The census measured this at zero violations. |
| The bare plus-or-minus: a symmetric perturbation stored as a negative lower and a positive upper bound, where the sentence writes `± b` with no left operand | `obs:velocity-perturbation` | The grammar reads a bare plus-or-minus as the interval from minus `b` to plus `b`, so the negative end is reachable. |
| The character-spaced caption: a two-letter unit whose cited figure caption is set one character at a time in the text layer | `obs:profile-halfwidth` | The unit rule is dropped, so no rule reads that slot. Nothing in the normalisation was widened; joining letters inside a word would join unrelated words throughout the reading. |

## Acceptance

From "Choose an adopter rule" in
[`.claude/skills/malleus-dev/SKILL.md`](../../../.claude/skills/malleus-dev/SKILL.md),
`EVERY_REFUSAL_EXPLAINED`: **every refusal on the honest population is
classified as a rule defect or a graph defect, and rule defects are zero.** Zero
refusals is required only on dimensions the review protocol already verified,
which citation faithfulness is not. A rule that finds a graph defect in an
honest population is a result, not a failure.

The census predicts zero refusals here under all four adopted definitions. That
is a prediction, not an assumption: gate 1 measures it, and any refusal is
classified one line at a time before gate 2 runs.

## The two gates

**Gate 1, the honest population.** Run-23's own capture and records are
admitted under the policy in a fresh history whose selected policy is this
directory's. Separately, run-23's own `run.py` runs unmodified on this Core as
a control, so a refusal by Core's structural gate is never read as a refusal by
the rules. The honest admission's exported records must be byte-identical to
run-23's frozen export; the control's replay receipt is expected to differ from
run-23's frozen receipt only at the two producer-digest leaves
(`/evidence/producer/sha256` and `/evidence_sha256`), and the policied run's
receipt differs by more by construction, because its normative profile carries
the policy. Both differences are reported by path.

**Gate 2, the 55 faults with the rules on.** `fault-injection-01`'s frozen
catalogue, same seed, same population bytes trial for trial, through the same
admission with the policy selected, against
`fault-injection-02`'s 45 refused and 10 admitted on the structural gate alone.
`run_faults.py` gains one additive argument, `--runner`, defaulting to
run-23's own runner, so the first cell's coordinate and its thirty tests are
untouched and a default-coordinate regression reproduces its `outcomes.json`.

Gate 2 runs only if gate 1's rule defects are zero.

## Run

    # gate 1: the control and the honest population under the policy
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/content-rules-doc-02/gate1.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-content-rules-doc-02

    # the equivalence of the two implementations
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/content-rules-doc-02/equivalence.py \
      --private private/paper-v4-content-rules-doc-02

    # gate 2: the 55 faults with the rules on
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/fault-injection-01/run_faults.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-content-rules-doc-02/faults \
      --core-commit d867c3ab \
      --runner paper-v4/experiment-v4/content-rules-doc-02/admit.py \
      --outcomes paper-v4/experiment-v4/content-rules-doc-02/fault-outcomes.json

    # the side by side and the public rows
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/content-rules-doc-02/gate2.py \
      --private private/paper-v4-content-rules-doc-02

    # the default coordinate, unchanged: run-23's own runner on the frozen pin
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/fault-injection-01/run_faults.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-content-rules-doc-02/regression \
      --outcomes private/paper-v4-content-rules-doc-02/regression-outcomes.json

    # the contract
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
      paper-v4/experiment-v4/content-rules-doc-02/test_content_rules_doc_02.py

## Leak rule

No public file in this directory shares a 60-character normalised run with the
selected reading. `test_content_rules_doc_02.py` applies
`fault-injection-01`'s own check over every public file here, `RESULTS.md`,
`outcomes.json` and `fault-outcomes.json` included. Public rows carry record
ids, slots, rules, mechanisms and classes; no value and no sentence.

## What this is not

- Not a Core change and not a request for one. Fact contract version 3 already
  carries what the rules need.
- Not a claim about the paper's other six model-produced populations. Only
  run-23 was rebuilt under this policy.
- Not a general conflict detector. Rule (a) knows the three quantity families
  this ontology declares and nothing else.
- Not a verdict on run-23's faithfulness. The rules read nine numeric slots and
  three formula slots and never read what a producer authors.
- Not a proof that an engine ran at replay. Reopening reads the retained
  history and does not rerun Prolog; it preserves an execution attestation.
- Not registered under the paper gate. `paper-v4/active-test-manifest.json` and
  `answer-demonstration/test_gate_integration.py` are being edited by another
  session, so nothing was added to either. Registration of this cell, with
  `private/paper-v4-content-rules-doc-02` pinned, is owed.

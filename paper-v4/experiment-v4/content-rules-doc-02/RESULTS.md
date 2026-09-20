# Four adopted rules: what they refuse on the honest population, and on 55 faults

**Gate 1 is zero.** Run-23's own honest population is admitted under the
policy, `SATISFIED`, no violation, no refusal to classify, rule defects zero.
Its exported records are byte-identical to run-23's frozen export.

**Gate 2 moves eight trials.** The same 55 faults, the same population bytes
trial for trial, through the same admission with the four rules selected: the
structural gate alone refuses 45 and admits 10; the structural gate plus the
four rules refuses 53 and admits 2. Both open gaps `fault-injection-02` left
are narrowed and one of them is closed: every
`LOCATOR_REPOINTED_COHERENT_DERIVATION` trial is now refused, five for five,
and three of the five `VALUE_NOT_IN_BLOCK` trials are refused. The two that
remain admitted both replace `quantity_kind`, a slot no adopted rule reads.

## Coordinates

| | |
| :-- | :-- |
| Core | the working checkout at `d867c3ab`, `src/malleus` byte-identical to `e7937b89` |
| fact contract | version 3, asserted at collection |
| base population | run-23's admitted capture and records, read only |
| compiled ontology | `sha256:67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd`, run-23's own |
| check contract | `sha256:5eb30d131ed4f90105249077490e09e8fb947ede80655453cb6836e25dc26c65` |
| policy | `sha256:02d65e48e5e7e62b373c52d95dc11913ef660ee881b41c1322600e6f09bae002` |
| engine | SWI-Prolog 10.0.2, one fresh process per check, 6,405 facts |
| provenance supplied | 2,720 derivations, 333 retained sentences |
| private outputs | `private/paper-v4-content-rules-doc-02/` |

## RED before GREEN

| suite | RED | GREEN |
| :-- | :-- | --: |
| 52 tests, against a stub declaring the four rules and implementing none | 29 failed, 21 passed, 2 errors | |
| the same 52, after `rules.pl`, before either gate ran | 13 failed, 39 passed | |
| the same 52, after both gates | | 52 passed |
| 56, after four tests were added | | **56 passed** |

The stub declared `malleus_violation/3` dynamic with no clause, so every
refusal test failed on the behaviour rather than on a missing predicate, and
every admission test passed for the wrong reason, which is what a stub is for.
The second row is the same suite once the rules existed: the thirteen that
remained are the two gates, the leak rule and the note, none of which had run.
The four added afterwards are stated as added rather than folded in: one over
the corpus equivalence counts, and three guarding the first cell's default
coordinate, which only existed once `--runner` did.

`ruff check` and `ruff format --check` are clean on the cell's five Python
files and on `fault-injection-01/run_faults.py`.

## Prolog is the only admissible check implementation

Asked before anything was written, because the answer decides where the
normalisation lives. Core's check contract admits a pinned Prolog program and
nothing else: `LogicContract.load` closes the contract's fields against
`logic.CONTRACT_FIELDS`, its only implementation field is `rules_file`,
`PrologVerifier` is the one verifier Core ships, and `LogicCheckResult` carries
an `engine_name` the verifier sets rather than an implementation identity the
contract pins. The protocol machine records a check as `check_contract_id`,
`check_contract_identity`, `outcome`, `policy_identity`, `proposal_id` and
`receipt_id`, and no more. A Python check would be an outcome the caller
authored.

So the declared normalisation and the number grammar are implemented in
`rules.pl`, and their equivalence to `rule-census-01/normalise.py` is measured
rather than asserted.

## The two implementations agree

| table | strings | disagreeing | declared differences |
| :-- | --: | --: | --: |
| the shared fixture table | 81 | 0 | 5 |
| run-23's own sentences and string slot values | 2,637 | 3 | 3 |

The fixture table is every string `rule-census-01/test_normalise.py` hands to
its own normaliser, which a test extracts from that file's syntax tree rather
than copying, plus seven bare plus-or-minus cases. Each string goes through
`normalise.normalise(text, GLUED)` and `normalise.numbers_in(text, GLUED,
attached=True)` on one side and through the pinned rule bytes on the other,
loaded the way `PrologVerifier` loads them. Numbers are compared as exact
rationals, so no float printing enters the comparison.

Five fixture rows are declared before the run to differ, and by exactly what:
the bare plus-or-minus production yields the negative end the census's grammar
cannot reach. Every one of those five differs by exactly the declared extra
number and by nothing else. The other 76 agree exactly, normalised string and
number set alike.

On the corpus the normalised string agrees on all 2,637 strings. Three
sentences differ in their number set; all three carry a plus-or-minus with no
digit before it, every number only the Prolog reads is the negation of one the
Python reads, and no number is read by the Python alone. That is the declared
production and nothing else. Zero rows differ any other way.

## What is derived from the ontology and what is declared

`numeric_slot/1` and `subject_slot/1` are read off run-23's compiled contract
and a test recomputes both from that contract:

- **Nine numeric slots**, every slot declared with a `Float` or `Integer`
  range: `assertion_confidence`, `count`, `publication_year`, `ratio_value`,
  `strength`, `uncertainty`, `value`, `value_lower`, `value_upper`. The census
  read five by name; the four the declared range adds are set on no citing
  record, so the two sets give the same rows, as the census also measured.
- **One subject slot**, `subject`, the only `Entity`-ranged slot on a type that
  is not a `Relation` subtype. `source_id` and `target_id` are `Entity`-ranged
  too and are excluded because relation endpoints are `m_relation/4` facts and
  never property facts.

The formula slots, the twelve qualifiers, the three quantity families and the
interval slots are adopter declarations, in `rules.pl` beside the derived
facts, each held by a test to the range the contract declares for it. They are
declarations rather than derivations because the compiled contract declares
`analyte`, `numerator_kind`, `denominator_kind`, `quantity_kind`,
`count_scope`, `name` and `description` all as `String` and says nothing about
which of them a producer copies from the source and which it authors. That is
the per-slot source relation E-0430 recorded as a Core requirement and
`ROADMAP.md` carries as items E2 and E3.

**The declaration could not go where Luis asked.** `LogicContract.load` calls
`_exact_fields` against a closed field set, so a `formula_slots:` key in
`logic.yaml` makes the contract unloadable and the policy unusable, and a YAML
comment is not a field a rule can read. The declarations are in `rules.pl`,
which `logic.yaml` pins by digest and `policy.json` pins in turn; `logic.yaml`
carries the comment and the `ROADMAP.md` pointer. This is a mechanical
refusal by Core, not a preference.

The compiled contract also flattens inheritance: `effective_slots` on `Ratio`
returns `name`, `description` and `tags` beside `numerator_kind` and
`ratio_value`, and the slot-use facts carry `onClass` for inherited slots too,
so "the slots this type declares itself" is not recoverable and a range-only
derivation of the quantity identity would put `name` in it.

## Gate 1, the honest population

| | |
| :-- | :-- |
| outcome | ADMITTED |
| check outcome | SATISFIED |
| rules checked | all four |
| violations | 0 |
| refusals to classify | 0 |
| rule defects | **0** |
| graph defects | 0 |
| records | 440, of which 236 cite an assertion |
| exported records | `sha256:0634e069…a286`, byte-identical to run-23's frozen export |
| ledger | 16 events against the control's 14 |

### The census predicted this, and is reproduced

| candidate | census on run-23 | here |
| :-- | --: | --: |
| (a) `NO_CONFLICTING_QUANTITY` with `assertion_modality` | 0 | 0 |
| (b) `INTERVAL_SANITY` | 0 | 0 |
| (c) `NUMBER_IN_CITED_TEXT`, `GLUED`+`ATTACHED` | 1 | **0** |
| (e) `FORMULA_IN_SOURCE`, `GLUED` | 0 | 0 |

The one row that moved is the census's second rule defect,
`obs:velocity-perturbation`: a symmetric perturbation carried as a negative
lower bound and a positive upper bound, cited to a sentence that writes it once
as a plus-or-minus with no left operand. The added production reads that as the
interval from minus to plus, so the lower bound is reachable and the refusal is
gone. Nothing else changed, and the change is the one Luis ruled, declared in
`README.md` before the run and shown in the fixture table and in a synthetic
test rather than inferred from the count moving.

The census's first rule defect, the conflict pair `obs:bdb-isotherm` and
`obs:h1-isotherms`, is removed by `assertion_modality` in the qualifier list; a
synthetic test shows the pair refusing when the two modalities are equal and
admitting when they differ. Its third, `obs:profile-halfwidth`'s
character-spaced unit, is out of reach because the unit rule is dropped and no
adopted rule reads that slot.

### What the receipts say

The control is run-23's own runner, unmodified, on this Core: admitted, 417
entities, 1 event, 22 relations, replay receipt
`sha256:f3a014b1…1f75`, which is the receipt `fault-injection-02`'s control
returned on `e7937b89`. Against run-23's frozen `sha256:a3abceec…1eec` the
validated contract differs at exactly two leaves,
`/evidence/producer/sha256` and `/evidence_sha256`, which is the producer
digest and nothing else.

The policied run's receipt is `sha256:0c88365b…4abe` and differs from the
control's by construction. Where: its validated contract is byte-identical to
the control's, zero differing leaves, and its partial effective contract
differs at exactly five, all under `/normative_profile` — the policy
identifier, the required check contract's id and identity, the policy program
identity and the normative profile identity. The domain contract did not move;
the policy the history selects did. The same difference is visible in the
bootstrap: the control retains `malleus:structural-admission-check/v1` and the
policied history retains `logic.yaml` and `rules.pl` instead.

## Gate 2, the 55 faults with the rules on

Same catalogue, same seed, same population bytes: every trial's
`population_sha256` equals `fault-injection-02`'s, which equals
`fault-injection-01`'s. The runner is this cell's `admit.py`;
`fault-injection-01/run_faults.py` gained one argument, `--runner`, defaulting
to run-23's own runner.

| # | class | n | structural gate alone | structural gate plus the four rules |
| :-- | :-- | --: | :-- | :-- |
| 1 | `VALUE_NOT_IN_BLOCK` | 5 | ADMITTED_INVISIBLE | ADMITTED_INVISIBLE / REFUSED, `CONTENT_RULE_VIOLATED` |
| 2 | `LOCATOR_REPOINTED_STALE_DIGEST` | 5 | REFUSED, `DIGEST_MISMATCH` | REFUSED, `DIGEST_MISMATCH` |
| 3 | `LOCATOR_REPOINTED_COHERENT_DIGEST` | 5 | REFUSED, `LOCATOR_NOT_DERIVED` | REFUSED, `LOCATOR_NOT_DERIVED` |
| 4 | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | 5 | ADMITTED_INVISIBLE | REFUSED, `CONTENT_RULE_VIOLATED` |
| 5 | `DIGEST_MISMATCH` | 5 | REFUSED, `DIGEST_MISMATCH` | REFUSED, `DIGEST_MISMATCH` |
| 6 | `DANGLING_ENDPOINT` | 5 | REFUSED, `DANGLING_ENDPOINT` | REFUSED, `DANGLING_ENDPOINT` |
| 7 | `TYPE_OUTSIDE_ONTOLOGY` | 5 | REFUSED, `RECORDS_NOT_REHYDRATABLE` | REFUSED, `RECORDS_NOT_REHYDRATABLE` |
| 8 | `SLOT_OUTSIDE_ONTOLOGY` | 5 | REFUSED, `RECORDS_NOT_REHYDRATABLE` | REFUSED, `RECORDS_NOT_REHYDRATABLE` |
| 9 | `DUPLICATE_RECORD_ID` | 5 | REFUSED, `MALFORMED_CAPTURE` | REFUSED, `MALFORMED_CAPTURE` |
| 10 | `RECORD_WITH_NO_SOURCE_WITH_FIELDS` | 5 | REFUSED, `UNDERIVED_FIELD` | REFUSED, `UNDERIVED_FIELD` |
| 11 | `RECORD_WITH_NO_SOURCE_NO_FIELDS` | 5 | REFUSED, `UNDERIVED_RECORD` | REFUSED, `UNDERIVED_RECORD` |

**45 refused and 10 admitted becomes 53 refused and 2 admitted.** Eight trials
moved, all in one direction: `admitted_to_refused` 8, `refused_to_admitted` 0,
and no trial changed in any other way. The eight are `a-01`, `a-02`, `a-05`, `b4-01`, `b4-02`, `b4-03`, `b4-04`, `b4-05`.

### Which rule refused what

| trial | class | rule | violation code | witness |
| :-- | :-- | :-- | :-- | :-- |
| `a-01` | `VALUE_NOT_IN_BLOCK` | `FORMULA_IN_SOURCE` | `FORMULA_NOT_IN_CITED_TEXT/analyte` | `gchem:eq-atlantic-co2-avg` |
| `a-02` | `VALUE_NOT_IN_BLOCK` | `FORMULA_IN_SOURCE` | `FORMULA_NOT_IN_CITED_TEXT/analyte` | `gchem:rc2-co2-rb` |
| `a-05` | `VALUE_NOT_IN_BLOCK` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/ratio_value` | `ratio:vp-vs` |
| `b4-01` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/count` | `cnt:subsections` |
| `b4-01` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_lower` | `cnt:subsections` |
| `b4-01` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_upper` | `cnt:subsections` |
| `b4-02` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_lower` | `obs:co2-saturation-temperature` |
| `b4-02` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_upper` | `obs:co2-saturation-temperature` |
| `b4-03` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_lower` | `obs:model1-vp` |
| `b4-04` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/value_upper` | `obs:relocation-rms` |
| `b4-05` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `FORMULA_IN_SOURCE` | `FORMULA_NOT_IN_CITED_TEXT/denominator_kind` | `ratio:co2-ba` |
| `b4-05` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `FORMULA_IN_SOURCE` | `FORMULA_NOT_IN_CITED_TEXT/numerator_kind` | `ratio:co2-ba` |
| `b4-05` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/ratio_value` | `ratio:co2-ba` |
| `b4-05` | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | `NUMBER_IN_CITED_TEXT` | `NUMBER_NOT_IN_CITED_TEXT/uncertainty` | `ratio:co2-ba` |

Ten trials reach the rules at all: the ten the structural gate admits. The
other 45 are refused before any Prolog runs, by the same mechanism and with the
same typed diagnostic as on the structural gate alone.

### What remains admitted

Two, `a-03` and `a-04`. Both replace `quantity_kind` with a synthetic string on
a record whose locator, digest and derivations are untouched. No adopted rule
reads `quantity_kind` against the source: the conflict rule uses it as an
identity key and nothing compares it with a sentence. Both come back
`SATISFIED`, with the injected value in the exported graph and both
post-admission checks clean, which is the honest statement of what this rule
layer does not cover.

The rule that would reach them is one over the producer-authored string slots,
and that is the family the census measured refusing 216 of 236 honest records
(E-0430). It becomes available when the ontology can say which slots a producer
copies and which it authors, which is the per-slot source relation, `ROADMAP.md`
items E2 and E3. Dropping the unit rule does not bear on these two: the fault is
in `quantity_kind`, not in `unit`.

**The expectation this tested, and did not confirm.** Rule (c) was expected to
be what the five `VALUE_NOT_IN_BLOCK` trials exist to catch. It catches one of
them, `a-05`, a `ratio_value` replaced with a synthetic float. Two more,
`a-01` and `a-02`, are caught by rule (e) because the catalogue replaced an
`analyte`. The remaining two are `quantity_kind` and no rule reaches them. The
class the rules cover completely is the other one:
`LOCATOR_REPOINTED_COHERENT_DERIVATION`, which `fault-injection-02` recorded as
invisible to everything on the admission path, is refused five for five,
because moving a record's whole citation to another sentence leaves its numbers
and its formulas in a sentence that does not state them.

### Every refusal left the history without an admission event

All 53 refusals wrote a ledger with none of the four admission events
(`KNOWLEDGE_CHANGE_SET_RETAINED`, `CHANGE_PROPOSED`, `CHECK_RECORDED`,
`VERDICT_RECORDED`). Their shapes differ by where the refusal happened, which
is worth stating rather than smoothing over:

| refusal | ledger | byte prefix of the control's |
| :-- | --: | :-- |
| structural, 45 trials | 8 events, the bootstrap alone | yes, except the five `SLOT_OUTSIDE_ONTOLOGY` trials, which retain different capture bytes |
| by a rule, 8 trials | 11 events: the bootstrap and the three retention events | no: the retained plan carries the fault |

A rule refusal happens after preparation has retained the plan and before any
admission event, so the plan bytes are in the ledger and the change is not. The
policied bootstrap is 8 events against the control's 7: it retains
`logic.yaml` and `rules.pl` as evidence and does not retain
`malleus:structural-admission-check/v1`, which is the check the shipped
structural policy names.

After all 55 trials the honest population was run again through the same
admission and returned the control's receipt,
`sha256:0c88365b…4abe`.

## What was not done

- **Not registered under the paper gate.** `paper-v4/active-test-manifest.json`
  and `answer-demonstration/test_gate_integration.py` are being edited by
  another session, so nothing was added to either. Registration of this cell,
  with `private/paper-v4-content-rules-doc-02` pinned, is owed.
- **Only run-23.** The paper's other six model-produced populations were not
  rebuilt under this policy.
- **The rules read nine numeric slots and three formula slots.** They never
  read `name`, `description`, `claim_kind`, `count_scope`, `quantity_kind`,
  `estimation_proxy` or `unit` against the source, which is most of what a
  producer writes. Gate 2 shows the cost of that directly: the two faults that
  remain admitted replace `quantity_kind`.
- **One consumer.** `rule-census-01` measured these candidates on the Shop as
  well and found that its compiled contract declares none of the slots (a), (b)
  and (e) read and one numeric slot for (c), set on six records. By
  `CENSUS_FIRST` that makes this layer a document-path adapter until a second
  shaped consumer exists. Nothing here changes that.
- **The equivalence harness feeds text as JSON, not as an escaped atom.** The
  rule receives a sentence as the atom `malleus.logic` writes into the fact
  program; the fixture and corpus comparison hands the same string to the same
  rule bytes through a JSON file. That the two paths agree is not proved
  directly; what stands in for it is gate 1, where the rules read all 333
  sentences through the fact path and refused nothing, and gate 2, where they
  read them and refused eight trials.
- **No Core change.** Nothing under `src/malleus` was read into this directory
  or modified.
- **No model call, no tuning.** No rule, declaration, normalisation or grammar
  was changed after a count. The one grammar change is Luis's ruling, made
  before the run and measured both ways.

## The first cell's default coordinate is unchanged

`run_faults.py` gained one argument. Its default is run-23's own runner, so the
first cell's coordinate is exactly what it was, which three things establish:
`fault-injection-01/outcomes.json` still digests to
`sha256:7b7dd161…adb9`, the value its own note states; a test asserts every
parser default, the new one included; and a test feeds run-23's own stderr
through `diagnostic` and gets the same three fields the literal prefix used to
give.

The fourth is the run itself. All 55 trials were rerun at the default
coordinate, run-23's own runner on the frozen pin
`c95dba7b86bb61487bda9a52458e1ea47cce20ab`, and compared leaf by leaf against
`fault-injection-01/outcomes.json`:

| | |
| :-- | --: |
| leaves where both files carry a value and they differ | **0** |
| leaves the frozen file does not carry at all | 46 |
| trials | 55, 35 refused, 15 admitted invisible, 5 admitted exposed |
| control replay receipt equals run-23's frozen receipt | yes |
| honest replay after all 55 trials equals it | yes |

The 46 are keys added since that file was written: `core_repository`,
`core_is_the_frozen_pin`, the control's two comparisons against run-23,
`replay_after_trials.equals_control` and the two per-trial comparisons against
this run's own control, all from the Core-coordinate change at E-0429, plus
`runner` from this one. Every field the frozen record carries is reproduced
exactly, trial for trial, including each ledger digest and each typed
diagnostic. The regression's own outputs stay private; the frozen file was not
rewritten.

## The public record

`outcomes.json` beside this file carries both gates. A gate-1 refusal row would
carry the rule, the violation code, the slot, the witness record identities, a
class (`RULE_DEFECT`, `GRAPH_DEFECT` or `UNDECIDED`) and one line of reason;
there are none, so the list is empty and the acceptance block reads zero,
zero, zero. A gate-2 row carries the trial, the fault class, the rule, the
violation code, the slot and the witness record identities; the violation code
is the mechanism, because a rule names in it what it read and where. No value
and no sentence is in either file, and the leak check covers both.

`fault-outcomes.json` is `run_faults.py`'s own record, written by that script in
its own schema and not edited here.

## Reproducing

The exact commands are in [README.md](README.md) under "Run".

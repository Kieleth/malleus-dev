# Three content rules on the document path

The Shop rule layer
(`research/ontology_driven_kg_realization/experiments/small_shop/content_rules/`)
shipped two adopter rules and deferred the third. The deferred one, "a record's
value must appear in the text it cites", was measured against the Shop's honest
population before anything was built and refused 145 of its 294 retained
derivations, because a Shop derivation says "this cell is why this value is
here" and not "this value is the text of this cell". It was moved here, to the
path where a record transcribes a sentence (E-0406, E-0408).

This directory carries all three rules against the paper's marine-article
population, run-23. The policy is an adopter choice, not a Malleus invariant:
an optional profile, a research-local reference implementation, and a set of
conformance fixtures. None of it is evidence of delivery, and nothing under
`src/malleus` was read into it or changed.

## Coordinates

- Core: the isolated candidate at `e7937b89`, exported with
  `git archive --format=tar <commit> src/malleus` and put first on
  `PYTHONPATH`, the way `fault-injection-01` and run-23's own parent-side
  commands ran it. Fact contract version 3, which carries
  `m_derivation(RecordId, FieldPath, SourceId, Locator)` and
  `m_source_text(SourceId, Locator, Text)`.
- Base population: run-23's admitted capture and records, read only, from
  `private/paper-v4-v4-run-23/producer/work/document-population.json`.
- Compiled ontology: run-23's own closure, root `paper-v4-project`, compiled
  identity `sha256:67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd`,
  pinned in `logic.yaml`.
- History profile: `SOURCE_ASSERTION_PROFILE`, run-23's own.
- Private outputs: `private/paper-v4-content-rules-doc-01/`.
- Engine: SWI-Prolog, executed by Core's `PrologVerifier` in one fresh process
  per check, over the candidate subgraph only.

## What the layer is

`policy.json` is a `PolicyProgram` requiring one check contract by digest and
mapping its outcome to a verdict. `logic.yaml` pins the contract: the compiled
ontology identity, the fact contract version, the rule manifest and the
timeout. `rules.pl` carries the three rules. `run.py` selects the policy in a
fresh history before the first record, retains the rule bytes, stages the
change's exact operations, submits the real Prolog result to the policy, and
admits the receipt and the change atomically. It never accepts a
caller-supplied outcome. The shape follows the Shop layer; this directory adds
no second interpreter.

The outcome grammar is the Shop's and has not moved: `SATISFIED` maps to
`ACCEPT`, `VIOLATED` to `REJECT`, `UNKNOWN` to `DEFER`, and any terminal
verdict that is not `ACCEPT` refuses the whole atomic admission with
`REJECTED_CHANGE`. There is no verdict that admits a change while recording a
violation.

## The definitions, written before the run

Everything in this section was fixed before the honest population was admitted
under the policy. Nothing in it was changed after a result.

### Rule 1, `VALUE_IN_CITED_TEXT`

For every record that carries a non-empty `assertion_locator`, every scalar
property of that record must carry a value that, after normalisation, occurs
as a substring of the retained text at that locator.

**The locator is the record's, not the property's.** A record's
`assertion_locator` names one assertion of the capture. The rule reads
`m_source_text` at that one locator and asks every in-scope property of that
record against it. A property derived from a different assertion of the same
capture is still asked against the record's cited one. That is the rule as
specified; the alternative, asking each property against the locator of its own
derivation, is a different rule and is not implemented here.

**Normalisation, whitespace and case only.** Both the value and the retained
text pass through the same two steps and no others:

1. Case: SWI-Prolog `downcase_atom/2`.
2. Whitespace: every maximal run of the characters space, tab, newline,
   carriage return, vertical tab, form feed and no-break space becomes one
   space, and leading and trailing runs are removed.

No punctuation stripping, no Unicode normalisation, no unit folding, no number
reformatting, no accent folding, no stemming. A number reaches the rule as
Prolog prints it, so a float the producer wrote as `40.0` is compared as
`40.0`.

**Containment is substring containment**, not word containment. A value that
normalises to the empty string is contained in every text and never violates.

**Which property kinds are excluded by construction, and why.** The fact
contract gives a rule the property's name, its value kind and its value; it
gives no slot range, so the exclusions are a list of slot names in `rules.pl`,
each justified here by what run-23's compiled ontology says the slot is. The
list was derived from the compiled contract, not from a result.

| kind | slots | why the rule cannot read them |
| :-- | :-- | :-- |
| record reference | `subject`, `caused_by` | The value names another record. `subject` compiles to range `https://malleus.dev/schema/Entity`; `caused_by` is declared `range: string` and documented as the ID of the event or agent that caused an event. The reference resolves through the graph, not through a sentence, and the record identity is minted by the producer, so containment would run the other way at best. |
| enumeration that is an ontology term | `agent_type`, `assertion_modality`, `contribution_role`, `depth_reference`, `determination`, `event_type`, `hypothesis_disposition`, `melt_stage`, `quantity_kind_class`, `relation_type`, `source_kind`, `temporal_precision`, `value_qualification` | Each compiles to an enum range declared in this contract or an imported pack. The value is a permissible-value name the ontology mints (`MEASURED`, `PRIMARY_MELT`, `Length`), and the source states the concept in its own words. This is the Shop's `event_type` finding on the other path: `Place SO` to `PLACE_SUPPLIER_ORDER` is an abbreviation expansion no character-level normalisation reaches. |
| capture coordinate | `assertion_locator`, `statement_sha256` | Coordinates of this capture, not statements the source makes. `assertion_locator` is the rule's own input and `statement_sha256` is a digest of the sentence, never a phrase inside it. |
| record bookkeeping | `created_at`, `updated_at`, `order_key` | Timestamps and an ordering key the record carries about itself. They are not values the source states. |

Out of the rule's reach by construction rather than by exclusion, recorded so
the reach is not overstated:

- **Multivalued slots.** `tags`, `feature_orientation` and `award_identifier`
  compile to `m_list/3` and `m_list_item/5`, never to `m_property/4`, so the
  rule never sees them. It reads `m_property` only.
- **`id` and `type`.** Neither is emitted as a property fact. A relation's
  `source_id` and `target_id` are emitted as `m_relation/4` and are likewise
  not property facts.
- **Value kinds.** The rule reads the `string`, `integer` and `float` kinds. It
  does not read `boolean` (no slot in this contract has a boolean range, and a
  boolean's spelling is a contract token rather than the source's words) or
  `null` (the absence of a value is not a value).
- **Records with no locator.** 236 of run-23's 440 records carry
  `assertion_locator`; it is declared on `Claim`, `GeophysicalObservation`,
  `GeochemicalObservation`, `CountObservation` and `ElementRatio` through the
  research pack's `SourceAsserted` mixin. The other 204 records are of types
  that do not declare the slot, so the rule reaches none of them.

Everything else a reachable record carries is in scope, `name` and
`description` included.

**Where the rule is silent.** A record citing a locator the caller supplied no
retained text for produces no violation. The engine returns violations, so
there is no way to say "cannot check" from inside a rule; the policy's
`UNKNOWN` outcome is not reachable from the Prolog result. Every locator in
run-23's capture has retained text, so the case does not arise here.

### Rule 2, `NO_CONFLICTING_QUANTITY`

Two current records that state a different value for the same quantity of the
same subject refuse the candidate. Stated in run-23's compiled ontology's own
slots:

- **Same subject** is the `subject` slot of the research pack's `SourceAsserted`
  mixin, range `https://malleus.dev/schema/Entity`. Both records set it and the
  values are equal. A record that does not set `subject` is not compared.
- **Same quantity kind** depends on which quantity-bearing mixin the record
  wears, because this ontology has three and they carry different slots:
  - metrology `Quantified`: the `quantity_kind` slot, `range: string`, the
    source's own wording of the reported quantity. `quantity_kind_class` is a
    coarse enum and is not the identity.
  - metrology `Counted`: the `count_scope` slot, `range: string`, what the
    count includes.
  - metrology `Ratio`: the `numerator_kind` and `denominator_kind` slots, both
    `range: string`, taken together.
- **Different value** likewise:
  - `Quantified`: the closed pair (`value_lower`, `value_upper`), both
    `range: float`. The pairs differ, counting an absent bound as different
    from any number.
  - `Counted`: the `count` slot, `range: integer`.
  - `Ratio`: the `ratio_value` slot, `range: float`.
- **Qualifiers that must agree**, or the two records are not reporting the same
  quantity of the same subject and a different value is not a disagreement:
  `unit`, `determination`, `value_qualification`, `depth_reference`,
  `melt_stage`, `analyte`, `estimation_proxy`, `begins_at`, `ends_at`,
  `temporal_precision`, `temporal_reference_system`. Agreement means either
  neither record sets the slot, or both set it to the same value. This is the
  document path's form of the Shop rule's "the value kind is shared so a
  representation difference is never a conflict".

  `uncertainty` is deliberately **not** a qualifier. It is part of the value
  the record reports, not part of what the value is about, so two records that
  disagree on a number and also on its uncertainty are still disagreeing.

**Scope is current records only.** The check runs over the accepted graph with
this change's retirements already removed, which is the base Core applies the
change to. An explicit correction is not a conflict. Run-23 carries zero
supersessions, so the branch has nothing to remove here and is retained for the
same reason the Shop retains it.

**What the rule cannot catch.** A wrong value that nothing disagrees with, and
a disagreement stated in different units, at a different melt stage, from a
different datum, or under a different determination. Those are two quantities
by this definition, and the definition was fixed before the run.

### Rule 3, `NO_EMPTY_RECORD`

A record carrying no property at all is refused. The rule reads presence, not
adequacy: a record with one meaningless property passes.

Core's plan compiler at `e7937b89` now refuses a record with no derivation
(`UNDERIVED_RECORD`), which closes the half of `fault-injection-01`'s gap 4 a
structural gate can see. The half left to this layer is the other one: a record
that names the source it came from and then says nothing. The rule counts both
`m_property/4` and `m_list/3`, so a record carrying only a multivalued slot is
not called empty.

The rule applies to every record kind, relations included.

## Gate 1, the false-positive gate

The honest run-23 population is admitted under the policy on a copy of its
capture, and every honest record the rules refuse is counted, per rule, with
the record identity, the slot, and the mechanism. No rule and no normalisation
is tuned to reduce that count. The table is in [RESULTS.md](RESULTS.md); the
values and the cited texts stay in the private directory, because they are the
reading.

**Outcome: gate 1 is not zero.** `VALUE_IN_CITED_TEXT` refuses 216 of the 236
records that cite an assertion, `NO_CONFLICTING_QUANTITY` refuses one pair and
`NO_EMPTY_RECORD` refuses nothing. Gate 2 was not reached.

## Run

Both steps read Core from an export of the isolated candidate, put first on
`PYTHONPATH`. The repository's own pytest configuration prepends its working
`src`, so the test command clears it with `-o pythonpath=`; otherwise the tests
run against the checkout's Core and fail to import the version-3 vocabulary.

    CORE=/tmp/core-e7937b89
    mkdir -p "$CORE" && git -C <candidate checkout> archive --format=tar \
      e7937b89 src/malleus | tar -x -C "$CORE"

    # the control, the honest population under the policy, and the probe
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$CORE/src:." .venv/bin/python \
      paper-v4/experiment-v4/content-rules-doc-01/run_policy.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-content-rules-doc-01

    # the contract
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$CORE/src:." .venv/bin/python -m pytest \
      -q -p no:cacheprovider -o pythonpath= --import-mode=importlib \
      paper-v4/experiment-v4/content-rules-doc-01/test_content_rules_doc.py

`policy.json` pins `logic.yaml`'s contract digest, which moves whenever
`rules.pl` moves. `test_the_policy_requires_this_exact_check_contract` fails
when the two drift.

This cell is not in `paper-v4/active-test-manifest.json`. Adding it needs a
Core pin entry for the candidate commit, and that file is being edited by
another session; the entry is owed.

## Leak rule

No public file in this directory shares a 60-character normalised run with the
selected reading. `test_content_rules_doc.py` reuses `fault-injection-01`'s
check over every public file here, `RESULTS.md` and `outcomes.json` included.

## What this is not

- Not a Core change, and not a request for one. Fact contract version 3 already
  carries what the rule needs.
- Not gate 2. Rerunning `fault-injection-01`'s twenty admitted faults through
  this policy is a separate step, gated on gate 1 reading zero.
- Not a claim about the paper's other six model-produced populations. Only
  run-23 was rebuilt here.
- Not a general conflict detector. Rule 2 knows the three quantity-bearing
  mixins this ontology declares and nothing else.
- Not a proof that an engine ran. Reopen reads the retained history and does not
  rerun Prolog; it preserves an execution attestation. Caller-authored machine
  events remain a trusted boundary.

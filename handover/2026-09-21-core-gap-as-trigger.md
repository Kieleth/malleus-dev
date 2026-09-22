# A declared gap is a trigger, not a note

ROADMAP F2, built 2026-09-21 on main `d3833d02` (overseer head `OVR-000476`).

The decision, Luis, 2026-09-21, "go": a producer that meets a record the
ontology cannot type declares a gap of kind `TYPE_ABSENT` or `RELATION_ABSENT`.
Six kinds exist, `malleus.compiler.POPULATION_GAP_KINDS`, and the gaps artifact
has been retained and bound to its plan id since the population pipeline shipped.
Nothing consumed it. From now on a declared ontology gap is an open question on
the ontology with a recorded answer.

## The slice

- **Claim.** `OPTIONAL_PROFILE: semantic-history with compiler-enabled`. The two
  ontology gap kinds become open questions with one recorded decision each, and
  the replay reports what is still open. Under any other profile nothing binds:
  a history with no compiled contract has no revision to compose, and a producer
  that declares no gap sees no change.
- **Smallest observation.** On a history carrying one open gap: `open_gaps()`
  lists it with no proposals; a retained proposal shows as open against it;
  acceptance records the revision, closes the gap, and the graph replays
  byte-identical apart from the new class being available; a second acceptance
  refuses; on a fresh copy refusal closes the gap with its reason and no revision
  exists; a non-additive or non-compiling proposal refuses at retention and
  writes nothing; a proposal against an `AGGREGATE_ONLY` gap refuses. Then, on
  the same history: the retained ontology source reproduces the running
  contract; a proposal carries a fragment and no artifact; Core composes,
  compiles and retains the target; acceptance makes the composed root the
  current source; a second proposal composes on it.
- **Reuse.** `compile_contract_revision` and `CONTRACT_REVISION_POLICY` for the
  additive check, unchanged and with no new change kind;
  `KnowledgeChangeHistory.compose_contract_revision` and
  `record_contract_revision`'s entry for the recorded revision; the public
  `compile_linkml_contract` and `compose_partial_effective_contract` for the
  derivation, with no new compiler; the ordinary anchor retention door, driven
  by the history binding's own declared retention events rather than a
  hard-coded event name; the gaps artifact `prepare_population_change` already
  generates, read and never written.
- **Excluded.** Core drafting a proposal; deriving a class or slot name from a
  gap's statement (architectural law 8); authenticating the deciding actor;
  any change to check-contract re-binding, which stays the declared
  `REBIND_CHECK_CONTRACT` change; any change to the six gap kinds, to the gaps
  artifact's bytes, or to the revision policy's change kinds; recompiling the
  fragment inside the fold, which would put LinkML in replay.

## The identity measurement, taken before building

The contract revision policy is content-addressed over its change kinds. When
`REBIND_CHECK_CONTRACT` was added on 2026-09-17 every frozen Shop evidence
re-pinned (`OVR-000466`, paper ledger E-0464). So the first question was what
this design would move. Read first, then designed around:

- `ContractRevisionPolicy` digests `{"change_kinds": [...], "grammar": ...}`,
  `revision.py:182`. **No change kind is added**, so
  `CONTRACT_REVISION_POLICY.identity` does not move. A test pins the five kinds.
- `ContractRevision.from_bytes` closes its field set, `revision.py:315`. The
  answered gap identities and the deciding actor are therefore **not fields on
  the revision**. They are a separate `malleus.ontology-gap-answer/v1` record
  that names the revision by its identity and is appended in the same ledger
  batch. This is the smaller shape the brief asked for if anything moved; it was
  taken before anything moved, because the decision's wording, "recorded on the
  revision", would have required a new optional field and a second reading of
  every recorded revision.
- The gaps artifact is `{"gaps": [...], "plan_id": ...}`, generated at
  `population.py:1655` and `population.py:1810`. Nothing is added to it, so no
  retained gaps artifact's digest moves. A gap identity is derived from those
  bytes rather than stored in them.
- `KnowledgeHistoryReceipt` is built from the contract, binding, machine state,
  ledger head and count, graph, retained inputs and accepted changes,
  `knowledge.py:_history_receipt`. `gap_answers` is a new replay field with a
  default and does not enter the receipt, so no history receipt moves.
- The new `ONTOLOGY_GAP_ANSWER_RECORDED` fold branch and the proposal check in
  the retention branch fire only on the new event type and on bytes carrying the
  literal `malleus.ontology-revision-proposal/v1`. No existing ledger holds
  either.

The second build was measured the same way before it was written:

- `retain_ontology_source` appends only when called, and nothing calls it, so
  no existing history gains an event. Three tests say exactly that:
  `test_a_new_history_holds_no_ontology_source` (a fresh history has none),
  `test_a_recorded_revision_does_not_retain_a_source_set_by_itself` (recording a
  revision does not create one), and
  `test_the_act_is_explicit_and_moves_nothing_already_written` (after the act
  the ledger's earlier bytes are an unchanged prefix, and the graph records,
  acceptance head, materialization head and contract identity are identical).
- The proposal grammar was reshaped rather than versioned because no consumer
  exists: no retained bytes anywhere carry
  `malleus.ontology-revision-proposal/v1`, so there is nothing to migrate and
  nothing that replays differently. That was the condition Luis attached to the
  reshape.
- The two new fold branches fire only on bytes carrying the literal
  `malleus.ontology-source-set/v1` or `malleus.ontology-revision-target/v1`. No
  existing ledger holds either.
- `KnowledgeHistoryReplay` gained methods, not fields, so `_history_receipt` is
  untouched and no history receipt moves.
- `_retention_anchor` reads the binding's own declared retention events instead
  of adding a role or an event type, so `_HEAD_ROLES` and every shipped binding
  are unchanged.

One thing frozen did move, and it was withdrawn rather than re-pinned. The
second build added three paths to the wheel's `include` list in
`pyproject.toml`, and CC-X02's duplicate scan pins that file's exact bytes as
retained evidence:

| Coordinate | Frozen at `d3833d02` | With the edit |
|---|---|---|
| `pyproject.toml` byte length | 12074 | 12243 |
| `pyproject.toml` sha256 | `037567e39af4eca01f8ff0560625075d053729f8311d5dce3bc9270b0f47a47d` | `6ad46e080a1f3fdd382bc0674af23d17daeb891022acc56557b8f37b181fd88d` |

Four tests read those bytes: three in
`tests/test_contract_compiler_duplicate_scan.py`
(`test_scan_has_exact_packaged_modules_and_source_identities`,
`test_render_is_deterministic_and_matches_retained_bytes`,
`test_cli_checks_without_rewriting_retained_bytes`) and
`test_environment_correction_replaces_only_the_availability_guarantee` in
`tests/test_contract_compiler_divergence.py`. The brief says to stop when frozen
evidence moves and not to re-pin it, so the edit was withdrawn at
`3147ccd3a8a5b45e285ffba27d41d1d3d2113912`.
The file is byte-identical to `d3833d02` again, the four tests pass (29 passed
over both files), and `pyproject.toml` left the entry's document set. What it
costs is under Residuals, and the decision is Luis's.

That commit's own message overstates that cost and is corrected here
rather than rewritten. It says an installed wheel cannot import
`malleus.compiler`. That was read off the `include` list and its comment, not
measured. Four builds afterwards show the wheel is whole, because the wheel
target sets `packages = ["src/malleus"]`, and only the sdist and anything built
from it are missing the three modules. The table under Residuals is the
measurement.

**Nothing else frozen moved, on either build.** The suite counts are under
Measurements, and the `small_shop` and `document_paper` suites, which are where
the frozen digests live, are the check.

## What was built

Three new modules under `src/malleus/_contract_pipeline/`:

| Module | What it holds |
|---|---|
| `gap_answer.py` | Gap identity, the proposal grammar, the answer grammar, the gap index and the answerability check. |
| `linkml_addition.py` | The one additive composition rule, as a pure function over exact bytes. It imports `yaml` and nothing else, not even from Malleus. |
| `ontology_source.py` | The source-set grammar and the derived-target grammar, both identified by their own bytes. |

Plus the fold branches, the four recorded acts and the readers in
`knowledge.py`, and the public names in `compiler.py`. None of the three is
named in `pyproject.toml`'s `include` list; adding them moved frozen evidence,
so the lines were withdrawn. The wheel ships them anyway and the sdist does not,
which is measured in a residual below and is Luis's to rule on.

### Gap identity

`malleus.compiler.ontology_gap_identity(gap=..., plan_id=...)`. Exactly this is
digested, and nothing else: the canonical JSON encoding, UTF-8, sorted keys, no
whitespace, of

```json
{"gap": {"kind": "...", "locator": "...", "source_id": "...", "statement": "..."},
 "plan_id": "..."}
```

prefixed `sha256:`. The gap object is its four declared fields exactly as the
retained gaps artifact holds them; the plan id is the one the gaps artifact
binds. Nothing is derived from a path or a record name. Two consequences, both
intended: the same gap declared in another plan is another gap, and a closed gap
re-declared later with new evidence is a new gap with a new identity, not this
one reopened.

A gaps artifact is recognised by its own bytes and checked against its own
record id: canonical JSON with exactly `gaps` and `plan_id`, retained under
`<plan_id>:gaps`, which is the id `prepare_population_change` derives when it
generates one, with every gap inside carrying exactly the four closed fields.
Anything else is not a gaps artifact.

### The source set grammar

A history holds its validated contract and never the LinkML behind it. That is
enough to admit and to replay, and not enough to compose an addition: composing
needs the root. So the source enters explicitly, under
`malleus.ontology-source-set/v1`, canonical JSON, closed field set, five fields:

| Field | What it is |
|---|---|
| `compiler_execution_identity` | The compiled artifact's `evidence_sha256`: which compilation produced this contract. |
| `grammar` | The literal `malleus.ontology-source-set/v1`. |
| `modules` | Sorted by locator, unique. Each entry is closed to `byte_length`, `locator`, `media_type`, `sha256`. |
| `root_locator` | Must name one of the modules. |
| `validated_contract_identity` | The `validated_fact_set_sha256` this set reproduces. |

The record id is `ontology-source-set:<digest of these bytes>`, so a source set
cannot be retained under a name that is not its own bytes. The module bytes are
retained as ordinary artifacts under `ontology-source:<digest>`, and the fold
refuses `ONTOLOGY_SOURCE_BYTES_NOT_RETAINED` for any digest the set names and the
history does not hold, and `MALFORMED_SOURCE_SET` when a declared byte length
denies its bytes.

A set is **current** while `validated_contract_identity` is the active
contract's. Nothing derives currency from arrival order or from a path. A
recorded revision moves the contract, so the set behind the old one stops being
current and stays as the record of what that contract was compiled from.

### The derived target grammar

`malleus.ontology-revision-target/v1`, canonical JSON, closed field set, six
fields: `composed_root_sha256`, `grammar`, `partial_contract`,
`proposal_identity`, `source_set_identity`, `validated_contract`. Record id is
`ontology-revision-target:<digest of these bytes>`.

This is what Core derived for one proposal. The binding to the proposal is the
proposal's own identity, never a name and never a path. The fold refuses
`ONTOLOGY_SOURCE_BYTES_NOT_RETAINED` if the composed root it names is not
retained, `ONTOLOGY_SOURCE_NOT_RETAINED` if the source set it names is not, and
`REVISION_TARGET_SOURCE_SET_NOT_CURRENT` if that set is not the active
contract's.

### The composition rule

`malleus.compiler.compose_linkml_addition(base_root_bytes, fragment_bytes)` is a
pure function over exact bytes, in `_contract_pipeline/linkml_addition.py`. Both
inputs parse as strict YAML mappings: one document, no anchor, alias, tag,
directive or document marker, no duplicate key, no BOM. The fragment may carry
only `classes`, `enums`, `imports`, `prefixes`, `slots`, and under them it may
only add. Nine closed refusals, listed below.

The output keeps the base's key order, appends in the fragment's order, and is
written by one fixed serialiser. **The measurement that decided the serialiser:**
compiling
`research/.../small_shop/partial_shipments/small-shop-with-shipments.yaml` and
compiling its round trip through `yaml.safe_dump` give the same
`validated_fact_set_sha256` under `sort_keys` both false and true and under both
flow styles. Re-serialising a LinkML root is therefore not a semantic act, and
the form chosen is one the compiler treats identically to the authored file.
Comments do not survive, which costs the retained source its prose and costs the
contract nothing.

### The proposal grammar

`malleus.ontology-revision-proposal/v1`, canonical JSON, closed field set, seven
fields:

| Field | What it is |
|---|---|
| `answers_gaps` | Nonempty, sorted, unique gap identities this proposal answers. |
| `grammar` | The literal `malleus.ontology-revision-proposal/v1`. |
| `issued_at` | The issue time the composed migration receipt carries. |
| `linkml_addition` | The addition as its owner wrote it, an additive LinkML fragment. Core composes it; nobody interprets its names. |
| `proposal_id` | Declared by its owner. Also the retained record id, which is what makes a proposal addressable. |
| `reason` | The revision reason the composed migration receipt carries. |
| `revision_id` | The id the recorded revision will carry, declared by its owner. |

There is no `target`. A proposal that supplies one refuses `MALFORMED_PROPOSAL`
with that word in the detail. Core derives the target, which is what lets a
proposer hold no compiler and stops anyone handing Core an artifact Core did not
compile.

A proposal is retained through
`KnowledgeChangeHistory.retain_ontology_revision_proposal`, which is the only
door that derives a target. The ordinary anchor door still reads any bytes that
claim the grammar and now refuses `PROPOSAL_TARGET_NOT_DERIVED` when no derived
target names the proposal's identity, so **retention is still the check** and a
proposal cannot enter through a path that does not know about proposals.

### The answer grammar

`malleus.ontology-gap-answer/v1`, canonical JSON, closed field set, seven
fields: `answered_gaps`, `deciding_actor`, `disposition` (closed to `ACCEPTED`
and `REFUSED`), `grammar`, `proposal_id`, `reason`, `revision_identity`. On
`ACCEPTED`, `proposal_id` and `revision_identity` are set and `reason` is the
proposal's reason; on `REFUSED` both are `null` and `reason` is the deciding
actor's. The precedent for a closed field set carrying a null is
`ContractRevisionChange.value`.

The ledger event is `ONTOLOGY_GAP_ANSWER_RECORDED`, payload closed to
`answer_identity` and `gap_answer_bytes_base64`, event id
`gap-answer:<identity>`. It is a Core-authored event outside the machine
program, exactly as `CONTRACT_REVISION_RECORDED` already is.

### The four acts

`KnowledgeChangeHistory.retain_ontology_source(root_locator=..., sources=...,
transaction_time=..., actor_id=...)` takes exactly what
`compile_linkml_contract` takes, and that is the whole parameter list. **There
is no compiler profile parameter, because there is none in play:**
`compile_linkml_contract(root_locator, sources)` accepts no profile, and the
only profile-shaped parameter in the pipeline is the private LinkML entry's
compatibility `profile`, which accepts `None` or an exact copy of the packaged
profile and refuses anything else. Inventing a parameter with one legal value
would be a shape with no consumer. What the compilation actually used is not
lost: the retained set records the compiler execution identity, which is the
artifact evidence digest and binds the adapter profile, the binder profile, the
producer and the resolver selection. Core compiles the set and refuses
`ONTOLOGY_SOURCE_DOES_NOT_REPRODUCE_CONTRACT` unless the compiled validated
contract identity is the one this history runs. It appends the module bytes this
history lacks and then the set that names them, in one batch.

The comparison is the contract identity, not the artifact envelope. **This was
measured, not assumed:** the fixture's closure builder and
`compile_linkml_contract` compile one source set to the same
`validated_fact_set_sha256` and to different `evidence_sha256` and different
artifact bytes, because the envelope carries the compiler's own evidence.
Requiring envelope equality would admit only histories created through this
exact door. The envelope is not discarded: the retained set records the compiler
execution identity, so two executions are still told apart.
`test_the_reproduction_check_is_the_contract_identity_not_the_envelope` holds it.

`KnowledgeChangeHistory.retain_ontology_revision_proposal(proposal_bytes=...,
transaction_time=..., actor_id=...)` reads the current source set, refusing
`ONTOLOGY_SOURCE_NOT_RETAINED` if there is none, composes the fragment onto the
root, compiles the composed set with that set's own dependency map, and composes
the target partial contract with this history's normative profile. Four records
go in one batch, in this order because the fold checks each against what is
already retained: the composed root's bytes, the source set the next contract
will have, the derived target, the proposal. The next source set is retained
here rather than at acceptance on purpose: it names a contract identity that is
not active yet, so it is simply not current until the revision lands, and
acceptance needs to append nothing extra.

`KnowledgeChangeHistory.accept_ontology_revision_proposal(proposal_id=...,
deciding_actor=..., transaction_time=..., actor_id=...)` composes the additive
revision from the derived target and appends the revision event and the answer
event in **one** `_append` batch, which validates the whole candidate before any
byte is written. The fold then refuses an `ACCEPTED` answer whose revision is not
recorded in the same history with the same `revision_id` and the same target
bytes, so there is no state in which a proposal is accepted and not applied, and
the invariant is enforced on replay rather than only at the call. After it, the
composed root is the current source, so the next proposal composes on it.

`KnowledgeChangeHistory.refuse_ontology_gaps(gap_identities=..., reason=...,
deciding_actor=..., transaction_time=..., actor_id=...)` records one `REFUSED`
answer. The gaps close; the ontology does not move.

The deciding actor is recorded, not authenticated. Whether this actor may decide
is the adopter's to establish; Core records who did.

### Where LinkML is required, and where it is not

Exactly two acts import LinkML, both by a deferred import inside the method:
`retain_ontology_source` and `retain_ontology_revision_proposal`. Both are
compiler-enabled by definition. Admission, acceptance and replay import none:
they read the target retention already derived. Two tests hold the boundary by
running a fresh interpreter, replaying a history with a retained source set and
accepting a proposal in it, and asserting that no module named `linkml`,
`linkml.*` or `linkml_runtime*` is in `sys.modules` afterwards.

**Both probes were inert when first written, and that is recorded here rather
than quietly fixed.** They ran `sys.executable -c` with the parent environment
inherited, so they only reached this tree because the run happened to export
`PYTHONPATH`. A bare subprocess on this laptop resolves `malleus` to
`/Users/luis/Projects/malleus-dev/src/malleus`, the main checkout, which carries
none of this work. Measured, not reasoned: a bare probe prints that path and
reports `has retain_ontology_revision_proposal False`. Both probes now pin
`PYTHONPATH` to this tree explicitly and begin by asserting
`malleus.__file__` starts with the tree's root, and
`test_the_linkml_free_probe_runs_the_tree_under_test` is the control: it runs
the probe with `PYTHONPATH` emptied and requires an `AssertionError`. This is
the second time in this task a control was inert for this reason; the first is
in the commit message of `a7108e52`.

The residual, stated plainly: the fold checks the additive diff and does **not**
recompile the fragment, because recompiling would put LinkML in replay. The
derivation is checked at the door that performs it. What makes it auditable
later is that the target records the source set it composed onto and the
composed root's digest, and both sets of bytes are in the ledger, so anyone with
a compiler can reproduce the derivation from the history alone.

### The report

`KnowledgeHistoryReplay.open_gaps()` returns a tuple of `OpenOntologyGap`:
`identity`, `kind`, `locator`, `plan_id`, `source_id`, `statement`, and
`open_proposals`, a tuple of `OpenRevisionProposal` carrying `proposal_id` and
`identity`. Gaps are sorted by plan id then gap identity, proposals by proposal
id then identity, so two reads of one history and a read of a reopened copy give
the same bytes. `KnowledgeHistoryReplay.gap_answers` holds the recorded
decisions. `OpenOntologyGap.as_dict()` is the JSON form a runner prints.

The second build adds three readers beside it, all on the replay and all
LinkML-free: `ontology_source_set()` returns the current source set or `None`,
`ontology_source_map()` returns `{locator: bytes}` for it or refuses
`ONTOLOGY_SOURCE_NOT_RETAINED`, `ontology_source_bytes(locator)` returns one
module, and `ontology_revision_target(proposal_id)` returns what Core derived
for one retained proposal.

## Every refusal, and when it fires

Three closed enums, all raised as `ValueError` subclasses like every other
refusal in the pipeline. `KnowledgeChangeHistory.replay` lets them through
rather than folding them into `MALFORMED_HISTORY`.

`OntologyGapAnswerRefusalReason`, eleven:

| Reason | Fires when |
|---|---|
| `MALFORMED_PROPOSAL` | Bytes claim the proposal grammar and are not canonical, or the field set is not closed, or `answers_gaps` is empty, unsorted or has duplicates, or a required text is empty, or the retained record id is not the declared `proposal_id`. A supplied `target` is named in the detail. |
| `MALFORMED_ANSWER` | A recorded answer's bytes are not canonical or closed, its disposition is not declared, a `REFUSED` answer names a proposal or a revision, an `ACCEPTED` answer closes gaps its proposal does not name, or an `ACCEPTED` answer's revision is not recorded in this history. Also when `refuse_ontology_gaps` is given no gap identities. |
| `UNKNOWN_GAP` | A proposal or a refusal names an identity no retained gaps artifact declares. |
| `GAP_ALREADY_ANSWERED` | A named gap is already closed by a recorded answer. |
| `GAP_KIND_NOT_ONTOLOGY` | A named gap is one of the other four kinds: `AGGREGATE_ONLY`, `INTERVAL_NOT_EXPRESSIBLE`, `MODALITY_NOT_EXPRESSIBLE`, `REQUIRED_FIELD_ABSENT_IN_SOURCE`. |
| `PROPOSAL_NOT_ADDITIVE` | The composition rule refused, with its own reason name in the detail; or the compiled revision refuses `NON_ADDITIVE_CHANGE` or `POLICY_REFUSAL`. |
| `PROPOSAL_DOES_NOT_COMPILE` | The composed source will not compile, or the compiled revision refuses for any other reason. |
| `UNKNOWN_PROPOSAL` | Acceptance names a proposal id the history does not retain. |
| `PROPOSAL_ALREADY_DECIDED` | A second acceptance of the same proposal, checked before the gap check and again in the fold. |
| `MISSING_DECIDING_ACTOR` | The deciding actor is absent or empty, on either act. |
| `PROPOSAL_TARGET_NOT_DERIVED` | A proposal is retained with no derived target naming its identity, which is what the ordinary anchor door now hits. |

`OntologySourceRefusalReason`, seven:

| Reason | Fires when |
|---|---|
| `MALFORMED_SOURCE_SET` | Bytes claim the source-set grammar and are not canonical or closed, modules are unsorted or duplicated, the root locator names no module, the record id is not the bytes' digest, or a declared byte length denies its bytes. |
| `MALFORMED_REVISION_TARGET` | The same, for the derived-target grammar. |
| `ONTOLOGY_SOURCE_NOT_RETAINED` | A proposal is retained, or the source map is read, on a history whose active contract has no retained source set. Also when a derived target names a source set the history does not hold. |
| `ONTOLOGY_SOURCE_ALREADY_RETAINED` | `retain_ontology_source` is called twice with the same set. |
| `ONTOLOGY_SOURCE_BYTES_NOT_RETAINED` | A source set names a module digest, or a target names a composed root digest, the history does not hold. |
| `ONTOLOGY_SOURCE_DOES_NOT_REPRODUCE_CONTRACT` | The set does not compile, or compiles to a validated contract identity that is not the one this history runs. |
| `REVISION_TARGET_SOURCE_SET_NOT_CURRENT` | A derived target composed onto a source set that is not the active contract's. |

`LinkMLAdditionRefusalReason`, nine:

| Reason | Fires when |
|---|---|
| `MALFORMED_BASE` | The base is not exact bytes, not UTF-8, carries a BOM, is not one strict YAML mapping, or carries an anchor, alias, tag, directive or document marker. |
| `MALFORMED_FRAGMENT` | The same for the fragment, plus an empty section, a duplicate key, or a section of the wrong shape. |
| `UNSUPPORTED_FRAGMENT_KEY` | Any top-level key outside `classes`, `enums`, `imports`, `prefixes`, `slots`. |
| `EXISTING_CLASS` | The fragment names a class the base declares, including one carrying nothing but `slot_usage`. |
| `EXISTING_SLOT` | The fragment names a slot the base declares. |
| `EXISTING_ENUM_FIELD` | An existing enum's entry carries anything but `permissible_values`. |
| `EXISTING_PERMISSIBLE_VALUE` | A permissible value the enum already declares. |
| `EXISTING_IMPORT` | An import literal already imported. |
| `EXISTING_PREFIX` | A prefix name already bound. |

## The two consumer shapes

Both run the same path, and the observation tests are parametrized over the two
so neither can drift.

1. **A population-plan history.** The gaps artifact is the one
   `prepare_population_change` generates from a compiled plan, retained as
   `plan:neutral:1:gaps`. The plan is admitted with
   `check_and_admit_change_set`.
2. **A change-set history.** The producer composes its own operations with
   `compose_change_set`, admits them, and retains its own gaps artifact for the
   round as `round:change-set:1:gaps`. There is no compiled plan anywhere.

The second is the one that proves this is not an adapter for the population
pipeline: nothing in the path reads a plan, a derivation or a profile. It reads
a gaps artifact, by its own bytes.

Both now retain their ontology source first, through the same act with the same
three-module source map shape `partial_shipments/run.py::revise` assembles: the
domain root, `malleus`, and `linkml:types` from the LinkML runtime. The private
`shop-progressive-01/d0/revision.py::_compile` assembles a wider one, eight
modules including profiles and packs, and the operation takes it unchanged
because it takes what `compile_linkml_contract` takes. Reading both before
designing is what kept the parameter from being shaped around one of them.

## The runners, and the one that could not be migrated

`OpenOntologyGap.as_dict()` goes into the round report of the two Small Shop
runners that print one as JSON and can be edited: `content_rules/run.py` and
`shipment_policy/run.py`, each as a new `open_gaps` key. Every other key of
those reports is unchanged, and each has a test that reads its stdout by key
rather than as a whole document.

Both report `"open_gaps": []` today, and that is the honest state, not a broken
report. No tracked program under
`research/ontology_driven_kg_realization/experiments/` declares a `TYPE_ABSENT`
or a `RELATION_ABSENT` gap: a grep for either kind across that tree returns
nothing, and `connected_story/mapping.json` declares no gap of any kind. The
Shop round that declared a customer `TYPE_ABSENT`, which is where this roadmap
item came from, lives under `private/`, which never enters git. The report line
is exercised against a history that does carry an open gap by Core's own tests,
over both consumer shapes.

**`connected_story/run.py` cannot be migrated without re-pinning frozen
evidence, so it was not.** It retains its own source bytes, `Path(__file__)` at
`run.py:320`, as the evidence artifact `artifact:connected-shop:adapter`, and
every one of its 23 population plans names that artifact's digest in its
evidence closure. A four-line comment and one key in `main()` therefore moved,
measured against the same Core in a pristine tree at `d3833d02`:

| Coordinate | Frozen | With the edit |
|---|---|---|
| `artifact:connected-shop:adapter` | `sha256:7bb13ede36a9969b79ff5d93bbc02313d79328f0e6567beb7284a887c34c1e30` | `sha256:519c2d9e7e62c63cd749a0a59ee3834bff5203474c1bed47e30d94627f421620` |
| every `plan:shop-connected:e*` digest, 23 of them, e.g. `e1` | `sha256:1473c69591d38bcce22b6b59fdb0b18ddf0754cba62126620d11d24599466305` | `sha256:54c276f8d3379c4a756419e34a1d7736a307067e7cea8ce72d9ce3957070396d` |
| ledger head | `sha256:9e0cff50f34fcdb8888b0f6d2d4ebbfcc832fc485876f85871bc7b633216cd4a` | `sha256:aa712ffcf4a98b2c8650f36bd49e6cc940a721aed383530b963d86bbb3c0b563` |
| replay receipt, which `connected_story/run_receipt.json` pins | `sha256:cf0fe19f0263e9945ffc6ad4337208df86e5c353f9263bcb054fd9c7923feee2` | `sha256:10e546712705c4d131d7cd4ccd4290b46348418c4e7fd132ce6a75bcedb4d718` |

The accepted graph's state digest and the contract identity did **not** move.
What moves is the evidence closure and the ledger identity cut against it. The
blast radius was 6 failed tests and 22 errors, all downstream of that history:
`connected_story/test_connected_run.py`, `test_object_timelines.py`,
`test_shipment_explanation.py`, `connected_story/partial_shipments/`,
`connected_story/warehouse/`, and `content_rules`'s own control
`test_baseline_reproduces_the_committed_connected_receipt`, which builds the
connected history to compare against.

This is established by identity, not by inference and not by bisection. The
committed `connected_story/run.py` hashes to
`sha256:7bb13ede36a9969b79ff5d93bbc02313d79328f0e6567beb7284a887c34c1e30`, which
**is** the frozen `artifact:connected-shop:adapter` digest, and the same file
with the four comment lines and the one key hashes to
`sha256:519c2d9e7e62c63cd749a0a59ee3834bff5203474c1bed47e30d94627f421620`, which
is the digest the failing run reported. The runner's source bytes are the
artifact, so editing the file moves the artifact by definition. Core is not
involved.

One correction to the record, because the first attempt at this was wrong and
the commit message of `2d18c6e2` still carries it. That message says the finding
was established by bisection, "the same test passes in a pristine `d3833d02`
tree with this branch's Core and fails in this branch's tree with pristine
Core". Those two runs do not show what they were read as showing:
`pyproject.toml:256` sets `pythonpath = [".", "src"]`, and pytest prepends that
to `sys.path`, so under pytest the Core is always the rootdir's `src` whatever
`PYTHONPATH` says. Both runs used the Core of the tree they ran in, so they
varied nothing and isolated nothing. The conclusion they were read as supporting
is right, but the two digests above are why, and they were measured afterwards.
Anyone swapping Core for a control in this repository must move the tree or
override `pythonpath`, not export `PYTHONPATH`.

**The smallest shape that does not move them**, for whoever decides: stop
retaining the runner's source as the adapter artifact, and retain the adapter's
declared identity and version the way every other runner does, so that editing
the runner is no longer an ontology-visible act. That is a change to what the
connected story retains, which re-pins its evidence once and deliberately. It
was not taken here because the brief says not to re-pin frozen evidence, and
because it is a separate decision about what an adapter's identity is. Until
then, the connected story's round report has no `open_gaps` key and
`replay.open_gaps()` is still available to anyone reading that history.

Four further Small Shop runners were left alone because their stdout is frozen
evidence compared byte for byte or is the evidence itself:
`showcase/run.py` and `correction/run.py` (`pareto/test_vertical.py:492`,
`correction/test_correction_vertical.py:773`, `showcase/test_query.py:339`), and
`object_event/run.py` and `public_population/run.py`, which print their evidence
bytes rather than a summary.

**`document_paper/` has no runner that prints a round summary.** Its five
`main` entry points are `query_replay`, `query_score`, `multimodel`,
`v2_experiment` and `text_layer_reading`; the first four write files and print
nothing, and `text_layer_reading` prints a reading census with no knowledge
history in hand. There was nothing there to migrate, and nothing was invented to
migrate.

## Residuals, stated plainly

- **The fold does not recompile the fragment.** It runs the additive diff, which
  is LinkML-free, against the target retention derived. Recompiling inside the
  fold would put the LinkML runtime in replay, which the boundary above refuses.
  What makes the derivation auditable anyway: the target records the source set
  it composed onto and the composed root's digest, and both sets of bytes are in
  the ledger, so the derivation is reproducible from the history alone by anyone
  with a compiler. It is not reproduced automatically, and that is the residual.
- **The composition rule is Core's, not LinkML's.** `compose_linkml_addition`
  decides additivity from the two documents' own structure, not from LinkML
  semantics. It refuses more than LinkML would: a fragment that re-declares a
  class identically is refused as `EXISTING_CLASS` rather than merged. That is
  the fail-closed direction and no consumer has met it.
- **`ADD_IMPORT` is a composition rule without a compiled proof.** A fragment
  may add an import literal, and the rule refuses one already imported. The
  compiled round-trip proof covers `ADD_CLASS`, `ADD_SLOT` and `ADD_ENUM_VALUE`
  only, because a new import needs a module the retained dependency map does not
  carry. What happens through the proposal door was measured rather than
  assumed:
  `test_a_fragment_importing_a_module_the_source_set_lacks_refuses` retains such
  a proposal and gets `PROPOSAL_DOES_NOT_COMPILE` with the ledger untouched.
  That is the honest outcome and it is not the same as proving an added import
  compiles, which nothing here does.
- **The sdist does not carry the three new modules.** `pyproject.toml`'s
  `[tool.hatch.build] include` list names every `_contract_pipeline` module it
  packages and does not name `gap_answer.py`, `linkml_addition.py` or
  `ontology_source.py`. Four builds were run rather than reasoned about, all
  from the restored `pyproject.toml`:

  | Artifact | Carries the three | `import malleus.compiler` |
  |---|---|---|
  | wheel built from the tree | yes | works |
  | sdist built from the tree | no | not applicable |
  | wheel built from that sdist | no | `ModuleNotFoundError: No module named 'malleus._contract_pipeline.gap_answer'` |

  The wheel is whole because `[tool.hatch.build.targets.wheel]` sets
  `packages = ["src/malleus"]`, which takes the package directory entire and
  makes the `include` list irrelevant for that target. The sdist has no such
  override, so the `include` list is what it ships. The comment above that list,
  "Only the files explicitly listed below are packaged", is therefore true of
  the sdist and false of the wheel, which is why reading it alone led to the
  wrong conclusion here first.
  The hole is not new: `gap_answer.py` has been missing since the first build's
  commit `0374937f`, and this build widens it by two modules. Nothing in the
  repository suite sees it, because every suite runs from the tree, and the one
  test that reads the list, CC-X02's duplicate scan, asserts its bytes rather
  than that it is complete. **The decision for Luis:** adding the three lines is
  the fix and it re-pins CC-X02's retained evidence, which the brief says is not
  mine to do, so either re-pin CC-X02 deliberately with the three lines in, or
  leave the sdist unable to import `malleus.compiler`. Worth naming beside it: a
  test that derives the expected `include` list from what `malleus.compiler`
  actually imports would have caught `gap_answer.py` in September and would
  catch the next one. It re-pins nothing on its own and only passes once the
  list is complete.
- **A partially closed proposal.** A proposal may name two gaps and a separate
  refusal may close one of them. The proposal then stays visible under its
  remaining open gap and refuses `GAP_ALREADY_ANSWERED` on acceptance. That is
  honest but not pretty; no consumer has met it.
- **The gap field set has two literals.** `population.py` writes the four-field
  set inline and `gap_answer.GAP_FIELDS` reads it. They are held to one value by
  a test that asserts the set of a gap which population itself accepted and
  retained, rather than by a shared constant, because `population` imports
  `knowledge` and `knowledge` imports `gap_answer`, so the shared home would be
  a cycle.

## Measurements

RED first, on the untouched Core at `d3833d02`, before any of the above existed:
`tests/contract_compiler/pareto/test_ontology_gap_answer.py` reported
**28 failed, 2 passed**. The two that passed are the guards that must pass on an
untouched Core and must keep passing: the six population gap kinds are unmoved,
and the revision policy's five change kinds are unmoved. Of the 28, 26 fail on
behaviour that did not exist and 2 fail only because their fixture calls
`ontology_gap_identity`.

GREEN: **30 passed** in that file after the first build.

The second build, the one that made the proposal a fragment, was measured the
same way, three RED-then-GREEN cycles against the branch tip:

| Selection | RED | GREEN |
|---|---|---|
| `test_linkml_addition.py` | 24 failed, 0 passed | 24 passed |
| `test_ontology_source_set.py` | 13 failed, 0 passed | 17 passed |
| `test_ontology_gap_answer.py` | 22 failed, 18 passed | 42 passed |

The GREEN counts are higher than the RED counts because four tests were added
after the build, and each is worth naming rather than hiding. The reproduction
check was written against the artifact envelope; the first run refused a source
set whose contract identity matched, and the expectation was wrong rather than
the code, so
`test_the_reproduction_check_is_the_contract_identity_not_the_envelope` records
the measurement that settled it. The LinkML-free probes had no control, so
`test_the_linkml_free_probe_runs_the_tree_under_test` is one. And two refusal
reasons, `MALFORMED_REVISION_TARGET` and
`REVISION_TARGET_SOURCE_SET_NOT_CURRENT`, were declared in the tables below
while nothing in the suite had ever made either fire; both now have a test that
does. Every refusal reason in the three tables is now exercised.

The 18 that passed RED in the gap-answer file are the ones the reshape does not
touch: gap identity, the open-gap report, the whole refusal path, determinism
across a reopen and the two unmoved-identity guards. The 22 that failed are the
reshaped grammar, the derived target, the new source requirement and the
LinkML-free acceptance.

Suites, run from the worktree root with `PYTHONPATH` exported and
`-p no:randomly`. Note for anyone repeating this: the export is belt and braces,
not what selects the tree. `pyproject.toml:256` sets
`pythonpath = [".", "src"]`, which pytest prepends to `sys.path`, so a pytest
run always uses the rootdir's own `src` whatever `PYTHONPATH` says. The baseline
column below is therefore a real baseline for a different reason: it was
measured in this worktree at `d3833d02` with a clean tree, before any file here
existed. The RED column was measured in the same worktree when the test file was
the only thing that existed.

| Selection | Baseline at `d3833d02` | First build | This branch |
|---|---|---|---|
| `tests/contract_compiler` + `small_shop` + `document_paper` | 1 failed, 1826 passed | 1 failed, 1856 passed | 1 failed, 1904 passed |
| the same three, rerun by the Overlord at the final tip `590b9a39` | | | 1 failed, 1909 passed |
| `tests/contract_compiler` alone | | | 1380 passed |
| `small_shop` + `document_paper` alone | | | 1 failed, 524 passed |
| `test_ontology_gap_answer.py` | 28 failed, 2 passed | 30 passed | 42 passed |

Lint and formatting, over the eleven Python files this branch changed:
`ruff check` passes, and `ruff format --check` reports all eleven already
formatted. That took a commit. `knowledge.py` at `d3833d02` is format-clean
under ruff's default profile, `pyproject.toml` carries no `[tool.ruff]` section
so the profile is the default, and this branch's edits to it were not clean.
Six files drifted on line joins only, and
`590b9a394a54cd92d5fde645efc13e505b2c8a88` brings them back. The
repository does not enforce `ruff format` globally: 83 of the 146 files under
`src` and `tests` would still be reformatted, which is why the pass is scoped
to this branch's files and not the tree.

Every frozen digest, receipt and accepted-state identity in `small_shop` and
`document_paper` is unchanged. Those suites are the check, and they pass apart
from one failure that is not this work:
`research/.../document_paper/test_v2_experiment.py::test_driver_recompiles_the_exact_accepted_ontology_coordinate`
refuses with `recompiled validated contract differs from acceptance`
(`v2_experiment.py:163`). **Measured here, not repeated from the earlier
record:** a pristine tree extracted from `d3833d02` into a scratch directory,
with an untouched Core, runs that file and reports `1 failed, 8 passed` with the
same refusal. It is a stale pinned LinkML recompile coordinate, the same class
of defect as ROADMAP F6, and it is not fixed here.

The full default suite, `pytest -q -p no:randomly` over `testpaths`, reports
**24 failed, 3670 passed, 3 skipped** at the first build; rerun by the Overlord at
the final tip `590b9a39` with PYTHONPATH exported it reads **24 failed, 3731 passed,
3 skipped**, the same 24 (14 integration, 7 ledger, 3 docs), every one of them
the `docs/contract_compiler/index.md` digest guard. All 24 have one cause, printed verbatim
by each of them:

```text
OVR-000472: latest document digest mismatch for docs/contract_compiler/index.md,
expected sha256:a8ff630e…, got sha256:c57886e0…
```

They are 7 in `tests/test_contract_compiler_ledger.py`, 14 in
`tests/test_contract_compiler_integration.py` and 3 in `tests/test_docs.py`,
whose documentation build runs the same validator. The overseer ledger is
checked against the governed documents' current bytes, so any branch that edits
a governed document fails these until its entry is sealed. `OVR-000477` below is
that entry. This is not an assertion: in the sealed scratch copy described under
the entry, with the re-cut `OVR-000477` inserted and `head.json` advanced, those
three files plus `tests/test_capability_declaration.py` report **506 passed, 0
failed**. No other test in the default suite moved.

That count was taken on the rebuilt copy, over all sixteen documents, so it
covers everything this entry gained on the second build, including the two new
modules and their tests. It does not depend on the wording of
this file: the sealer recomputes this file's digest from the copy it just built,
so paragraphs written after the run, such as this one, move the head hash and
not the result.

## Commits

| Hash | Subject |
|---|---|
| `0374937fb0f95b305a6404a56facf32abeffda4e` | A declared ontology gap is an open question with a recorded answer |
| `2d18c6e22d946d9217eb298d1e4bdfb199d83ead` | The round report says which ontology gaps are still open |
| `0ac2d432a05fb0eb9452c5fd1e5406fbdca39dc5` | The gap answer enters the compiler page, the status boundary and the changelog |
| `5a5737b83e854ba71a9c47b863ab5210c76d99ab` | Core declares the gap answer as a capability |

| `a21962b3e4dbd038c5153fce17285cd166b3c493` | A proposal is born a fragment and Core compiles it |
| `7178797dd897a79e49c5e1ad52f5f27a23cb7fba` | The retained source and the composed fragment enter the docs |
| `3e55d43c28bbad051b24b85ee618afb6e4dacb59` | The capability row follows the new shape |
| `b82c5cb4e44b0f1e5d06d5a12defa080de4861d5` | The import residual becomes a test instead of a claim |
| `a465222b1ebfb13235a91b8d1710e96e416f6a32` | The two target guards that had never fired now have tests |
| `3147ccd3a8a5b45e285ffba27d41d1d3d2113912` | Restore pyproject.toml to its frozen bytes; the packaging gap is Luis's call |
| `590b9a394a54cd92d5fde645efc13e505b2c8a88` | The six files this branch wrote follow the formatter the repository already uses |

Four further commits carry this file and the record:
`9a45942748e67181bdcb3028964c7d6781632fc2`,
`a7108e52523517e32411bfc21f3912c8bf52492a`,
`bfeea1e5887f9d1202ed8c408048c71741c664ef` and
`1636e5415cbb365f16aef910fd2642ed4ae60cfa`, plus the one that carries its
final state. The entry evidences the eleven in the table above, which are the
work.

## The declared capability

`malleus.IMPLEMENTATION_STATUS` gains `recorded-ontology-gap-answers`, beside
`explicit-record-supersession`, and
`.claude/skills/malleus-dev/references/CAPABILITIES.md` gains the matching row,
placed immediately after the additive-revision row it builds on and carrying the
same six columns as its neighbours: the public entry points, what the capability
does, `implemented`,
`OPTIONAL_PROFILE: semantic-history with compiler-enabled`, and
`Public compiler and population facade`. The row was revised when the proposal
became a fragment; it now names twenty-two entry points, including
`retain_ontology_source`, `retain_ontology_revision_proposal`,
`compose_linkml_addition` and the two new grammars.

The capability ID did not change. The authorization for this file is one row,
and `recorded-ontology-gap-answers` still names what the capability does: a
declared gap gets a recorded answer. Retaining the ontology source is arguably a
capability of its own and would be a second row; that is a judgment left to
Luis, not taken here.

The two are one act, not two: `tests/test_capability_declaration.py` refuses an
ID in the status module that the declaration does not carry, and refuses a
declared entry point that does not import. Both were run again after the
revision: **11 passed** there, and **107 passed, 1 skipped** in
`tests/test_inquisition.py`, unchanged, because no acolyte-facing text moved.
All twenty-two entry points resolve.

This matters more than a row in a table. The rule at the top of that file exists
because three consumer projects met a limitation on 2026-09-17 and worked around
it while Core already carried the capability. A capability that ships and is not
declared is a capability the next project will work around, which is the exact
failure this whole roadmap item came from.

## The overseer entry: `OVR-000477`

How the document set was computed, mechanically:

1. Every path an active sealed `DOCUMENT_REVISION` entry records, with its
   latest `after_digest`, read from
   `design/contract_compiler/overseer/entries/OVR-*.json` with `CORRECTION`
   supersession applied and `REMOVED` respected.
2. Everything this branch changed, `git diff --name-only d3833d02..HEAD`:
   **15 paths**, plus this file.
3. The intersection with the governed set: **8 MODIFIED**. The other **8** have
   never been recorded and are **CREATED**, by the precedent `OVR-000472` set
   when it added eight existing documents to the set the same way. This file is
   one of them, with `after_digest` the literal placeholder the sealing step
   re-derives. The earlier cut of this entry said 8 MODIFIED while listing 9;
   the count is now taken from the block itself, which reads 8 and 8.
4. **16 documents**, one entry, under the cap of 20.

Every `before_digest` was checked twice, against the ledger's own latest
recorded digest for that path **and** against the file's bytes at `d3833d02`:
all eight agree, so the two readings of "the committed bytes this branch started
from" are the same bytes. The latest recording per path is `OVR-000472` for
`CAPABILITIES.md`, `CHANGELOG.md`, `docs/IMPLEMENTATION_STATUS.md` and
`docs/contract_compiler/index.md`, `OVR-000473` for `shipment_policy/run.py`,
`OVR-000474` for `knowledge.py` and `compiler.py`, and `OVR-000442` for
`src/malleus/status.py`.

`pyproject.toml` joined the set on the second build and then left it again. The
edit that put it there moved CC-X02's frozen evidence, so it was withdrawn and
the file is back to its `d3833d02` bytes; what the missing `include` entries
cost is measured in a residual above, not changed here. `ROADMAP.md`, `head.json`, `status.md`,
`design/contract_compiler/overseer/entries/` and `paper-v4/` were not touched.

`.claude/skills/malleus-dev/references/CAPABILITIES.md` is in the set because
the declaration was authorized separately, for one row and nothing else. That
row and the matching `recorded-ontology-gap-answers` ID in
`malleus.IMPLEMENTATION_STATUS` are why `src/malleus/status.py` is here too:
`tests/test_capability_declaration.py` holds the two to each other, so they are
one act, not two.

One of the two migrated runners, `content_rules/run.py`, is `CREATED` rather
than `MODIFIED`: it has never been recorded in the ledger, while
`shipment_policy/run.py` was, at `OVR-000473`. That is a finding about the
ledger's coverage, not about this change.

The block below validates against
`design/contract_compiler/overseer/ledger.schema.json` with
`Draft202012Validator` and a `FormatChecker`, substituting
`sha256:0000…0000` for `entry_hash`, for the placeholdered `after_digest` and
for the placeholdered previous hash, and a real UTC timestamp for the
placeholdered sealing moment: **1 of 1 valid, 0 errors, 16 documents**. The
probe reads the fenced `json` blocks of this file and finds two, of which
exactly one parses as an object with an `entry_id`. `why` is 1197 characters,
under the 1200 cap; `summary` is 205, under 240. The counts above are from the
re-cut taken after `pyproject.toml` was restored.

Proved end to end in a scratch copy of the repository, hardlinked so every
governed document is the exact byte this branch holds, with the entry inserted
at the real previous hash and `head.json` advanced to 477.
`python scripts/contract_compiler_ledger.py render` then `check` both exit 0 and
`check` reports `validated 477 entries` with `head OVR-000477`. That run reaches
the real Git ancestry read-only, so the evidenced commits are checked for
durable reachability rather than assumed. The real worktree was never written
to.

**Whoever seals must build the scratch copy after the last edit to this file.**
The copy is hardlinked, and the entry records this file's digest, so an edit
made after the copy was built reaches the hardlink while the entry keeps the
old digest. That happened here and cost one run: the ledger validator refused
with `OVR-000477: latest document digest mismatch for
handover/2026-09-21-core-gap-as-trigger.md`, which was the proof being stale and
not the branch being wrong. The figures below are from the rebuild.

**The head hash is deliberately not quoted here.** It is a digest over the
entry, and the entry records this file's digest, so writing the hash into this
file changes the file and moves the hash. The first cut of this entry quoted
`sha256:30f5c38a…` and the second quoted `sha256:3ac5843c…`; both were stale the
moment they were written, for exactly that reason. The verbatim `check` line for
the final tree is in the commit message of the commit that carries this file,
where it does not feed back into its own input, and the sealer recomputes it
anyway from `<digest of this file once final>`.

### `OVR-000477`

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:5fd1e2c4624d8124484fa5144a69cbd1504e41c695a824160cb4c7187b7fc03c",
        "before_digest": "sha256:428abf6449b7f55864e8e8b7cef44dfd23cf808ea738fec997be344c25377240",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"
      },
      {
        "after_digest": "sha256:e457392794b3f7fb1a24c63ce177fc05c76d08cc3b6ed98e0b3dc7e5fbadef9a",
        "before_digest": "sha256:71ee0e48be085c1e75af6658df40719c1b7b1cff933a11f6b731c9840bf696ee",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:1f97126796b8b1420805c4d4e05703f12629650f1650325253e232493da7dca2",
        "before_digest": "sha256:09feedab1dac003c5ec959ef0367f603070e3c544a5346b9a678320cb5b4d137",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:9e0ae5a84478e414f79b5c60500e4c8f9db8cd30a31a1ffa0bf39ebb82fd6262",
        "before_digest": "sha256:a8ff630e712d695f5567505907541b51ec41dbdb84238291635cebc146367797",
        "change": "MODIFIED",
        "path": "docs/contract_compiler/index.md"
      },
      {
        "after_digest": "<digest of this file once final>",
        "change": "CREATED",
        "path": "handover/2026-09-21-core-gap-as-trigger.md"
      },
      {
        "after_digest": "sha256:dc918f4fb855fff7e8aa6af50119b66a1e7af33e1bfad723f5aea6acebedd90a",
        "change": "CREATED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/content_rules/run.py"
      },
      {
        "after_digest": "sha256:06ce9cb9657c18e6e74f18ac2398cd9e1f0a6c21aa2db344241bb92958747f7d",
        "before_digest": "sha256:f1d14f37497829e2871471a3e2413213ba0b34ae55e38413d7e50080568cb415",
        "change": "MODIFIED",
        "path": "research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/run.py"
      },
      {
        "after_digest": "sha256:93582a2ad71bee08f93b2319ad22287496b0bb2c33968c75434a63ca63ddfd48",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/gap_answer.py"
      },
      {
        "after_digest": "sha256:e4bac3ccf1c2da4cff4c03c7e02eb0574bb4f7d211eab49a701b4338ed6b712c",
        "before_digest": "sha256:0d4fa887438300337891684bb7e4d0c63d561d2cb99de5655b635498ac5f801c",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/knowledge.py"
      },
      {
        "after_digest": "sha256:2d5d3999b10b2f0b34dde729fc929a2483f7bb6fc4718f7972e986f98088ce57",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/linkml_addition.py"
      },
      {
        "after_digest": "sha256:57025fb7f4d691b236162c6234ebebbca5df2856f965ece744bee1b24d3fdd3c",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/ontology_source.py"
      },
      {
        "after_digest": "sha256:1c31e27c035a050772871582d92523ea4dd3a05bd667835eee0e280a6adbedbb",
        "before_digest": "sha256:5fc3a0253da35bb37c10379c54ad0b4cafcad8593e922f49c07c7cae4d880b5e",
        "change": "MODIFIED",
        "path": "src/malleus/compiler.py"
      },
      {
        "after_digest": "sha256:941b9fd36246629798947ad0c00e732165d4e41b34fed8a0e9bb086170d9079d",
        "before_digest": "sha256:392e9a58615a44974c2e4b2327c4bd4f98bc014199c10baf5ccca60b658a27d7",
        "change": "MODIFIED",
        "path": "src/malleus/status.py"
      },
      {
        "after_digest": "sha256:d1ea9d9ea5069160ad1d172f80ed47b6f622097c62257f74910e7095a94a7801",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_linkml_addition.py"
      },
      {
        "after_digest": "sha256:6316aa9b7f9b46ac359e9f67f4659a9b171b6ad4e71921553b1348fe0d954bc6",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_ontology_gap_answer.py"
      },
      {
        "after_digest": "sha256:d4ad4a3553570c029c866bab86708b67ec1150bef858257897e4a15efa219b2a",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_ontology_source_set.py"
      }
    ]
  },
  "entry_id": "OVR-000477",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "0374937fb0f95b305a6404a56facf32abeffda4e",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "2d18c6e22d946d9217eb298d1e4bdfb199d83ead",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "0ac2d432a05fb0eb9452c5fd1e5406fbdca39dc5",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "5a5737b83e854ba71a9c47b863ab5210c76d99ab",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "a21962b3e4dbd038c5153fce17285cd166b3c493",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "7178797dd897a79e49c5e1ad52f5f27a23cb7fba",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "3e55d43c28bbad051b24b85ee618afb6e4dacb59",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "b82c5cb4e44b0f1e5d06d5a12defa080de4861d5",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "a465222b1ebfb13235a91b8d1710e96e416f6a32",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "3147ccd3a8a5b45e285ffba27d41d1d3d2113912",
      "type": "COMMIT"
    },
    {
      "relation": "EVIDENCES",
      "target": "590b9a394a54cd92d5fde645efc13e505b2c8a88",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 477,
  "subject": {
    "id": "core-gap-as-trigger",
    "type": "DOCUMENT"
  },
  "summary": "ROADMAP F2, second build: the ontology revision proposal is born a LinkML fragment, Core composes it onto the source the history now holds and compiles it, and no version with an unchecked field is sealed.",
  "why": "Luis, 2026-09-21, go. The first build retained linkml_addition verbatim and never parsed it, so a proposal whose text did not describe its own target would have been accepted. The fragment is now the checked input and target is gone from the grammar: a proposal supplying one is refused. Deriving the target needs the LinkML the contract was compiled from, which a history did not hold, so retain_ontology_source puts it in explicitly: it takes what compile_linkml_contract takes and refuses unless the set reproduces the running contract's identity. Genesis retains none and a recorded revision retains none, so no existing history moves. compose_linkml_addition is one pure additive rule with a deterministic serialiser, chosen by measuring that the compiled contract does not depend on YAML key order or style. retain_ontology_revision_proposal composes, compiles, and appends the composed root, the next source set, the derived target and the proposal in one batch; the additive diff under CONTRACT_REVISION_POLICY runs in the fold as the second check. Acceptance reads that target, so only two acts import LinkML and replay imports none. No change kind was added, so no frozen identity moves."
}
```

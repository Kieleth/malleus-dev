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
  writes nothing; a proposal against an `AGGREGATE_ONLY` gap refuses.
- **Reuse.** `compile_contract_revision` and `CONTRACT_REVISION_POLICY` for the
  additive check, unchanged and with no new change kind;
  `KnowledgeChangeHistory.compose_contract_revision` and
  `record_contract_revision`'s entry for the recorded revision; the ordinary
  anchor retention door for the proposal; the gaps artifact
  `prepare_population_change` already generates, read and never written.
- **Excluded.** Core drafting a proposal; deriving a class or slot name from a
  gap's statement (architectural law 8); authenticating the deciding actor;
  any change to check-contract re-binding, which stays the declared
  `REBIND_CHECK_CONTRACT` change; any change to the six gap kinds, to the gaps
  artifact's bytes, or to the revision policy's change kinds; compiling the
  proposal's LinkML fragment, which is retained as the owner's declared bytes
  and is not what Core checks. That last one is the residual, below.

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

**Nothing frozen moved.** The suite counts are under Measurements.

## What was built

One new module, `src/malleus/_contract_pipeline/gap_answer.py`, plus the fold
branches, the two recorded acts and the report in `knowledge.py`, and the public
names in `compiler.py`.

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

### The proposal grammar

`malleus.ontology-revision-proposal/v1`, canonical JSON, closed field set, eight
fields:

| Field | What it is |
|---|---|
| `answers_gaps` | Nonempty, sorted, unique gap identities this proposal answers. |
| `grammar` | The literal `malleus.ontology-revision-proposal/v1`. |
| `issued_at` | The issue time the composed migration receipt carries. |
| `linkml_addition` | The addition as its owner wrote it, LinkML text. Retained, not interpreted. |
| `proposal_id` | Declared by its owner. Also the retained record id, which is what makes a proposal addressable. |
| `reason` | The revision reason the composed migration receipt carries. |
| `revision_id` | The id the recorded revision will carry, declared by its owner. |
| `target` | Closed to `partial_contract` and `validated_contract`, the exact artifacts the revision would install. |

The proposal is retained through the ordinary anchor door as `RETAINED_EVIDENCE`.
There is no new retention entry point and no new role, which is deliberate:
**retention is the check**. Whichever door retains the bytes, the fold reads
them as a proposal and refuses before any write, so a bad proposal cannot enter
through a path that does not know about proposals.

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

### The two acts

`KnowledgeChangeHistory.accept_ontology_revision_proposal(proposal_id=...,
deciding_actor=..., transaction_time=..., actor_id=...)` composes the additive
revision from the proposal's own bytes and appends the revision event and the
answer event in **one** `_append` batch, which validates the whole candidate
before any byte is written. The fold then refuses an `ACCEPTED` answer whose
revision is not recorded in the same history with the same `revision_id` and the
same target bytes, so there is no state in which a proposal is accepted and not
applied, and the invariant is enforced on replay rather than only at the call.

`KnowledgeChangeHistory.refuse_ontology_gaps(gap_identities=..., reason=...,
deciding_actor=..., transaction_time=..., actor_id=...)` records one `REFUSED`
answer. The gaps close; the ontology does not move.

The deciding actor is recorded, not authenticated. Whether this actor may decide
is the adopter's to establish; Core records who did.

### The report

`KnowledgeHistoryReplay.open_gaps()` returns a tuple of `OpenOntologyGap`:
`identity`, `kind`, `locator`, `plan_id`, `source_id`, `statement`, and
`open_proposals`, a tuple of `OpenRevisionProposal` carrying `proposal_id` and
`identity`. Gaps are sorted by plan id then gap identity, proposals by proposal
id then identity, so two reads of one history and a read of a reopened copy give
the same bytes. `KnowledgeHistoryReplay.gap_answers` holds the recorded
decisions. `OpenOntologyGap.as_dict()` is the JSON form a runner prints.

## Every refusal, and when it fires

All ten are `OntologyGapAnswerRefusalReason`, raised as
`OntologyGapAnswerRefusal`, a `ValueError` like every other refusal in the
pipeline. `KnowledgeChangeHistory.replay` lets it through rather than folding it
into `MALFORMED_HISTORY`.

| Reason | Fires when |
|---|---|
| `MALFORMED_PROPOSAL` | Bytes claim the proposal grammar and are not canonical, or the field set is not closed, or `answers_gaps` is empty, unsorted or has duplicates, or a required text is empty, or the retained record id is not the declared `proposal_id`. |
| `MALFORMED_ANSWER` | A recorded answer's bytes are not canonical or closed, its disposition is not declared, a `REFUSED` answer names a proposal or a revision, an `ACCEPTED` answer closes gaps its proposal does not name, or an `ACCEPTED` answer's revision is not recorded in this history. Also when `refuse_ontology_gaps` is given no gap identities. |
| `UNKNOWN_GAP` | A proposal or a refusal names an identity no retained gaps artifact declares. |
| `GAP_ALREADY_ANSWERED` | A named gap is already closed by a recorded answer. |
| `GAP_KIND_NOT_ONTOLOGY` | A named gap is one of the other four kinds: `AGGREGATE_ONLY`, `INTERVAL_NOT_EXPRESSIBLE`, `MODALITY_NOT_EXPRESSIBLE`, `REQUIRED_FIELD_ABSENT_IN_SOURCE`. |
| `PROPOSAL_NOT_ADDITIVE` | The composed revision refuses `NON_ADDITIVE_CHANGE` or `POLICY_REFUSAL`: a removal, a narrowing, or `ADD_IMPORT`. |
| `PROPOSAL_DOES_NOT_COMPILE` | The composed revision refuses for any other reason, or the target artifacts cannot be read. |
| `UNKNOWN_PROPOSAL` | Acceptance names a proposal id the history does not retain. |
| `PROPOSAL_ALREADY_DECIDED` | A second acceptance of the same proposal, checked before the gap check and again in the fold. |
| `MISSING_DECIDING_ACTOR` | The deciding actor is absent or empty, on either act. |

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

## The runners, and the one that could not be migrated

`OpenOntologyGap.as_dict()` goes into the round report of the two Small Shop
runners that print one as JSON and can be edited: `content_rules/run.py` and
`shipment_policy/run.py`, each as a new `open_gaps` key. Every other key of
those reports is unchanged, and each has a test that reads its stdout by key
rather than as a whole document.

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

This was established by bisection, not inference: the same single test passes in
a pristine `d3833d02` tree with this branch's Core, and fails in this branch's
tree with pristine `d3833d02` Core. Core is not what moved it; the runner's own
bytes are.

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

- **The LinkML addition is declared, not compiled.** What Core checks is the
  proposal's `target` artifacts, which it composes against the history's current
  contract through `compile_contract_revision`. `linkml_addition` is retained
  verbatim as the owner's statement of what is being added and is not parsed.
  Core has no composition rule for a LinkML fragment against a compiled contract
  it does not hold the source of, and inventing one was outside this slice. A
  proposal whose `linkml_addition` does not describe its `target` would be
  accepted; what would be installed is the `target`, which is checked.
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

GREEN: **30 passed** in that file after the build, covering all seven
observations (a) to (g), both consumer shapes, the ten refusals, determinism
across a reopen, and the two unmoved-identity guards. Eight of the thirty are
the observation tests parametrized over both consumer shapes.

Suites, `PYTHONPATH` exported from the worktree root, `-p no:randomly`:

| Selection | Baseline at `d3833d02` | This branch |
|---|---|---|
| `tests/contract_compiler` + `small_shop` + `document_paper` | 1 failed, 1826 passed | 1 failed, 1856 passed |
| `tests/contract_compiler/pareto/test_ontology_gap_answer.py` | 28 failed, 2 passed | 30 passed |

The one failure is the same in both columns and is not this work:
`research/.../document_paper/test_v2_experiment.py::test_driver_recompiles_the_exact_accepted_ontology_coordinate`
refuses with `recompiled validated contract differs from acceptance`
(`v2_experiment.py:163`). It fails on a clean `d3833d02` in this environment,
before anything here existed. It is a stale pinned LinkML recompile coordinate,
the same class of defect as ROADMAP F6, and it is not fixed here.

`tests/test_docs.py` reports **3 failed, 137 passed**, all three with one cause:
`OVR-000472: latest document digest mismatch for docs/contract_compiler/index.md`.
The documentation build validates the overseer ledger against the governed
documents' current bytes, so a branch that edits a governed document fails it
until its entry is sealed. `OVR-000477` below is that entry. The three go green
with it; nothing else in `tests/test_docs.py` moved.

## Commits

| Hash | Subject |
|---|---|
| `0374937fb0f95b305a6404a56facf32abeffda4e` | A declared ontology gap is an open question with a recorded answer |
| `2d18c6e22d946d9217eb298d1e4bdfb199d83ead` | The round report says which ontology gaps are still open |
| `0ac2d432a05fb0eb9452c5fd1e5406fbdca39dc5` | The gap answer enters the compiler page, the status boundary and the changelog |

A fourth commit carries this file. The entry evidences the three above, which
are the work.

## The CAPABILITIES.md row

`.claude/skills/` is out of scope by the brief, so the declaration was not
edited. This is the row to add, after the existing additive-revision row:

```text
| A declared ontology gap answered by an additive revision, or refused with a reason | `malleus.compiler.ONTOLOGY_GAP_KINDS`, `malleus.compiler.ontology_gap_identity`, `malleus.compiler.ONTOLOGY_REVISION_PROPOSAL_GRAMMAR`, `malleus.compiler.ONTOLOGY_GAP_ANSWER_GRAMMAR`, `malleus.compiler.OntologyRevisionProposal`, `malleus.compiler.OntologyGapAnswer`, `malleus.compiler.OpenOntologyGap`, `malleus.compiler.OntologyGapAnswerRefusal`, `malleus.compiler.KnowledgeChangeHistory.accept_ontology_revision_proposal`, `malleus.compiler.KnowledgeChangeHistory.refuse_ontology_gaps`, `malleus.compiler.KnowledgeHistoryReplay.open_gaps` | Turns a declared `TYPE_ABSENT` or `RELATION_ABSENT` gap into an open question with one recorded answer. A gap's identity is the digest of the canonical `{"gap": <its four declared fields>, "plan_id": <the plan it was declared in>}`; a `malleus.ontology-revision-proposal/v1` record names the gaps it answers and carries the target contract artifacts, and is refused at retention unless every named gap is open, of an ontology kind, and the composed result is purely additive. Accepting composes and records the revision and the answer in one ledger batch, so a proposal is never accepted without being applied; refusing closes the gaps with a reason and moves no ontology; `open_gaps` reports what is still open with the proposals open against it. The deciding actor is recorded, not authenticated. Core drafts no proposal and derives no class or slot name from a gap's statement. | implemented | OPTIONAL_PROFILE: semantic-history with compiler-enabled | Public compiler and population facade |
```

No capability ID was added to `malleus.IMPLEMENTATION_STATUS`, deliberately:
`tests/test_capability_declaration.py` requires every ID there to appear in
that declaration, and the declaration could not be edited here. Adding the ID
and the row is one act, for whoever owns the skill.

## The overseer entry: `OVR-000477`

How the document set was computed, mechanically:

1. Every path an active sealed `DOCUMENT_REVISION` entry records, with its
   latest `after_digest`, read from
   `design/contract_compiler/overseer/entries/OVR-*.json` with `CORRECTION`
   supersession applied and `REMOVED` respected: **722 paths**, plus 2 recorded
   as removed.
2. Everything this branch changed, `git diff --name-only d3833d02..HEAD`:
   **9 paths**, plus this file.
3. The intersection with the governed set: **6 MODIFIED**. The other 3 have never
   been recorded and are **CREATED**, by the precedent `OVR-000472` set when it
   added eight existing documents to the set the same way. This file is the
   tenth, **CREATED**, with `after_digest` the literal placeholder the sealing
   step re-derives.
4. **10 documents**, one entry, under the cap of 20.

Nothing else qualified. `pyproject.toml` did not change: its `include` list
declares no new file and its `testpaths` names `tests/contract_compiler` as a
directory rather than the new module, so the new test file needs no entry there.
`ROADMAP.md`, `head.json`, `status.md`, `design/contract_compiler/overseer/entries/`,
`paper-v4/` and `.claude/skills/` were not touched, by the brief.

One of the two migrated runners, `content_rules/run.py`, is `CREATED` rather
than `MODIFIED`: it has never been recorded in the ledger, while
`shipment_policy/run.py` was, at `OVR-000473`. That is a finding about the
ledger's coverage, not about this change.

The block below validates against
`design/contract_compiler/overseer/ledger.schema.json` with
`Draft202012Validator` and a `FormatChecker`, substituting
`sha256:0000…0000` for `entry_hash`, for the placeholdered `after_digest` and
for the placeholdered previous hash, and a real UTC timestamp for the
placeholdered sealing moment: **1 of 1 valid, 0 errors**. The probe reads the
fenced `json` blocks of this file and finds two, of which exactly one parses as
an object with an `entry_id`. `why` is 1170 characters, under the 1200 cap;
`summary` is 163, under 240.

Proved end to end in a scratch copy of the repository, hardlinked so every
governed document is the exact byte this branch holds, with the entry inserted
at the real previous hash and `head.json` advanced to 477.
`python scripts/contract_compiler_ledger.py render` then `check` reports,
verbatim:

```text
validated 477 entries; head OVR-000477 sha256:30f5c38a809c50c9df0859cf6ed516d649896134686961b01d328905816622b0
```

That run reaches the real Git ancestry read-only, so the three evidenced commits
are checked for durable reachability rather than assumed. It binds this file as
it stood immediately before this paragraph was written; the entry records
`<digest of this file once final>`, so sealing re-derives it and the head hash
above moves with it. The real worktree was never written to.

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
        "after_digest": "sha256:ce005ed65084dec9482092366f586f0a56b62a89992e8e824c23b90360e0c966",
        "before_digest": "sha256:71ee0e48be085c1e75af6658df40719c1b7b1cff933a11f6b731c9840bf696ee",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:53a62bb6ddbcf6ea2e0e69db9174b157455323575d5fd44b6c6d3358910c78fe",
        "before_digest": "sha256:09feedab1dac003c5ec959ef0367f603070e3c544a5346b9a678320cb5b4d137",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:c57886e015154ed164c7f65b5cdae52f0e14725d6ccfa9051a5264bde9ec2e75",
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
        "after_digest": "sha256:d28447a7cbf9ef05c6c51217675fc6376e49a83adc669d96acb88fe41c7145a1",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/gap_answer.py"
      },
      {
        "after_digest": "sha256:65dfd2c6a11d18aaa59ee92f77b88c2ebbcd4cc1d270fd2106f162a1f5a81254",
        "before_digest": "sha256:0d4fa887438300337891684bb7e4d0c63d561d2cb99de5655b635498ac5f801c",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/knowledge.py"
      },
      {
        "after_digest": "sha256:5dd1677d19b5b73f9aa763843a142b86278a51d54fa4adf03fd704fccc20121f",
        "before_digest": "sha256:5fc3a0253da35bb37c10379c54ad0b4cafcad8593e922f49c07c7cae4d880b5e",
        "change": "MODIFIED",
        "path": "src/malleus/compiler.py"
      },
      {
        "after_digest": "sha256:aecb3fd93cfba0eeaae7f9b8be89640ff906cef887318a8ccec5e10404a2fed1",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_ontology_gap_answer.py"
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
  "summary": "ROADMAP F2: a declared ontology gap becomes an open question with one recorded answer, a proposal checked at retention, and acceptance that is the revision itself.",
  "why": "Luis, 2026-09-21, go. TYPE_ABSENT and RELATION_ABSENT were retained as a gaps artifact and nothing consumed them. A gap now has an identity derived from the bytes it identifies, the digest of the canonical {gap, plan_id} object, so a gap re-declared in a later plan is a new gap. A malleus.ontology-revision-proposal/v1 record names the gaps it answers and carries the exact target contract artifacts; retention is the check, so whichever door retains the bytes refuses an unknown gap, an answered gap, a gap of a non-ontology kind, or a composition that is not purely additive under the existing CONTRACT_REVISION_POLICY, and writes nothing. accept_ontology_revision_proposal composes the revision from the proposal's own bytes and appends it with one malleus.ontology-gap-answer/v1 record in one ledger batch, and the fold refuses an ACCEPTED answer whose revision is not recorded, so a proposal is never accepted without being applied. refuse_ontology_gaps closes gaps with a reason and moves no ontology. open_gaps is the report. No change kind was added and the gaps artifact is read and never written, so no frozen digest, receipt or accepted-state identity moves."
}
```

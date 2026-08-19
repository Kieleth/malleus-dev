# Roadmap

Candidates for later grooming. Nothing here is committed work. Each item
records what earned it, so that grooming can weigh evidence rather than
enthusiasm.

Two standing rules govern promotion into this file and out of it:

- **A concept promotes on the second consumer, not the first.** One project
  wanting something is a local solution; two independent projects wanting it
  is shared vocabulary. Designing a general API from a single example
  produces an API shaped by that example's accidents.
- **Rites for capabilities malleus does not provide enter at NOTE with
  `status: open_question`, never at HERESY.**
- **An accepted rite names its id here and exists in the rubric.** A section
  carrying a `Rite:` line whose id is absent from `rubric.yaml` fails the
  suite. Five accepted rites once sat here for a release while the code fixes
  shipped without them, so the lesson an adopter paid for never travelled back
  to anyone else. The loop is only closed when the rite ships. Condemning adopters for lacking
  what we do not offer is the defect three self-inquisitions removed from our
  own documents.

---

## A. From adopters, via the upstream channel

Lessons sent up by an adopting project, already written project-free. Source
document held locally by that project; only the generic lesson travels.

### A1. Per-instance reader coverage (refines `reader_census`)

Rite: `instance_reader_coverage` (landed, rubric v8)

A reader census is satisfied by one reader touching one instance, so a type
can be read once, extended with a hundred new instances, and stay green while
none of the hundred is reached. Reported case: two dozen rows, every row
cited to its source and counted by an invariant, referenced by exactly one
thing in the repository, which was the generator that wrote them. A
neighbouring path reached the same content through a side door, so the type
had a reader and the census was clean. Found by auditing output; no gate saw
it.

Proposed severity is conditional, and the condition is good: SUSPICION where
unread data means wasted storage, HERESY where the graph is the program,
because unread rules are absent behaviour rather than dead weight.

Two mechanical discharges, catching different amounts: a static walk from
entry points (cheap, blind to side doors, which was 17 of 23 in the reported
case), and a runtime journal of touched ids plus a sweep (complete, costs a
journal).

**Verdict: accept as a rite.** Groom the severity condition.

### A2. Fidelity, coherence and consequence are three claims

Rite: `claim_kinds_distinguished` (landed, rubric v8)

Projects conflate them because they are all "the checks pass". Fidelity: the
data matches its source. Coherence: the assembled graph is well-formed.
Consequence: the system acts on it. A project can hold the first two to an
unusually high standard and have no vocabulary for the third, and the
strength of the first two is what makes the absence invisible.

**Verdict: accept at NOTE.** Needs a `status:` field to load under rubric v7.

### A3. A declared-unread annotation

Rite: `unread_declared` (landed, rubric v8)

Schemas commonly have a slot for a partially expressed rule. There is no
mirror for a record that is fully expressed and never invoked. Without a
declared-exception slot a coverage gate has two settings, pass and nuisance,
and the second gets it switched off. With one, the gap is a countable set of
argued exceptions instead of a silence.

**Verdict: accept at NOTE.** Pairs with A1; groom them together.

### A4. Guidance newer than runtime

Rite: `guidance_newer_than_runtime` (landed, rubric v8)

A resolution order that tries the installed package first and a local
checkout second degrades in the dangerous direction: the fallback is not
equivalent, it is newer. The adopter reads the current rubric and protocol
docs while running a package several minor versions old. Reported as an
`ImportError` from a bootstrap step against an installed 0.1.0 with a 0.6.0
checkout beside it, the symbol having been added in between. This is
`root_currency` inverted, and worse, because that rite compares two copies of
the root while this compares documentation against code and nothing diffs
them.

Concrete fix, small: make the version a first-class output of the bootstrap
step. `malleus-inquisitor` already prints the rubric path, version and
digest; it should also print the installed malleus version and the resolved
bundled root, so one command answers "which root am I actually running
against" and a stale install announces itself.

This is one leaf of B3. A bootstrap version line detects one mismatch; an
execution bundle commits the complete code, schema, data, producer, runtime,
interaction, and budget combination used by an executable stage.

**Verdict: accept the rite, and do the CLI line soon.** It is one line and it
closes a confusing first-contact failure.

### A5. Unknown-range blast radius (highest value in this batch)

Rite: `unknown_range_blast_radius` (landed, rubric v8)

Three defects, one root:

1. The loader's range allowlist is five names where the schema language
   defines nineteen. The missing fourteen include the double-precision float,
   the decimal, the date and the URI, which are the ones an adopter reaching
   for precision uses first. Rejecting a legal built-in punishes an adopter
   for using their tools correctly.
2. Construction is rite one and a failed rite one short-circuits the run, so
   one unrecognised name silently blinds every later rite on that file and on
   every file importing it. Reported: five files of thirteen failed to
   construct, and seven of eight mechanical rites had therefore never
   executed anywhere in that repository, with nothing in the report saying so.
   Construction failure should report the rites it prevented.
3. **The tool manufactures findings against correct schemas.** Run without
   `--map` on a schema importing a sibling, it reports "does not construct",
   indistinguishable in the output from a real failure. Twelve schemas
   appeared broken and none were. Either resolve sibling imports relative to
   the inspected file by default, or say `CANNOT INSPECT` rather than
   `HERESY`.

**Independently corroborated.** A second, unrelated project lost its schema
to the same allowlist gap on `uri` in the same week. Two projects, one hole,
found separately.

**Verdict: accept all three, highest priority in this file.** (3) first: an
adopter's first run is exactly when they cannot tell a manufactured finding
from a real one.

### A6. Provisional concepts (feature, not just a rite)

Rite: `provisional_declared` (landed at NOTE, rubric v9)

Documents introduce terms before defining them; that is normal prose, not a
defect in the source. A knowledge system with no provisional state offers its
writers three moves and all three are bad: invent the definition, refuse the
passage, or store an unresolved string and promise to fix it later. The third
gets chosen because it is the only one that lets the ingest continue, and it
reintroduces magic strings under a name nobody is watching.

The proposal: a typed provisional status that is addressable and
referenceable, that names the source location forcing it, that no executable
path may consume, and that is cleared only by a definition being found and
judged. Lewis's rule of accommodation is the formal ancestor, and the
objection clause is the part a knowledge system has to supply.

The trap, correctly identified by the proposer: reference counting may rank
the backlog and must never settle a concept. A concept referenced forty times
and never defined is the most important open question in the ingest, not
thereby defined. Promotion by accumulated weight rebuilds a half-open gate on
precisely the entities the graph leans on hardest.

Distinct from staging: staging asks whether a claim has been assented to;
accommodation asks whether a concept is fully known. A staged claim about a
settled concept and a committed claim about a half-known concept are
different states.

**Verdict: the design deserves real consideration; the rite does not enter at
HERESY.** As proposed it would condemn every adopter for lacking a capability
malleus does not offer, which is the exact defect rounds three through six
removed from our own documents. Either the capability lands first, or the
rite enters at NOTE with `status: open_question` like
`module_declares_its_interface`.

---

### A7. The version marker makes "superset" unreachable (confirmed here)

Reported through the upstream channel and reproduced against the shipped
registry before acceptance. `strict_fingerprint()` carries
`fingerprint_version:N` as an ordinary member of the fact set, and
`check_compatibility_strict` answers by plain subset test. A project that is a
strict structural superset of a legacy root, and that uses a feature lifting
its marker from 3 to 4, therefore differs from that root by one fact in each
direction. Neither set contains the other, so the answer is `divergent` no
matter what the structures actually say.

```text
newer project asked about the legacy root    -> divergent
same pair with the version marker normalized -> superset
```

The reporter proposed normalizing the version before the subset test, and that
is the right shape: the marker describes which fingerprint grammar produced the
set, so comparing it as though it were a structural fact asks the wrong
question. The version relationship still has to be judged, separately and
explicitly, rather than dropped.

Cost of leaving it: `root_currency` is a HERESY rite and it consults the strict
consumer-side check, so an adopter whose root is genuinely current is told it
is divergent and cannot get a seal. Reported blocking a release pipeline whose
gate runs the full suite.

**Verdict: accept, and it precedes the other upstream work.** A rite that
condemns a correct schema is worse than a missing rite.

### A8. Content-hash semantics changed between releases with no migration path

Reported, not yet reproduced here. A content hash that has been written into
accepted append-only ledgers is a public contract, because the ledger cannot
be rewritten to match a new hashing rule. Changing the rule between releases
leaves existing ledgers permanently unverifiable, with no supported way
forward.

Two possible shapes and they are not equivalent. Hash stability, meaning the
rule may never change once a release has written it. Or a first-class migration
receipt, a typed record binding the old identity, the new identity, the rule
that changed, and the exact boundary event, so a ledger can carry both and say
which applies where.

Related and already accepted: `historical-timezone-database-migration` in the
not-implemented list is the same problem for a different stored value, and
`FINGERPRINT_VERSION` at 4 with a legacy 3 is the same problem already
half-handled for a third.

**Verdict: accept for grooming. Reproduce first.** The reported symptom is
consistent with A7, so part of it may be A7 wearing a second face. Establish
which before designing a migration record.

---

## B. From our own use

### B1. A commitment-lifecycle facade

Measured on a real adapter that drives one proposal through the full
lifecycle: **644 lines of generic lifecycle against 105 lines of domain
content.** The generic part is artifact, source, graph-base, candidate,
monitor-specification and policy construction, proposal-member assembly,
state transitions, and accepted-graph application. `AssentPlan` (0.8.0)
orchestrates the monitoring step and leaves the stages either side of it to
the caller.

The pain is real and it is the same class that earned `get_relation`,
`export_records`, `from_records` and `schema_version`. It is also the class
our own doctrine lists under default exclusions ("orchestration layers"), and
promotion needs a second consumer.

**Verdict: do not build in core yet.** Let the pattern be extracted locally by
its user, and revisit when three adapters exist and the shape has stopped
moving. Design the facade from three examples or not at all.

Design under grooming: `design/COMMITMENT_LIFECYCLE.md`. Three layers, a
four-slot adapter protocol, and explicit promotion criteria so the move to
core is a move rather than a rewrite. Note the survey behind it: level 5 has
no consumer outside this repository, so the abstraction axis is
benchmark-to-benchmark, not application-to-application.

### B2. Make a construction failure report its blast radius

Same as A5 (2), reached independently: a report that shows one heresy per
file and says nothing about the seven rites it skipped invites the reader to
conclude that everything else passed.

**Verdict: accept, groom with A5.**

### B3. Content-address the complete execution combination

The paper pilot and the retained benchmark harness independently need one
identity for a combination currently scattered across commits, package
versions, ontologies, rules, corpora, producer settings, prompts, tools,
runtime dependencies, condition definitions, and budgets. A package version
or model alias alone cannot identify the executable system.

The adopted design is `design/EXECUTION_BUNDLE.md`. Each executable stage gets
one immutable `ExecutionBundleManifest`; any material input change creates a
new digest. The feasibility pilot and final experiment therefore have
different roots. A later authorization names one exact digest rather than a
mutable set of filenames and version strings. The authorization also names the
stage gate-record digest plus the exact bundle `SourceArtifact` and ledger
record identities, so the portable content identity and one concrete protocol
registration remain distinct and cross-checked.

The first implementation stays in the research harness and records canonical
bundle bytes as a Malleus 0.9.0 `SourceArtifact`. It preserves the public
boundary: core commits caller declarations but does not authenticate bytes,
providers, licenses, hidden inputs, or actual execution.

The active paper binds Malleus 0.9.0 as its executable core and Malleus 0.10.0
Recon as separate literature tooling. Recon is not a paper execution-bundle
component. A later core migration requires its own author decision and renewed
G3 review even when the newer package contains byte-identical assent code.

The reserved core type is `ExecutionBundleArtifact`. Do not add it to the
assent ontology from this roadmap item alone. Promotion requires explicit core
authorization, exact historical-ontology replay policy, a second non-paper
consumer, and renewed protocol, API, fingerprint, and replay review. The paper
must not silently rebase from its frozen 0.9.0 substrate.

**Verdict: accept the shared design and paper-local implementation path. Core
implementation remains a separately authorized change.**

### B4. Cost-aware producer orchestration around commitment control

Status: `open_question`.

The evidence review in
`research/cost_aware_model_architecture_recon` asks whether a cheaper producer,
typed external memory, deterministic checks, one bounded repair, and selective
escalation can lower expected cost at matched reliability. Published systems
report conditional savings from routing, task-specific harnesses, reusable
memory, and executable checks. They also show that escalation overhead,
incomplete verification, stale memory, orchestration failures, and fixed setup
cost can reverse the result. No reviewed evidence establishes the complete
lifecycle claim.

The candidate boundary keeps model selection outside Malleus. An external
scheduler chooses a producer or escalation path. Malleus receives a proposed
transaction, runs the declared checks, records witnesses, derives a
fail-closed decision, and retains replayable accepted or unresolved state. A
study contract may permit at most one linked diagnostic revision. Core does not
schedule calls, manage memory, or claim a cost advantage.

The current paper is one prospective consumer and tests only the commitment
layer with a fixed producer and fixed generation budget. A literature corpus is
not a second consumer. Do not add routing, memory management, or escalation to
core from this item alone.

Any three-tier study is a separate follow-on after a valid
`P4_FEASIBILITY_REVIEW`, not an extension of the current P2 attempt. The choice
to compare small, medium, and strong producer tiers is an experimental design
decision, not a finding from the Recon corpus. That follow-on requires a new
claim and estimand, a new contract, a separate execution-bundle root, and its
own author authorization. It must not reuse the inspected P2 identity or treat
P2 feasibility evidence as a tier-comparison result.

After a valid P4 review, retain the pilot result as project study evidence in
a separate experimental-evidence graph. Do not append it to or rewrite the
Recon literature KG. A later contract may reference both immutable roots while
keeping reviewed publications and project-generated measurements distinct.
Invalid or halted pilot roots remain provenance evidence only.

Promotion requires a second non-paper consumer and a controlled study against
strong-only, medium-only, small-only, simple-routing, and cheap-first-cascade
baselines. The study must count setup, calibration, calls, tokens, latency,
monetary cost, storage, adapter work, unresolved coverage, human intervention,
recovery, and drift maintenance. A cost claim fails if the strongest simple
baseline wins at the prespecified risk and coverage points.

The bounded synthesis and candidate paper motivation are in
`docs/COST_AWARE_MODEL_ARCHITECTURE_RECON.md`.

**Verdict: retain as a measured research question. No core implementation or
paper outcome claim is authorized.**

---

## C. OCR evidence-integrity profile

Profile-local work. Not core capabilities and not rites: these are defects and
gaps in `malleus.ocr` itself, found by probing the verifier rather than by
reading it.

### C1. Conditional requirements the schema states and does not enforce

Four probes were run against a conforming bundle with one field changed. All
four were accepted. Three are defects and one is not.

**Defect: an unavailable attempt need not say why.** `status="UNAVAILABLE"`
with no `unavailable_reason` verifies clean. The slot's own description in
`ontology/domains/ocr.yaml` reads "Required reading when status is
UNAVAILABLE". A schema that states a requirement and does not perform it is
the same class of defect as a document claiming a capability the code lacks,
which three self-inquisitions removed from our own prose. Discharge: a LinkML
class expression, since `OntologyRegistry._validate_class_expressions` already
evaluates them, so this needs no new mechanism.

**Defect: a correction can say CORRECTED and supply no correction.**
`verdict="CORRECTED"` with no `corrected_text_digest` verifies clean. The
record asserts a different reading was produced and does not carry it. Two
discharges, and they are not equivalent. Requiring the digest to be present is
cheap. Requiring it to equal the `text_digest` of the hypothesis carrying that
`correction_id` is stronger: it asserts the two planes agree about what the
corrected text is, and catches a correction whose digest and whose resulting
reading have drifted apart. Groom which.

**Defect, weak: mandate B3 is recorded and never checked.** A correction whose
`reviewer_id` equals the model identity in the attempt that produced the
reviewed hypothesis verifies clean. B3 says a separate reviewer is an identity
that did not produce the hypothesis under review. The bundle carries both
identities today, so an exact-string check is possible without
`protocol-actor-registration`. It catches only exact equality, which raises a
real question before it is built: a check that catches the naive case and
nothing else may read as enforcement and be worth less than an honest absence.
Decide that before writing it.

**Not a defect: a completed attempt need not retain a response.**
`status="COMPLETED"` with no `response_digest` verifies clean, and that is
correct. Decision C6 retains the raw response under the adopter's declared
retention rule, so an adopter whose policy is no retention is right to omit
it. Recorded here because closing it looked obvious and would have contradicted
an owner decision.

### C2. Dependency-closed partial claims (decision C2, unbuilt)

The largest unbuilt piece of the profile and the reader `required_units` is
waiting for. `required_units` is declared in the schema and consumed by
nothing, recorded there as declared-unread rather than left silent.

Needs, each with fixtures: a frozen required-unit inventory, a map from claim
to the units its evidence occupies, a map from claim to claim, transitive
closure over both, cycle detection, and replay semantics so the same bundle
re-verified yields the same partial set.

### C3. No adapter has crossed the boundary

Established: an emitter that imports no plane class and touches no dataclass
builds a bundle document by hand and conforms, so the emitter role is
replaceable. Not established: that a production OCR stack fits. The profile
does not claim portability and must not until an adapter passes.

### C4. The verifier walks lineage only from readings

Found by an independent investigation into whether another subpackage could
be the profile's first adapter, then reproduced directly. Three bundles, each
granted a purity seal:

1. A `Region` naming a raster the bundle does not carry, with no hypothesis
   referencing that region.
2. A `Raster` naming a source the bundle does not carry, with no hypothesis
   referencing it.
3. A bundle with one source, zero regions, zero attempts and zero readings.

The cause is one loop: OCR-D003 walks hypothesis to region to raster to source
and nothing walks the planes that no reading reaches. An orphan plane is
therefore unexamined rather than refused.

The third case is the one that matters, and it is not a cosmetic gap. The
profile's open claim is that it becomes portable when the first adapter passes
the suite. An adapter that emits a source and no readings passes today, so
that milestone could be reached without a single reading ever being verified.
A rejection rate of zero is not evidence of a gate.

Discharge: check every plane's references regardless of what points at it, and
decide separately whether a bundle carrying no readings is a conforming bundle
or an incomplete one. The second is a judgement about what the profile is for,
not a bug fix, and it wants an explicit answer rather than a quiet threshold.

### C5. Recon's classification vocabularies are ungoverned

Adjacent finding from the same investigation, verified against the live
ledger. `claim_kind` and `coverage_maturity` in `ontology/domains/recon.yaml`
are `range: string`. One project's ledger carries 78 distinct `claim_kind`
values across 121 claims, 59 of them used exactly once. This is not
`constrained_tongues`, which governs `event_type`, `relation_type` and
`signal_type`, so no rite fires. It is the same disease in a slot the rite does
not name: a classification field that classifies nothing, because a vocabulary
where half the values appear once is free text with a schema slot around it.

Belongs to recon rather than the OCR profile, kept here so it is not lost.

---

## D. Recon: standing on the root instead of beside it

Recon answered a problem the root has no answer for, locally. That is not
disobedience, because malleus does not offer the capability either, and it is
exactly the case where the requirement travels upstream first and recon
consumes it afterwards. Nothing here is discharged by recon alone.

Two facts frame the section. Recon's schema takes a purity seal today, and
that seal covers the 9 mechanical rites; the other 29 are judgment tier, are
declared rather than implemented in `rubric.yaml`, and have never been run
against recon by anyone. Separately, two of the defects below are named by no
rite at all, so even a complete inquisition would walk past them.

### D1. No provisional-concept state (blocked on core)

`ComparisonAxis` requires `axis_definition`, and requiredness does not vary by
review state. Verified: an axis in `PROPOSED` with no definition is refused, and
so is one with an empty definition. A claim may be staged with no evidence; a
concept may not be staged at all without its definition.

Recon does not need this today, because a human reads the paper and authors a
defined axis. Five relations in the live ledger record that a source does not
define something, and in every one the axis exists, fully defined by the
reviewer, with the gap recorded on the coverage edge as `PARTIAL` or
`NOT_ESTABLISHED` plus prose. The under-definition lands on the edge, never on
the concept.

The moment the ingest reads source text rather than a reviewer's summary, that
stops working and A6's three bad moves are the only ones left. Depends on the
A6 capability existing in core. Recon is the consumer that motivates it.

### D2. Classification vocabularies are free strings

Rite: `classification_is_closed` (landed, rubric v9)

`claim_kind` and `coverage_maturity` are `range: string`. One project's ledger
carries 78 distinct `claim_kind` values across 121 claims, 59 used exactly
once. `constrained_tongues` governs `event_type`, `relation_type` and
`signal_type`, so no rite names these. A vocabulary where half the values
appear once is free text with a schema slot around it.

### D3. No media type on an evidence attachment

`EvidenceAttachment` has no `media_type` slot anywhere in recon. The OCR
profile's `SourceRepresentation` requires one. Blocks the one plane recon
could otherwise populate.

### D4. Source bytes are declared, not computed

`artifact_sha256` and `artifact_byte_length` are optional and must be supplied
together. Filled on 14 of 255 attachments in one project and 3 of 59 in
another. Recon preserves caller declarations and computes nothing from bytes,
which `docs/RECON_CONTRACT.md` states openly and names as future adapter work.
Recon's digest pattern is byte-identical to the OCR profile's, so the two
already agree on the shape of an identity and disagree on who produces it.

### D5. Position is prose

`locator` is free text: "pp. 312-313, §6 Evaluation", "Entire file at commit
384ecc3". Of 255 attachments, 25 mention pages, 31 mention sections, 197
neither. No page, span, offset or coordinate is a typed slot. Blocks `Region`,
and `Region` is where the OCR selector profile would carry the work.

### D6. No extraction provenance

No model, prompt, config, attempt or provider identity is recorded anywhere.
`SearchEvent` records the act of searching, not the act of reading. Blocks
`OCRAttempt` and `Hypothesis`, which is to say it blocks every plane the
profile exists to verify.

### D9. Recursive ingestion by pointer is blocked by the same refusal as D1

Wanted: ingest a URL, a GitHub repository for example, discover what it points
at, and ingest that too, recording each pointer as an edge so the graph grows
as the discovery does.

The graph can hold the result. Nothing performs it, and the write path refuses
the intermediate state. Demonstrated against the shipped registry:

```text
A cites something not yet fetched -> REJECTED | Target entity does not exist
same edge, after inventing a stub -> COMMITTED
```

`kg.py:317` refuses a relation whose endpoint entity is absent. So the pointer
edge cannot be recorded until the pointed-at thing is a full record, and a
`Work` requires `label`, `title`, `priority_date_basis`, `publication_status`
and `review_state`. A discovered URL therefore forces four inventions, and the
invented stub commits with no rejection and no mark. `Work` has no URL slot at
all; the URI lives on `EvidenceAttachment`.

This is D1 wearing different clothes. A pointer seen and not yet fetched is
addressable, is referenced, names the source location that forced it, must not
be consumed by any executable path, and is cleared only by the thing being
fetched and judged. That is A6's description word for word.

Consequence for promotion: A6 now has a second consumer, the pointer frontier,
which is independent of the provisional-concept case that motivated it. The
roadmap's own rule, that a concept promotes on the second consumer and not the
first, is satisfied.

Still open even with the capability: the frontier needs a stopping rule, and
dedup by content address across pointers that resolve to the same bytes.
Neither is a graph question.

### D7. `confidence` means opposite things in the two schemas

Recon's `confidence` is the reviewer's, required on every relation. The OCR
profile's is provider-reported and explicitly barred from controlling
acceptance, because confidence without calibration cannot. Two schemas about to
meet, one word, two meanings. Resolve before they meet, not after.

Direction taken: the concept is solved in core, with an override available to
anyone who needs a different one. These two are malleus modules rather than
third-party adopters, so they harmonize on the core definition rather than each
keeping a local one. An adopter outside malleus may still override.

### D8. No verbatim source text is retained

`statement` is a reviewer paraphrase and `evidence_description` is a summary.
Nothing holds the bytes a claim came from. `quotation_is_byte_exact` is a
HERESY-tier rite and `citation-byte-verification` is an unimplemented core
capability, so this is the same gap seen from two sides. Recon does satisfy
`citation_integrity`, the companion rite: a cited id must resolve, enforced at
replay and at final-state validation.

### Dependency order

Upstream before recon, and within recon, planes before the things that stand
on them.

1. OCR C4, the lineage walk. Until an empty bundle stops taking a seal, no
   adapter passing the suite means anything, including recon.
2. OCR C1, the conditional requirements the schema states and does not enforce.
3. D7. One word, two meanings, cheapest to fix while nothing depends on it.
4. D3 and D4 together. They complete `SourceRepresentation`, the one plane
   recon nearly has.
5. D2. Independent of the OCR work, and it is the ontology sanitization.
6. D5, then D6. `Region` before the readings that select over it. Both need a
   document-reading pipeline that exists nowhere in the repository today.
7. A6 capability in core, then D1 and D9 together.

D9 moved A6 up rather than leaving it last. URL and pointer ingestion is
blocked on the same capability as provisional concepts, so building the
fetcher before the capability means building the stub-inventing path first and
removing it afterwards.

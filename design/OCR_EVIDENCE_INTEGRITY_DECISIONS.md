# OCR evidence-integrity profile: decision record

Decision ID: `OCR-D001`
Status: accepted by the author on 2026-08-18
Governs: the upstream candidate `MALLEUS_OCR_UPSTREAM.md` v0 (3,109 lines,
reviewed at its 2026-08-17 evidence cutoff) and its 33 owner decisions.
Shipped capability: none. This record decides scope, not delivery.

The proposal put 33 decisions to the author. Ten were already forced by
repository facts, three by the author's own mandate, ten are internal to a
profile-local format that no adapter has stressed, and eight are decisions of
substance. Only the last group is recorded here as author choices; the rest
are recorded as findings so nobody re-litigates them.

## A. Forced by repository facts, not chosen

**A1. v0 is `AUDIT_ONLY`.** `EventType` has eleven members and not one carries
a `ReviewReport`; `review-report-recording` remains on the not-implemented
list. Human review and correction is the centre of this profile and it has no
door into the protocol ledger. Separately, the `ASSENT_INTEGRATED` target named
in proposal decision 26 does not exist: the temporal representation is
mid-flight in an unlanded worktree, and PyPI carries `0.9.0`, `0.7.0`, `0.1.0`.
Neither `0.8.0` nor `0.10.0` was ever published, so the proposal's reference to
a "shipped `0.10.0` and Assent `0.8.0` baseline" is factually wrong and must be
corrected before acceptance.

This settles proposal decisions 5, 12, 13, 16, 18 and 26. Each bites only if
v0 touches Assent, and v0 cannot.

**A2. Nothing new enters core.** *(Landed: the profile ontology is
`ontology/domains/ocr.yaml`, importing the root and adding nothing to it. It
was written a release late. v0 shipped with the planes as Python dataclasses
governed by no schema, which is the defect `root_has_speakers` and
`instance_reader_coverage` both name, in the module that shipped alongside the
rubric carrying them.)* Replaceability is empirical and no adapter has
crossed the boundary. `StageExecutionDeclaration` and `StageExecutionRealization`
stay profile-local (17), the new graph vocabulary lands in the profile's own
ontology rather than the root (31), spatial data and raw responses are
content-addressed artifacts rather than graph records (2), and a
`malleus.ocr` core module waits for stable mechanics (8).

**A3. The two audited adopters are design evidence, not conformance evidence.**
Neither has implemented the profile. The profile may say it was designed from
two audited adopters. It may not claim portability until an adapter passes the
corpus. This settles decision 7.

## B. Already answered by the author's mandate

**B1** (decision 10). Confidence without calibration cannot control acceptance.
**B2** (decision 15). Verified blank, unreadable, unavailable, failed, excluded
and absent stay distinct; none may be padded, snapped or converted into
another.

*(Landed late, and the delay is the lesson. The six states were distinct in the
schema from the first release and the census that consumed them was not:
`ABSENT` had no branch, so a reviewer stating that a unit is not present in the
source got the unit reported `READ`. Absence converted into a reading, which is
this mandate's exact prohibition, under a clean verdict and a met coverage bar.
Nothing caught it because nothing read the outcome vocabulary: it was a module
tuple with no consumer, and a vocabulary nobody consults cannot report that one
of its values is unreachable. The vocabulary now lives in the schema as
`UnitDisposition` and three outcome enums, `malleus.ocr.verify` reads the
mapping from there, and a test requires every declared outcome to have a
fixture proving a bundle can produce it. The census answer is also three-valued
now rather than the single `accounted` bit: a unit nobody fetched and a unit
whose only call failed were one word for two different repairs.)*

*(Second correction, from the review of the first. The census reports one
outcome per unit, a unit may carry several verdicts, so something has to
choose, and a hardcoded precedence tuple was choosing in silence. Two of those
choices were the prohibition again: a unit whose regions carried both
`VERIFIED_BLANK` and `ABSENT` reported `ABSENT`, and `UNREADABLE` beside
`VERIFIED_BLANK` reported `UNREADABLE`, each under a clean seal. A third was
worse and nobody had reported it: a superseded verdict outranked the review
that replaced it, so a reviewer revising `UNREADABLE` to `VERIFIED_BLANK` was
still reported `UNREADABLE`. C9 below splits the cases. Summarising a unit's
several regions is a stated scope rule with a published order; two live
verdicts about one region are refused as `OCR-D016`, because no summary of
those is anything but a conversion; and a superseded verdict no longer
speaks.)*

**B3** (decision 6). A separate reviewer is an identity that did not produce the
hypothesis under review.

## C. Author decisions

**C1. Standards are pinned at a swappable boundary** (decisions 11, 3, 25).
W3C Web Annotation selectors, PROV derivation and IIIF image coordinates are
the first-party default region profile. They receive no privilege, no hidden
field and no bypass. Any custom region layer replaces them by emitting the same
normative intermediate and passing the same conformance suite.

This is the `ContractFrontend` pattern already accepted for LinkML, applied to
selectors, and it is deliberately the same pattern rather than a second idiom.
Consequence: the coordinate, orientation, transform and multipage contract is
the specification's, not ours, which is why decisions 3 and 25 close with it.
Cost: the profile versions against external specifications and must declare
which profile of each it supports, fail-closed.

**C2. Missing required pages block promotion, with dependency-closed partial
claims** (decision 28). A claim whose evidence does not depend on a missing
page may promote, marked partial. Page-to-claim closure, claim-to-claim
closure, cycle detection and replay semantics all become normative and all
need fixtures. This is the most expensive decision in the record and likely
half of v0's specification work. It was chosen over block-only because real
corpora are incomplete and a rule that blocks everything gets bypassed.

**C3. Coverage is a precommitted per-source-class metric family** (decision 4).
The inventory is derived from the source and then explicitly confirmed or
overridden as a recorded act, so a truncated source cannot certify itself.
Section 11's nine families stand, extended with visual and semantic
completeness observations: ink coverage under the Coverage family, semantic
capture rate under Semantics. Families are selected per source class and
differ by domain.

**Guardrail, and the profile must state it.** The family selection, denominators
and thresholds are frozen before ingest. A metric set chosen after seeing the
scan is a metric set chosen to flatter it. Section 11 currently forbids silent
omission but does not say when the declaration freezes.

**C4. Temporal policy is declared per source class** (decision 14). No invented
defaults. Each source class states what its printed date means and whether it
can be ordered by valid time. An undated class is usable for content and
carries no timeline.

**C5. Privacy and hostile-content contracts are mandatory for conformance**
(decision 23). No adapter conforms without a bound declaration of data
classification, local versus remote processing, provider retention, encryption,
access, export, deletion and raw-response policy, plus a hostile-content
isolation hook. The profile enforces that the declaration exists and is bound.
It never enforces what the declaration says. Document text is untrusted data
everywhere: it cannot alter prompts, tools, policy, ontology, permissions or
execution instructions.

**C6. Credentials never enter the bundle** (decision 22). The bundle binds exact
request semantics, prompt, config, model and tool identity, and the raw response
under the adopter's declared retention rule. No key, token or authorization
header is recorded, and preflight refuses when one is detected. Consequence,
stated rather than discovered: a request cannot be replayed byte-for-byte
against a provider without out-of-band credentials.

**C7. Staleness is two properties, not one** (decision 9).

*Invalidation* applies only to source and render bytes. Prior readings describe
pixels that no longer exist and are void.

*Currency* applies to prompt, model, ontology, mapping and policy. Prior
readings remain valid observations of the same bytes and are demoted from
current, which triggers re-review without destroying anything.

The author's instinct was that every listed change should matter, and it does.
Collapsing them into one flag would have made engine comparison impossible,
because the older reading would be stale by definition while section 11's
metric families exist precisely to compare routes and engines. The two planes
already exist in the mandate as `hypothesis` and `selection`.

Consequence: "which reading is current when three exist" becomes an explicit
selection rule with its own fixtures.

**C8. One object carries C2, C3 and C4.** Required-page inventory, coverage
metric families and temporal policy all vary by class of document and all must
be frozen before ingest. That is one declaration per source class, not three
independent ones. The proposal has no single name for it and needs one.

**C9. `ABSENT` is a disowned rendering, not a missing one, and a unit's answer
is summarised from its regions by scope before severity.**

Accepted on 2026-08-20, after a review asked what `ABSENT` means when the same
bundle carries a rendering of the unit, a completed attempt over a region on
it, and a reading of those pixels. The reference case
`absence-is-not-a-reading.json` carries exactly that shape and verifies clean,
and the review's reading was that the planes contradict each other.

They do not, and the schema settles it rather than taste. `ReviewVerdict.ABSENT`
is defined as "the unit the region belongs to is not present in the source": it
is reached **through a region**. A correction reviews a hypothesis, a hypothesis
names a region, a region names a raster, and a raster names the unit it renders.
So a raster of the unit, a region on it and a reading of that region are not
evidence contradicting `ABSENT`; they are the mechanism by which a reviewer
points at what they looked at, and the profile cannot record `ABSENT` without
them. A rule refusing `ABSENT` in their presence would refuse it everywhere,
putting an unreachable value back in a closed enum, which is the defect this
release exists to remove.

What `ABSENT` therefore means: the renderer emitted a unit, the pipeline read
it, and a human states that what was emitted is not the required unit. A
scanner separator sheet counted as page 7. A duplicated page. A page the
renderer synthesised. The unit that was never rendered at all is
`NOT_RENDERED`, and the distinction between the two is the whole reason both
exist.

Consequences, stated rather than discovered:

- `ABSENT` outranks the region-scoped verdicts for the same unit. That is not
  a precedence convenience. It is scope: `VERIFIED_BLANK` is an answer about
  one region of a rendering that `ABSENT` says does not represent the unit, so
  it was never a unit-level answer to displace. `VERDICT_PRECEDENCE` in
  `malleus.ocr.verify` carries the order and `unit_verdict_precedence` in the
  published projection carries it to an adopter.
- Below `ABSENT` the three region-scoped verdicts rank worst-first, so a unit
  is `VERIFIED_BLANK` only when every region answer is blank. Summarising
  several regions into one unit is not converting one of the six into another;
  it is answering a different question from the one each region answered.
- Two live verdicts about the **same** region have no such story. Whichever the
  census reported would convert the other, which is mandate B2's literal
  prohibition, so the bundle is refused as `OCR-D016`. An adopter satisfies it
  by recording one terminal verdict per region.
- A review chain supersedes. `predecessor_id` is now read: a correction another
  correction names as its predecessor no longer speaks, so revising a verdict
  changes the census. Superseding is not erasing and the superseded record
  stays in the bundle. A chain with no earliest review is refused as
  `OCR-D017`, so reading supersession cannot make a verdict vanish quietly.

Reversible: delete the `OCR-D016` and `OCR-D017` blocks, stop filtering by
`_live_correction_ids`, and the profile is back where it was, with this section
recording what was given up.

**Excluded from this decision, recorded rather than closed.** A `Selection`
naming a reading of a unit a reviewer has declared `ABSENT` is not refused
today. That is a bundle both disowning a unit and keeping a reading of it
current, and it is a genuine contradiction, but it lives in the selection plane
rather than the verdict plane and no adopter has produced one. Roadmap C7.

## D. Accepted as proposed, revisited at the first adapter

Decisions 19, 20, 21, 24, 27, 29, 30, 32 and 33 concern the internal shape of a
profile-local bundle format that no adapter has yet stressed. They are
internally coherent, they are revisable without a core change, and choosing
differently now would be guessing. They are accepted as written and reopened by
the first conformance run that contradicts them.

## E. Corrections required before acceptance

1. The "shipped `0.10.0` and Assent `0.8.0` baseline" claim is false. Published
   versions are `0.9.0`, `0.7.0`, `0.1.0`.
2. Section 11 must state when the metric declaration freezes (C3).
3. The source-class declaration object needs a name and a schema (C8).
4. The staleness section must carry both planes (C7).

## F. Upstream defect recorded from the paper stream, 2026-09-05

**F1. Letter-spaced runs in PDF text layers are a damage class this profile
must handle.** The paper's frozen reading (pypdf 6.16.2, `PdfReader(strict=True)`
plus `extract_text()`, 186 blocks) carries a space between letters wherever the
PDF positions characters individually: a byline name arrives as
`S a t i s h C . S i n g h`, and 27 of the 186 blocks carry a run of five or
more spaced characters, almost all in the byline, the acknowledgements and the
reference list. A producer bound to verbatim capture cannot record such a name
without reconstructing it, and reconstruction is invention, so the paper cell
run-04 recorded 20 `REQUIRED_FIELD_ABSENT_IN_SOURCE` gaps for exactly these
spans and the manuscript declares the limit (section 4.5). Nothing in Core or
in the packs is wrong here; the damage is in the reading.

Recorded as an owner decision for this profile, not for the paper: the frozen
reading stays as it is, because every cell, manifest and review is pinned to
its digest. The pragmatic fix belongs to this profile's extraction path:
detect letter-spaced runs mechanically (a run of single characters separated by
single spaces above a length threshold is unambiguous in Latin text), keep the
text layer as one extraction candidate beside raster OCR, and reconcile a
damaged span against the other candidate before it enters a reading, recording
the reconciliation as an evidence operation with both candidates retained. A
span that no candidate renders legibly stays a gap. The threshold, the
reconciliation rule and its evidence shape are open until the first adapter
stresses them (section D applies).

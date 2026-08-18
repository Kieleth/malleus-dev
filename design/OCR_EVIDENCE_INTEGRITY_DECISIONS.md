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

**A2. Nothing new enters core.** Replaceability is empirical and no adapter has
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

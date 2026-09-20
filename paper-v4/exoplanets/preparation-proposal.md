# Next preparation cut: exact sources and explicit analytical choices

Date: 2026-09-14. Source conversion approved and implemented under EXO-007.
The remaining choices are proposals, not a launch packet or history policy.

## The concrete demonstration

Initially, the system retains what the earlier study reports and an identified
choice of inputs for our analysis. A calculation uses those inputs; an explanation
states what supports their use. After adding the later study, the system can
propose a different choice with reasons, without erasing either publication.
Replaying the earlier history must recover the earlier choice and calculation.
A change in choice is allowed, not required. Insufficient evidence must leave
the choice unresolved rather than manufacture progress.

Three different things stay separate: the publications' estimates, our decision
about which estimates to use, and the result of applying a declared calculation.
This is a scientific workflow representation, not a claim that the planet changed
or that the newer estimate is true.

## 1. Bind table values to native sources

Implemented: a small, deterministic VOTable-to-NDJSON projection, owned here.
NDJSON is one JSON object per line, a format Core's existing row-locator checker
reads. The original XML stays unchanged and remains the source authority. This
does not select a new archive response or revive the rejected CSV reader.

Keep original column names and decimal text. Preserve empty cells as null, never
zero. Preserve field definitions, units, published-solution references and exact
parent row/field coordinates in the projection's declared metadata. Identify any
selected row/column subset and its exclusions. One retained derivation description
binds parent bytes, selection, converter and outputs; do not create a manifest
for every cell. The reader must be able to follow a graph derivation back through
the projected field to its original XML cell and unit declaration.

Do not attach astronomical meaning in this converter. No planet ontology,
population records, preferred solution, density calculation or inferred relation.
The model still interprets the supplied material. Do not give the first producer
the all-reference archive or our investigator comparison. Current metadata in an
older study's row is not automatically safe for the earlier-stage packet.

FITS remains native. A separately identified header-only projection may expose
the selected target, instrument, processing and observation metadata, with exact
header-card locations. Bulk samples stay outside the graph. No assertion that
these are the authors' exact working bytes, or that a transit fit was reproduced.

Alternative: a native XML/FITS locator checker in this adopter. It avoids the
extra row representation but creates another lookup convention and still needs
the same parent-byte, unit and missing-value checks. Recommend the supported row
projection first because it reuses Core's existing locator boundary. Neither
option was authorized by the original proposal alone. Luis subsequently approved
the row projection under EXO-007; it is now implemented. The alternative and FITS
conversion are not implemented. See [source-packet.md](source-packet.md#converted-archive-rows-exo-007)
for exact outputs, tests and candidate column scope.

## 2. Settle history semantics without building another protocol

Requirements, independent of the eventual class names:

- Published solutions remain separate and attributable to their exact studies
  and fit locations. A later solution does not supersede an earlier publication.
- A choice identifies its purpose, exact selected inputs, responsible proposer,
  reason and supporting evidence. Its scientific assessment is separate from
  Core's structural acceptance. No fixed "newest wins" rule.
- Replacing a choice preserves the source records and every unrelated record.
  The previous choice remains recoverable. The adopter must test this allowed
  change boundary; generic structural admission does not select it for us.
- Observation time, publication date, choice time and import order stay distinct.
  Unknown domain time stays unknown. No timezone, midnight or historical snapshot
  is invented to fill a required field.
- Initial ontology acquisition remains source-grounded and question-withheld.
  Our analytical choice is not a fact asserted by either astronomy paper. Any
  later application-layer vocabulary must be identified separately and, if it
  needs an ontology extension, approved and recorded rather than handed to the
  initial producer as an answer-shaped schema.

The existing API has passed a small feasibility check: a source-assertion batch,
a state-version batch and a replacement state-version batch can share one
default structural history. Reopen preserves the statement and both historical
choice versions; only the replacement choice is current. Every saved prefix
reconstructs its recorded graph and receipt. A mismatched supplied profile
refuses without changing ledger bytes.

This is not yet the chosen composition. The shipped source-assertion profile
describes partial-import capture batches; state-version declares genesis over
an empty graph and domain-time semantics. Our probe shows that Core accepts
their per-plan identities, not whether both genesis declarations describe the
whole mixed history correctly. We have not established a per-stream interpretation
that resolves this. Do not infer it from successful tests or silently relabel
document-adapter output with another profile.

Before selecting the route, resolve whether these profile declarations describe
each batch or the containing history, and whether an existing explicitly defined
composition fits. If no existing contract fits, present the smallest domain-neutral
Core clarification/request with this probe. Do not ask Core to choose astronomy
semantics or invent a general framework. The clarification was sent to Malleus
Core under EXO-007 with the synthetic reproducer. EXO-008 records its answer:
the mixed probe does not establish semantic compatibility. One explicit adopter
composition profile is the smaller existing pattern, but the document adapter's
fixed source-assertion output cannot be silently relabeled. No implementation
was requested. The profile/producer-contract decision remains with Luis.

## 3. Deliverables and discriminating checks

| Deliverable | What must pass before we advance |
| --- | --- |
| Source projection | Exact retained bytes; original lexical values, nulls, units and reference identities; every projected field resolves to its parent; duplicate or ambiguous coordinates refuse; repeated output is identical. |
| Stage packets | Explicit source/row/column allowlists; changed selections refuse; later-study rows and current metadata cannot enter the first packet implicitly. Whole-file digests alone are insufficient. |
| Selected reading | One named reproducible reader, inspected prose order, tables and captions, stable block locators, and explicit exclusions. The older PDF's page-6 extraction defect stays open until resolved. |
| History route | Explicit origin, batch meaning, time and allowed replacements; a synthetic source-plus-choice example; refusal of an unauthorized replacement; old source records and earlier graph/results preserved. |
| Execution packet | Exact Core and dependency identities, model/input delivery, bounded feedback and source-grounded review rules; questions withheld from acquisition. The editable environment's metadata mismatch must not pass the launch check. |

Use tests first for new implementation, then the smallest change that passes.
The history probe tests existing behavior; it is not a new Core implementation
or a scientific experiment. No negative case may be called a Core refusal when
only an adopter check supplied that refusal. Retention before failed admission
may leave preparation evidence, even though accepted domain state is unchanged.

Completed under Luis's approval: mechanical source projection, table-stage tests
and the [PDF-reading investigation](READING-FINDINGS.md). The four tested reading
conditions trade different losses; none is a verified full reading. The report
proposes a bounded prose-and-table scope instead of a new PDF engine. Reading
scope, history semantics and the complete staged delivery boundary still need
decisions before launch. No astronomy population, new Core version, shared-paper
edit or manuscript claim follows from this work.

# Temporal first cut: Luis's rulings

One ruling per entry, in the order taken. DECISION.md holds the options.

## R-01, 2026-09-24: target naming (G1 OC-01, DECISION.md decision 2)

A transition and a correction always name the record they act on. Core infers
no target from subject, property or start time.

Luis: "correct, always explicit, enables full provenance/traceability, even in
the temporal domain."

## R-02, 2026-09-24: representation (DECISION.md decision 1)

Option A: every version is its own identified record in the one graph that the
semantic ledger produces. Grouping by membership records only where a case needs
a group. No second store: not SQLite, not a native temporal store, and not an
external index kept beside the KG. Anything Malleus holds is stored in the KG and
enters as semantic ledger transactions.

Luis: "yes, A, no second store, truly, anything needs to be stored in the KG
itself and as semantic ledger transactions, no external tools, otherwise keeping
them in sync is going to be a total nightmare"

Consequence: G2b (SQLite) stays as research evidence only. The "index under A"
option in DECISION.md is withdrawn as an external tool; any future speed-up must
be derived inside Core from the ledger.

## R-03, 2026-09-24: what a transition records (DECISION.md decision 3)

A transition closes its target's valid period at its own start, as Core does
today, and the history records that the closing kind was TRANSITION. The target
stays believed for its closed period. A correction records kind CORRECTION. The
current graph keeps today's meaning: records not replaced.

Luis: "correct, fully, indeed, next"

## Direction D-04, 2026-09-24: correction is general; the narrow rule is refused as a design

DECISION.md decision 4 (a correction covers exactly its target's period) is not
accepted as the design. A correction can apply to anything that belongs to an
entity in the KG. The design must not constrain by default what a correction
may change. A first cut may prove a narrow case, and the more complex corrections
go on the roadmap, but the shape is general. A correction may also need to ask
the KG what depends on the corrected thing and re-derive that part of the graph.
Paused for research before any ruling.

Luis: "a correction can apply to 'anything' that belongs to an entity in the KG,
therefore we should not prepare or constraint by default any application to a
correction, if we need to start small, so be it, and narrow proof of this, and
then we add to the roadmap other more complicated corrections, but as we design
and build this, we need to keep in mind this is just the start, and 'correction'
might need to query the kg for 'what things affect this specific correction
'here' and go and recalculate/compute that part of the KG'"

## R-04, 2026-09-24: one general correction, judged on its result (supersedes DECISION.md decision 4)

A correction is one change of kind CORRECTION. It names every target (R-01),
gives each a successor version in which any field may differ, records its kind
(R-03) and cites its evidence. Core admits it only if the resulting state passes
Core's checks. A first cut narrows by refusing results Core cannot yet reconcile,
each with its own typed reason and roadmap item (TYPE_CHANGE, VALID_TIME_EXTENT,
WITHDRAWAL, IDENTITY_MERGE_OR_SPLIT, HISTORICAL_USE_ENDPOINT,
CUSTOM_POLICY_HISTORICAL_SCOPE, ONTOLOGY_FACT), never by listing allowed fields.
A stale target (not the latest version of its line) is a permanent refusal with
its own reason. "Covers exactly its target's period" is no longer the definition
of a correction; it is the only valid-time outcome the first cut supports.

Luis: "a) for sure, track the why from this research and next"

Why, from CORRECTION-RESEARCH-01.md (commit a608f598):

- Core's limits on correction today come from specific checks, not from the
  record shape: type must match, one successor per record, valid time owned by
  the change set and required to start strictly later for INSTANT
  (knowledge.py 3365 to 3389), and incoming live relations block retirement
  (kg.py 169 to 184). Each can be lifted one at a time, so a general shape with
  per-category refusals is buildable incrementally. [code, probe]
- A supersession already produces a whole new record version, so any property or
  relation endpoint can already differ; the general shape extends what exists
  rather than adding a mechanism. [code, probe P4, P5]
- One change kind per correctable thing would move the structural builtin
  identity with every addition, re-pinning the check contract, policy, profile,
  bundle and every ledger head each time (the OVR-000466 blast radius, G3
  route C), and would constrain by default, which D-04 rejects. [G3 measurement]
- Truth maintenance (de Kleer's ATMS, section 4.9) and nanopublications retract
  by adding a record, never by removing one; PROV-O's wasInvalidatedBy means no
  longer usable, not false. A general correction that adds a successor and keeps
  the target in history matches that. [literature]

## R-05, 2026-09-24: the first cut includes an extracted impact read

Dependencies are extracted after the fact from the ontology, the ledger and the
KG, not declared per use. The first cut includes a read-only query, "what refers
to this exact version", over ontology-typed references (slots whose range is a
record class) across the whole history, followed backwards transitively, which
states what it cannot see: uses never recorded in the ledger, what a rule read,
and query scopes. No identity moves and no kg.py change for it.

Luis asked: "isn't 'what depends on this' extractable from the semantic ledger
or even the KG itself, and not a priori?" Then: "yes".

Why, from code read on 2026-09-24 (not yet probed):
- A slot whose range is a class and is not inlined is a typed reference in the
  compiled contract (view.py around 584); the ontology marks it once, so no use
  needs its own declaration.
- Such a reference is a node property, not a graph edge (kg.py create_entity and
  create_relation, around 560 to 605); the retirement block in kg.py 169 to 184
  applies to edges only, so a reference to r1 does not block correcting r1.
- Correction to CORRECTION-RESEARCH-01 section D: "a historical use has to be a
  typed relation, or the reverse read cannot find it" does not hold for typed
  reference slots. G3 used string-ranged slots, which the ontology does not know
  are references; that is why the dependency looked a priori.

Gaps recorded for later decisions: Core does not check that a reference
resolves (only a nonblank identifier); rule reads could be extracted by Core
while a rule runs instead of declared (RULE_DECLARES_ITS_READS), unresearched;
query scopes must be recorded when a use happens.

## R-06, 2026-09-24: Core finds and reports; it never recomputes on its own

When the impact read finds a use of a corrected version, the use stays bound to
the version it used and is reported as affected, which is not false. A rerun is
a separate execution whose result enters as an ordinary change set through the
normal gate, beside the old one. Core writes nothing on its own. A Core-prepared
rerun proposal for calculations whose inputs and model are declared in the KG is
roadmap, waiting for a second calculation consumer (promotion gate). Automatic
rerun and admit is excluded (architectural laws 5 and 13). The README decision
"this work does not automatically recompute" stands.

Luis: "a)"

## R-07, 2026-09-24: persisted-format route

Build RED then GREEN on the branch under route A (an optional operation field;
no identity moves). Merging to main requires route C (structural builtin
version 2) together with route D (the state-version profile distinguishes the
two kinds), with the affected evidence regenerated and the moved artifacts
counted from the regeneration, not from grep. Coordinate with the saved
core/add-enum-revision candidate so the Shop evidence is regenerated once.

Luis: "correct"

## D-08, 2026-09-24: nothing we hold is final

Luis: "I think a 'correction' in essence is just an 'update' to the system or in
a way a 'change' given new evidence, correction in a way means 'definitive answer
to get it good' but we should never get complacent on 'good' our task here is to
capture knowledge, and as such, it's all in flux, never absolute, 'we know as much
as we know, and we're clear on what we do not know, until new evidence comes'"

Consequences proposed, pending confirmation: the kind is named for what changed,
not for being right; a revised version is "no longer the current account given
evidence E", never "wrong"; revising a revision is ordinary; the stale-target
refusal is about concurrency (revise the latest version), not finality.

## R-08, 2026-09-24: the kinds are REVISION and TRANSITION

The kind that replaces our account of a record is named REVISION (PROV-O
wasRevisionOf), not CORRECTION. A revised version is "no longer the current
account, given evidence E", never "wrong". Revising a revision is ordinary; the
stale-target refusal concerns concurrency only. TRANSITION (the world changed)
stays a separate kind. Added detail is not a third kind now; the cited evidence
carries the why, and a reason field may be added when a consumer needs it.
Wherever R-04 says CORRECTION, read REVISION.

Luis: "go, agreed"

## R-09, 2026-09-24: an undeclared closing is not guessed

A REVISION whose target was closed by a supersession that declared no kind
refuses as STALE_TARGET. Core does not infer whether an undeclared supersession
was a transition or a revision. "For now": revisit if a consumer needs to revise
histories written before the kinds existed.

Luis: "refuse for now"

Built in T3 (837cb7ea) and presented without objection, not separately ruled:
undeclared supersessions record no closing; a revision of a closed period under
a PROLOG_RULES policy refuses CUSTOM_POLICY_HISTORICAL_SCOPE; the impact read
also follows inlined values and event-participation endpoints; its position is
the change set id; r2 keeps supersedes_record_id r1.

## R-10, 2026-09-24: the UMR refinement is an interpretation record beside the annotation

Our reading of a source statement lives in its own record, linked to the
annotation by a class-ranged reference slot, never written into the annotation.
That record is what a REVISION targets when new evidence refines the reading.
The source annotation stays what the source said; cited-source facts get their
own records; the reader's inference sits in the interpretation record. Probed
end to end on copies of the retained main-clause-04 and Marine 02 ledgers
(HISTORICAL-USE-01.md C4; REFINEMENT-SPEC-05.md option 2 / D2(c)). Correcting
the annotation itself as a new artifact with the passage edge restated is
mechanically admissible (P2j) and rejected as the design: it writes another
source's meaning into a record that claims to be the source's wording.

Luis: "record beside"

## R-11, 2026-09-24: link behaviour on revision is a declared kind, not the carrier

Each relation class and each class-ranged reference slot is declared either
STRUCTURAL (part of one interpretation: restated when its target is revised,
or Core refuses; resolves in the current view) or VERSION (names an exact
version on purpose: resolves against record history, never blocks a revision,
followed by the impact read). Defaults while nothing is declared are today's
behaviour: relation STRUCTURAL, class-ranged slot VERSION. The declaration lives
inside contract identity. OD-010 (design/contract_compiler/decisions.md,
accepted 2026-08-27) is to be amended so a VERSION reference resolves in record
history and is exempt from current-view closure; it predates R-02 and never
considered a reference that names an old version on purpose. The carrier rule
proposed before this ruling ("uses are records with typed references; relations
are structure") is withdrawn: it contradicted OD-010, removed structural slots,
and ruled against the Shop, computational graphs and kg_reentry_loop, which all
mix carriers. Research: CARRIER-CONVENTION-01.md (939f7737).

Luis: "declared kind of course"

Phasing proposed there, not yet ruled: phase 1 the ruling, the OD-010
amendment, slot resolution against history built RED then GREEN and taken with
R-07's route C so evidence regenerates once, plus HISTORICAL-USE-01's typed
refusal, its not_covered entry and bearer_id in the impact read; phase 2
declared STRUCTURAL slots block retirement; phase 3 declared VERSION relations
(old versions stay legal endpoints; version graph derived inside Core).

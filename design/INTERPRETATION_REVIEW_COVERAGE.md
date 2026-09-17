# Bounded interpretation-review coverage

Luis approved the read-only checker proposed in
`handover/2026-09-15-core-progressive-interpretation.md` on 15 September 2026.
This is its implementation contract, not a universal acquisition requirement.

## Scope before implementation

Role: `REFERENCE_IMPLEMENTATION` of an optional, explicitly selected
review-coverage profile. The consumer declares the review set and supplies
interpretation judgments. The checker accounts for those declarations only.

1. Claim: missing or stale reviews prevent claiming coverage of the declared
   set. A current unresolved disposition can close review without resolving
   knowledge. No check changes accepted state.
2. Observation: two staged synthetic interpretations, one previously complete,
   both need fresh reviews at a new evidence boundary. Exact refusals and
   receipts distinguish missing, stale, unresolved and proposed correction.
   An integration test retains evidence beside a real accepted history and
   checks that review adds no accepted-state mutation.
3. Reuse: the canonical JSON/digest helpers, explicit retained references,
   existing package layout and history conformance helpers. No separate ledger.
4. Exclude: semantic judgment, dependency discovery, reviewer authentication,
   time-based expiry, scheduler, automatic correction/admission, ontology
   changes, consumer integration, release, and cross-language parity claims.

Pre-action checks: local code/artifacts only, no server or API endpoint. No
runtime mechanism is replaced. No new dependency or implicit input default is
needed. Malformed inputs get typed errors; incomplete coverage is inspectable
and `require_complete()` refuses it explicitly.

## Placement and contract

Public module `malleus.acquisition`, separate from compiler and admission.
`check_review_coverage(boundary_bytes=..., review_bytes=...)` takes exact JSON
bytes and returns a frozen `ReviewCoverage`. It receives no path, history,
graph, writer, callback, model, inventory count or retry budget.

The installed `profiles/interpretation-review.json` declares the closed input
fields, current experimental grammar labels, and outcome requirements/report
groups. The interpreter validates and compares references; it does not hide
domain-specific policy in Python. This first cut selects that one profile, not
an arbitrary profile/plugin language.

An exact reference is `{id, sha256}`. Identity uses existing canonical JSON:
UTF-8, sorted object keys, compact separators, no non-finite numbers. Declared
reference arrays are sets, sorted by ID, with duplicate IDs refused. Meaningful
text is retained unchanged. Input JSON whitespace is not identity-bearing.

Boundary fields: `schema`, `id`, nonempty `evidence`, `ontology`, `knowledge`,
`dependencies`, and nonempty `interpretations`. Ontology and knowledge are
explicit references or explicit null when not selected. The checker does not
fetch or authenticate references. Pin the selected knowledge position's complete
receipt, not merely a convenient graph digest. The caller is responsible for
supplying the actual current boundary. All declared interpretations are required;
no prior complete status can exclude one. Changed evidence, ontology, knowledge,
dependency or interpretation identity changes boundary identity.

Review fields: `schema`, `id`, `boundary_identity`, `interpretation`, `outcome`,
`rationale`, nonempty `supporting_references`, `proposed_change`, `open_issue`,
and `affected_uses`. Each reference pins exact content. Rationale is nonblank;
this checks presence, not whether the explanation is intellectually justified.

| Outcome | Required payload | Coverage meaning |
|---|---|---|
| CORRECTION | proposed-change reference; null open issue | Reviewed; correction remains pending admission. |
| NO_CHANGE | null proposed change and open issue | Reviewed; consumer asserts justified no-change. |
| CONFLICT | specific nonblank open issue; null proposed change | Reviewed; conflict remains visible. |
| UNRESOLVED | specific nonblank open issue; null proposed change | Reviewed; uncertainty remains visible. |

At most one supplied review per interpretation and one unique review ID are
allowed. An unknown interpretation or duplicate review is a typed input refusal,
not silently filtered history. Consumers select the intended review explicitly.
A review bound to another boundary or interpretation version is stale. Current
reviews must cite only exact references declared in the boundary's context.
Affected-use references name declared downstream impacts, not discovered ones.

The result binds profile identity, boundary identity and every supplied review
identity. It gives sorted missing/stale interpretation IDs and current review
dispositions grouped by the profile. Specific open issues and proposal references
are included, not replaced by a Boolean. `complete` means only that every
declared interpretation has one current review. `require_complete()` returns
the receipt when complete and otherwise raises `INCOMPLETE_REVIEW` with both
missing and stale lists. Invalid bytes/fields, unsupported grammar, duplicate
IDs, unknown interpretations and undeclared support references refuse before
a successful receipt. All outputs are deterministic and content-addressed.

Registering a review through a consumer's chosen retention path may append audit
history. The checker itself persists nothing. Evidence/review retention is not
knowledge admission, and accepted corrections still use the selected policy.

```turtle
@prefix stage: <urn:malleus:stage:> .
@prefix role: <urn:malleus:role:> .
@prefix artifact: <urn:malleus:artifact:> .
@prefix profile: <urn:malleus:profile:> .
@prefix rel: <urn:malleus:design-relation:> .
stage:review-coverage rel:implements role:declared-review-accounting ;
    rel:consumes artifact:review-boundary, artifact:interpretation-review ;
    rel:produces artifact:review-coverage-receipt ;
    rel:governedBy profile:interpretation-review ;
    rel:conformsTo artifact:review-coverage-conformance .
artifact:review-coverage-receipt rel:derivedFrom
    artifact:review-boundary, artifact:interpretation-review .
```

Replacement would require an independent implementation to consume these same
artifacts and reproduce these receipts/refusals. None is implemented or claimed.

## Separate incoming requirement

Shop's accepted graph-rule activation requirement remains separate. Its handoff
is frozen at `fca9ab3fada6fad7e3bbf673826ccd6ad988beaf` in the Shop candidate.
Core must assess graph-state enforcement first, then same-history activation.
A failed activation leaves the current policy and accepted knowledge untouched;
failed-report persistence must be explicitly selected. Recovery remains future
work. No graph-rule or activation code belongs to this review-coverage cut.

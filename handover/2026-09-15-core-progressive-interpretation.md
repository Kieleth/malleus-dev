# Progressive interpretation: guidance and completion boundary

## Approved cut

Core owns shared guidance and its installed delivery. Consumers own domain
interpretation; KGs owns the thought experiments. The author-approved direction
is to reconsider earlier interpretations as evidence accumulates, including
interpretations previously marked complete. This candidate starts from
`18015352e2eb5bffbb58125c95de40eba0f4c992` in an isolated clone. It does not
modify the shared checkout, release or replay candidates, or consumer pins.

Role: `REFERENCE_IMPLEMENTATION` guidance for an adopter-selected acquisition
workflow. Distribution checks are `CONFORMANCE_FIXTURE` evidence, not evidence
that a model obeys the guidance or that an interpretation is true.

1. Claim: one shared acquisition rule declares review boundaries, a bounded
   interpretation set, and current dispositions before reporting completion.
2. Observation: the real project installer delivers that rule and its routes
   from Core development, document acquisition, and structured acquisition.
   The existing capture-accounting counterexample remains valid.
3. Reuse: Acolyte's outcome/permission check, existing revision limits, the
   installed skill mechanism, and the completion-boundary test file.
4. Exclude: a new runtime/report grammar, automatic relevance selection,
   source-truth evaluation, new ontology, automatic accepted-state changes,
   consumer experiments, integration, release, publication, or rebind.

Before code: this is local skill/test work, with no server interaction or API
endpoint. Required inputs are explicit. No runtime mechanism is being replaced.
The defect class is missing instruction delivery and misleading completion
claims, not an established failure of an existing semantic completion checker.

## Existing mechanism audit

At the base commit:

- `tests/contract_compiler/pareto/test_adopter_completion_boundary.py` checks
  installed navigation and proves that complete block accounting can coexist
  with an unresolved relationship and `NO_DOMAIN_CHANGE`. Neither test decides
  acquisition completion.
- `src/malleus/assent.py`, `_review_request`, `_review_report`, and
  `_review_disposition`, bind immutable review records to an exact protocol
  target and check identities, reviewer, and report/finding associations. They
  do not declare an acquisition evidence boundary or a required interpretation
  set, and do not gate acquisition completion. These protocol records are not
  interchangeable with arbitrary consumer interpretations.
- `src/malleus/_contract_pipeline/document.py` accounts for supplied captures
  and gaps. It does not choose earlier interpretations for reconsideration.
  Replay and trace recover recorded state and provenance, not a review decision.
- `design/MALLEUS_INTELLECTUAL_SUBSTRATE.md`, section 4.3, identifies
  dependency-closed revision and evidence-triggered revalidation as missing
  general mechanisms. That remains design intent.

There is no existing acquisition completion surface to extend with this check.
The generic protocol machine could execute a selected program, but no selected
acquisition review program or input contract presently supplies this meaning.
No behavioral enforcement will be claimed from instruction-presence tests.

## Proposed placement, not implemented

Use an adopter-selected, read-only completion check beside acquisition reporting,
not in ontology compilation, capture census, knowledge admission, or replay.
Core would execute declared obligations; consumers would provide judgments.
Reuse each project's retained records by exact reference. Do not add another
ledger or require every interpretation to become an Assent ProtocolRecord.

The smallest proposed input contract contains:

- A declared evidence boundary and its exact evidence identities.
- The bounded set of interpretation IDs and versions to reconsider, including
  completed ones. For the first cut, review the whole declared set. No relevance
  engine, dependency discovery, or scheduler is needed.
- For each required interpretation, a review bound to that boundary, evidence
  identities and interpretation version. It names a supported correction,
  justified no-change, conflict, or specific unresolved disposition, with the
  rationale and supporting references. A correction points to a proposal; it
  does not admit it. Record known affected downstream uses without inventing
  undeclared dependencies.

The proposed output separates review coverage from unresolved knowledge and
pending correction work. Missing or stale required reviews prevent a review-
completion claim. A specific unresolved disposition completes that review but
leaves the knowledge gap visible. Retry exhaustion and inventory counts cannot
substitute for reviews. A structurally valid disposition does not prove its
rationale is justified. Consumer review owns that judgment.

These are proposed fields and behavior, not a new public schema or enum. The
next decision is whether to implement this bounded reporting check and define
its exact input/output contract. Until approved, no new Core surface is created.

### Behavioral acceptance cases for that decision

Use synthetic staged evidence. At the first boundary, one interpretation has an
unresolved reference and another is recorded as complete. Later evidence resolves
the reference and qualifies the completed interpretation. Keep both in the
declared review set.

| Case | Required observation |
|---|---|
| New boundary, no reviews | Both missing obligations are reported; completion refuses. |
| Review only the formerly unresolved item | The previously completed item still blocks completion. |
| Reuse a review from old evidence or an old interpretation version | Stale review refuses completion. |
| Supported correction | Review coverage may complete; the proposed change remains pending selected-policy admission. |
| Justified no-change | Review closes with exact supporting references and rationale; interpretation stays unchanged. |
| Specific unresolved or conflict disposition | Review closes, while unresolved knowledge or conflict remains visible. |
| Complete inventory or exhausted retry budget | Missing review still blocks completion; the attempt can end incomplete. |
| Register evidence or record any review | Accepted-state bytes and digest remain unchanged. Selected-policy changes are tested separately. |

These cases have not been executed. The current cut delivers guidance only.
No automatic truth judgment, complete dependency discovery, or semantic
completion guarantee is proposed.

## Execution record

Pending RED and GREEN delivery evidence.

# Progressive interpretation: guidance and completion boundary

## Approved cut

Core owns shared guidance and its installed delivery. Consumers own domain
interpretation; KGs owns the thought experiments. The author-approved direction
is to reconsider earlier interpretations as evidence accumulates, including
interpretations previously marked complete. This candidate starts from
`18015352e2eb5bffbb58125c95de40eba0f4c992` in an isolated clone. It does not
modify the shared checkout, release or replay candidates, or consumer pins.
The inspected Overlord handoff has SHA-256
`78988cb5bffcfc644e1256b2344a4e889d8dea6a5a6a107ec39d368e75eea884`.
It remains an untracked input in the shared checkout, not an implicitly
published research packet. Domain-specific examples were not copied into skills.

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
- `_validate_completed_assessment` in `assent.py` checks assessment outcome and
  payload consistency for a proposal. `KnowledgeHistoryProjection._require_complete`
  in `knowledge.py` checks that recorded changes were applied and action
  transactions finished. Neither declares interpretation-review coverage.
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

- A declared evidence boundary and its exact evidence identities, ontology
  version and selected knowledge position. Any declared dependency references
  are pinned as context, not discovered by the checker.
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

RED: `9a35e9d3`. The completion-boundary selector returned **2 failed, 2 passed**.
The new installed rule and its acquisition routes were absent. The existing
delivery check and unresolved/no-change accounting test already passed. These
are instruction-delivery failures, not failures of a semantic evaluator.

GREEN: `7c39e8d4cdc7fb527bcebc580a7a42dcc4cfe393`, tree
`0880c80c9e750c9651e6174a13ce6e9b3dc94a20`. It changes exactly two skills:

- `.claude/skills/malleus-acolyte/SKILL.md` owns the rule once, inside the
  outcome/permission section. Both document and structured-source acquisition
  link to it. The ontology-growth rule no longer appears to exclude review of
  otherwise structurally complete interpretations.
- `.claude/skills/malleus-dev/SKILL.md` routes development to that rule and
  explicitly separates distribution from behavioral enforcement.

The two new tests in
`tests/contract_compiler/pareto/test_adopter_completion_boundary.py` invoke the
real Codex project installer, compare installed Acolyte bytes, check the review
guidance, and resolve navigation from the installed development and acquisition
paths. This report is the fourth non-generated changed file.

Validation at GREEN: completion, capture accounting and existing Assent review
tests passed **25 tests**. Inquisitor passed **107 tests, one skip**. The skip is
the optional private doctrine absent from the clean clone. Both skill-creator
quick validators, changed-test Ruff/format and diff checks passed.
The combined command below reproduced **132 passed, one skip** at the committed
GREEN, without changing any file in the clean clone.

Commands, run from the isolated clone using the declared project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -ra --tb=short -p no:cacheprovider tests/contract_compiler/pareto/test_adopter_completion_boundary.py tests/contract_compiler/pareto/test_capture_coverage_boundary.py tests/test_protocol.py::TestLeanReviewProtocol tests/test_inquisition.py
/Users/luis/Projects/malleus-dev/.venv/bin/python /Users/luis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/malleus-acolyte
/Users/luis/Projects/malleus-dev/.venv/bin/python /Users/luis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/malleus-dev
```

No runtime, ontology, selected policy, capture grammar or package configuration
changed. No model trial or new behavioral completion check ran. Existing Assent
review tests provide regression evidence for that separate mechanism, not a
claim that it now enforces progressive interpretation.

The candidate's local governance follows its base at OVR-000458. It does not
reserve shared ledger numbers. If another candidate lands first, integration
must reconcile this document revision against the then-current head rather than
copy a conflicting local entry. Main, the release candidate and the replay
candidate remain untouched. No integration, global skill refresh, push or
consumer rebind is included.

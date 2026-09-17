# Reconsidering interpretations after new evidence

An earlier record can pass every structural check and still need another look.
For example, a later passage may qualify a statement previously read as settled.
The question here is not "is it true?" but "did every interpretation we agreed
to revisit get a current review?"

The optional, experimental `malleus.acquisition` module checks this declared
coverage. It does not choose interpretations, read sources, authenticate a
reviewer, judge a rationale, or change accepted knowledge. It is separate from
Assent review records, compiler admission and replay. Existing callers do not
automatically acquire this requirement.

## Inputs and outputs

`check_review_coverage(boundary_bytes=..., review_bytes=...)` takes one JSON
boundary and an explicit list or tuple of review JSON bytes. It returns an
immutable `ReviewCoverage`. The installed `REVIEW_COVERAGE_PROFILE` bytes expose
the exact closed shapes and outcome rules; `REVIEW_COVERAGE_PROFILE_IDENTITY`
identifies that data. The current grammars are experimental `private-v0`, not
stable interchange formats.

| Input | Meaning |
|---|---|
| Boundary ID and evidence references | The declared reading/evidence boundary being reviewed. |
| Ontology, knowledge and dependency references | Exact context at that boundary. Ontology and knowledge may be explicitly null when not selected; missing fields refuse. |
| Interpretation references | Every declared interpretation needs review, including previously complete ones. This first profile requires a nonempty set. |
| Reviews | Exact boundary and interpretation identities, outcome, rationale, supporting references, proposed change or open issue, and declared affected uses. |

Every reference contains `id` and lowercase `sha256`. Reference lists are
unordered sets, normalized by ID, with duplicate IDs refused. JSON formatting
does not affect identity; substantive strings are unchanged. Identical IDs
cannot denote different content within a boundary. Supporting and affected-use
references in current reviews must resolve to that boundary's declared context.
Proposal references identify proposed content and need not already be accepted.
References are checked for binding, not fetched or authenticated.

Pin the complete selected knowledge-position receipt, not only its graph digest.
The caller supplies the actual evidence boundary. Reusing an old boundary
deliberately asks an old question; the checker cannot discover later evidence.
Review/audit retention does not automatically declare another evidence boundary.
Consumers decide and record boundaries explicitly, without moving a frozen one.

The result lists `missing` and `stale` interpretation IDs. Its `document` gives
current reviews in four groups, preserving rationale, proposal and open-issue
fields. `CORRECTION` requires a proposed-change reference; `NO_CHANGE` requires
a rationale with no proposal or open issue; `CONFLICT` and `UNRESOLVED` require
a nonblank open issue and no proposal. All require supporting references.
This does not establish that the rationale is justified or the issue specific
enough for the domain; that remains the reviewer's responsibility.

Call `result.require_complete()` before reporting this boundary reviewed. It
raises `ReviewCoverageRefusal` with reason `INCOMPLETE_REVIEW` if reviews are
missing or stale. Unsupported grammar, malformed data, duplicate reviews,
unknown subjects and undeclared support references also refuse explicitly.
There is no preferred-review selector: pass one intended review per subject.
Retry counts and inventory-completion flags are not accepted inputs.

## Small executable example

These are synthetic evidence and interpretation references, not accepted graph
records. One completed interpretation stays in the required set. A review may
finish while its uncertainty remains visible.

```{doctest}
>>> import json
>>> from hashlib import sha256
>>> from malleus.acquisition import check_review_coverage
>>> def raw(value):
...     return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
>>> def reference(identifier, content):
...     return {"id": identifier, "sha256": "sha256:" + sha256(content.encode()).hexdigest()}
>>> evidence = [reference("source:first", "Initial statement."), reference("source:later", "Later qualification.")]
>>> interpretations = [reference("meaning:a", "Previously complete interpretation."), reference("meaning:b", "Unresolved reference.")]
>>> boundary = {"schema": "malleus.interpretation-review-boundary/private-v0", "id": "reading:second", "evidence": evidence, "ontology": None, "knowledge": None, "dependencies": [], "interpretations": interpretations}
>>> pending = check_review_coverage(boundary_bytes=raw(boundary), review_bytes=())
>>> pending.missing
('meaning:a', 'meaning:b')
>>> review_a = {"schema": "malleus.interpretation-review/private-v0", "id": "review:a", "boundary_identity": pending.boundary_identity, "interpretation": interpretations[0], "outcome": "NO_CHANGE", "rationale": "The later qualification concerns the other interpretation.", "supporting_references": evidence, "proposed_change": None, "open_issue": None, "affected_uses": []}
>>> check_review_coverage(boundary_bytes=raw(boundary), review_bytes=(raw(review_a),)).missing
('meaning:b',)
>>> review_b = dict(review_a, id="review:b", interpretation=interpretations[1], outcome="UNRESOLVED", rationale="The new passage still does not name the referent.", open_issue="An identifying source passage is still needed.")
>>> result = check_review_coverage(boundary_bytes=raw(boundary), review_bytes=(raw(review_a), raw(review_b)))
>>> result.require_complete().complete
True
>>> result.document["groups"]["unresolved"][0]["open_issue"]
'An identifying source passage is still needed.'
```

The receipt is deterministic and content-addressed, including the profile,
boundary and supplied review identities. `document` returns a defensive copy.
It is not a signature, a truth certificate or proof that a person actually read
the evidence. A consumer can retain it through its selected audit mechanism;
this function performs no persistence. Proposed corrections still require their
own selected-policy admission. Neither review nor receipt grants permission to
rewrite accepted knowledge.

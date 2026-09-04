# Core population piece 4: document assertions

Status: implemented in Core, awaiting independent overseer verification.

This is the historical P4 surface. P6 removes the caller-supplied `valid_time`
argument and derives `ORDER_ONLY` capture/import time from `capture_id`. See
`2026-09-03-core-population-p6-report.md` for the current contract.

## Coordinates

- RED commit: `7b986618e52ca9d52c228cc6a3720f28f4815add`
- GREEN commit: `7dacc511329e5bb7d743b4247205174e2d7bc32d`
- GREEN tree: `d896742741561dc857fa6a39e416bfe591f1262d`

The implementation adds one optional source adapter. It does not change the
neutral population plan, knowledge-change history, admission, replay, or graph
model.

## Public surface

`malleus.compiler` exports:

- `DOCUMENT_ASSERTION_ADAPTER`
- `DOCUMENT_CAPTURE_GRAMMAR`
- `DocumentAssertionCompilation`
- `DocumentAssertionRefusal`
- `DocumentAssertionRefusalReason`
- `adapt_document_assertions`

The adapter consumes exact reading bytes, exact capture bytes, and
adopter-proposed records. It checks the capture against the reading and returns
canonical neutral population-plan bytes, canonical census bytes, and the exact
evidence identities.

## Usage

```python
from malleus.compiler import adapt_document_assertions

result = adapt_document_assertions(
    reading_bytes=reading_bytes,
    capture_bytes=capture_bytes,
    capture_id="capture:inspection-note",
    plan_id="plan:inspection-note:1",
    contract_identity=effective_contract.identity,
    records=proposed_records,
    supersessions=[],
)
```

The returned plan enters the same public population compiler used for
structured rows. The capture is retained as evidence. Its assertions are not
added to the domain graph. The adapter derives the capture batch's
`ORDER_ONLY` valid time from `capture_id`; assertion and domain dates remain
optional fields in the retained capture.

## Mechanical evidence

- The RED commit collected 15 tests and failed all 15 because the public
  adapter surface did not exist.
- At GREEN, all 15 adapter tests pass. They cover exact plan and census bytes,
  reading identity, block references, verbatim text with whitespace
  normalisation, modality, formalisation targets, required and known gaps,
  closed capture shape, malformed inputs, independent census axes, and a
  gaps-only plan.
- The four existing public-compiler tests pass with the adapter tests.
- The combined document, population, governed-history, replay, and graph seam
  passes 341 tests.
- Ruff and formatting checks pass for the changed Python surface.

## Non-claims

This piece does not extract assertions from prose, invent records, choose a
domain ontology, accept a plan, or mutate a graph. It does not make the capture
grammar stable. It does not claim that reviewing one statement reviews every
statement in a block. The minimal `source-assertion` profile retains assertion
modality as evidence, but does not yet guarantee that modality is visible in
ordinary graph queries. The later domain-history-profile work must choose a
queryable qualification, a reified claim, or a typed provenance join before a
hypothesised relation can be presented as epistemically qualified graph data.

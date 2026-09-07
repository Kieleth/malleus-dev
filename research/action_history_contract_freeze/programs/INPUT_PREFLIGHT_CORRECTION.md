# Input-preflight consumer-review correction

Base: `f276271b6719355e1002dd44aa6f4214cb74dd46`.
Scope remains the research OPTIONAL_PROFILE supplied-input preflight; the
regressions are CONFORMANCE_FIXTURE evidence. No history or runtime claim.

## Bound correction before code

Claim: required collection fields contain actual lists, not merely present
keys. Empty lists remain valid at this shape boundary. Malformed record
canonicalization must produce PacketRefusal, preserving its lower-layer cause,
not leak LedgerError. Inputs remain unchanged on success or refusal.

Smallest observation: the five independently reported null collections refuse
after correctly recomputing record/reference hashes; each corresponding empty
list passes shape checks; an unencodable actor string refuses through the
preflight interface. These tests do not establish membership or provenance.

Reuse: the existing ancestor-to-field binding table, compiled instance
validation, record_hash and its LedgerError, and the existing PacketRefusal
interface. Name the table required_collections so its list requirement is
explicit data. Remove the presence-only lookup, with no fallback.

Exclude: production validation or schema changes, general Assent admission,
cross-record references, actual history resolution, check execution, persistence,
new artifacts/instructions, public promotion, shared main and consumer edits.
No server, endpoint, dependency install or production mechanism replacement.
Missing data refuses; null is never coerced to an empty list. RED precedes GREEN.

InputPreflight consumes DeclaredRequiredCollections
InputPreflight translates RecordCanonicalizationRefusal
ConformanceFixture distinguishes NullFromEmptyCollection

## Independent evidence reproduced

The consumer's exact test file has SHA-256
`babd59582b078e032fd4e62df027cfa8cb710e5b9cb36958811e663e295919a2`.
Its retained RED JUnit has SHA-256
`925f15f294af5da90454a0a9ba6cc0f05fa4a71f783dda5fc434c946b5374f03`.
Running those unchanged tests against this base reproduced all six failures:
five nulls returned STATIC_INPUTS_VALID and one record hash raised LedgerError.
The consumer independently ran 38 focused tests, not the broader owner gate.
The earlier INPUT_PREFLIGHT_REPORT.md stays intact as historical evidence;
this correction supersedes its completeness claim for these two input classes.

## Root cause and correction

The compiled validator treats None as absent for these optional multivalued
fields. The preflight's additional presence check therefore needed a type
requirement, not just key membership. The renamed binding now explicitly
declares required collections. One shared ancestor-aware guard requires a list
for every declared field. No field names are embedded in the checker, no old
presence-only lookup remains, and no null-to-empty normalization occurs.
Collection contents still pass through the existing compiled validator.

Record hashing already refuses unencodable strings as LedgerError. The missing
piece was the preflight's translation of that typed lower-layer error.
The record-hash call now translates LedgerError to
PacketRefusal(INPUT_RECORD_SHAPE), retaining the exception cause. It does not
catch arbitrary exceptions or redefine canonical JSON.

## Exact corrective evidence

- RED: `5786a6546826d387b78fb3d7558dce160abd1bca`.
- RED tree: `b83b81e19adb6004ae7864fb66e6b87991501b13`.
- GREEN: `da6f8c86c2ffc654ad0367d96a050ddbcc86ab6a`.
- GREEN tree: `e84ce4f0900fd0caeae63b677804799bfbd470d4`.

The RED commit changes only this research report and test_input_preflight.py.
The GREEN commit changes only input-bindings.json and input_preflight.py,
with 12 insertions and 5 deletions across those two files.

Both the working checkout and a clean detached clone reproduced the corrective
RED: 7 failed, 31 passed. Six failures reproduce the consumer findings; one
checks removal of the old presence-only binding. Five new empty-list controls
pass before and after the fix. GREEN has 38 preflight tests.

Owner verification on exact GREEN:

- Working checkout: preflight, carrier and unchanged external consumer file,
  55 passed, zero skipped.
- Clean detached clone: the unchanged external consumer file,
  6 passed, zero skipped.
- Working checkout and clean detached clone: the exact combined selector in
  INPUT_PREFLIGHT_REPORT.md, 331 passed, zero skipped.
- Changed-Python Ruff and format, aggregate diff check and clean clone status
  passed. An explicit import-origin check verified both malleus.compiler and
  input_preflight resolved inside the exact clone.

All commands used the configured interpreter
`/Users/luis/Projects/malleus-dev/.venv/bin/python`, `PYTHONPATH=src:.`,
`PYTHONDONTWRITEBYTECODE=1`, `-c pyproject.toml`, and `-p no:cacheprovider`.
The external selector was
`/private/tmp/malleus-reentry-input-review.qjeQu7/test_consumer_input_boundary.py`.
Corrective RED selects only the committed programs/test_input_preflight.py.
The 331-test selector excludes the six external tests; do not count them twice.
These corrective runs are Core self-verification, not a new independent audit
or the full repository/package gate.

Exact GREEN SHA-256 identities:

- input-bindings.json: `bfe174196e2041f90544344e3ee816844cdb62f809439e964a1f571637fea28b`.
- input_preflight.py: `f87861b7d198f136d34377d6098d5e5d9708fc1ded669a7343320e90282b5e85`.
- test_input_preflight.py: `c93a1c29185c12d292a5e8916aeabd99fd71456c4bf73485fb6177b663d8ffca`.

The Malleus development skill kept this corrective slice inside the existing
research boundary. No runtime, history verification, shared-Core, public
ontology/API, package or consumer capability changed. The accepted carrier
choice and the remaining declarative/history-binding work are unchanged.

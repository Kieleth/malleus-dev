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

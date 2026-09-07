# Retained-input carrier: existing-type reuse candidate

Status: PROPOSED. Operator selection and complete runtime binding remain open.

## Evidence and scope

Base: `5b564399808efecbde2c80c0f969c5702931a995`.
RED: `726a0c0a2c0ad6079ae4b49e1194a2987a1a0974`.
GREEN: `a9d78edf3eaa907d6ca35c58793e6502abfe6cd7`.
GREEN tree: `03827e1db18ae63096dd6c5abaf0e7a2f9675819`.

Only the research plan, test and candidate JSON changed before this report.
No production, ontology, public API, package, shared ledger, main, paper, or
adopter file changed. No runtime mechanism was added or activated.

The existing SourceArtifact description in `ontology/assent.yaml` identifies
caller-declared bytes used by evidence, without authenticity or truth claims.
Its existing semantic hash binds ID, version, byte digest, length, media type
and locator. `docs/ASSENT_PROTOCOL.md` distinguishes that identity from truth.
The existing monitor specification accepts applied ProtocolArtifact dependency
records and checks their record hashes. SourceArtifact already has that parent.

This supports a reuse candidate: use SourceArtifact as a byte carrier for the
compiled record contract, scope association, requested interval, original
context and current context. Keep each role's existing content checks separate.
Do not infer permission, currentness, scope validity or trusted input membership
from the generic carrier type or media type.

Record inputs remain their existing typed records. The intended executor stays
an explicit scalar. The proposed table does not turn them into source blobs.
It preserves the existing invocation roles without changing their order.

## Observed tests

Working-checkout RED: 11 failures with the candidate absent. Working-checkout
GREEN: 11 passed, zero skipped, for `programs/test_input_carrier.py`.

The tests use actual compiled-contract bytes and existing lexical
scope/interval/context witnesses. Every full carrier record validates under
compiled Assent, and each payload passes its separate existing content parser.
Changing payload bytes changes the byte, artifact and record identities.
Arbitrary `{}` bytes still produce a valid source carrier but fail every
selected role parser. This proves the distinction, not a new admission guard.

A clean detached local clone at exact GREEN reproduced the combined selector
from `OUTPUT_FIELDS_REPORT.md`: 293 passed, zero skipped, in 18.82 seconds.
Changed-Python Ruff and format, aggregate diff check and clean state passed.
This was Core self-validation, not an independent carrier audit. The earlier
consumer review covered output fields only, not this candidate.

Exact GREEN SHA-256 identities:

- input-carrier-candidate.json: `872527a5c634ad0935c4cc3e255ce4e7e3dd1a57fdd5c2350f909069206b0529`.
- test_input_carrier.py: `f5c7fff7da3757d384269d560d6edfad1b2c4e7cd94bbb63f896fbf75c400d71`.

## Proposed choice and remaining obligations

Recommendation for operator review: reuse this existing byte carrier, with
explicit role-specific content validation. No new artifact kind appears
necessary for these five inputs. That recommendation is not recorded as an
accepted carrier selection by the tests or candidate table.

Still required: the history retention-event binding, wrapper/content ID
association, real applied-prefix resolution, complete static dependency set,
input/provenance ordering, concrete retained instances and producer identities.
In particular, dynamically supplied context/proposal/action inputs cannot be
placed into a static monitor specification that precedes them. An executor ID
cannot stand in for a retained artifact. A SourceArtifact has its own record
and semantic hashes, neither of which substitutes for its raw-byte digest.

No check ran, record was retained, policy was evaluated, action was authorized,
or graph changed. The lowest affected role remains research OPTIONAL_PROFILE;
the probes are CONFORMANCE_FIXTURE. The development skill kept this proposed
representation out of production and prevented a compatibility test from
becoming protocol authority.

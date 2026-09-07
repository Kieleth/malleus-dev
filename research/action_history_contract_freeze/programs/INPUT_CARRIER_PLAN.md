# Retained check inputs: reuse probe

Status: research candidate, not a selected public carrier or runtime contract.
Base: `5b564399808efecbde2c80c0f969c5702931a995`.

OPTIONAL_PROFILE claim: test whether the existing SourceArtifact record can
carry the five declared byte-input roles without a new artifact kind. Its
ontology description covers caller-declared bytes used by evidence, not just
observed world state. This is a proposed use of that existing type, not a
decision that a source record alone satisfies a check-input contract.

CONFORMANCE_FIXTURE observation: construct full SourceArtifact specimens from
actual compiled contract bytes and the existing context/scope/interval shape
witnesses. Validate records with compiled Assent and contents with their own
declared parser. Check exact byte, semantic-artifact and record identities.
Well-hashed arbitrary bytes must fail the relevant content check. Record and
scalar inputs must remain distinct from byte inputs.

Reuse: SourceArtifact, source_artifact_fields, record_hash, the public compiled
contract loader, and existing research content validators. No production code,
new instruction, artifact kind, public interface, parser or retention event.

Excluded: applied-prefix lookup, actual retention, producer implementations,
complete monitor dependency/provenance ordering, lifecycle execution, shared
files, ontology changes, merge and push. Test-only construction is not a
retained input instance. The proposed carrier needs review before activation.

Pre-action checks: no server or endpoint; no missing-value defaults; no old
mechanism replacement or fallback. Commit RED before the candidate table.
This probes a representation option without choosing a new protocol authority.

SourceArtifactCandidate describes ExactInputBytes
InputRole selects ExistingContentContract
InputRole doesNotEstablish AppliedPrefixMembership
CandidateFieldBinding governedBy ExistingHashDomains

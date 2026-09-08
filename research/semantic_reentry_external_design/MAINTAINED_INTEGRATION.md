# Re-entry on the maintained Core reader

Status: integration in progress, not a new runtime or release claim.

## Bound slice

Luis requested completion of integration after the supported undesired-result
experiment. The committed Core base is
`0af4364025a6fdff2b032e028d30e4d12ebf4289`, with source tree
`156592a98156f51562eda5f8164cf02ed654a0f5`. The three consumer commits from
`8dc2d607dd13deafdf06dd87bcf79d6d8857c8ec` apply without conflict. Their original
receipts remain historical evidence, not results for this new runtime.

Claim: the existing Re-entry consumer accepts Core's maintained
`KnowledgeHistoryReplay` at exact requested ledger coordinates, and agrees with
full replay through proposal, authorization, execution, observation, ordinary
KCS admission and terminal evaluation. A supported observation of three is
accepted as three while the exact-two goal remains unsatisfied, with one
dispatch and no automatic retry.

Smallest observation: follow the existing supplier episode with one reader,
compare its graph, receipt, temporal history, provenance and protocol state at
each tested boundary, then feed its result to the existing immutable
`AcceptedReadView` and synthesizer. Repeated terminal reads must neither refold
the ledger nor invoke a model or effect. A lagging reader and a stale
replay/context pairing must refuse, without changing the published position.

Reuse: Core's public `KnowledgeHistoryProjection.open/current/refresh`, the
existing history-owned composition context, `freeze_accepted_replay`, the
same supplier lifecycle and independent observation adapter. No test substitutes
a Core proposal, authorization, observation, admission or replay boundary.

Exclusions: new Core API, ontology or fixture vocabulary, changed exact-two
goal or action grammar, new retries, production supplier, delivery, planner,
Robotics execution, database, release or push. No new dependency or setup step.

## Roles and costs

The added integration checks are `CONFORMANCE_FIXTURE`. Core's reader and the
existing research-local consumer remain `REFERENCE_IMPLEMENTATION` under the
compiler-enabled semantic-history/state-version and experimental single-action
`OPTIONAL_PROFILE` selections. The goal, supported quantities and one-attempt
stopping rule remain `ADOPTER_CHOICE`. No new base invariant is introduced.
Without these profiles the composed history/action/replay guarantee is omitted.

The reader consumes verified ledger suffixes and produces the existing public
replay value. The immutable Re-entry view consumes that replay and an exact
history-owned composition context. The synthesizer consumes the view and bound
contract, and produces the existing action candidate or refusal. Only the
ordinary Core KCS admission can change accepted knowledge.

This does not make the entire application incremental. The public
`history.composition_context()` still obtains its own full replay, and
`freeze_accepted_replay` still validates an exported graph by reconstruction.
The independent full-replay oracle and context are obtained before checking
the maintained read/synthesis region. No private context constructor or
fingerprint bypass is added. Core refresh also verifies prefix bytes and copies
state as documented in its own result. These costs are not hidden or benchmarked
as constant-time work.

## Pre-action checks

No server calls beyond authorized session coordination. No endpoint, required
data default, new dependency, production mechanism replacement or Core fix.
Changes are consumer conformance tests and integration evidence only. The
earlier experiment's actual mapper/model changes remain its three separately
identified commits. Each integration refusal gets an executable assertion.

The new gate must retain the old exact-epoch guards unchanged, exclude their
historical actual-runtime assertions explicitly, and bind the reviewed Core
source tree itself. Fresh runs cannot relabel earlier evidence.

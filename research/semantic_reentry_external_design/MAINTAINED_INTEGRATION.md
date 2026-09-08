# Re-entry on the maintained Core reader

Status: integration in progress, not a new runtime or release claim.

## Bound slice

Luis requested completion of integration after the supported undesired-result
experiment. The committed landing base is Core release candidate
`6f37a75ec942100e973bb30763b2e73f281b74a0`, with source tree
`3b4fd1c9eb66d84c31050b5f0fd970a6fc2572a8`. The three consumer commits from
`8dc2d607dd13deafdf06dd87bcf79d6d8857c8ec` apply without conflict. Their original
receipts remain historical evidence, not results for this new runtime.

The first integration check used `0af43640` and source tree
`156592a98156f51562eda5f8164cf02ed654a0f5`. Its maintained quantity-three E2E
passed and produced byte-identical history to the earlier full-replay run.
While that check ran, Core committed version 0.14.0. The only source change
between these Core commits is `status.py`'s package-version string. The landing
gate explicitly pins and reruns against 6f37a75e; the earlier runs are not
relabeled as release-candidate results.

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

## Existing consumer seam

The adopter keeps a reader open and supplies the requested full coordinates.
For already retained inputs and an existing original context, the composition
is:

```python
reader = core.KnowledgeHistoryProjection.open(history.path)
# At each evaluation boundary, acquire the existing public context explicitly.
context = history.composition_context()
replay = reader.refresh(
    expected_head_hash=context.base_ledger_head,
    expected_event_count=context.base_ledger_event_count,
)
view = freeze_accepted_replay(replay=replay, context=context)
contract = reentry.bind_supplier_reentry(
    view=view, original_context_bytes=original, rule_source_id=rule_source_id,
)
result = reentry.SupplierReentrySynthesizer().synthesize(
    contract, view,
    model=reentry.SupplierSourceModel(),
    update_strategy=reentry.SupplierActionStrategy(),
)
```

`core` is `malleus.compiler`; `reentry` is the existing research-local
`supplier_reentry` module. The existing `accepted_read_view` supplies
`freeze_accepted_replay`. This is composition of existing calls, not a new
convenience API. Ledger movement between context acquisition and refresh
refuses; the consumer does not silently rebase a proposal.

## Pre-action checks

No server calls beyond authorized session coordination. No endpoint, required
data default, new dependency, production mechanism replacement or Core fix.
Changes are consumer conformance tests and integration evidence only. The
earlier experiment's actual mapper/model changes remain its three separately
identified commits. Each integration refusal gets an executable assertion.

The new gate must retain the old exact-epoch guards unchanged, exclude their
historical actual-runtime assertions explicitly, and bind the reviewed Core
source tree itself. Fresh runs cannot relabel earlier evidence.

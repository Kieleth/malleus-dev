# Re-entry on the maintained Core reader

Status: IMPLEMENTED and verified, ready for Core-owned local landing. This is
not a new runtime, public API or release claim.

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

## Verified result

The configured Python 3.12.9 run used clean integration commit
`ab631edac75513b317f69e33963b009e228a86b7`, tree
`8fd500bb934e151025adf6c1ee07901646f8d290`. The integration after the original
experiment changes only conformance tests and documentation, not its three
runtime modules or Core. Documentation and this evidence receipt were finalized
after the gate, without changing the tested code.

The focused Re-entry group passed 139 tests. The other two groups passed 173
and 140 tests, with one existing optional private-doctrine skip. Their exact
union accounts for all 453 collected cases: **452 passed, 1 skipped**, no
omissions, extra cases, duplicate cases, failures or errors. These include
Core's thirteen maintained-reader conformance cases. Five separate current
epoch checks passed. Scoped Ruff and the base-to-head diff check passed.
This is the relevant unified gate, not full repository CI or clean-install
verification. Exact selectors and evidence hashes are in
[the gate](maintained-integration-gate.json) and
[the result receipt](maintained-integration-result.json).

All seven fresh lifecycle histories are byte-identical to the original
undesired-observation experiment. A separate process reopened each with the
release-candidate Core and consumed the maintained reader using production
modules, without importing the test helpers. During these independent evaluations,
full replay, disk reads and model invocation were forbidden mechanically.

| Controlled case | Accepted quantity | Fresh Re-entry result |
| :--- | :--- | :--- |
| Requested two, observed two | 2 | SATISFIED / LINKED_OBSERVED_KCS |
| Write reached two, execution receipt failed | 2 | SATISFIED / LINKED_OBSERVED_KCS |
| Receipt succeeded, source stayed at one | 1 | REFUSED / EPISODE_TERMINAL |
| Observed two, corrupted episode binding | 2 | REFUSED / EVIDENCE_DISAGREEMENT |
| Requested two, observed three | 3 | REFUSED / GOAL_UNSATISFIED |
| Observed three, corrupted episode binding | 3 | REFUSED / EVIDENCE_DISAGREEMENT |
| Observed three, falsely recorded CONFIRMED | 1 | PENDING / AWAITING_OBSERVED_KCS |

Every case has one dispatch attempt and zero new candidates after observation.
In the last case the observed-source mapper refuses EVIDENCE_DISAGREEMENT
before new retention; Re-entry does not falsely close the episode. No repair
path for a faulty observer, new retry policy or automatic intervention is added.
In the main quantity-three case the accepted replacement, trace, supersession
and terminal refusal survive JSONL-only reopen. The zero shortfall does not
satisfy this adopter's exact-equality goal.

The earlier actual-epoch guard correctly failed on the new Core source tree.
It remains unchanged. The separate landing guard rejects older or unknown
source trees and preserves the earlier gates and receipts byte-for-byte.
No Core defect or missing seam was hidden by a fixture substitute.

Self-inquisition: this is one research-local consumer exercising the existing
public reader, not a second projector, generic Re-entry API, new authority,
source-truth proof or end-to-end performance claim. The one ledger remains the
only accepted-state authority. The role/profile selections and costs above
remain unchanged.

## Landing boundary

Core owns the main checkout and the separate 0.14.0 release. This task neither
pushes nor tags. The verified diff from 6f37a75e is confined to
`research/semantic_reentry_external_design/`. Existing paper, Recon and release
work must not be staged or changed by its landing.

At the final read-only coordination check, Core's 77d7b9b4 retained the exact
tested source tree. Its subsequent CI portability and OCR corpus metadata
changes are not Re-entry changes. The only changed helper imported by the
selected Core reader tests moved `tomllib` to a module-level import with a
Python 3.10 fallback; Python 3.12.9 still selects `tomllib`. Core must check its
actual landing state and rerun the affected reader/epoch checks. An unreviewed
runtime source tree refuses rather than silently rebinding this receipt.

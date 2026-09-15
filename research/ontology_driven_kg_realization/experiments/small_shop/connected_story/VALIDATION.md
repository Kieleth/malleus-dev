# Frozen Shop validation, 2026-09-08

This file is chronological evidence. Earlier pending statuses describe their
frozen boundary; the connected-run successor at the end records current work.

Source and probe implementation:
`5ea6c9031604916472a5402724bd09968de70905`, tree
`685e09249865b924fb0e5477a4c4763587b71bbe`.

Final behavioral validation used an isolated export of released Core
`v0.14.0`, commit `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`, overlaid with
only that commit's `connected_story/` and `CONNECTED_STORY_PLAN.md`. This
excluded concurrent Core, paper and Re-entry work. The Python import path was
verified to resolve to the isolated export. Dependencies came from the
repository's existing declared development environment; no installation or
package change was made.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story tests/contract_compiler/pareto/test_domain_history_profile.py tests/contract_compiler/pareto/test_object_event_population.py tests/contract_compiler/pareto/test_small_shop_default_admission.py
```

Result: **35 passed in 26.37s**, zero skips. The same selector in the live
checkout previously returned 35 passed in 26.55s. The new Shop-only tests
account for ten of these: seven source-boundary and three integration tests.
Scoped Ruff lint, format and whitespace checks pass. The proposed schema's
public PROJECT grounding check passes. None of these is human ratification of
the source or the proposed profile.

The independent source denominator is the retained publisher image, not an
image regenerated from our transcription. Its SHA-256 is
`d553b5bd5f9ecf3d0051a685c0bbe30cf99055f8dd09f712a6cf3ca302ed58e8`.

The isolated positive probe produces 18 ledger events, two KCS, seven
historical records and six current records. Repeated runs reproduce:

- History bytes: `sha256:72be0178fc066f2dbb36ab76bfc580c50755251f499593aaa50be6a0ddab6181`.
- Ledger head: `sha256:86bf7cbc723b37d68f7b02b472621e6371161c3f53bda2e63fd1f20615f529f8`.
- Replay receipt: `sha256:979edce122f566e38530c12662442b0976abfbd2136f008b1d4d73a2534b60be`.

The contract probe independently reproduces Event replacement as `ADMITTED`,
with the old event retained and its replacement current. That observation is
the open Core classification question in [CORE_REQUIREMENT.md](CORE_REQUIREMENT.md),
not a passing test of the proposed state-only correction guarantee.

The request was delivered to the separate **Malleus Core** task
`01a02f71-fec6-7382-9c68-c3efd3dba5d4`. Shop has not implemented an upstream
fix, selected the final profile, populated all 21 events, or published a release.
The next dependent action is to resolve the enforceable history contract,
then complete the joined Shop runner with its independent expectations.

## Source answer-key addition

The later Shop-only addition follows test-data RED `50b7df40`, seven failures
for the absent `source_expectations.json`. The hand-authored file supplies nine
source questions and exact witnesses. Seven tests pass, including four mutated
copies with a missing row, missing field, false value or duplicate case. These
are source-accounting checks, not graph-query correctness or human ratification.
The future producer must not read the expectation file.

The combined selector above, now including these seven tests, returns **42
passed**, zero skips, in the live declared environment. No installed-package,
full-repository or release gate was run for this test-data addition. The frozen
35-test release-baseline result above remains its own separate receipt.

Core has acknowledged that custom correction text is descriptive, not a
state-type admission restriction, and is investigating the execution contract.
Shop has not selected that profile or implemented an upstream workaround.

## Restricted-history successor

Core later delivered the optional transition rule at
`2ef5442efec6e43f2b2623a288933f7c62d46d4e`. Shop consumer RED `0f793c54` and
GREEN `04794b4d6a14ebd9237311d77dc1a26ca8dd9a4e` verify the narrow replacement
restriction in a fresh history. Eight consumer cases pass. An isolated
detached Core checkout with only the Shop successor files passes **283 tests,
zero skips**, covering the whole Shop directory and Core's transition suite.
This is not a full repository or release test. The initial archive-only setup
failed the existing historical-Git journal check; the final checkout retains
those objects and passes without changing the guard.

[The consumer report](RESTRICTED_HISTORY.md) records exact rules, source/history
identities, replay parity, matching controls, refusal atomicity and limitations.
The earlier structural-only evidence stays frozen. The missing Core capability
is closed; final Shop history semantics and the full connected population are
still pending selection and implementation respectively.

## Ontology-led connected run

The user selected the ontology-led approach after rejecting the exact-concrete-
type recommendation. RED `dd36af1e` commits the modeling decision and eleven
expected missing-module errors. GREEN is
`90c3aeee0b04335a6eb6e9bf11f93c200b2d7dc4`; its runtime, ontology, profile,
mapping and instruction are all Shop-owned. Guard commit
`f53b48c16931003c691d46d79eca60bb0acdf159`, tree
`0fc7a4e871b456a1adfed3401a3f538e5824fbcc`, adds tests without runtime changes.
Core's unrelated closing documentation commit falls between RED and GREEN;
it is not a Shop change. No old probe bytes were replaced.

The frozen implementation uses the delivered Core transition mechanism,
unchanged since `2ef5442e`. A local detached clone of exact `f53b48c1` retained
its Git object history and excluded all shared worktree dirt. Python imports
resolved under that clone via `PYTHONPATH=src:.`; dependencies came from the
existing repository `.venv`, with no installation. Bytecode and pytest cache
writes were disabled. The exact command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_transition_admission.py
```

Result: **296 passed, zero skips**, 122.83 seconds. The selector includes the
13 connected-run tests at that commit. The detached checkout remained clean.
This is a Shop/transition regression gate, not the full repository or package
gate. Scoped Ruff and format checks pass. The public schema check and its
intentional notes are recorded in [MALLEUS_INQUISITION.md](MALLEUS_INQUISITION.md).

A separate run from the same detached source produced 895,225 ledger bytes,
121 protocol events, 21 domain changes, 107 historical records and 106 current
records. Formatting-only successor `88f8889d` wraps the retained-profile lookup;
no behavior changes. Its detached rerun produces 895,257 bytes with the same
domain results. Source attestation changes because the adapter itself is
retained. Those final identities and output joins are in
[run_receipt.json](run_receipt.json). Repetition and reopen tests agree. The
maintained reader was opened at the final checkpoint, so this result does not
claim incremental advancement across every row. That broader observation is
still distinct from the earlier two-row incremental probe.

All 21 retained table rows and 123 nonempty fields have plan derivations or
declared gaps. Every historical record traces back to the retained table.
The source mapper is tested with independent answer-file reads forbidden.
The test suite separately specifies quantities, physical identity, invoice and
payment joins, missing invoice values, malformed quantity inputs and same-owner
predecessor selection. A synthetic occurrence replacement is refused after
successful preparation with the admission-boundary bytes unchanged.

The final documentation/receipt addition also exercises the documented read-only
CLI against that exact history and binds the receipt to input bytes. It changes
no implementation. Test counts for overlapping selectors must not be summed.

No source authenticity, human semantic ratification, universal identity policy,
business-rule eligibility, domain event ordering, authorization, action,
incremental performance, installed-package or release result is claimed.

Final detached gate at `7bdef4105518f8960bf417782e5e35104a02b20e`, tree
`5c7df14a87403e628a080257c0e93fc2065a13e3`: the same Shop/transition selector
returns **297 passed, zero skips**, 123.44 seconds. This includes 14 connected
tests and the read-only CLI/committed-receipt guard. Ruff lint, format and diff
checks pass; the detached checkout remains clean. The final commit after this
coordinate only appends this validation result, with no implementation or
receipt-byte change.

## Shipment explanation successor

RED `c363ffc5971e03e8c6e10c147e9333ac2548d55b` records the Shop-only scope and
18 missing-reader errors. GREEN `b28b2ffe4cef0c029707508884133ad630b774c2`, tree
`7083bfdc961700936fdcc151d88ba532c77a3c31`, adds the reader, its explicit source
and rule specification, and two additional context-retention guards. The focused
suite is **20 passed**, zero skips. No existing population, ontology, source,
mapping, historical receipt or Core implementation changed.

A local detached clone at exact GREEN, retaining Git objects but no shared
worktree dirt, ran the same whole-Shop plus transition selector above. Result:
**317 passed, zero skips**, 145.00 seconds. Dependencies are the existing
declared repository environment; no installation or packaging work was done.

A separate from-empty run in that clone reproduced the existing history digest
`sha256:1c989c554b9aa68e97226c0efc6355496723613f17e901bb7689a4c4da28acbe`,
head, replay receipt and all 107 historical records. The reader's after-e28,
after-e30 and final reports reproduced identically after reopen. Their exact
digests are retained in [shipment_explanation_receipt.json](shipment_explanation_receipt.json).
The later documentation/receipt guard checks those exact values against a fresh
history. It does not change the implementation or historical receipt.

The read-only CLI is executed in the tests. Actual source data returns
`CANNOT_DETERMINE` for the unpaid limit, both before and after the two invoice
clearings. Missing invoice, receipt and relation evidence cannot shrink the
selected inventory into a passing result. Synthetic explicit PAID/UNPAID inputs
separately distinguish SATISFIED, VIOLATED and incomplete evidence. They never
enter the source history. Checkpoints are accepted import positions, not domain
times, and the full retained commentary is labeled as such.

This proves the bounded payment explanation and reproducible read results. It
does not prove a complete customer account, historical unpaid balances, causal
delay, shipment permission, source truth or every part of the connected Shop
plan. No full-Core, package, external-effect, push or release claim follows.

Final detached gate at `07b8fe3a6f44dca07326b0b7e97b023416eca981`, tree
`0ca4cedbb8579574835f16049c3f64b03c978980`: **318 passed, zero skips**, 146.29
seconds, with the same whole-Shop plus transition selector. This includes all
21 shipment-reader cases and the committed three-report receipt guard. Scoped
Ruff lint, formatting and diff checks pass; the isolated checkout remains clean.
The later commit only appends this result. Source/history inputs and the earlier
run receipt remain byte-identical, and no Core path changed.

## Per-object reader successor, 2026-09-14

RED `03fd5bcb` records 12 missing-reader errors and the approved source-trust
assumption. The implementation introduces only a Shop read specification and
reader over existing public APIs. It does not modify source, ontology, mapper,
admission configuration or earlier receipts.

Focused command in the declared repository environment:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/test_object_timelines.py
```

Result: **14 passed, zero skips**, 93.26 seconds. An initial test incorrectly
counted 18 objects; exact enumeration of the retained columns gives 17. The
test now names the entire independent inventory. Another test initially used
`history_sha256` to read the existing receipt's `ledger_sha256`; its corrected
lookup verifies the same frozen history bytes. No runtime bypass was involved.

The final tests execute two from-empty connected histories. One checks the
reader, source witnesses, committed receipt, exact reopen and actual read-only
CLI. The other opens a maintained reader before the first domain admission and
compares it to full replay after each of the 21 admissions. The existing
shipment explanation also agrees at the e28, e30 and final checkpoints. This
closes the earlier final-checkpoint-only limitation for these selected reads,
not for arbitrary readers or arbitrary admission permutations.

The original history digest remains
`sha256:1c989c554b9aa68e97226c0efc6355496723613f17e901bb7689a4c4da28acbe`.
The new read-report digest is
`sha256:afc5072a5f8cd1e5988874d3c2d1d5423f5af25f34f23c90eb07508fb81254b6`.
The exact binding is in [timeline_receipt.json](timeline_receipt.json).

The 21 occurrences are referenced from 17 enduring-object views. e30 stays one
occurrence shared by I1, I2 and P1. e6 and e8 stay unplaced, with their original
printed strings. Ties are unordered groups. The report states its relative
printed-coordinate convention and makes no calendar, duration or causal claim.
Supplier A and B remain separate views; no flattened supplier history is built.

Scoped Ruff lint/format and diff checks pass. No Core, packaging, release,
external execution or full-repository gate is claimed. The isolated combined
Shop regression result is recorded below after the implementation is frozen.

Isolated final gate at GREEN `993ce04b704b99d922fdef0d9015f971467f09a8`, tree
`1cd6a23f9cd8184d1bc222f04609152f2652f396`, from a clean detached local clone:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_transition_admission.py
```

Result: **332 passed, zero skips**, 256.40 seconds. This includes the 14 reader
tests; do not sum overlapping selectors. The clone remains clean. Scoped Ruff
lint, format and diff checks pass. The entire change from the previous main
boundary touches nine Shop files only. Core, ontology, dependencies, original
source and mapping, producer, original history receipt and earlier shipment
receipt remain byte-identical. This is not a full Core or installed-package
gate. No push or release was performed.

## Warehouse source extension, 2026-09-14

The accepted continuation adds Figure 14 of the same chapter, not invented
warehouse data. The unchanged publisher PNG and a manually inspected JSONL
transcription retain 13 occurrences and 52 nonempty fields. Attribution,
CC BY 4.0 licensing, source URLs and exact digests are in
[warehouse/source_boundary.json](warehouse/source_boundary.json). Digests prove
byte identity, not transcription truth; no independent human audit is claimed.

RED `3aa8f7f48ee3f22103b8470e318584b3113e03a9` has 10 missing-module errors.
Before that recorded RED, a test import mistakenly used pytest's empty package
name; it was corrected to the existing Shop module's package. The later test
commit `567acda404ff94cc11dc885902801e4774467468` adds an actual schema-inspector
and read-only command-line check. Against the working implementation that check
exposed Python tuple paths versus JSON array paths. The runtime now emits lists
in the report, and the same check prevents representation drift. This second
failure was observed in the working tree, not an immutable missing-code RED.

The schema introduces only three activity values, SCAN, STORE and RETRIEVE.
One public contract revision and 13 checked changes extend the original ledger.
All 895,257 baseline bytes remain its exact prefix; all earlier graph and
record-history entries remain unchanged. The result has 34 occurrences, 75
participations, 17 enduring objects, 34 domain changes and 193 protocol events.
Every new property traces to its retained row and field. No new actor, machine,
unit, order, year or timezone is supplied by this source or inferred here.

The final from-empty CLI run contains 1,646,996 bytes at
`sha256:ae9bbf870fd928e96de9f62c54a43d05575929b2546bb1e4376ecc9b8191cc06`.
Its read report is
`sha256:52f2141be794b9d9b1a5db06013cc50cffd7bb282227bb34f6ff713286638cc3`.
The full machine-readable coordinates are in
[warehouse/receipt.json](warehouse/receipt.json).

Tests distinguish unknown units and extra fields, require exact prefix
preservation, refuse a repeated append before writing, inspect source witnesses,
exercise the actual public schema command and read-only CLI, and compare reopen
with maintained replay. A maintained reader opened before the schema revision
is refreshed after the 13 new changes and agrees with full replay. This is not
an after-every-new-row refresh claim. The original payment explanation must
remain unchanged except for its history checkpoint.

X1 now has observed Scan, Store and Retrieve steps between Unpack and Pack. Y2
is scanned before Y1 although it was unpacked later. Those paths support the
next bounded comparison with the chapter. Missing Y1 warehouse steps, unusable
old dates, amounts and invoice correction values stay missing. No elapsed-time,
complete FIFO, causal delay, real warehouse execution or source-truth claim is
made. Each change is atomic; whole-import rollback and interrupted-import
resume are not implemented. Core, dependencies and earlier receipts are
unchanged.

Focused command in the declared repository environment:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/test_warehouse.py
```

Result: **12 passed, zero skips**, 92.33 seconds. Scoped Ruff lint, formatting
and diff checks pass. The isolated whole-Shop gate is recorded below after the
implementation is frozen. No full-Core or packaging gate is claimed.

Isolated whole-Shop gate at GREEN
`557adf6f38e591fe22cb163fabc43e2be54c037e`, tree
`19b5e3856e29807253f6df20a48c9017cd4ff1b6`, from a clean detached local clone:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_transition_admission.py
```

Result: **344 passed, zero skips**, 354.15 seconds. This includes the 12
warehouse cases, not an additional 12. Its fresh run reproduces the committed
receipt exactly, including the source-bearing ledger and JSON read report.
Scoped Ruff lint, formatting and aggregate diff checks pass. The detached
checkout remains clean. The aggregate cut changes 13 Shop paths only. The final
documentation successor appends this result and spells the printed date format
explicitly; it changes no executable, source, schema or receipt bytes. No Core,
dependency, package, remote push or release change was performed.

## Warehouse ordering comparison, 2026-09-14

Luis selected a bounded comparison with section 6.2 of the chapter. The
remaining three extensions are TODO in the existing Shop plan. This piece
adds only a read-side report and its selected-unit/stage specification; the
warehouse history, sources, schema, mapping and previous receipts stay exact.

RED `8c50e8717ad4c72be10a9ffeac8ec02a5ae20203` changes the plan and adds
`warehouse/test_ordering.py`. All 14 tests fail with the missing ordering
module, in 0.55 seconds. The minimal implementation reuses the existing
printed-coordinate ordering and public replay/source trace.

Focused GREEN command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/test_ordering.py
```

Result: **14 passed, zero skips**, 95.85 seconds. Eleven cases distinguish
ordering behavior over controlled views, including reversed order, ties,
unusable times, repeated stages, missing units and observations, backward
stage order and iteration-order independence. Three cases rebuild the real
history, inspect every compared observation's source/unit witnesses, and
compare full reopen, maintained replay and the read-only CLI. Every read
preserves exact ledger bytes. The committed new report receipt reproduces.

Across five selected units and ten pairs per queue: Unpack-to-Scan has five
preserved pairs, one reversal and four undetermined; Scan-to-Store and
Store-to-Retrieve each have six preserved and four undetermined. All three
have partial coverage. The Y1/Y2 reversal is reproducible. The X3 unpack time
and absent Y1 Store/Retrieve remain explicit limits. No full FIFO, elapsed
duration, causal explanation or counterfactual result is claimed.

Scoped Ruff lint/format and diff checks pass. The isolated whole-Shop gate
at the frozen implementation is recorded below when complete. This is not a
Core, package, independent human interpretation or publication gate.

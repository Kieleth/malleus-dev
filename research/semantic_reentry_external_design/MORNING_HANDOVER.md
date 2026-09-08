# Semantic Re-entry: morning evidence handover

Snapshot: 7 September 2026, 07:15 America/Los_Angeles. The overnight watch
continues until 08:00; this is not an observation of the later cutoff.

**External Re-entry E2E: NOT PROVED.** The completed work establishes a real
replay counterexample, reviews the Core action definition and records concrete
Robotics constraints. It does not implement the missing external action path.

This handover summarizes existing CONFORMANCE_FIXTURE evidence under the
compiler-enabled semantic-history/state-version profiles. The external action
contract remains a proposed OPTIONAL_PROFILE; the supplier policy is an
ADOPTER_CHOICE. No additional protocol guarantee, second action consumer or
replaceable implementation is claimed. The Malleus development and inquisitor
rules kept those claims separate. The scoped review remains in this research
directory, without modifying Core, root audit files or paper work.

## What was actually observed

| Boundary | Result | Exact scope |
| :--- | :--- | :--- |
| Canonical KCS serialization | PASS | Every accepted KCS in the replay witness survives exact object/byte round-trip. |
| Log replay is not invertible | PASS | Independently reopened histories have 28 and 29 events, different heads and receipts, but the same complete current KG and accepted KCS sequence. |
| Source-backed internal correction | Exercised | The witness consumes the existing e4-to-e7 correction. The source was already retained; it is not a newly observed supplier action. |
| Core action definition | Shape and binding checks PASS | The packet does not yet supply complete event programs or executable producer implementations. |
| Robotics comparison | Read-only evidence audit | Its assessment/replay pilot and failure-accounting witness are not an integrated ActionProposal/controller path. |

The replay witness preserves B/Y/2, the unchanged complement, source bytes and
record history. Its extra event retains an explicitly authored conformance
note, not a new supplier observation. See [the proof](REPLAY_NONINVERTIBILITY.md)
and [the exact result](replay-noninvertibility-result.json).

One actual harness defect was found and guarded: pytest initially imported the
wrong Core checkout. That apparent pass is excluded. The corrected invocation
selects the exact configuration; preflight checks module origin, the pinned
commit and tracked tree, and the witness checks the retained compiler producer.
The original faulty invocation now refuses before fixture setup. A hard negative
test rejects another checkout. No failed or excluded run was rewritten.

## Test evidence, not an aggregate score

| Retained run | Core pin | Observed result |
| :--- | :--- | :--- |
| New replay witness and origin guard | `2af45e03ee7d7bf528cef8db42c0798e6d99685b` | 2 passed |
| Unified relevant replay/consumer/compiler selection | Same `2af45e0` | 112 passed, including the two above |
| Independent action-definition review selection | `63e1c3bcc6df9a161f177fa70e8c0e6f39d237d1` | 140 passed |
| Successor readiness/binding assertions | `ae434b5b54b4d1f76440586fddb270b0543a09fe` | 3 passed |

These four retained JUnit files have zero failures, errors and skips. They were
read and hashed during this handover, not rerun. The 140-test result belongs to
`63e1c3b`; only the three changed checks were independently run on `ae434b5`.
Paper separately reported reproduction of the two replay tests, not the whole
112-test selection. Robotics test counts remain owner-reported, not our runs.

The older compiler prerequisite is BOUNDED_COMPATIBILITY_PASS, not raw full-suite
GREEN: its repaired run retained 1165 passes, nine exact historical receipt
mismatches and one existing xfail. No original receipt was replaced to make the
suite pass. See [the independent gate report](COMPILER_GATE_CHECK.md).

## Exact remaining gate and ownership

The outstanding operator decision is R1 in
[CORE_DEFINITION_REVIEW.md](CORE_DEFINITION_REVIEW.md): whether the proposal must
immediately follow registration of its pinned original context. This was asked
once; there is no recorded approval. Atomic grouping and orphan-registration
behavior must also be explicit in the resulting contract. Persistence is not
authorization to choose those semantics.

Core next supplies the dependency-closed definition: complete event programs,
operand and index resolution, monitor input/output contracts and typed refusals.
The ten-instruction vocabulary remains a candidate until those programs express
the full lifecycle. Exact producer code is not yet available. The corrected
readiness wording permits failing tests before implementation; it still requires
real implementation identities before any successful execution claim.

After the contract and authority gates close, Core owns generic implementation
and its guards. This thread consumes those exact interfaces for synthesis, the
controlled synthetic supplier-file executor, independent capture and observed
source-to-existing-KCS adapter. The decisive sequence remains:

```text
accepted B/Y/1 -> pinned proposal -> authorization and one effect attempt
-> actual source capture -> ordinary KCS acceptance -> JSONL-only replay
-> accepted B/Y/2 with preserved complement -> no candidate and no further write
```

Execution receipts and observations cannot themselves change accepted quantity.
The hard cases still need real action-runtime tests: stale context, unsupported
operations, ambiguity, direct graph access, pending versus satisfied, success
with unchanged bytes, failure after a real write, refused KCS and quiescence.
An oracle file cannot stand in for a capture. A failed attempt cannot disappear
from a resumable summary and restore the one-attempt budget. The last constraint
is reinforced by the [Robotics audit](ROBOTICS_REENTRY_MAP.md), not newly proved
for the missing action runtime.

## Audited coordinates and landing order

Consumer baseline: `f221c0994df530170c80726be29ff876d3dd195e`, tree
`2bad91898a27618107997c526f9cbc99cbaf5c2b`.
Audited overnight head: `828aac44baf9279c23de52e0d93f9670cd4e305c`, tree
`5f6058630a25838307f35ebadaea525b31030536`.

The exact base-to-head diff contains six added files, 950 lines, all under
research/semantic_reentry_external_design. The only added Python file is the
181-line replay conformance test. No production, ontology, locked fixture,
dependency, paper or unrelated path changed. The tracked/untracked status and
base-to-head whitespace check were clean. All six file contents were inspected.
This handover and its plan pointer are a later documentation-only addition.

The six research commits, in dependency order, are `9a58729`, `51bb72a`,
`fd5c294`, `86c6249`, `a7c0666`, `828aac4`. They build on `f221c099`.
Their reports retain their original Core pins; landing the evidence must not
silently rebind its test to a newer runtime. No merge, push or publication was
performed. This is an evidence landing order, not a runtime-ready release.

Current owner checkouts were clean and unchanged at inspection:
Core `ae434b5b54b4d1f76440586fddb270b0543a09fe`, tree
`7beabc42555fe0a8a7bb8875b82f5f9a89a13569`; Robotics
`7b481232e5d32f111a212fc2a202c6488ae97801`, tree
`73c2872076ad4953023e869f2ae10ea40ae4b9e7`.
No fresh executable handoff was present. Neither owner was restarted merely
to acknowledge unchanged state. No external call or physical effect ran here.

## Rechecked SHA-256

Files below are the exact bytes at the audited consumer head `828aac4`.
The plan gains a pointer after that snapshot; its row is not a successor hash.

| File | SHA-256 |
| :--- | :--- |
| CORE_DEFINITION_REVIEW.md | 8f11fd3d295051d5cd67ca492702363bf3649cb2e47f993d6fb1aa1c4f004151 |
| OVERNIGHT_PLAN.md | ab78c94702bd272eec8ab06a035c8a13d30460a995ddd41d32663207245afd1f |
| REPLAY_NONINVERTIBILITY.md | 12f2158525d78a067225b1155e39fcee9cc266711092dc119d473bf25712f887 |
| ROBOTICS_REENTRY_MAP.md | 1b78a040a46b105740a018721cab36726ee49569e8012a0d4297be22b72484a9 |
| replay-noninvertibility-result.json | e30ae4e6fc4b194b9a2fb49bca01bd776a667254c28c5b0ccfd724b408da4d0f |
| test_replay_noninvertibility.py | 8cd5eea6de67ca085cf2848820660809e40e70fbf276e44a65784e5e9d882200 |

The raw ledger files remain under
`/private/tmp/malleus-reentry-replay-law.5vrGQQ/final-run/test_distinct_histories_share_0`:
short-ledger-only/history.jsonl is
`4351970225ff5562d0a59d6eb2257acfbe70094e5a8bb5f6f7177da50264c928`;
long-ledger-only/history.jsonl is
`2b7a752ec5360f09775ccde733078f69f4a613fb4c41702f7ba45df13594f379`.
Both match the retained result. JUnit paths and hashes:

| Absolute path | SHA-256 |
| :--- | :--- |
| /private/tmp/malleus-reentry-replay-law.5vrGQQ/final-focused.xml | 4f2349876fa4790bfc297fa7f280d54c1f9912ae3ce24e65eae34d8eff6c549d |
| /private/tmp/malleus-reentry-replay-law.5vrGQQ/final-relevant-gate.xml | 3201f5c926240b80f2e42b1610c7b239138aaed8f459facab455a1bbfdf7b351 |
| /private/tmp/malleus-reentry-definition-audit.EK2FnT/independent-focused.xml | 9e34a03d7a7501077b56151d8efa79edd2e9b87c5345e0fa9f3bddf1c1fe9cbe |
| /private/tmp/malleus-reentry-readiness-audit.bfd2NY/targeted.xml | 829374e04bdfa4ad8b3866e1c7a1601c1ac0d81e13a8b4a2560eded31f2f43ad |

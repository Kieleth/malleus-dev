# Current-Core landing

Status: VERIFIED, READY FOR CORE-OWNED MAIN LANDING. This is not a merge-to-main
receipt. The historical proof and walkthrough receipts remain unchanged; their
earlier statements describe their original coordinates. The adjacent
`current-core-landing-result.json` binds this verification and its exact files.

## Bounded integration contract

Claim: the completed single-action supplier proof and runnable walkthrough
compose with current Core without changing protocol meaning or implementation.
The stages remain REFERENCE_IMPLEMENTATION under the compiler-enabled
state-version and experimental single-action profiles. Tests and this landing
evidence are CONFORMANCE_FIXTURE. The exact-two goal, operator and preservation
policy remain ADOPTER_CHOICE. No guarantee is promoted to a base invariant.

Smallest observation: the same real source/proposal/effect/observation/KCS/replay
loop passes with current Core, preserves the complement, and ends quiescent.
The existing negative tests must still refuse unauthorized graph writes, stale
inputs, unsupported or ambiguous synthesis, and receipt-as-observation errors.

Reuse: the completed proof at `dfa40981f6d537c81f2397b5c40be54c6ff5ae57`,
the existing public compiler/history owner, and the selected finite programs.
Core's new action-input constructors are additive. This landing checks their
coexistence but does not claim the supplier adapters delegate to them. The
graph-free synthesis input is not replaced with an owning history handle.

Exclusions: runtime refactoring, new ontology or identities, additional goals
or actions, retries, delivery, production suppliers, Robotics, paper changes,
new dependencies, remote calls, package release and push. No architecture
choice or failed production behavior requires a new repair in this integration.

## Isolated merge

Checkout: `/private/tmp/malleus-reentry-merge.8hAxQB/repo`.
Branch: `codex/semantic-reentry-landing`.
The local clone captured Core `39f9566e2f612175c016680349a00cde80dc8afc`,
which advanced from the initially inspected `0cdf8ed` while Core was working.
Merge `a857ef01e96b4717b7aa764cc96b40c8456b2e54`, tree
`4309ffb4f7c561a2f7fa46d0b83c2234b780c861`, has that Core commit and the
frozen proof tip as its parents. It required no conflict resolution.

The 98-file Re-entry diff contains only its research directory and the 23-line
adopter-skill addition. Core runtime and ontology bytes are unchanged from the
proof pin `90146c380994621a2f8df25876affd03fc9e57e3`; the source tree remains
`763d3b72ad2143bc5735eed32d47a69e3f6b8cd1`. Historical pins are not rewritten.

Fresh verification selects every module in `supplier-reentry-gate.json`, the
standalone walkthrough tests, Core's new `test_action_inputs.py`, and the two
existing installability/guidance test classes. Its retained JUnit and temporary
artifacts live in the new isolated parent directory, not the old evidence root.
Ruff and format checks pass for all 33 Re-entry Python files.

## Final verification

The fresh combined gate passed 426 tests, with no failures or errors and one
existing skip: the private paper-program doctrine is absent from this clone.
This includes all 394 proof/walkthrough tests, eight Core input-builder tests,
and 24 passing guidance/installability tests. These are disjoint parts of this
one run, not sums of earlier runs. JUnit SHA-256:
`3f5c8ccce6c65930548f51d6137fd12050874b547f8afcaed5a052e4add670ee`.

Core finished at `f3bcb620076da560476b3facdc3bf45dd7f214c4`, tree
`9eb580c94119627510e15e2b33749ec344c3f23b`. Synchronization merge
`896ddad5e90e61dcca4804dff3f0e76d3b58f0e4`, tree
`fc2365d38357a5964641b37468f64ecfd1c450ae`, incorporates it without conflicts.
Core's intervening shipment fixture, documentation and governance changes do
not change the tested runtime, ontology, action producers, package configuration
or guidance-test code. A fresh post-synchronization focused run passed 27 tests
with the same one skip: the two guidance classes plus all three replay-law tests.
The combined runtime run remains bound to `a857ef0`, not relabeled as a later run.

All four new lifecycle ledgers and all 14 standalone walkthrough artifacts are
byte-identical to their historical counterparts. The 92 original proof files,
their ten external artifacts, and all 22 walkthrough manifest entries match
their retained hashes. Historical evidence roots were not reused for pytest.

Scoped self-inquisition: PASS for compatibility of the declared optional
profiles. `protocol_role_is_explicit` and `optional_profile_stays_optional`
remain satisfied. No reference implementation or fixture acquired Core
authority. No new defect required a code repair; existing hard negative tests
remain unchanged and pass. Root-ontology rites, full repository CI, independent
replacement, package release and real supplier integration are not claimed.

Before main changes, synchronize the exact Core head, inspect any intervening
diff, append the skill's exact document revision through Core's existing
governance owner, and verify that ledger and integration gate. Do not overwrite
Core's concurrent work, accept an unbound skill digest, or call branch-only
integration a main merge. The skill changes from SHA-256
`4c74a274c52e34feff3493f9ee935fea908c6914e83a0006ba0918f260f9c06d`
to `e20f33af0159be22bbe16877fe4c28ce038aee93dad6c713447be3da641c65c6`.
Core owns the corresponding append and final landing receipt. No push is
authorized by this handoff.

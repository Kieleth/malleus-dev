# Executable-contract freeze: exact blocker

Status: BLOCKED on a public compiler input prerequisite. The approved semantic
cut remains in force; no action runtime or substitute contract is implemented.

The operator approved using the semantic draft at `7d64747` as the basis for
the executable contract: separate action and KCS acceptance, explicit action
initialization, a bounded one-consumer Core exception for this proof, equality
to two, one action attempt and independent capture. This permitted artifact
definition, not interpreter/writer implementation, merge or push.

## What could be frozen

The [supplier fixture](fixtures/supplier_commitment_v1/README.md) now fixes the
exact one-row initial source, separately authored expected output, goal,
stable episode/action key, operator, mapping, preservation and expected
outcomes. Its closed source-row schema rejects missing/extra/mistyped fields
without supplying defaults. This is source/oracle conformance only. Expected
output remains under `oracle`, never available as a pre-observed input.

There are no invented runtime heads, policy producer hashes or compiled
contract identities. No action subtype or runtime instance is frozen around
the missing input. Existing canonical Shop fixtures and all prior audit/design
files remain unchanged.

## Why the executable contract cannot be frozen

Core compiled both the exact shipped Assent ontology and a tiny independent
adopter importing it through public `compile_linkml_contract`. Both refuse
`INVALID_RANGE` for the `calendar_date` slot's LinkML `date` range. The current
compiler seed scalar set is boolean, datetime, float, integer and string.
The existing registry loads that closure; an Entity-only public compilation
control passes. This is a support-boundary mismatch, not an environment or
supplier-source failure.

Core's immutable reproducer:

- Commit `28cd4b7f608eae18a771fe14afe6d3ff8be6815c`.
- Tree `750c2db782d424af175ff35e4ae68a43d0513f97`.
- Base `2a11240556532c2b6160ac0bfa5ab1165e862fd2`.
- Packet `research/action_history_contract_freeze` in that commit.
- README SHA-256 `8e0ebcb3642de9b66e56ca3a3a7540587bd6adae6e2ce70ad67a37c94f6b9919`.

The compiled action record identity, initialization/O instances, versioned
machine/binding closure and positive lifecycle fixtures remain UNFROZEN.
Passing the existing refusals is not action-runtime GREEN. Date is the first
observed incompatibility, not proof that correcting it closes every import.

## Verification and scope

New source/oracle checks: 16 passed. Their initial availability RED had four
failures and twelve setup errors from absent input/schema files. Final combined
selection: 52 passed in 14.96 seconds, consisting of the new fixture tests,
the eight existing seam probes, existing generic-effect tests and landed
Re-entry integration/guardrails. Changed-file Ruff and format checks pass.
The full repository/runtime gate was not repeated for this fixture-only cut.

Core independently reports 15 blocker probes and 67 tests in its selected
combined gate, with no skips or xfails. Those results belong to its packet;
they demonstrate existing support/refusal boundaries, not the proposed loop.

No source/ontology/runtime/package/governance/paper change, installation,
external-domain call, shared-main integration or push occurred. The only new
Python file here contains fixture tests, not a synthesizer, monitor, mapper,
executor, observer or protocol validator.

## Smallest decision needed

Authorize Core to perform a separate bounded TDD compatibility correction so
the public compiler can consume the exact required Assent closure without
weakening its range or record semantics. Re-run those exact imports and check
the selected structured records. Any further unsupported semantic feature
must be surfaced before expanding the fix.

Do not strip imported declarations, replace date with string, silently use
the registry instead of the compiler, or manufacture a compiled digest.
A lossless selected-record projection is an alternative requiring a separate
coverage/authority decision, not an assumed workaround. After the input gate
closes, resume the already approved contract freeze. This document does not
authorize that compatibility fix or the later action runtime.

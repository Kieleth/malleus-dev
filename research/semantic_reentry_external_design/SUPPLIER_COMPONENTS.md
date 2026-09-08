# Pure supplier components

Classification: REFERENCE_IMPLEMENTATION of the approved ADOPTER_CHOICE
equality-to-two, one-operator scenario. Tests are CONFORMANCE_FIXTURE evidence.
The lowest consumption profile is compiler-enabled population/state-version.
There is no action-runtime or package/API promotion claim.

## Before implementation

Claim: explicit source bytes plus the frozen rule suffice to predict the narrow
amendment and independently map a supplied replacement row to existing
population-plan fields. No component receives a graph, ledger, file, executor,
observer, clock, callback, receipt or admission capability.

Distinguishing observation: the model predicts B/Y/1 at e4 becoming B/Y/2 at
reentry-amendment-1, preserving the other fields. Mapping authored replacement
bytes compiles against the real public population seam without changing the
accepted B/Y/1 graph or its history. Missing bytes, ambiguous rows and a success
receipt do not substitute for a source row.

Reuse: the unmodified supplier_commitment_v1 fixture, SupplierOrderState,
explicit supersession, ORDER_ONLY, row locators and the existing neutral
population-plan grammar. There is no new change identity or Re-entry Contract.

Excluded: source capture/authentication, truth or causal attribution, actual
effects, ActionProposal production, synthesizer integration, authorization,
admission, stale-ledger handling, pending/retry policy, replay quiescence and
full external Re-entry E2E. These remain separate Core/lifecycle obligations.

## Function boundary

`model_amendment(before_bytes, *, source_sha256, goal, operator)` consumes the
goal and operator objects already present in the fixture. It returns predicted
canonical UTF-8 JSONL bytes, or None when the supplied row already satisfies
the goal. Only the declared integer 1 to 2 amendment is supported. The source
digest is checked before satisfaction. That is a byte precondition, not proof
that a caller's claimed digest belongs to an accepted ledger head.

`map_observation(observed_bytes, *, before_bytes, source_sha256, goal, operator,
mapping, source_id)` independently validates the supplied row and preservation
condition. It returns canonical JSON bytes containing only existing `records`,
`sources`, `derivations`, `supersessions` and `valid_time` fields, or None for
an unchanged row. The caller supplies the rest of the existing plan, including
real contract/profile and evidence identities. A fragment is not a submitted
plan, KCS or public protocol artifact.

Both functions reject missing/unknown rule fields and malformed source values.
Inputs are one UTF-8 JSON object on one nonempty JSONL row. Duplicate keys,
non-finite numbers, bool quantities, empty identifiers and multiple rows refuse.
The mapper supports integer replacements 2 and 3 at the declared new occurrence,
unchanged order/product and complete four-field mapping. It cannot infer
initial-state admission or supersession authority from a supplied record ID.
The public compiler remains responsible for checking that ID against its base.
Mapping 3 preserves an undesired observed value; it does not change the model's
strict one-to-two action or establish goal satisfaction. Other replacement
quantities remain unsupported in this bounded adapter. See
[the mismatch slice](OBSERVED_MISMATCH.md).

Refusals are local SupplierInputError values with a reason string. They are not
Core protocol events. Input dictionaries are not mutated, and outputs are
immutable bytes with deterministic field/derivation ordering. Plan fragments
have no trailing newline; model JSONL has one. Runtime code never reads the
fixture, expected-output oracle or an implementation file to discover identity.

## Evidence limits

The compatibility test explicitly retains authored fixture bytes in temporary
history before compiling. It neither calls the model to manufacture an
observation nor admits the compiled result. The oracle remains expected output,
not evidence of an executed action. A None result here means source-level
no-change/satisfaction only, never fresh-ledger lifecycle quiescence.

The model's frame condition covers the other source fields. The compiler check
also verifies the current KG and ledger remain byte-for-byte unchanged. It does
not prove complement preservation after admission. No operational producer
identity is bound here; the evidence harness hashes the exact implementation.

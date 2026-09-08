# Action inputs on an adopter-owned history

Luis approved this extraction after the clean Core suite at `386bb42` and
the read-only constructor finding recorded at `1189190`.

## Bounded contract

Classification: REFERENCE_IMPLEMENTATION of the already selected experimental
finite action profile. The new module is repository-local. It is not a public
SDK, new interpreter, protocol invariant or new domain vocabulary. Shop and a
non-Shop history are CONFORMANCE_FIXTURE witnesses. Domain history, selected
programs, sources, policies, actors, timestamps and action meaning remain
ADOPTER_CHOICE inputs.

The claim: one reference producer constructs existing source-registration,
initialization and context/proposal inputs against a caller-owned
`KnowledgeChangeHistory`. It never creates a history, runs Shop, selects a
policy, checks an action, admits a change or performs an effect. Its outputs
remain proposals for the existing owner and selected finite transactions.

The caller first creates/populates its history, retains/selects exact finite
program bytes and registers its chosen prerequisites. The producer reads the
verified replay and exact registered source/policy identities. It accepts
explicit IDs, actors, clock values, source metadata and a caller-built action
record. It emits the existing checkpoint/context bytes and event dictionaries.
No new persisted grammar or initialization migration is introduced.

Reuse: `make_record`, source byte metadata, canonical serialization, the
selected registration/initialization/context programs, and the owning
`append_protocol_events` gate. Initialization remains its existing transaction;
context and proposal still commit together or neither commits. This does not
claim an atomic multi-transaction bootstrap.

Smallest RED: compile/populate a non-Shop domain, prepare real prerequisites,
then invoke the new producer and owning admission in a fresh process that
refuses test and Shop imports. Require exact custom source retention, explicit
metadata, unchanged domain state, atomic context/proposal admission and reopen.
Missing roles/records must refuse clearly; stale or malformed submissions must
preserve ledger bytes. Existing Shop initialization/proposal helpers must
delegate to the same implementation, with the two-action history unchanged.

The prerequisite fixture may reuse existing test builders to prepare the
isolated input prefix. The producer and its fresh-process caller may not import
those builders. Registration of adopter-specific monitors/policies and actual
check execution remain outside this extraction.

Dependency sketch:

```text
selected finite action profile -> governs action input producer
owning history + retained prerequisites + caller action -> consumed by producer
existing checkpoint/context/event inputs -> produced by producer
existing owning finite transaction -> validates and persists inputs
Shop + independent domain -> exercise the same producer
```

## Pre-action checks and exclusions

No server interaction, endpoint, installation, package change or external
effect. Required inputs have no guessed defaults. Remove the old checkpoint
and context assembly from the test helpers, leaving only fixture input choices.
Guard the observed coupling class with a non-Shop, no-test-import witness.

No Robotics domain records, second ledger, new machine instruction, new policy,
recovery, implicit legacy fallback, stable-wire claim, SDK promotion, consumer
merge or remote push. This proves reuse by two fixtures, not replacement by a
second implementation. Performance debt from the prior full suite is separate.

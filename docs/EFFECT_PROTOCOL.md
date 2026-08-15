# Authorized Effect Protocol

Malleus records a generic path from authorization to an externally observed
outcome. Domain adapters perform effects. Core Malleus never reads payment,
deployment, email, or other domain payload fields.

## The three records

```text
AuthorizationDecision(AUTHORIZE)
  -> ActionDispatch
  -> ActionExecution
  -> OutcomeObservation
```

`ActionDispatch` is the protocol gate. It binds the exact action, authorization
decision, authorized executor, dispatch adapter, acceptance head, and dispatch
time. Replay refuses it after `BLOCK` or `CLARIFY`, for another actor, after the
authorization expires, or after another dispatch was already recorded.

`ActionExecution` is the domain adapter's terminal receipt. It binds the exact
dispatch, executor, start and end times, terminal status, and a digest of the
adapter result. It contains no domain fields.

`OutcomeObservation` is a separate actor's post-execution attestation. It
binds the exact execution, a content-addressed `OutcomeContractArtifact`, and a
content-addressed `SourceArtifact` containing the external state that was
inspected. Its result is `CONFIRMED`, `CONTRADICTED`, or `INDETERMINATE` under
that contract.

For the research adapter, the effect source is the exact bytes of
`payments.jsonl`. The outcome contract says what condition the external
observer checks. Core Malleus sees only hashes, IDs, times, actors, and the
three-state result.

## What the observer proves

An observation proves this bounded statement:

> This identified observer, using this pinned contract, reported this result
> after inspecting these exact registered bytes for this exact execution.

It does not prove that the external state is authentic, that the observer is
honest, or that the observation contract correctly captures the domain. Those
remain separate empirical and trust questions.

## Delivery profiles

Replay permits one `ActionDispatch` per authorized action and one
`ActionExecution` per dispatch. This prevents duplicate recorded protocol
transitions. The Stage 8c profile governs and records the path through dispatch,
receipt, and observation. It does not select an external delivery guarantee.

A process can write an external effect and crash before recording its receipt.
An optional stronger profile can close that gap by binding an idempotency key,
transactional outbox, adapter deduplication record, and external effect ledger
to the same action and dispatch. Those records can extend the protocol without
putting domain payloads or effect execution into core Malleus.

The current profile is therefore the plain composable layer: one governed
dispatch, one recorded terminal receipt, and one recorded outcome observation.
Exactly-once effect delivery is future profile work, not a universal guarantee
required from every Malleus consumer.

## Failure boundary

No authorization means no valid dispatch record. The reference research
adapter must require that record before touching its effect store. A failed or
aborted adapter call still records a terminal `ActionExecution` receipt when
the caller can persist it. Storage failure remains fail-closed: an invalid
dispatch, execution, or observation event changes no ledger bytes.

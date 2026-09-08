# Independent supplier source capture

REFERENCE_IMPLEMENTATION under the existing experimental one-action profile.
The controlled source, observer selection and equality-to-two observation policy
are ADOPTER_CHOICE. Tests are CONFORMANCE_FIXTURE. This is the next stage contract,
not an executed observation result or a new public protocol object.

Claim: a separately identified observer reads the actual controlled source after
an applied execution, retains those exact bytes and records the existing
OutcomeObservation. The smallest observation is CONFIRMED after actual B/Y/2 with
the declared new occurrence, CONTRADICTED for the unchanged valid source, and no
domain-state change in either case. FAILED execution can coexist with CONFIRMED
observation; neither failure nor causal uncertainty is rewritten.

Reuse existing SourceArtifact, OutcomeContractArtifact, OutcomeObservation,
outcome_contract_digest and Core's source/outcome-contract/observation transactions.
No caller-supplied observation verdict, model prediction, execution result payload,
expected-output file or historical e7 source supplies captured bytes.

`register_supplier_observer` takes owning history, expected ledger head/count,
implementation SourceArtifact ID, outcome-contract ID, actor/time and artifact
version. It retains actual loaded observer implementation bytes, then the existing
outcome contract identifying their digest and OBSERVED_SOURCE observation type.
Both registrations use the normal Core gates. The implementation is separate from
the executor and model; this is not proof of independent trust or world truth.

`observe_supplier_execution` takes owning history, expected head/count, execution
and outcome-contract IDs, observer ID, fresh observed-source and observation IDs,
observation time, explicit absolute controlled source path, logical source ID and
artifact version. Both functions have only required keyword arguments and return
existing Core replay. No new observation, change-set or permission identity is added.

Before capture, verify applied execution/dispatch/action and outcome contract,
actual loaded observer identity, source binding, observer distinct from executor,
aware time no earlier than execution end, fresh output IDs and no earlier
observation for that execution/contract. Execution status is not a success gate.
Source capture is read-only and does not follow a final-component symlink. Missing
or unreadable source refuses without fabricating empty bytes or an observation.

The observer classifies the exact captured canonical, closed four-field supplier
row against the action's declared order, product, target quantity and new occurrence.
Exact agreement is CONFIRMED. A valid different row is CONTRADICTED. Unsupported
or malformed source representation is INDETERMINATE, with the actual bytes retained.
The result describes this observation policy, not source authenticity or causality.
No mapper or source-to-KCS admission runs inside this stage.

The captured SourceArtifact retains exact bytes, byte length, digest and the logical
controlled-source locator. Its provenance names the execution and outcome contract.
OutcomeObservation then binds the exact execution, contract and captured source
record hashes. Individual Core appends are atomic; capture/source registration/
observation registration is not one transaction. Interrupted progress may leave
captured evidence without a completed observation. No automatic retry is inferred.

Conformance must include success with changed bytes; success with unchanged bytes;
failed-after-write plus supporting bytes; malformed capture; wrong source/observer/
implementation/time; unavailable capture; duplicate observation; full domain-frame
preservation; and JSONL-only reopen without reading the file or invoking the observer.
The captured bytes must be compared with an independent oracle only by tests.

The following source-to-KCS stage must explicitly bridge roles. Population requires
RETAINED_SOURCE, while the protocol capture is SOURCE_ARTIFACT. Register a separately
identified ordinary source/artifact pair from those exact captured bytes, retaining
the observation/source binding as mapping evidence. Do not silently relabel a
retained input, reuse a public change identity or map a receipt. The eventual KCS
trace and episode closure must verify that link, not just equal quantities.

Dependencies: loaded observer bytes govern the outcome contract; applied execution
and actual file feed capture; exact captured bytes feed SourceArtifact retention;
execution/contract/source feed OutcomeObservation admission. All feed the same Core
history. Later ordinary source mapping and KCS admission own any KG revision.

Excluded: source modification, receipt-derived truth, synthetic replacement bytes
as capture, KCS preparation/admission, full Re-entry Contract closure, satisfied
episode closure, empirical replacement, generic Core promotion and full E2E claims.
No server, installation, real supplier, physical/paid effect or Core/ontology/locked
fixture/paper edit is required. New material semantics still require their owner.

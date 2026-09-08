# Controlled supplier dispatch and execution

REFERENCE_IMPLEMENTATION under the existing experimental single-action profile.
The synthetic file target, exact-two amendment, actors and one-attempt policy are
already approved ADOPTER_CHOICE. Tests are CONFORMANCE_FIXTURE. No Core semantics,
new public object, retry mechanism or second accepted-state writer is introduced.

Claim: a coordinator admits one fresh existing ActionDispatch, checks the actual
controlled source immediately before its attempt, and records the existing
ActionExecution with exact result bytes. The smallest observation is that only
the controlled file may change. The complete accepted domain frame remains B/Y/1
through dispatch and receipt; neither success nor failure is observation.

`dispatch_and_execute_supplier` takes required keyword-only inputs: owning history,
expected ledger head/count, original/current context IDs, action/authorization IDs,
executor implementation SourceArtifact ID, executor/dispatcher actor IDs,
dispatch/execution IDs, dispatch/start/end instants, explicit absolute source path
and its logical source ID. It returns existing Core replay after recording a
terminal receipt. The implementation source bytes and their SHA-256 are exposed
for ordinary retention before use. They identify this loaded implementation, not
an OS-enforced attestation or self-contained Python environment. Core and Python
remain installed dependencies. A different implementation may consume this same
contract, but replacement is not demonstrated by this first implementation.

Static inputs, fresh output IDs, source binding, actual retained implementation
bytes, the accepted action and its original goal/pre-state binding are checked
before dispatch. Timestamps must be aware, dispatch no later than start and start
strictly before end. The exact accepted supplier payload must request integer
1-to-2, preserve order/product and use a distinct declared source occurrence.
The retained original goal is equality-to-two, not delivery or fulfilled demand.
Core separately governs actual permission, current context, actor, time and
duplicate-dispatch eligibility. A rejected dispatch invokes no file attempt.

Only after that fresh Core append does the private file attempt run. It reads the
explicit regular file without following a final-component symlink, compares exact
bytes with the action's pre-state digest, and validates the closed canonical JSONL
row. It changes only quantity and occurrence. It consumes no oracle, model output,
fixture path or receipt as source state. Source mismatch or unsupported shape
records ABORTED without writing the source. An OSError during the actual attempt
records FAILED; a write operation that completes records SUCCEEDED. Exact result
bytes describe the attempt, not independently observed source truth.

Source writes are not part of Core's persistence transaction and are not claimed
atomic with dispatch or receipt. A failed write may have changed the file. Failure
after a completed write must remain FAILED while a later independent observation
may support the new fact. A success receipt with unchanged bytes must leave the KG
unchanged and supplies no correction by itself. Crash or failure to retain a receipt
leaves a dispatched unresolved episode. Reinvocation cannot retry: Core refuses
another dispatch for the action before any further file attempt. No new durable
attempt identity or mutable progress log is used.

The controlled source has one writer; concurrent external edits, parent-directory
replacement attacks, arbitrary Python monkeypatching, power-loss guarantees and
exactly-once delivery are outside this bounded experiment. The coordinator is the
effect entry point; private file functions are implementation, not permission APIs.

Conformance: actual authorization before effect; wrong actor, stale head, expired
permission, wrong implementation/source binding and invalid static metadata refuse;
one fresh dispatch permits one actual source attempt; duplicate invocation never
attempts again; stale source aborts; failures before and after write retain their
own outcome; exact source/frame agreement; no graph change; JSONL-only receipt replay
does not access the source or rerun the executor. Actual independent observation,
observation-linked KCS, full synthesis closure and final quiescence remain later work.

Dependencies: accepted action/original goal plus actual permission/current context
feed Core dispatch; applied fresh dispatch gates the controlled file attempt;
attempt result bytes feed Core execution admission; Core replay reconstructs the
receipt and unchanged domain. No effect occurs inside Core validation or replay.

Pre-action checks: no server, endpoint, installation, paid/physical effect, Core,
ontology, locked fixture or paper edit. Only the explicitly controlled synthetic
file is writable through this stage. Required inputs have no inferred defaults.

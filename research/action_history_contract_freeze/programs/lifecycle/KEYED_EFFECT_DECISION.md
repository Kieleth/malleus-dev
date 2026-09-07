# A protocol index update needs an explicit key

Status: ACCEPTED for the research instruction definition. Luis replied
"Approved" to the explicit key-operand refinement after checkpoint `8d341b0`.
Research OPTIONAL_PROFILE only. No runtime activation, production path or
public API change is authorized by this decision.

## Observed gap

The existing execution receipt handler in `src/malleus/assent.py`, `_execution`,
stores `execution_by_dispatch[dispatch["id"]] = execution["id"]`. It first
rejects a dispatch that already has a receipt. Other dispatch entries survive.
The observation handler uses a two-part key, execution ID and outcome-contract
ID. These are replay-derived protocol indexes, not accepted domain knowledge.

At checkpoint `8d341b0`, `SET_PROTOCOL_STATE` declares a target, name and value.
It cannot declare the entry key. Its target's `storage_path` identifies the
whole named index, not an entry. Static validation therefore cannot establish
which entry a future interpreter should update. Inferring that entry from
`ActionExecution` or a field named `dispatch_id` would leave protocol rules in
Python. Replacing the whole index is not the existing receipt behavior either.

That checkpoint's `execution.json` retains the missing operand as a candidate
`keys` list. Its closed instruction schema rejects it with `INSTRUCTION_SHAPE`.
The 17 preceding instructions pass static checking. Neither result executes
the program or establishes the truth of any input.

## Accepted refinement

For `PROTOCOL_INDEX`, require explicit ordered string-key operands and matching
key schemas on the named profile target. One key identifies a dispatch entry;
two keys identify an execution/contract entry. Composite keys remain tuples,
not delimiter-joined strings. Refuse missing keys, wrong arity or wrong types.

Stage the assignment of the exact value at that key, preserving every other
entry. Assignment may insert or replace; a program that requires absence must
declare `REQUIRE_UNIQUE` before assignment, as this receipt program does.
Existing state transitions can instead declare the required previous state.
Commit staged assignments only with the owning failure-atomic transaction.
Keep scalar `ACTION_ACCEPTANCE_HEAD` assignment separate and forbid keys there.
Do not add arbitrary paths, expressions, callbacks or accepted-KG effects.

The research definition and static checks may now implement this refinement.
This does not authorize runtime work. Static checks resolve the ordered key
operands and compare arity, string type, declared format and coordinate domain.
Value constraints and the actual update/preservation law remain interpreter
obligations, not outcomes established by static checking.

## Bounded implementation plan

Claim: no keyed index write can omit its key or infer it in Python; scalar
action-head writes remain keyless. A uniqueness check against an index uses
the same declared key arity/types as assignment.

Smallest observation: the retained 18-instruction receipt candidate passes
static checking; omitted, unresolved, wrongly typed or wrong-arity keys refuse;
an action-head write with keys refuses. Tests are CONFORMANCE_FIXTURE, not
evidence of executing an update. Existing whole-index keyless assignments are
removed from the accepted research shape without a fallback.

Reuse the operand resolver, named target declarations, `_same_type`, and
the existing instruction schema. Keep the one-history transaction unchanged.
Do not modify source/ontology/main, run effects, add callbacks or install
dependencies. Only local research definitions/tests and their evidence change.
Commit the failing tests before the definition/checker change.

KeyedAssignment consumes OrderedKeyOperands
KeyedAssignment governedBy DeclaredProtocolIndex
StaticValidator conformsTo KeyArityAndTypeClosure

## Evidence and remaining work

The concrete receipt example binds a full minimal ActionExecution variant to
event identity, actor, time and an applied ActionDispatch reference. A test
validates concrete dispatch/receipt records against compiled Assent and the
declared static schemas. This proves those examples agree, not that every
optional field or subtype is represented by the selected variant.

Still unfinished independently of the key: verified full-history input
resolution, actual compiled-contract binding, complete source/dependency
resolution, result-byte retention and hash checking, all other lifecycle
program variants, and real monitor input/output bindings. No check producer or
interpreter has run. No receipt, proposal, permission, external effect or domain
change has been admitted. Completing the keyed definition alone would not
close these obligations.

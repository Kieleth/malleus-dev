# One new instruction decision

The context/proposal transaction question is CLOSED. Nothing is waiting on
Robotics, Paper or a second Re-entry acknowledgement.

## Exact gap

Current Assent authorization requires:

```python
action["action_type"] in grant["permitted_action_types"]
```

The existing `AuthorityGrant.permitted_action_types` is a multi-valued string
slot. The test compiles the exact Assent closure and validates a grant containing
both READ and AMEND. This is not a new supplier-only permission model.

`missing-membership.json` retains the exact attempted instruction: REQUIRE_COMPARE
with comparison IN, scalar action_type on the left and the grant list on the
right. The frozen instruction schema refuses it. Its permitted comparisons are
EQ, NE, LT and LE over two scalars. Both ordered examples are retained: AMEND
must pass against [READ, AMEND]; DELETE must fail against that same list.

Comparing only index zero rejects the valid AMEND case. Requiring equality to
the entire list has the wrong types. REQUIRE_UNIQUE and REQUIRE_COVERAGE already
have different declared meanings, respectively uniqueness and exact monitor
coverage; silently reinterpreting either would change its contract. A satisfied
authority assessment alone does not replace the existing independent replay
grant check. This packet does not claim a mathematical impossibility theorem;
it identifies the missing operation under the current declared operand and
instruction contracts.

## Smallest proposed change, not implemented

Add one bounded `REQUIRE_MEMBER` instruction with explicit STRING value operand,
finite STRING-list operand and typed refusal. It compares exact values without
coercion and produces no output or state change. No arbitrary expressions,
iteration program, predicate callback, scope hierarchy or new grant shape.

Luis's decision is required before this is added to the instruction vocabulary.
Restricting grants to one action type or dropping replay's membership check are
not selected fallbacks. This does not authorize an action runtime or producer.

After a decision, freeze the instruction's positive/negative/type tests, finish
the complete JSON event programs and their static closure, and bring the actual
producer/interpreter implementation cut for review. Further discovered semantic
gaps must be reported; this is not a claim that this one instruction alone proves
the whole language sufficient.

## Independent work completed despite this gap

The research static validator checks every preceding instruction's declared
operand shape, path and basic type, earlier results, introduction dependency
order/cycles, capabilities and permitted state target paths. Concrete interval
contents, closed equality-scope/current-context schemas and the explicit
monitor invocation/output definitions are tested. `LIFECYCLE.md` maps all event
roles to required checks, deltas and positive/negative runtime observations.

The full executable event programs and real check producers remain unfinished.
No production code, instruction grammar, ontology, history or external source
is changed by this packet. The successful test results do not erase that gap.

# Approved finite membership instruction

Luis answered yes to adding the bounded membership instruction and sharing the
preceding private packet with Malleus-semantic-reentry. This closes the decision
in `NEXT_DECISION.md` at `fdb4972`; it does not authorize runtime activation.
Original-context registration and proposal remain one failure-atomic transaction.

Role: OPTIONAL_PROFILE definition, exercised by research CONFORMANCE_FIXTURE
checks. The concrete requirement is the existing Assent authorization check:
an action's type must belong to its grant's permitted action types. Reuse the
existing finite operand grammar and static validator. No production mechanism,
public grammar, ontology, source effect or shared checkout changes.

`REQUIRE_MEMBER` has exactly five fields: opcode, value, members, value_kind,
and refusal. value_kind is STRING. value resolves one string; members resolves
one finite list of strings. Every operand is explicit and follows the existing
required-field/zero-based-index rules. No result, state target or callback.

Required execution semantics for the future interpreter: pass if any member
equals the value exactly, otherwise raise the instruction's declared refusal.
Case, whitespace and Unicode spelling are significant; no conversion or
normalization is performed. Empty lists do not contain any value. List order
and repeated matching values do not change membership. Invalid operand types
refuse before comparison, even if another member would match. The instruction
does not mutate the operands, grant, protocol or domain state.

Smallest observations now: the new instruction shape passes; missing/extra
operands and incorrect scalar/list/item types refuse statically. The AMEND
example must be expressible against a READ/AMEND list without a singleton-grant
restriction. Required value-level outcomes are retained separately as fixtures;
they are not executed by the static validator or counted as runtime proof.

Pre-action checks: no server, endpoint, installation, missing-data default or
replacement path. This adds the approved instruction to the research schema;
it neither calls a producer nor executes an action. Tests precede definition
and validator changes. Full event programs remain the next definition work.

MembershipInstruction implements ExactStringListMembership
StaticValidator consumes MembershipInstruction
FutureInterpreter conformsTo FrozenMembershipCases
MembershipInstruction governedBy OneHistoryActionProfile

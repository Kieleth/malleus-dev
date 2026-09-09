# Semantic Re-entry: start with one order

The capability is simple: something derived from accepted knowledge can return
as a constrained proposal. Deriving a proposal gives it no permission to change
accepted knowledge or execute an action.

## The main example

The accepted record says supplier order **B requests one unit of product Y**.
We supply an explicit goal: **make that order request exactly two units**.
The example reuses the Shop's B/Y/e4 values in a controlled fixture. The target
of two is a separate test input, not customer demand discovered in the dataset.
These are order quantities, not delivered goods or available inventory.

1. The system compares the accepted record with the goal and finds a shortfall
   of one unit.
2. It proposes amending B from one unit to two. That proposal is based on the
   exact accepted history it read. It changes neither the order nor accepted
   knowledge, and a later history change can make it stale.
3. The proposal passes through the existing checks and authorization process.
   Only a separate authorized executor can attempt the amendment. In this
   experiment it changes a local file representing the supplier's order record.
4. Accepted knowledge still says one unit. An execution receipt, even one
   reporting success, does not establish the new state.
5. An independent observer captures the actual source. Normal source processing
   proposes a knowledge change. Only after that change is checked and admitted
   does the accepted graph reflect two units. The old record remains in history.
6. The system evaluates the goal again. It is satisfied, so there is no further
   proposal or action.

This is the original thin slice. No second order is needed to prove it. The
[one-order walkthrough](SUPPLIER_WALKTHROUGH.md) gives the command to run it and
the files to inspect at each checkpoint.

## What the extra order tests, and why three

The [two-alternative extension](TWO_ALTERNATIVES.md) adds a synthetic order C
for one unit of Y. With B=1 and C=1, two units are ordered in total. Its explicit
test goal is at least three units across exactly those two orders.

Three is chosen to leave a one-unit shortage with two permitted solutions:
increase B to two or increase C to two. It is not an inferred customer-demand
quantity and not a Semantic Re-entry requirement. The exact supplied goals are
visible in the [one-order fixture](fixtures/supplier_commitment_v1/case.json)
and [two-order fixture](fixtures/supplier_choice_v1/case.json).

Without a declared way to choose, the selector returns an ambiguity refusal
and no proposal. With an explicit preference for B, it returns only B's proposal.
The preference governs this generator; it does not replace authorization or
prove that B is commercially preferable. B then follows the same observed-update
loop. C is unchanged. This extension tests choice, not a general planner.

## The boundary we proved

The system keeps a proposed change, permission to act, an attempted action and
observed evidence separate. Tests include success reported without any source
change, and failure reported after a real source change. Accepted knowledge
follows the observed source through normal admission, not the receipt's status.

In the implementation, an `ActionProposal` requests the external change. A
`KnowledgeChangeSet` proposes the later change to accepted knowledge. The
Re-entry Contract records the goal, accepted starting state, permitted actions,
evidence and preservation requirements, selected implementations, choice rules,
budget and stopping conditions. There is one authoritative append-only history;
the accepted knowledge graph is derived from it and has no separate write path.

## What this does not establish

The experiment changes a controlled local supplier record, not a real supplier
service. It does not prove delivery, customer-order fulfilment, general planning,
automatic retries or replacement by a second independent synthesizer. It also
does not prove that the whole application has stopped rebuilding graph views.

The [original proof handoff](SUPPLIER_E2E_HANDOFF.md) and the later
[authorization compatibility receipt](supplier-choice-authorization-result.json)
identify the exact tested versions. A working proof, its integration into main,
and a production deployment are separate milestones. Those receipts do not
automatically verify later Core code or claim that a merge has happened.

This page is an explanation of the existing reference implementation and its
conformance fixtures. It changes no fixture, contract, runtime or earlier
verification receipt.

# Three promises of accepted knowledge

Author-endorsed distinction, 2026-09-06. Recorded here by the paper task for
coordination across Malleus. This is a project/protocol principle, not a new
Core runtime contract, evaluator or mandatory profile.

| Promise | What must establish it |
| --- | --- |
| The proposal satisfies its declared structural and evidence-binding rules | Compiler and admission checks |
| The representation faithfully expresses the source | Source-grounded semantic assessment |
| The representation contains enough information for its intended use | Explicit coverage requirements and evaluation |

These promises must be stated and supported separately. Passing one does not
establish either of the others. Faithfulness concerns the representation of a
source, not independent truth about the world. Sufficiency is relative to an
identified use and its requirements, not universal completeness.

Replay adds a distinct mechanical property: reconstruction of accepted state.
It can reproduce an omission or incorrect interpretation exactly. Replay
agreement therefore does not establish source faithfulness or sufficiency.

## Consequence for acceptance claims

An acceptance statement must identify the contract and checks under which the
state was accepted. A successful structural check must not be paraphrased as
semantic verification or task sufficiency. A source locator establishes where
to inspect evidence; it does not by itself prove that a value follows from it.

The ontology declares legal structure, including any required fields. The
history profile declares the meaning of changes. Neither establishes that all
relevant source meaning was represented. Any stronger representational
obligations must be stated explicitly, with omissions and unresolved matters
visible rather than silently treated as complete.

Partial representation can be a legitimate accepted result under its declared
policy. Removing an optional field can make a proposal pass a conditional
check without making the representation more useful or complete. This must
not be reported as semantic improvement merely because a refusal disappeared.

## Ownership and limits

Core owns generic protocol mechanisms and enforcement of declared contracts.
Domain adopters own domain interpretation, intended uses and the requirements
and assessments needed for stronger acceptance claims. Source-grounded review
and task evaluation do not become Core-owned scoring by this distinction.

No universal required-subject rule, relation quota, automated semantic repair,
new evaluation API or mandatory completeness threshold is selected here.
Purpose-specific evaluation requirements must not silently become inputs to a
general ontology builder. Any such experiment or policy change remains a
separate decision.

The three promises apply to document assertions, operational state and agent
environment models. An accepted symbolic statement is not evidence that an
external action occurred or that its intended effect was observed.

## Record

Luis explicitly endorsed the three-row distinction as critical to Malleus as
a project and protocol. Paper decision/evidence entry: E-0219. Master plan
version 1.5.2 references this note. Coordination transfers the principle, not
ownership of paper evaluation or authorization to alter another task's scope.

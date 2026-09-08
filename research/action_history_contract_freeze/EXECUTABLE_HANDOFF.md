# Executable action boundary, isolated candidate

This is Core's implementation of the approved one-history action contract.
It is not a main-branch publication, stable wire or finished Robotics or
Semantic Re-entry experiment. The final execution report and exact commit
determine readiness; this document alone does not.

## What the mechanism does

The same `KnowledgeChangeHistory` now has a finite-program attachment for
protocol records alongside ordinary KnowledgeChangeSets. Knowledge changes
still enter only through the existing KCS admission path. Action events change
only protocol records and indexes. Epistemic ACCEPT advances the separate
action head; authorization does not change the knowledge graph.

Program data declares the record types, references, field comparisons,
uniqueness, time rules, transitions and refusals. The private Core interpreter
executes the twelve identified instructions. It does not import the research
builders, checker or effect code during append or replay.

| Stage | Executable definition | What is committed |
| :--- | :--- | :--- |
| Prerequisites and initialization | `programs/registration_bundle.py`, `programs/initialization_bundle.py` | Exact records, bytes, policies and checkpoint |
| Original context and proposal | `programs/proposal_bundle.py` | Both logical events in one atomic append |
| TYPE judgments and epistemic decision | `programs/assessment_bundle.py`, `programs/decision_bundle.py` | Actual outputs, then recomputed decision and transition |
| Current context and direct-grant judgments | `programs/current_bundle.py`, `programs/authority_bundle.py` | Verified context and actual outputs |
| Permission | `programs/authorization_bundle.py` | Recomputed AUTHORIZE, BLOCK or CLARIFY and transition |
| Dispatch | `programs/dispatch_bundle.py` | Eligibility for an exact executor and declared adapter |
| Receipt | `programs/execution_bundle.py` | Terminal receipt and exact result bytes |
| Observation | `programs/observation_bundle.py` | Independent observer, outcome contract and source references |

These Python files author data before selection. Their output is one retained
`malleus.finite-protocol-bundle/private-v0` artifact, including the exact
compiled Assent record contract. Its `transactions` field contains the
executable programs and closed event-input schemas. The initial supplied
record contract is not the domain contract governing the Shop graph.

## Calls and ownership

`KnowledgeChangeHistory` is obtained from `malleus.compiler`. This attachment
remains experimental; its presence on that class does not stabilize its wire.

1. Retain the exact selected bundle as evidence with `history.append_anchors`.
2. Call `history.select_protocol_programs` with that record ID and identity,
   explicit event metadata, and the actual expected full head and count.
3. Compute checks explicitly with the reference
   `programs.history_checks.run_history_check(history, invocation=...)`.
   Its identified producer reads the owning replay, not a caller's record map.
   It returns full existing assessment records and the computation's base.
   This helper remains repository-local, not a packaged public check SDK.
4. Call `history.append_protocol_events(transaction=..., events=...,
   expected_head=..., expected_count=...)`. The transaction name and exact
   data shape come from the selected artifact, not an inferred default.
   Raw retention inputs contain `content: bytes`; Core owns their persisted
   encoding. Do not supply pre-encoded storage envelopes.
5. Reopen with `KnowledgeChangeHistory.reopen(path)`. `history.replay()`
   returns the domain graph and `protocol_replay`, with full records, indexes
   and the action head. Retained bytes are read from the replay result with
   `replay.retained_bytes(record_id)`, not from the writer.

Append and replay never invoke a checker, supplier adapter, simulator or
observer. Control is recomputed from applied judgments. The caller cannot
select its own authorization verdict. Computation and persistence have
different jobs; a retained judgment is not authenticated process execution.

The caller still authors registration and lifecycle event bodies against the
selected schemas. There is no general high-level action SDK here. The current
reference programs use one first-revision `LocalAction`, two TYPE monitors,
two direct-grant monitors, one dispatch, and finite grant/permission intervals.
`LocalAction` is a conformance fixture, never required domain vocabulary.
Supplier and robot subtypes require their own exact compiled record contract
and selected program variant. Do not silently rename types in retained bytes
or make a downstream copy of the Core interpreter.

## Evidence and limits

The focused stage tests invoke actual TYPE/direct-grant producers and exercise
valid negative decisions, typed refusals, atomic rollback and reopen. The Shop
composition test uses real e4/e7 KCS admission: the correction invalidates
pre-dispatch permission, while an already dispatched action can still receive
a failed receipt and independent observation. A fresh process reopens from
JSONL while refusing every research/test import.

The historical e7 correction is not caused by the synthetic action. The
neutral action/receipt/observer cases establish protocol composition, not a
supplier amendment, robot movement, goal satisfaction or source truth.
Robotics owns its controller, assets and observations. Semantic Re-entry owns
its synthesizer, domain action model, source adapter and goal experiments.
Neither consumer's experiment gates the other; both need Core's exact tested
boundary, plus their separately approved domain inputs.

No default structural-history behavior, existing standalone Assent history,
public ontology, main branch or downstream repository is replaced. This cut
does not claim multi-action scheduling, retries, grant legitimacy, actor
authentication, concurrent-writer safety, OS enforcement, a portable interpreter
demonstration or an installed all-in-one action SDK.

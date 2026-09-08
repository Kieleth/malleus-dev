# Core action definition: independent consumer review

Date: 7 September 2026. Verdict: definition integrity and reported test scope
PASS; executable Re-entry gate OPEN. No runtime authorization is inferred.

Inspected Core commit `63e1c3bcc6df9a161f177fa70e8c0e6f39d237d1`, tree
`f59d998bb0c22dfaaf694c344d53c77db0f42085`. Independent clean clone:
`/private/tmp/malleus-reentry-definition-audit.EK2FnT/repo`.
Consumer base: `fd5c294b4bb14c4209ab0edce56e8267f2c896af`.

Scope: the seven-file definition packet against the frozen CORE_CONTRACT.md
and ADOPTER_CONTRACT.md. This is a CONFORMANCE_FIXTURE review of a proposed
OPTIONAL_PROFILE under compiler-enabled semantic history and the bounded
one-consumer exception. Without that profile, no combined action/KCS lifecycle
guarantee follows. No root-ontology change or profile audit is claimed.

The Malleus development and inquisitor skills guided the review, using rubric
v12 resolved from the exact Core checkout. Root-ontology mechanical rites:
NOT RUN, that profile is not the subject. To preserve task ownership, this
scoped report lives in the consumer research directory; no Core/root report,
CLAUDE.md, rubric, ontology, paper or runtime file was modified.

## Observed evidence

All seven added paths match the owner handoff. Git comparison from `ff0e1b3`
shows no other changed paths. The local byte-binding table covers exactly its
five declared files; each digest matches. Every upstream semantic file also
matches the bytes at its declared `f221c099` commit. The two unlisted metadata
files are identified by the enclosing Git commit, as the report declares.

The exact owner selection ran independently against the final report commit:
**140 passed in 14.92 seconds**, including all 28 definition tests. No failure,
error or skip. Explicit `-c pyproject.toml` selected this Core checkout; a
separate diagnostic verified the loaded compiler path and exact clean HEAD.
Ruff, formatting and base-to-head whitespace checks pass. The clone remained
clean. JUnit: `/private/tmp/malleus-reentry-definition-audit.EK2FnT/independent-focused.xml`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider \
  -c pyproject.toml research/action_history_contract_freeze/test_definition.py \
  tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
  tests/contract_compiler/pareto/test_contract_alternatives.py \
  tests/contract_compiler/pareto/test_public_compiler.py \
  tests/test_assent_ontology.py tests/test_compiler_compatibility_gate.py
```

This uses the existing configured project interpreter and dependencies. Core's
earlier RED checkouts were not rerun here. The historical bounded compiler gate
was not rerun or reclassified. This is not full repository CI or E2E GREEN.

| Claim | Role | Evidence | Unsupported transfer | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Closed context/instruction/binding shapes | CONFORMANCE_FIXTURE | 28 shape tests in the 140-test selection | None when limited to shape | PASS |
| One ledger, one KCS identity, no direct KG write | OPTIONAL_PROFILE | Definition preserves the frozen rule; no runtime diff | Shape rejection is not writer enforcement | Definition agrees, execution OPEN |
| Context identity excludes self-digest | OPTIONAL_PROFILE | Complete canonical-value hashing and shape tests | No current-context authentication follows | PASS within definition |
| Exact producer implementations exist | REFERENCE_IMPLEMENTATION | Explicitly UNBOUND; no implementations supplied | Cannot instantiate from specification hashes | NOT ESTABLISHED |
| Ten operations express the whole lifecycle | OPTIONAL_PROFILE | Operation shapes exist; event programs absent | Cannot infer completeness from opcode count | OPEN |

## Concrete limits, not newly discovered runtime defects

Three read-only probes against the actual schemas reproduced declared gaps:

| Synthetic input | Observed shape result | Required later guard and hard test |
| :--- | :--- | :--- |
| Swap distinct A and D digest values while preserving their field names | Valid | Compare each coordinate with its own replay-derived value; a cross-domain value swap refuses before append |
| SET_PROTOCOL_STATE target PROTOCOL_INDEX, name accepted_graph | Valid | Resolve an exact declared protocol-owned index; a name or alias targeting any D component refuses before execution |
| TYPE implementation bytes_sha256 set to a lexically valid all-zero digest | Valid | Resolve and verify actual implementation bytes; absent, wrong or specification-only bytes cannot instantiate an executable monitor |

The probes reused the owner's explicitly synthetic shape witnesses. They did
not initialize a history, execute an action, invoke a producer or mutate a KG.
They are diagnostic observations, not three new lifecycle tests. Core already
states these limits at DEFINITION.md:155 and :187. The existing unsupported-
grammar control prevents using this packet through the current public machine.
No repaired runtime defect or new conformance capability is claimed.

## Decisions and dependency-closed next cut

### R1. Adjacent original-context registration and proposal requires approval

Where: Core DEFINITION.md:63. The rule fixes an unnamed part of the frozen
contract: O binds prefix L0, registering O produces L1, and its proposal must
be the immediately following event. The proposal's commit checks actual L1;
O retains L0. A and D must still match their original values. Later ordinary
action-only progress need not keep the original full log head current.

This is compatible with the frozen distinction between immutable O, current
append expectation L, and semantic coordinates A/D. It is nevertheless a
newly chosen scheduling restriction. Recommendation for Luis: approve this
adjacency rule for the bounded proof, not arbitrary intervening appends or
silent rebasing. Do not call this recommendation accepted.

Acceptance cases for the successor contract: adjacent registration/proposal
works; an intervening unrelated evidence event refuses the old proposal;
wrong O/action association refuses; D or A movement refuses; subsequent valid
own-lifecycle appends still work. The event program must also state whether
registration and proposal share one atomic batch. If separate commits are
permitted, specify the status of an orphan registration after proposal refusal.
No cancellation, retry or new episode policy may be invented to fill that gap.

### R2. Do not freeze the instruction vocabulary from shape tests alone

Where: Core DEFINITION.md:80 and :195; instructions.schema.json:10 and :112.
No impossible supplier requirement or contradictory meaning was found in the
stated definition. Sufficiency is still unproved because there are no complete
event programs. Keep the ten operations as a candidate vocabulary until Core
expresses each existing transition without a hidden handler or new operation.

The smallest next definition packet must close:

1. Initialization and registration through proposal, assessment/decision,
   authority, dispatch, execution and observation, with exact event programs,
   input/output wrappers, dependency order, declared indexes and typed refusals.
2. Literal/absent/null/empty-list constraints through identified artifacts or
   declared operations. In particular, show the no-claims/no-application subset
   and existing acceptance_result_head computation, not a caller-trusted head.
3. Monitor invocation metadata and ordered inputs, output provenance and paired
   unavailable records, plus interval, equality-scope and current-context
   content contracts. TYPE and direct-grant remain separately identified,
   explicitly invoked pure producers; append/replay must not run them.
4. Static rejection of unresolved paths, output reuse, forward/cyclic
   dependencies, unknown capabilities and domain-state aliases. Every required
   lifecycle invariant must map to one test with an expected typed refusal or
   exact allowed state transition.

Core owns this closure. Re-entry supplies the unchanged supplier expectations
and consumes the resulting interfaces. Robotics is useful as a second design
comparison, but its assessment pilot is not a demonstrated action consumer and
does not satisfy generic promotion or action replaceability.

### N1. Clarify the RED/implementation ordering

Where: Core DEFINITION.md:214. Requiring actual producer/interpreter identities
and live initialized contexts before runtime RED can be read as requiring the
implementation before its failing tests. That is an unsafe scheduling reading,
not a discovered protocol bug.

Clarify the gate: freeze reviewed semantics, fixtures and expected refusals
before implementation; retain failing tests for the missing boundary; bind
actual implementation bytes and instantiate verified contexts when they exist,
before any successful executable freeze or E2E claim. Missing implementations
must still refuse real runs. No placeholder digest makes that readiness gate
GREEN. This clarification does not authorize runtime work.

## Commendations and conclusion

The packet preserves distinct identity domains, makes unknown producer code
explicit, rejects arbitrary execution hooks, and keeps current parser refusal
as a passing control. Its report distinguishes shape evidence from execution.
These are useful guards against overstating this work.

There is no new Core repair request from this review. There is one concrete
operator ordering decision, one Core-owned definition closure, and a RED-gate
wording clarification. Runtime implementation remains unauthorized; full
external Semantic Re-entry E2E remains unproved. No merge, push, external call,
consumer runtime rebind or Small Shop change occurred.

## Exact handoff file SHA-256

All paths below are in Core research/action_history_contract_freeze.

| File | SHA-256 |
| :--- | :--- |
| DEFINITION.md | 3a4172e992cc6f4d0a367d2e8606310b38a9c3e18ffa1d7698c22a9407ac5090 |
| DEFINITION_REPORT.md | 3be054a8449b28ce2041b561414edf3cf19d247301fe18f6c5f5202f8bf609bc |
| contexts.schema.json | 43f5e2f040e408d18de9448b56145284caa83b901c810f1ac08a2776c4f2dd68 |
| instructions.schema.json | 3951a88c0db38aab91148c61276410d3189bb1f2e47ad54f2dd48f50d6cee6f5 |
| capabilities.schema.json | 0e832d453c078b382071e19b3eea001255f4bf5518509c52b350082d645800b3 |
| definition-inputs.json | 14c84b5b550b3792664251cfee4d43b7a261584e2c77a41a921fdcaff6b156bd |
| test_definition.py | 253a667d04cbfe2fc2d776dedc8ed20f6d47e312acfa2673e23b9cacc4f4a70f |

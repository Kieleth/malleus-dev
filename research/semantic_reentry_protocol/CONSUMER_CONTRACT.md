# Consumer contract and RED cut

This adds consumer-side requirements to the frozen `1bbff3c` prerequisite
packet. That packet remains unchanged. Core has now been authorized to build
the immutable-context KCS composer. Its public names and integration commit
are not assumed here.

## Claim, observation, reuse, exclusions

Claim: under one explicit source-backed Shop ViewDelta, a pure consumer can
decide whether the request needs composition, is already satisfied, or must
refuse. The subsequent synthesizer will use Core to construct the sole KCS
identity. An internal `READY` assessment is not a candidate, admission,
authorization, or new change identity.

Observation: accepted RET-010 plus e4 yields `READY` for the retained e7
observation, with only quantity and source occurrence differing. After ordinary
Core admission of e7, a newly bound invocation yields `SATISFIED` without new
retention. An old contract must still refuse against that new head.

Reuse: the existing Shop source, mapping, population templates, correction
ontology, state-version profile, public replay/trace and population APIs.
`test_prerequisites.py` supplies the already-frozen test fixture; production
consumer code must not import test helpers or a research runner.

Exclusions: no Core implementation, KCS serialization, substitute composer,
new source facts, canonical fixture edits, ontology edits, external actions,
or paper work. No GREEN synthesis claim before the actual Core seam is bound.

| Deliverable | Classification | Lowest affected profile |
| :--- | :--- | :--- |
| Local contract and request assessment | REFERENCE_IMPLEMENTATION | Compiler-enabled semantic history plus state-version |
| Tests and copied replay read-model | CONFORMANCE_FIXTURE | Same |
| Mapping, exact footprint, refusal strategy, budget and stopping | ADOPTER_CHOICE | Same |

Without this consumer, Core still composes and admits structural changes but
does not provide its source-agreement, preservation or stopping policy.

## Local boundary

`ReentryContract.from_bytes` consumes closed canonical JSON and returns an
immutable, content-addressed local value. It is not exported from `malleus`.
Every field is required. Unknown grammar, input/output kind, policy, operation,
or required field refuses explicitly; no required value acquires a default.

The contract binds these exact inputs and choices:

- Ledger head/count, acceptance/materialization heads, effective contract,
  accepted graph digest and replay receipt identity.
- The bytes of a caller-extracted projection, containing active records,
  record history and retained-input identities/roles.
- Plan, source and explicit mapping byte identities, source/mapping IDs,
  occurrence e7, predecessor e4 and target record e7.
- KCS output, `CREATE_ENTITY`, explicit mapping supersession, exact complement,
  `REFUSE_IF_NOT_UNIQUE`, integer candidate budget and exact-target stopping.
- The expected synthesizer identity, supplied separately by the invoking
  implementation and checked for agreement. In these policy tests it is a
  named test mechanism digest, not a claimed production execution identity.

`assess_request` receives that contract, canonical projection and plan bytes,
exact source/mapping bytes, and the invoking synthesizer identity. It performs
no I/O and accepts no writer or mutable graph object. Its immutable result
contains `READY` or `SATISFIED`, sorted changed field names and sorted preserved
record IDs. Failures raise a typed local `ReentryRefusal`; no result escapes.

The projection is a test-local read-model copied from actual public replay.
It is not a substitute Core composition context, authenticated state proof,
or new authority. Its identity binds what this assessment saw. Integration
must obtain composition context from Core's validated immutable boundary.

## Assessment semantics

Check closed grammar and supported policy, then invocation identity and exact
base/input bindings. Staleness is checked before satisfaction. Validate retained
source/mapping roles and identities. Select exactly one e7 occurrence and one
explicit mapping change. Missing or competing matches refuse, never rank by
row order, minimality, or enumeration order.

Compare every declared source-to-property binding, the exact record type/ID,
supersession and ORDER_ONLY valid time with the chosen mapping and plan. Reject
extra records even if Core would accept their shapes. The only permitted
replacement footprint is e4 to e7. All other records and relation endpoints
are the complement. `READY` identifies the changed fields; it does not prove
that a proposed KCS preserves the complement. Integration must also compare
the full complement after ordinary application/replay.

Return `SATISFIED` only when current e7 has the exact requested properties,
e7 is active, and record history records the exact e4-to-e7 supersession and
selected valid time. Equal quantity, wrong provenance or duplicate IDs do not
establish satisfaction. A satisfied request consumes zero candidate budget.
An unsatisfied request with budget zero refuses. No retries or rebasing occur.

For a first unsatisfied request, the caller may assess before new plan
retention. `READY` then permits caller-owned preparation, not admission. After
required retention, bind the final contract and Core context at the new head,
reassess, compile and compose through Core. Reuse existing retained artifacts
on subsequent invocations; never write merely to discover a no-op.

## Core acceptance requirements and integration gate

Core's context must bind exact base coordinates and retained closure; refuse
inconsistent or mutated replay input; expose no writer or mutable graph; and
preserve byte parity with the existing composer. Composition must reject
unsupported operations and invalid closure before effects. The same output
must cross ordinary admission/reopen/trace. Later ledger movement is checked
by admission, not guessed by an isolated snapshot.

After Core supplies its exact public API commit, add the real integration test:

```text
empty history -> RET-010 -> e4
e7 request -> pure assessment -> explicit retention -> final binding
pure synthesizer -> existing KCS -> ordinary admission
JSONL-only reopen -> exact e7 query and trace -> unchanged complement
new-head invocation -> zero candidates and zero writes
```

Those integration arrows are not implemented by the policy tests. The tests
may admit e7 directly through existing Core solely to prepare a real satisfied
input. No test double will stand in for the missing composition API.

Dependency tuples: request assessment implements local ViewDelta policy;
assessment consumes bound source/mapping/plan/projection; assessment produces
an internal decision; synthesizer consumes that decision and Core context;
synthesizer produces KCS; admission consumes KCS; replay produces accepted KG.
Replacement requires a second real producer passing the same consumer and
integration suite, not just an interface or adversarial stub.

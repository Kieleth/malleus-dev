# Supplier component result and scoped self-inquisition

Date: 2026-09-07. Scope: the pure supplier component cut authorized by Luis.
This report stays inside Re-entry research; no shared/root audit or paper is
changed. Skills: malleus-dev, malleus-acolyte, malleus-inquisitor. Rubric v12,
resolved from this checkout's `src/malleus/inquisition/rubric.yaml`.

## Result

The pure model predicts the frozen e4/B/Y/1 row becoming
reentry-amendment-1/B/Y/2. The mapper independently converts supplied, authored
replacement bytes into existing population fields. The public population
compiler accepts those fields and emits one SupplierOrderState replacement
operation with explicit e4 supersession and ORDER_ONLY validity. The test does
not prepare or admit a KCS. Its ledger, graph and record history remain unchanged
after compilation, and its accepted supplier quantity remains one.

The source digest is checked before source-level satisfaction. Unknown fields,
malformed bytes, bool quantities, multiple rows, unsupported rules, wrong
order/product/occurrence, incomplete mapping and quantity three refuse. An
execution receipt cannot substitute for source bytes. Repeated identical
inputs produce identical bytes and derivation order; unchanged source produces
None. This None is not proof of fresh-head lifecycle quiescence.

Model output SHA-256:
`7828cebdf6a98496196a72e501f1637d2141550d76f4313751787d4a04d03ea0`.
Population fragment SHA-256, with the authored test source ID:
`04b49239da6221b91203fa2bd8cb8c844dc1eeb1337991e5d89cc307d8032fc8`.
Neither identity claims a capture, effect, accepted fact or causal link.

## Verification and retained failures

The final focused selection passed 84 tests. The unified relevant selection in
`supplier-component-gate.json` passed 422, with zero failures, errors, skips or
xfails. This is not a full repository CI or external-action E2E claim. Unchanged
historical integration receipts and action-runtime prerequisites are not
silently relabeled by this result.

A clean detached checkout at implementation GREEN independently reproduced
all 422 passes with the compiler loaded from that checkout's `src` directory.
The checkout is `/private/tmp/malleus-supplier-component-review.3iYqsO/repo`.
Exact implementation, input, report and test-result hashes are retained in
[supplier-component-result.json](supplier-component-result.json).

Initial contract RED at `c3e93775263785e4f1b61306b9d015dd272dbef6` records 80
failures because the implementation module did not exist. The first component
run passed 79 and failed one incorrect test expectation: the Core compiler's
evidence closure contains profile and plan IDs before the supplied mapping ID.
The corrected test asserts the whole closure, not just membership.

**SC-1, fixed:** generic Unicode line splitting misclassified valid JSON string
characters as row delimiters. Three regression witnesses, U+0085, U+2028 and
U+2029, fail at `7b55f577e3e9c1a79872fbdb34908897d37832e3`, alongside 80 passing
controls. The guard in `_row` frames only on LF, as JSONL requires. The same
three cases pass in GREEN. The rule applies to every source parsed by either
component, not just the frozen B/Y row.

**Gate setup error, corrected:** an initial wider command named a test from
Core's newer checkout. Pytest refused collection and ran zero tests. The retained
manifest now names only real files in this base; preflight and a hard test check
those paths and require the public compiler and component imports to originate
inside the selected checkout. No collection refusal is counted as GREEN.

Ruff check, format check and base-to-GREEN diff check pass. A syntax-aware scan
of 46 Python source files found no imports from research or tests. Parsed root
ontology imports are exactly `linkml:types`; no ontology is modified.

## Self-inquisition

Lowest affected profile: compiler-enabled population/state-version.
Root ontology profile: NOT CLAIMED by this change. Mechanical schema rites:
NOT RUN, profile not claimed. No package, new dependency, endpoint, server
interaction, old-mechanism replacement or deployment change is introduced.

| claim | role | evidence | unsupported transfer | verdict |
| :--- | :--- | :--- | :--- | :--- |
| Implement the declared narrow supplier model | REFERENCE_IMPLEMENTATION | Model agrees with independent frozen oracle; source frame and refusals checked | No world-state prediction guarantee beyond this model | pass |
| Equality-to-two and the single 1 to 2 operator remain scenario choices | ADOPTER_CHOICE | Existing goal/operator inputs are explicit and closed; other meanings refuse | Not a Core instruction or universal ontology rule | pass |
| Supplied replacement bytes map to existing population fields | REFERENCE_IMPLEMENTATION | All four source fields, exact digest, locators, new occurrence and supersession compile publicly | No authenticated capture, initial-state authority or admission | pass |
| Test inputs remain authored fixtures | CONFORMANCE_FIXTURE | Runtime imports only json/hashlib; no oracle or filesystem access; harness labels retention as setup | No effect, observation or causal evidence | pass |
| Re-entry stages do not write accepted state | REFERENCE_IMPLEMENTATION | No writer/callback ports; I/O guard; complete graph/history and ledger comparisons | Not a Python process sandbox or a new lifecycle proof | pass |
| Gate inputs and runtime match the selected checkout | CONFORMANCE_FIXTURE | Manifest preflight and origin/path regression | Not installed-package or release validation | pass |

`protocol_role_is_explicit`, `optional_profile_stays_optional`, `silent_drop`,
`fail_closed`, `encodable_at_the_gate`, `evidence_does_not_transfer` and
`module_declares_its_interface` are satisfied within this cut. Closed source
fields, complete mapping and immutable canonical output are the concrete guards.
The protocol-authority and single-ledger rules acquire no alternative
interpreter, accepted-state writer or change identity here. The components are
adopter code, not an interpreter for Core's action programs.

No unresolved in-scope heresy or suspicion remains. Commendations: the oracle is
outside runtime dependencies, and the compiler compatibility test proves the
absence of admission instead of inferring it from API names. Replaceability is
NOT PROVED: only one implementation has run. Other schema, rule-engine, reader
census, queue, package and release rites concern unchanged or unclaimed
surfaces; this review makes no new claim about them.

## Landing and remaining dependency

Base: `49b78a27bd807b90e42973d14f710e2bde09707a`, tree
`5eec6f5157181c714cbfa8152fdb8bb3203bf440`.
Implementation GREEN: `e30fac8caacefe5272b6cbbd5764b24c45701b47`, tree
`8de73e0765fbbd2ad62a9c4b63c37d9b5bface32`.

Apply the isolated commits in order: c3e9377 contract RED, 7b55f57 initial
implementation plus framing RED, e30fac8 guard and GREEN, then this evidence
commit. Intermediate RED is intentional, not a landing candidate by itself.
Six implementation-cut files are confined to Re-entry research. Existing Shop
fixture bytes, Core, ontology, package configuration and paper work are unchanged.
No merge, push or publication was performed.

This completes the authorized pure component cut. The full external loop still
needs the separately reviewed and authorized Core action lifecycle, followed by
adopter executor/independent observer integration, fresh-context source-to-KCS,
admission, replay and true quiescence tests. Core's live task currently reports
a missing key operand for the dispatch-to-receipt state update. That is a Core
definition decision, not authority for this task to invent an implementation.
No supplier public action subtype or producer identity is silently bound here.

# Membership definition and static-array repair

The approved instruction addition is complete at the research definition and
static-check boundary. It is not an action runtime. The context/proposal
transaction and membership choices are closed; neither awaits another answer.

## Exact changes and evidence

Membership RED: `c7df89bd9b16c5a8c8f7a723f14268eff6708101`.
In a clean detached checkout, the membership and definition test files produced
13 failed and 26 passed. Failures include the absent instruction, missing case
artifact, and deliberately stale byte binding after the new tests.

The status guard is RED `e25875b`; it prevents the current definition from
reopening approved choices or claiming an implemented interpreter.

Re-entry independently found a positional-array typing defect in `fdb4972`:
the checker treated index zero as `items` despite a different `prefixItems`
schema. Core verified the review at consumer commit
`6636e886076036b18d879804d6e598fe4959a333`, tree
`f7747e6bfacbbe3e441164a54898557a4287c853`, report SHA-256
`cffe96a939968495f87e4fe0e1b84cf71989d3640d2f0cda72d39b34a66d1d9c`.
RED `8207027ffc3727b7aeeaad4a3846b37eb1f56555` retains its exact witness,
nested cases, a homogeneous positive, and the membership variant.
The clean three-file selection produced 18 failed and 27 passed before GREEN.
The mixed membership case at this RED also lacks the new instruction schema;
the original positional comparison witness independently exposes the type bug.

GREEN: `70c2374fc9fb2829c142cec807061d1860072e52`, tree
`5de1a5b4faa66746e289942d80cf0734f7b4a64d`.
The checker now accepts only declared string/list-of-string operands for
REQUIRE_MEMBER and refuses positional schemas recursively. It does not interpret
positional schemas or add a callback. The original IN comparison remains refused.

The exact combined selector in `REPORT.md`, which includes this directory,
reproduced **231 passed, zero skipped** in a clean detached checkout using the
existing configured project interpreter. The focused three-file selector is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider -c pyproject.toml \
  research/action_history_contract_freeze/programs/test_static_arrays.py \
  research/action_history_contract_freeze/programs/test_membership_definition.py \
  research/action_history_contract_freeze/test_definition.py --tb=short
```

That selector passed 45 tests after the fix. Ruff, format and aggregate diff
checks passed; the clean verification checkout remained unchanged. No installs,
network, full repository run or package rebuild were needed. This report is a
subsequent documentation-only commit.

SHA-256 at GREEN:

- instructions.schema.json: `ba6b8b04626a4511de20b4b9c3202386a6128681efea70c59d0d8aaef4820b94`
- programs/packet_validator.py: `55dd53ba75764a74477a24fccfecc27bcd2a943224e34beb6e96ddf5670cf504`
- programs/MEMBERSHIP_DECISION.md: `358e0a4d5175b8c0bcc5baaadb34f6ce519eb1b9dd842f0c0c36f33aa8b349ae`

The original packet was delivered to Malleus-semantic-reentry after Luis's
explicit sharing approval. Its prior pending-choice wording is historical.
Current definition metadata and the lifecycle map reflect both closed decisions.
The rejected old IN example remains historical evidence, not a current blocker.

## What remains and who owns it

The next authorized Core definition deliverable is complete executable JSON
programs for the lifecycle in `LIFECYCLE.md`, with static cross-record closure
and actual monitor/input binding definitions. The obligation map alone does not
satisfy it. No additional acknowledgement from a consumer is needed to do that
work. A genuinely missing operation still requires its own explicit decision.

After that definition freeze, the proposed runtime deliverable is one bounded
one-history action path: initialization, atomic context/proposal, computed TYPE
and direct-grant assessments, policy-derived decisions, eligible dispatch,
receipt and independent observation recording, and reopen/replay. It must test
stale/refused batches before dispatch eligibility and preserve domain state
through action-only events. It does not execute a domain effect itself.
That producer/interpreter/persistence implementation cut still needs separate
authorization. No public callable name or executable consumer handoff exists
for the new path yet. Robotics and Re-entry own their adapters, not this Core
implementation, and cannot infer its readiness from these static tests.

The Malleus development skill constrained this to OPTIONAL_PROFILE definitions
and CONFORMANCE_FIXTURE checks. Changed paths stay inside the isolated action
research directory. Production, ontology, shared main, paper, supplier data and
governance are unchanged. Nothing was merged or pushed. No instruction execution,
permission decision, transactional persistence, source truth, external effect,
runtime replacement or E2E action claim is made. The preceding compatibility
debt remains in `../GATE.md`.

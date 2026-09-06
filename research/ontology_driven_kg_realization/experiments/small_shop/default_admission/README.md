# Small Shop through Core's structural admission bundle

Status: contract frozen before implementation.

This is a `CONFORMANCE_FIXTURE` for the optional compiler-enabled,
state-version history path. It is not new protocol vocabulary or a new public
API. The operator approved this slice on 2026-09-06.

## Completion contract

Reuse the existing five Shop population templates and exact source bytes.
Compile the base ontology, start from empty accepted state, admit O1/X1 and
their relation, apply the existing additive ontology revision, then admit
invoices, payment settlement, B/e4 quantity 1, and B/e7 quantity 2.

Use `malleus.compiler.create_structural_history`,
`population_retention_events`, and `admit_structural_change`. The example must
not construct admission outcomes or load a fixture-specific runtime policy.
The shipped structural bundle is a selected implementation, not a universal
Malleus requirement.

The observations are nine current records, ten historical records, five
accepted changes, one contract revision, and a source trace for every record.
Reopening from the retained ledger alone must reproduce the receipt and graph.
The correction preserves every unrelated record. Fresh runs from identical
inputs must produce identical ledger and evidence bytes.

Two negative stories: a preparation made stale by a later ledger event refuses
without another write; a relation naming a nonexistent endpoint refuses before
retention or partial population. Existing lower-level tests remain in place.

## Identity and scope

The old public-population fixture remains frozen evidence. This successor
selects Core's structural bundle instead of the old fixture policy, so the
templates' contract identities must be rebound to the current compiled
contract. Retain both the template bytes and each resulting plan. Do not
rewrite source values, mappings, times, supersession rules, or old receipts.

The source-to-record mapping remains adopter-authored. Source registration
still uses explicit public anchor inputs. Structural checks do not establish
source truth, domain adequacy, epistemic acceptance, or action authorization.
This slice adds no locator resolver, time kind, Event population, general
mapping language, stable wire, cross-language claim, or Semantic Re-entry.

Ownership is this directory, one new test file, and the slice handover report.
No paper, runtime, existing Shop fixture, skill, or shared governance file is
reserved. Work starts at Core 8233b771a4f6ae8d248274fdda0185920f99421b in an
isolated worktree. Fable retains locator/time work and the shared ledger head.

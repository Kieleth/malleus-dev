# Action/history contract input gate

Status: **BLOCKED before executable contract freeze**. This is an isolated
Core-owned research audit, not a runtime change or an accepted profile.

Base: Core `2a11240556532c2b6160ac0bfa5ab1165e862fd2`, tree
`2f376922f108601d871361d9a7b53e4b5e156ad5`.
Reviewed semantic design: `7d64747bbc39495a6766e3f00c6379755d24b298`, tree
`5961c4ec600646731431a60fe5e855e0ff34adbe` in the separately owned
Semantic Re-entry design checkout. This packet does not copy or mutate it.

## Scope authorized and attempted

The relayed operator approval permits concrete contract definition for one
optional one-history action proof: separate action acceptance from KCS
acceptance, explicit initialization, an equality-to-two goal, one action
attempt and independent observation. The bounded one-consumer exception is
limited to that proof. It does not authorize an interpreter, writer, migration,
default expansion, merge, push or a general rule language.

Before freezing initialization, original-context and machine artifacts, the
record contract must have a real supported representation. Existing Assent
records must not become smaller substitute records or unchecked JSON strings.
The earliest input gate fails, so later artifact instances and implementation
identities remain absent rather than carrying invented hashes.

## Exact failure

Through the public `malleus.compiler.compile_linkml_contract`, both of these
inputs refuse:

1. Exact `ontology/assent.yaml`, root `assent`, with exact root and packaged
   LinkML types bytes.
2. [action-probe.yaml](action-probe.yaml), which imports that same closure and
   declares one neutral `LocalAction is_a ActionProposal`.

Both produce this typed diagnostic:

```text
INVALID_RANGE: https://malleus.dev/schema/assent/calendar_date has an unbound range https://w3id.org/linkml/types/date; a range binds as one of the seed scalars boolean, datetime, float, integer, string, or a class or enum declared in the closure
```

The supplier vocabulary and any proposed machine opcode are irrelevant to
this reproduction. Neither compilation reaches a validated record contract.
The neutral action is a probe only, not the eventual supplier subtype.

The existing public `OntologyRegistry` loads this same Assent/adopter import
and recognizes the concrete action and effect types. The Entity-only
[control](entity-control.yaml) compiles through the public compiler using the
same environment and root/types bytes. This localizes the failure to the
compiler's support boundary, not missing dependencies or invalid import paths.

## Root cause and consequences

`ontology/assent.yaml:1555` declares `calendar_date` with range `date`.
`src/malleus/_contract_pipeline/elaborate.py:68` declares five seed scalar
types. Its range validation at line 327 excludes this exact imported range.
Slot preparation at line 398 validates the imported closure, not only slots
used by the requested concrete action. The source identity binds all those
retained bytes, including declarations unrelated to this first action.

This is the first observed compiler incompatibility, not evidence that fixing
one scalar will make the entire Assent closure conform. After a future fix,
the same exact closure must run again. No declaration was stripped, rewritten
to string, or diverted to a fallback parser here.

The known machine gaps are also reproduced separately: its current grammar
refuses BOOLEAN, INTEGER, ARRAY and OBJECT field kinds, while its current
policy grammar refuses AUTHORIZE, BLOCK and CLARIFY outputs. Unmodified
machine and policy content load after their required canonical encoding.
These probes do not define the future machine grammar or claim that a changed
type spelling would supply an implementation.

## What is frozen, and what is not

[inputs.json](inputs.json) binds the inspected Core/design coordinates, exact
source and implementation byte digests, actual packaged types bytes and the
observed environment. It is an audit inventory, not a new protocol grammar or
a complete environment lock. Dependencies remain in the existing pyproject.

[test_contract_inputs.py](test_contract_inputs.py) executes the two real public
refusals and positive controls. It also discriminates unsupported machine
field/policy outputs. These are passing **snapshot tests of missing support**,
not GREEN action tests, executable-contract conformance, or an xfail hiding a
runtime implementation. The future positive contract must supersede this
blocked packet rather than use these refusals as completion evidence.

The closed initialization/O shapes, their instances, a compiled record
identity, the versioned action program/binding and its positive lifecycle
fixtures are **not frozen**. Neither are supplier/check producer identities.
The accepted semantic distinction between full history, KCS state, action
acceptance and original proposal context remains unchanged by this result.

## Smallest next decision

Recommendation: authorize a separate, bounded TDD compatibility slice that
lets the public compiler consume the exact Assent source closure required by
the selected action records, preserving the existing range/record semantics.
Its first acceptance tests are these two actual imports, then validation of
the selected structured action/assessment records. If another unsupported
semantic feature appears, surface it rather than widening support silently.
This audit does not authorize that implementation.

An alternative is an explicitly designed, lossless record-contract projection
of the required Assent closure. That is another mechanism and needs its own
authority/coverage decision. This task did not choose it. Hand-copying a
smaller ontology, using the registry as an invisible compiler substitute or
pretending a future compiled digest exists are not acceptable resolutions.

Once the record-contract input is resolved, resume the already approved
contract definition, freeze the finite typed instruction/operand and context
grammars, and only then request the action runtime RED-to-GREEN slice.
No additional action semantics are needed to explain this blocker.

## Public integration signature proposal, not an API selection

The smallest prospective persistence surface remains a method on the existing
`KnowledgeChangeHistory`, taking an explicit expected full ledger head/count
and a nonempty ordered tuple of canonical event drafts. Each draft has the
existing input fields `event_id`, `event_type`, `transaction_time`, `actor_id`
and `payload`. Replay supplies actual coordinates and validates every record
under the selected profile before a failure-atomic append. The return is the
existing `KnowledgeHistoryReplay`; no new KCS, writer object or second log.

A possible spelling for discussion is `history.append_protocol_events(...)`.
It is not implemented, exported or frozen. Record/source registration stays
with the selected retention contract; any registration needed by a batch must
be explicit. Batch/retention composition must be resolved in the executable
binding before this signature can be accepted. No opaque callback is proposed.

## Reproduce this input audit

From this isolated checkout with the project's configured development
environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider research/action_history_contract_freeze/test_contract_inputs.py
```

The test reads committed source files and installed dependency resources. It
does not write a ledger, import research test helpers, invoke a supplier effect
or contact a server. Source inputs remain byte-identical after each refusal.

Recorded checks:

- Input-audit file alone: 15 passed, no skips or xfails.
- Input audit plus `tests/test_assent_ontology.py` and
  `tests/contract_compiler/pareto/test_public_compiler.py`: 67 passed, no skips
  or xfails. These verify existing boundaries, not the future composition.
- Changed-file Ruff, format and Markdown parse checks passed.

The combined command is the command above with those two test paths appended.
No full-repository, package, release or new action-runtime gate was run.

An initial audit-helper positive control incorrectly supplied pretty-printed
resource bytes to a constructor requiring canonical JSON. It was corrected
to use canonical encoding. Two hard guards now distinguish resource bytes
from canonical artifact bytes. No Core behavior was changed for this mistake.

## Non-claims

No executable action profile, approved wire, portable interpreter, composed
Assent/KCS runtime, external effect, authority legitimacy, supplier fact,
source truth, repeat safety or complete replay law is demonstrated here. No
existing default, source, ontology, public symbol, package or governance ledger
changed. No paper file or other task's worktree was edited.

# OCR evidence-integrity conformance, v0

Capability: `AUDIT_ONLY`. Decisions: `design/OCR_EVIDENCE_INTEGRITY_DECISIONS.md`.

`profile.json` is a generated projection of the diagnostics registry in
`malleus.ocr.verify`. Do not edit it; run `conformance/ocr/v0/generate.py`.
`tests/test_ocr.py` fails when the two disagree.

Seven cases ship inside the package, at `malleus/ocr/cases/`. An adopter with
only the wheel runs them:

```text
malleus-ocr --conformance
malleus-ocr path/to/their-bundle.json
```

They are the wiring check: four documents that must be accepted, three that
must be refused, because a verifier that refuses nothing is indistinguishable
from one that is not running. Their `expect` lists are checked against the live
verifier on every test run, so a case that stops meaning what it says fails
rather than drifts.

Each case also fixes its census, unit by unit, as `expect_units`: the outcome
and the disposition that outcome carries. Cases used to state only whether the
bundle was complete, which is one bit, and one bit cannot distinguish a unit
nobody fetched from a unit whose only call failed. Four cases were green while
a reviewer's `ABSENT` was being reported `READ`.

Two of the seven exist for that distinction. `absence-is-not-a-reading` holds a
unit a reviewer states is not present in the source: an answer, so the unit is
accounted for, and not a reading, so the census must not say `READ`.
`silence-is-not-success` claims `FINISHED_READING`, raises no diagnostic, and
is not complete: one unit was rendered and its only call failed, one was never
fetched, and the suite requires those to report `CHECK_FAILED` and
`NOT_CHECKED` rather than one word for both. Paperwork that holds together is
not a reading.

`refuses-conflicting-review` is the other side of `absence-is-not-a-reading`,
and reading them together is the point. Both hold a unit a reviewer calls
`ABSENT` while the bundle carries a rendering of it, a region on it and a
reading of those pixels. That shape is not a contradiction: `ABSENT` is reached
through a region, so the reading is the evidence the reviewer disowns. The
second case adds a different reviewer answering the same region
`VERIFIED_BLANK`, and that is refused as `OCR-D016`, because the census reports
one outcome per unit and either choice converts the other reviewer's answer.
Two regions of one unit may still answer differently; two regions are two
subjects and the unit takes the worst of them, in the order published as
`unit_verdict_precedence`. Decision C9 carries the reasoning.

That case is also the reminder that the two answers are separate: it is refused
and its census is complete. A complete census is not a clean seal.

The exhaustive cases live in `tests/test_ocr.py`, one negative per diagnostic,
plus the currency matrix for decision C7. A diagnostic with no negative case
is a claim the profile cannot support, and a test enforces that too. Those
test the verifier; the packaged seven test an adopter's emitter.

Everything here is invented. No production document, credential, network
dependency or adopter fixture is present, and none may be added: an adopter's
real document is a private fixture that stays in the adopter.

## What an adapter must do to conform

Emit a bundle whose objects carry the identity planes declared in
`ontology/domains/ocr.yaml`, then pass `verify_bundle` with zero diagnostics.
The schema is the authority: every plane is a typed record under a root
primitive, and a record that violates it is refused as `OCR-D013` before any
other check runs. The dataclasses in `malleus.ocr.bundle` are one carrier for
those records and not the contract; an adapter in another language conforms by
emitting records the schema accepts.

The adapter keeps its own OCR stack, engine, renderer and provider. This
profile verifies evidence; it does not perform recognition and never selects an
engine.

Two adopters were audited while designing this profile. Neither has yet run
this suite, so the profile is designed from evidence and is not yet proven
portable by a real adapter. That claim waits on the first one to pass.

What is established: a document emitter that imports no plane class and knows
nothing about Python dataclasses crosses the boundary and conforms
(`test_an_emitter_that_never_touches_the_carrier_conforms`). That is a
deliberately different implementation of the emitter role, not proof that a
production OCR stack will fit.

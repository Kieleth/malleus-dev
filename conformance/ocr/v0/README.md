# OCR evidence-integrity conformance, v0

Capability: `AUDIT_ONLY`. Decisions: `design/OCR_EVIDENCE_INTEGRITY_DECISIONS.md`.

`profile.json` is a generated projection of the diagnostics registry in
`malleus.ocr.verify`. Do not edit it; run `scripts/gen_ocr_conformance.py`.
`tests/test_ocr.py` fails when the two disagree.

The executable cases live in `tests/test_ocr.py`, one negative per diagnostic,
plus the currency matrix for decision C7. A diagnostic with no negative case
is a claim the profile cannot support, and a test enforces that too.

Everything here is invented. No production document, credential, network
dependency or adopter fixture is present, and none may be added: an adopter's
real document is a private fixture that stays in the adopter.

## What an adapter must do to conform

Emit a bundle whose objects carry the identity planes in
`malleus.ocr.bundle`, then pass `verify_bundle` with zero diagnostics. The
adapter keeps its own OCR stack, engine, renderer and provider. This profile
verifies evidence; it does not perform recognition and never selects an engine.

Two adopters were audited while designing this profile. Neither has yet run
this suite, so the profile is designed from evidence and is not yet proven
portable. That claim waits on the first adapter to pass.

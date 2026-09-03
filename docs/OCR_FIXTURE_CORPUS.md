# OCR fixture corpus

The fixture corpus turns OCR's abstract bundle rules into concrete files. It
lives at `conformance/ocr/v0/corpus/` and contains three deterministic,
self-authored cases licensed Apache-2.0:

| Case | What it anchors |
| --- | --- |
| `region-control` | One source with multiple regions. Its two mutations prove that an attempt, hypothesis, and selection cannot cross region identities. |
| `multipage-control` | A complete document with ordered required units and an exact correspondence between each embedded PDF page image, retained raster, fixed response, and selected text. |
| `incomplete-sequence` | A two-physical-page source labelled logical pages 1 and 3 while its declared inventory requires pages 1, 2, and 3. It anchors a source-sequence gap and the difference between integrity conformance and coverage completion. It does not model OCR skipping a physical page present in the source. |

These are repository fixtures, not claims about production OCR quality. The
PDF cases are raster-only and the reference reader returns fixed readings. It
does not invoke a recognition engine. The source bytes, page rasters, requests,
responses, selected text, bundle, oracle, and verification result are separate
artifacts. Digests bind the retained source, raster, request, response, and text
bytes where the bundle has digest fields. IDs bind their semantic
relationships. For each PDF page, tests decode its sole embedded image and
require pixel identity with the corresponding retained PNG. This is an exact
fixture correspondence, not proof that an external renderer derived the PNG
from the PDF.

## Layout and authority

`corpus.json` declares the cases, their artifact paths, the Malleus and
ontology versions used to produce the reference results, and the CPython,
Pillow, PNG, pypdf, ReportLab, and zlib generator contract.
`checksums.json`
closes every retained case artifact plus `corpus.json` with byte lengths and
SHA-256 digests. `README.md` and `generate.py` are authored control files
outside that checksum set. The generated `checksums.json` excludes itself to
avoid a recursive identity. These are the only explicit exceptions. Unlisted
retained files, duplicate paths, and listed files that do not exist are errors.

Each case contains:

- `source/`: the exact source bytes. These remain the source identity.
- `rasters/`: retained PNG counterparts to source images or embedded PDF page
  images. The manifest path is bound to one exact raster ID and logical unit.
  PNG dimensions are checked from each file's IHDR chunk. PDF page images are
  decoded and compared with their retained PNGs pixel for pixel.
- `requests/`, `responses/`, and `selected/`: retained sidecars. Their bytes,
  not parsed or normalized variants, determine the digests recorded by the OCR
  bundle.
- `bundle.json`: the portable `malleus.ocr.evidence_integrity` document.
- `oracle.json`: the expected conformance bit, completeness bit, diagnostics,
  unit census, coverage metrics, and retained artifact paths.
- `verification.json`: the result frozen when the corpus was generated. Tests
  recompute the result and require it to match both this file and the oracle.

The corpus also retains four mutations and their expected verification
results:

- `hypothesis-attempt-cross-region` must be refused with `OCR-D003`.
- `selection-hypothesis-cross-region` must be refused with `OCR-D003`.
- `correction-text-digest-mismatch` must be refused with `OCR-D015`.
- `observed-without-raster` remains structurally conforming, but the asserted
  unit must remain `NOT_RENDERED` rather than becoming a reading.

The two cross-region mutations change identity references only. They do not
remove records, so their refusal proves the region-alignment rule rather than a
simpler missing-reference rule.

## Core source projection

For every case, the source representation in `bundle.json` must equal the
digest, byte length, media type, and locator computed from the retained source
file. Tests also pass the same bytes through
`malleus.source.source_artifact_fields`. The resulting core projection must
preserve all four source facts exactly. Its additional `artifact_hash` is the
core record identity, not a replacement for the source content digest.

## Enforced behavior and pending decisions

The corpus asserts behavior already implemented by the v0 verifier:

- exact artifact digests and byte lengths;
- exact raster path, ID, logical unit, dimensions, and PDF-page pixel identity;
- resolvable source, raster, region, attempt, hypothesis, and selection paths;
- agreement between declared required units and the oracle census;
- retained request, response, and selected-text byte identity;
- agreement among the reference-reader declaration, request and response
  contracts, response outcome, attempt configuration, and any human verdict;
- absence of local absolute paths, credential-bearing JSON keys, PNG metadata,
  and undeclared or active PDF metadata;
- refusal of attempt-to-hypothesis and selection-to-hypothesis region changes;
- separation of integrity conformance from coverage completion, including the
  exact two-physical-page, three-logical-unit source-sequence case.

Four matters remain contract decisions. The corpus records no expected
behavior for them, and the test suite does not hide them behind `xfail`:

- **Selector-profile governance.** A region declares a selector profile, but
  v0 has no registry or profile-specific selector validator.
- **Ingest-time ordering.** A source class must carry `frozen_at`, but v0 does
  not prove that the declaration preceded ingest.
- **C2 claim dependencies.** The OCR bundle has no dependency-closed model for
  partial downstream claims.
- **Actor and reviewer identity.** `reviewer_id` is retained, but v0 does not
  establish actor registration, reviewer independence, or authority.

Adding an executable expectation for one of these subjects requires a profile
decision, a diagnostic contract, and a negative fixture. Until then, they stay
explicitly outside what this corpus proves.

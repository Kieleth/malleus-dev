# OCR fixture corpus

This corpus grounds the OCR evidence profile in small, self-authored documents.
It contains no production document, copied text, credential, network response, or
private research material. The generated source documents are contributions to
this repository under its Apache-2.0 license. Every source oracle states that
origin and license explicitly.

The retained responses come from `malleus.fixture.control_reader@1`. That reader
is a deterministic fixture producer, not a production OCR engine. It returns
fixed readings or a fixed controlled failure for self-authored regions so tests
can inspect the evidence boundary without depending on a provider, model,
network, or native OCR stack.

The five cases separate different questions:

* `region-control` has two visible regions in one PNG. Its mutations cross the
  attempt and selection lineage between the regions.
* `multipage-control` is a two-page raster-only PDF. The first page contains
  known text and an intentionally ambiguous token. The second page is blank.
  Its bundle retains the machine-shaped reading and the human correction. The
  blank-page review revises `UNREADABLE` to `VERIFIED_BLANK` through an explicit
  predecessor edge, retaining both review records.
* `incomplete-sequence` is a raster-only PDF containing visible logical pages
  1 of 3 and 3 of 3. Logical page 2 is absent from the source and the evidence
  census remains incomplete.
* `failed-attempt` retains a request and controlled failure response over one
  rasterized region. The attempt remains `FAILED / CHECK_FAILED`, and no
  hypothesis, selection, or selected text is invented. Its `retry-succeeds`
  variant appends a completed attempt and first reading while retaining the
  failed attempt byte-for-byte.
* `unavailable-attempt` retains the intended request and the reason the call
  could not start. It carries no response artifact or digest, and removing the
  reason triggers `OCR-D015`.

`generate.py` owns every file below `cases/`, plus `corpus.json` and
`checksums.json`. It writes invariant PDF metadata, fixed timestamps, canonical
JSON, and deterministic PNG bytes. It refuses undeclared files under its owned
paths. The manifest pins the Malleus version, both ontology byte hashes, and the
OCR registry content hash used for verification. `checksums.json` covers every
generated file except itself, avoiding a self-referential digest.

Run `python conformance/ocr/v0/corpus/generate.py check` to regenerate the
corpus in memory and compare every byte with the retained artifacts. Run the
same command without `check` to write the declared artifacts.

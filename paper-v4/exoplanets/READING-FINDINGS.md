# Reading investigation: preserve meaning before capture

2026-09-14. Preparation result, not an approved reading or a model experiment.

Forward correction, EXO-009: [READING-RCA.md](READING-RCA.md) supersedes the
causal interpretation and source-narrowing recommendation below. The PDFs render
legibly; isolated tests recover missing labels and mathematical glyphs from
retained source data. One supposedly missing label was a ligature false alarm.
The original comparison and its limitations remain recorded here, not rewritten.

## Outcome

Changing extractor is not a complete repair. Pypdf preserves a solar-unit
symbol that Poppler loses; Poppler recovers figure labels that pypdf loses.
Both expose broken equation characters in the later paper. The exact NASA
table conversion is unchanged and remains usable source preparation.

Four methods were run over both complete PDFs: pypdf 6.16.2 plain/layout and
Poppler 26.03.0 default/layout. This accounts for all 53 pages in each method,
212 extracted page surfaces. It is not 212 pages of independent evidence or a
full visual audit. Visual inspection covered the earlier page 6 and Table B.3,
and the later Table D1 and equation pages 19, 22, 23 and 25. Page text alone
was screened everywhere. No reading was selected.

| Observed problem | Evidence and cause | Consequence |
| --- | --- | --- |
| Earlier page 6 loses figure text in pypdf plain | The page invokes 14,396 Form XObjects, with 11 distinct forms. Pypdf's plain extractor stops after 5,000 form invocations and records that further content was skipped. | This output cannot support claims based on missing labels. |
| Layout mode also loses those labels | Four visual probes fail on page 6, even though that page emits no warning in layout mode. | A quiet extractor is not a completeness check. |
| Poppler loses the solar-unit symbol in Table B.3 | The rendered table and pypdf preserve the symbol. The embedded `txsy` font has neither a ToUnicode map nor explicit Encoding. Poppler's tested output omits the symbol. | Better figure extraction does not imply better units. No silent whole-document replacement. |
| Later equations contain control characters | All methods expose such characters on pages 19, 22, 23 and 25. The CMEX10 ToUnicode map inspected on page 19 omits codes used for delimiters, including 0x12/0x13. The rendered equations have visible delimiters. | These linear strings are not a verified mathematical transcription. |

The font findings explain why correct rendering and defective text can coexist.
We inspected source font dictionaries/maps and extractor code; we did not repair
the maps or establish which PDF producer introduced them. Pypdf's layout path
was observed to lose labels; its internal cause was not separately established.
No claim is made that the two extraction modes fail through the same mechanism.

Other spot checks did not supply a clean replacement. The existing bundled
PDFium 5.13.0 recovered page-6 signs/labels but inserted control characters at
some line breaks. Pdfplumber 0.11.9 exposed unmapped character IDs and interleaved
columns. These were narrow diagnostic reads, not complete comparisons or selected
dependencies. We did not install or modify either package.

## What the tests now prevent

`reading_audit.py` checks source binding, exact page accounting, extractor
diagnostics, suspicious/control characters and visually established text probes.
Probe text stays in the private investigator workspace, not a producer prompt.
The source check removes whitespace only for comparison; it never rewrites the
retained text, supplies a missing symbol or changes a number.

Known losses and diagnostics block the screen. An unfamiliar private-use glyph
alone requires review, not a declaration that information is missing. Even a
screen with no findings returns `CHECKS_PASS_REVIEW_REQUIRED`, never launch
approval. Marker presence does not establish table-cell association, equation
structure, reading order or whole-source completeness.

The first investigation mislabeled every flagged private-use math glyph as a
defect. A failing regression then separated review-needed glyphs from confirmed
control characters and missing probes. Both reports are retained. All 212 page
strings and warnings are identical between them; the correction is to our audit,
not an improvement in extraction. Every final method still has a real failing
check. The later parameter table passes its five probes in all four methods;
that positive control does not erase losses on other pages.

The local suite now has 74 passing tests, including 21 reading-audit tests.
The report publisher also refuses overwrite and exposes no final file after
a failed staging write. No Core, shared-paper or package gate was run.

## Decision proposed, not taken

Keep the first experiment about scientific prose plus exact published parameter
rows, not recovering all mathematics and graphics from PDFs. Prepare one pinned
text reading with explicit unresolved regions; use the already verified archive
rows and their own unit definitions for exact-data inputs. Original page images
remain available for source review. Missing figure labels and damaged equations
must not become model-invented facts or silently repaired text.

This narrows the capture claim. It does not authorize dropping inconvenient
scientific conclusions, supplying evaluator-authored facts, or calling the
reading complete. Before adopting it, identify affected regions and which claims
cannot be supported from the delivered text. Where the experiment genuinely
needs a damaged region, choose an explicitly governed additional reading surface
or leave that requirement unresolved. A full visual-reading route is an
alternative requiring a separate acquisition/evidence decision, not an implicit
fallback. No answer questions, model execution or record population is approved.

Separately, Core confirms that the mixed-profile probe does not establish profile
compatibility. The next history decision should consider one explicit composition
profile and any smallest generic change needed for the document producer to bind
it honestly. The current adapter's source-assertion profile must not be relabeled.
No Core implementation request has been dispatched.

## Reproduction and limits

Private workspace: `private/paper-v4-exoplanets-lhs1140-01/`.
`reading-probes-v1.json` contains 14 source-bound visual checks, nine earlier and
five later. `reading-investigation-v1.json` is the retained first audit;
`reading-investigation-v2.json` is the corrected audit and full extracted output.
Its SHA-256 is `4a05200d6057932c8b1e7554a5a28de3ac3656676faa24ecac6859dff6d62eef`.
The report binds source identities, page-text hashes, probes, Python version,
extractor versions, Poppler executable hash and both audit implementation hashes.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python paper-v4/exoplanets/inspect_pdf_readings.py --pdftotext /opt/homebrew/bin/pdftotext --output <new-private-result.json>
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider paper-v4/exoplanets
```

`reading-audit-tools.json` declares the local diagnostic requirements. Pypdf is
already a pinned research dependency. Poppler is an existing inspection tool,
not a new project runtime dependency or a clean-install recipe. Exact executable
identity does not freeze its dynamic libraries. A reproducible clean execution
environment still has to be selected before an experiment uses an extractor.
This investigation cannot authorize that environment by reporting local success.
